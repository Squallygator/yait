# UC-26 — Photo-manager and operating-system leftovers are junk

| Field | Value |
|---|---|
| Group | `RG-2 File classification` |
| Status | `Enforced` ▶ |
| Stories | `US-03-06` |
| Legacy findings | — |

## Rule

A file whose name matches a known list of application and operating-system
detritus — `Thumbs.db`, `Picasa.ini`, `.picasa.ini`, `desktop.ini`,
`.DS_Store`, `ZbThumbnail.info`, `Picasa.db`, `AlbumArt_*.jpg`, `folder.jpg`
when it is Windows Media Player's cover cache — is classified as `junk`. Junk is
reported, kept apart from the media, and moved to the recycle area rather than
processed. It is matched by name, case-insensitively; its content is not
inspected.

## Why

Every collection that has been through Picasa, an old Windows, or a Mac carries
a layer of these files — one `Thumbs.db` per folder, a `Picasa.ini` recording
crop rectangles, a `.DS_Store` remembering icon positions. They are worthless
outside the application that wrote them and they clutter every count and every
screen. `dvd-tools` left them in place, so the inventory of a 5 000-photo
archive listed 5 400 "files" and the operator had to mentally subtract the
noise on every screen.

Matching by an explicit list, not by a heuristic, is deliberate: the cost of
wrongly discarding a real photograph is far higher than the cost of leaving one
unknown leftover in place, so the list only grows by names that have been seen
and confirmed.

## Scope

This rule recognises *named* leftovers. A camcorder `.THM` thumbnail looks like
junk but is not — it dates its video and must survive; that is `UC-38`, and the
two rules are kept apart on purpose (finding `#6`). A file that is damaged
rather than junk is `UC-24`; an empty one is `UC-25`. That junk is *recycled
rather than deleted* is a safety rule, `RG-7` `UC-49`..`UC-53`.

## Counter-examples

- `MVI_2468.THM` beside `MVI_2468.AVI` — a sidecar, not junk (`UC-38`).
- `my thumbs.db backup.jpg` — a real photo whose name merely contains the
  string; the match is on the whole filename, not a substring.
- `folder.jpg` that is actually someone's scanned photo of a folder — the
  WMP-cover match only applies when the file is the known cover-art shape;
  an ambiguous `folder.jpg` stays an `image`.
- `notes.txt`, `readme.rtf` — unknown non-media, left in place; not on the junk
  list, so not this rule's concern.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   Photo-manager and OS leftovers are worthless outside their app and
             inflate every count and screen. An explicit name list keeps the
             match safe: the list only grows by confirmed names, so a real
             photo is never discarded by a greedy heuristic.
Fallback:    n/a
Revisit if:  A leftover type appears that carries information worth keeping
             (as the .THM does), in which case it earns its own rule rather
             than a place on this list.
Supersedes:  —
```

## Example

`files/junk/Picasa.ini` holds a plausible `[Picasa]` body. It must be
classified `junk` on its name alone, without its content being read. An
implementation that only recognises `Thumbs.db`, or that tries to parse the
file before deciding, fails the scenario.

Proven by [`rule.feature`](rule.feature).
