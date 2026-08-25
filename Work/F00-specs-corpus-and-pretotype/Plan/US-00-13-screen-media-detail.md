# US-00-13 — Mockup: Media detail, why this date

> **Feature** F00 — Specs corpus & pretotype · **Lot 13/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner le panneau qui explique, pour un fichier donné, **toutes** les dates candidates
et pourquoi l'une l'emporte.

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
docs/20-mockups/04-media-detail.html
```

## Contenu attendu

C'est l'écran qui distingue YAIT d'un renommeur de fichiers. `dvd-tools` produisait cette
information dans une colonne de CSV que personne ne lisait ; ici elle devient consultable.

- L'aperçu du média et son chemin complet.
- **La liste de toutes les dates candidates**, une ligne par source : date lue dans le nom, date
  portée par chaque répertoire ancêtre, date des métadonnées, date d'un sidecar. Chacune avec sa
  valeur et son statut : retenue, écartée, absente.
- **La raison de l'arbitrage**, en une phrase lisible : « la date du nom prime sur les métadonnées
  parce qu'elle a été écrite délibérément », ou « métadonnée écartée : 412 jours d'écart avec le
  répertoire, horloge d'appareil probablement jamais réglée ».
- Les métadonnées existantes du fichier : titre, objet, commentaire, dimensions, poids.
- Le nom cible proposé.

Montrer **au moins deux variantes** dans la maquette : un cas simple où tout concorde, et un cas
d'arbitrage où une source est écartée. Le second est le seul qui justifie l'écran.

## Étapes

1. `T-00-13-01` Structure du panneau latéral, en-tête et aperçu.
2. `T-00-13-02` Tableau des dates candidates avec leurs statuts.
3. `T-00-13-03` Encart d'explication de l'arbitrage.
4. `T-00-13-04` Métadonnées existantes et nom cible.
5. `T-00-13-05` La seconde variante, avec une source écartée.

## Vérification

Ouvrir `docs/20-mockups/04-media-detail.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- Faire lire l'encart d'arbitrage à quelqu'un qui ne connaît pas le projet : comprend-il pourquoi
  cette date-là a été retenue ?
- Le cas « horloge d'appareil fausse » est-il compréhensible sans jargon ?

## Commit

```
feat(US-00-13): add media-detail mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
