# UC-41 — Running the namer twice changes nothing the second time

| Field | Value |
|---|---|
| Group | `RG-3 Target naming` |
| Status | `Enforced` ▶ |
| Stories | `US-04-02` |
| Legacy findings | — |

## Rule

Applying the naming policy to a file whose name is already the policy's output
yields that same name. A file called `2007-08-25-arrivee ferry.jpg` that
resolves to `2007-08-25` does not become `2007-08-25-2007-08-25-arrivee
ferry.jpg` on a second pass. The target name is a fixed point: `name(name(x))
== name(x)`.

## Why

A batch that renames 30 000 files gets interrupted — a laptop sleeps, a network
share drops. The operator's only safe recovery is to point the tool at the
half-processed collection and run it again. That is only safe if a file already
in its final form is recognised as done: the resolver must see the leading
`YYYY-MM-DD-` it wrote last time as *the date token it would use*, so `UC-39`
removes it and the description is rebuilt identical, not stacked.

Without this, every re-run corrupts the names it already fixed, and the one
recovery move the operator has makes things worse.

## Scope

This rule is about the *name* being stable. That the *move* is safe to replay —
skipping files already at their destination rather than erroring — is execution
(`RG-4` `UC-53`, and `US-04-06`). Deciding the date itself is `RG-1`; this rule
relies on the date resolving the same way on both passes, which it does because
nothing about the file changed.

## Counter-examples

- `2007-08-25-arrivee ferry.jpg` in a folder that *also* names a different date
  — the filename token still wins (`UC-36`), so the name is still a fixed
  point.
- `2007-08-25 arrivee ferry.jpg` (space, not hyphen, after the date) — first
  pass normalises the separator to `2007-08-25-arrivee ferry.jpg`; the second
  pass is then a no-op.
- A file whose resolved date genuinely changed between runs because the
  operator edited its Exif — not idempotence's concern; the name *should*
  change.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   The one safe recovery from an interrupted batch is to re-run it.
             That is only safe if a file already in final form is a fixed point
             of the namer; otherwise every re-run corrupts the names it fixed
             last time.
Fallback:    n/a
Revisit if:  The name format changes shape (a new prefix or suffix), which
             would require the re-run to recognise both the old and the new
             form as "already done" during the transition.
Supersedes:  —
```

## Example

`files/2007-08-25 retour/2007-08-25-arrivee ferry.jpg` is already in target
form. Its date resolves from the filename token `2007-08-25` at day precision,
and its target name is `2007-08-25-arrivee ferry.jpg` — identical to its
current name, so a second run moves nothing. An implementation that re-prefixes
the resolved date produces `2007-08-25-2007-08-25-arrivee ferry.jpg` and fails.

Proven by [`rule.feature`](rule.feature).
