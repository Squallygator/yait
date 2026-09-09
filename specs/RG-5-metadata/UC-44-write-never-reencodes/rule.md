# UC-44 — Writing metadata never re-encodes the image

| Field | Value |
|---|---|
| Group | `RG-5 Metadata deduction and writing` |
| Status | `Enforced` ▶ |
| Legacy findings | — |
| Stories | `US-06-05` |

## Rule

When YAIT writes metadata into a JPEG, only the header segments are rebuilt.
The entropy-coded scan — every byte from the start-of-scan marker to the end of
the image — is copied through verbatim. Before and after a metadata write, the
compressed image data is byte-for-byte identical.

## Why

JPEG is lossy on every save. `dvd-tools` wrote metadata by decoding the image
with Pillow and re-saving it, so each pass — a caption here, a date correction
there — ran the pixels through the encoder again and lost a little more detail.
Over a normalisation run that touches most files once, and re-runs, that is
visible generational loss on irreplaceable photographs.

The compressed scan is not metadata and there is never a reason to touch it.
`tools/strip_exif.py` already applies exactly this guarantee to the seed
photograph — split the file at start-of-scan, rebuild the header, splice the
original scan back unchanged — and the application must do the same. It is one
of the data-safety non-negotiables: *never re-encode an image*.

## Scope

This rule is about not altering pixels. *Which* fields are written is `UC-43`;
*what* they contain is `UC-32`. Doing the write atomically, through a temp file,
so a crash cannot corrupt the original is `RG-7` `UC-49`; keeping the original
header blocks so the write can be undone is `RG-7` `UC-51`.

## Counter-examples

- A file with no existing Exif segment — a segment is *added* to the header;
  the scan is still spliced back untouched.
- A progressive JPEG — same guarantee; the scan is opaque bytes to this rule
  either way.
- A non-JPEG (PNG, TIFF) — its own container's metadata is edited in place by
  the same principle: rewrite the metadata chunks, never re-compress the raster.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   JPEG re-saves are lossy. dvd-tools decoded and re-encoded to write
             metadata, losing detail on every pass over irreplaceable photos.
             The compressed scan is not metadata and is copied through verbatim.
Fallback:    n/a
Revisit if:  Never for JPEG. A future format that is cheap to fully re-serialise
             losslessly would not need the split-and-splice, but would still
             not be *re-encoded*.
Supersedes:  —
```

## Example

`files/2003-07 corse/plage.jpg` carries an Exif capture date, so it has a
header segment that a write must rebuild. After the deduced label
`corse - plage` is written to its caption fields, the bytes from start-of-scan
onward are identical to the original. An implementation that re-saves the whole
image changes those bytes and fails the scenario.

Proven by [`rule.feature`](rule.feature).
