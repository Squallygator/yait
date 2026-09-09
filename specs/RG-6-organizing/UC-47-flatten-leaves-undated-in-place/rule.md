# UC-47 — Flatten leaves an undated file where it is

| Field | Value |
|---|---|
| Group | `RG-6 Organizing` |
| Status | `Assumed exclusion` ⊘ |
| Legacy findings | — |
| Stories | `US-05-02` |

## Rule

In the flatten layout — every file moved into one directory for a one-gesture
upload — a file with no resolved date is **not** moved. It stays at its
original path inside the collection. Dated files flatten as normal; undated
ones are left in their folders.

## Why

Flatten exists to produce a single pile ready to drag into a cloud album, where
the filename (`YYYY-MM-DD-...`) is the only structure left. An undated file has
no such name — it would land in the pile as `mystere.jpg` among thousands,
context-free and unfindable. The folder it came from (`scans from mum`,
`à trier`) is the last thread of context it has, and flattening would cut it.

Leaving it in place is the lesser evil: the operator sees a small residue of
undated files still in folders, which is an accurate picture — those are
exactly the files that need a human to date them before they can be filed.

This is an **assumed exclusion**: flatten deliberately does not handle undated
files. It does not error, does not invent a date, does not dump them nameless
into the flat folder — it leaves them, visibly, for review.

## Scope

This is the flatten-layout behaviour for undated files. The `YYYY/MM` layout
sends them to `_undated/` instead — that is `UC-46`, and the two layouts differ
here on purpose. Pruning the folders that flatten *does* empty is `UC-48`.

## Counter-examples

- A file dated only to the year — it *has* a resolved date, so it flattens
  normally (its name is `2009-...`); this rule is for *no* date at all.
- An `unreadable` file with no date — set aside by `RG-2` before flatten is
  reached; not left "in place" by this rule, recycled by that one.
- A dated file in the same undated file's folder — it flattens out; the folder
  may end up holding only the undated file, and that is fine.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   A flat pile is navigable only by the YYYY-MM-DD name. An undated
             file has no such name; dropped in flat it is lost among thousands.
             Its source folder is its last context, so flatten leaves it there
             for a human to date.
Fallback:    The undated file is not moved. It stays at its original path; the
             operator finds a small residue of such files still in folders,
             which is the accurate picture of what still needs dating.
Revisit if:  A flatten consumer appears that can carry folder context some
             other way (a manifest, a tag), making it safe to move undated
             files in too — then this scenario goes red (the file would no
             longer be at its original path) and an enforced rule replaces it.
Supersedes:  —
```

## Example

With the flatten layout selected, `files/2011-06 corse/plage.jpg` (Exif
`2011-06-14`) flattens to the root as `2011-06-14-plage.jpg`, while
`files/divers/mystere.jpg` (no date anywhere) **stays at**
`divers/mystere.jpg`. An implementation that moves the undated file into the
flat root fails the scenario.

Proven by [`rule.feature`](rule.feature).
