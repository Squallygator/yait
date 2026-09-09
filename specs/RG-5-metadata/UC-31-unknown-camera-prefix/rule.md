# UC-31 — An unrecognised filename prefix is kept, not stripped

| Field | Value |
|---|---|
| Group | `RG-5 Metadata deduction and writing` |
| Status | `Enforced` ▶ |
| Legacy findings | — |
| Stories | `US-06-02` |

## Rule

When deducing the filename context for the label (`UC-32`), only a prefix on a
known list of camera and phone patterns is removed — `IMG_`, `IMG-`, `DSC_`,
`DSCN`, `DSCF`, `PICT`, `P` followed by seven digits, `MVI_`, `HPIM`, `SDC`,
`GOPR`, `DJI_`, and the like. A leading token that is *not* on that list is
left in the context as-is. The tool never strips "something that looks like a
camera prefix" by shape.

## Why

A generic rule — "drop a leading run of letters followed by digits" — is
tempting and wrong. It eats `SANY0032` (a Sanyo camera, not on the list) the
same way it eats `IMG_0032`, but it also eats `EXPO2000`, `CD1998`, `SET03` —
tokens that are the only thing the filename says about the photo. Once the
context is gone, the label collapses to just the folder name and every photo in
that folder gets the same caption.

Keeping an unknown token is the conservative choice: an opaque `SANY0032` in
the label is mildly ugly; an eaten `EXPO2000` is information destroyed. The
known list grows only by prefixes that have been seen and confirmed.

## Scope

This rule is the guard on *context extraction* for the label. The overall label
shape is `UC-32`. It has nothing to say about *classification* — a `SANY0032`
file is still an `image` (`RG-2`) — nor about *dating*; a camera prefix is
never a date.

## Counter-examples

- `IMG_0032.jpg` in the same folder — `IMG_` is on the list, removed; if
  nothing else remains, the context is legitimately empty and the label is the
  folder alone.
- `IMG_2003-07-14.jpg` — the `IMG_` goes, the date is handled by `RG-1`; what is
  left for context depends on `UC-39`.
- `dscn a walk in the woods.jpg` — `dscn` here is a word in a sentence, not a
  prefix token (no digits follow, there is a space); it stays.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   A shape-based prefix strip ("letters then digits") eats real
             information — EXPO2000, CD1998 — as readily as IMG_0032, and then
             every photo in a folder gets the same folder-only label. An
             explicit list keeps only confirmed camera prefixes in scope.
Fallback:    n/a
Revisit if:  Unlisted-but-real camera prefixes turn out to be so common in
             practice that a careful shape heuristic beats the list's coverage.
Supersedes:  —
```

## Example

`files/2012-06 Ouessant/SANY0032.jpg` carries no metadata; its date comes from
the folder, `2012-06`. `SANY` is not a known prefix, so the context keeps
`SANY0032` and the deduced label is `Ouessant - SANY0032`. An implementation
that strips any `[A-Za-z]{3,4}\d{3,4}` token produces the bare label
`Ouessant` and fails.

Proven by [`rule.feature`](rule.feature).
