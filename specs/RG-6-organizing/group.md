# RG-6 — Organizing

Moving the normalised files into their final shape: a `YYYY/MM` tree, or a single
flat directory for a one-gesture upload.

## Rules

| Rule | Status | Decides |
|---|---|---|
| `UC-46-organize-by-precision` | ▶ | Day/month to `YYYY/MM`, year to `YYYY/`, none to `_undated` |
| `UC-48-empty-folders-pruned` | ▶ | And only counted once actually removed |
| `UC-47-flatten-leaves-undated-in-place` | ⊘ | Sending an undated file flat defeats the purpose |

Precision drives placement: a file known only to the year does not get invented a
month. This is the same honesty as the partial dates themselves.

## Boundaries

Deciding the name is [RG-3](../RG-3-target-naming/group.md); this group only
decides where the file goes.
