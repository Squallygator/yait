# UC-02 — Dropbox "Camera Uploads" names carry a full timestamp

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

A filename of the form `YYYY-MM-DD HH.MM.SS` — the pattern Dropbox gives every
photo it ingests through *Camera Uploads* — yields that calendar date, at day
precision.

## Why

Dropbox renames every photo it imports to the moment of capture, read from the
device at upload time, using dots as the time separator because a colon is
illegal in a Windows filename. On archives assembled from a family Dropbox this
is the single most common filename shape, and it is trustworthy: the stamp comes
from the phone's own capture time, not from whenever the file was copied.

It is listed as its own rule rather than folded into "a leading date" (`UC-01`)
because the trailing `HH.MM.SS` is distinctive and load-bearing: the dots must be
recognised as a time being discarded, not as a version suffix or an extension.
Dropbox is also a moving target — the day it changes the format, only this rule
and its example need to move.

## Scope

This rule recognises the shape and extracts the date. Whether that date then
beats a folder date or embedded metadata is `UC-36`. A leading `YYYY-MM-DD` with
no time is `UC-01`.

## Counter-examples

- `2013-08-15 12.34.56-2.jpg` — the `-2` is Dropbox's own collision suffix; the
  date is still `2013-08-15`.
- `2013-08-15.jpg` — no time component; handled as a plain leading date (`UC-01`).
- `12.34.56.jpg` — a time with no date; nothing to resolve here.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   The "YYYY-MM-DD HH.MM.SS" shape is produced only by Dropbox Camera
             Uploads, from the device capture time. It is the most frequent
             filename in family-Dropbox archives and the trailing dotted time
             must be consumed, not mistaken for a suffix.
Fallback:    n/a
Revisit if:  Dropbox changes its Camera Uploads naming scheme, or another tool
             starts emitting the same shape from a non-capture time.
Supersedes:  —
```

## Example

`files/Camera Uploads/2013-08-15 12.34.56-2.jpg` — the dotted time and the `-2`
collision suffix are both present, so a pattern that stops at the first dot or
chokes on the suffix fails. The image carries no metadata, so the name is the
only source.

Proven by [`rule.feature`](rule.feature).
