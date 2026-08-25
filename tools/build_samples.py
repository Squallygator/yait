#!/usr/bin/env python3
"""Build the sample corpus under ``specs/`` from ``samples.toml`` recipes.

Every rule directory (``specs/RG-*/RG-*/UC-*/``) may carry a ``samples.toml``
recipe describing the example files a rule needs. This tool reads every
recipe, and produces two kinds of example file:

- images derived from the seed photograph (``specs/_seed/river.jpg``), with
  EXIF injected as described by the recipe;
- artefacts a photograph cannot produce — videos, archives, damaged and junk
  files — forged byte by byte, with no encoder and no third-party content.

It writes every sample under that rule's ``files/`` directory, and writes the
consolidated manifest ``specs/.manifest.json``.

The generator is deterministic: two runs against the same recipes and the
same Pillow version produce the same manifest. It is not byte-for-byte
stable across Pillow versions (the JPEG encoder changes), which is why
``--check`` compares the manifest rather than file contents.

Usage::

    python tools/build_samples.py
    python tools/build_samples.py --check

Requires Pillow: see requirements-dev.txt.
"""

from __future__ import annotations

import argparse
import io
import json
import logging
import shutil
import sys
import tempfile
import tomllib
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from PIL import Image

logger = logging.getLogger("build_samples")

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS_ROOT = REPO_ROOT / "specs"
SEED_PATH = SPECS_ROOT / "_seed" / "river.jpg"
MANIFEST_PATH = SPECS_ROOT / ".manifest.json"
MANIFEST_VERSION = 1

DEFAULT_WIDTH = 320
DEFAULT_QUALITY = 70

RECIPE_FILENAME = "samples.toml"
SUPPORTED_RECIPE_VERSION = 1
TOP_LEVEL_FIELDS = frozenset({"version", "files"})
COMMON_FILE_FIELDS = frozenset({"path", "source"})
IMAGE_FILE_FIELDS = COMMON_FILE_FIELDS | {"width", "quality", "exif"}
FORGE_FILE_FIELDS = COMMON_FILE_FIELDS | {"kind", "params"}

RECIPE_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# QuickTime's `mvhd` epoch is 1904-01-01, not the Unix epoch — mixing the two
# up is the classic mistake and misdates every decoded timestamp by 66 years.
_QT_EPOCH = datetime(1904, 1, 1, tzinfo=timezone.utc)
_UNIX_EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)
QT_EPOCH_OFFSET_SECONDS = int((_UNIX_EPOCH - _QT_EPOCH).total_seconds())


class RecipeError(ValueError):
    """A ``samples.toml`` recipe does not respect the schema this generator understands."""


class ExifFieldName(str, Enum):
    """The only EXIF tags this generator knows how to inject.

    A rule needing another tag adds it here, deliberately: an unrecognised
    name in a recipe is a typo, not a request for a new capability.
    """

    ORIENTATION = "Orientation"
    DATE_TIME_ORIGINAL = "DateTimeOriginal"
    DATE_TIME_DIGITIZED = "DateTimeDigitized"


class ForgeKind(str, Enum):
    """The forged artefact shapes this generator can build, byte by byte."""

    RIFF_IDIT = "riff-idit"
    MP4_MVHD = "mp4-mvhd"
    ZIP = "zip"
    TRUNCATED_JPEG = "truncated-jpeg"
    EMPTY = "empty"
    BYTES = "bytes"


def parse_recipe_datetime(value: object, context: str) -> datetime:
    if not isinstance(value, str):
        raise RecipeError(f"{context} must be a string, got {value!r}")
    try:
        return datetime.strptime(value, RECIPE_DATETIME_FORMAT)
    except ValueError as exc:
        raise RecipeError(f"{context}: {value!r} is not '{RECIPE_DATETIME_FORMAT}'") from exc


def _encode_orientation(value: object, field_name: ExifFieldName) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise RecipeError(f"exif.{field_name.value} must be an integer, got {value!r}")
    return value


def _encode_exif_datetime(value: object, field_name: ExifFieldName) -> str:
    parsed = parse_recipe_datetime(value, f"exif.{field_name.value}")
    return parsed.strftime("%Y:%m:%d %H:%M:%S")


