# UC-54 — RAW files are not opened to read their capture date

| Field | Value |
|---|---|
| Group | `RG-1.3 Dates read from the file's content` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-04` |
| Legacy findings | — |

## Rule

Files with a camera-RAW extension — `.CR2`, `.CR3`, `.NEF`, `.NRW`, `.ARW`,
`.RAF`, `.ORF`, `.RW2`, `.DNG` — are **not** parsed for an embedded capture date.
Their date is resolved from the filename and the folder only, exactly as for a
still with no metadata.

## Why

Reading the Exif inside a RAW file reliably means a RAW library — `rawpy` /
LibRaw, or a full ExifTool — because each vendor's container is its own format
and the TIFF-like ones hide the real `DateTimeOriginal` in a maker note. That is
a new runtime dependency, and runtime dependencies are frozen: adding one needs
an ADR merged first.

The cost of not doing it is low. In every collection seen so far, a RAW file
sits directly beside its out-of-camera JPEG and inside a dated folder — the
photographer who shoots RAW also files carefully. The name and folder answer.

This is an **assumed exclusion**: YAIT deliberately treats a RAW file as opaque
for dating. It does not fail on it and does not skip it — it just resolves the
date the same way it would for any file whose bytes it does not read.

## Scope

RAW stills only. HEIC is the neighbouring exclusion `UC-55`, for the same
dependency reason. Ordinary JPEG/TIFF Exif reading is `UC-17`. What a file with
no readable content date does next — fall to name, then folder — is `UC-18`.

## Counter-examples

- `.DNG` written by a phone that also embeds a standard JPEG preview with Exif —
  still not inspected; the extension decides, not the internal layout.
- A `.CR2` renamed to `.jpg` — read as a JPEG (`UC-17`); classification is by
  extension and this is the user mislabelling the file.
- A RAW file with a full date in its name (`2016-05-14 ...`) — resolves from the
  name; this rule is why the name is consulted at all.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Reliable RAW date extraction needs a RAW library or ExifTool — a
             new frozen-list dependency, ADR-gated. RAW files in practice sit
             beside a dated JPEG in a dated folder, so name and folder suffice.
Fallback:    The date is resolved from the filename, then the folder, as for any
             file whose content is not read (UC-18). No error, no skip.
Revisit if:  A collection appears with RAW files in undated folders and
             uninformative names, making the embedded date the only source — at
             which point an ADR for a RAW reader is on the table, this scenario
             goes red, and the rule folder is replaced by an enforced RAW rule.
Supersedes:  —
```

## Example

`files/2016-05 Iceland/IMG_8801.CR2` carries a real `DateTimeOriginal` of
`2016-05-14 07:12:00`, but sits in a folder dated `2016-05`. The scenario
asserts the **fallback**: `2016-05` at month precision, from `folder-name` — so
an implementation that simply opens the file and reads the Exif (its bytes are a
readable JPEG) produces a different, day-precision answer and fails.

Proven by [`rule.feature`](rule.feature).
