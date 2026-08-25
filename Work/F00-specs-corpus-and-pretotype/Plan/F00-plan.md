# F00 — Specs corpus & pretotype · plan consolidé

Document de **référence**, pas d'exécution. Pour exécuter, prendre une fiche de lot
`US-00-<nn>-*.md` : elle est autosuffisante.

Le plan directeur du programme entier est conservé dans
[`brief/plan-v3-approved.md`](brief/plan-v3-approved.md).

---

## Objectif de la feature

Livrer, **avant toute ligne de code de production** :

1. un **corpus d'échantillons** reproductible sur n'importe quelle machine, dérivé d'une seule
   photo seed embarquée au dépôt ;
2. les **60 règles métier** écrites sous forme de spécifications exécutables ;
3. les **12 écrans** en maquettes HTML statiques, navigables ;
4. une **revue de pretotyping** qui peut réordonner le reste du backlog.

Aucune écriture dans `src/`. Aucune API. Aucun test de production.

---

## Arbitrages retenus

| Sujet | Décision | Motif |
|---|---|---|
| Générateur d'échantillons | **Pillow en prérequis dev** | Aucun codec JPEG en stdlib : sans lui, pas de résolutions différentes, donc `UC-27` inspécifiable. Pillow est déjà une dépendance runtime gelée. |
| `strip_exif.py` | **stdlib pure**, par exception | Seule vérification qu'un relecteur externe fera sans environnement. |
| Corpus | **commité**, régénération non requise | « Lancer les tests partout » compte ; « régénérer partout » non. |
| Vérification en CI | **manifeste**, pas les octets | L'encodeur JPEG de Pillow n'est pas stable d'une version à l'autre. |
| Source de vérité | **`rule.md`**, jamais un fichier de fixtures | Un manifeste unique aurait grossi sans fin et inversé la hiérarchie. |
| Polarité des règles | **Enforced ▶ / Assumed exclusion ⊘**, pas de troisième état | Un revirement doit produire un test rouge et une règle à supprimer. |
| Licence du corpus | **CC0** | MIT est une licence logicielle, inadaptée à une photographie. |
| Archive réelle | **jamais commitée** | Noms de personnes, événements privés. `@pytest.mark.private`, hors CI. |

---

## Architecture des specs

```
specs/
├── README.md                       comment lire et ajouter une règle
├── LICENSE                         CC0
├── _seed/river.jpg                 900×403, aucune métadonnée
├── _templates/                     rule.md · rule.feature · samples.yaml · group.md
└── RG-<n>-<slug>/
    ├── group.md                    intention du groupe ET ses frontières
    └── [RG-<n>.<m>-<slug>/]
        └── UC-<nn>-<slug>/
            ├── rule.md             la règle, son pourquoi, son bloc Decision
            ├── rule.feature        un scénario Gherkin écrit à la main
            ├── samples.yaml        recette technique des fichiers d'exemple
            └── files/              les échantillons générés, commités
```

Quatre artefacts, toujours. Rien n'est généré depuis rien : `rule.feature` et `samples.yaml` ne
se rejoignent que par **le nom des fichiers**.

## Règles transverses

- **Vocabulaire de pas Gherkin figé**, implémenté une seule fois dans `tests/acceptance/steps/`.
  Tout scénario résolvant une date doit affirmer **d'où elle vient** : une bonne date obtenue pour
  une mauvaise raison est un bug en sursis.
- **Identifiants d'UC plats et permanents.** `UC-14` garde son numéro même s'il change de groupe.
  Le regroupement vit dans l'arborescence, jamais dans le numéro.
- **Aucun nom de personne réelle, aucun événement privé** dans le corpus. Les cas observés dans
  l'archive privée sont transposés en formulation neutre.
- **Rien de lourd.** Les échantillons portent un nom, un dossier et quelques champs de métadonnées ;
  les pixels ne comptent presque jamais. Budget de taille vérifié en CI.

## Les 7 groupes de règles

| Groupe | Rôle | Règles |
|---|---|---|
| RG-1 | Date resolution — le cœur | 29 (4 sous-groupes) |
| RG-2 | File classification | 5 |
| RG-3 | Target naming | 5 |
| RG-4 | Collisions | 2 |
| RG-5 | Metadata deduction & writing | 6 |
| RG-6 | Organizing | 3 |
| RG-7 | Safety & reversibility | 6 |

15 des 60 sont des **exclusions assumées** ⊘. C'est ce qui distingue ce backlog d'une liste de
fonctionnalités : chacune est un choix daté, justifié, testé — révocable par un test rouge,
jamais par un oubli.

---

## Découpage en lots

| Lot | Titre | Dépend de |
|---|---|---|
| `US-00-01` ✅ | Repository bootstrap | — |
| `US-00-02` ✅ | Seed photograph | 01 |
| `US-00-03` ✅ | Specs structure | 01 |
| `US-00-04` | Sample generator — images | 02, 03 |
| `US-00-05` | Sample generator — forged artefacts | 04 |
| `US-00-06` | Write RG-1 rules | 05 |
| `US-00-07` | Write RG-2 to RG-7 rules | 05 |
| `US-00-08` | Spec guards in CI | 06, 07 |
| `US-00-09` | Design system | 03 |
| `US-00-10` → `US-00-20` | Les 12 écrans | 09 |
| `US-00-21` | Clickable prototype | 10→20 |
| `US-00-22` | Pretotyping review — **point d'arrêt** | 21 |

Deux chaînes parallèles : **corpus** (04→08) et **maquettes** (09→21). Elles ne se rejoignent
qu'en `US-00-21`, où le prototype affiche les vrais noms du corpus.

---

## Vérification de fin de feature

```
python tools/build_samples.py --check
python tools/strip_exif.py --check specs/_seed/river.jpg
python tools/check_specs.py
```

Puis : ouvrir `docs/20-mockups/index.html`, parcourir les 12 écrans dans les deux thèmes, à
1280 px et 1920 px, en vérifiant qu'ils affichent bien les noms de fichiers du corpus.

Sortie attendue de `US-00-22` : un journal de décisions et, le cas échéant, un backlog réordonné.

---

## Risques

| Risque | Parade |
|---|---|
| Le générateur produit des fixtures subtilement fausses → tests verts qui ne prouvent rien | Minimiser le code maison (Pillow plutôt qu'IFD à la main) ; `--check` régénère et compare le manifeste |
| Le corpus grossit sans contrôle | Budget de taille en CI ; échantillons minuscules par défaut |
| Les 60 règles rédigées mécaniquement, sans réfléchir au pourquoi | `rule.md` impose une section `## Why` et un bloc `Decision` ; `check_specs.py` refuse un bloc incomplet |
| Les maquettes montrent une ergonomie invalidable par les contraintes techniques | Elles précèdent l'API : c'est le principe. `US-00-22` peut réordonner |
| Une exclusion assumée devient un oubli déguisé | Test **vert** obligatoire affirmant le repli ; pas de statut « à faire » |