@dataclass(frozen=True)
class ExifField:
    """Where one EXIF tag lives and how to turn a recipe value into wire form."""

    tag_id: int
    in_exif_ifd: bool
    encode: Callable[[object, ExifFieldName], int | str]


def _build_exif_field_table() -> dict[ExifFieldName, ExifField]:
    from PIL import ExifTags

    return {
        ExifFieldName.ORIENTATION: ExifField(
            tag_id=int(ExifTags.Base.Orientation), in_exif_ifd=False, encode=_encode_orientation
        ),
        ExifFieldName.DATE_TIME_ORIGINAL: ExifField(
            tag_id=int(ExifTags.Base.DateTimeOriginal), in_exif_ifd=True, encode=_encode_exif_datetime
        ),
        ExifFieldName.DATE_TIME_DIGITIZED: ExifField(
            tag_id=int(ExifTags.Base.DateTimeDigitized), in_exif_ifd=True, encode=_encode_exif_datetime
        ),
    }


# --- recipe entries ---------------------------------------------------------


@dataclass(frozen=True)
class ImageSample:
    """One ``files[]`` entry with ``source = "seed"``, already validated."""

    relative_path: str
    width: int
    quality: int
    exif: dict[ExifFieldName, object]


@dataclass(frozen=True)
class RiffIditParams:
    idit: str

    def to_manifest(self) -> dict[str, object]:
        return {"idit": self.idit}


@dataclass(frozen=True)
class Mp4MvhdParams:
    created: datetime

    def to_manifest(self) -> dict[str, object]:
        return {"created": self.created.strftime(RECIPE_DATETIME_FORMAT)}


@dataclass(frozen=True)
class ZipEntry:
    name: str
    exif: dict[ExifFieldName, object]


@dataclass(frozen=True)
class ZipParams:
    entries: tuple[ZipEntry, ...]

    def to_manifest(self) -> dict[str, object]:
        return {
            "entries": [
                {"name": entry.name, "exif": {name.value: value for name, value in sorted(entry.exif.items())}}
                for entry in self.entries
            ]
        }


@dataclass(frozen=True)
class TruncatedJpegParams:
    keep_bytes: int

    def to_manifest(self) -> dict[str, object]:
        return {"keep_bytes": self.keep_bytes}


@dataclass(frozen=True)
class EmptyParams:
    def to_manifest(self) -> dict[str, object]:
        return {}


@dataclass(frozen=True)
class BytesParams:
    content: str

    def to_manifest(self) -> dict[str, object]:
        return {"content": self.content}


ForgeParams = RiffIditParams | Mp4MvhdParams | ZipParams | TruncatedJpegParams | EmptyParams | BytesParams


@dataclass(frozen=True)
class ForgeSample:
    """One ``files[]`` entry with ``source = "forge"``, already validated."""

    relative_path: str
    kind: ForgeKind
    params: ForgeParams


Sample = ImageSample | ForgeSample


@dataclass(frozen=True)
class Recipe:
    output_dir: Path
    samples: list[Sample]


def find_recipes(specs_root: Path) -> list[Path]:
    return sorted(
        path
        for path in specs_root.rglob(RECIPE_FILENAME)
        if "_templates" not in path.relative_to(specs_root).parts
    )


def load_recipe(recipe_path: Path) -> Recipe:
    with recipe_path.open("rb") as handle:
        try:
            data = tomllib.load(handle)
        except tomllib.TOMLDecodeError as exc:
            raise RecipeError(f"{recipe_path}: invalid TOML: {exc}") from exc

    unknown_top = set(data) - TOP_LEVEL_FIELDS
    if unknown_top:
        raise RecipeError(f"{recipe_path}: unknown top-level field(s): {sorted(unknown_top)}")

    version = data.get("version")
    if version != SUPPORTED_RECIPE_VERSION:
        raise RecipeError(f"{recipe_path}: unsupported recipe version {version!r}, expected {SUPPORTED_RECIPE_VERSION}")

    files = data.get("files")
    if not isinstance(files, list) or not files:
        raise RecipeError(f"{recipe_path}: 'files' must be a non-empty array of tables")

    output_dir = recipe_path.parent / "files"
    samples = [_load_file_entry(recipe_path, index, entry) for index, entry in enumerate(files)]
    return Recipe(output_dir=output_dir, samples=samples)


