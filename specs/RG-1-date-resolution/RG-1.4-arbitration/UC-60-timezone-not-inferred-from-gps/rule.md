# UC-60 — Timestamps are kept as written; no timezone is applied

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

A capture timestamp is used exactly as written in the file. **No timezone
conversion is applied** — not to UTC, not from GPS coordinates, not from an
`OffsetTimeOriginal` tag. `2006-08-29 23:30` resolves to **29 August 2006**, and
never rolls forward to the 30th.

## Why

Family photographs are remembered in local wall-clock time. "The party was on
the 29th" — the fact that the camera's local time was UTC+2, or that a
GPS-derived timezone would nudge it, is not something anyone filing these
pictures cares about. Exif `DateTimeOriginal` has no timezone by design: it *is*
local time.

"Normalising" to UTC gains nothing and costs the near-midnight shots, which flip
to the wrong calendar day — and then to the wrong month, and the wrong folder.
The reference archive has evening photographs whose UTC-shifted date would move
them a day, and in one case a New Year's Eve shot that would jump to 1 January of
the next year.

This is an **assumed exclusion**: YAIT deliberately does not compute or apply an
offset, even when the information to do so (GPS, an offset tag) is present.

## Scope

This rule is about **not shifting** a timestamp that was read. That GPS is not a
date source at all is `UC-57`. Which timestamp is read in the first place is
`UC-17` (Exif), `UC-21` (`mvhd`, whose value is UTC but whose wall-clock date is
likewise kept as-is).

## Counter-examples

- `2006-08-29 09:30` with GPS in a UTC+2 zone — resolves to 29 August; the
  daytime time was never at risk, and no offset is applied regardless.
- An `OffsetTimeOriginal = +02:00` tag present — recorded for display, not
  applied to the resolved date.
- A video `mvhd` time of `2011-06-04 23:50` UTC — resolves to 4 June; the UTC
  origin of the field does not trigger a conversion.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Exif local time IS the answer people want. Converting to UTC (or via
             a GPS timezone) gains nothing and flips near-midnight shots to the
             wrong day, month and folder. Timestamps are kept as written.
Fallback:    The resolved date is the wall-clock calendar date from the
             timestamp, unshifted, at the timestamp's precision.
Revisit if:  A use case appears that genuinely needs UTC-normalised dates — even
             then a display-time toggle would be safer than changing what
             "resolved date" means, so this scenario stays the guard.
Supersedes:  —
```

## Example

`files/2006-08 birthday/IMG_0512.JPG` carries `DateTimeOriginal = 2006-08-29
23:30:00` — thirty minutes before midnight. The scenario asserts the resolved
date is `2006-08-29`, day precision, from `embedded-metadata`: any positive
UTC offset applied would produce `2006-08-30` and fail the test.

Proven by [`rule.feature`](rule.feature).
