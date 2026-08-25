# YAIT — YetAnotherImageTools · Plan directeur

## Contexte

`dvd-tools` (3 CLI *vibe-codées* : `dvdphotos.py`, `dvdmeta.py`, `csvedit.js`) fonctionne et
encode de vraies leçons métier, mais l'audit conduit juste avant a relevé **36 findings**, dont
5 pouvant détruire des photos irremplaçables et 3 rendant le mode simulation mensonger.

Plutôt que de le réparer, on repart d'une application neuve : **YAIT**, 100 % Python, une IHM
navigateur unique adossée à une web API locale, conçue par un développeur fullstack adepte du
DDD et du software craftsmanship.

**Ce plan n'est pas le livrable.** Le livrable est un corpus documentaire multi-fichiers
(Feature / User Story / Task + ADR + spécifications exécutables + maquettes HTML), exécuté
ensuite **US par US, dans des sessions Claude Code séparées**.

> **Note de langue.** Ce fichier de plan reste en français — c'est notre document de travail.
> **Tout le livrable est produit en anglais** : documentation, ADR, fiches US, Gherkin, écrans,
> identifiants de code, messages d'API et libellés d'IHM. Motif : publication publique visée.

### Décisions arrêtées avec l'utilisateur

| Sujet | Décision |
|---|---|
| Emplacement | **`C:\Repo\yait`** — hors de l'arborescence photo. |
| Publication | **GitHub public, licence MIT.** Doc, écrans et code **en anglais**. |
| Lancement | **Natif uniquement** (`yait.ps1` / `yait.sh` + venv + uvicorn). Docker **étudié et différé** (ADR-003, feature F09). |
| Sélection du dossier | **Saisie / collage du chemin**, validé côté API, historique des collections récentes. |
| Front-end | **Vanilla ESM zéro-build**, servi en statique par FastAPI. Aucun npm, aucun bundler. |
| Méthode produit | **Pretotyping** : les maquettes constituent le **lot 0**, avec un point d'arbitrage qui peut rebattre la priorisation. |
| Méthode spec | **Specification by Example** : 1 règle métier → 1 exemple → 1 test d'acceptance. |
| Corpus de test | **Généré depuis une image seed unique** + artefacts forgés, embarqué dans le dépôt. |
| Premier lot de code | **Walking skeleton en lecture seule**. **Aucune écriture disque avant le lot 2.** |

---

## Conventions de numérotation

| Niveau | Format | Exemple | Porté par |
|---|---|---|---|
| **Feature** | `F<nn>` | `F03` | un répertoire `docs/10-features/F03-inventory/` |
| **User Story** | `US-<nn>-<mm>` | `US-03-05` | une fiche `US-03-05-folder-dates.md` |
| **Task** | `T-<nn>-<mm>-<pp>` | `T-03-05-02` | une ligne à cocher **dans** la fiche US |
| **Use case / règle métier** | `UC-<nn>-<slug>` | `UC-14-deepest-folder-wins` | un répertoire de spécification exécutable |
| **Finding dvd-tools** | `#<n>` | `#6` | l'audit initial, référencé en traçabilité |

Branche = `feat/US-03-05-folder-dates` · Tag = `US-03-05` · Commit = `feat(US-03-05): …`

Les numéros d'UC déjà attribués **ne bougent plus** : ce sont des identifiants stables. Le
regroupement est porté par l'arborescence, pas par le numéro — un UC peut changer de groupe sans
changer d'identité.

---

## Specification by Example — la structure de vérité

**Ce qui change par rapport à la version précédente du plan.** Un `manifest.yaml` unique
générant les scénarios Gherkin était une fausse bonne idée : il aurait grossi sans limite, et
surtout il aurait fait d'un fichier technique de fixtures la source de vérité fonctionnelle.
C'est l'inverse qu'il faut.

**La règle métier est la source.** Chaque UC est une unité autonome contenant *tout* ce qui la
concerne — l'énoncé, l'exemple, le test, les fichiers :

```
specs/
├─ README.md                          comment lire et ajouter une règle
├─ RG-1-date-resolution/
│  ├─ group.md                        intention du groupe, règles qu'il contient
│  ├─ RG-1.2-folder-dates/
│  │  ├─ group.md
│  │  └─ UC-14-deepest-folder-wins/
│  │     ├─ rule.md          ★ l'énoncé métier, son POURQUOI, ses limites, ses contre-exemples
│  │     ├─ rule.feature     ★ Gherkin ÉCRIT À LA MAIN — 1 scénario, langage fonctionnel
│  │     ├─ samples.yaml     ★ recette de fabrication des échantillons de CE seul UC
│  │     └─ files/           ★ les échantillons générés, commités
```

**Séparation des rôles, sans génération croisée :**

