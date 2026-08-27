# UC-08 — A long run of digits is an identifier, never mined for a date

| Field | Value |
|---|---|
| Group | `RG-1.4 Arbitration and refusals` |
| Status | `Assumed exclusion` ⊘ |
| Stories | `US-03-05` |
| Legacy findings | — |

## Rule

A run of **nine or more digits** in a filename that does not match a recognised
timestamp shape (`YYYYMMDD`, an epoch stamp — see `UC-09`) is treated as an
opaque identifier. No eight-digit slice of it is read as a date, at either end or
in the middle.

## Why

Messenger, Facebook and older WhatsApp builds name saved images
`received_862666160799536.jpg`, `FB_IMG_1466721878.jpg`,
`1466721878123.jpg` — long opaque ids. Inside `862666160799536` there are
plenty of eight-digit windows that parse to a valid-looking date
(`86266616`, `26661607`, …), all meaningless. A resolver that goes hunting for a
date substring in a long id will confidently produce one and be wrong every time.

The safe rule is blunt: once a digit run is that long and is not a shape we
positively recognise, we do not read a date out of any part of it. The filename
still contributes nothing; the folder or the content answers, or the file is
undated.

## Scope

This is a refusal about the **filename** only. A recognised bare `YYYYMMDD` (up
to eight digits, isolated) is still read — `UC-07`. A 10- or 13-digit epoch
stamp is its own refusal — `UC-09`. Long digit runs in *folder* names are
covered by the folder format registry not recognising them (`UC-13`).

## Counter-examples

- `20080614_beach.jpg` — eight digits, isolated, a valid date; read normally
  (`UC-07`). This rule starts at nine.
- `IMG_1288000000.jpg` — ten digits; handled as an epoch stamp refusal (`UC-09`),
  not here.
- `DSC_00123456.jpg` — eight digits but not a plausible date (year 0012); rejected
  by the range gate (`UC-30`), and it would not reach this rule anyway.

## Decision

```
Status:      Assumed exclusion
Decided on:  2026-08-27                    Owner: squallygator
Rationale:   Long ids from Messenger/Facebook contain many eight-digit windows
             that parse to plausible dates, all meaningless. Refusing to mine a
             date from any nine-plus-digit non-timestamp run is the only safe
             rule; a substring search is wrong every time.
Fallback:    The filename contributes no date. The folder or the file content
             answers; failing that, the file is undated (UC-29).
Revisit if:  A source appears whose long ids embed a genuine, positionally-fixed
             capture date worth extracting — then this scenario goes red (the
             date would have to come from "file-name") and an enforced
             extraction rule replaces this refusal.
Supersedes:  —
```

## Example

`files/2015-07 Barcelona/received_862666160799536.jpg` — a fifteen-digit
Messenger id, no Exif. The scenario asserts the date comes from `folder-name`
(`2015-07`, month precision) and **not** from `file-name`, so an implementation
that slices an eight-digit "date" out of the id fails.

Proven by [`rule.feature`](rule.feature).
