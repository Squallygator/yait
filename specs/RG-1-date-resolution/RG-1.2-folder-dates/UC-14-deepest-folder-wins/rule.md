# UC-14 — The deepest dated folder wins over its ancestors

| Field | Value |
|---|---|
| Group | `RG-1.2 Dates carried by folder names` |
| Status | `Enforced` ▶ |
| Stories | `US-03-03` |
| Legacy findings | — |

## Rule

When several folders on a file's path carry a date, the date of the **closest**
folder to the file is used. Ancestors are only consulted when no nearer folder
answers.

## Why

Archives are filed in layers. Somebody creates `2002-07-20 Wedding at Arras` for
a whole event, then subdivides it by day as the photographs come in from several
cameras and several people. The outer folder names the *event*; the inner one
names the *day*. The inner one is more specific, and more recent in intent — it
was created by someone who already had the pictures in front of them.

Taking the outermost date would file three days of a wedding under a single date,
which is exactly what the subdivision was created to avoid.

The reference archive contains this shape: a folder for the wedding weekend, and
inside it one folder per day, including days *before* the outer folder's own date
— the preparations. An ancestor-wins rule would silently move those back onto the
ceremony day and destroy the distinction.

## Scope

This rule decides **which** dated folder wins. It says nothing about which
written forms count as a date — `2002-07-20`, `18-07-2002`, `2002_07_20` are
recognised (or not) by `UC-13-folder-date-formats`, and a month written out in
letters by `UC-15-folder-french-month`.

It also says nothing about whether a folder date beats the camera clock: that is
arbitration, `UC-36-source-priority-order`.

## Counter-examples

- A nearer folder whose name merely *looks* dated — `2006-2` is a disc number,
  not February 2006 (`UC-16`). It does not answer, so the search continues
  outwards.
- A nearer folder with no date at all — `Originals`, `photos`, `Camera Roll`.
  It does not answer; the ancestor applies. That is this rule working, not an
  exception to it.

## Decision

```
Status:      Enforced
Decided on:  2026-08-24                    Owner: squallygator
Rationale:   The innermost dated folder is the most specific statement anyone
             made about when these files belong. Subdividing an event by day is
             a deliberate act; overriding it with the event date discards it.
Fallback:    n/a
Revisit if:  An archive appears where inner folders are dated by processing date
             rather than capture date, making the outer folder the truthful one.
Supersedes:  —
```

## Example

`files/2002-07-20 Wedding at Arras/18-07-2002/026-the-couple-and-the-mother.jpg`
— two dated ancestors that disagree, and the nearer one is two days *earlier*
than the outer one, so a wrong implementation cannot accidentally pass by
picking the maximum, the minimum, or the first match found walking down.

The image carries no metadata of its own, so the path is the only thing that can
answer.

Proven by [`rule.feature`](rule.feature).
