# TODO

Vue de pilotage. Une ligne par feature, les lots en sous-liste.
États : ⬜ à faire · ⌛ en cours · ✅ terminé

---

## Lot 0 — Corpus et pretotype

- ⌛ **F00** — Specs corpus & pretotype ([🔗](F00-specs-corpus-and-pretotype/overview.md))
  - ✅ Planification [🔗](F00-specs-corpus-and-pretotype/Plan/F00-plan.md) **(25/08/2026)**
  - ✅ `US-00-01` Repository bootstrap [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-01-repository-bootstrap.md) **(25/08/2026)**
  - ✅ `US-00-02` Seed photograph [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-02-seed-photograph.md) **(25/08/2026)**
  - ✅ `US-00-03` Specs structure [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-03-specs-structure.md) **(25/08/2026)**
  - ✅ `US-00-04` Sample generator — images [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-04-sample-generator-images.md) **(25/08/2026)**
  - ⬜ `US-00-05` Sample generator — forged artefacts [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-05-sample-generator-forged.md)
  - ⬜ `US-00-06` Write RG-1 rules [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-06-write-rg1-rules.md)
  - ⬜ `US-00-07` Write RG-2 to RG-7 rules [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-07-write-rg2-rg7-rules.md)
  - ⬜ `US-00-08` Spec guards in CI [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-08-spec-guards.md)
  - ⬜ `US-00-09` Design system [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-09-design-system.md)
  - ⬜ `US-00-10` Screen — Home [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-10-screen-home.md)
  - ⬜ `US-00-11` Screen — Collection summary [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-11-screen-collection-summary.md)
  - ⬜ `US-00-12` Screen — Inventory [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-12-screen-inventory.md)
  - ⬜ `US-00-13` Screen — Media detail [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-13-screen-media-detail.md)
  - ⬜ `US-00-14` Screen — Rename plan [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-14-screen-rename-plan.md)
  - ⬜ `US-00-15` Screen — Collisions [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-15-screen-collisions.md)
  - ⬜ `US-00-16` Screen — Organize [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-16-screen-organize.md)
  - ⬜ `US-00-17` Screen — Metadata editor [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-17-screen-metadata-editor.md)
  - ⬜ `US-00-18` Screen — Job progress [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-18-screen-job-progress.md)
  - ⬜ `US-00-19` Screen — History and undo [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-19-screen-history-undo.md)
  - ⬜ `US-00-20` Screens — Empty and error states [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-20-screen-empty-and-error-states.md)
  - ⬜ `US-00-21` Clickable prototype [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-21-clickable-prototype.md)
  - ⬜ `US-00-22` Pretotyping review **(point d'arrêt)** [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-22-pretotyping-review.md)

---

## Lot 1 — Walking skeleton, lecture seule

> Fiches de lot à écrire au démarrage de chaque feature — le backlog n'est figé qu'après `US-00-22`.

- ⬜ **F01** — Foundation & launcher
  - ⬜ `US-01-01` Repository skeleton, pyproject, ruff, mypy, pytest, CI Ubuntu + Windows
  - ⬜ `US-01-02` FastAPI app, `/health`, OpenAPI, RFC 9457 error handler
  - ⬜ `US-01-03` Configuration (pydantic-settings)
  - ⬜ `US-01-04` Launcher `yait.ps1` / `yait.sh`
  - ⬜ `US-01-05` Structured logging — diagnostics on stderr
  - ⬜ `US-01-06` UI shell matching the mockups
- ⬜ **F02** — Collections
  - ⬜ `US-02-01` Enter and validate a collection path (confinement, long Windows paths)
  - ⬜ `US-02-02` Recent collections
  - ⬜ `US-02-03` Home and Summary screens wired
- ⬜ **F03** — Inventory & date resolution
  - ⬜ `US-03-01` Pure domain model — testable without Pillow
  - ⬜ `US-03-02` Dates written in the filename (RG-1.1)
  - ⬜ `US-03-03` Dates carried by folder names (RG-1.2)
  - ⬜ `US-03-04` Dates read from file content (RG-1.3)
  - ⬜ `US-03-05` Arbitration and refusals (RG-1.4)
  - ⬜ `US-03-06` File classification (RG-2)
  - ⬜ `US-03-07` Filesystem walk, exclusions, fingerprints
  - ⬜ `US-03-08` `scan_collection` + fingerprint-invalidated cache
  - ⬜ `US-03-09` Scan API + jobs + SSE
  - ⬜ `US-03-10` Inventory screen wired
  - ⬜ `US-03-11` Media detail screen wired

---

## Lot 2 — Écritures

- ⬜ **F07** — Journal & undo *(livré avant toute écriture)*
  - ⬜ `US-07-01` Journal port + write-ahead JSONL adapter
  - ⬜ `US-07-02` Legacy `dvd-tools` journal reader
  - ⬜ `US-07-03` `undo_operation` + coherence check
  - ⬜ `US-07-04` History API + screen
- ⬜ **F04** — Renaming
  - ⬜ `US-04-01` `atomic_write` / `safe_move` / `PathGuard`
  - ⬜ `US-04-02` Naming policy (RG-3)
  - ⬜ `US-04-03` Collisions (RG-4)
  - ⬜ `US-04-04` Frozen plan with fingerprints
  - ⬜ `US-04-05` Move ordering (cycles, case-only renames)
  - ⬜ `US-04-06` Journalled, resumable execution
  - ⬜ `US-04-07` Rename API
  - ⬜ `US-04-08` Rename plan and Collisions screens wired
- ⬜ **F05** — Organizing
  - ⬜ `US-05-01` Layouts (RG-6)
  - ⬜ `US-05-02` Flatten
  - ⬜ `US-05-03` Global uniqueness guard
  - ⬜ `US-05-04` Empty folder pruning
  - ⬜ `US-05-05` Organize API + screen

---

## Lot 3 — Métadonnées

- ⬜ **F06** — Metadata
  - ⬜ `US-06-01` Read existing metadata, decode `XP*`
  - ⬜ `US-06-02` Label deduction
  - ⬜ `US-06-03` Review sheet — statuses computed server-side only
  - ⬜ `US-06-04` Drift detection
  - ⬜ `US-06-05` Atomic EXIF + XMP write, no re-encoding
  - ⬜ `US-06-06` Original block backup
  - ⬜ `US-06-07` Audit / apply API
  - ⬜ `US-06-08` Metadata editor wired
  - ⬜ `US-06-09` CSV import/export compatible with v1

---

## Lot 4 — Durcissement et distribution

- ⬜ **F08** — Quality & safety
  - ⬜ `US-08-01` Path attack tests
  - ⬜ `US-08-02` Schemathesis contract testing
  - ⬜ `US-08-03` Private non-regression campaign against `dvd-tools`
  - ⬜ `US-08-04` Robustness — interruption, full disk, locked file
  - ⬜ `US-08-05` Enriched OpenAPI
  - ⬜ `US-08-06` Every production anomaly becomes a new rule
- ⬜ **F09** — Distribution
  - ⬜ `US-09-01` Docker reassessment
  - ⬜ `US-09-02` Cold install
  - ⬜ `US-09-03` Public repository finishing touches
