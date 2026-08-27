# UC-01 — A date a person typed at the head of a filename outranks the camera clock

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

When a filename begins with a calendar date in `YYYY-MM-DD` form — optionally
followed by a space and a description — that date is the file's capture date,
and it is preferred over any date found in the file's own metadata.

## Why

A leading `YYYY-MM-DD` is not something a camera produces. Someone sat down,
looked at the picture, decided when it belongs, and typed it at the front of the
name so the folder would sort correctly. That is an act of filing, and it is the
most deliberate statement anyone has made about this file.

The camera clock, by contrast, is frequently wrong: never set after the battery
was pulled, still on the factory date, or an hour off for daylight saving. In the
reference archive a scanned print carried the flatbed scanner's *digitisation*
date in `DateTimeOriginal` — years after the photograph was taken — while the
person who scanned it had helpfully named the file `1974-08-11 grandparents
house.jpg`. Trusting the metadata there would have filed a 1974 photograph under
the year it was scanned.

So a human date at the head of the name wins. Not because filenames are more
reliable in general — device-generated stamps are treated as just another
mechanical source (`UC-04`) — but because *this* shape only appears when a person
put it there on purpose.

## Scope

This rule covers the human-typed leading date and its precedence over embedded
metadata. It does not decide the precedence between a filename date and a
*folder* date, nor the full ladder when three sources disagree: that is
`UC-36-source-priority-order`.

Which written forms of a date are recognised at all is `UC-13` for folders and,
for filenames, the sibling rules of this group. A date written with a month name
in letters is `UC-10`; a year alone is `UC-12`.

## Counter-examples

- `IMG_20150704_193000.jpg` — a device stamp, not a human filing decision. It is
  read (`UC-04`), but it does not outrank metadata the way this rule does.
- `2015-07 holidays.jpg` — month precision only, a different rule (`UC-11`).
- `20150704 beach.jpg` — a bare run with no separators (`UC-07`); still read, but
  it is not the deliberate `YYYY-MM-DD` filing shape.
- `Invoice 2015-07-04 scan.jpg` — the date is not at the *head* of the name. Out
  of scope here; not treated as a filing decision.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   A leading YYYY-MM-DD is only ever produced by a person filing the
             file on purpose. That intent outranks a camera clock, which is
             wrong often enough that the audit found a scanner date sitting in
             DateTimeOriginal for a 1970s print.
Fallback:    n/a
Revisit if:  A device or an export tool appears that writes a leading
             YYYY-MM-DD prefix mechanically, breaking the "a human typed this"
             assumption this rule rests on.
Supersedes:  —
```

## Example

`files/Scans/1974-08-11 grandparents house 03.jpg` — the name carries a leading
`1974-08-11`, and the embedded `DateTimeOriginal` is `2009-03-20`, the day it was
scanned. The two disagree by thirty-five years, so an implementation that reads
metadata first cannot pass by accident.

Proven by [`rule.feature`](rule.feature).
