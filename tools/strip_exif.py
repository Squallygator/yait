#!/usr/bin/env python3
"""Remove every metadata segment from a JPEG, without re-encoding the image.

Only the header segments are rebuilt: the compressed scan is copied byte for
byte. This is the same guarantee the application itself must offer when it
writes metadata (rule ``UC-44``), applied here to the seed photograph.

Why the seed must carry no metadata at all: the sample corpus is built by
re-injecting, for each rule, exactly the fields that rule needs. A leftover
``DateTimeOriginal`` on the seed would silently leak into every derived sample
and make the tests depend on data nobody can see in ``samples.toml``.

Usage::

    python tools/strip_exif.py specs/_seed/river.jpg
    python tools/strip_exif.py --check specs/_seed/river.jpg

Standard library only: this runs before any environment is set up.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Iterator, NamedTuple

logger = logging.getLogger("strip_exif")

SOI = b"\xff\xd8"
MARKER_SOS = 0xDA
MARKER_APP0 = 0xE0

#: Segments carrying metadata rather than image structure. APP0 (JFIF) is kept:
#: it describes pixel density and is not metadata about the photograph.
METADATA_MARKERS = frozenset(
    {
        0xE1,  # APP1  - Exif, XMP
        0xE2,  # APP2  - ICC profile, Flashpix
        0xE3,  # APP3  - Meta / Kodak
        0xEB,  # APP11 - JPEG XT / JUMBF
        0xEC,  # APP12 - Picture Info, Ducky
        0xED,  # APP13 - Photoshop IRB, IPTC
        0xEE,  # APP14 - Adobe
        0xFE,  # COM   - free-text comment
    }
)

#: Standalone markers: two bytes, no length field.
STANDALONE = frozenset({0x01, *range(0xD0, 0xD8)})


class MalformedJpegError(ValueError):
    """The file is not a JPEG we are willing to touch."""


class Segment(NamedTuple):
    """One JPEG header segment, marker byte and full bytes including the prefix."""

    marker: int
    data: bytes

    @property
    def is_metadata(self) -> bool:
        return self.marker in METADATA_MARKERS

    def describe(self) -> str:
        if self.marker == MARKER_APP0:
            return "APP0 (JFIF, kept)"
        if self.marker == 0xE1:
            payload = self.data[4:24]
            kind = "Exif" if payload.startswith(b"Exif") else "XMP" if b"ns.adobe.com" in payload else "?"
            return f"APP1 ({kind})"
        return f"marker 0x{self.marker:02X}"


def iter_header_segments(data: bytes) -> Iterator[Segment]:
    """Yield header segments up to, but excluding, the start of scan.

    Raises:
        MalformedJpegError: if the file does not start with SOI, or a segment
            length runs past the end of the buffer.
    """
    if not data.startswith(SOI):
        raise MalformedJpegError("missing SOI marker: not a JPEG")

    offset = 2
    while offset < len(data) - 1:
        if data[offset] != 0xFF:
            raise MalformedJpegError(f"expected a marker at offset {offset}")
        marker = data[offset + 1]
        if marker == MARKER_SOS:
            return
        if marker in STANDALONE:
            yield Segment(marker, data[offset : offset + 2])
            offset += 2
            continue
        if offset + 4 > len(data):
            raise MalformedJpegError(f"truncated segment header at offset {offset}")
        length = (data[offset + 2] << 8) | data[offset + 3]
        end = offset + 2 + length
        if length < 2 or end > len(data):
            raise MalformedJpegError(f"segment at offset {offset} declares an impossible length {length}")
        yield Segment(marker, data[offset:end])
        offset = end


def scan_offset(data: bytes) -> int:
    """Byte offset of the start-of-scan marker — everything after it is untouched."""
    offset = 2
    for segment in iter_header_segments(data):
        offset += len(segment.data)
    return offset


def strip(data: bytes) -> tuple[bytes, list[Segment]]:
    """Return the image without its metadata segments, and what was removed.

    The compressed scan is copied verbatim; the image is never decoded.
    """
    kept: list[bytes] = [SOI]
    removed: list[Segment] = []
    for segment in iter_header_segments(data):
        if segment.is_metadata:
            removed.append(segment)
        else:
            kept.append(segment.data)
    kept.append(data[scan_offset(data) :])
    return b"".join(kept), removed


def remaining_metadata(data: bytes) -> list[Segment]:
    return [segment for segment in iter_header_segments(data) if segment.is_metadata]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("image", type=Path, help="JPEG file to inspect or strip")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the file carries no metadata, write nothing, exit 1 if it does",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)

    try:
        original = args.image.read_bytes()
    except OSError as exc:
        logger.error("cannot read %s: %s", args.image, exc)
        return 2

    try:
        if args.check:
            leftovers = remaining_metadata(original)
            if leftovers:
                for segment in leftovers:
                    logger.error("metadata still present: %s", segment.describe())
                return 1
            logger.info("%s carries no metadata segment", args.image)
            return 0

        stripped, removed = strip(original)
    except MalformedJpegError as exc:
        logger.error("%s: %s", args.image, exc)
        return 2

    if not removed:
        logger.info("%s already carries no metadata, left untouched", args.image)
        return 0

    # The whole point of this tool: the pixels must survive untouched.
    if stripped[scan_offset(stripped) :] != original[scan_offset(original) :]:
        logger.error("internal error: the compressed scan changed, refusing to write")
        return 3

    # Written through a temporary file so an interrupted run cannot truncate
    # the only copy of the seed — the same rule the application must follow.
    temporary = args.image.with_suffix(args.image.suffix + ".tmp")
    temporary.write_bytes(stripped)
    temporary.replace(args.image)

    for segment in removed:
        logger.info("removed %s, %d bytes", segment.describe(), len(segment.data))
    logger.info("%s: %d -> %d bytes, compressed scan unchanged", args.image, len(original), len(stripped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
