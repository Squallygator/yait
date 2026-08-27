# UC-19 — Embedded date far from the folder date is treated as clock drift

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Enforced` ▶ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

When a file carries both an embedded content date and a folder date, and the two
disagree by **more than 12 months**, the embedded date is treated as an unset or
wrong camera clock: the **folder date wins**, and the resolved source is
`folder-name`. Within 12 months, the embedded date keeps its normal precedence
(`UC-36`).

## Why

A camera whose clock was never set stamps the same wrong date on everything —
`2000-01-01`, `2008-01-01`, whatever the firmware defaults to — and it stamps it
with full Exif confidence. The folder, named by the person who burned the disc or
sorted the shoot, knows the real occasion.

The reference archive has a run of photos in a folder called `2009-06 Corsica`,
every one of them carrying `DateTimeOriginal = 2000-01-01`. Trusting the metadata
files a family holiday under the first day of the millennium. The 12-month band
is deliberately wide: real clock error (daylight saving, a few days adrift, a
timezone) stays well inside it and is left alone; a decade of drift does not.

## Scope

This rule only fires when **both** an embedded date and a folder date exist and
are far apart. It decides that the embedded date is untrustworthy *here*; it does
not change the tag preference order (`UC-17`) or the plausible-range check
(`UC-30`), which apply first. The overall ladder, including where a
drift-flagged embedded date lands, is `UC-36`.

## Counter-examples

- Exif `2009-05-30`, folder `2009-06` — under a month apart; the embedded date
  wins as usual.
- Exif `2000-01-01`, no folder date anywhere — this rule cannot fire; the
  implausible date is instead caught by the year-range guard (`UC-30`) if it is
  out of range, or kept if it is in range with nothing to contradict it.
- Exif `2009-06-15`, folder `2006-2` — the folder segment is a disc index, not a
  date (`UC-16`), so there is no folder date to compare against.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   An unset camera clock stamps a fixed wrong date on a whole shoot
             with full Exif confidence. A folder date more than a year away is
             the human-filed truth; a 12-month band leaves ordinary clock error
             untouched.
Fallback:    n/a
Revisit if:  An archive appears whose folders are dated by processing date, so a
             far-apart embedded date is the correct one and this guard inverts
             the right answer.
Supersedes:  —
```

## Example

`files/2009-06 Corsica/IMG_0007.JPG` carries `DateTimeOriginal = 2000-01-01
00:00:00`, more than nine years off the folder. The scenario asserts the folder
wins: `2009-06`, month precision, from `folder-name` — and **not** from
`embedded-metadata`.

Proven by [`rule.feature`](rule.feature).
