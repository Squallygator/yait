# UC-15 — A French month name in a folder gives month precision

| Field | Value |
|---|---|
| Group | `RG-1.2 Dates carried by folder names` |
| Status | `Enforced` ▶ |
| Stories | `US-03-03` |
| Legacy findings | — |

## Rule

A folder whose name contains a month written in French letters next to a
four-digit year — `22 JUILLET 2002`, `juillet 2002` — yields that year and
month, at **month** precision. Any number beside the month is not read as a day.

## Why

CDs burned in the 2000s carry folders labelled the way an envelope would be:
`JUILLET 2002`, often shouted in capitals, sometimes with a number in front. That
number is unreliable — it may be a day, but just as often it is a count of prints
or a disc index — so the rule does not gamble on it. Month precision is the
truthful answer: these pictures belong to July 2002, and `RG-3` will name them
`2002-07`.

This mirrors `UC-10`, which already treats a trailing number beside a French
month *in a filename* as a sequence rather than a day. Folders and filenames make
the same call so the corpus stays consistent.

The month name is *data*: the recogniser must know `janvier`…`décembre`, accented
or not, any case.

## Scope

A month in letters *in a folder name*. The same shape in a *filename* is `UC-10`.
Numeric folder forms are `UC-13`. Which dated folder on the path wins is `UC-14`.

## Counter-examples

- `juillet 2002` — no number at all; still month precision, `2002-07`.
- `2002-07-22` — a numeric day is present and padded; day precision, `UC-13`.
- `JUILLET` with no year — no year to anchor to; the folder carries no date.
- `mardi 2002` — `mardi` is a weekday; nothing to read.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Envelope-style folder labels ("22 JUILLET 2002") name a month, not a
             day; the leading number is unreliable. Month precision keeps the
             answer honest and matches UC-10's treatment of the same shape in
             filenames.
Fallback:    n/a
Revisit if:  A collection appears where the number beside a spelled-out month is
             consistently the day of month.
Supersedes:  —
```

## Example

`files/22 JUILLET 2002/numérisation 08.jpg` — an all-caps French month with a
leading `22` that must not become the day, and no metadata. The assertion is
month precision, so an implementation that reads `2002-07-22` fails.

Proven by [`rule.feature`](rule.feature).
