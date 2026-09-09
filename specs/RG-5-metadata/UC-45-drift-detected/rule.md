# UC-45 — A file that changed since the audit is not written blind

| Field | Value |
|---|---|
| Group | `RG-5 Metadata deduction and writing` |
| Status | `Enforced` ▶ |
| Stories | `US-06-04` |
| Legacy findings | — |

## Rule

The metadata audit records a fingerprint (size and content hash) for every file
in the plan. When the plan is applied, each file's fingerprint is checked
again. If it no longer matches — the file was edited, replaced, rotated, or
re-saved between audit and apply — the write for that file is refused. The file
is left exactly as it is and reported as drifted; the rest of the plan
proceeds.

## Why

The audit and the apply can be minutes or days apart — the operator reviews the
proposed captions, goes to lunch, comes back. In that gap they might open a
photo in an editor, straighten it, and save. If the tool then applies the plan
it computed against the *old* bytes, it either clobbers the operator's change
or writes a caption deduced from a file that is no longer the file it saw.
`dvd-tools` had no fingerprint and did exactly this.

Refusing the stale write, loudly, is the safe choice: the operator re-audits
the handful of drifted files and applies again.

## Scope

This rule is the guard on the *metadata* apply. The equivalent guard for the
*rename/move* plan is `US-04-04` (frozen plan with fingerprints) — same idea,
different operation. What a correct write does to the bytes is `UC-44`; doing it
atomically is `RG-7`.

## Counter-examples

- A file whose `mtime` changed but whose bytes did not (a backup tool touched
  it) — fingerprint is content-based, so it still matches; the write proceeds.
- A file deleted between audit and apply — not drift, a different error
  (missing), handled by the apply's own preconditions.
- A file that drifted and then drifted *back* to its audited bytes — matches
  again; the write proceeds. The check is on content, not history.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   Audit and apply are separated in time; the operator may edit a
             photo in between. Writing the plan against stale bytes clobbers
             that edit or captions the wrong file. A content fingerprint checked
             at apply time turns that into a loud refusal.
Fallback:    n/a
Revisit if:  Fingerprinting every file at apply time becomes a measurable cost
             on very large collections, forcing a cheaper (mtime+size) fast
             path with content hash only on mismatch.
Supersedes:  —
```

## Example

`files/2010-05 corse/IMG_0042.jpg` is recorded by the audit. Its bytes then
change on disk, and the plan is applied. The write is refused because the file
no longer matches its audited fingerprint, and the file is left untouched. An
implementation with no fingerprint check writes over the changed file and fails
the scenario.

> The step that mutates the file between audit and apply is provided by the
> acceptance harness in `US-06-04`; this rule states the required behaviour and
> the corpus carries only the file in its audited state.

Proven by [`rule.feature`](rule.feature).
