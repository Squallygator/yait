# Historique

Ce qui est terminé, daté. Uniquement du ✅.

---

## 2026

- ✅ `US-00-03` — Executable specification structure **(25/08/2026)** [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-03-specs-structure.md)
  Gabarits `rule.md` / `rule.feature` / `samples.yaml` / `group.md`, taxonomie RG-1 à RG-7 avec
  frontières entre groupes, vocabulaire de pas Gherkin, et `UC-14-deepest-folder-wins` comme
  exemple de référence. Tag `US-00-03`.

- ✅ `US-00-02` — Seed photograph integrated and stripped **(25/08/2026)** [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-02-seed-photograph.md)
  Photo originale 900×403 sous CC0. Retrait des blocs APP1 Exif (144 o) et XMP (434 o) —
  ni GPS, ni modèle, ni numéro de série n'étaient présents, seulement une date de prise de vue.
  Scan compressé identique au bit près (sha256 vérifié indépendamment).
  `tools/strip_exif.py` en stdlib pure, avec `--check` pour la CI. Tag `US-00-02`.

- ✅ `US-00-01` — Public repository bootstrap **(25/08/2026)** [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-01-repository-bootstrap.md)
  `CLAUDE.md` (contrat de projet), `README.md`, `CONTRIBUTING.md`, `LICENSE` MIT, `.gitignore`
  posé **avant** tout autre fichier, `.gitattributes` pour les fins de ligne. Tag `US-00-01`.
