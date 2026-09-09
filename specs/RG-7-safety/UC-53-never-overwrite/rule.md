# UC-53 — An occupied destination is an error, never a silent suffix

| Field | Value |
|---|---|
| Group | `RG-7 Safety and reversibility` |
| Status | `Enforced` ▶ |
| Legacy findings | — |
| Stories | `US-04-01` |

## Rule

At execution time, if the destination path of a move or rename already exists
on disk, the operation fails for that file. It names the file, leaves the
existing file at the destination untouched, and does not write. It never
invents a `~2`, `_1` or `(copy)` name to complete the move anyway.

## Why

Planned collisions between two source files are resolved *in the plan*, before
anything moves, by adding `_1` (`RG-4`). This rule is the backstop for a
destination that is occupied by something the plan did not know about: a file
already sitting there from a previous partial run, a file a concurrent process
just created, a case-insensitive clash the plan missed.

`dvd-tools` handled this by appending `~2` and moving on. The result was two
files that were supposed to be one, diverging silently — and the operator
learned about it months later, if ever. Failing loudly instead means the
operator resolves the real conflict, once, with full information.

## Scope

This rule is the *execution-time* guard. Reconciling collisions known while the
plan is built is `RG-4` (`UC-42`, `UC-27`). Not truncating the original during
the write is `UC-49`. A destination path that is occupied because an external
input pointed somewhere unexpected is still also subject to `UC-52`.

## Counter-examples

- The destination exists but *is* the source file (a case-only rename on a
  case-insensitive filesystem) — handled as a rename, not a collision
  (`US-04-05`), not this error.
- The destination was created by an *earlier step of the same batch* that is
  being resumed and matches what this step would write — the operation is
  skipped as already done (`UC-41`, `US-04-06`), not failed.
- Two source files genuinely competing for one name — that never reaches this
  rule; `RG-4` gave one of them a `_1` in the plan.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   dvd-tools appended ~2 to an occupied destination and moved on,
             silently splitting one file into two divergent copies. An occupied
             destination the plan did not foresee is a real conflict and must
             stop for the operator, not be papered over.
Fallback:    n/a
Revisit if:  Never. "Never overwrite" is a data-safety non-negotiable
             (CLAUDE.md).
Supersedes:  —
```

## Example

`files/src/photo.jpg` is planned to move to a destination that, at execution
time, is already occupied by an unrelated file. The scenario asserts the
operation fails, names the file, and leaves the file already there untouched —
with no `~2` created.

> Staging a destination that appears *after* the plan is frozen is done by the
> `US-08-04` harness. This rule states the required failure; the corpus carries
> the source file only.

Proven by [`rule.feature`](rule.feature).
