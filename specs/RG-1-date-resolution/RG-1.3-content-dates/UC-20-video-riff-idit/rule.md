# UC-20 — An AVI's capture date comes from its IDIT chunk

| Field | Value |
|---|---|
| Group | `RG-1.3 Dates read from the file's content` |
| Status | `Enforced` ▶ |
| Stories | `US-03-04` |
| Legacy findings | — |

## Rule

For an AVI file, the capture date is read from the RIFF `IDIT` chunk, which
cameras write as a C `asctime` string — `Tue Aug 29 09:43:38 2006`. The calendar
date is taken from it, at day precision, with `embedded-metadata` as the source.

## Why

AVI was the camcorder and compact-camera video format through the 2000s, and
`IDIT` ("digitisation time") is where those devices recorded when the clip was
shot. It is the only place: an AVI has no Exif. The chunk is read directly from
the RIFF structure — a few bytes of header walking — so no external tool is
needed, which matters because the archive must be processable on a machine with
nothing installed.

The `asctime` format is fixed-width and locale-C, so parsing it is unambiguous;
the rule names the format so a future reader knows the abbreviated English month
and weekday are expected, not a bug.

## Scope

This rule covers the AVI/`IDIT` case only. MP4 and MOV containers keep their
date in `moov/mvhd` — `UC-21`. A video with no readable embedded date that has a
`.THM` sidecar is `UC-22`. Whether a video date beats a folder date is `UC-36`.

## Counter-examples

- `IDIT` present but holding a non-date string — unreadable; the container
  yields no date and resolution continues (see `UC-22`).
- An MP4 renamed to `.avi` — not a RIFF file; this rule does not apply, the
  container is identified by its bytes, not its extension.
- The `IDIT` weekday disagreeing with the date — the date fields win; the
  weekday is not cross-checked.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   AVI carries no Exif; IDIT is where 2000s camcorders wrote the
             capture time. It is read straight from the RIFF layout with no
             external dependency, so an archive stays processable on a bare
             machine.
Fallback:    n/a
Revisit if:  A camera family is found that writes IDIT in a non-asctime format,
             needing a second parser.
Supersedes:  —
```

## Example

`files/holidays/MVI_0031.AVI`, forged byte for byte with
`IDIT = "Tue Aug 29 09:43:38 2006"`. The folder names no date, so the chunk is
the only source. Resolves to `2006-08-29`, day precision.

Proven by [`rule.feature`](rule.feature).
