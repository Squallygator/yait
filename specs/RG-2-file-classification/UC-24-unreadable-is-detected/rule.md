# UC-24 — A file that cannot be read is reported, never silently skipped

| Field | Value |
|---|---|
| Group | `RG-2 File classification` |
| Status | `Enforced` ▶ |
| Stories | `US-03-06` |
| Legacy findings | — |

## Rule

A file that carries an image extension but whose bytes cannot be decoded far
enough to classify it — a JPEG whose header is intact but whose scan is cut
short, a file that ends in the middle of a segment — is classified as
`unreadable`. It appears in the inventory with that status. It is never dropped
from the count and never treated as "no date found".

## Why

These collections come off scratched CDs and dying hard drives. A truncated
JPEG is the signature of a bad sector: the first kilobytes read fine, then the
file just stops. `dvd-tools` handled this by catching the decode error and
moving on, so a disc that had lost two hundred photos to rot reported two
hundred files "with no date" — indistinguishable from undated holiday snaps.
Nobody noticed the disc was failing until the next copy lost more.

A file the tool cannot read is the one piece of news the operator most needs:
it means *go back to the source medium while it still spins*. Silently folding
it into the undated pile destroys that signal.

## Scope

This rule is about a file whose content is *damaged*. A file that is simply
empty — zero bytes — is `UC-25`; the distinction matters because a zero-byte
file is usually a failed copy, while a truncated one is usually rot. A file
whose extension is unknown, or which is a recognised non-media leftover, is
`UC-26`. What a date resolver does when handed an `unreadable` file (nothing —
it is not a date candidate) is `RG-1`.

## Counter-examples

- A JPEG with a corrupt *thumbnail* but a fully readable main image — readable,
  classified `image`; the broken thumbnail is not consulted.
- A perfectly valid image with an unusual subsampling the decoder is slow on —
  readable; slowness is not damage.
- A `.jpg` that is actually a small HTML "file not found" page saved by a
  browser — not a JPEG at all; it is `unreadable` here for a different reason,
  and that is fine, the outcome is the same.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   A file the tool cannot decode is evidence the source medium is
             failing. Catching the error and moving on, as dvd-tools did, hides
             that evidence inside the undated pile and lets the disc rot
             further before anyone acts.
Fallback:    n/a
Revisit if:  A partial-recovery path appears — reading the intact leading
             portion of a truncated JPEG to salvage its Exif — at which point
             "unreadable" would gain a sub-state for "readable enough to date".
Supersedes:  —
```

## Example

`files/damaged/corrupt-scan.jpg` is a real JPEG header followed by only the
first 4 096 bytes of its scan — the rest is gone, exactly as a bad sector
leaves it. It must be classified `unreadable`. An implementation that catches
the decode exception and returns "no date" puts it in the wrong pile and the
scenario fails.

Proven by [`rule.feature`](rule.feature).
