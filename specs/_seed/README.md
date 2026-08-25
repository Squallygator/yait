# Seed photograph

`river.jpg` — 900 x 403, JPEG, an original photograph by the author, released
under [CC0](../LICENSE).

It is the single source of every image in the sample corpus. Rules never ship a
photograph of their own: `tools/build_samples.py` derives what each rule needs
from this one file — different dimensions, different quality, different EXIF.

## It carries no metadata, on purpose

The file as committed has **no Exif and no XMP segment**. Only the structural
APP0/JFIF marker remains.

This is not tidiness. The corpus works by re-injecting, for each rule, exactly
the fields that rule is about. A leftover `DateTimeOriginal` on the seed would
propagate into every derived sample and make tests depend on data that appears
nowhere in `samples.toml` — invisible input, unexplainable failures.

What was removed when the seed was integrated:

| Segment | Size | Contents |
|---|---|---|
| APP1 Exif | 144 B | `Orientation`, `DateTimeOriginal` and `DateTimeDigitized` (2022-07-19 12:01:05), sub-second fields |
| APP1 XMP | 434 B | `exif:DateTimeOriginal`, an Adobe packet uuid |

No GPS coordinates, no camera make, model or serial number were present — the
image had already been resized before integration.

The compressed scan was **not** re-encoded: stripping rebuilt the header
segments only, and the image data is byte-for-byte the original
(sha256 of the scan verified identical, 88 309 bytes).

## Verifying

```bash
python tools/strip_exif.py --check specs/_seed/river.jpg
```

Exits non-zero if any metadata segment reappears. This check runs in CI.
