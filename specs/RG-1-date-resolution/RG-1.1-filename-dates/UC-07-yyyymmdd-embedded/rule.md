# UC-07 — An isolated YYYYMMDD anywhere in the name is a date

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

An eight-digit run `YYYYMMDD` that stands alone in the filename — bounded by a
separator or the start or end of the name, not part of a longer run of digits —
and that forms a valid calendar date in the plausible year range, yields that
date at day precision. No device prefix is required.

## Why

Plenty of files carry a date with no recognisable device or app signature:
`20080614_beach.jpg`, `sunset-20080614.jpg`, `20080614.jpg`. A person or a
long-forgotten batch tool put the date there, and it is usually the only one
available.

The two guards are what make this safe. **Isolation**: the run must not be a
slice of something longer, or the id `received_862666160799536` would decode to a
"date" (`UC-08` makes that refusal explicit). **Validity**: `20081340` is not
June-plus-nonsense, it is not a date at all, and must be rejected rather than
coerced.

## Scope

This rule reads a bare, unprefixed run. The prefixed device forms are `UC-03`
(WhatsApp), `UC-04` (Android), `UC-05` (Screenshot), `UC-06` (Windows Phone) —
listed separately because their lifecycles differ. Long digit runs that must
*not* be read are `UC-08`; epoch seconds are `UC-09`. Priority against folders
and metadata is `UC-36`.

## Counter-examples

- `received_862666160799536.jpg` — a 15-digit id; no isolated 8-digit date
  inside it (`UC-08`).
- `20081340_note.jpg` — month 13, day 40; not a valid date, resolves to nothing
  from the name.
- `IMG_00012345.jpg` — an 8-digit sequence that is not a plausible date
  (year 0001); rejected by the year range (`UC-30`).
- `P1000820.jpg` — a Lumix sequence; only seven digits and not a date anyway.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   An unprefixed YYYYMMDD is a common hand- or batch-applied date and
             often the only one. It is only safe with two guards: the run must
             be isolated (not a slice of a longer id) and must be a real
             calendar date in range.
Fallback:    n/a
Revisit if:  A digit run that is isolated and passes the calendar check is still
             found in practice not to be a capture date often enough to matter.
Supersedes:  —
```

## Example

`files/scans/20080614_sunset_over_the_bay.jpg` — the date leads the name with no
device prefix, followed by a separator and words, no metadata. A sibling of the
`UC-08` refusal: here the run is isolated and valid, so it is read.

Proven by [`rule.feature`](rule.feature).
