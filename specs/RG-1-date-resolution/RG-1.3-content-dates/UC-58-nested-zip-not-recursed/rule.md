# UC-58 — Archives are read one level deep, not recursed

| Field | Value |
|---|---|
| Group | `RG-1.3 Dates read from the file's content` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-04` |
| Legacy findings | — |

## Rule

When an archive is inspected for its date (`UC-23`), only its directly-contained
entries are considered. An entry that is itself an archive is **not** opened, and
nothing inside it — no date, no deeper entry — contributes to the outer
archive's resolved date.

## Why

Nested archives in these collections are almost always packaging noise: an old
`backup.zip` swept up whole into this year's `backup.zip`, a downloaded bundle
left zipped inside a folder that was then zipped again. The inner archive's
oldest photo is not a statement about when the outer archive belongs — it is
just something that got carried along.

Recursing also opens a denial-of-service and a complexity hole (zip bombs,
unbounded depth) for a payoff that has never mattered in practice. One level is
enough to date the "bag of photos" case that archives actually are.

This is an **assumed exclusion**: YAIT stops at the first archive boundary. It
does not error on a nested archive and does not treat the outer archive as
undatable — it simply ignores the nested entry and dates the outer archive from
everything else it directly contains.

## Scope

This rule is about **depth** during archive dating. The oldest-wins choice among
the entries that *are* read is `UC-23`. Whether a nested archive, once extracted
elsewhere, gets its own date is a separate question handled per file. Archive
formats other than ZIP are out of scope entirely.

## Counter-examples

- A ZIP containing only images — fully read; this rule never engages (`UC-23`).
- A ZIP whose only old date is inside a nested `old.zip` — that date is not
  used; the outer archive is dated by its shallow entries, and may end up with a
  more recent date than its deepest contents.
- A nested archive that is empty or corrupt — same outcome as any nested
  archive: ignored, no error.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Nested archives are packaging noise, not a date signal, and
             recursing invites zip-bomb and unbounded-depth problems for a
             payoff never seen in practice. One level dates the bag-of-photos
             case that archives really are.
Fallback:    The outer archive is dated by the oldest date among its directly-
             contained, non-archive entries (UC-23). A nested-archive entry
             contributes nothing.
Revisit if:  A real collection is found whose meaningful dates live only inside
             nested archives — then this scenario goes red and a bounded-depth
             recursion rule replaces it.
Supersedes:  —
```

## Example

`files/backups/2012-full-backup.zip` contains two datable images
(`DateTimeOriginal` `2012-07-10` and `2012-07-11`) and a third entry named
`old-stuff.zip` standing in for a nested archive, whose own stored date is
`2001-01-01`. The scenario asserts the outer archive resolves to `2012-07-10` —
the oldest *readable image* — proving the `2001` nested entry was skipped, not
counted.

> Sample-fidelity note: the generator builds one archive level, so
> `old-stuff.zip` is a seed-derived entry with that name, not a real inner ZIP.
> The rule's teeth are in the date arithmetic (a wrongly-counted `2001` entry
> changes the answer). A follow-up can add true archive nesting to the sample
> generator and tighten this example.

Proven by [`rule.feature`](rule.feature).
