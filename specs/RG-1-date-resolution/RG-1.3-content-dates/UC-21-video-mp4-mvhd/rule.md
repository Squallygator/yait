# UC-21 — An MP4/MOV's capture date comes from the moov/mvhd atom

| Field | Value |
|---|---|
| Group | `RG-1.3 Dates read from the file's content` |
| Status | `Enforced` ▶ |
| Stories | `US-03-04` |
| Legacy findings | — |

## Rule

For an MP4 or MOV file, the capture date is read from the `creation_time` field
of the `moov/mvhd` atom. That field counts seconds from the **QuickTime epoch,
1904-01-01 UTC** — not the Unix epoch. The calendar date is taken at day
precision, with `embedded-metadata` as the source.

## Why

MP4/MOV is the format of every phone and modern camera video, and `mvhd`
`creation_time` is where the capture instant lives. The atom is found by walking
the box structure from the start of the file — no decoder, no `ffprobe`
required.

The epoch is the whole reason this is a written rule. `mvhd` timestamps are
seconds since 1904, and treating them as seconds since 1970 misdates every video
by exactly 66 years — a 2011 clip becomes 1945, or a 1998 clip becomes 2064 and
is then thrown out by the year-range guard. `dvd-tools` shipped this bug. The
offset is 2 082 844 800 seconds and it is applied on the way in.

## Scope

MP4/MOV containers via `mvhd`. AVI via `IDIT` is `UC-20`. A per-track `tkhd`
time is not used — `mvhd` is the movie-level truth. A `creation_time` of 0
(unset) means the container yields no date, and resolution continues. Timezone:
the value is UTC but the wall-clock date is kept as written (`UC-60`).

## Counter-examples

- `creation_time = 0` — unset; no date from the container.
- A `mvhd` date in 1970 — almost always an unset clock that got the Unix epoch;
  outside the plausible range (`UC-30`), not used.
- An MP4 with `©day` iTunes metadata — a different field; this rule reads
  `mvhd`, and `©day` handling would be its own rule.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   mvhd/creation_time is the capture instant for MP4/MOV, readable by
             walking boxes with no decoder. Its epoch is 1904-01-01, not 1970;
             getting that wrong shifts every video by 66 years, a bug dvd-tools
             shipped.
Fallback:    n/a
Revisit if:  A camera is found that leaves mvhd at 0 but fills a usable date
             elsewhere in the container (e.g. ©day), warranting a fallback.
Supersedes:  —
```

## Example

`files/holidays/MVI_0032.MOV`, forged with `mvhd creation_time` for
`2011-06-04 18:22:00`. The folder names no date. Resolves to `2011-06-04`, day
precision — and a 1904-vs-1970 epoch mistake would land it decades away.

Proven by [`rule.feature`](rule.feature).
