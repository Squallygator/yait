# UC-29 — When nothing answers, the file is undated, and that is a real state

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Enforced` ▶ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

When no source yields a date — no date in the filename, no dated folder on the
path, no readable content date, no sidecar — the file has **no resolved date**.
Its precision is `none` and its source is `none`. This is a first-class outcome,
not an error: the file is carried through the inventory as undated so a person
can look at it.

## Why

Some files simply cannot be dated from what is on disk, and pretending otherwise
is how originals get misfiled. `dvd-tools` in this situation would sometimes fall
back to the file's modification time, sometimes skip the file without a word —
either way the undated file vanished from view and its real date was lost or
faked.

Undated has to be visible. A file with no resolved date is reported as such,
counted, and left where it is; nothing downstream renames or moves it on a
guessed date.

## Scope

This rule defines the outcome when every source is exhausted. That the
modification time is specifically **not** an eligible last-resort source is
`UC-37`. The plausible-range guard that can *cause* a candidate to be rejected
and lead here is `UC-30`. The full order in which sources are tried is `UC-36`.

## Counter-examples

- A file in a folder named `Originals` with a blank name and no Exif, but two
  levels up there is a `2004` folder — that ancestor answers (`UC-14`); not
  undated.
- A file whose only date candidate was an out-of-range year — the candidate is
  rejected (`UC-30`) and, if nothing else answers, the file lands here.
- A file with an unreadable Exif block but a dated folder — the folder answers;
  the read error is logged (`UC-18`), the file is not undated.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Some files genuinely cannot be dated from disk. Making "undated" an
             explicit, visible outcome prevents the dvd-tools failure where such
             files were silently skipped or stamped with their mtime.
Fallback:    n/a
Revisit if:  A new source of truth is added (e.g. an external index) that could
             answer for files currently ending here.
Supersedes:  —
```

## Example

`files/Originals/scan.jpg` — a blank-ish name with no date, no Exif, and a
parent folder (`Originals`) that carries no date either. The scenario asserts
the file **has no resolved date** and that its precision is `none`.

Proven by [`rule.feature`](rule.feature).