def _load_file_entry(recipe_path: Path, index: int, entry: object) -> Sample:
    if not isinstance(entry, dict):
        raise RecipeError(f"{recipe_path}: files[{index}] must be a table")

    path = entry.get("path")
    if not isinstance(path, str) or not path:
        raise RecipeError(f"{recipe_path}: files[{index}].path is required and must be a non-empty string")

    source = entry.get("source")
    if source == "seed":
        return _load_image_entry(recipe_path, index, entry, path)
    if source == "forge":
        return _load_forge_entry(recipe_path, index, entry, path)
    raise RecipeError(f"{recipe_path}: files[{index}].source={source!r} must be 'seed' or 'forge'")


def _load_exif_table(recipe_path: Path, index: int, raw_exif: object) -> dict[ExifFieldName, object]:
    if not isinstance(raw_exif, dict):
        raise RecipeError(f"{recipe_path}: files[{index}].exif must be a table")

    exif: dict[ExifFieldName, object] = {}
    for name, value in raw_exif.items():
        try:
            field_name = ExifFieldName(name)
        except ValueError:
            supported = sorted(field.value for field in ExifFieldName)
            raise RecipeError(
                f"{recipe_path}: files[{index}].exif has unknown tag {name!r}, supported: {supported}"
            ) from None
        exif[field_name] = value
    return exif


def _load_image_entry(recipe_path: Path, index: int, entry: dict[str, object], path: str) -> ImageSample:
    unknown = set(entry) - IMAGE_FILE_FIELDS
    if unknown:
        raise RecipeError(f"{recipe_path}: files[{index}] has unknown field(s): {sorted(unknown)}")

    width = entry.get("width", DEFAULT_WIDTH)
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
        raise RecipeError(f"{recipe_path}: files[{index}].width must be a positive integer")

    quality = entry.get("quality", DEFAULT_QUALITY)
    if not isinstance(quality, int) or isinstance(quality, bool) or not (1 <= quality <= 100):
        raise RecipeError(f"{recipe_path}: files[{index}].quality must be an integer between 1 and 100")

    exif = _load_exif_table(recipe_path, index, entry.get("exif", {}))
    return ImageSample(relative_path=path, width=width, quality=quality, exif=exif)


def _load_forge_entry(recipe_path: Path, index: int, entry: dict[str, object], path: str) -> ForgeSample:
    unknown = set(entry) - FORGE_FILE_FIELDS
    if unknown:
        raise RecipeError(f"{recipe_path}: files[{index}] has unknown field(s): {sorted(unknown)}")

    supported_kinds = sorted(kind.value for kind in ForgeKind)
    raw_kind = entry.get("kind")
    if raw_kind is None:
        raise RecipeError(f"{recipe_path}: files[{index}].kind is required, expected one of {supported_kinds}")
    try:
        kind = ForgeKind(raw_kind)
    except ValueError:
        raise RecipeError(
            f"{recipe_path}: files[{index}].kind={raw_kind!r} is not supported, expected one of {supported_kinds}"
        ) from None

    raw_params = entry.get("params", {})
    if not isinstance(raw_params, dict):
        raise RecipeError(f"{recipe_path}: files[{index}].params must be a table")

    params = _FORGE_PARAM_LOADERS[kind](recipe_path, index, raw_params)
    return ForgeSample(relative_path=path, kind=kind, params=params)


def _load_riff_idit_params(recipe_path: Path, index: int, raw: dict[str, object]) -> ForgeParams:
    unknown = set(raw) - {"idit"}
    if unknown:
        raise RecipeError(f"{recipe_path}: files[{index}].params has unknown field(s): {sorted(unknown)}")
    idit = raw.get("idit")
    if not isinstance(idit, str) or not idit:
        raise RecipeError(f"{recipe_path}: files[{index}].params.idit is required and must be a non-empty string")
    return RiffIditParams(idit=idit)


