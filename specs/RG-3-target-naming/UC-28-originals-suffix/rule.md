# UC-28 — A camera master in an "Originals" folder takes an -original suffix

| Field | Value |
|---|---|
| Group | `RG-3 Target naming` |
| Status | `Enforced` ▶ |
| Stories | `US-04-02` |
| Legacy findings | — |

## Rule

When a file sits in a folder named `Originals` (also `Original`, `Originaux`,
`_orig`, case-insensitive) and another file one level up shares its resolved
date and its description, the one in the `Originals` folder gets `-original`
appended to its description in the target name. The other keeps the plain name.
Both files are kept.

## Why

A common filing habit: the out-of-camera JPEG goes into an `Originals`
sub-folder, the cropped or colour-corrected version stays in the parent with
the same name. Once the tree is flattened into `YYYY/MM`, those two files
collide — same date, same description — and the generic collision rule would
give one of them a bare `_1`, which says nothing about *which* is the keeper.

`-original` is a name a human can read: it marks the untouched master, keeps
the pair together when sorted, and makes the relationship survive the flatten.

## Scope

This rule only fires when the twin actually exists one level up. A lone file in
an `Originals` folder with no matching parent file just gets the plain name.
The general case of two unrelated files racing for one target name is `RG-4`
(`UC-42`, `UC-27`). Deciding the *date* for either file is `RG-1`.

## Counter-examples

- `Originals/coastal path.jpg` with nothing named `coastal path.*` in the
  parent — plain name, no suffix.
- `Edits/coastal path.jpg` beside `coastal path.jpg` — `Edits` is not an
  originals-folder name; this rule does not fire (the two are reconciled by
  `RG-4` if they collide).
- A master and twin with *different* resolved dates — no collision, so no
  suffix needed.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   Master-in-Originals beside edited-twin is a frequent shape that
             collides on flatten. A bare _1 loses which copy is the untouched
             master; -original is a readable marker that keeps the pair
             together and survives reorganising.
Fallback:    n/a
Revisit if:  A collection uses "Originals" to mean something else (an album
             title, a scanner's output folder) often enough that the suffix
             becomes misleading.
Supersedes:  —
```

## Example

`files/Bretagne 2011/Originals/coastal path.jpg` and
`files/Bretagne 2011/coastal path.jpg` both carry Exif `2011-07-02`. The master
in `Originals/` resolves its target to `2011-07-02-coastal path-original.jpg`;
the twin in the parent resolves to `2011-07-02-coastal path.jpg`. An
implementation that ignores the `Originals` convention sends both to the same
name and has to fall back to `_1`, failing the scenario.

Proven by [`rule.feature`](rule.feature).
