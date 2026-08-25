# US-00-20 — Mockup: Empty, error and permission states

> **Feature** F00 — Specs corpus & pretotype · **Lot 20/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner les états dégradés que les autres écrans ne montrent pas : vides, erreurs,
permissions refusées.

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
docs/20-mockups/11-states.html
```

## Contenu attendu

Ce sont les écrans qu'on oublie de dessiner et qu'on découvre en production. Les regrouper sur
une page force à les traiter.

Au minimum :

| État | Contexte |
|---|---|
| Aucune collection sélectionnée | premier lancement |
| Chemin inexistant | saisie erronée |
| Chemin illisible | permissions refusées par le système |
| Chemin hors des racines autorisées | tentative de sortie du périmètre |
| Collection vide | dossier sans média |
| Aucun résultat | filtres trop restrictifs |
| Service backend injoignable | le processus s'est arrêté |
| Traitement en échec | erreur pendant un lot, avec ce qui a été fait |
| Chemin trop long | limite Windows dépassée |

Chaque état dit **ce qui s'est passé** et **quoi faire ensuite**. Un message d'erreur qui ne
propose pas d'action est un cul-de-sac.

## Étapes

1. `T-00-20-01` Structure de la page en sections.
2. `T-00-20-02` Les états vides.
3. `T-00-20-03` Les états d'erreur de chemin.
4. `T-00-20-04` Les états d'erreur système.
5. `T-00-20-05` Relire chaque message : contient-il une action ?

## Vérification

Ouvrir `docs/20-mockups/11-states.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- Lire les neuf messages à la suite : sont-ils compréhensibles par quelqu'un qui n'a pas écrit
  le code ?
- Aucun ne doit contenir de terme technique non expliqué, ni de trace d'exception.

## Commit

```
feat(US-00-20): add empty-and-error-states mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
