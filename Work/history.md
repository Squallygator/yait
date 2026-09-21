# Historique

Ce qui est terminé, daté. Uniquement du ✅.

---

## 2026

- ✅ `US-00-07` — RG-2 to RG-7 rules **(21/09/2026)** [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-07-write-rg2-rg7-rules.md)
  Les 27 règles de RG-2 à RG-7, quatre artefacts chacune, un commit par groupe. RG-2 classification
  (5 dont 1 exclusion), RG-3 nommage (5), RG-4 collisions (2), RG-5 métadonnées (6 dont 1
  exclusion), RG-6 rangement (3 dont 1 exclusion), RG-7 sûreté (6). `UC-24` (posée en warm-up par
  `US-00-05`) réduite à son unique exemple ; les entrées déplacées vers `UC-25`, `UC-26`, et celles
  déjà couvertes par `UC-20`/`UC-21`/`UC-23` supprimées. `specs/README.md` : vocabulaire de pas
  étendu par groupe (déduction de libellé, rangement, sûreté). Trois `> Sample-fidelity note` —
  `UC-33` (le générateur ne sait pas semer un `XPTitle`, à plier dans `US-00-23`), `UC-40` (le jeu
  de caractères que Windows refuse ne peut pas vivre dans un chemin de corpus committé), `UC-34`
  (un chemin réellement > 260 caractères non plus). RG-7 relié aux findings `dvd-tools` via la
  table de traçabilité de `plan-v3-approved.md`, jusque-là non exploitée pour ces règles : `#1`/`#4`
  → `UC-49`, `#2`/`#3` → `UC-50`, `#9`-`#12` → `UC-52`, `#35` → `UC-34` (`#6` déjà posé sur
  `UC-22`/`UC-38`). 74 échantillons au manifeste, `build_samples.py --check` vert. Comptage : la
  fiche disait « 31 » restantes, la table `Livrables` et les six `group.md` en listent 27 — avec les
  33 de RG-1, le corpus totalise 60 règles / 15 exclusions, conforme à ce qu'attend `US-00-08`.
  L'écart « 31 » n'a pas été corrigé dans la fiche. PR #4, tag `US-00-07`.

- ✅ `US-00-06` — RG-1 date-resolution rules **(09/09/2026)** [🔗](F00-specs-corpus-and-pretotype/Plan/US-00-06-write-rg1-rules.md)
  Les 32 règles neuves de RG-1 (UC-14 préexistait), quatre artefacts chacune, un commit par
  sous-groupe. RG-1.1 lecture du nom (10), RG-1.2 répertoires (3), RG-1.3 contenu (9), RG-1.4
  arbitrage (10 dont 6 exclusions). `UC-36` — l'échelle de priorité complète — rédigé en dernier ;
  son exemple est un conflit à trois sources dont la bonne réponse est la valeur médiane, pour
  qu'un `min`/`max`/premier-trouvé échoue. 42 échantillons au manifeste, `build_samples.py --check`
  vert. `specs/README.md` : ajout des formes `YYYY-MM` / `YYYY` au vocabulaire de pas (résolution
  à la précision, jamais complétée à `-01`). Deux écarts de fidélité d'échantillon assumés et
  signalés en `rule.md` — `UC-57` (le générateur ne sait pas forger d'IFD GPS, exemple dégénéré)
  et `UC-58` (archives non imbriquables) — reportés dans `US-00-23`. Comptage : la fiche disait
  « 29 » mais les tables `group.md`, autoritaires, en listent 33. PR #3, tag `US-00-06`.

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
