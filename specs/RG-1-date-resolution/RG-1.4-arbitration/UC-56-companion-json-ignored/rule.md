# UC-56 — Google Takeout companion JSON is not read for a date

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

A Google Takeout sidecar — a `.json` file next to a media file, named
`<media>.json`, `<media>.supplemental-metadata.json` or similar, carrying a
`photoTakenTime` — is **not** used as a date source. The media's date is
resolved from its own Exif, name and folder, as if the JSON were not there.

## Why

Google Photos Takeout splits each image's metadata into a companion JSON. Its
`photoTakenTime` is frequently wrong: Takeout has shipped bugs that write the
export date, or a bulk-edited value, or the time the album was created. The file
is also just noise in the tree — one per photo, doubling the file count.

Unlike a camcorder `.THM`, which is a genuine capture-time artefact and *is*
trusted (`UC-22`), the Takeout JSON is a lossy re-export and is not. Naming this
as its own refusal keeps that contrast explicit: sidecars are not trusted as a
class, each type is a decision.

## Scope

This refusal is about the Takeout `.json` sidecar as a **date** source. Whether
that JSON is later used to recover a *caption* or *album* is a metadata question
(`RG-5`), out of scope here. The trusted sidecar case is `UC-22`. That these
`.json` files are swept aside rather than kept is classification (`RG-2`).

## Counter-examples

- A `.THM` beside a video — trusted, dates the video (`UC-22`). This rule is
  Takeout JSON only.
- A media file with a real Exif date and a Takeout JSON — the Exif answers; the
  JSON was never going to be consulted.
- A `.json` that is not a Takeout sidecar (some app's settings file) — ignored
  for dating for the same outcome, though it is not what this rule is about.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Takeout photoTakenTime is unreliable — export dates, bulk edits,
             shipped bugs — and the sidecars are tree noise. A camcorder .THM is
             a real capture artefact and is trusted (UC-22); the Takeout JSON is
             a lossy re-export and is not.
Fallback:    The media's date comes from its own Exif, then its name, then its
             folder (UC-36). The .json contributes nothing.
Revisit if:  Google fixes photoTakenTime reliability, or a collection has media
             with no other date where the JSON is the only witness — then this
             scenario goes red (the date would come from "sidecar") and an
             enforced JSON rule replaces it.
Supersedes:  —
```

## Example

`files/2018-09 Rome/IMG_1234.JPG` has no Exif, sits in a `2018-09` folder, and
is accompanied by `files/2018-09 Rome/IMG_1234.JPG.json` whose `photoTakenTime`
is `2003-01-01`. The scenario asserts the resolved date is the folder's
`2018-09`, month precision, from `folder-name`, and **not** from `sidecar` — so
an implementation that reads the JSON lands fifteen years off and fails.

Proven by [`rule.feature`](rule.feature).
