# UC-05 — Screenshot names carry the moment the screenshot was taken

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

A filename beginning with `Screenshot_` followed by `YYYY-MM-DD` — the Android
screenshot convention — yields that calendar date, at day precision. Anything
after the date (a `-HH-MM-SS` time, an app package name) is not part of it.

## Why

Screenshots almost never carry Exif, so the filename is the only witness. Android
writes `Screenshot_2024-02-15-08-13-22-123_com.example.app.png`: the date, then
the time, then the foreground app. On a family archive these are receipts,
tickets, recipes and conversations that someone deliberately kept, and the date
they were captured is exactly the date that matters.

The trailing package name is the trap — it contains dots and digits and can look
like more date material to a loose pattern. Keeping this as its own rule makes
the "stop at the date, ignore the rest" boundary explicit.

## Scope

Recognises the `Screenshot_` prefix and reads the leading date. It does not cover
iOS screenshots (which have no date in the name) or the older `Screenshot_YYYYMMDD-HHMMSS`
form without dashes — a future rule can sit beside this one for those. Priority
against other sources is `UC-36`.

## Counter-examples

- `Screenshot_2024-02-15-08-13-22-123_com.android.chrome.png` — the package name
  trails the time; the date is still `2024-02-15`.
- `Screenshot from 2024-02-15 08-13-22.png` — the GNOME form; a separate shape,
  not covered by this example.
- `Screenshot_20240215.png` — no dashes; falls to the bare-run rule (`UC-07`).

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Screenshots carry no Exif, so the "Screenshot_YYYY-MM-DD-..." name
             is the only date. The trailing app package name has dots and digits
             and must not be read as further date material.
Fallback:    n/a
Revisit if:  Android changes the screenshot naming scheme, or the iOS / GNOME
             forms need to be recognised alongside this one.
Supersedes:  —
```

## Example

`files/Pictures/Screenshots/Screenshot_2024-02-15-08-13-22-123_com.example.app.png`
— no metadata, a dashed time immediately after the date, and a dotted package
name after that, so a pattern that keeps consuming digit groups fails.

Proven by [`rule.feature`](rule.feature).
