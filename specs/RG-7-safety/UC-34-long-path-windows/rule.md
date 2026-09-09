# UC-34 — Paths beyond 260 characters still work

| Field | Value |
|---|---|
| Group | `RG-7 Safety and reversibility` |
| Status | `Enforced` ▶ |
| Legacy findings | — |
| Stories | `US-04-01` |

## Rule

A media file whose full path is longer than Windows' legacy `MAX_PATH` of 260
characters is inventoried, renamed, given metadata and organised like any
other. It is never skipped, and no operation on it fails, because of its path
length. YAIT uses extended-length path handling (the `\\?\` form / long-path
aware APIs) throughout.

## Why

Deeply nested archives — a backup of a backup of a Camera Uploads folder — hit
260 characters easily, and the naive Win32 file APIs silently fail past it:
`open` raises, `os.scandir` stops, a move reports success and does nothing.
`dvd-tools` inherited that limit and just skipped the files it could not reach,
so the deepest, most-buried photographs — often the ones most in need of
rescue — were the ones it quietly left behind.

The fix is not to shorten paths (that would rename folders the operator did not
ask to rename); it is to open every path in the extended-length form so the
260 limit never applies.

## Scope

This rule is about *length*. A long path that tries to leave the collection
root is still rejected by `UC-52`. Characters that are invalid regardless of
length are `UC-40`. Non-Windows platforms have no `MAX_PATH` and this rule is a
no-op there.

## Counter-examples

- A path just under 260 — works, and always did; the rule is about the files
  past the cliff.
- A single path *component* longer than 255 — that is a real filesystem limit,
  not `MAX_PATH`; out of scope, and rare in practice.
- A UNC path (`\\server\share\...`) already over 260 — same handling; the
  extended form is `\\?\UNC\server\share\...`.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   Deep archives cross 260 characters easily, and naive Win32 APIs
             fail past it — often silently. dvd-tools skipped those files, i.e.
             the most deeply buried photos. Extended-length path handling makes
             the limit not apply.
Fallback:    n/a
Revisit if:  Windows' long-path opt-in becomes universal and unconditional,
             making the explicit \\?\ handling redundant (it would stay
             harmless).
Supersedes:  —
```

## Example

`files/deeply nested archive folder from an old backup disc/one more level down
the tree/family gathered on the beach at sunset.jpg` is a deliberately long,
deep path used as a smoke test: it must be inventoried, named and organised
with no error.

> **Sample-fidelity note.** A corpus file whose *full* path genuinely exceeds
> 260 characters cannot be committed: `tools/build_samples.py` writes every
> recipe path to disk, and a Windows checkout without long-path support enabled
> — the exact environment this rule is about — would fail to create it, and so
> would `--check` under a long temp prefix. The real >260 boundary is therefore
> exercised by a Windows-only test in `US-08-04` (and the Windows CI leg from
> `US-01-01`); this corpus example only proves that a long, deep path is
> handled like a short one.

Proven by [`rule.feature`](rule.feature).
