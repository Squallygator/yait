# UC-11 — A numeric YYYY-MM in the filename gives month precision

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

A filename carrying `YYYY-MM` (or `YYYY_MM`) as an isolated token — not followed
by a `-DD` that would complete a full date — yields that year and month, at
**month** precision. A number after it is a sequence counter.

## Why

`2011-12 christmas market 08.jpg`: the person filed a month's worth of pictures
and numbered them. The `08` is the eighth photo, not the eighth of December. An
implementation that greedily reads `2011-12-08` invents a day that was never
claimed and files the picture on a specific, wrong date.

Returning month precision is the honest answer: the file belongs to December
2011, and `RG-3` will name it `2011-12` without a day.

## Scope

Numeric `YYYY-MM` in a *filename*. A French month in letters is `UC-10`. A full
`YYYY-MM-DD` at the head is `UC-01`. A folder named `2006-2` that means "disc 2"
rather than February is the exclusion `UC-16`. A bare year is `UC-12`.

## Counter-examples

- `2011-12-08 market.jpg` — a complete date; day precision, `UC-01`.
- `2011-12.jpg` — no counter; still month precision, `2011-12`.
- `2011-13 note.jpg` — month 13 is not a month; nothing to read.
- `IMG_2011-12.jpg` — the token is still isolated; month precision `2011-12`.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   "YYYY-MM <words> <nn>" is a month of pictures with a running
             number. Reading the trailing number as a day fabricates a
             precise date that nobody stated. Month precision keeps the answer
             truthful.
Fallback:    n/a
Revisit if:  A source appears where the number after YYYY-MM is reliably the day
             of month rather than a counter.
Supersedes:  —
```

## Example

`files/divers/2011-12 christmas market 08.jpg` — the `08` sits a few words after
`2011-12` and is a decoy day. No metadata. The assertion is month precision, so
an implementation that stitches `2011-12-08` fails.

Proven by [`rule.feature`](rule.feature).
