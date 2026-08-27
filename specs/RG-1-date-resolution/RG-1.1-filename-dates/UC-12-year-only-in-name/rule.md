# UC-12 — A year on its own in the filename gives year precision

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

A filename whose only date material is a single four-digit year in the plausible
range — `2011 - family reunion.jpg` — yields that year, at **year** precision. No
month or day is inferred.

## Why

Some things are only known to the year: a scanned print with "2011" pencilled on
the back, an album folder someone emptied into a flat directory. The year is real
information and must not be thrown away — but neither may it be inflated. Filing
such a file as `2011-01-01` with day precision is a lie that later steps
(collision handling, organising by month) will act on.

Year precision lets `RG-3` produce `2011` and stop there.

## Scope

A lone year in a *filename*. A lone year on a *folder* is covered by the folder
rules (`UC-13` recognises the form, `UC-14` picks which folder). `YYYY-MM` is
`UC-11`; `YYYY-MM-DD` is `UC-01`. The plausible range itself is `UC-30`.

## Counter-examples

- `2011-12 reunion.jpg` — month material present; month precision, `UC-11`.
- `20110000.jpg` — not a year token, a malformed 8-digit run; nothing to read.
- `photo 1998 2011.jpg` — two years; ambiguous, this example does not cover it
  and a tie-break rule would be its own case.
- `IMG_2011.jpg` — a four-digit sequence that happens to be in range; this is the
  known soft edge of the rule, accepted as year precision.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   A lone in-range year is genuine but coarse information. Keeping it
             at year precision preserves it without fabricating a month or day
             that downstream steps would treat as exact.
Fallback:    n/a
Revisit if:  Four-digit camera sequence numbers in the plausible year range
             (IMG_2011.jpg) cause enough false year matches to need a guard.
Supersedes:  —
```

## Example

`files/albums/2011 - family reunion.jpg` — a single year, no other digits, no
metadata. The assertion is year precision, so an implementation that pads to
`2011-01-01` at day precision fails.

Proven by [`rule.feature`](rule.feature).
