# CLAUDE.md — YAIT project contract

Read this file fully before touching anything. Then read the User Story you were
assigned (`docs/10-features/`) and every `UC-*` rule it references (`specs/`).

Implementation is delegated batch by batch to separate sessions. This file is the
only context guaranteed to be loaded every time. It carries the **non-negotiable
structural decisions**; it does not duplicate the documentation, it points at it.

---

## What this is

YAIT (YetAnotherImageTools) is a local-first photo and video archive normaliser:
a browser UI backed by a local FastAPI service. It resolves a capture date for
every media file, renames, reorganises, and edits EXIF/XMP metadata.

It is a rewrite of `dvd-tools`, whose audit produced 36 findings — 5 of which
could destroy irreplaceable photos. Read
`docs/00-project/08-lessons-from-dvd-tools.md` once. **Do not reintroduce them.**

---

## Where authority lives

| Question | Authoritative source |
|---|---|
| What a business rule says | `specs/RG-*/UC-*/rule.md` — **never** the code |
| How a rule is proven | `specs/RG-*/UC-*/rule.feature` |
| Why a technical choice was made | `docs/adr/ADR-*.md` |
| What to build right now | the assigned US fiche in `docs/10-features/` |
| Which rules exist and their status | `docs/00-project/10-decision-log.md` (derived) |

This file is a digest. On conflict, the sources above win — and you fix this file
in the same commit.

---

## Non-negotiable — architecture

- `domain/` imports **no** framework, **no** I/O, **no** `os`, **no** Pillow.
  Dependency rule: `interface` -> `application` -> `domain`. Never the reverse.
- The domain declares its needs as `Protocol` classes in `domain/ports/`;
  `infrastructure/` implements them. A new I/O need means a new port, not an import.
- **Every module must be importable without optional dependencies installed.**
  Dependency checks belong in `main()`, never at module level. (In `dvd-tools`,
  a module-level `raise SystemExit` made it impossible to unit-test a regex
  without installing Pillow — finding #24.)
- Business rules live in the domain, not in routers, not in the front-end.

## Non-negotiable — data safety

This tool rewrites irreplaceable family photos. These are not suggestions.

- **Never write in place.** Use `atomic_write` / `safe_move` only: temp file then
  `os.replace`. A crash mid-write must never truncate an original.
- **Journal before acting.** One JSONL line per operation, flushed immediately.
  Never accumulate the log in memory and write it at the end of the batch.
- **Never overwrite.** An occupied destination is an error, not a `~2` fallback.
- **Every path coming from outside** (CSV cell, journal entry, API payload) goes
  through `PathGuard` and must resolve inside the collection root.
- **Dry-run is the default.** Writing is always the explicit opt-in.
- **Never re-encode an image.** Rebuild header segments only; the compressed
  stream is copied byte for byte.
- **`mtime` is never a date source.** On a copied tree it is the copy date. See `UC-37`.

## Non-negotiable — specification by example

Every behaviour is a rule under `specs/`, with four artefacts:
`rule.md`, `rule.feature`, `samples.yaml`, `files/`.
Target shape: **1 rule -> 1 example -> 1 acceptance test.**

- Each rule carries a polarity in its `## Decision` block:
  **`Enforced`** or **`Assumed exclusion`**. There is no "not yet implemented" state.
- An assumed exclusion has a **green** acceptance test asserting the *fallback*
  behaviour. It states what happens, not what is missing.
- To reverse a decision: the exclusion's test goes **red** -> **delete** the rule
  folder -> add the enforced rule with its own example and test. Never silently
  amend an exclusion. The git diff is the trace of the doctrine change.
- **Never hand-write files into `files/`.** Edit `samples.yaml`, then run
  `python tools/build_samples.py`.
- New behaviour without a rule is out of scope. Ask; do not improvise.

---

## Conventions

- **IDs**: Feature `F03` · Story `US-03-05` · Task `T-03-05-02` ·
  Rule `UC-14-deepest-folder-wins` · Legacy finding `#6`
- **English everywhere**: code, docs, Gherkin, API messages, UI labels, commits.
  (French month names inside date patterns are *data*, not code language.)
- **Typing**: `mypy --strict` passes. No bare `dict` records, no magic strings —
  use dataclasses and `Enum`.
- **Errors**: never `except Exception: pass`. Catch precisely; log with context.
  A permission error must not silently become "no date found".
- **Output**: data on stdout, diagnostics on stderr, through `logging`.
- **Front-end**: vanilla ESM, no bundler, no npm, no CDN. Use `textContent`;
  never build DOM by string concatenation into `innerHTML`.

## Dependencies

Runtime dependencies are frozen: **Pillow, piexif, tzdata, FastAPI, Uvicorn, Pydantic**.

Adding one requires an ADR merged first. **Never vendor a library** — `dvd-tools`
shipped a copy of piexif without its MIT licence file, which is a licence
violation in a public repository (finding #26).

## Git

- One branch per US: `feat/US-03-05-folder-dates`
- Conventional commits, scoped by US: `feat(US-03-05): resolve dates from folder names`
- Annotated tag `US-03-05` on `main` after merge
- CI must be green before merge
- Never commit generated artefacts, except `specs/**/files/` which are the
  reproducible corpus

---

## Definition of Done — run before claiming completion

```bash
ruff check . && mypy src && pytest -q --cov=src/yait --cov-fail-under=85
python tools/check_specs.py
python tools/build_samples.py --check
```

Plus: every `UC-*` referenced by the US is green, and the US task list is fully
checked. Report failures with their output; never mark work done on a red or
skipped test.

---

## Do not

- **Do not touch `C:\Users\pasca\Pictures\DVD`.** It is the private reference
  archive, read-only, and never a test target. Tests write to `tmp_path` or to
  the generated corpus.
- **Do not commit the real archive**, nor any personal name, into `specs/`,
  `docs/` or `tests/`. The corpus is generated from a single seed image.
- **Do not widen the scope of a US.** Out-of-scope findings are noted in the US
  fiche and become their own story.
- **Do not mark work done with a red or skipped test.**
