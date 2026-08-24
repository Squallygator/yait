# RG-7 — Safety and reversibility

The rules that exist because this tool rewrites irreplaceable family photographs.
Most of them come straight from the `dvd-tools` audit, where five findings could
have destroyed originals.

These are not quality-of-life features. They are the reason the tool is allowed
to touch anything at all.

## Rules

| Rule | Status | Decides |
|---|---|---|
| `UC-49-atomic-write-survives-interruption` | ▶ | Temp file then replace — a crash never truncates an original |
| `UC-50-journal-written-ahead` | ▶ | One flushed line per operation, before it happens |
| `UC-51-undo-restores-bit-for-bit` | ▶ | The round trip is exact, not approximate |
| `UC-52-path-confinement` | ▶ | A path from a CSV or a journal cannot escape the collection |
| `UC-53-never-overwrite` | ▶ | An occupied destination is an error, not a suffix |
| `UC-34-long-path-windows` | ▶ | Paths beyond 260 characters still work |

## Why a journal entry precedes its operation

`dvd-tools` wrote its journal once, after the whole batch. A crash at file 19 000
left 19 000 files moved and no way back. The entry must be on disk, flushed,
before the operation it describes — that is the difference between a log and a
recovery mechanism.
