# RG-4 — Collisions

Two files, one target name. Uniqueness is checked across the **whole
collection**, not per folder, because the end state is often a flat upload where
folders no longer exist to disambiguate.

## Rules

| Rule | Status | Decides |
|---|---|---|
| `UC-42-uniqueness-is-global` | ▶ | Scope of the uniqueness check |
| `UC-27-quality-ordering` | ▶ | Which of the competing files earns `_1` |

Ordering is by resolution, then file size, then capture time, then path — the
last criterion exists purely to make the outcome reproducible.

## Boundaries

Never overwriting a file that already exists is a safety rule,
[RG-7](../RG-7-safety/group.md) `UC-53`. Collisions are resolved in the plan,
before anything moves; a collision discovered at execution time is a defect.