| Artefact | Écrit par | Rôle |
|---|---|---|
| `rule.md` | un humain | La règle et sa justification. **Source de vérité fonctionnelle.** |
| `rule.feature` | un humain | Le scénario d'acceptance, en langage métier. Ne dérive de rien. |
| `samples.yaml` | un humain | **Uniquement** comment fabriquer les fichiers d'exemple. Purement technique. |
| `files/` | le générateur | Sortie reproductible de `samples.yaml`. |

Le `.feature` et le `samples.yaml` se rejoignent par **le nom des fichiers**, pas par
génération. Le pas à pas Gherkin lit `files/` ; personne ne génère personne.

**Invariants vérifiés en CI** — ce sont eux qui empêchent la structure de pourrir :
- tout `UC-*/` contient les quatre artefacts ;
- tout `rule.feature` a **au moins un scénario** et **au moins un test d'acceptance** qui passe ;
- tout `UC` porte une **polarité décidée** (voir ci-dessous) — aucune valeur « à faire » possible ;
- tout `UC` est référencé par **au moins une US** ;
- toute US référence **au moins un UC** ;
- tout fichier de `files/` est mentionné dans au moins un `.feature` (pas d'échantillon orphelin).

Idéal visé : **1 règle → 1 exemple → 1 TA**. Quand une règle en exige plusieurs, c'est souvent
le signe qu'elle en cache deux — le `rule.md` doit alors le justifier explicitement.

### Polarité : une exclusion est une règle, pas un trou

Un cas identifié mais volontairement non traité **n'est pas un manque** : c'est une décision, et
elle se spécifie comme les autres. Deux polarités, jamais de troisième :

| | Polarité | Le scénario affirme… |
|---|---|---|
| **▶** | **Enforced** | … le comportement attendu quand la règle s'applique. |
| **⊘** | **Assumed exclusion** | … **le comportement de repli**, et que le cas n'est délibérément *pas* interprété. |

Une exclusion assumée a donc, exactement comme une règle positive : un `rule.md`, un scénario
Gherkin, un échantillon, et **un test d'acceptance vert**. Exemple : `UC-09` n'affirme pas
« on ne sait pas lire les epoch » — il affirme *« un horodatage epoch dans le nom `FB_IMG_…` est
ignoré, et la date provient du répertoire parent »*, avec l'échantillon qui le prouve.

**C'est ce qui rend le revirement sûr.** Le jour où l'on décide d'exploiter un cas jusque-là
exclu, la mécanique est forcée :

1. le test d'acceptance de l'exclusion **passe au rouge** — impossible de rater le changement ;
2. la règle négative doit être **supprimée** du dépôt, pas amendée ;
3. une règle positive la remplace, avec son propre exemple et son propre TA ;
4. l'historique Git porte la suppression : la trace du changement de doctrine est le diff.

Le `rule.md` porte donc un bloc de décision obligatoire :

```markdown
## Decision
Status:      Assumed exclusion (⊘)
Decided on:  2026-08-24                    Owner: <auteur>
Rationale:   Un horodatage epoch date l'ENREGISTREMENT du fichier, pas la prise de vue.
             Observé sur l'archive : l'un d'eux décodait à la veille pour une photo de 2010.
Fallback:    La résolution poursuit à l'échelon suivant (répertoire parent).
Revisit if:  Un lot arrive où l'epoch est la seule source disponible ET s'avère fiable.
Supersedes:  —
```

`tools/check_specs.py` publie l'index consolidé dans `docs/00-project/10-decision-log.md` :
toutes les règles, leur polarité, leur date de décision et leur condition de réexamen, sur une
seule page. C'est un index dérivé — la vérité reste dans les `rule.md`.

### Corpus d'échantillons (ADR-013)

- **Seed** : la photo personnelle de l'utilisateur (rivière et arbres), copie déjà redimensionnée.
  **EXIF intégralement supprimé dès la première tâche** — GPS, modèle, numéro de série, date
  d'origine. Motif double : hygiène sur un dépôt public, et correction — un champ résiduel ferait
  dépendre les tests d'une donnée invisible. Le générateur ré-injecte uniquement ce que chaque
  UC exige.
- **Autres formats : forgés, légers, libres de droit par construction** — aucun contenu tiers.
  AVI avec chunk RIFF `IDIT` (~100 octets), MP4 avec atome `moov/mvhd`, `.THM` (un JPEG dérivé du
  seed), `.zip`, JPEG tronqué en plein scan (secteur de CD abîmé), fichier de 0 octet, EXIF avec
  IFD `1st` décrivant une miniature absente, `Thumbs.db` / `Picasa.ini` / `desktop.ini`.
  Aucune dépendance externe, pas de ffmpeg.
- **Licence** : `specs/LICENSE` en **CC0** — MIT n'a pas de sens pour une photo.
- **Garde-fous CI** : budget de taille global ; régénération et comparaison du **manifeste**
  consolidé (chemins, EXIF, dimensions) et **non des octets** — l'encodeur JPEG de Pillow n'est
  pas stable d'une version à l'autre.
- **L'archive réelle reste locale**, jamais commitée (elle contient des noms de personnes et des
  événements privés), référencée par variable d'environnement, et sert uniquement à la campagne
  de non-régression contre `dvd-tools` — tests `@pytest.mark.private`, **skippés** en CI.

