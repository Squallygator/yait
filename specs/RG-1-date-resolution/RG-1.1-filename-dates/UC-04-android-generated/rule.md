# UC-04 — Android camera names embed the capture date

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

A filename beginning with `IMG_`, `VID_`, `PANO_` or `BURST_` immediately
followed by `YYYYMMDD` — the Android camera and Google Photos convention —
yields that calendar date, at day precision. A trailing `_HHMMSS` is a time and
is discarded.

## Why

Stock Android, and Google Photos on export, name captures `IMG_20150704_193000`:
a fixed prefix, the capture date, an underscore, the capture time. The prefix is
what separates this from an arbitrary digit run — it marks the number that
follows as a deliberately formatted date from the device, aligned with the Exif.

Unlike a human-typed date (`UC-01`), this is a mechanical stamp and is treated as
one more device source, not as a filing decision. It earns its own rule because
the four prefixes share a lifecycle — an Android naming change would move all of
them at once — and because the trailing time must be consumed cleanly.

## Scope

Recognises the prefix-and-date shape and extracts the date. It does not rank the
result against folders or metadata (`UC-36`). A bare `YYYYMMDD` with no
recognised prefix is `UC-07`.

## Counter-examples

- `IMG_20150704_193000_1.jpg` — a trailing `_1` collision suffix; date unchanged.
- `IMG_0042.jpg` — an old sequential name with no date; nothing to read here.
- `IMG-20161013-WA0001.jpg` — WhatsApp's hyphenated shape, a different rule
  (`UC-03`).
- `PXL_20210812_… .jpg` — the Pixel-era prefix; out of scope for this example,
  noted so a future rule can add it beside these four.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   IMG_/VID_/PANO_/BURST_ + YYYYMMDD is the stock-Android and Google
             Photos naming, aligned with the device capture time. The prefix is
             what makes the digits a date rather than an opaque run; the
             trailing _HHMMSS must be dropped.
Fallback:    n/a
Revisit if:  Android or Google Photos introduces a new prefix or changes the
             date layout (as the Pixel "PXL_" prefix already hints).
Supersedes:  —
```

## Example

`files/DCIM/Camera/IMG_20150704_193000.jpg` — no metadata, and the `_193000`
capture time trails the date directly, so an implementation that keeps reading
digits past the date produces a wrong result.

Proven by [`rule.feature`](rule.feature).
