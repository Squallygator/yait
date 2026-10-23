# UC-61 — A caption in place is compared to its proposal ignoring case, accents and spacing

| Field | Value |
|---|---|
| Group | `RG-5 Metadata deduction and writing` |
| Status | `Enforced` ▶ |
| Stories | `US-06-03` |
| Legacy findings | — |

## Rule

When the review sheet decides whether a caption field in place — title, subject
or comment — already matches the value YAIT proposes, both strings are first
**normalised**: decomposed with Unicode NFD and stripped of their combining
marks (so `é` becomes `e`), lower-cased, every run of whitespace collapsed to a
single space, and trimmed at both ends. Equal after normalisation, the field is
**compliant**; different, it is **divergent**. An empty field — or one holding
only whitespace — with a proposal to offer is **to fill**, and a field with no
proposal at all has **nothing to propose**.

The normalised form is used to *compare* and nowhere else. Neither the value in
place nor the proposal is altered, and a compliant field is never rewritten: a
title typed `ROME - LE FORUM` stays exactly that.

## Why

The same caption reaches a file through many hands: typed in a gallery, edited
in Explorer's Details pane, pasted from a spreadsheet. `Etretat` for `Étretat`,
`Rome - le forum` for `Rome - le Forum`, a double space after a dash — none of
these is a disagreement about what the photograph is. If the comparison were
exact, every one of them would be reported divergent, and the *divergent* filter
— the one a person reads line by line before writing anything — would fill with
false alarms that bury the real ones, the file captioned `Menhir de Carnac`
where the folder says `Bretagne`.

`dvd-tools` already compared this way: its metadata editor (`csvedit.js`) folds
case, accents and repeated spaces before deciding a status, with a comment that
the rule is shared with `dvdmeta.py`. The behaviour is kept, and now written
down: a status that is computed in two places and specified in neither drifts.

## Scope

This rule decides the **status** of a caption field, not what is written. A
divergent field is never overwritten (`UC-33`); the label proposed in the first
place is `UC-32`; one label going to all three fields is `UC-43`. Title,
subject and comment are compared independently, each against the same
proposal. Capture dates are not text and are not compared this way. Where the
comparison runs — once, in the domain, and never again in the browser — is
`US-06-03`'s concern.

## Counter-examples

- Punctuation is not normalised: `disc 1 – plage` (en dash) against
  `disc 1 - plage` (hyphen) is **divergent**. Only case, accents and spacing are
  forgiven.
- Letters that Unicode does not decompose stay distinct: `Cœur` against `Coeur`,
  or `Straße` against `Strasse`, are **divergent**. Normalising is not
  transliterating.
- A genuinely different caption is divergent however it is spelled:
  `Menhir de Carnac` against `Bretagne - menhir debout`.
- Title divergent, subject compliant — each field keeps its own status; one
  divergent field does not make its siblings divergent.
- A field holding only spaces is empty, hence to fill, never compliant with an
  empty proposal.

## Decision

```
Status:      Enforced
Decided on:  2026-10-23                    Owner: squallygator
Rationale:   Case, accents and stray spaces are not disagreements. Folding them
             keeps the divergent status for captions that really differ, and
             matches what dvd-tools already did, now specified once.
Fallback:    n/a
Revisit if:  A collection shows two captions that differ only by case, accents
             or spacing and must still be reported divergent (case carrying
             meaning in a caption, for instance), or a script whose letters
             decompose into distinct readings.
Supersedes:  —
```

## Example

Five stills, each in a folder whose deduced label (`UC-32`) differs from the
caption already in place in exactly one way: capital letters
(`ROME - LE FORUM`), missing accents (`Etretat` for `Étretat`), extra spaces,
a real difference (`Menhir de Carnac`), and an en dash for a hyphen. The first
three are compliant, the last two divergent. An exact comparison fails the first
three; a comparison that also forgave punctuation fails the last.

> **Sample-fidelity note.** `tools/build_samples.py` cannot seed a caption
> field (`XPTitle`, `ImageDescription`), so the titles in the scenarios are set
> by the acceptance harness rather than baked into the corpus files, exactly as
> for `UC-33`. Caption-field seeding is not part of any lot yet.

Proven by [`rule.feature`](rule.feature).
