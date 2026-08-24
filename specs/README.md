# Executable specifications

Every behaviour of YAIT is a **rule** living in this directory. Not in the code,
not in a ticket, not in someone's head. If it is not written here, it does not
exist — and if it is written here, a test proves it.

## Anatomy of a rule

```
specs/RG-1-date-resolution/RG-1.2-folder-dates/UC-14-deepest-folder-wins/
├── rule.md         the rule, why it exists, and the decision behind it
├── rule.feature    one Gherkin scenario, written by hand in business language
├── samples.yaml    how to build this rule's example files — technical only
└── files/          the generated examples, committed
```

Four artefacts, always. `tools/check_specs.py` fails the build if one is missing.

**Target shape: one rule, one example, one acceptance test.** When a rule needs
several, it usually hides two rules. `rule.md` must then say why it does not.

## Who is the source of truth

| Artefact | Written by | Answers |
|---|---|---|
| `rule.md` | a human | *What* the rule is and *why*. **The source of truth.** |
| `rule.feature` | a human | *How* it is proven, in business language |
| `samples.yaml` | a human | *How* the example files are built. Nothing else. |
| `files/` | `tools/build_samples.py` | The example files themselves |

Nothing is generated from anything else. `rule.feature` and `samples.yaml` meet
through **file names**: the scenario names a file, the recipe builds that file.

This separation is deliberate. An earlier design had one big manifest generating
the scenarios; it would have grown without limit and, worse, it would have made a
technical fixture file the source of functional truth. The rule comes first.

## The reference rule

[`RG-1-date-resolution/RG-1.2-folder-dates/UC-14-deepest-folder-wins/`](RG-1-date-resolution/RG-1.2-folder-dates/UC-14-deepest-folder-wins)
is the worked example. Read it before writing your first rule: it shows the
expected depth of the `## Why` section, how `## Scope` fences a rule off from its
neighbours, and why its example was chosen so that a wrong implementation cannot
pass by accident.

> Its `files/` directory does not exist yet — the generator arrives in `US-00-04`
> and `US-00-05`. This is the one place in the corpus where the four-artefact
> rule is knowingly unmet, and it closes with the generator.

## Polarity: an exclusion is a rule, not a gap

Every rule declares one of exactly two states in its `## Decision` block:

| | Status | The scenario asserts… |
|---|---|---|
| **▶** | `Enforced` | the behaviour obtained when the rule applies |
| **⊘** | `Assumed exclusion` | the **fallback** behaviour, and that the case is deliberately not interpreted |

There is no third state. **"Not implemented yet" is not a status.** A case we
have identified and chosen not to handle is a decision, and it is specified like
any other: rule, scenario, sample, and a **green** acceptance test.

An exclusion never says "we cannot read epoch timestamps". It says *"an epoch
timestamp in `FB_IMG_1288000000.jpg` is ignored, and the date comes from the
parent folder instead"* — and proves it.

### Reversing a decision

The day we decide to exploit a case previously excluded, the mechanism is forced:

1. the exclusion's acceptance test **turns red** — the change cannot pass unnoticed;
2. the exclusion's rule folder is **deleted**, not amended;
3. an enforced rule replaces it, with its own example and test;
4. the git diff carries the deletion: that is the trace of the change of doctrine.

Never edit an exclusion into an enforcement in place. The deletion is the record.

## Adding a rule

1. Pick the group. Rule identifiers are **flat and permanent**: `UC-14` keeps its
   number forever, even if it moves to another group. Grouping lives in the tree,
   never in the number.
2. Copy `_templates/` into `RG-x-…/RG-x.y-…/UC-nn-slug/`.
3. Write `rule.md` first — including the `## Decision` block. If you cannot state
   the rationale, the rule is not ready.
4. Write `rule.feature`. Business language: no file formats, no function names,
   no "the parser". Someone who has never opened the code must be able to judge
   whether the scenario is right.
5. Describe the example files in `samples.yaml`, then run
   `python tools/build_samples.py`. **Never place a file into `files/` by hand.**
6. Reference the rule from at least one User Story.

## Step vocabulary

Scenarios draw on a deliberately small vocabulary, implemented once in
`tests/acceptance/steps/`. Reuse it; extend it only when a genuinely new kind of
assertion appears, and add the new step to this table in the same commit.

```gherkin
Given the collection of "UC-14-deepest-folder-wins"

When the media "<relative/path.jpg>" is inspected
When the collection is inventoried

Then its resolved date is "YYYY-MM-DD"
Then it has no resolved date
And the date comes from "<source>"
And the date does not come from "<source>"
And the date precision is "<day|month|year|none>"
And it is classified as "<image|video|archive|sidecar|junk|unreadable>"
And its target name is "<name.ext>"
```

`<source>` is one of: `file-name`, `folder-name`, `embedded-metadata`,
`sidecar`, `none`. It is the answer to *"why this date?"* and every scenario that
resolves a date must assert it — a right date obtained for the wrong reason is a
bug waiting for the next batch of DVDs.

## Sample recipes

`samples.yaml` is purely technical. It says how to make bytes, never what they
should produce.

```yaml
version: 1

files:
  # An image derived from the seed photograph.
  - path: "2002-07-20 Wedding at Arras/18-07-2002/026-the-couple.jpg"
    source: seed
    width: 480          # optional, defaults to the small standard size
    exif: {}            # no metadata at all — forces resolution by path

  # An image carrying a capture date.
  - path: "holidays/IMG_0042.JPG"
    source: seed
    exif:
      DateTimeOriginal: "2006-08-29 09:43:38"

  # An artefact forged byte by byte — no encoder, no third-party content.
  - path: "holidays/MVI_0027.AVI"
    source: forge
    kind: riff-idit
    params:
      idit: "Tue Aug 29 09:43:38 2006"
```

Available `kind` values are documented in `_templates/samples.yaml`.

Paths may contain directories: the folder names are usually the point of the
rule. Accents, spaces and ampersands are welcome — the real archive is full of
them, and they must not be the thing that breaks.

## What the corpus may not contain

- **No real person's name, no real private event.** Cases observed in the private
  reference archive are transposed onto the seed with neutral wording.
- **No third-party content.** Everything derives from `_seed/river.jpg` (CC0) or
  is forged. See [LICENSE](LICENSE).
- **Nothing heavy.** Samples exist to carry a filename, a folder and a few
  metadata fields; the pixels almost never matter. CI enforces a size budget.