def _load_mp4_mvhd_params(recipe_path: Path, index: int, raw: dict[str, object]) -> ForgeParams:
    unknown = set(raw) - {"created"}
    if unknown:
        raise RecipeError(f"{recipe_path}: files[{index}].params has unknown field(s): {sorted(unknown)}")
    created = parse_recipe_datetime(raw.get("created"), f"{recipe_path}: files[{index}].params.created")
    return Mp4MvhdParams(created=created)


def _load_zip_params(recipe_path: Path, index: int, raw: dict[str, object]) -> ForgeParams:
    unknown = set(raw) - {"entries"}
    if unknown:
        raise RecipeError(f"{recipe_path}: files[{index}].params has unknown field(s): {sorted(unknown)}")

    raw_entries = raw.get("entries")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise RecipeError(f"{recipe_path}: files[{index}].params.entries must be a non-empty array of tables")

    entries: list[ZipEntry] = []
    for entry_index, raw_entry in enumerate(raw_entries):
        if not isinstance(raw_entry, dict):
            raise RecipeError(f"{recipe_path}: files[{index}].params.entries[{entry_index}] must be a table")
        unknown_entry = set(raw_entry) - {"name", "exif"}
        if unknown_entry:
            raise RecipeError(
                f"{recipe_path}: files[{index}].params.entries[{entry_index}] has unknown field(s): "
                f"{sorted(unknown_entry)}"
            )
        name = raw_entry.get("name")
        if not isinstance(name, str) or not name:
            raise RecipeError(
                f"{recipe_path}: files[{index}].params.entries[{entry_index}].name is required "
                "and must be a non-empty string"
            )
        exif = _load_exif_table(recipe_path, index, raw_entry.get("exif", {}))
        if ExifFieldName.DATE_TIME_ORIGINAL not in exif:
            raise RecipeError(
                f"{recipe_path}: files[{index}].params.entries[{entry_index}] needs "
                "exif.DateTimeOriginal to set a distinct archive entry timestamp"
            )
        entries.append(ZipEntry(name=name, exif=exif))
    return ZipParams(entries=tuple(entries))


def _load_truncated_jpeg_params(recipe_path: Path, index: int, raw: dict[str, object]) -> ForgeParams:
    unknown = set(raw) - {"keep_bytes"}
    if unknown:
        raise RecipeError(f"{recipe_path}: files[{index}].params has unknown field(s): {sorted(unknown)}")
    keep_bytes = raw.get("keep_bytes")
    if not isinstance(keep_bytes, int) or isinstance(keep_bytes, bool) or keep_bytes <= 0:
        raise RecipeError(f"{recipe_path}: files[{index}].params.keep_bytes must be a positive integer")
    return TruncatedJpegParams(keep_bytes=keep_bytes)


def _load_empty_params(recipe_path: Path, index: int, raw: dict[str, object]) -> ForgeParams:
    if raw:
        raise RecipeError(f"{recipe_path}: files[{index}].params must be empty for kind 'empty'")
    return EmptyParams()


def _load_bytes_params(recipe_path: Path, index: int, raw: dict[str, object]) -> ForgeParams:
    unknown = set(raw) - {"content"}
    if unknown:
        raise RecipeError(f"{recipe_path}: files[{index}].params has unknown field(s): {sorted(unknown)}")
    content = raw.get("content")
    if not isinstance(content, str):
        raise RecipeError(f"{recipe_path}: files[{index}].params.content is required and must be a string")
    return BytesParams(content=content)


_FORGE_PARAM_LOADERS: dict[ForgeKind, Callable[[Path, int, dict[str, object]], ForgeParams]] = {
    ForgeKind.RIFF_IDIT: _load_riff_idit_params,
    ForgeKind.MP4_MVHD: _load_mp4_mvhd_params,
    ForgeKind.ZIP: _load_zip_params,
    ForgeKind.TRUNCATED_JPEG: _load_truncated_jpeg_params,
    ForgeKind.EMPTY: _load_empty_params,
    ForgeKind.BYTES: _load_bytes_params,
}


# --- image derivation --------------------------------------------------------


