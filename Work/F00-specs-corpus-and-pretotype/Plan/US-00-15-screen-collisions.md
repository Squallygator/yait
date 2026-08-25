# US-00-15 — Mockup: Collisions

> **Feature** F00 — Specs corpus & pretotype · **Lot 15/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner l'écran des collisions de noms : quels fichiers se disputent le même nom cible,
et dans quel ordre ils seront départagés.

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
docs/20-mockups/06-collisions.html
```

## Contenu attendu

L'unicité est vérifiée sur **toute la collection**, pas répertoire par répertoire, parce que la
destination est souvent un dépôt à plat où les répertoires n'existent plus.

- Un groupe par nom cible en conflit, avec les fichiers concurrents en dessous.
- Pour chaque concurrent : sa résolution, son poids, son heure de prise de vue, son chemin —
  c'est-à-dire les quatre critères de départage, dans l'ordre où ils s'appliquent.
- Le suffixe qui sera attribué (`_1`, `_2`), et **pourquoi ce fichier-là obtient `_1`**.
- Le cas particulier des sous-répertoires `Originals` : le master brut reçoit un suffixe distinct
  et sort donc du conflit. Le montrer, c'est un cas fréquent et déroutant.

## Étapes

1. `T-00-15-01` Structure en groupes.
2. `T-00-15-02` Détail d'un concurrent avec ses quatre critères.
3. `T-00-15-03` Affichage du suffixe attribué et de sa justification.
4. `T-00-15-04` Un groupe illustrant le cas `Originals`.

## Vérification

Ouvrir `docs/20-mockups/06-collisions.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- L'ordre de départage est-il compréhensible sans lire la documentation ?
- Un utilisateur peut-il repérer un départage qui ne lui convient pas ?

## Commit

```
feat(US-00-15): add collisions mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
