# UC-03 — WhatsApp media names encode the send date

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

A filename of the form `IMG-YYYYMMDD-WAnnnn` or `VID-YYYYMMDD-WAnnnn` — WhatsApp's
naming for received media — yields that calendar date, at day precision. The
`WAnnnn` counter is not part of the date.

## Why

WhatsApp strips original metadata from everything that passes through it and
renames the file to the date it was sent, with a daily sequence number. For a
large share of a modern family archive this is the *only* date available: the
Exif is gone, and the send date is usually the same day as, or a day after, the
photograph.

It is kept separate from the other device patterns because its lifecycle is its
own. WhatsApp has already changed this format once; when it does so again, only
this rule moves.

## Scope

Recognises the shape, extracts the date. It does not claim the send date equals
the capture date — it is simply the best available and is recorded with
`file-name` as its source so the approximation is visible. Priority against other
sources is `UC-36`.

## Counter-examples

- `IMG-20161013-WA0001-2.jpg` — a re-saved copy; the date is still `2016-10-13`.
- `IMG-20161013-WA0042.jpg` — `WA0042` is the 42nd item that day, not a time.
- `received_862666160799536.jpg` — a different WhatsApp-era shape, a long opaque
  id with no date in it at all (`UC-08`).

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   WhatsApp deletes Exif and renames to IMG/VID-YYYYMMDD-WAnnnn. For
             much of a modern archive this filename is the only surviving date.
             The WAnnnn counter must be discarded, not read as a time.
Fallback:    n/a
Revisit if:  WhatsApp changes its media naming again, or begins preserving the
             original capture metadata it currently strips.
Supersedes:  —
```

## Example

`files/WhatsApp/IMG-20161013-WA0001.jpg` — no metadata (WhatsApp removed it), and
the `WA0001` counter directly follows the date, so a greedy digit match that
swallows it would produce a wrong day.

Proven by [`rule.feature`](rule.feature).
