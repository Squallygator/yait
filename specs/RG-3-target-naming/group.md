# RG-3 — Target naming

Turning a resolved date and an original name into the name the file will carry:
`YYYY-MM-DD-original.ext`, sortable, and stable across runs.

## Rules

| Rule | Status | Decides |
|---|---|---|
| `UC-39-date-token-removed-only-if-it-provided-the-date` | ▶ | The name keeps what the name meant |
| `UC-28-originals-suffix` | ▶ | A camera master beside its retouched twin |
| `UC-40-illegal-chars-sanitised` | ▶ | Characters Windows refuses |
| `UC-35-accents-and-ampersand-preserved` | ▶ | `Suede`, `Breiz & Gwada`, parentheses survive |
| `UC-41-idempotent-on-rerun` | ▶ | Running twice changes nothing the second time |

`UC-41` is the rule that makes the tool safe to point at a half-processed
archive — which is what actually happens when a batch is interrupted.

## Boundaries

Two files competing for the same target name is
[RG-4](../RG-4-collisions/group.md).
