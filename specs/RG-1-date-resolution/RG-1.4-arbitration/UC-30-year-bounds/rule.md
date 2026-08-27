# UC-30 — A candidate date outside the plausible year range is rejected

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Enforced` ▶ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

A candidate date is accepted only if its year is **≥ 1970** and **not later than
the day the collection is processed**. A candidate outside that range is
discarded, and resolution continues with the next source. If no source produces
an in-range date, the file is undated (`UC-29`).

## Why

Every source produces garbage occasionally: an epoch-zero Exif date in 1970, a
camera clock that jumped to 2097, a filename digit run that parses to year 0. A
single sanity range catches all of them in one place, so no individual reading
rule has to carry its own bounds check and they cannot disagree about what
"plausible" means.

The lower bound is 1970: the archive contains scanned prints from the 1970s, and
nothing older has turned up. The upper bound is the processing date, with no
future slack beyond it — a capture cannot have happened after the disc was read.
1970 is also the Unix epoch year, which conveniently means an epoch-zero
timestamp sits exactly on the boundary and is rejected.

## Scope

This is the range gate every candidate passes through, whatever its source. It
does not decide *which* in-range candidate wins (`UC-36`), and it is separate
from the clock-drift guard (`UC-19`), which compares an in-range embedded date
against an in-range folder date. Recognising a date shape at all is the job of
the `RG-1.1`/`RG-1.2`/`RG-1.3` rules.

## Counter-examples

- Filename `19551103_wedding.jpg` — a valid calendar date, but 1955 is before
  1970; rejected, resolution continues.
- Exif `2043-01-01` — after the processing date; rejected.
- Filename `20991231 note.jpg` in a `2015-08` folder — `2099` is rejected, the
  folder answers.
- Filename `20150704` processed in 2026 — in range; accepted.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Every source emits an implausible date now and then. One shared
             range gate (1970 .. processing date) catches epoch-zero stamps,
             runaway clocks and mis-parsed digit runs without each reading rule
             growing its own check.
Fallback:    n/a
Revisit if:  Media older than 1970 (scanned 1960s prints) enters scope, or a
             reason appears to allow a small amount of future slack for timezone
             skew.
Supersedes:  —
```

## Example

`files/2015-08 wedding/note-20991231.jpg` — the filename holds the valid
calendar date `2099-12-31`, whose year is far in the future and therefore
rejected. The scenario asserts the resolved date is the folder's `2015-08`, at
month precision, from `folder-name`, and **not** from `file-name`.

Proven by [`rule.feature`](rule.feature).
