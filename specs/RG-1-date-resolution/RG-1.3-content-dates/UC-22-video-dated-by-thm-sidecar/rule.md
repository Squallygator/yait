# UC-22 — A .THM thumbnail dates its video

| Field | Value |
|---|---|
| Group | `RG-1.3 Dates read from the file's content` |
| Status | `Enforced` ▶ |
| Stories | `US-03-04` |
| Legacy findings | `#6` |

## Rule

When a video has no usable date in its own container, and a file with the same
stem and a `.THM` extension sits beside it, the `.THM` is a JPEG thumbnail: its
Exif capture date is read and used as the video's date, with `sidecar` as the
source.

## Why

Canon and other camcorders wrote a companion `.THM` for every clip — a tiny
JPEG preview carrying full Exif, including `DateTimeOriginal`. On old AVI clips
whose `IDIT` chunk is missing or corrupt, that thumbnail is the only surviving
record of when the video was shot.

This is one half of finding `#6`. In `dvd-tools` the code that read dates and the
code that cleaned up "junk" disagreed about `.THM` files: one wanted the date
from it, the other deleted it as clutter — and depending on order, the video
either got its date or lost its only source. Splitting the concern into two
rules that cite each other is the fix: this rule takes the date, `UC-38` keeps
the file alive.

## Scope

This rule reads the date **from** the sidecar and attributes it to the video.
That a `.THM` must survive the junk filter as long as its video exists is the
twin rule `UC-38` in `RG-2`. When the video's own container *does* carry a date,
that wins and the sidecar is not consulted (`UC-20`, `UC-21`). Matching a
sidecar to its media by stem is also used for other companion types elsewhere.

## Counter-examples

- The video's `IDIT` or `mvhd` holds a valid date — the container wins; the
  `.THM` is not read for dating (but is still kept, `UC-38`).
- A `.THM` with no matching video stem — an orphan; it is not used to date
  anything and its own classification is `RG-2`'s problem.
- A `.THM` that is not a readable JPEG — yields no date; the video stays
  dateless and resolution continues.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   A camcorder .THM is a full-Exif JPEG and is often the only date
             left for an AVI whose IDIT is gone. Reading it here, and keeping it
             alive in UC-38, resolves the dvd-tools contradiction (finding #6)
             where the two behaviours raced.
Fallback:    n/a
Revisit if:  A sidecar type appears whose date should *not* propagate to its
             media (e.g. an edit-side thumbnail regenerated years later).
Supersedes:  —
```

## Example

`files/CANON/MVI_2468.AVI` — a real RIFF/AVI whose `IDIT` chunk holds the
non-date string `"unknown"`, so the container yields nothing — beside
`files/CANON/MVI_2468.THM`, a JPEG carrying `DateTimeOriginal = 2005-12-25
16:30:00`. Inspecting the **video** must resolve to `2005-12-25` from the
`sidecar`. The folder names no date, so a wrong implementation that ignores the
sidecar gets no date at all.

Proven by [`rule.feature`](rule.feature).
