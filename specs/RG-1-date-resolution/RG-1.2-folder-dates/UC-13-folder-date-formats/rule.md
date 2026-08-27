# UC-13 — Which written forms count as a folder date

| Field | Value |
|---|---|
| Group | `RG-1.2 Dates carried by folder names` |
| Status | `Enforced` ▶ |
| Stories | `US-03-03` |
| Legacy findings | — |

## Rule

A folder name is read as carrying a date when it contains a calendar date in one
of the recognised numeric forms, anywhere in the name, alongside any description:

| Form | Example | Precision |
|---|---|---|
| `YYYY-MM-DD`, `YYYY_MM_DD`, `YYYY.MM.DD`, `YYYY MM DD` | `2002_07_20 Wedding` | day |
| `DD-MM-YYYY` and the same separators | `18-07-2002` | day |
| `YYYYMMDD` (bare, isolated) | `20020720 wedding` | day |
| `YYYY-MM` / `YYYY_MM` (zero-padded month) | `2002-07 summer` | month |
| `YYYY` alone | `2002 album` | year |

Ambiguous day/month order is resolved **day-first** (`DD-MM-YYYY`): the reference
archive is European. The date must be a real calendar date in the plausible year
range (`UC-30`), or the folder is treated as carrying no date.

## Why

Folders are labelled by hand, across decades, by many people and a few tools.
The same date turns up written a dozen ways: dashes, underscores, dots, day
first, year first, with or without a day. If every folder rule re-implemented
recognition, they would drift apart. This rule is the **single registry** of what
a written calendar date looks like in a folder name; `UC-14` (which dated folder
wins) and `UC-15` (a month in letters) build on it.

Day-first is a genuine decision, not a default: `01-02-2003` is 1 February here,
never 2 January. It is stated once, here, so no sibling rule quietly picks the
other convention.

## Scope

This rule decides **whether** a folder name carries a date and at what precision.
It does not decide **which** dated folder on a path wins — that is `UC-14`. A
month written in French letters is `UC-15`. A single unpadded digit after the
year (`2006-2`) is a disc number, not February — the exclusion `UC-16`. Reading a
date from the file's own name is `RG-1.1`.

## Counter-examples

- `2006-2` — an unpadded single-digit suffix; a batch index, not February
  (`UC-16`).
- `2003-13-05` — month 13; not a date, the folder carries none.
- `Photos 2002` mixed with `IMG_1234` — the `2002` is a year; `1234` is not a
  date and must not be read as one.
- `Rechnung 20020720` inside an invoice dump — recognised as a date by form;
  whether that is *desirable* is arbitration, not recognition.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Hand-labelled folders spell the same date many ways. One registry
             of accepted forms keeps the folder rules from each growing their
             own parser. Day-first order is fixed here because the archive is
             European.
Fallback:    n/a
Revisit if:  A collection appears that is US-formatted (month-first), which would
             need an explicit per-collection convention rather than a global one.
Supersedes:  —
```

## Example

`files/2002_07_20 Wedding at Arras/img_0042.jpg` — the folder uses the
underscore form, the least obvious of the accepted separators, with a
description after it. The image carries no metadata, so the folder is the only
source, and it resolves at day precision.

Proven by [`rule.feature`](rule.feature).
