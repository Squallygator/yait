# Contributing to YAIT

Read [`CLAUDE.md`](CLAUDE.md) first — it holds the structural decisions that apply
to every change, whoever or whatever writes it.

## The unit of work is a User Story

Work is organised as Feature -> User Story -> Task:

| Level | Format | Example |
|---|---|---|
| Feature | `F<nn>` | `F03` |
| User Story | `US-<nn>-<mm>` | `US-03-05` |
| Task | `T-<nn>-<mm>-<pp>` | `T-03-05-02` |
| Business rule | `UC-<nn>-<slug>` | `UC-14-deepest-folder-wins` |

One branch per US (`feat/US-03-05-folder-dates`), conventional commits scoped by
US (`feat(US-03-05): ...`), annotated tag `US-03-05` on `main` after merge.

## Changing behaviour means changing a rule

Code is never the source of truth for behaviour. To change what the tool does:

1. Edit or add the rule in `specs/RG-*/UC-*/rule.md`, including its `## Decision` block.
2. Write the Gherkin scenario in `rule.feature` — by hand, in business language.
3. Describe the sample files in `samples.toml`, then run `python tools/build_samples.py`.
   Never hand-place files into `files/`.
4. Implement, and make the acceptance test pass.

To **reverse an assumed exclusion**, delete its rule folder and add the enforced
rule. Do not amend the exclusion in place — the deletion is the trace.

## Before opening a pull request

```bash
ruff check . && mypy src && pytest -q --cov=src/yait --cov-fail-under=85
python tools/check_specs.py
python tools/build_samples.py --check
```

`check_specs.py` enforces the structure: every rule has its four artefacts, a
decided polarity, at least one scenario, at least one passing acceptance test, at
least one referencing User Story, and no orphan sample.

## Privacy

The reference archive used to derive real-world cases is private and never
committed. Sample data must not contain the name of a real person or a real
private event. If you need a new case, transpose it onto the seed image.
