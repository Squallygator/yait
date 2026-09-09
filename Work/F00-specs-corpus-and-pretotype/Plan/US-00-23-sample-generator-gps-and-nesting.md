# US-00-23 — Sample generator : champ date GPS + archives imbriquées

> **Feature** F00 — Specs corpus & pretotype · **Lot 23/23** *(ajouté après coup, suivi de `US-00-06`)* · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md) puis [`specs/README.md`](../../../specs/README.md).

## Objectif

Combler les deux capacités qui manquaient au générateur d'échantillons pendant `US-00-06`, et qui
ont forcé deux règles de RG-1 à se contenter d'un exemple dégénéré :

- `UC-57` (le GPS n'est pas une source de date) — le générateur ne sait pas écrire d'IFD GPS, donc
  son échantillon est une image **sans aucune métadonnée**, indiscernable de `UC-18`.
- `UC-58` (les archives ne sont pas parcourues récursivement) — le `kind = "zip"` ne construit
  qu'un seul niveau, donc l'entrée « archive imbriquée » est un JPEG renommé `old-stuff.zip`, pas
  un vrai zip.

Une fois le générateur étendu, resserrer les deux échantillons pour que leur `rule.feature`
prouve réellement le repli, et retirer la note `> Sample-fidelity note` de chaque `rule.md`.

## État au démarrage

**Placement.** Ce lot appartient à la **chaîne corpus** (`US-00-04` → `US-00-08`), pas aux
maquettes. Il est numéroté après `US-00-22` uniquement parce qu'il a été ajouté après le
découpage initial ; le **point d'arrêt de `US-00-22`** concerne l'ordre des écrans et du backlog
F01+, il n'interdit pas une correction d'outillage du corpus. Ce lot peut être fait dès qu'une
session est disponible, avant ou après `US-00-07`/`US-00-08`.

**Le générateur.** `tools/build_samples.py` (Pillow) :

- Liste EXIF **fermée** : `ExifFieldName` = `Orientation`, `DateTimeOriginal`, `DateTimeDigitized`.
  Un nom de tag inconnu dans une recette échoue explicitement (`RecipeError`). Les tags « date »
  sont écrits dans l'IFD Exif via `Image.Exif().get_ifd(ExifTags.IFD.Exif)` ; `Orientation` dans
  l'IFD principal. Table de correspondance construite dans `_build_exif_field_table()`.
- `kind = "zip"` : `_load_zip_params` **exige** `exif.DateTimeOriginal` sur chaque entrée ;
  `build_zip` dérive une image du seed par entrée et cale le `date_time` du `ZipInfo` dessus. Une
  entrée ne peut pas être un binaire arbitraire ni une archive.
- `--check` régénère dans un répertoire temporaire **par le même chemin de code** qu'un run réel,
  puis compare `specs/.manifest.json` (jamais les octets). Toute recette doit rester déterministe.
- Le manifeste enregistre, pour une image, `{path, width, height, quality, exif, size}` ; pour un
  forgé, `{path, kind, params, size}`. `exif` y est un dict `{tag: valeur}` trié.

**Dépendances.** Runtime gelé : **Pillow, piexif, tzdata, FastAPI, Uvicorn, Pydantic**. `piexif`
est disponible et sait écrire l'IFD GPS proprement — utilisable si l'écriture GPS via Pillow se
révèle pénible. **Aucune dépendance nouvelle.**

**Les deux règles à resserrer** (leurs `## Decision` ne changent pas, seulement `## Example`,
`samples.toml`, éventuellement `rule.feature`) :

- `specs/RG-1-date-resolution/RG-1.4-arbitration/UC-57-gps-not-used-for-dating/`
- `specs/RG-1-date-resolution/RG-1.3-content-dates/UC-58-nested-zip-not-recursed/`

Chacune porte aujourd'hui un bloc `> Sample-fidelity note` dans `rule.md`, à supprimer une fois
l'exemple honnête.

**Ce qui n'existe pas encore** : `tools/check_specs.py` (c'est `US-00-08`), le résolveur de dates
(`src/`, c'est F03). La vérification de ce lot est donc structurelle — l'artefact contient bien
ce qu'il prétend — pas « le résolveur donne la bonne date ».

## Règles applicables

- **Aucune dépendance nouvelle.** Pillow ou `piexif`, tous deux déjà gelés.
- **Liste EXIF fermée, étendue d'un cran, pas ouverte.** On ajoute `GPSDateStamp` nommément à
  `ExifFieldName` ; un tag inconnu doit toujours échouer. Ne pas introduire de mécanisme
  « n'importe quel tag ».
- **Déterminisme.** Deux runs, même Pillow → même manifeste. Pas d'horodatage courant, pas d'ordre
  d'itération de `dict` non trié dans le manifeste.
- **Le générateur reste minimal.** Objectif : porter un nom, un dossier, quelques champs de
  métadonnée. Un IFD GPS complet (lat/lon/alt) n'est pas demandé — seul `GPSDateStamp` (et
  `GPSTimeStamp` si le coût est nul) sert à `UC-57`.
- **On ne touche pas aux décisions des règles.** `UC-57` et `UC-58` gardent leur polarité ⊘, leur
  `Fallback`, leur `Revisit if`. Seul l'exemple devient fidèle.
- **Ne jamais poser un fichier à la main dans `files/`.** Éditer `samples.toml`, lancer le
  générateur.

## Livrables

### A — Champ date GPS

