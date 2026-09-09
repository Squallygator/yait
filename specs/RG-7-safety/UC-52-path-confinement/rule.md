# UC-52 — A path from outside cannot escape the collection root

| Field | Value |
|---|---|
| Group | `RG-7 Safety and reversibility` |
| Status | `Enforced` ▶ |
| Legacy findings | — |
| Stories | `US-04-01` |

## Rule

Every path that enters YAIT from outside its own inspection of the tree — a
cell in an imported CSV, an entry in a journal being replayed, a value in an
API payload — is resolved and checked against the collection root before it is
used. If it resolves to anywhere outside that root, the operation is rejected.
No file outside the root is ever read, written, moved, or deleted, whatever the
input says.

## Why

The tool takes instructions from files it did not write: a CSV the operator
edited in a spreadsheet, a journal from a previous run or from `dvd-tools`. Any
of those can carry `..\..\..\Windows\System32\...`, an absolute path, a
drive-relative path (`C:foo`), or a symlink whose target climbs out of the
tree. Acting on such a path means the tool can be steered into reading or
clobbering files anywhere the process has rights — from a document the operator
did not mean to touch to a system file.

Confinement is checked once, centrally (`PathGuard`), on the resolved real
path, so a clever encoding cannot slip past a naive string check. `dvd-tools`
trusted journal paths verbatim.

## Scope

This rule is the boundary check on *externally supplied* paths. Paths YAIT
derives from its own walk of the collection are inside by construction. That an
occupied destination *inside* the root is still not overwritten is `UC-53`.
Long paths that are legitimately inside the root are `UC-34`.

## Counter-examples

- A relative path with `..` segments that still resolves *inside* the root
  (`a/b/../c`) — allowed; it is inside, the `..` is just untidy.
- A path exactly equal to the collection root — allowed as the root itself;
  operations on its direct children are the normal case.
- A symlink inside the root pointing to another location inside the root —
  allowed; the resolved target is still confined.
- A path outside the root that happens not to exist — still rejected; the
  rejection is on location, not on whether the target is there to hit.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   The tool acts on paths from CSVs and journals it did not write.
             Those can carry ..-traversal, absolute paths or escaping symlinks
             that steer reads and writes anywhere the process has rights.
             Every outside path is resolved and confined to the root first.
Fallback:    n/a
Revisit if:  Never. Path confinement is a data-safety non-negotiable
             (CLAUDE.md); it only ever tightens.
Supersedes:  —
```

## Example

`files/inside/kept.jpg` is an ordinary file within the collection. The scenario
hands an operation a path that climbs out of the root and asserts it is
rejected, with nothing outside the root read or written.

> The set of escape strings — `..`-traversal, absolute, drive-relative, symlink
> targets — and the `PathGuard` that resolves and checks them are built and
> attacked in `US-04-01` and `US-08-01`. This rule states the required refusal;
> the corpus carries one legitimate in-root file.

Proven by [`rule.feature`](rule.feature).
