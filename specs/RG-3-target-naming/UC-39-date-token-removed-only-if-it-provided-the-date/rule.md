# UC-39 — A date token is dropped from the description only if it supplied the date

| Field | Value |
|---|---|
| Group | `RG-3 Target naming` |
| Status | `Enforced` ▶ |
| Stories | `US-04-02` |
| Legacy findings | — |

## Rule

The target name is `<resolved date>-<description>.<ext>`. The description is the
original filename stem, minus the one date token that actually produced the
resolved date — that token is removed so it is not written twice. Any *other*
digit run that looks like a date but did not supply it is left in the
description untouched.

## Why

When the date came from the filename, prefixing the resolved date and keeping
the original stem whole would give `2003-07-14-2003-07-14-....jpg`. So the
token that was used has to go. The trap is to then strip *every* date-shaped
run of digits — and archives are full of second dates that carry meaning: "1998
reunion re-scan", "copy of the 1974 album", "notes from 2001". Eat those and
the name stops meaning what it meant.

The discriminator is provenance, not shape: remove exactly the substring the
resolver pointed at, and nothing else.

## Scope

This rule governs which part of the *description* survives. Which token the
resolver chose, and why a filename date beats or loses to a folder or Exif
date, is `RG-1` arbitration (`UC-36`). Sanitising characters in the surviving
description is `UC-40`; keeping accents and punctuation in it is `UC-35`.

## Counter-examples

- Date came from the *folder*, filename is `holiday 2001.jpg` — `2001` did not
  supply the resolved date, so it stays: `2003-06-holiday 2001.jpg`.
- Date came from Exif, filename is `IMG_0042.jpg` — no date token in the name,
  nothing to remove.
- Filename `2003-07-14 2003-07-14.jpg` (the token literally twice) — only the
  occurrence the resolver matched is removed; the other stays as description.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   The used token must not be duplicated in the name, but stripping
             every date-shaped digit run destroys second dates that carry
             meaning. Remove exactly the substring the resolver used, by
             provenance, not by pattern.
Fallback:    n/a
Revisit if:  A resolver change stops reporting the exact source span, making
             "the token that was used" impossible to identify precisely.
Supersedes:  —
```

## Example

`files/Scans/2003-07-14 - 1998 reunion rescan.jpg` has no metadata; the date
resolves from the filename token `2003-07-14`, at day precision. The target
name is `2003-07-14-1998 reunion rescan.jpg`: the used token and its ` - ` glue
are gone, and `1998` — a bare year that did *not* supply the date — is kept. An
implementation that strips all date-shaped digits produces
`2003-07-14-reunion rescan.jpg` and fails; one that strips nothing produces a
doubled date and fails too.

Proven by [`rule.feature`](rule.feature).
