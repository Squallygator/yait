# US-00-16 — Mockup: Organize and flatten

> **Feature** F00 — Specs corpus & pretotype · **Lot 16/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner l'écran de rangement : la répartition prévisionnelle des fichiers, en mode
arborescent `YYYY/MM` ou en mode à plat.

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
docs/20-mockups/07-organize.html
```

## Contenu attendu

- Un sélecteur entre les deux modes, avec une phrase expliquant à quoi sert chacun. Le mode à
  plat existe parce que les noms commencent par la date : le tri alphabétique donne l'ordre
  chronologique, ce qui permet de tout sélectionner d'un bloc pour un envoi vers un service de
  tirage.
- La **répartition prévisionnelle** : combien de fichiers dans chaque destination. En mode
  arborescent, une vue par année et par mois.
- Le sort des fichiers sans date : un répertoire dédié en mode arborescent, **laissés sur place**
  en mode à plat. Cette différence doit être explicite à l'écran, c'est une règle assumée.
- Le sort des fichiers datés à l'année seule : rangés à la racine de l'année, sans mois inventé.
- Le garde-fou : le rangement refuse de démarrer s'il reste des doublons de noms.

## Étapes

1. `T-00-16-01` Sélecteur de mode et explications.
2. `T-00-16-02` Répartition prévisionnelle par destination.
3. `T-00-16-03` Traitement visible des sans-date et des dates à l'année.
4. `T-00-16-04` État bloqué par le garde-fou de doublons.

## Vérification

Ouvrir `docs/20-mockups/07-organize.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- La différence de traitement des fichiers sans date entre les deux modes est-elle compréhensible ?
- L'état bloqué explique-t-il quoi faire pour débloquer ?

## Commit

```
feat(US-00-16): add organize mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
