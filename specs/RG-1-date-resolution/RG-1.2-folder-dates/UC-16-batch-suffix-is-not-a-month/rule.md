# UC-16 — An unpadded digit after the year is a disc number, not a month

| Field | Value |
|---|---|
| Group | `RG-1.2 Dates carried by folder names` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-03` |
| Legacy findings | — |

## Rule

A folder named `YYYY-N`, where `N` is a single unpadded digit `1`–`9` and there
is no further date material, is **not** read as month `N` of that year. It is
treated as a batch or disc index, and the folder resolves to the **year** alone,
at year precision.

## Why

When a year's photographs are burned across several CDs, the folders get named
`2006-1`, `2006-2`, `2006-3` — disc one, disc two, disc three. `2006-2` is
byte-for-byte a valid `YYYY-M`, and reading it as February files ten other
months' worth of pictures into February 2006.

The reference archive has exactly this: sibling folders `2006-1` and `2006-2`
side by side, each holding a full year's spread of events. The tell is the
missing zero-padding — a tool or a person writing a real month writes `2006-02`;
`2006-2` is how you number a sequence you are counting by hand.

This is an **assumed exclusion**: YAIT deliberately does not interpret `2006-N` as
a month. It keeps the year, which is solid, and lets the file's name or a deeper
folder supply the rest if they can.

## Scope

This rule refuses one specific shape. Zero-padded `YYYY-MM` *is* a month
(`UC-13`). A numeric `YYYY-MM` in a *filename* is `UC-11`. Which dated folder
wins once a folder does carry a date is `UC-14`.

## Counter-examples

- `2006-02` — zero-padded; this is February 2006, month precision (`UC-13`).
- `2006-2-15` — a day follows; this is a full date, `2006-02-15` (`UC-13`).
- `2006-10` — two digits, a plausible month; read as October, not a batch index.
- `Disc 2` beside `2006` — no `YYYY-N` shape; the year is read from the sibling
  segment and `Disc 2` is ignored, which is this rule's spirit already.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   "YYYY-N" with an unpadded single digit is how hand-numbered disc
             sets are labelled. Reading it as a month collapses a whole year
             into one wrong month. Zero-padding is the signal that separates a
             real month from a batch index.
Fallback:    The folder resolves to the year only, at year precision. The month
             and day, if any, come from the filename or a deeper folder.
Revisit if:  An archive appears that uses unpadded "YYYY-N" folders to mean real
             months. That would turn the scenario below red: the folder would
             have to resolve to "2006-02" at month precision, and this rule
             folder would be deleted in favour of an enforced YYYY-N month rule.
Supersedes:  —
```

## Example

`files/2006-2/family new year 025.jpg`, with a sibling `files/2006-1/scan
001.jpg` so the disc-set shape is visible in the corpus. The inspected file
carries no metadata and its name has no date, so `2006-2` is the only candidate.
The scenario asserts the **fallback**: year `2006`, year precision — not
`2006-02`, and not "no date".

Proven by [`rule.feature`](rule.feature).
