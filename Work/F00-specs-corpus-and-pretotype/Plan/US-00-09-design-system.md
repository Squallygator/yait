# US-00-09 — Design system for the mockups

> **Feature** F00 — Specs corpus & pretotype · **Lot 9/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Poser la feuille de style et les composants partagés dont les douze maquettes se serviront :
jetons de couleur, thème clair/sombre, typographie, et les quelques composants qui reviennent
partout (tableau dense, barre de filtres, pastilles de statut, boutons, panneau latéral).

Les maquettes sont du **HTML statique** : on regarde des écrans, on ne construit pas encore
l'application. Mais ce qui est écrit ici sera repris tel quel par `US-01-06` pour la coquille
réelle de l'IHM — donc autant que ce soit propre.

## État au démarrage

Rien côté interface. Le dépôt contient `specs/`, `tools/` et la documentation de projet.
Aucun `docs/20-mockups/`, aucun CSS, aucun JavaScript.

## Règles applicables

- **Vanilla, zéro build.** Pas de npm, pas de bundler, pas de CDN. Du CSS et des modules ES
  servis en statique. C'est une décision arrêtée (ADR-004) : la machine cible ne doit rien avoir
  à installer, et le projet ne doit pas entretenir une seconde culture technique.
- **Pas de `innerHTML` construit par concaténation.** `textContent` et création de nœuds. Dans
  `dvd-tools`, un seul endroit dérogeait à cette règle et interpolait un en-tête de CSV non
  échappé — inoffensif en l'état, à une distraction de l'être.
- **Thème clair et sombre**, par jetons CSS. Les deux doivent être regardables : l'outil sert à
  trier des photos, souvent le soir.
- **Densité.** Ces écrans affichent des milliers de lignes de fichiers. Le confort de lecture
  d'une grille dense prime sur l'aération.

## Livrables

```
docs/20-mockups/
├── assets/
│   ├── mockup.css          jetons, thème, composants
│   └── mockup.js           le strict minimum : bascule de thème, tri de colonne
└── components.html         la galerie de composants, qui sert de référence visuelle
```

`components.html` n'est pas un écran de l'application : c'est la planche de référence où l'on
voit tous les composants côte à côte. Elle sert à juger la cohérence avant de dessiner les écrans.

## Contenu attendu

**Jetons** — surface, surface élevée, bordure, texte, texte atténué, accent, et quatre couleurs
sémantiques correspondant aux quatre statuts du domaine : conforme, à remplir, divergent, rien à
proposer. Ces quatre-là ne sont pas décoratives, elles portent du sens métier et se retrouveront
dans l'éditeur de métadonnées.

**Composants** — au minimum :

| Composant | Usage |
|---|---|
| Grille dense | l'inventaire, le plan de renommage, l'éditeur |
| Barre de filtres | sélecteurs + recherche plein texte |
| Pastille de statut | les quatre statuts, en une lettre, lisible d'un coup d'œil |
| Pastille de source de date | `file-name`, `folder-name`, `embedded-metadata`, `sidecar` |
| Bouton primaire / secondaire / danger | les actions destructives se distinguent |
| Panneau latéral | le détail d'un média |
| Barre de progression | les traitements longs |
| État vide | pas de résultat, pas de collection sélectionnée |
| Bandeau d'avertissement | mode simulation, opération irréversible |

**Le bandeau « simulation »** mérite une attention particulière : la simulation par défaut est un
engagement central du produit, et l'utilisateur doit voir en permanence dans quel mode il est.
C'est un composant, pas une mention en bas de page.

## Étapes

1. `T-00-09-01` Arborescence `docs/20-mockups/assets/`.
2. `T-00-09-02` Jetons et thème clair/sombre dans `mockup.css`.
3. `T-00-09-03` Typographie et grille dense.
4. `T-00-09-04` Les composants listés ci-dessus.
5. `T-00-09-05` `mockup.js` : bascule de thème et tri de colonne, rien d'autre.
6. `T-00-09-06` `components.html` : la planche de référence.

## Vérification

Ouvrir `docs/20-mockups/components.html` dans un navigateur.

Aucune commande automatisable à ce stade : il n'y a ni test ni linter côté interface, et il ne
faut pas prétendre le contraire. La vérification est visuelle.

## Vérification manuelle (STOP)

- Basculer clair / sombre : les quatre couleurs de statut doivent rester distinguables dans les
  deux thèmes, y compris pour quelqu'un qui distingue mal le rouge et le vert — ne pas s'appuyer
  sur la seule couleur, garder la lettre.
- Regarder à 1280 px et à 1920 px.
- Vérifier qu'aucune requête réseau ne part : onglet réseau vide, hors les fichiers locaux.

## Commit

```
feat(US-00-09): add mockup design system and component gallery
```

## Ne pas faire

- Ne pas dessiner d'écran de l'application : ils arrivent à partir de `US-00-10`.
- Ne pas installer de dépendance, ne pas créer de `package.json`.
- Ne pas écrire de logique métier en JavaScript : les maquettes sont statiques, les données y
  sont en dur.
