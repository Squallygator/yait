# UC-33 — A caption field a human already filled is never overwritten

| Field | Value |
|---|---|
| Group | `RG-5 Metadata deduction and writing` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-06-05` |
| Legacy findings | — |

## Rule

If a caption field — title, subject or comment — already holds a non-empty
value when YAIT goes to write the deduced label, that field is left exactly as
it is. The deduced label is still written to whichever of the three fields are
empty, but a field with content in it is not touched. YAIT does not merge,
append, or replace a human value.

## Why

A non-empty caption field was, almost always, typed by a person — and a person
who took the trouble to caption one photo knew something the folder path does
not say: a name, an occasion, a joke. The deduced label `Bretagne - vieux scan`
is a reasonable guess; "Grandpa's last summer at the house, 1974" is the truth,
and it is not recoverable once overwritten.

`dvd-tools` wrote its deduced caption unconditionally and destroyed exactly
these. Making non-destruction the rule — and stating it as a deliberate
exclusion rather than a silent "we skip populated fields" — keeps the contrast
sharp: YAIT will *fill* metadata, it will not *revise* it.

## Scope

This exclusion is about not clobbering a human value in a caption field. Which
fields the label targets when they *are* empty is `UC-43`. Detecting that the
file changed under the tool is a different guard, `UC-45`. Whether a value
"looks machine-written" (a bare `IMG_0042` some tool dumped into the title) and
could safely be replaced is explicitly *not* decided here — any non-empty value
is treated as human until a rule says otherwise.

## Counter-examples

- Title set, subject and comment empty — the deduced label is written to
  subject and comment; the title is kept.
- A field containing only whitespace — treated as empty and written; "non-empty"
  means it has real content.
- A field holding the *same* string the tool would write — left as is (writing
  it would be a no-op anyway); not counted as an overwrite.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   A non-empty caption field was typed by a person who knew something
             the path does not say. dvd-tools overwrote these and lost them.
             YAIT fills empty metadata; it does not revise existing metadata.
Fallback:    The deduced label is written only to the caption fields that are
             empty. Any field already holding a value keeps it, unchanged.
Revisit if:  A reliable way appears to tell a machine-dumped placeholder
             (a bare camera filename in the title) from a real human caption —
             then those placeholders could be replaced, this scenario would go
             red for that case, and an enforced "replace placeholder" rule
             would take over.
Supersedes:  —
```

## Example

`files/2004-09 Bretagne/vieux scan.jpg` already has the title
`Family house, summer 1974`. When its metadata is written, the title still
reads `Family house, summer 1974` afterwards — the deduced label
`Bretagne - vieux scan` was not written to it. An implementation that writes the
label unconditionally destroys the human caption and fails the scenario.

> **Sample-fidelity note.** `tools/build_samples.py` can only inject
> `Orientation`, `DateTimeOriginal` and `DateTimeDigitized`; it cannot yet seed
> a `XPTitle` / `ImageDescription` value. Until it can, the pre-existing title
> in this rule's scenario is set by the acceptance harness rather than baked
> into the corpus file. Adding title-field seeding to the generator folds into
> `US-00-23` (which already extends the closed EXIF list for `GPSDateStamp`);
> this note is removed once the corpus carries the title itself.

Proven by [`rule.feature`](rule.feature).
