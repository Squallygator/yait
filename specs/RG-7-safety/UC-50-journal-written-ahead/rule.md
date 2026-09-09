# UC-50 — The journal entry is written and flushed before the operation runs

| Field | Value |
|---|---|
| Group | `RG-7 Safety and reversibility` |
| Status | `Enforced` ▶ |
| Stories | `US-07-01` |
| Legacy findings | — |

## Rule

Before any operation that changes the filesystem — a move, a rename, a metadata
write, a recycle — YAIT appends one line describing it to the journal (JSONL)
and flushes that line to disk. Only then does the operation run. The journal is
never held in memory and written at the end; each line is on disk before the
change it describes.

## Why

This is the difference between a log and a recovery mechanism, and it is a
`dvd-tools` finding. `dvd-tools` accumulated its journal in memory and wrote it
once, after the whole batch. A crash at file 19 000 of 40 000 left 19 000 files
moved and a journal file that was empty or stale — nothing to replay, nothing
to reverse, no way to even know which 19 000.

Write-ahead flips that. After any crash, the journal is a precise record of
every operation that had at least *started*. Recovery walks it: an entry with
no matching completion is either finished by hand or rolled back, and the
collection is put back into a known state.

## Scope

This rule is about *ordering and durability* of the journal line. That an
interrupted single write does not corrupt its file is `UC-49`. Reversing an
operation from its journal entry is `UC-51`. Resuming a whole batch is
`US-04-06`. Reading a legacy `dvd-tools` journal is `US-07-02`.

## Counter-examples

- A pure read (inspecting, auditing) — changes nothing, needs no journal line.
- A batch that completes cleanly — every line has its completion; recovery is a
  no-op. Write-ahead costs one `fsync` per operation and that is the price.
- The journal write itself fails (disk full) — the operation does not run; a
  change with no durable record is exactly what this rule forbids.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   dvd-tools journalled in memory and wrote once at the end; a crash
             mid-batch left thousands of files moved with no usable record. A
             line flushed to disk before each operation turns the journal from
             a log into a recovery mechanism.
Fallback:    n/a
Revisit if:  Never. This is a data-safety non-negotiable (CLAUDE.md).
Supersedes:  —
```

## Example

`files/originals/portrait.jpg` is about to be renamed. The scenario asserts
that the journal already holds the entry for that rename, flushed to disk,
before the file is moved — so a crash between the two leaves a recoverable
record.

> Stopping the process precisely between the journal line and the move is set
> up by the `US-08-04` harness. This rule states the required ordering; the
> corpus only carries the file.

Proven by [`rule.feature`](rule.feature).
