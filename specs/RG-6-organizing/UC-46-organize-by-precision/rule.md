# UC-46 — Placement follows the precision of the resolved date

| Field | Value |
|---|---|
| Group | `RG-6 Organizing` |
| Status | `Enforced` ▶ |
| Legacy findings | — |
| Stories | `US-05-01` |

## Rule

In the `YYYY/MM` layout, a file is placed according to how precisely its date
is known:

- day or month precision → `YYYY/MM/`
- year precision → `YYYY/`
- no date → `_undated/`

A file known only to the year is never given a month folder. The three
branches are one rule — "the tree is only as deep as the date is certain" — not
three.

## Why

The partial dates are deliberate: `2009` means the month is unknown, not
"January" (`specs/README.md`). Placement has to carry that honesty through. If
a year-only file were dropped into `2009/01/` it would sit among photos
genuinely known to be January, and the distinction the partial date preserved
would be silently lost the moment the file moved.

`_undated/` rather than a guessed year keeps the "we don't know" pile visible
and reviewable instead of scattering it into arbitrary folders.

## Scope

This rule decides the *destination folder* from the date's precision. It does
not decide the date or its precision — that is `RG-1`. It does not decide the
*name* the file carries into that folder — `RG-3`. The flat/`_undated` special
case when the layout is flatten, not `YYYY/MM`, is `UC-47`.

## Counter-examples

- Day precision and month precision land in the *same* place, `YYYY/MM/` — the
  extra day precision shows in the name (`RG-3`), not the folder depth.
- A file dated `2009-00` — there is no such thing; a month is either known
  (`2009-06`) or not (`2009`). Precision is one of day/month/year/none.
- An `unreadable` or `junk` file — not organised by this rule at all; it goes
  to the recycle area (`RG-2`, `RG-7`).

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   Partial dates mean "unknown", not "01". Placing a year-only file
             in YYYY/MM/ would mix it with photos genuinely known to that
             month and destroy the distinction the partial date kept.
Fallback:    n/a
Revisit if:  Users ask for a flat YYYY/ tree regardless of precision — that is
             a layout option, not a change to this rule.
Supersedes:  —
```

## Example

Three files in the `YYYY/MM` layout:
`files/2011-06-14 rando/a.jpg` (Exif `2011-06-14`, day) → `2011/06/`;
`files/2009 albums/b.jpg` (folder `2009`, year) → `2009/`;
`files/sans date/c.jpg` (no date anywhere) → `_undated/`. An implementation
that pads year precision to `2009/01/`, or that guesses a year for the undated
file, fails the scenario.

Proven by [`rule.feature`](rule.feature).
