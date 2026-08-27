# UC-06 — Windows Phone camera names embed the capture date

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

A filename beginning with `WP_` followed by `YYYYMMDD` — the Windows Phone camera
convention — yields that calendar date, at day precision.

## Why

Windows Phone named every capture `WP_20140713_001.jpg` or
`WP_20140713_15_22_30_Pro.jpg`. The platform is dead, but its files are all over
archives from 2011–2016, and the phones were notorious for a clock that reset to
the epoch after a flat battery — so the Exif is often less trustworthy than the
name, which was written once at capture and never touched again.

It is a small, closed, never-growing pattern. It gets its own rule so that when
the last Windows Phone file has been processed, this rule and its example can be
deleted as a unit without disturbing anything else.

## Scope

Recognises the `WP_` prefix and reads the date. Priority against other sources,
including the frequently-wrong Windows Phone camera clock, is `UC-19`
(clock-drift guard) and `UC-36`.

## Counter-examples

- `WP_20140713_15_22_30_Pro.jpg` — the `_Pro` marks an HDR shot; the date is
  still `2014-07-13`.
- `WP_ss_20140713_001.jpg` — a screenshot variant; the date reads the same, and
  the example does not need to distinguish them.
- `wp-content/…` — a WordPress upload path, not a Windows Phone file. The `WP_`
  prefix with an underscore and a date is what this rule keys on.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   WP_YYYYMMDD is the Windows Phone camera naming. The platform is
             gone but the files persist, and their camera clocks frequently
             reset to the epoch, so the name is often the better source.
Fallback:    n/a
Revisit if:  Never expected to grow. Delete this rule as a unit once no Windows
             Phone files remain in scope.
Supersedes:  —
```

## Example

`files/Camera Roll/WP_20140713_15_22_30_Pro.jpg` — no metadata, and the name
piles three underscore-separated numbers and a `_Pro` marker after the date, so a
pattern that does not anchor on the `WP_YYYYMMDD` head can drift.

Proven by [`rule.feature`](rule.feature).