def build_exif_bytes(exif: dict[ExifFieldName, object], exif_field_table: dict[ExifFieldName, ExifField]) -> bytes | None:
    if not exif:
        return None

    from PIL import Image, ExifTags

    container = Image.Exif()
    exif_ifd = container.get_ifd(ExifTags.IFD.Exif)
    for field_name, raw_value in exif.items():
        field = exif_field_table[field_name]
        value = field.encode(raw_value, field_name)
        target = exif_ifd if field.in_exif_ifd else container
        target[field.tag_id] = value
    return container.tobytes()


def derive_image(
    seed: Image.Image,
    width: int,
    quality: int,
    exif: dict[ExifFieldName, object],
    exif_field_table: dict[ExifFieldName, ExifField],
) -> tuple[bytes, int, int]:
    from PIL import Image

    ratio = width / seed.width
    height = max(1, round(seed.height * ratio))
    resized = seed.resize((width, height), Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    save_kwargs: dict[str, object] = {"quality": quality}
    exif_bytes = build_exif_bytes(exif, exif_field_table)
    if exif_bytes is not None:
        save_kwargs["exif"] = exif_bytes
    resized.save(buffer, format="JPEG", **save_kwargs)
    return buffer.getvalue(), width, height


# --- byte-level forging -------------------------------------------------------


def _pad_even(data: bytes) -> bytes:
    return data if len(data) % 2 == 0 else data + b"\x00"


def _riff_chunk(four_cc: bytes, data: bytes) -> bytes:
    return four_cc + len(data).to_bytes(4, "little") + _pad_even(data)


def build_riff_idit(idit: str) -> bytes:
    """A minimal AVI: RIFF/AVI header, an ``hdrl`` list, and the ``IDIT`` chunk.

    Only chunk presence and the date string are under test here, never stream
    decoding, so ``avih`` carries zeroed placeholder fields.
    """
    avih_chunk = _riff_chunk(b"avih", b"\x00" * 56)
    idit_chunk = _riff_chunk(b"IDIT", idit.encode("ascii") + b"\x00")
    hdrl_list = _riff_chunk(b"LIST", b"hdrl" + avih_chunk + idit_chunk)
    payload = b"AVI " + hdrl_list
    return b"RIFF" + len(payload).to_bytes(4, "little") + payload


def _mp4_box(box_type: bytes, payload: bytes) -> bytes:
    return (len(payload) + 8).to_bytes(4, "big") + box_type + payload


def _build_mvhd(timestamp: int) -> bytes:
    payload = b"\x00\x00\x00\x00"  # version 0, flags 0
    payload += timestamp.to_bytes(4, "big")  # creation_time
    payload += timestamp.to_bytes(4, "big")  # modification_time
    payload += (1000).to_bytes(4, "big")  # timescale
    payload += (0).to_bytes(4, "big")  # duration
    payload += (0x00010000).to_bytes(4, "big")  # rate, 1.0
    payload += (0x0100).to_bytes(2, "big")  # volume, 1.0
    payload += b"\x00" * 10  # reserved
    for value in (0x00010000, 0, 0, 0, 0x00010000, 0, 0, 0, 0x40000000):  # identity matrix
        payload += value.to_bytes(4, "big")
    payload += b"\x00" * 24  # pre_defined
    payload += (1).to_bytes(4, "big")  # next_track_ID
    return _mp4_box(b"mvhd", payload)


def build_mp4_mvhd(created: datetime) -> bytes:
    """A minimal MP4/MOV: ``ftyp`` plus a ``moov`` box carrying ``mvhd`` v0."""
    timestamp = int(created.replace(tzinfo=timezone.utc).timestamp()) + QT_EPOCH_OFFSET_SECONDS
    ftyp = _mp4_box(b"ftyp", b"isom" + (0).to_bytes(4, "big") + b"isom" + b"mp42")
    moov = _mp4_box(b"moov", _build_mvhd(timestamp))
    return ftyp + moov


def build_zip(seed: Image.Image, params: ZipParams, exif_field_table: dict[ExifFieldName, ExifField]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        for entry in params.entries:
            data, _, _ = derive_image(seed, DEFAULT_WIDTH, DEFAULT_QUALITY, entry.exif, exif_field_table)
            captured = entry.exif[ExifFieldName.DATE_TIME_ORIGINAL]
            parsed = parse_recipe_datetime(captured, f"zip entry {entry.name!r} exif.DateTimeOriginal")
            try:
                info = zipfile.ZipInfo(
                    entry.name,
                    date_time=(parsed.year, parsed.month, parsed.day, parsed.hour, parsed.minute, parsed.second),
                )
            except ValueError as exc:
                raise RecipeError(f"zip entry {entry.name!r}: {exc}") from exc
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, data)
    return buffer.getvalue()


def build_truncated_jpeg(
    seed: Image.Image, params: TruncatedJpegParams, exif_field_table: dict[ExifFieldName, ExifField]
) -> bytes:
    data, _, _ = derive_image(seed, DEFAULT_WIDTH, DEFAULT_QUALITY, {}, exif_field_table)
    if params.keep_bytes >= len(data):
        raise RecipeError(
            f"truncated-jpeg: keep_bytes={params.keep_bytes} is not smaller than the "
            f"{len(data)}-byte derived image, nothing would be truncated"
        )
    return data[: params.keep_bytes]


def build_forge_bytes(sample: ForgeSample, seed: Image.Image, exif_field_table: dict[ExifFieldName, ExifField]) -> bytes:
    match sample.params:
        case RiffIditParams(idit=idit):
            return build_riff_idit(idit)
        case Mp4MvhdParams(created=created):
            return build_mp4_mvhd(created)
        case ZipParams() as zip_params:
            return build_zip(seed, zip_params, exif_field_table)
        case TruncatedJpegParams() as truncated_params:
            return build_truncated_jpeg(seed, truncated_params, exif_field_table)
        case EmptyParams():
            return b""
        case BytesParams(content=content):
            return content.encode("utf-8")
    raise AssertionError(f"unhandled forge kind: {sample.kind}")


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(path)


# --- manifest ------------------------------------------------------------------


@dataclass(frozen=True)
class ImageManifestEntry:
    path: str
    width: int
    height: int
    quality: int
    exif: dict[str, object]
    size: int

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path,
            "width": self.width,
            "height": self.height,
            "quality": self.quality,
            "exif": dict(sorted(self.exif.items())),
            "size": self.size,
        }


