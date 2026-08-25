# US-00-03 - Executable specification structure

> **Feature** F00 - Specs corpus & pretotype - **Lot 3/22** - Statut : ✅ **(25/08/2026)**
> Fiche rétrospective : le lot est livré, tag `US-00-03`.

## Objectif

Fixer la structure que suivront les 60 règles métier : gabarits, taxonomie, vocabulaire.

## Ce qui a été livré

- `specs/README.md` - comment lire et ajouter une règle, le vocabulaire de pas Gherkin, le
  format des recettes d'échantillons, ce que le corpus ne doit pas contenir
- `specs/_templates/` - `rule.md`, `rule.feature`, `samples.yaml`, `group.md`
- L'arborescence `RG-1` à `RG-7`, chaque `group.md` portant sa table de règles **et ses
  frontières** avec les groupes voisins
- `UC-14-deepest-folder-wins` comme exemple de référence

## Décisions prises

1. **Quatre artefacts par règle**, et leur indépendance : `rule.feature` et `samples.yaml` ne se
   rejoignent que par **le nom des fichiers**. Rien n'est généré depuis rien. Un manifeste unique
   générant les scénarios aurait grossi sans fin et aurait fait d'un fichier technique de
   fixtures la source de vérité fonctionnelle.
2. **Toute résolution de date doit affirmer sa source** dans le scénario (`file-name`,
   `folder-name`, `embedded-metadata`, `sidecar`, `none`). Une bonne date obtenue pour une
   mauvaise raison est un bug en sursis.
3. **Section `## Boundaries` obligatoire** dans chaque `group.md`. C'est là que se joue la
   non-pourriture : `RG-2` explique pourquoi `UC-38` (le `.THM` survit au nettoyage) est séparé
   de `UC-22` (le `.THM` date la vidéo). Dans `dvd-tools` ces deux facettes vivaient dans des
   fonctions différentes et se contredisaient : c'est le finding #6.
4. **Identifiants d'UC plats et permanents.** `UC-14` garde son numéro même s'il change de groupe.

## Limite assumée

`UC-14` n'a pas encore son répertoire `files/`. C'est le seul endroit du corpus où la règle des
quatre artefacts n'est pas tenue ; `specs/README.md` le dit explicitement, et cela se referme
avec le générateur en `US-00-04` / `US-00-05`.

## Traces

Commit `c21cf72`. Tag `US-00-03`.
