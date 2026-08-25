# US-00-18 — Mockup: Job progress

> **Feature** F00 — Specs corpus & pretotype · **Lot 18/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner l'écran de suivi d'un traitement long : progression, ce qui se passe, et comment
l'interrompre.

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
docs/20-mockups/09-job-progress.html
```

## Contenu attendu

Un inventaire de vingt mille fichiers ne tient pas dans une requête. Le suivi est donc un écran
à part entière, pas un curseur qui tourne.

- Barre de progression avec un compteur explicite : *n* sur *N* fichiers.
- Le fichier en cours de traitement, pour que l'attente soit lisible.
- Une estimation de temps restant, ou son absence assumée si elle n'est pas fiable.
- Le journal des événements notables au fil de l'eau : fichiers illisibles rencontrés, dates
  écartées. Pas tous les fichiers, seulement ce qui mérite l'attention.
- Un bouton d'interruption, et l'état obtenu après interruption : ce qui a été fait reste fait,
  ce qui reste n'est pas commencé.
- L'état terminé, avec le résumé et le lien vers l'écran de résultat.

Montrer trois variantes : en cours, interrompu, terminé.

## Étapes

1. `T-00-18-01` Barre de progression et compteurs.
2. `T-00-18-02` Journal des événements.
3. `T-00-18-03` Action d'interruption.
4. `T-00-18-04` Les trois états.

## Vérification

Ouvrir `docs/20-mockups/09-job-progress.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- L'état « interrompu » dit-il clairement ce qui a été fait et ce qui ne l'a pas été ?
- Le journal reste-t-il lisible sans défiler frénétiquement ?

## Commit

```
feat(US-00-18): add job-progress mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