@dataclass(frozen=True)
class ForgeManifestEntry:
    path: str
    kind: str
    params: dict[str, object]
    size: int

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path,
            "kind": self.kind,
            "params": dict(sorted(self.params.items())),
            "size": self.size,
        }


ManifestEntry = ImageManifestEntry | ForgeManifestEntry


def _manifest_int(data: dict[str, object], key: str) -> int:
    value = data[key]
    if not isinstance(value, int) or isinstance(value, bool):
        raise RecipeError(f"{MANIFEST_PATH}: {key!r} must be an integer, got {value!r}")
    return value


def _manifest_dict(data: dict[str, object], key: str) -> dict[str, object]:
    value = data[key]
    if not isinstance(value, dict):
        raise RecipeError(f"{MANIFEST_PATH}: {key!r} must be a table, got {value!r}")
    return value


def manifest_entry_from_json(data: dict[str, object]) -> ManifestEntry:
    if "kind" in data:
        return ForgeManifestEntry(
            path=str(data["path"]),
            kind=str(data["kind"]),
            params=_manifest_dict(data, "params"),
            size=_manifest_int(data, "size"),
        )
    return ImageManifestEntry(
        path=str(data["path"]),
        width=_manifest_int(data, "width"),
        height=_manifest_int(data, "height"),
        quality=_manifest_int(data, "quality"),
        exif=_manifest_dict(data, "exif"),
        size=_manifest_int(data, "size"),
    )


