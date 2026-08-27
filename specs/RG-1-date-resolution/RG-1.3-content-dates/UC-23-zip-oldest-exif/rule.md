# UC-23 — An archive takes the oldest date it contains

| Field | Value |
|---|---|
| Group | `RG-1.3 Dates read from the file's content` |
| Status | `Enforced` ▶ |
| Stories | `US-03-04` |
| Legacy findings | — |

## Rule

For a ZIP archive, the resolved date is the **oldest** capture date among its
directly-contained entries — read from each entry's own Exif, falling back to the
entry's stored modification time. Day precision, `embedded-metadata` as the
source.

## Why

Archives in these collections are almost always a bag of photos someone zipped
to email or to burn: "holiday-2009.zip". There is no single capture instant for
the archive, so one has to be chosen, and the oldest entry is the safest anchor —
it is the earliest moment anything inside was known to exist. Picking the newest
would let one stray screenshot, added later, drag the whole archive forward
years.

The oldest-wins choice also composes cleanly with organising: an archive sorts
next to the start of the events it holds, not after them.

## Scope

This rule covers a flat ZIP read one level deep. A ZIP entry that is *itself* an
archive is not opened — `UC-58`. Whether the archive's resolved date then loses
to a date in the archive's own filename or folder is arbitration (`UC-36`). Other
archive formats (RAR, 7z) are out of scope and would each be their own rule.

## Counter-examples

- Entries in arbitrary order — the oldest still wins; order in the central
  directory is irrelevant.
- One entry with no Exif — its stored modification time is used for that entry;
  the archive's date is still the minimum across all entries.
- A nested `inner.zip` entry holding an even older photo — not opened; it does
  not lower the archive's date (`UC-58`).
- An empty archive — no entries, no date; resolution continues to the name and
  folder.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   An archive has no single capture time. The oldest contained date is
             the earliest moment its contents demonstrably existed, and it stops
             a late addition from dragging the whole archive's date forward.
Fallback:    n/a
Revisit if:  A workflow appears where archives are incremental and the newest
             entry is the meaningful date.
Supersedes:  —
```

## Example

`files/backups/holiday-photos.zip` with three entries whose `DateTimeOriginal`
values are `2010-05-01`, `2009-12-24`, `2011-02-02` — the oldest,
`2009-12-24`, is the **middle** entry, so an implementation that takes the first,
the last, or the maximum fails. Neither the archive's name nor its folder carries
a date, so the entry dates are the only source, answering at day precision.

Proven by [`rule.feature`](rule.feature).
