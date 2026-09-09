# UC-40 — Characters Windows refuses are removed from the target name

| Field | Value |
|---|---|
| Group | `RG-3 Target naming` |
| Status | `Enforced` ▶ |
| Stories | `US-04-02` |
| Legacy findings | — |

## Rule

The target name contains none of the characters Windows forbids in a path
component — `< > : " / \ | ? *`, and control characters 0–31 — and no trailing
dot or trailing space on the description, which Windows silently strips. Each
forbidden character is removed; the runs of whitespace that removal leaves
behind are collapsed to a single space; a description that becomes empty falls
back to the original stem with only the forbidden characters taken out.

## Why

These names come from decades of scanner software, phone exports and hand
typing, and plenty carry a `:` from a timestamp, a `?` from a guessed title, or
a trailing space a person did not see. If the tool proposes such a name, the
move either fails outright or — worse — Windows accepts it and quietly renames
`report .jpg` to `report.jpg`, so the journal now records a move that did not
happen as written and undo cannot find the file.

Sanitising up front means the planned name is exactly the name on disk, which
is the whole basis for a reversible operation.

## Scope

This rule removes characters that are unsafe. Keeping the ones that are merely
unusual but valid — accented letters, `&`, parentheses — is `UC-35`, and the
two must agree on every character. Removing the date token is `UC-39`. Two
sanitised names that collide are `RG-4`.

## Counter-examples

- `Suède & Gwada (2).jpg` — every character is legal; nothing is removed
  (`UC-35`).
- `holiday...jpg` (dots inside the stem) — interior dots are legal and kept;
  only a *trailing* dot on the description is stripped.
- A name that is only forbidden characters — the description falls back to the
  stem minus those characters, it does not become blank.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   A proposed name containing a character Windows rejects either
             fails the move or is silently rewritten on write, breaking the
             journal's record and undo. The planned name must equal the name
             that lands on disk.
Fallback:    n/a
Revisit if:  The tool ever targets a filesystem with a different forbidden set
             (it would widen, not narrow — POSIX forbids only "/" and NUL).
Supersedes:  —
```

## Example

`files/scans/holiday day 1. .jpg` has a description ending in a dot then a
space — both of which Windows strips on write. The target name is
`2005-08-01-holiday day 1.jpg`, trailing dot and space gone. The date comes
from Exif; the folder carries none.

> **Sample-fidelity note.** The characters Windows outright forbids in a path —
> `< > : " | ? *` and the reserved device names (`CON`, `NUL`, `COM1`, …) —
> cannot appear in a committed corpus file: `tools/build_samples.py` writes
> every recipe path to disk, and both Windows and `git` on Windows reject them
> on checkout. This example therefore covers the representable case (trailing
> dot and space on the description). The forbidden set proper is exercised by
> unit tests in `US-04-02`.

Proven by [`rule.feature`](rule.feature).
