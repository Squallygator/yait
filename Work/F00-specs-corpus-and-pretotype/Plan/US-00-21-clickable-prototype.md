# US-00-21 — Clickable prototype

> **Feature** F00 — Specs corpus & pretotype · **Lot 21/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Relier les onze écrans en un parcours navigable, avec un index, pour qu'on puisse traverser
l'application du début à la fin et juger l'enchaînement — pas seulement les écrans pris isolément.

C'est ce qui transforme une collection de maquettes en pretotype.

## État au démarrage

- `docs/20-mockups/assets/` — le design system
- `docs/20-mockups/components.html` — la planche de référence
- Les onze écrans, de `01-home.html` à `11-states.html`
- Le corpus d'échantillons sous `specs/`, dont les vrais noms peuplent les maquettes

## Règles applicables

- **Vanilla, zéro build.** Les liens sont des `<a href>`, la navigation est celle du navigateur.
- **Aucune logique métier.** Le prototype simule un parcours, il ne calcule rien.
- **Cohérence de l'enchaînement** : chaque écran doit offrir la sortie vers l'écran suivant du
  parcours naturel, et un retour.

## Livrable

```
docs/20-mockups/index.html      l'index + le parcours
```

Plus les liens de navigation ajoutés dans les onze écrans existants.

## Contenu attendu

**L'index** : les douze pages listées avec, pour chacune, une phrase disant ce qu'elle montre et
ce qu'on est censé y juger. Un lecteur qui arrive par le dépôt GitHub doit comprendre en trente
secondes ce qu'il regarde.

**Le parcours principal**, celui qu'on traversera en revue :

```
Home → Collection summary → Job progress → Inventory → Media detail
     → Rename plan → Collisions → Organize → History
```

L'éditeur de métadonnées et la page des états dégradés sont hors parcours principal : ils
s'atteignent depuis l'index.

**Une barre de navigation** discrète en tête de chaque maquette : retour à l'index, écran
précédent, écran suivant. Elle est visiblement un artifice de maquette, pas un élément de
l'application — le distinguer clairement, sans quoi la revue jugera un chrome qui n'existera pas.

## Étapes

1. `T-00-21-01` Écrire `index.html` : la liste commentée des douze pages.
2. `T-00-21-02` Définir le parcours principal et l'afficher comme tel dans l'index.
3. `T-00-21-03` Ajouter la barre de navigation de maquette aux onze écrans.
4. `T-00-21-04` Traverser le parcours de bout en bout et corriger les impasses.
5. `T-00-21-05` Vérifier que les données affichées viennent bien du corpus réel, et corriger
   les écrans où du texte de remplissage subsiste.

## Vérification

Ouvrir `docs/20-mockups/index.html` et parcourir les douze pages, dans les deux thèmes, à 1280 px
puis 1920 px.

Aucune commande automatisable : pas de test ni de linter côté interface à ce stade.

Contrôle qui, lui, est mécanisable et vaut la peine : vérifier qu'aucune page ne référence une
ressource externe.

```bash
grep -rniE "https?://|cdn|googleapis" docs/20-mockups --include=*.html --include=*.css --include=*.js
```

Attendu : aucune correspondance, hors éventuels liens de documentation en commentaire.

## Vérification manuelle (STOP)

- Traverser le parcours principal sans jamais utiliser le bouton « retour » du navigateur : y
  a-t-il une impasse ?
- Compter les écrans où subsiste du texte de remplissage : il doit y en avoir zéro. Une maquette
  peuplée de faux noms ne permet pas de juger la densité réelle, et c'est tout l'intérêt d'avoir
  construit le corpus avant.

## Commit

```
feat(US-00-21): link the mockups into a navigable prototype
```

## Ne pas faire

- Ne pas câbler d'API, ne pas ajouter de dépendance.
- Ne pas modifier le fond des écrans : ce lot relie, il ne redessine pas. Une correction
  nécessaire se fait dans le lot de l'écran concerné, ou se note pour `US-00-22`.
