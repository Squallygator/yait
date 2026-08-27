# UC-10 — A French month name in the filename gives month precision

| Field | Value |
|---|---|
| Group | `RG-1.1 Dates written in the filename` |
| Status | `Enforced` ▶ |
| Stories | `US-03-02` |
| Legacy findings | — |

## Rule

A filename containing a month written in French letters next to a four-digit
year — `suède juin 2004 045.jpg` — yields that year and month, at **month**
precision. Any trailing number is a sequence counter, not a day.

## Why

Before phones, people named scans and downloads the way they would label a
shoebox: a place, a month, a year, a running number. The reference archive is
full of `<lieu> <mois> <année> <nnn>` names. There is no day in them, and there
was never meant to be — the `045` is the 45th scan of that batch.

The month name is *data*, not a language choice: the archive is French, so the
recogniser must know `janvier`…`décembre` (with and without accents, any case).
The rule returns month precision so that `RG-3` names the file `2004-06` and
nothing downstream invents a day.

## Scope

This rule handles a month spelled in letters *in a filename*. The same shape in a
*folder* name is `UC-15`. A numeric `YYYY-MM` in a filename is `UC-11`. A year on
its own is `UC-12`. Precision itself — what "month" means downstream — is carried
through by `RG-3`.

## Counter-examples

- `juin 2004.jpg` — no sequence number; still month precision, `2004-06`.
- `12 juin 2004.jpg` — a day is present; this example does not cover that, a
  day-precision variant would be its own case.
- `June 2004 045.jpg` — English month; the archive is French and this example
  does not require English names to be recognised.
- `mardi 2004 045.jpg` — `mardi` is a weekday, not a month; nothing to read.

## Decision

```
Status:      Enforced
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   "<place> <French month> <year> <nnn>" is a pervasive pre-phone
             filing style in a French archive. There is no day in it; the
             trailing number is a batch counter. The month name is data the
             recogniser must carry.
Fallback:    n/a
Revisit if:  A collection appears whose language is not French and needs its own
             month-name table, or where the trailing number turns out to be a
             day often enough to matter.
Supersedes:  —
```

## Example

`files/numérisations/suède juin 2004 045.jpg` — an accented path, a French month,
and a trailing `045` that must be read as a counter, not a day. No metadata, so
the name is the only source, and the assertion is month precision.

Proven by [`rule.feature`](rule.feature).
