# US-00-10 — Mockup: Home, choosing a collection

> **Feature** F00 — Specs corpus & pretotype · **Lot 10/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner l'écran d'accueil : saisie du chemin de la collection à traiter, et
liste des collections récemment ouvertes.

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
docs/20-mockups/01-home.html
```

## Contenu attendu

Le navigateur ne donne jamais de chemin disque réel au backend : c'est pourquoi la saisie se
fait au clavier ou par collage, décision arrêtée (ADR-006). L'écran doit rendre ce geste
confortable malgré tout.

- Un champ de saisie large, avec un exemple de chemin en indication.
- Un bouton de validation, et l'état d'erreur associé : chemin inexistant, chemin illisible,
  chemin hors des racines autorisées.
- La liste des **collections récentes** : chemin, date de dernière ouverture, nombre de fichiers
  connu. C'est elle qui fait le vrai gain d'ergonomie, la saisie n'étant utile qu'une fois.
- Un mot sur ce que l'outil va faire, pour quelqu'un qui ouvre l'application pour la première
  fois. Deux phrases, pas une page.

## Étapes

1. `T-00-10-01` Structure de la page et en-tête.
2. `T-00-10-02` Champ de saisie et bouton de validation.
3. `T-00-10-03` Les trois états d'erreur, montrés en variantes commentées dans le HTML.
4. `T-00-10-04` Liste des collections récentes, avec trois entrées plausibles.

## Vérification

Ouvrir `docs/20-mockups/01-home.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- Se demander honnêtement : quelqu'un qui découvre l'outil comprend-il quoi coller dans le champ ?
- Vérifier qu'un chemin Windows long s'affiche sans casser la mise en page.

## Commit

```
feat(US-00-10): add home mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
