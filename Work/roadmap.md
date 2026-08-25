# Roadmap YAIT

Vue programme : les dix features, leur ordre et leurs dépendances. Ni une fiche de lot, ni le
plan d'une feature — l'endroit où l'on voit la trajectoire d'ensemble.

Détail d'un lot : `F<nn>-<slug>/Plan/US-<nn>-<mm>-*.md`. Vue de pilotage : [`todo.md`](todo.md).

---

## Ce qu'on construit

Un normaliseur d'archives photo/vidéo local : IHM navigateur adossée à une API FastAPI locale.
Réécriture de `dvd-tools`, dont l'audit a produit 36 findings — 5 pouvant détruire des originaux.

Décisions structurantes, arrêtées avant le premier commit :

| Sujet | Décision |
|---|---|
| Lancement | Natif (`yait.ps1` / `yait.sh` + venv + uvicorn). Docker étudié et **différé** en F09. |
| Sélection du dossier | Saisie / collage du chemin, validée côté API, avec historique. |
| Front-end | Vanilla ESM zéro-build, servi en statique. Aucun npm, aucun bundler. |
| Méthode produit | **Pretotyping** : les maquettes constituent le lot 0, avec un point d'arbitrage. |
| Méthode spec | **Specification by Example** : 1 règle → 1 exemple → 1 test d'acceptance. |
| Corpus de test | Généré depuis une image seed unique + artefacts forgés, embarqué au dépôt. |
| Première livraison de code | Walking skeleton **en lecture seule**. Aucune écriture disque avant le lot 2. |

---

## Les features

| # | Feature | Lot | Rôle |
|---|---|---|---|
| **F00** | Specs corpus & pretotype | 0 | Le corpus d'échantillons et les maquettes. Aucune ligne de code de production. |
| **F01** | Foundation & launcher | 1 | Squelette Python, API minimale, lanceur, journalisation, coquille d'IHM. |
| **F02** | Collections | 1 | Saisir et valider un chemin, historique des collections récentes. |
| **F03** | Inventory & date resolution | 1 | **Le cœur métier.** Résolution des dates et traçabilité de la source. |
| **F07** | Journal & undo | 2 | Livré **avant** toute écriture, par principe. |
| **F04** | Renaming | 2 | Politique de nommage, collisions, plan figé, exécution. |
| **F05** | Organizing | 2 | Rangement `YYYY/MM`, mise à plat, nettoyage. |
| **F06** | Metadata | 3 | Lecture, déduction, écriture EXIF/XMP, éditeur. |
| **F08** | Quality & safety | 4 | Tests d'attaque, contract testing, robustesse, campagne de non-régression. |
| **F09** | Distribution | 4 | Réévaluation Docker, installation à froid, finition du dépôt public. |

L'ordre de livraison n'est pas l'ordre des numéros : **F07 précède F04**. Le journal et
l'annulation existent avant la première écriture disque, pas après.

---

## Dépendances

```
F00 ──► F01 ──► F02 ──► F03 ──► F07 ──► F04 ──► F05 ──► F06 ──► F08 ──► F09
 │                       ▲               ▲
 └── le corpus alimente ─┘               │
     les tests de F03+                   │
                                         │
     F04-01 (atomic_write, PathGuard) ───┘  socle d'écriture, prérequis de F05 et F06
```

- **F00 ne dépend de rien** et conditionne tout : sans corpus, aucun test d'acceptance.
- **US-00-22 est un point d'arrêt.** Le backlog au-delà de F00 n'est figé qu'après la revue de
  pretotyping, qui peut le réordonner. Les fiches de lot de F01 à F09 sont donc écrites au
  démarrage de leur feature, pas maintenant.
- **F03 est le cœur.** Tout ce qui précède existe pour lui permettre d'être testé ; tout ce qui
  suit exploite son résultat.

---

## Les 36 findings de `dvd-tools`

L'audit initial est la dette de départ. Chaque finding est rattaché à la règle ou au lot qui le
traite — matrice complète dans `docs/00-project/09-traceability.md` (produit en F01).

Les cinq critiques, pour mémoire :

| # | Défaut | Traité par |
|---|---|---|
| #1 | Écriture EXIF en place, non atomique — une coupure détruit la photo | `UC-49` · F04-01 · F06-05 |
| #2 | Journal écrit après la boucle — un plantage supprime toute possibilité d'annuler | `UC-50` · F07-01 |
| #3 | Idem sur les déplacements de fichiers | `UC-50` · F07-01 |
| #4 | Écriture CSV non atomique | `UC-49` · F04-01 |
| #5 | `--hard-delete` : suppression de masse irréversible, sans journal ni confirmation | F05, corbeille seule |

Et les trois qui rendaient le mode simulation mensonger : #6 (conflit `.thm`), #7 (le plan relu
n'est pas le plan appliqué), #8 (ordre des renommages non topologique).

---

## Limites assumées de ce document

- Les lots de **F01 à F09 ne sont pas détaillés** en fiches. C'est délibéré : le plan approuvé
  place un point d'arbitrage en `US-00-22`, et écrire maintenant des fiches que cette revue peut
  invalider serait du travail jeté. Les intitulés de lot figurent dans [`todo.md`](todo.md).
- Les estimations de charge ne figurent nulle part. Elles n'ont pas été demandées et seraient
  inventées.
