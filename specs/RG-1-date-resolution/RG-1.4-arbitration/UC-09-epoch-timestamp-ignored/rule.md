# UC-09 — An epoch timestamp in the name dates the transfer, not the photograph

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

A 10-digit (Unix seconds) or 13-digit (Unix milliseconds) run in a filename —
`FB_IMG_1288000000.jpg`, `1466721878123.jpg` — is **not** read as a capture
date, even when it decodes to a plausible one. It is a transfer timestamp
written by the app that saved the file. The date comes from another source.

## Why

Facebook and Messenger prefix or name saved images with the epoch second (or
millisecond) at which *they* processed the image — the download, not the shot.
Decode it and you get the day the picture was forwarded into a chat, which for an
old photograph is years or decades wrong.

In the reference archive an `FB_IMG_` file whose epoch stamp decoded to *the day
before the archive was assembled* was sitting on a photograph fifteen years
older. The stamp was real, well-formed, and completely misleading.

This is an **assumed exclusion**: YAIT recognises the epoch shape specifically so
it can refuse it. It does not fall through to `UC-08` (which would ignore it as
just a long run) — it is named, so that the day someone wants to use it, the
decision to reverse is explicit.

## Scope

Epoch stamps in a **filename**. Longer opaque ids with no timestamp meaning are
`UC-08`. A normal `YYYYMMDD` is `UC-07`. Once the epoch stamp is refused, which
remaining source wins is `UC-36`.

## Counter-examples

- `20101025.jpg` — eight digits, a calendar date, not an epoch; read normally
  (`UC-07`).
- `1288000000` as a folder name — not a recognised folder date form (`UC-13`);
  ignored there for a different reason.
- A 10-digit run that decodes outside the plausible range — refused here anyway;
  the range gate (`UC-30`) would also stop it.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Facebook/Messenger epoch stamps are the moment the app handled the
             image, not the capture. In the archive one decoded to the day
             before assembly for a fifteen-year-old photo. The shape is
             recognised precisely so it can be refused by name.
Fallback:    The epoch run contributes no date. The folder or the file content
             answers; failing that, the file is undated (UC-29).
Revisit if:  A workflow appears where the epoch in the name genuinely equals the
             capture instant — then this scenario goes red (the date would come
             from "file-name") and an enforced epoch-parsing rule replaces it.
Supersedes:  —
```

## Example

`files/2003 vacances/FB_IMG_1288000000.jpg` — the epoch stamp `1288000000`
decodes to October 2010, but the photograph is filed under `2003`. No Exif. The
scenario asserts the resolved date is `2003`, year precision, from `folder-name`,
and **not** from `file-name`.

Proven by [`rule.feature`](rule.feature).
