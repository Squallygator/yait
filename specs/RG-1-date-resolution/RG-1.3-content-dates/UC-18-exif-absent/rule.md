# UC-18 — A still with no Exif date is normal, not a dead end

| Field | Value |
|---|---|
| Group | `RG-1.3 Dates read from the file's content` |
| Status | `Enforced` ▶ |
| Stories | `US-03-04` |
| Legacy findings | — |

## Rule

When a still image carries no usable Exif date, that is not an error and the
file is not yet dateless. Resolution continues with the other sources — the
filename and then the folder path — exactly as if the metadata step had not run.

## Why

A large fraction of an old archive has no Exif at all: scans, images saved from
email or the web, anything that passed through WhatsApp, screenshots. If a
missing `DateTimeOriginal` were treated as a failure, those files would all land
in the "no date" bucket even when the folder they sit in names the year plainly.

In `dvd-tools` a permission error while reading Exif was swallowed and reported
as "no date found", which is why this rule is written down: *absent* metadata and
*unreadable* metadata are both just "this source did not answer", and resolution
moves on to the next source. A genuine read error is logged with its cause, never
folded silently into the result.

## Scope

This rule is about what happens *after* the metadata step comes up empty for a
still: keep going. Which Exif tags are tried, and in what order, is `UC-17`. What
happens when *every* source comes up empty is `UC-29`. The filename rules are
`RG-1.1`; the folder rules are `RG-1.2`.

## Counter-examples

- Exif present with a valid `DateTimeOriginal` — the metadata step answers; this
  rule does not apply (`UC-17`).
- No Exif, no date in the name, no dated folder — resolution still ends with no
  date, but by `UC-29`, not because metadata was absent.
- Exif physically unreadable (I/O error) — logged with its cause, then treated
  like absence: move to the next source.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Most of an old archive has no Exif. Treating that as a failure
             would discard folder and filename dates that are right there.
             Absent and unreadable metadata are both just "no answer from this
             source"; a real read error is still logged, not hidden.
Fallback:    n/a
Revisit if:  A case appears where continuing past absent metadata produces a
             worse answer than stopping would.
Supersedes:  —
```

## Example

`files/vacances corse 2004/DSC_0009.JPG` — no Exif at all, a filename with no
date, and a folder that names only the year. The scenario asserts that a date
*is* resolved (2004, year precision) and that it does **not** come from
`embedded-metadata` — proving resolution continued past the empty metadata step.

Proven by [`rule.feature`](rule.feature).
