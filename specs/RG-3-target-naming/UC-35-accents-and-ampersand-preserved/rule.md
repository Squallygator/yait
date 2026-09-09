# UC-35 — Accents, ampersands and parentheses are kept in the target name

| Field | Value |
|---|---|
| Group | `RG-3 Target naming` |
| Status | `Enforced` ▶ |
| Stories | `US-04-02` |
| Legacy findings | — |

## Rule

Characters that are valid in a filename but merely uncommon are kept as they
are in the description: accented and non-Latin letters (`é`, `ü`, `ñ`, `ß`, …),
`&`, parentheses, square brackets, spaces, apostrophes, commas, `+`, `=`. The
description is not transliterated to ASCII, not lower-cased, not
punctuation-stripped. Only the characters `UC-40` names as unsafe are removed.

## Why

The reference archive is French: folders and files are full of `Suède`,
`Noël & Jour de l'an`, `plage (2)`, `Île de Ré`. Folding all of that to
`suede`, `noel-jour-de-l-an`, `plage-2` makes every name a little wrong and
some ambiguous — `Ré` and `Re` are different words. Modern Windows, macOS and
Linux all handle Unicode filenames; there is no technical reason left to
mangle them, and doing so only loses information.

## Scope

This rule says what is *kept*. What is *removed* for safety is `UC-40`, and the
two lists are complementary — no character is on both. Removing the used date
token from the description is `UC-39`.

## Counter-examples

- `holiday: the best <ever>.jpg` — `:` and `<>` are unsafe and are removed
  (`UC-40`); this rule does not protect them.
- `CAFÉ.JPG` — the `É` is kept; the rule does not force a case change, so the
  description stays `CAFÉ` (a separate normalisation may lower-case the
  extension, but not the description here).
- A name already all-ASCII — nothing to do; the rule is a no-op, not a
  requirement to add anything.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   The archive is French; ASCII-folding and punctuation-stripping
             make every accented name slightly wrong and some ambiguous. Every
             target OS handles Unicode filenames, so there is nothing to gain
             by mangling them.
Fallback:    n/a
Revisit if:  A downstream consumer appears that genuinely cannot handle
             non-ASCII filenames (an old sync client, a FAT device), in which
             case transliteration becomes an opt-in output mode, not the
             default.
Supersedes:  —
```

## Example

`files/2004-07 corse/Étretat & la plage (2).jpg` carries no metadata; the date
comes from the folder, `2004-07`, at month precision. The target name is
`2004-07-Étretat & la plage (2).jpg` — the `É`, the `&`, the parentheses and
the spaces all survive. An implementation that ASCII-folds and strips
punctuation produces `2004-07-etretat-la-plage-2.jpg` and fails.

Proven by [`rule.feature`](rule.feature).