def generate_all(output_root: Path) -> list[ManifestEntry]:
    """Regenerate every sample under ``output_root`` and return their manifest entries.

    ``output_root`` is ``SPECS_ROOT`` for a real build, or a temporary directory
    for ``--check``: both cases share this exact code path, so a check can
    never drift from what a real run would produce.
    """
    from PIL import Image, ExifTags  # noqa: F401  (import-time dependency check)

    exif_field_table = _build_exif_field_table()

    recipe_paths = find_recipes(SPECS_ROOT)
    if not recipe_paths:
        raise RecipeError(f"no {RECIPE_FILENAME} recipe found under {SPECS_ROOT}")

    entries: list[ManifestEntry] = []
    with Image.open(SEED_PATH) as seed:
        seed.load()
        for recipe_path in recipe_paths:
            recipe = load_recipe(recipe_path)
            recipe_output_dir = output_root / recipe.output_dir.relative_to(SPECS_ROOT)
            if recipe_output_dir.exists():
                shutil.rmtree(recipe_output_dir)

            for sample in recipe.samples:
                destination = recipe_output_dir / sample.relative_path
                manifest_path = destination.relative_to(output_root).as_posix()

                if isinstance(sample, ImageSample):
                    data, width, height = derive_image(seed, sample.width, sample.quality, sample.exif, exif_field_table)
                    write_atomic(destination, data)
                    entries.append(
                        ImageManifestEntry(
                            path=manifest_path,
                            width=width,
                            height=height,
                            quality=sample.quality,
                            exif={name.value: value for name, value in sample.exif.items()},
                            size=len(data),
                        )
                    )
                    logger.info(
                        "built %s (%dx%d, quality %d, %d bytes)", manifest_path, width, height, sample.quality, len(data)
                    )
                else:
                    data = build_forge_bytes(sample, seed, exif_field_table)
                    write_atomic(destination, data)
                    entries.append(
                        ForgeManifestEntry(
                            path=manifest_path,
                            kind=sample.kind.value,
                            params=sample.params.to_manifest(),
                            size=len(data),
                        )
                    )
                    logger.info("forged %s (kind %s, %d bytes)", manifest_path, sample.kind.value, len(data))

    entries.sort(key=lambda entry: entry.path)
    return entries


def write_manifest(entries: list[ManifestEntry], manifest_path: Path) -> None:
    payload = {"version": MANIFEST_VERSION, "files": [entry.to_json() for entry in entries]}
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
    write_atomic(manifest_path, text.encode("utf-8"))


def load_manifest(manifest_path: Path) -> list[ManifestEntry]:
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [manifest_entry_from_json(item) for item in payload["files"]]


def diff_manifests(expected: list[ManifestEntry], actual: list[ManifestEntry]) -> list[str]:
    expected_by_path = {entry.path: entry for entry in expected}
    actual_by_path = {entry.path: entry for entry in actual}

    problems: list[str] = []
    for path in sorted(expected_by_path.keys() - actual_by_path.keys()):
        problems.append(f"{path}: present in specs/.manifest.json but no longer produced by any recipe")
    for path in sorted(actual_by_path.keys() - expected_by_path.keys()):
        problems.append(f"{path}: produced by a recipe but missing from specs/.manifest.json (run without --check)")
    for path in sorted(expected_by_path.keys() & actual_by_path.keys()):
        if expected_by_path[path] != actual_by_path[path]:
            problems.append(f"{path}: manifest is stale — {expected_by_path[path].to_json()} != {actual_by_path[path].to_json()}")
    return problems


def run_build() -> int:
    entries = generate_all(SPECS_ROOT)
    write_manifest(entries, MANIFEST_PATH)
    logger.info("wrote %d sample(s), manifest at %s", len(entries), MANIFEST_PATH)
    return 0


def run_check() -> int:
    if not MANIFEST_PATH.exists():
        logger.error("%s does not exist: run 'python tools/build_samples.py' first", MANIFEST_PATH)
        return 1

    expected = load_manifest(MANIFEST_PATH)
    with tempfile.TemporaryDirectory(prefix="yait-build-samples-check-") as tmp:
        actual = generate_all(Path(tmp))

    problems = diff_manifests(expected, actual)
    if problems:
        for problem in problems:
            logger.error(problem)
        return 1

    logger.info("%s matches the recipes: %d sample(s)", MANIFEST_PATH, len(expected))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify specs/.manifest.json still matches what the recipes produce, write nothing",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)

    try:
        import PIL  # noqa: F401
    except ImportError:
        logger.error("Pillow is required: pip install -r requirements-dev.txt")
        return 2

    try:
        return run_check() if args.check else run_build()
    except RecipeError as exc:
        logger.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
