# UC-32 — The label is deduced from the folder and the filename together

| Field | Value |
|---|---|
| Group | `RG-5 Metadata deduction and writing` |
| Status | `Enforced` ▶ |
| Stories | `US-06-02` |
| Legacy findings | — |

## Rule

The label proposed for a photograph is `<folder label> - <filename context>`,
where the folder label is the enclosing folder's name with any date token
removed, and the filename context is the file's stem with any recognised camera
prefix removed and separators turned into spaces. When one side is empty, the
label is just the other side, with no dangling ` - `.

## Why

People file photographs meaningfully: `2004_09 Bretagne/menhir debout.jpg` says
this is a picture from Brittany, of a standing stone. That knowledge is already
written down, in the path — it just is not in any metadata field a viewer
shows. Deducing the label from the folder and the name recovers it for free,
for the whole collection, without anyone retyping a caption.

Combining both parts matters: the folder alone gives every photo of a two-week
trip the same label; the filename alone is often just `IMG_0042`. Together they
are usually a serviceable one-line caption.

## Scope

This rule builds the label string. Writing that string into the actual metadata
fields is `UC-43` (it goes to title, subject and comment). Handling a camera
prefix the tool does not recognise is `UC-31`. Not overwriting a caption a
human already wrote is `UC-33`. The date token removed from the folder label is
the same one `RG-1` used to resolve the date.

## Counter-examples

- `Originals/IMG_0042.jpg` — folder label `Originals` is not meaningful, but the
  rule does not know that; it produces `Originals - <context>`. Curating the
  folder-label vocabulary is a later concern, not this rule's.
- `2004-09 Bretagne/2004-09-04.jpg` — the filename is only a date; context is
  empty, so the label is just `Bretagne`.
- A file at the collection root with no enclosing folder — folder label empty;
  the label is the filename context alone.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   The path already records what a photo is about; it is just not in a
             field any viewer shows. Deducing <folder> - <filename> recovers a
             usable caption for the whole collection with no retyping.
Fallback:    n/a
Revisit if:  Folder-label noise (Originals, Scans, New folder) turns out to
             dominate real collections, making a stop-list part of this rule
             rather than a later refinement.
Supersedes:  —
```

## Example

`files/2004-09 Bretagne/menhir debout.jpg` carries no metadata; its date comes
from the folder, `2004-09`. The deduced label is `Bretagne - menhir debout`:
the folder label `Bretagne` (date token `2004-09` removed) joined to the
filename context `menhir debout`. An implementation that uses only the folder,
or only the filename, produces a different string and fails.

Proven by [`rule.feature`](rule.feature).