1. `GPSDateStamp` ajouté à `ExifFieldName` (valeur `"GPSDateStamp"`), encodé au format EXIF
   `"YYYY:MM:DD"` depuis une entrée de recette `"YYYY-MM-DD HH:MM:SS"` (réutiliser
   `parse_recipe_datetime`, ne garder que la date). Écrit dans l'IFD GPS
   (`ExifTags.IFD.GPSInfo`, tag `GPSDateStamp` = 29) — via Pillow si possible, sinon `piexif`.
2. `samples.toml` de `UC-57` réécrit : une image **sans `DateTimeOriginal`**, avec
   `GPSDateStamp` calé un jour avant la date du dossier, dans un dossier daté au mois. Le
   `rule.feature` doit continuer d'affirmer : date depuis `folder-name`, précision `month`, et
   **pas** depuis `embedded-metadata`.
3. `rule.md` de `UC-57` : `## Example` réécrit sur le vrai cas (un `GPSDateStamp` présent, à un
   jour d'écart, ignoré) ; bloc `> Sample-fidelity note` **supprimé**.

### B — Archives imbriquées

4. `kind = "zip"` étendu pour qu'une entrée puisse être elle-même une archive. Forme proposée
   (l'implémenteur tranche) : une entrée porte soit `exif = {...}` (image, comme aujourd'hui),
   soit `nested = { entries = [...] }` produisant un vrai sous-zip. Le sous-zip est construit par
   le même code que le zip racine (récursion sur une fonction commune).
5. `samples.toml` de `UC-58` réécrit : un zip racine avec deux images datables (2012-07-10,
   2012-07-11) et une entrée `old-stuff.zip` qui est **un vrai zip** contenant une image datée
   2001-01-01. Le `rule.feature` continue d'affirmer : le zip racine résout à `2012-07-10`.
6. `rule.md` de `UC-58` : `## Example` réécrit ; bloc `> Sample-fidelity note` **supprimé**.

### C — Documentation

7. `specs/_templates/samples.toml` et `specs/README.md` (section « Sample recipes ») : documenter
   `GPSDateStamp` dans la liste des tags EXIF, et la forme `nested` du `kind = "zip"`.
8. Mettre à jour la mémoire projet `sample-generator-gaps` (hors dépôt) ou la retirer : les deux
   écarts sont comblés.

## Étapes

1. `T-00-23-01` Ajouter `GPSDateStamp` à `ExifFieldName` + l'encodeur + l'écriture IFD GPS.
   Vérifier en Python que le tag se relit (`Image.open(...).getexif().get_ifd(GPSInfo)`).
2. `T-00-23-02` Réécrire `UC-57` : `samples.toml`, `rule.feature` si besoin, `rule.md`
   (`## Example`, suppression de la note). `build_samples.py --check` vert.
   **Commit A** : `feat(US-00-23): add GPSDateStamp to the sample generator, tighten UC-57`.
3. `T-00-23-03` Étendre `kind = "zip"` pour l'imbrication (fonction de construction récursive,
   validation de recette, manifeste).
4. `T-00-23-04` Réécrire `UC-58` : `samples.toml`, `rule.feature` si besoin, `rule.md`.
   `--check` vert.
   **Commit B** : `feat(US-00-23): build real nested archives, tighten UC-58`.
5. `T-00-23-05` Documentation (`specs/_templates/samples.toml`, `specs/README.md`).
   **Commit C** : `docs(US-00-23): document GPSDateStamp and nested zip recipes`.

Les blocs A et B sont indépendants : deux sessions possibles, un commit chacun.

## Vérification

```bash
python tools/build_samples.py && python tools/build_samples.py --check
python tools/strip_exif.py --check specs/_seed/river.jpg
```

Puis, en Python :

- `UC-57` : ouvrir l'image, lire l'IFD GPS, confirmer que `GPSDateStamp` porte la date attendue
  et qu'il **n'y a pas** de `DateTimeOriginal`.
- `UC-58` : ouvrir le zip racine avec `zipfile`, confirmer que `old-stuff.zip` est une entrée
  dont le contenu est **lui-même un zip valide** (`zipfile.is_zipfile` sur les octets extraits),
  contenant une entrée datée 2001.
- Rejouer le script d'invariants de `US-00-06` (quatre artefacts, bloc `## Decision` complet,
  chemin du `rule.feature` présent dans `files/`) sur `UC-57` et `UC-58`.
- Taille totale de `specs/` toujours très en dessous du mégaoctet.

## Vérification manuelle (STOP)

- Ouvrir l'image `UC-57` dans l'Explorateur Windows → l'onglet « Détails » doit montrer une date
  GPS et **aucune** date de prise de vue. C'est le contrôle croisé qui confirme que le champ est
  écrit là où un vrai lecteur EXIF l'attend.
- Relire les `## Example` réécrits de `UC-57` et `UC-58` : l'exemple prouve-t-il maintenant le
  repli **parce que** la source refusée est présente, et pas seulement absente ?

## Commit

Trois commits (blocs A, B, C), messages en tête d'étapes. Scope `US-00-23`.
Tag annoté `US-00-23` sur `main` après merge.

## Ne pas faire

- Ne pas ajouter de dépendance, ni ouvrir la liste EXIF à des tags arbitraires.
- Ne pas écrire une ligne de résolveur : le comportement de `UC-57`/`UC-58` est implémenté en
  F03 (`US-03-04`, `US-03-05`), pas ici.
- Ne pas modifier les `## Decision` de `UC-57`/`UC-58`, ni toucher à une autre règle RG-1.
- Ne pas forger un IFD GPS complet (coordonnées) : seul `GPSDateStamp` est requis.
- Ne pas parcourir plus d'un niveau d'imbrication dans l'échantillon : `UC-58` prouve qu'on
  s'arrête au premier, un seul sous-zip suffit.
