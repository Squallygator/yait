#!/usr/bin/env python3
"""Build the sample corpus under ``specs/`` from ``samples.toml`` recipes.

Every rule directory (``specs/RG-*/RG-*/UC-*/``) may carry a ``samples.toml``
recipe describing the example files a rule needs. This tool reads every
recipe, derives the described images from the seed photograph
(``specs/_seed/river.jpg``), writes them under that rule's ``files/``
directory, and writes the consolidated manifest ``specs/.manifest.json``.

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
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable

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
FILE_FIELDS = frozenset({"path", "source", "width", "quality", "exif"})


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


def _encode_orientation(value: object, field: ExifFieldName) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise RecipeError(f"exif.{field.value} must be an integer, got {value!r}")
    return value


def _encode_exif_datetime(value: object, field: ExifFieldName) -> str:
    if not isinstance(value, str):
        raise RecipeError(f"exif.{field.value} must be a string, got {value!r}")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise RecipeError(
            f"exif.{field.value}: {value!r} is not 'YYYY-MM-DD HH:MM:SS'"
        ) from exc
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


@dataclass(frozen=True)
class ImageSample:
    """One ``files[]`` entry from a recipe, already validated."""

    recipe_path: Path
    output_dir: Path
    relative_path: str
    width: int
    quality: int
    exif: dict[ExifFieldName, object]


@dataclass(frozen=True)
class ManifestEntry:
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

    @staticmethod
    def from_json(data: dict[str, object]) -> "ManifestEntry":
        return ManifestEntry(
            path=str(data["path"]),
            width=int(data["width"]),
            height=int(data["height"]),
            quality=int(data["quality"]),
            exif=dict(data["exif"]),  # type: ignore[arg-type]
            size=int(data["size"]),
        )


def find_recipes(specs_root: Path) -> list[Path]:
    return sorted(
        path
        for path in specs_root.rglob(RECIPE_FILENAME)
        if "_templates" not in path.relative_to(specs_root).parts
    )


def load_recipe(recipe_path: Path) -> list[ImageSample]:
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
    return [
        _load_file_entry(recipe_path, index, entry, output_dir)
        for index, entry in enumerate(files)
    ]


def _load_file_entry(recipe_path: Path, index: int, entry: object, output_dir: Path) -> ImageSample:
    if not isinstance(entry, dict):
        raise RecipeError(f"{recipe_path}: files[{index}] must be a table")

    unknown = set(entry) - FILE_FIELDS
    if unknown:
        raise RecipeError(f"{recipe_path}: files[{index}] has unknown field(s): {sorted(unknown)}")

    path = entry.get("path")
    if not isinstance(path, str) or not path:
        raise RecipeError(f"{recipe_path}: files[{index}].path is required and must be a non-empty string")

    source = entry.get("source")
    if source != "seed":
        raise RecipeError(
            f"{recipe_path}: files[{index}].source={source!r} is not handled by this generator "
            "(forged artefacts are out of scope here, see US-00-05)"
        )

    width = entry.get("width", DEFAULT_WIDTH)
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
        raise RecipeError(f"{recipe_path}: files[{index}].width must be a positive integer")

    quality = entry.get("quality", DEFAULT_QUALITY)
    if not isinstance(quality, int) or isinstance(quality, bool) or not (1 <= quality <= 100):
        raise RecipeError(f"{recipe_path}: files[{index}].quality must be an integer between 1 and 100")

    raw_exif = entry.get("exif", {})
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

    return ImageSample(
        recipe_path=recipe_path,
        output_dir=output_dir,
        relative_path=path,
        width=width,
        quality=quality,
        exif=exif,
    )


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


def derive_image(seed: "Image.Image", sample: ImageSample, exif_field_table: dict[ExifFieldName, ExifField]) -> tuple[bytes, int, int]:
    from PIL import Image

    ratio = sample.width / seed.width
    height = max(1, round(seed.height * ratio))
    resized = seed.resize((sample.width, height), Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    save_kwargs: dict[str, object] = {"quality": sample.quality}
    exif_bytes = build_exif_bytes(sample.exif, exif_field_table)
    if exif_bytes is not None:
        save_kwargs["exif"] = exif_bytes
    resized.save(buffer, format="JPEG", **save_kwargs)
    return buffer.getvalue(), sample.width, height


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(path)


def generate_all(output_root: Path) -> list[ManifestEntry]:
    """Regenerate every sample under ``output_root`` and return their manifest entries.

    ``output_root`` is ``SPECS_ROOT`` for a real build, or a temporary directory
    for ``--check``: both cases share this exact code path, so a check can
    never drift from what a real run would produce.
    """
    from PIL import Image, ExifTags  # noqa: F401  (import-time dependency check)

    exif_field_table = _build_exif_field_table()

    recipes = find_recipes(SPECS_ROOT)
    if not recipes:
        raise RecipeError(f"no {RECIPE_FILENAME} recipe found under {SPECS_ROOT}")

    entries: list[ManifestEntry] = []
    with Image.open(SEED_PATH) as seed:
        seed.load()
        for recipe_path in recipes:
            samples = load_recipe(recipe_path)
            recipe_output_dir = output_root / recipe_path.parent.relative_to(SPECS_ROOT) / "files"
            if recipe_output_dir.exists():
                shutil.rmtree(recipe_output_dir)

            for sample in samples:
                data, width, height = derive_image(seed, sample, exif_field_table)
                destination = recipe_output_dir / sample.relative_path
                write_atomic(destination, data)

                manifest_path = destination.relative_to(output_root).as_posix()
                entries.append(
                    ManifestEntry(
                        path=manifest_path,
                        width=width,
                        height=height,
                        quality=sample.quality,
                        exif={name.value: value for name, value in sample.exif.items()},
                        size=len(data),
                    )
                )
                logger.info("built %s (%dx%d, quality %d, %d bytes)", manifest_path, width, height, sample.quality, len(data))

    entries.sort(key=lambda entry: entry.path)
    return entries


def write_manifest(entries: list[ManifestEntry], manifest_path: Path) -> None:
    payload = {"version": MANIFEST_VERSION, "files": [entry.to_json() for entry in entries]}
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
    write_atomic(manifest_path, text.encode("utf-8"))


def load_manifest(manifest_path: Path) -> list[ManifestEntry]:
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [ManifestEntry.from_json(item) for item in payload["files"]]


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
