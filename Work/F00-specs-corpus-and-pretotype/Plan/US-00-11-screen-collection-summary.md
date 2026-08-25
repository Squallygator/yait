# US-00-11 — Mockup: Collection summary

> **Feature** F00 — Specs corpus & pretotype · **Lot 11/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Dessiner l'écran qui suit la validation d'un chemin : ce que contient la collection,
avant tout traitement.

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
docs/20-mockups/02-collection-summary.html
```

## Contenu attendu

C'est l'écran de confiance : l'utilisateur vérifie qu'il a désigné le bon dossier avant de
lancer quoi que ce soit.

- Le chemin retenu, en évidence, **complet et non tronqué**. Se tromper de racine est le premier
  risque de l'outil.
- Volumétrie : nombre de fichiers, poids total, nombre de répertoires.
- Répartition par extension, les douze premières.
- Répartition par type : image, vidéo, archive, autre.
- Les alertes éventuelles : fichiers illisibles détectés, fichiers de 0 octet, fichiers parasites.
  **Signalées, pas traitées** — aucune action destructive depuis cet écran.
- Le bouton qui lance l'inventaire.

## Étapes

1. `T-00-11-01` En-tête avec le chemin retenu.
2. `T-00-11-02` Cartes de volumétrie.
3. `T-00-11-03` Répartitions par extension et par type.
4. `T-00-11-04` Bandeau d'alertes.
5. `T-00-11-05` Action de lancement de l'inventaire.

## Vérification

Ouvrir `docs/20-mockups/02-collection-summary.html` dans un navigateur, dans les deux thèmes.

Aucune commande automatisable : il n'y a ni test ni linter côté interface à ce stade, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- Le chemin est-il lisible en entier, y compris un chemin profond avec des accents ?
- Les alertes se distinguent-elles clairement d'une information neutre, sans être alarmistes ?
  Un fichier illisible sur un CD de vingt ans est attendu, pas catastrophique.

## Commit

```
feat(US-00-11): add collection-summary mockup
```

## Ne pas faire

- Ne pas câbler d'API : les maquettes précèdent le backend, c'est le principe du pretotyping.
- Ne pas dessiner un autre écran que celui-ci.
- Ne pas ajouter de dépendance JavaScript.
