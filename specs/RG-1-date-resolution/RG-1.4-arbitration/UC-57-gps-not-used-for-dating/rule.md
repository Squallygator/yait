# UC-57 — GPS metadata is never used to resolve a capture date

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

The GPS block of an image's Exif — the coordinates, and the `GPSDateStamp` /
`GPSTimeStamp` fields — is **not** a date source. When `DateTimeOriginal` and the
other capture-date tags (`UC-17`) are absent, the GPS timestamp is not used as a
substitute: resolution falls to the filename and folder as for any dateless
still (`UC-18`).

## Why

`GPSDateStamp` is the time of the satellite fix, in UTC. It is not the shutter
time: the fix can be minutes to hours stale, it can be absent while the photo is
otherwise fine, and being UTC it can name a different calendar day than the one
the photograph was taken on. It is precise-looking and quietly wrong — the same
trap as an epoch stamp (`UC-09`).

Coordinates are for *place*, and place is not time. Using them to look up a
timezone and shift the wall clock is a related mistake, refused separately in
`UC-60`.

This is an **assumed exclusion**: the GPS block is recognised (YAIT can read it
for display and for `RG-5` metadata work) but is struck from the date-source
list on purpose.

## Scope

GPS as a **date** source. Keeping the wall-clock time as written, with no
timezone conversion from coordinates, is `UC-60`. The ordinary capture-date tags
are `UC-17`; the fall to name then folder when they are absent is `UC-18`.

## Counter-examples

- An image with a valid `DateTimeOriginal` and a GPS block — the capture tag
  answers; GPS was never in contention.
- An image with GPS coordinates but no `GPSDateStamp` — nothing changes; GPS
  still contributes no date.
- A GPS track log (`.gpx`) beside a photo — a different artefact; correlating
  photos to a track is out of scope entirely.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   GPSDateStamp is the UTC fix time, not the shutter time — stale,
             often absent, and able to name a different calendar day. Precise-
             looking and wrong, like an epoch stamp. Coordinates are place, not
             time.
Fallback:    With no capture-date tag, the date comes from the filename, then
             the folder (UC-18). The GPS block contributes nothing.
Revisit if:  A camera or workflow is found where GPSDateStamp is reliably the
             capture instant and is the only date present often enough to matter
             — then this scenario goes red and an enforced GPS-date rule
             replaces it.
Supersedes:  —
```

## Example

`files/2013-07 Sicily/DSCN2043.JPG` — no capture-date Exif, a filename with no
date, a `2013-07` folder. The scenario asserts the resolved date is `2013-07`,
month precision, from `folder-name`, and **not** from `embedded-metadata`.

> Sample-fidelity note: the sample generator cannot yet write a GPS IFD, so this
> example is the degenerate case — a still with no metadata at all — and is
> observationally the same as `UC-18`. What makes `UC-57` a distinct rule is the
> `## Why`: a *present* `GPSDateStamp` must still be ignored. Tightening the
> example (a real GPS block, `GPSDateStamp` a day off, asserting it is not read)
> needs a small generator addition and is tracked as a follow-up.

Proven by [`rule.feature`](rule.feature).
