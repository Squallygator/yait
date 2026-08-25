# US-00-12 — Mockup: Inventory grid

> **Feature** F00 — Specs corpus & pretotype · **Lot 12/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner l'écran central de consultation : la grille de tous les fichiers, avec leur
date résolue et **la source de cette date**.

Maquette **statique** : données en dur, aucune logique métier, aucun appel réseau. On regarde un
écran pour juger l'ergonomie avant de construire quoi que ce soit.

## État au démarrage

- `docs/20-mockups/assets/mockup.css` et `mockup.js` — le design system, livré en `US-00-09`
- `docs/20-mockups/components.html` — la planche de référence des composants
- Le corpus d'échantillons sous `specs/` : **utiliser ses vrais noms de fichiers** dans les
  données en dur. Une maquette peuplée de lorem ipsum ne permet pas de juger la densité réelle.

## Règles applicables

- **Vanilla, zéro build.** Pas de npm, pas de bundler, pas de CDN.
- **Réutiliser les composants du design system**, ne pas en inventer. Si un composant manque,
  l'ajouter à `mockup.css` et à `components.html` dans le même commit.
- **Thème clair et sombre** tous les deux regardables.
- **Le bandeau de mode** (simulation / exécution) est visible en permanence quand l'écran porte
  une action qui écrit.

## Livrable

```
docs/20-mockups/03-inventory.html
```

## Contenu attendu

C'est l'écran le plus dense de l'application et celui qui décide de son ergonomie. Il affichera
couramment plusieurs milliers de lignes.

- Grille dense : nom de fichier, répertoire, type, date résolue, **source de la date**, précision.
- La **source** est une pastille, pas du texte : `file-name`, `folder-name`, `embedded-metadata`,
  `sidecar`, `none`. C'est l'information qui permet de repérer une résolution douteuse d'un coup
  d'œil sur mille lignes.
- La **précision** est visible : `2010-12-00` doit se lire comme « décembre 2010, jour inconnu »
  et non comme une date bancale. Trouver une manière de l'afficher qui ne ressemble pas à un bug.
- Filtres : par source de date, par précision, par type, par répertoire, plus une recherche
  plein texte.
- Un encart de répartition : combien de fichiers par source de date. C'est le premier indicateur
  de santé d'un lot.
- L'indication que la grille est virtualisée (des milliers de lignes), même si la maquette
  n'en affiche que cinquante.
- Une action d'export CSV.

## Étapes

1. `T-00-12-01` Barre de filtres et recherche.
2. `T-00-12-02` Encart de répartition par source de date.
3. `T-00-12-03` La grille, avec une cinquantaine de lignes tirées du corpus réel.
4. `T-00-12-04` Pastilles de source et rendu des dates partielles.
5. `T-00-12-05` Action d'export.

## Vérification

Ouvrir `docs/20-mockups/03-inventory.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- Afficher cinquante lignes et se demander : repère-t-on une ligne dont la date vient d'une source
  douteuse sans la chercher ?
- Les dates partielles (`2011-00-00`) sont-elles lisibles comme une imprécision assumée ?
- La grille tient-elle à 1280 px sans défilement horizontal du corps de page ?

## Commit

```
feat(US-00-12): add inventory mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
