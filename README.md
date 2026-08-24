# YAIT — YetAnotherImageTools

Local-first normaliser for photo and video archives — the kind you get when you
finally rip a stack of family CDs and DVDs and end up with thirty folders named
`2006-2`, `IMG_0047.JPG` and `MVI_0027.THM`.

YAIT resolves a capture date for every file, renames them to a sortable
`YYYY-MM-DD-name.ext`, reorganises the tree, and fills in EXIF/XMP metadata —
through a browser UI backed by a local API. Nothing leaves your machine.

> **Status: early construction.** The specification corpus and the screen
> pretotypes come first; the application follows. See `docs/00-project/07-roadmap.md`.

## Why another one

Because the interesting part is not renaming files, it is **deciding which date
to trust**. A camera whose clock was never set, a folder named `22 JUILLET 2002`,
a WhatsApp export, a Windows Phone timestamp, a `.THM` thumbnail that is the only
witness of when a video was shot — each is a rule, and each rule is written down,
illustrated by an example, and covered by a test.

## Design commitments

- **Dry-run by default.** Writing is always an explicit opt-in.
- **Nothing is overwritten.** Ever.
- **Every operation is journalled before it happens**, and can be undone.
- **Images are never re-encoded** — only header segments are rebuilt.
- **`mtime` is never used as a capture date.** On a copied tree it is the copy date.
- **Partial dates stay partial.** `2010-12-00` means "December 2010, day unknown",
  not an invented 1st of the month.

## Specification by example

Every behaviour lives in `specs/` as a self-contained rule:

```
specs/RG-1-date-resolution/RG-1.2-folder-dates/UC-14-deepest-folder-wins/
├── rule.md         the business rule and why it exists
├── rule.feature    one Gherkin scenario, written by hand
├── samples.yaml    how to build this rule's sample files
└── files/          the generated samples, committed
```

Rules are either **enforced** or **assumed exclusions** — a case we identified and
deliberately chose not to interpret. Exclusions carry a *green* test asserting the
fallback behaviour, so reversing the decision later turns a test red and forces the
change to be explicit.

The sample corpus is generated from a **single seed photograph** plus forged
lightweight artefacts (AVI, MP4, ZIP, truncated JPEG). It is reproducible on any
machine and contains no third-party content.

## Getting started

Nothing to run yet. Once the first batch lands:

```bash
./yait.sh          # Linux / macOS / Git Bash
.\yait.ps1         # Windows PowerShell
```

## Licence

Code: [MIT](LICENSE). Sample corpus under `specs/`: [CC0](specs/LICENSE).
