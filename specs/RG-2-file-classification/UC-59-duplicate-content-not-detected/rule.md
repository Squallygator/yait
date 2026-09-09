# UC-59 — Identical content in two files is not detected or merged

| Field | Value |
|---|---|
| Group | `RG-2 File classification` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-06` |
| Legacy findings | — |

## Rule

Two files with byte-for-byte identical content but different names are **not**
recognised as duplicates of each other. Each is classified, dated, named and
organised on its own, exactly as if the other did not exist. The only
deduplication YAIT does is on the *target name*: if the two end up competing for
the same output name, the collision rule (`RG-4`) gives one a suffix — but both
files are kept.

## Why

Content-level deduplication is a different tool. Deciding that two files are
"the same" needs a hashing pass over every byte of every file, a policy for
which copy to keep (the one in the better-named folder? the one with richer
Exif? the older `mtime`?), and a way to record what was removed so it can be
undone. Each of those is a design with its own failure modes, and getting the
"which to keep" wrong means silently deleting the copy the operator actually
wanted.

The value is also low here. In these archives the near-duplicates are a
retouched photo beside its camera original (handled deliberately by `UC-28`) or
the same picture filed under two events — and in the second case the operator
usually *wants* both, one per event. Removing one would quietly break the album
it was filed in.

This is an **assumed exclusion**: YAIT does not look at content for duplication.
It does not fail on identical files and does not merge them — it processes each
independently, and a genuine dedup pass, if ever wanted, is a separate step run
before or after.

## Scope

This refusal is about *content* identity. Two files heading for the same
*target name* are still reconciled — that is `UC-42` (the check is
collection-wide) and `UC-27` (which one takes the clean name). A camera master
beside its retouched twin is named deliberately by `UC-28`. Nothing here stops
a future standalone dedup tool from consuming YAIT's inventory.

## Counter-examples

- Two byte-identical JPEGs, `sunset.jpg` and `sunset (copy).jpg`, in one folder
  — both kept, both named from their own stems; not merged.
- The same photo in `2007 Corsica/` and in `Best of/` — both kept; removing
  either would gut one of the two albums.
- Two files with the same *target* name but different content — reconciled by
  `RG-4`, which is a different question from this one.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   Content deduplication needs a keep/discard policy whose wrong
             answer is silent data loss, and the near-duplicates in these
             archives are usually wanted in both places. Name-level collision
             handling (RG-4) is the only merging YAIT does.
Fallback:    Each file is classified, dated, named and organised independently.
             If two land on the same target name, RG-4 suffixes one; both
             files remain.
Revisit if:  A collection appears that is mostly exact duplicates from repeated
             backups, where keeping both copies is pure waste — then a dedup
             step gets its own design, this scenario goes red (one file would
             have no target name of its own), and an enforced rule replaces
             this one.
Supersedes:  —
```

## Example

`files/2007-08 corse/sunset.jpg` and `files/2007-08 corse/sunset (copy).jpg`
are byte-for-byte identical — same seed, same size, no metadata. The scenario
asserts the **fallback**: each keeps a target name built from its own stem,
`2007-08-sunset.jpg` and `2007-08-sunset (copy).jpg`, so both survive to the
plan. An implementation that hashes content and drops one leaves that file with
no target name and fails.

Proven by [`rule.feature`](rule.feature).
