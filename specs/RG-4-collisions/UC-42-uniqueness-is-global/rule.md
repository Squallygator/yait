# UC-42 — Target-name uniqueness is checked across the whole collection

| Field | Value |
|---|---|
| Group | `RG-4 Collisions` |
| Status | `Enforced` ▶ |
| Stories | `US-04-03` |
| Legacy findings | — |

## Rule

Two files collide when they resolve to the same target name *anywhere in the
collection*, not only when they sit in the same folder. The uniqueness check
runs over the flat set of all target names; a clash between two files in
different folders is a collision and is resolved (`UC-27` decides which file
keeps the clean name, the other gets `_1`).

## Why

The end state of a normalised collection is very often a single flat folder —
`YYYY/MM` at most, sometimes one directory for a one-gesture upload to a cloud
album. Folders stop disambiguating anything. If uniqueness was only enforced
per source folder, `2006-05 disc 1/plage.jpg` and `2006-05 disc 2/plage.jpg`
would both be renamed `2006-05-14-plage.jpg`, look fine in place, and then
collide the instant they are moved together — at which point the safe move is
to *error*, and the operator is stuck.

Catching it while the plan is still being built is the only point where the
tool can add a `_1` calmly instead of refusing to proceed.

## Scope

This rule fixes the *scope* of the check — collection-wide. *Which* of two
clashing files keeps the clean name is `UC-27`. A collision that somehow
reaches execution unresolved is a defect and is handled by `UC-53` (never
overwrite). Deciding each file's date and description is `RG-1` and `RG-3`.

## Counter-examples

- Two `plage.jpg` in the same folder with different resolved dates — different
  target names, no collision.
- `2006-05 disc 1/plage.jpg` and `2007-08 corse/plage.jpg` — different dates,
  different names, no collision even though the stems match.
- Two files that only collide *after* an unrelated `_1` is added elsewhere —
  the check is run to a fixed point, so cascades are resolved too.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   Normalised collections end up flat, so per-folder uniqueness lets
             a collision hide until the files are moved together, where the
             only safe response is to error. A collection-wide check catches it
             while the plan can still add a _1.
Fallback:    n/a
Revisit if:  A layout is added that keeps source folders permanently and never
             flattens, making per-folder uniqueness sufficient for that mode.
Supersedes:  —
```

## Example

`files/2006-05 disc 1/plage.jpg` and `files/2006-05 disc 2/plage.jpg` are
identical images carrying the same Exif date `2006-05-14`. Each is alone in its
folder, so a per-folder check sees no problem; both would become
`2006-05-14-plage.jpg`. The collection-wide check finds the clash and, by
`UC-27`'s tie-break on path, gives `disc 1` the clean name and `disc 2` the
`_1`. An implementation that checks per folder leaves both on the same name and
fails the scenario.

Proven by [`rule.feature`](rule.feature).
