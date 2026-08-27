# UC-37 — The filesystem modification time is never a capture date

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

The filesystem timestamps — modification time (`mtime`), change time (`ctime`),
creation/birth time — are **not** eligible as a date source, not even as a last
resort. A file with no date in its name, folder, or content stays undated
(`UC-29`); it does not fall back to `mtime`.

## Why

On any archive that has been copied — off a failing disc, from an old drive,
between two computers, out of a backup — `mtime` is the time of the *copy*, not
the photograph. Every file in a freshly-restored tree carries roughly the same
recent `mtime`.

The reference archive is exactly such a copied tree. Its files, photographs from
2011, all have an `mtime` from the week the DVDs were imaged. A resolver that
uses `mtime` as a fallback would file a decade of family pictures into the
current month, and it would do it silently and consistently, which is the worst
kind of wrong: it looks like it worked.

This is an **assumed exclusion**: `mtime` is a readable, always-present value
that YAIT deliberately refuses to consider. It is the root project rule
(`CLAUDE.md`, data-safety section) written up as a spec with a test behind it.

## Scope

This rule removes `mtime`/`ctime`/`birthtime` from the candidate sources. What
happens once every *eligible* source is exhausted — the undated outcome — is
`UC-29`. The plausible-range gate is `UC-30`. This rule is not about ordering; it
is about eligibility.

## Counter-examples

- A file with `mtime` in 2012 sitting in a `2012-07` folder — the folder
  answers; `mtime` played no part, and happening to agree is not this rule
  firing.
- A file whose `mtime` is older than any other candidate — still not used; "the
  oldest timestamp" is not a heuristic here.
- `birthtime` on a filesystem that tracks it accurately for never-copied files —
  still excluded; the tool cannot tell a copied tree from an original one, so it
  trusts neither.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   On a copied tree — which every recovered archive is — mtime is the
             copy date. Using it as a fallback files old photos into the current
             month silently and consistently. No filesystem timestamp is a
             capture date.
Fallback:    The file is undated (UC-29). The modification time is recorded as
             file metadata for display, but is never the resolved date.
Revisit if:  A workflow guarantees an un-copied tree with trustworthy birth
             times — even then, a per-collection opt-in would be safer than
             reversing this globally, so the scenario below stays the guard.
Supersedes:  —
```

## Example

`files/Copie de Photos/IMG_1234.JPG` — no date in the name, no Exif, and a
parent folder (`Copie de Photos`) with no date. The file is written fresh by the
sample generator, so its `mtime` is "now" — decades from any plausible capture.
The scenario asserts the file **has no resolved date** and precision `none`: if
`mtime` were consulted, a current-year date would appear and the test would
fail.

Proven by [`rule.feature`](rule.feature).
