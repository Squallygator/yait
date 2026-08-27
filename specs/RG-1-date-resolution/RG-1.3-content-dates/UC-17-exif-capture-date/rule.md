# UC-17 — A still's capture date comes from Exif, DateTimeOriginal first

| Field | Value |
|---|---|
| Group | `RG-1.3 Dates read from the file's content` |
| Status | `Enforced` ▶ |
| Stories | `US-03-04` |
| Legacy findings | — |

## Rule

For a still image, the capture date is read from the Exif date tags, in this
order of preference: `DateTimeOriginal`, then `DateTimeDigitized`, then
`DateTime`. The first one present and valid is used, at day precision, with
`embedded-metadata` as its source.

## Why

`DateTimeOriginal` is the moment the shutter fired, as the camera recorded it.
It is the single most reliable date a photograph can carry — when the camera
clock was set. `DateTimeDigitized` is when the image was written to a file
(identical to `DateTimeOriginal` for a digital camera, but the scan date for a
digitised negative), and `DateTime` is the last-modified time the camera or an
editor stamped. The order is strict preference: a later tag is consulted only
because an earlier one is missing or unreadable, never to override it.

Ordering them explicitly is the point of this rule. In `dvd-tools` two code
paths disagreed about which Exif tag to trust, and a photo could resolve to two
different dates depending on which one ran.

## Scope

This rule covers **which Exif tag** and **in what order**. Whether that Exif
date then beats a filename or folder date is arbitration (`UC-36`), and whether
an Exif date wildly far from the folder date should be distrusted as clock drift
is `UC-19`. What happens when *no* Exif date is present is `UC-18`. Video
containers are `UC-20` and `UC-21`.

## Counter-examples

- Only `DateTimeDigitized` present — it is used; the absence of
  `DateTimeOriginal` is not a failure.
- `DateTimeOriginal` present but `0000:00:00 00:00:00` — invalid; fall through
  to the next tag.
- `DateTimeOriginal` in 2043 — outside the plausible range (`UC-30`); not used.
- A GPS timestamp in the Exif — not a capture-date tag; never consulted for
  dating (`UC-57`).

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   DateTimeOriginal is the shutter time; DateTimeDigitized and
             DateTime are weaker and only fill in when it is missing. A fixed
             preference order stops two code paths from trusting different tags,
             as happened in dvd-tools.
Fallback:    n/a
Revisit if:  A camera or workflow is found that populates DateTimeOriginal with
             something other than the capture instant, making the order wrong.
Supersedes:  —
```

## Example

`files/holidays/IMG_0042.JPG` carries `DateTimeOriginal = 2006-08-29 09:43:38`
and `DateTimeDigitized = 2010-01-02 14:00:00` — four years apart, so an
implementation that reads *Digitized* first, or reads whichever it finds first,
cannot pass. The filename holds no date, so metadata is the only source.

Proven by [`rule.feature`](rule.feature).