---

## Backlog des règles métier

Sept groupes, **60 règles**, chacune décidée : **▶** appliquée, **⊘** exclusion assumée.
Aucune n'est « à faire » — ce qui n'a pas de règle n'est pas dans le backlog.

### RG-1 · Date resolution *(cœur métier)*

**RG-1.1 — Dates written in the filename**
▶ `UC-01` human-date-in-name *(prime sur l'EXIF, fonde l'idempotence)* · ▶ `UC-02` dropbox-camera-uploads ·
▶ `UC-03` whatsapp · ▶ `UC-04` android-img-vid-pano · ▶ `UC-05` screenshot · ▶ `UC-06` windows-phone ·
▶ `UC-07` yyyymmdd-embedded · ▶ `UC-10` french-month-in-filename · ▶ `UC-11` numeric-month-in-name ·
▶ `UC-12` year-only-in-name

**RG-1.2 — Dates carried by folder names**
▶ `UC-13` folder-date-ymd · ▶ `UC-14` deepest-folder-wins *(+ format JJ-MM-AAAA inversé)* ·
▶ `UC-15` folder-date-french-month · ⊘ `UC-16` batch-suffix-is-not-a-month *(`2006-2` → année seule)*

**RG-1.3 — Dates read from file content**
▶ `UC-17` exif-datetime-original · ▶ `UC-18` exif-absent · ▶ `UC-20` video-riff-idit ·
▶ `UC-21` video-mp4-mvhd · ▶ `UC-22` video-dated-by-thm-sidecar · ▶ `UC-23` zip-oldest-exif ·
⊘ `UC-54` raw-formats-not-inspected *(CR2/NEF/ARW : repli sur nom et répertoire)* ·
⊘ `UC-55` heic-not-inspected *(exigerait `pillow-heif` — contraire au zéro-dép)* ·
⊘ `UC-58` nested-zip-not-recursed *(un seul niveau d'archive)*

**RG-1.4 — Arbitration and guards**
▶ `UC-36` source-priority-order *(l'échelle complète, de bout en bout)* ·
▶ `UC-19` exif-clock-drift *(garde-fou `gap_days`)* · ▶ `UC-29` no-date-at-all *(comportement de repli)* ·
▶ `UC-30` year-bounds-are-decided *(bornes explicites et uniques)* ·
⊘ `UC-08` long-digit-run-is-not-a-date *(`received_862666160799536`)* ·
⊘ `UC-09` epoch-timestamp-ignored *(date l'enregistrement, pas la prise de vue)* ·
⊘ `UC-37` mtime-is-never-a-date-source *(sur une arborescence recopiée, c'est la date de copie)* ·
⊘ `UC-56` companion-json-ignored *(sidecars Google Takeout)* ·
⊘ `UC-57` gps-not-used-for-dating · ⊘ `UC-60` timezone-not-inferred-from-gps

### RG-2 · File classification
▶ `UC-24` unreadable-truncated · ▶ `UC-25` zero-byte-file · ▶ `UC-26` junk-files ·
▶ `UC-38` sidecar-is-not-junk *(un `.THM` survit tant que sa vidéo existe)* ·
⊘ `UC-59` duplicate-content-not-detected *(on dédoublonne les noms, pas les contenus)*

### RG-3 · Target naming
▶ `UC-28` originals-suffix · ▶ `UC-35` accents-and-ampersand ·
▶ `UC-39` date-token-removed-only-if-it-provided-the-date · ▶ `UC-40` illegal-chars-sanitised ·
▶ `UC-41` idempotent-on-rerun

### RG-4 · Collisions
▶ `UC-27` quality-ordering *(pixels, puis taille, puis heure, puis chemin)* ·
▶ `UC-42` uniqueness-is-global *(tous répertoires confondus)*

### RG-5 · Metadata deduction & writing
▶ `UC-32` label-from-folder-and-context · ▶ `UC-31` unknown-camera-prefix *(contexte préservé)* ·
▶ `UC-43` one-label-for-title-subject-comment · ▶ `UC-45` drift-detected-between-audit-and-apply ·
▶ `UC-44` exif-write-never-reencodes *(flux compressé identique au bit près)* ·
⊘ `UC-33` existing-fields-never-overwritten *(sauf `--overwrite` explicite)*

### RG-6 · Organizing
▶ `UC-46` organize-by-precision *(jour/mois → `YYYY/MM`, année → `YYYY/`, aucune → `_undated`)* ·
▶ `UC-48` empty-folders-pruned · ⊘ `UC-47` flatten-leaves-undated-in-place *(les envoyer sans
horodatage irait contre le but du mode à plat)*

### RG-7 · Safety & reversibility
▶ `UC-49` atomic-write-survives-interruption · ▶ `UC-50` journal-written-ahead ·
▶ `UC-51` undo-restores-bit-for-bit · ▶ `UC-52` path-confinement ·
▶ `UC-53` never-overwrite · ▶ `UC-34` long-path-windows

> Les 15 exclusions **⊘** sont ce qui distingue ce backlog d'une liste de fonctionnalités : chacune
> est un choix daté, justifié, testé — et **révocable par un test rouge**, jamais par un oubli.

---

## Architecture

### Principes

1. **Domaine pur** : `domain/` n'importe ni FastAPI, ni Pillow, ni `os`. Zéro I/O, zéro
   framework. Réponse directe au finding #24 — aujourd'hui il faut stuber `PIL` dans
   `sys.modules` rien que pour tester une regex.
2. **Ports & adapters** : le domaine déclare ses besoins (`MetadataReader`, `Journal`,
   `FileRepository`, `Clock`) ; l'infrastructure les implémente.
3. **Sûreté par construction** : toute écriture passe par `atomic_write`, toute opération par un
   journal write-ahead, tout chemin externe par `PathGuard`. Ce ne sont pas des options.
4. **Une seule implémentation de chaque règle.** Les statuts sont calculés **côté serveur** ;
   le front les affiche. Fin de la double implémentation Python/JS (#27, #28).
5. **Le plan est un artefact**, pas une suggestion : figé, empreinté, relu, puis rejoué (#7, #8).

### Bounded contexts

| BC | Responsabilité | Groupes de règles |
|---|---|---|
| **Inventory** | Parcourir, identifier, **résoudre la date**, tracer la source | RG-1, RG-2 |
| **Renaming** | Politique de nommage, collisions, plan figé, exécution | RG-3, RG-4 |
| **Organizing** | Rangement `YYYY/MM`, mise à plat, `_undated` | RG-6 |
| **Metadata** | Lecture/déduction/écriture EXIF-XMP, feuille de revue | RG-5 |
| **Journaling** | Journal write-ahead, annulation, historique | RG-7 |

### Arborescence cible

```
C:\Repo\yait\
├─ CLAUDE.md                 ★ contrat de projet, chargé à chaque session
├─ README.md · LICENSE (MIT) · CONTRIBUTING.md · .gitignore
├─ pyproject.toml            ruff · mypy strict · pytest · couverture
├─ yait.ps1 / yait.sh        lanceur : venv, port libre, navigateur, arrêt propre
├─ docs/                     documentation projet (anglais)
├─ specs/                    ★ spécifications exécutables : RG-*/UC-*/ (CC0)
├─ tools/build_samples.py    générateur déterministe, pilote les samples.yaml
├─ src/yait/
│  ├─ domain/                # pur — aucun import framework, aucun I/O
│  │  ├─ shared/             partial_date · status · precision · errors
│  │  ├─ inventory/          model · date_resolution/{name,folder,content,arbitration}
│  │  ├─ renaming/           naming_policy · collision · plan (aggregate)
│  │  ├─ organizing/         layout
│  │  ├─ metadata/           model · deduction · review (aggregate)
│  │  └─ ports/              file_repository · metadata_reader · metadata_writer · journal · clock
│  ├─ application/           use_cases/*.py · dto.py
│  ├─ infrastructure/
│  │  ├─ fs/                 walker · atomic · path_guard (chemins longs Windows)
│  │  ├─ exif/               pillow_reader · piexif_writer · jpeg_segments
│  │  ├─ video/              riff_idit · mp4_moov · ffprobe (optionnel, détecté)
│  │  ├─ journal/            jsonl_journal · legacy_reader (journaux dvd-tools v1)
│  │  └─ persistence/        recent_folders · plan_store · job_store · scan_cache
│  └─ interface/
│     ├─ api/                app · routers/ · schemas/ · errors (RFC 9457)
│     └─ web/                index.html · assets/ · components/ (web components ESM)
└─ tests/
   ├─ unit/ · integration/ · contract/
   ├─ acceptance/            pas-à-pas Gherkin, un module par RG
   └─ fixtures/legacy/       CSV et journaux dvd-tools v1
```

### Pile technique

| Besoin | Choix | Justification |
|---|---|---|
| API | **FastAPI + Uvicorn** | OpenAPI natif — « documentée norme OpenAPI » satisfait par construction. |
| Schémas | **Pydantic v2** | Validation en frontière, exemples injectés dans l'OpenAPI. |
| Erreurs | **RFC 9457 Problem Details** | Contrat d'erreur uniforme et documenté. |
| Images | **Pillow**, **piexif** *(dépendance PyPI, plus vendorisée)* | Le vendoring sans LICENSE était une violation (#26), inacceptable en dépôt public. |
| Fuseaux | **`tzdata` explicite** | Sous Windows, son absence dégradait les dates XMP en silence (#17). |
| Acceptance | **pytest-bdd** | Les `.feature` restent lisibles par un non-développeur. |
| Tests | pytest · httpx · **schemathesis** · pytest-cov | Contract testing de l'API contre son propre OpenAPI. |
| Qualité | **ruff** · **mypy strict** | |
| Traitements longs | `BackgroundTasks` + job store + **SSE** | Un scan de 20 000 fichiers ne tient pas dans une requête HTTP. |
| Front | **Vanilla ESM**, web components, grille virtualisée | Zéro build, zéro npm. |

---

## Documentation projet (`docs/`, en anglais)

```
docs/
├─ 00-project/
│  ├─ 01-vision.md · 02-ubiquitous-language.md · 03-architecture.md · 04-conventions.md
│  ├─ 05-test-strategy.md          pyramide, specification by example, contract testing
│  ├─ 06-git-workflow.md           branche/US, tag/US, conventional commits
│  ├─ 07-roadmap.md                lots, ordre des US, graphe de dépendances
│  ├─ 08-lessons-from-dvd-tools.md ★ le REX : pièges hérités, pourquoi, comment évités
│  ├─ 09-traceability.md           ★ matrice Finding ⇄ UC ⇄ US
│  └─ 10-decision-log.md           ★ index DÉRIVÉ : toutes les règles, polarité, réexamen
├─ adr/    ADR-001 → ADR-013
├─ 10-features/  F00-… → F09-…  (feature.md + fiches US)
└─ 20-mockups/   index.html + 12 écrans + assets/mockup.css
```

**ADR-003 — l'étude Docker.** *Décision : lancement natif, Docker reporté en F09.*
*Pour* : reproductibilité, isolation de Pillow/ffprobe, atout pour un dépôt public.
*Contre, ici* : les bind mounts Windows s'effondrent sur des dizaines de milliers de fichiers
(exactement la charge visée) ; le mapping `C:\Users\…` ⇄ `/photos` casse l'ergonomie de la saisie
de chemin retenue ; Docker Desktop est un prérequis lourd ; l'ouverture du navigateur depuis un
conteneur est bancale. *Réévaluation* : à la stabilisation, comme vecteur de distribution.

### Format imposé d'une fiche US

```markdown
# US-03-05 — Resolve a media date from a parent folder name

| Feature | F03 Inventory | Depends on | US-03-01 |
| Batch   | 1             | Branch     | feat/US-03-05-folder-dates |
| Size    | M             | Tag        | US-03-05 |

## Story            As a family archivist, I want … so that …
## Business rules   ▶ UC-13  ▶ UC-14  ▶ UC-15  ⊘ UC-16   ← chacun a son exemple et son TA vert
                    (les ⊘ comptent autant : leur test affirme le comportement de repli)
## Context          ADRs concernés · pitfalls dvd-tools hérités
## API contract     endpoint, schemas, error codes, OpenAPI excerpt
## Mockup           docs/20-mockups/xx.html
## Tasks
- [ ] T-03-05-01 …
- [ ] T-03-05-02 …
## Definition of Done
- [ ] Chaque UC listé a un `rule.feature` vert
- [ ] ruff · mypy · couverture ≥ 85 % · contract tests verts
```

---

## `CLAUDE.md` — le contrat de projet

Premier fichier du dépôt (tâche `T-00-01-01`), à la racine. L'implémentation étant déléguée lot
par lot à des sessions distinctes, potentiellement avec d'autres modèles, ce fichier est le seul
contexte garanti chargé à chaque fois. Il ne duplique pas la doc : il porte **les choix
structurels non négociables** et dit où trouver le reste.

Rédigé en **anglais**, comme le reste du dépôt public. Contenu prévu :

```markdown
# CLAUDE.md — YAIT project contract

Read this fully before touching anything. Then read the US you were assigned
(`docs/10-features/`) and every `UC-*` rule it references (`specs/`).

## What this is
Local-first photo/video archive normaliser. Browser UI + local FastAPI backend.
Rewrite of `dvd-tools`, whose audit produced 36 findings — see
`docs/00-project/08-lessons-from-dvd-tools.md`. Do not reintroduce them.

## Where authority lives
| Question | Authoritative source |
|---|---|
| What a business rule says | `specs/RG-*/UC-*/rule.md` — **never** the code |
| How a rule is proven | `specs/RG-*/UC-*/rule.feature` |
| Why a technical choice was made | `docs/adr/ADR-***.md` |
| What to build now | the assigned US fiche |
This file is a digest. On conflict, the sources above win — and you fix this file.

## Non-negotiable — architecture
- `domain/` imports **no** framework, **no** I/O, **no** `os`, **no** Pillow.
  Dependency rule: interface → application → domain. Never the reverse.
- The domain declares its needs as Protocols in `domain/ports/`; `infrastructure/`
  implements them. A new I/O need means a new port, not an import.
- Every module must be importable without optional dependencies installed.
  Dependency checks belong in `main()`, never at module level.

## Non-negotiable — data safety
This tool rewrites irreplaceable family photos. These are not suggestions.
- **Never write in place.** `atomic_write` / `safe_move` only: temp file + `os.replace`.
- **Journal before acting**, one JSONL line per operation, flushed. Never batch the log.
- **Never overwrite.** A busy destination is an error, not a `~2` fallback.
- **Every external path** (CSV cell, journal entry, API payload) goes through `PathGuard`.
- **Dry-run is the default.** Writing is the opt-in.
- **Never re-encode an image.** Header segments only; the compressed stream is copied.
- `mtime` is never a date source. See `UC-37`.

## Non-negotiable — specification by example
Every behaviour is a rule in `specs/`, with four artefacts: `rule.md`, `rule.feature`,
`samples.yaml`, `files/`. Target: 1 rule → 1 example → 1 acceptance test.
- Each rule carries a polarity: **▶ enforced** or **⊘ assumed exclusion**. There is no
  "not yet implemented" state.
- ⊘ rules have a **green** test asserting the fallback behaviour.
- To change a decision: the ⊘ test goes red → **delete** the rule folder → add the ▶ rule.
  Never silently amend an exclusion.
- Never hand-write files into `files/`. Edit `samples.yaml`, run `tools/build_samples.py`.
- New behaviour without a rule = out of scope. Ask; do not improvise.

## Conventions
- IDs: Feature `F03` · Story `US-03-05` · Task `T-03-05-02` · Rule `UC-14-slug` · Finding `#6`
- English everywhere: code, docs, Gherkin, API messages, UI labels, commits.
- Typing: `mypy --strict`. No bare `dict` records, no magic strings — dataclasses and Enums.
- Errors: never `except Exception: pass`. Catch precisely, log with context.
- Output: data on stdout, diagnostics on stderr, through `logging`.
- Front-end: vanilla ESM, no bundler, no npm. `textContent`, never `innerHTML`.

## Dependencies
Runtime deps are frozen: Pillow, piexif, tzdata, FastAPI, Uvicorn, Pydantic.
**Adding one requires an ADR merged first.** Never vendor a library.

## Git
One branch per US: `feat/US-03-05-folder-dates`. Conventional commits
(`feat(US-03-05): …`). Annotated tag `US-03-05` on main after merge.
Never commit generated artefacts other than `specs/**/files/`.

## Definition of Done — run before claiming completion
```bash
ruff check . && mypy src && pytest -q --cov=src/yait --cov-fail-under=85
python tools/check_specs.py && python tools/build_samples.py --check
```
Plus: every UC referenced by the US is green, and its task list is fully checked.

## Do not
- Do not touch `C:\Users\pasca\Pictures\DVD` — read-only reference archive, never a test target.
- Do not commit the real archive, or any personal name, in `specs/` or `tests/`.
- Do not widen an US's scope. Out-of-scope findings go in the US fiche as a note.
- Do not mark work done with a red or skipped test.
```

---

## Backlog ordonné

### Lot 0 — Corpus et pretotype *(aucune ligne de code de production)*

Les échantillons précèdent les maquettes : celles-ci affichent alors les **vrais noms du corpus**,
ce qui rend le pretotype honnête et permet de juger l'ergonomie sur des cas réels.

**F00 · Specs corpus & pretotype**
| US | Intitulé |
|---|---|
| US-00-01 | Dépôt public : **`CLAUDE.md`**, README, LICENSE MIT, CONTRIBUTING, `.gitignore` **au premier commit** |
| US-00-02 | Seed : intégrer l'image, **supprimer tout l'EXIF**, `specs/LICENSE` CC0 |
| US-00-03 | Structure `specs/` : gabarits `rule.md` / `rule.feature` / `samples.yaml`, `README.md` |
| US-00-04 | Générateur `tools/build_samples.py` — dérivés d'image (dimensions, qualité, EXIF injecté) |
| US-00-05 | Générateur — artefacts forgés : AVI `IDIT`, MP4 `mvhd`, `.THM`, `.zip`, tronqué, 0 octet, junk |
| US-00-06 | Rédaction RG-1 (29 règles du cœur métier) : `rule.md` + `rule.feature` + `samples.yaml` |
| US-00-07 | Rédaction RG-2 à RG-7 (31 règles) |
| US-00-08 | Garde-fous CI : invariants de structure **et de polarité**, budget de taille, manifeste |
| US-00-09 | Design system : tokens, thème clair/sombre, composants |
| US-00-10 | Écran **Home** — saisie du chemin, collections récentes |
| US-00-11 | Écran **Collection summary** |
| US-00-12 | Écran **Inventory** — grille virtualisée, filtres, répartition des sources |
| US-00-13 | Écran **Media detail** — **toutes** les dates candidates et *pourquoi* l'une l'emporte |
| US-00-14 | Écran **Rename plan** — avant/après, motif de chaque suffixe |
| US-00-15 | Écran **Collisions** |
| US-00-16 | Écran **Organize / Flatten** |
| US-00-17 | Écran **Metadata editor** — héritier de csvedit |
| US-00-18 | Écran **Job progress** |
| US-00-19 | Écran **History & undo** |
| US-00-20 | Écrans **Empty / error / permission states** |
| US-00-21 | **Prototype cliquable** alimenté par le corpus |
| US-00-22 | **Revue de pretotyping** : journal des décisions, **ré-arbitrage du backlog** |

> **US-00-22 est un point d'arrêt.** Le reste du backlog n'est figé qu'après elle.

### Lot 1 — Walking skeleton, lecture seule *(aucune écriture disque)*

**F01 · Foundation & launcher** — `US-01-01` squelette + CI (Ubuntu **et** Windows) ·
`US-01-02` FastAPI + `/health` + OpenAPI + RFC 9457 · `US-01-03` configuration ·
`US-01-04` lanceur `yait.ps1`/`yait.sh` · `US-01-05` journalisation structurée
*(diagnostics sur **stderr**, #31)* · `US-01-06` coquille d'IHM conforme aux maquettes.

**F02 · Collections** — `US-02-01` saisir et valider un chemin *(existence, lisibilité,
confinement `UC-52`, chemins longs `UC-34`)* · `US-02-02` collections récentes ·
`US-02-03` écrans Home et Summary câblés.

**F03 · Inventory & date resolution** ← le cœur
| US | Intitulé | Règles |
|---|---|---|
| US-03-01 | Modèle pur : `MediaFile`, `PartialDate`, `DateSource`, `Precision` — **testable sans Pillow** (#24, #29) | — |
| US-03-02 | Dates écrites dans le nom de fichier | RG-1.1 |
| US-03-03 | Dates portées par les noms de répertoires | RG-1.2 |
| US-03-04 | Dates lues dans le contenu : EXIF, vidéo, zip, sidecar THM | RG-1.3 |
| US-03-05 | Arbitrage et garde-fous : priorité, `gap_days`, bornes, faux positifs | RG-1.4 |
| US-03-06 | Classification des fichiers : parasites, illisibles, sidecars | RG-2 |
| US-03-07 | Parcours du système de fichiers : exclusions, empreintes, symlinks | — |
| US-03-08 | `scan_collection` + **cache invalidé par empreinte** (#33 : 5 scans → 1) | — |
| US-03-09 | API `POST /api/scans` + `GET /api/jobs/{id}` + flux SSE | — |
| US-03-10 | Écran Inventory câblé | — |
| US-03-11 | Écran Media detail câblé — justification du choix de date | `UC-36` |

### Lot 2 — Renommage, rangement, annulation *(premières écritures)*

**F07 · Journal & undo** — *livré avant toute écriture, par principe* — `US-07-01` port + adaptateur
JSONL write-ahead `UC-50` · `US-07-02` lecteur des journaux v1 · `US-07-03` `undo_operation`
`UC-51` · `US-07-04` API + écran History.

**F04 · Renaming** — `US-04-01` `atomic_write`/`safe_move`/`PathGuard` *(`UC-49`, `UC-52`, `UC-53`)* ·
`US-04-02` politique de nommage paramétrable *(RG-3)* · `US-04-03` collisions *(RG-4)* ·
`US-04-04` **plan figé** avec empreintes (#7) · `US-04-05` **ordonnancement** des déplacements (#8) ·
`US-04-06` exécution journalisée et reprenable · `US-04-07` API · `US-04-08` écrans câblés.

**F05 · Organizing** — `US-05-01` layouts *(RG-6)* · `US-05-02` mise à plat ·
`US-05-03` garde-fou d'unicité · `US-05-04` nettoyage des répertoires vides · `US-05-05` API + écran.

### Lot 3 — Métadonnées

**F06 · Metadata** — `US-06-01` lecture + décodage `XP*` · `US-06-02` déduction du libellé
*(`UC-32`, `UC-31`)* · `US-06-03` feuille de revue, **statuts calculés côté serveur** (#27, #28) ·
`US-06-04` détection de dérive *(`UC-45`)* · `US-06-05` écriture EXIF+XMP atomique sans
ré-encodage *(`UC-44`, `UC-49`)* · `US-06-06` sauvegarde des blocs d'origine · `US-06-07` API ·
`US-06-08` éditeur câblé · `US-06-09` import/export CSV compatible v1.

### Lot 4 — Durcissement et distribution

**F08 · Quality & safety** — `US-08-01` tests d'attaque sur les chemins · `US-08-02` contract
testing schemathesis · `US-08-03` **campagne privée de non-régression** contre `dvd-tools` ·
`US-08-04` robustesse (interruption, disque plein, fichier verrouillé) · `US-08-05` OpenAPI
enrichi · `US-08-06` **toute anomalie de production devient un nouvel UC**.

**F09 · Distribution** — `US-09-01` réévaluation Docker · `US-09-02` installation à froid ·
`US-09-03` finition du dépôt public.

---

## Traçabilité — les 36 findings dvd-tools

| Findings | Traités par |
|---|---|
| #1 #4 écriture non atomique | `UC-49` · US-04-01 · US-06-05 |
| #2 #3 journal écrit trop tard | `UC-50` · US-07-01 |
| #5 suppression irréversible | RG-7 · F05 (corbeille seule) |
| #6 conflit `.thm` | `UC-22` **et** `UC-38` — les deux faces du bug |
| #7 #8 plan non figé, ordre des renommages | US-04-04 · US-04-05 |
| #9 #10 #11 #12 confinement et validation | `UC-52` · US-02-01 · US-04-01 |
| #13 UTF-8 tronqué | disparaît (FastAPI/Pydantic gèrent le corps) |
| #14 #15 bornes d'années | `UC-30` |
| #16 mois numérique perdu | `UC-11` |
| #17 tzdata | dépendance explicite + US-06-05 |
| #18 → #23 bugs divers | réécrits dans les US correspondantes |
| #24 non-testabilité | US-03-01 (domaine pur) — principe fondateur |
| #25 #26 hygiène, licence, vendoring | US-00-01 · US-01-01 |
| #27 #28 duplications Python/JS | US-06-03 · ADR-002 |
| #29 stringly-typed | US-03-01 (dataclasses + Enum + mypy strict) |
| #30 `except Exception` | US-01-05 + revue systématique |
| #31 stdout/stderr | US-01-05 |
| #32 IHM dans un template literal | US-01-06 |
| #33 5 scans complets | US-03-08 |
| #34 contrat de retour · #35 chemins longs · #36 `sys.path` | US-01-02 · `UC-34` · US-01-01 |

---

## Vérification

**Structure des specs** — l'invariant qui empêche la documentation de mentir :
```bash
pytest tests/acceptance -q && python tools/check_specs.py
```
`check_specs.py` échoue si un UC n'a pas ses quatre artefacts, si un `.feature` n'a aucun
scénario, si un UC n'est référencé par aucune US, si un échantillon est orphelin — ou si un
`rule.md` n'a pas de bloc `Decision` complet avec une polarité **▶** ou **⊘**. Il n'existe pas de
statut « à faire » : la commande refuse la valeur.

**Corpus reproductible sur n'importe quelle machine :**
```bash
python tools/build_samples.py --check
```
Régénère depuis le seed et compare le **manifeste** (chemins, EXIF, dimensions), **pas les
octets** : l'encodeur JPEG de Pillow n'est pas stable d'une version à l'autre. Vérifie aussi que
le seed ne porte plus **aucun** tag EXIF, et que le budget de taille est respecté.

**À chaque US** — la DoD de la fiche :
```bash
ruff check . && mypy src && pytest -q --cov=src/yait --cov-fail-under=85
```

**Au niveau API** — l'exigence « toute fonctionnalité testée et documentée » :
```bash
pytest tests/contract -q
```
Un endpoint sans schéma de réponse, sans exemple ou sans code d'erreur documenté fait échouer la CI.

**Fin de lot 0** : ouvrir `docs/20-mockups/index.html`, parcourir les 12 écrans dans les deux
thèmes, à 1280 px et 1920 px, en vérifiant qu'ils affichent les **vrais noms du corpus**.
Sortie de US-00-22 : un journal de décisions et, le cas échéant, un backlog réordonné.

**Fin de lot 1** — bout en bout, sans jamais écrire :
1. `./yait.sh` ouvre l'IHM, le service répond sur `/health`.
2. Coller `C:\Users\pasca\Pictures\DVD`, lancer un scan, suivre la progression SSE.
3. L'écran Media detail justifie chaque date retenue.
4. **Non-régression** (campagne privée) : comparer aux dates de `01-inventaire.csv` v1. Les
   divergences attendues sont exactement celles que les règles annoncent — `UC-10`, `UC-11`,
   `UC-14`, `UC-15`, `UC-22`, `UC-30`, `UC-31`, `UC-34` ; tout le reste doit coïncider.
   **Toute divergence non annoncée par une règle est un défaut** : elle devient soit un nouvel UC
   décidé, soit une correction (US-08-06).
5. Vérifier qu'aucun octet n'a été écrit : `sha256` avant/après sur l'archive.

**Fin de lot 2** — l'aller-retour qui manque aujourd'hui : plan → apply → **interruption brutale
à mi-parcours** → undo → arborescence identique bit pour bit (`UC-51`).
