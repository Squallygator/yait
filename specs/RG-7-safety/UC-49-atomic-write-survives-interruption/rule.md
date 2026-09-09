# UC-49 — An interrupted write never truncates the original

| Field | Value |
|---|---|
| Group | `RG-7 Safety and reversibility` |
| Status | `Enforced` ▶ |
| Stories | `US-04-01` |
| Legacy findings | — |

## Rule

Every file YAIT writes — a metadata edit, a renamed copy — is written to a
temporary file in the same directory and then moved into place with a single
atomic `os.replace`. If the process is killed, the power drops, or the disk
fills at any moment during the write, the original file is left exactly as it
was: complete, uncorrupted, unchanged. There is never a window in which the
real file is half-written.

## Why

This is the first of the `dvd-tools` findings that could destroy originals. It
wrote metadata in place — open the real file for writing, stream the new bytes
over the old. A crash mid-stream left the only copy of a photograph truncated
to whatever had been flushed. On a batch of tens of thousands of files, "a
crash sometime during the run" is not a rare event, it is the expected case.

Temp-file-then-replace makes the write all-or-nothing. The temp file is in the
same directory so the replace is a rename within one filesystem, which is
atomic on POSIX and on NTFS. A failure leaves a stray `.tmp` to clean up and
the original intact — never the other way round.

## Scope

This rule is the atomic-write guarantee for a *single* file. That the operation
is recorded before it happens, so recovery knows what was in flight, is
`UC-50`. That the whole batch can be resumed is `US-04-06`. That the metadata
write also does not re-encode the pixels is `UC-44`.

## Counter-examples

- The disk fills while writing the temp file — the temp write fails, the
  original is never touched, the operation reports the failure.
- The process is killed *after* `os.replace` returns — the new file is fully in
  place; that is a completed operation, not an interrupted one.
- A network share drops mid-replace — `os.replace` fails as a unit; the
  original stays.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   dvd-tools wrote metadata in place; a crash mid-write truncated the
             only copy of a photo, and on a large batch a crash is expected,
             not rare. Temp-file-then-os.replace makes every write
             all-or-nothing.
Fallback:    n/a
Revisit if:  Never. This is a data-safety non-negotiable (CLAUDE.md).
Supersedes:  —
```

## Example

`files/originals/portrait.jpg` carries an Exif date. The scenario interrupts a
metadata write to it partway through and asserts the file is still intact byte
for byte, with no `.tmp` left beside it.

> Simulating the interruption — killing the write at a chosen point — is built
> in `US-08-04` (robustness: interruption, full disk, locked file). This rule
> fixes the required behaviour and the corpus carries the file in its original
> state; it is not claiming the cut is exercised here.

Proven by [`rule.feature`](rule.feature).
