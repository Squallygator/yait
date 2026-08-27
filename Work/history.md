# Historique

Ce qui est terminé, daté. Uniquement du ✅.

---

## 2026

- ✅ `US-00-05` — Forged artefact samples **(27/08/2026)** [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-05-sample-generator-forged.md)
  Six `kind` forgés octet par octet dans `tools/build_samples.py` : `riff-idit` (AVI), `mp4-mvhd`
  (MP4/MOV), `zip`, `truncated-jpeg`, `empty`, `bytes` — stdlib seule, aucun encodeur. Époque
  QuickTime (1904, pas 1970) calculée depuis deux `datetime` plutôt qu'une constante à la main.
  Le JPEG tronqué coupe une image réellement dérivée (SOI intact, pas d'EOI) au lieu de mentir sur
  ses dimensions, pour ne pas saper `UC-24`. Découverte en vérification manuelle : le lecteur de
  propriétés MP4 de l'Explorateur Windows n'affiche rien du tout sur un `moov` sans piste, contrairement
  au lecteur RIFF/AVI qui scanne les chunks sans exiger un flux valide — corrigé en ajoutant une piste
  vidéo minimale à zéro échantillon, toujours indécodable, confirmé via le magasin de propriétés du
  shell puis dans l'Explorateur. Recette de mise au point posée sous `UC-24-unreadable-is-detected`
  pour `US-00-07`. Tag `US-00-05`.

- ✅ `US-00-04` — Image sample generator **(25/08/2026)** [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-04-sample-generator-images.md)
  `tools/build_samples.py` (Pillow) dérive chaque image depuis `specs/_seed/river.jpg` : redimensionnement, qualité
  JPEG, injection EXIF sur liste fermée (`Orientation`, `DateTimeOriginal`, `DateTimeDigitized`) — un nom de champ ou
  de tag inconnu échoue explicitement. Format de recette basculé de YAML à TOML pour rester sur `tomllib` (stdlib),
  sans nouvelle dépendance. `--check` régénère dans un répertoire temporaire par le même chemin de code qu'un run
  réel puis compare le manifeste `specs/.manifest.json`, jamais les octets. `files/` de `UC-14` généré (une image,
  `exif = {}`) et vérifié sans métadonnée par `strip_exif.py --check`. Tag `US-00-04`.

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
