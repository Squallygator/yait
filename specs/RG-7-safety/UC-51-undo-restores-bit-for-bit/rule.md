# UC-51 — Undo restores the file bit for bit, not approximately

| Field | Value |
|---|---|
| Group | `RG-7 Safety and reversibility` |
| Status | `Enforced` ▶ |
| Stories | `US-07-03` |
| Legacy findings | — |

## Rule

Undoing an operation returns the file to its exact prior state. A renamed file
goes back to its original path with its content unchanged. A file whose
metadata was written has its original header blocks restored verbatim — the
same bytes that were there before, not a re-serialised equivalent — and its
compressed scan was never touched in the first place (`UC-44`). Round-tripping
an operation and its undo is the identity.

## Why

"Undo" that is only approximate is data loss wearing a safe-sounding name. If a
metadata undo rebuilds the Exif block from a parsed model, it can reorder tags,
drop an unknown maker note, or normalise a padding byte — and the file that
comes back is subtly not the file the operator had. Over a whole collection
those subtle differences are exactly the kind of silent corruption this tool
exists to prevent.

So undo does not *reconstruct* the prior state, it *reinstates* it: the
original bytes (the whole file for a small edit, or the exact header segments)
are kept alongside the journal entry and written back unchanged.

## Scope

This rule is about the fidelity of the restore. That the journal entry exists
at all, written ahead, is `UC-50`. That the forward write did not re-encode is
`UC-44`. Resuming or reversing a whole interrupted batch is `US-04-06` /
`US-07-03`; keeping the original metadata blocks for that is `US-06-06`.

## Counter-examples

- Undo of a rename whose target was never created (the forward op failed first)
  — nothing to undo; the file is already where it should be.
- A file the operator edited *after* the operation and before the undo — undo
  restores the pre-operation bytes and would overwrite that edit; this is why
  undo also checks the file still matches what the operation produced
  (coherence check, `US-07-03`).
- Undo run twice — the second is a no-op; the file is already restored.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   An approximate undo — rebuilding a metadata block from a parsed
             model — reorders tags and drops maker notes, which is the silent
             corruption the tool exists to prevent. Undo reinstates the kept
             original bytes, it does not reconstruct them.
Fallback:    n/a
Revisit if:  Never. Reversibility is a data-safety non-negotiable (CLAUDE.md).
Supersedes:  —
```

## Example

`files/2007-08 corse/IMG_0042.jpg` carries an Exif date. The scenario renames
it and then undoes the operation, asserting the file is back at
`2007-08 corse/IMG_0042.jpg` with identical bytes.

> The forward operation and its undo are driven by the journal/undo machinery
> built in `US-07-03`; the corpus carries only the file in its starting state.

Proven by [`rule.feature`](rule.feature).
