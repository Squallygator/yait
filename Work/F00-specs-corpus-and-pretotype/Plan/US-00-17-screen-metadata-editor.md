# US-00-17 — Mockup: Metadata editor

> **Feature** F00 — Specs corpus & pretotype · **Lot 17/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner l'éditeur de métadonnées, héritier de `csvedit` : la grille de relecture et de
correction des titres, objets, commentaires et dates.

Maquette **statique** : données en dur, aucune logique métier, aucun appel réseau. On regarde un
écran pour juger l'ergonomie avant de construire quoi que ce soit.

## État au démarrage

- `docs/20-mockups/assets/mockup.css` et `mockup.js` — le design system, livré en `US-00-09`
- `docs/20-mockups/components.html` — la planche de référence des composants
- Le corpus d'échantillons sous `specs/` : **utiliser ses vrais noms de fichiers** dans les
  données en dur. Une maquette peuplée de lorem ipsum ne permet pas de juger la densité réelle.
- L'ancien `csvedit.js` de `dvd-tools` est la référence ergonomique à reprendre et à améliorer.
  Ses bonnes idées : le regroupement Titre/Objet/Commentaire en une colonne avec trois pastilles
  `T O C`, les filtres par statut et par répertoire, l'application en masse, les listes
  déroulantes des libellés déjà présents.

## Règles applicables

- **Vanilla, zéro build.** Pas de npm, pas de bundler, pas de CDN.
- **Réutiliser les composants du design system**, ne pas en inventer. Si un composant manque,
  l'ajouter à `mockup.css` et à `components.html` dans le même commit.
- **Thème clair et sombre** tous les deux regardables.
- **Le bandeau de mode** (simulation / exécution) est visible en permanence quand l'écran porte
  une action qui écrit.

## Livrable

```
docs/20-mockups/08-metadata-editor.html
```

## Contenu attendu

C'est l'écran le plus riche. Les quatre statuts du domaine y sont omniprésents : conforme,
à remplir, divergent, rien à proposer.

- Grille dense : case à cocher de traitement, nom de fichier, répertoire, et une colonne par
  propriété.
- Chaque propriété se lit **valeur en place → proposition → statut**, de gauche à droite.
- **Titre, Objet et Commentaire reçoivent le même libellé** : les afficher en trois colonnes
  identiques serait illisible. Les regrouper en une seule colonne, avec trois pastilles `T O C`
  indiquant lesquels sont déjà renseignés dans le fichier, et une bascule pour revenir à
  l'affichage détaillé.
- Un marqueur quand les trois champs ne portent pas la même valeur.
- Filtres : par statut, par répertoire, par état de la case à cocher, plus une recherche.
- Application en masse d'un libellé à toutes les lignes affichées, avec confirmation.
- Un rappel que seules les lignes cochées seront écrites, et que par défaut on ne remplit que les
  champs vides.

## Étapes

1. `T-00-17-01` Barre de filtres et actions de masse.
2. `T-00-17-02` Grille avec le triptyque valeur / proposition / statut.
3. `T-00-17-03` Colonne groupée `T O C` et sa bascule.
4. `T-00-17-04` Les quatre statuts en situation.
5. `T-00-17-05` Confirmation d'application en masse.

## Vérification

Ouvrir `docs/20-mockups/08-metadata-editor.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- Comparer côte à côte avec `csvedit.js` : l'ergonomie est-elle meilleure, ou seulement différente ?
- Les quatre statuts restent-ils distinguables dans les deux thèmes, sans se fier à la seule couleur ?
- Sur cinquante lignes, repère-t-on les lignes divergentes sans les chercher ?

## Commit

```
feat(US-00-17): add metadata-editor mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
