# UC-55 — HEIC/HEIF files are not opened to read their capture date

| Field | Value |
|---|---|
| Group | `RG-1.3 Dates read from the file's content` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-04` |
| Legacy findings | — |

## Rule

Files with a `.HEIC` or `.HEIF` extension are **not** parsed for an embedded
capture date. Their date is resolved from the filename and the folder only, as
for a still with no readable metadata.

## Why

HEIC is an ISO-BMFF container with HEVC-coded image data. Neither Pillow (as
frozen) nor the standard library can open it; reading its Exif means
`pillow-heif` / libheif or ExifTool — a new runtime dependency, and the
dependency list is frozen pending an ADR.

The practical cost is small. HEIC only appears from modern iPhones, and those
files reach an archive through a Photos or iCloud export that names them
`IMG_1234.HEIC` inside a dated album or a `YYYY-MM` folder. The folder answers.

This is an **assumed exclusion**: a HEIC file is opaque for dating. It is not an
error and not skipped; it is dated like any file whose bytes are not read.

## Scope

HEIC/HEIF stills only. Camera RAW is the sibling exclusion `UC-54`, same
dependency reasoning. Ordinary Exif reading is `UC-17`; the fall to name then
folder is `UC-18`.

## Counter-examples

- A `.HEIC` that is actually a JPEG in disguise — classification is by
  extension; it is still not inspected here. (If renamed to `.jpg`, `UC-17`
  applies.)
- An `.avif` file — a different codec in the same container family; out of scope
  for this rule and would be its own decision.
- A HEIC with a date in its name — resolves from the name; that path exists
  because of this rule.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Opening HEIC needs libheif/pillow-heif or ExifTool — an ADR-gated
             new dependency. HEIC comes only from recent iPhones via exports
             that file it under a dated album or YYYY-MM folder, so name and
             folder suffice.
Fallback:    The date is resolved from the filename, then the folder, as for any
             file whose content is not read (UC-18). No error, no skip.
Revisit if:  HEIC starts arriving in undated folders with uninformative names,
             or Pillow gains built-in HEIC support so the dependency cost
             disappears — either turns this scenario red and replaces the rule.
Supersedes:  —
```

## Example

`files/2019-08 Algarve/IMG_2233.HEIC` carries a real `DateTimeOriginal` of
`2019-08-03 19:44:00` (the sample's bytes are a readable JPEG), but sits in a
folder dated `2019-08`. The scenario asserts the **fallback**: `2019-08` at
month precision, from `folder-name`.

Proven by [`rule.feature`](rule.feature).
