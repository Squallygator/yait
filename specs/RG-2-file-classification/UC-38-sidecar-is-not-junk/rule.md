# UC-38 — A .THM sidecar survives as long as its video does

| Field | Value |
|---|---|
| Group | `RG-2 File classification` |
| Status | `Enforced` ▶ |
| Stories | `US-03-06` |
| Legacy findings | `#6` |

## Rule

A `.THM` file that sits beside a video with the same stem is classified as
`sidecar`, not `junk`. It is kept for exactly as long as its video is in the
collection: it is never sent to the recycle area by the cleanup while the video
it belongs to is still there.

## Why

This is the other half of finding `#6`. Camcorders wrote a tiny full-Exif JPEG
— `MVI_3312.THM` — next to every clip, and on an old AVI whose `IDIT` chunk is
missing that thumbnail is the *only* surviving record of when the video was
shot. `UC-22` reads that date. But in `dvd-tools` the junk sweep and the date
reader were different functions that disagreed about `.THM`: the sweep saw a
stray thumbnail and binned it, the reader wanted its date — and whichever ran
first won. Run the sweep first and the video lost its only date source before
anyone tried to read it.

Splitting the concern into two rules that name each other is the fix. `UC-22`
takes the date; this rule keeps the file alive to be read. Neither can be
changed without the other coming into view.

## Scope

This rule decides that a *matched* `.THM` is protected from the junk filter. It
does not decide what date the video gets from it — that is `UC-22` in `RG-1.3`.
An *orphan* `.THM` with no video of the same stem is outside this rule's
protection; its classification falls back to the ordinary rules and it may well
be treated as junk. Matching sidecar to media by stem is the same mechanism
other companion types use elsewhere.

## Counter-examples

- `MVI_3312.THM` with no `MVI_3312.*` video anywhere in the collection — an
  orphan; this rule does not protect it.
- `holiday.THM` beside `holiday.thm.jpg` — the video, not another image, is
  what confers protection; two images do not make a sidecar pair.
- `Thumbs.db` beside a video — still junk (`UC-26`); the `.THM` extension is
  the trigger, not "any small file near a video".

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   A camcorder .THM is often the only date left for an AVI whose IDIT
             is gone. In dvd-tools the junk sweep and the date reader raced and
             the sweep could bin the thumbnail first (finding #6). Protecting a
             matched .THM here, and reading it in UC-22, removes the race.
Fallback:    n/a
Revisit if:  A camera family appears whose .THM is a regenerated edit-side
             preview with no capture date, making it genuinely disposable.
Supersedes:  —
```

## Example

`files/CANON/MVI_3312.THM` sits beside `files/CANON/MVI_3312.AVI`. Inspecting
the `.THM` must classify it `sidecar`, because its video is present. An
implementation that classifies any lone `.THM` as junk fails the scenario — and
in doing so would let the cleanup destroy the video's only date (`UC-22`).

Proven by [`rule.feature`](rule.feature).
