# UC-36 — The full source priority order

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Enforced` ▶ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

Every candidate date first passes the plausible-range gate (`UC-30`). Among the
candidates that remain, the resolved date is chosen by this order, highest
first:

1. **A leading human-typed `YYYY-MM-DD` in the filename** (`UC-01`) — a
   deliberate act of filing.
2. **An embedded content date** — Exif `DateTimeOriginal` and its fallbacks
   (`UC-17`), an AVI `IDIT` (`UC-20`), an MP4/MOV `mvhd` (`UC-21`) — *unless* the
   clock-drift guard (`UC-19`) fires against a folder date, in which case this
   candidate drops to just below the folder date (rank 5½).
3. **A sidecar date** for a video whose own container gave nothing — a `.THM`
   (`UC-22`).
4. **A device- or app-generated filename date** — Dropbox (`UC-02`), WhatsApp
   (`UC-03`), Android (`UC-04`), screenshot (`UC-05`), Windows Phone (`UC-06`),
   an isolated bare `YYYYMMDD` (`UC-07`).
5. **A folder date**, taking the deepest dated folder on the path (`UC-14`),
   whichever recognised form it is written in (`UC-13`, `UC-15`).
6. **A coarse filename date** — a French month (`UC-10`), a numeric `YYYY-MM`
   (`UC-11`), a lone year (`UC-12`).
7. **A coarse folder date** — a French month folder (`UC-15`), or the year kept
   from a disc-index folder (`UC-16`).
8. **Nothing** — the file is undated (`UC-29`). The modification time is never
   consulted (`UC-37`).

The resolved date carries the source of whichever rank won, and its precision.

## Why

The individual rules each say what *their* source yields. Something has to say
what happens when two or three of them yield different answers on the same file,
and that cannot be improvised per file — it has to be one ordered list everyone
can point at.

The shape of the list is: a deliberate human filing decision beats a machine; a
camera's own record of the shutter beats a folder someone dropped the file into;
a folder someone *named* beats a coarse, monthy guess from the filename; and a
guess beats nothing. The one twist is the clock-drift guard: a camera that
clearly never had its clock set loses to the folder, because at that point the
"camera's own record" is worthless.

`dvd-tools` had no such list. Two functions resolved dates with different
priorities and a file's date depended on which ran first.

## Scope

This rule is the ordering only. Each rank's *recognition* lives in its own rule,
cited above. The range gate is `UC-30`; the drift guard is `UC-19`; the undated
outcome is `UC-29`. Turning the resolved date into a filename is `RG-3`.

## Counter-examples

- Exif `2007-08-20` and folder `2007-08-19` — under a year apart, so the drift
  guard does not fire and the Exif date wins by rank 2.
- Leading `2007-08-20` in the name and Exif `2007-08-19` — the human date wins
  by rank 1, even though Exif is "more precise about the shutter".
- Folder `2007-08` and a French-month filename `août 2007` — the folder wins by
  rank 5 over the coarse filename date at rank 6, and both are month precision.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Conflicting sources need one ordered list, not per-file
             improvisation. Deliberate human filing > the camera's shutter
             record > a named folder > a coarse filename guess > nothing — with
             the drift guard demoting a clearly-unset camera clock below the
             folder.
Fallback:    n/a
Revisit if:  A new source is introduced (an external index, a trusted sidecar
             type) and has to be placed in the ladder, or field experience shows
             two adjacent ranks are in the wrong order.
Supersedes:  —
```

## Example

`files/2007-08-25 retour/20070815 arrivee ferry.JPG` carries
`DateTimeOriginal = 2007-08-20 14:03:22`. Three sources disagree:

| Source | Candidate | Rank |
|---|---|---|
| filename bare `YYYYMMDD` (`20070815`) | `2007-08-15` | 4 |
| Exif `DateTimeOriginal` | `2007-08-20` | 2 |
| folder `2007-08-25 retour` | `2007-08-25` | 5 |

The Exif date is 5 days from the folder date, so the drift guard stays silent
and rank 2 wins. The resolved date is `2007-08-20`, day precision, from
`embedded-metadata` — the **middle** of the three candidates, so an
implementation that takes the earliest, the latest, or the first source it
happens to check cannot pass.

Proven by [`rule.feature`](rule.feature).
