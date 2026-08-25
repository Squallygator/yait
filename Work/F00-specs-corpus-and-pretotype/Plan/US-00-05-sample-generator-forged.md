# US-00-05 — Sample generator, forged artefacts

> **Feature** F00 — Specs corpus & pretotype · **Lot 5/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Compléter le générateur avec les artefacts qu'une photo ne peut pas produire : vidéos, archives,
fichiers abîmés, fichiers parasites. Tous **forgés octet par octet**, sans encodeur ni outil
externe — donc légers et libres de droit par construction.

## État au démarrage

`tools/build_samples.py` sait lire les recettes et produire des dérivés d'image du seed, avec
injection EXIF. Le manifeste consolidé `specs/.manifest.json` et le mode `--check` fonctionnent.
`UC-14` a son répertoire `files/`.

Le format de recette (`samples.yaml` ou `samples.toml`) a été tranché en `US-00-04` : suivre ce
qui est en place, ne pas le rouvrir.

## Règles applicables

- **Aucune dépendance nouvelle.** Pillow suffit pour les images ; le reste est de la construction
  de binaires en stdlib (`struct`, `zipfile`).
- **Pas de ffmpeg, pas d'encodeur vidéo.** Un chunk RIFF `IDIT` fait une centaine d'octets et un
  atome `mvhd` guère plus : ce qui est testé est la lecture de la métadonnée, pas le décodage d'un
  flux.
- **Un fichier tronqué doit l'être honnêtement.** En-tête intact, scan coupé net — ce que produit
  un secteur de CD abîmé. Ne pas fabriquer un JPEG dont les dimensions déclarées mentent : cela
  saperait `UC-24`, qui repose sur la détection d'images réellement illisibles.

## Livrables

Extension de `tools/build_samples.py` avec les `kind` suivants :

| `kind` | Produit | Paramètres |
|---|---|---|
| `riff-idit` | AVI minimal portant un chunk `IDIT` | `idit` : chaîne de date façon `Tue Aug 29 09:43:38 2006` |
| `mp4-mvhd` | MP4/MOV minimal portant `moov/mvhd` | `created` : horodatage |
| `zip` | Archive contenant des images dérivées du seed | `entries[]` : nom + `exif` |
| `truncated-jpeg` | En-tête intact, scan coupé | `keep_bytes` |
| `empty` | Fichier de 0 octet | — |
| `bytes` | Contenu littéral, pour les fichiers parasites | `content` |

Un `.THM` n'est **pas** un `kind` : c'est un JPEG dérivé du seed, donc `source: seed` avec une
extension `.THM`.

## Étapes

1. `T-00-05-01` `riff-idit` : en-tête `RIFF` + type `AVI `, liste `hdrl` minimale, chunk `IDIT`
   portant la chaîne de date. Vérifier que le chunk se trouve dans les premiers 256 Ko, puisque
   c'est ainsi que le lecteur le cherchera.
2. `T-00-05-02` `mp4-mvhd` : boîte `ftyp` + boîte `moov` contenant `mvhd` version 0, avec le
   nombre de secondes depuis le **1er janvier 1904** — l'époque QuickTime, pas Unix. Se tromper
   d'époque est l'erreur classique et donne 66 ans d'écart.
3. `T-00-05-03` `zip` : archive contenant des images dérivées du seed, chacune avec son EXIF, et
   des horodatages d'entrée distincts pour pouvoir spécifier « la plus ancienne gagne ».
4. `T-00-05-04` `truncated-jpeg` : dériver une image normale puis la couper à `keep_bytes`.
5. `T-00-05-05` `empty` et `bytes`.
6. `T-00-05-06` Étendre le manifeste : pour un artefact forgé, enregistrer le `kind`, les
   paramètres et la taille — ni dimensions ni EXIF.
7. `T-00-05-07` Documenter chaque `kind` dans `specs/_templates/samples.*` et dans
   `specs/README.md`.
8. `T-00-05-08` Écrire une recette de mise au point couvrant les six `kind`, sous un UC réel de
   `RG-1.3` ou `RG-2`. Noter dans la fiche du lot qui écrira cette règle que sa recette existe
   déjà.

## Vérification

```bash
python tools/build_samples.py && python tools/build_samples.py --check
```

Puis, en Python, vérifier que chaque artefact est bien ce qu'il prétend :

- l'AVI contient le marqueur `IDIT` et la date attendue s'y lit ;
- le MP4 contient `mvhd` et les secondes décodées depuis 1904 donnent la date attendue ;
- le zip s'ouvre avec `zipfile` et ses entrées portent les horodatages attendus ;
- le JPEG tronqué commence bien par un SOI mais **ne se termine pas** par un EOI ;
- le fichier vide fait 0 octet.

## Vérification manuelle (STOP)

- Ouvrir l'AVI et le MP4 dans un lecteur : ils **ne se liront pas**, c'est normal et voulu. Ce qui
  compte est que l'Explorateur Windows affiche la date attendue dans les propriétés du fichier —
  c'est le meilleur contrôle croisé disponible sans outil tiers.
- Vérifier la taille totale de `specs/` : elle doit rester très en dessous du mégaoctet.

## Commit

```
feat(US-00-05): forge video, archive and damaged-file samples
```

Corps : expliquer que ces artefacts sont construits octet par octet plutôt qu'encodés — légers,
reproductibles, libres de droit — et pourquoi un JPEG tronqué doit l'être réellement plutôt que
par des dimensions mensongères.

## Ne pas faire

- Ne pas ajouter de dépendance, ni appeler ffmpeg.
- Ne pas écrire de règle métier : c'est `US-00-06` / `US-00-07`.
- Ne pas produire des artefacts « valides » au sens d'un lecteur multimédia : ce n'est ni
  nécessaire, ni souhaitable (poids), ni testé.
