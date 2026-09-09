# UC-48 — A source folder left empty by the move is pruned, and only then counted

| Field | Value |
|---|---|
| Group | `RG-6 Organizing` |
| Status | `Enforced` ▶ |
| Legacy findings | — |
| Stories | `US-05-04` |

## Rule

After the media have been moved into the target tree, a source folder that is
now completely empty is removed, and its now-empty parents in turn, up to (not
including) the collection root. A folder is reported as pruned only once it has
actually been removed — the count reflects deletions that happened, not folders
that were candidates.

## Why

Reorganising a deep archive leaves hundreds of hollow folders behind —
`2006-1/`, `Camera Uploads/`, `New Folder (3)/` — and an operator scrolling
through them cannot tell the run finished cleanly. Pruning them is the visible
sign the move is done.

Counting only real removals matters because pruning can fail partway: a folder
still open in Explorer, a permission quirk on a network share. If the summary
says "212 folders pruned" but only 190 went, the operator trusts a number that
is wrong and stops checking. The count has to be the truth about the
filesystem.

## Scope

This rule removes folders emptied *by the move*. It does not touch a folder
that still contains anything the organiser did not move — an unknown non-media
file, a document, a sub-folder with its own contents; those stay, and so does
their folder. Where each media file goes is `UC-46`; recycling junk and
unreadable files (which is what empties some folders) is `RG-2` and `RG-7`.

## Counter-examples

- A folder holding `notes.txt` after its photos moved out — not empty, not
  pruned; `notes.txt` was never the organiser's to move.
- The collection root itself, now empty — never pruned; the root is a boundary.
- A folder that could not be removed (locked) — not counted as pruned, and
  surfaced as a warning rather than silently included.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   Hollow folders left after a reorg hide whether the run finished.
             Pruning them is the visible "done" signal — but the count must be
             actual removals, because a summary that overstates success stops
             the operator from checking.
Fallback:    n/a
Revisit if:  Users want the original folder structure kept as an archive
             alongside the new tree, making pruning an opt-out.
Supersedes:  —
```

## Example

`files/alpha/one.jpg` and `files/alpha/beta/two.jpg` both move to `2011/06/`,
leaving `alpha/beta` and then `alpha` empty — both are pruned.
`files/gamma/three.jpg` also moves out, but `files/gamma/keep.txt` remains, so
`gamma` is left in place. An implementation that prunes any folder whose media
all moved would delete `gamma` and its `keep.txt`, and fails the scenario.

Proven by [`rule.feature`](rule.feature).
