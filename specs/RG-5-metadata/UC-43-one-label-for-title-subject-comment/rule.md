# UC-43 — One deduced label is written to title, subject and comment

| Field | Value |
|---|---|
| Group | `RG-5 Metadata deduction and writing` |
| Status | `Enforced` ▶ |
| Stories | `US-06-05` |
| Legacy findings | — |

## Rule

The single label deduced by `UC-32` is written, unchanged, to all three
caption fields at once: the title, the subject and the comment (in EXIF/XMP
terms: `XPTitle` + `XMP:title`, `XPSubject` + `XMP:description`, `XPComment` +
`EXIF:UserComment`). One deduction, three fields, same string.

## Why

There is no agreement across software about which field is "the caption".
Windows Explorer's Details pane shows *Title*; its tooltip shows *Comments*;
many gallery apps key on *Subject* or on the XMP *description*. `dvd-tools`
wrote one field and left the others blank, so whether the caption showed up at
all depended on which program the family opened the photo in.

Writing the same string to all three means the caption is visible wherever
anyone looks, and — because the value is identical — the fields never disagree
and there is nothing to reconcile later.

## Scope

This rule is about *where* the label goes. *What* the label says is `UC-32` and
`UC-31`. That writing it must not re-encode the pixels is `UC-44`. That a field
a human already filled in is left alone is `UC-33`. The atomic write itself,
and keeping a copy of the original blocks for undo, is `RG-7`.

## Counter-examples

- A file where subject is already set by a human but title and comment are
  empty — `UC-33` protects the subject; this rule still writes title and
  comment.
- XMP present but EXIF `XP*` tags absent — both are written; the rule is
  field-role based, not container based.
- A read-back that shows the three fields with different values — that is the
  failure this rule exists to prevent.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   No two programs agree on which field is the caption. Writing the
             same deduced string to title, subject and comment makes it visible
             everywhere and keeps the fields from ever disagreeing.
Fallback:    n/a
Revisit if:  A metadata standard consolidates on one caption field widely
             enough that writing three becomes redundant clutter.
Supersedes:  —
```

## Example

`files/2005-08 Rome/le Forum.jpg` carries a capture date and no caption. After
its metadata is written, the deduced label `Rome - le Forum` reads back
identically from the title, the subject and the comment. An implementation that
writes only one of the three fails the scenario.

Proven by [`rule.feature`](rule.feature).
