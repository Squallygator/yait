# RG-1.4 — Arbitration and refusals

Sources disagree. This group decides who wins, and — just as importantly — what
is **refused** as a date source.

The refusals are the hard-won part. Each one exists because a plausible-looking
source produced a wrong answer on a real archive, and each is an assumed
exclusion carrying a green test: the day one of them is reversed, that test turns
red and the rule must be deleted rather than quietly amended.

## Rules

| Rule | Status | Decides |
|---|---|---|
| `UC-36-source-priority-order` | ▶ | The full ladder, end to end |
| `UC-19-clock-drift-guard` | ▶ | Metadata far from the folder date means an unset camera clock |
| `UC-29-no-date-at-all` | ▶ | What a file gets when nothing answers |
| `UC-30-year-bounds` | ▶ | The plausible year range, stated once |
| `UC-08-long-digit-run-is-not-a-date` | ⊘ | `received_862666160799536` yields nothing |
| `UC-09-epoch-timestamp-ignored` | ⊘ | An epoch stamp dates the download, not the shot |
| `UC-37-mtime-is-never-a-date-source` | ⊘ | On a copied tree it is the copy date |
| `UC-56-companion-json-ignored` | ⊘ | Google Takeout sidecars |
| `UC-57-gps-not-used-for-dating` | ⊘ | |
| `UC-60-timezone-not-inferred-from-gps` | ⊘ | Local wall-clock time is kept as written |
