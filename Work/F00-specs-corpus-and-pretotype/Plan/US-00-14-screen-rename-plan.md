# US-00-14 — Mockup: Rename plan, before and after

> **Feature** F00 — Specs corpus & pretotype · **Lot 14/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner l'écran de relecture du plan de renommage : ce qui va changer, et pourquoi.

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
docs/20-mockups/05-rename-plan.html
```

## Contenu attendu

Le plan est un **artefact figé** que l'humain relit avant de l'appliquer — c'est la correction
d'un défaut de `dvd-tools`, où la commande d'application recalculait tout et ignorait le plan que
l'utilisateur venait de relire.

- Grille avant / après, sur deux colonnes lisibles côte à côte.
- Le **motif** de chaque transformation : quelle source a fourni la date, pourquoi un suffixe a
  été ajouté.
- Séparer visuellement : les fichiers qui changent, ceux déjà conformes, ceux sans date.
- Un compteur en tête : combien de renommages, combien de conformes, combien de collisions.
- Le **bandeau de mode** : simulation ou exécution, impossible à manquer.
- Deux actions : appliquer, ou exporter le plan pour relecture hors ligne.
- L'horodatage du plan et son empreinte, avec la mention que l'application vérifiera que
  l'arborescence n'a pas bougé depuis.

## Étapes

1. `T-00-14-01` En-tête : compteurs, horodatage du plan, bandeau de mode.
2. `T-00-14-02` Grille avant / après.
3. `T-00-14-03` Colonne des motifs.
4. `T-00-14-04` Séparation conformes / à renommer / sans date.
5. `T-00-14-05` Actions.

## Vérification

Ouvrir `docs/20-mockups/05-rename-plan.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- Le sens du changement est-il évident ? Une confusion avant/après sur un écran de renommage de
  masse serait grave.
- Le bandeau de mode est-il visible sans défiler ?

## Commit

```
feat(US-00-14): add rename-plan mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
