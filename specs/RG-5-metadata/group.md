# RG-5 — Metadata deduction and writing

Filling in title, subject, comment and capture date, deduced from where a
photograph sits: `2004_09_04 - Brittany/IMG0001_the-standing-stone.JPG` knows it
is about Brittany, and about a standing stone.

Writing is the most dangerous thing this tool does — it modifies originals in
place rather than moving them. The rules here are correspondingly strict.

## Rules

| Rule | Status | Decides |
|---|---|---|
| `UC-32-label-from-folder-and-context` | ▶ | `<folder label> - <filename context>` |
| `UC-31-unknown-camera-prefix` | ▶ | An unrecognised prefix must not eat the context |
| `UC-43-one-label-for-title-subject-comment` | ▶ | One deduction, written to all three fields |
| `UC-44-write-never-reencodes` | ▶ | Header segments only; the scan is copied |
| `UC-45-drift-detected` | ▶ | A file changed since the audit is not written blind |
| `UC-33-existing-fields-never-overwritten` | ⊘ | A value already there was probably typed by a human |

## Boundaries

Atomic writing and the ability to restore the original metadata blocks are
[RG-7](../RG-7-safety/group.md).
