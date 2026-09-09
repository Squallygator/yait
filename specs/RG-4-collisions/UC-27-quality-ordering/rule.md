# UC-27 — The higher-quality file keeps the clean name

| Field | Value |
|---|---|
| Group | `RG-4 Collisions` |
| Status | `Enforced` ▶ |
| Stories | `US-04-03` |
| Legacy findings | — |

## Rule

When several files collide on one target name, they are ordered and the first
keeps the clean name; the rest take `_1`, `_2`, … in that order. The ordering
key is, in priority: pixel resolution (width × height, larger first), then file
size (larger first), then capture time (earlier first), then the source path
(lexicographic). The path is only there to make the result total and
reproducible.

## Why

A collision is usually the same photo saved twice — once full-size, once as a
downscaled copy for e-mail; or an original beside a re-compressed export. The
clean, un-suffixed name is the one people will link to and browse first, so it
should point at the *best* copy. Resolution is the most reliable proxy for
"best" across a messy archive, with size as the tie-break when a crop changed
the pixel count but not much else.

Ending the key with the path guarantees two genuinely indistinguishable files
still get a stable, deterministic order — the plan must be the same on every
run (`UC-41`).

## Scope

This rule orders files that are *already known to collide*; establishing that
they collide, collection-wide, is `UC-42`. It does not deduplicate — every
colliding file is kept, just with a distinct name (`UC-59`). A master/edited
pair filed via an `Originals/` folder is named by `UC-28` before this rule is
reached.

## Counter-examples

- Two copies at the same resolution but different byte sizes — size breaks the
  tie; the larger keeps the clean name.
- Two identical files, byte for byte — resolution, size and time all tie; the
  path decides, deterministically.
- A high-resolution but badly re-compressed copy beside a smaller pristine one
  — resolution still wins; the rule proxies quality by pixels, not by
  inspecting compression.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   The un-suffixed name should point at the best copy, because that
             is the one people browse and link. Resolution is the best
             available proxy for quality across a messy archive; path last
             keeps the order total and every run identical.
Fallback:    n/a
Revisit if:  A collection appears where the largest file is routinely the worst
             (upscaled exports), making size or a real quality metric the
             better lead key.
Supersedes:  —
```

## Example

`files/2010-08 fete/a/photo.jpg` is 320 px wide; `files/2010-08 fete/b/photo.jpg`
is 640 px wide. Both carry Exif `2010-08-15 14:00:00`, so both resolve to
`2010-08-15-photo.jpg`. Resolution puts `b` first: `b` keeps
`2010-08-15-photo.jpg`, `a` becomes `2010-08-15-photo_1.jpg`. Ordering by path
alone would put `a` first — so an implementation that skips the quality key
fails the scenario.

Proven by [`rule.feature`](rule.feature).
