# RG-2 — File classification

What each file *is*, before anything is done to it: a photograph, a video, an
archive, a companion file, a leftover of some long-dead photo manager, or a
casualty of a scratched disc.

Classification decides what gets processed, what gets set aside, and what must be
protected from the cleanup.

## Rules

| Rule | Status | Decides |
|---|---|---|
| `UC-24-unreadable-is-detected` | ▶ | A truncated image is reported, never silently skipped |
| `UC-25-zero-byte-file` | ▶ | An empty file is a casualty, not a photograph |
| `UC-26-junk-files` | ▶ | `Thumbs.db`, `Picasa.ini`, `desktop.ini` and friends |
| `UC-38-sidecar-is-not-junk` | ▶ | A `.THM` survives as long as its video does |
| `UC-59-duplicate-content-not-detected` | ⊘ | Names are deduplicated, contents are not |

## Boundaries

Discarded files are moved to a recycle area, never deleted — that is a safety
rule, [RG-7](../RG-7-safety/group.md).

`UC-38` is the twin of `UC-22` in
[RG-1.3](../RG-1-date-resolution/RG-1.3-content-dates/group.md): one says the
thumbnail dates the video, the other says the cleanup must not eat it first.
Splitting them is deliberate — in `dvd-tools` the two facets lived in different
functions and contradicted each other (finding #6).
