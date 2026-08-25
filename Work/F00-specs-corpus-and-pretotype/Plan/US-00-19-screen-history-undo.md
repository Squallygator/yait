# US-00-19 — Mockup: History and undo

> **Feature** F00 — Specs corpus & pretotype · **Lot 19/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner l'écran d'historique des opérations et d'annulation.

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
docs/20-mockups/10-history-undo.html
```

## Contenu attendu

Chaque opération réelle écrit un journal, et l'annulation le rejoue à l'envers. C'est l'un des
engagements centraux du produit et il mérite un écran, pas une commande obscure.

- La liste des opérations, de la plus récente à la plus ancienne : date, type, nombre de fichiers,
  état (appliquée, annulée).
- Le détail d'une opération : les déplacements ou les écritures qu'elle contient.
- L'action d'annulation, avec sa confirmation.
- **Le garde-fou d'ordre** : on n'annule pas une opération ancienne si une plus récente n'a pas
  été annulée d'abord. L'écran doit le dire et proposer la bonne action, pas simplement refuser.
- L'état d'une opération partiellement annulable : des fichiers ne sont plus là où le journal les
  attend.

## Étapes

1. `T-00-19-01` Liste des opérations.
2. `T-00-19-02` Détail d'une opération.
3. `T-00-19-03` Confirmation d'annulation.
4. `T-00-19-04` État bloqué par le garde-fou d'ordre, avec la sortie proposée.

## Vérification

Ouvrir `docs/20-mockups/10-history-undo.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- Le garde-fou d'ordre est-il compréhensible ? C'est le point où un utilisateur pressé peut
  s'énerver et forcer.
- L'action d'annulation est-elle assez visible sans être dangereusement facile à déclencher ?

## Commit

```
feat(US-00-19): add history-undo mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
