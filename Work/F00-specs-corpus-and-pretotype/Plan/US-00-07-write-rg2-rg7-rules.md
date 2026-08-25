# US-00-07 — Write the RG-2 to RG-7 rules

> **Feature** F00 — Specs corpus & pretotype · **Lot 7/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md) puis [`specs/README.md`](../../../specs/README.md).

## Objectif

Écrire les **31 règles restantes** : classification des fichiers, nommage cible, collisions,
métadonnées, rangement, et sûreté. Chaque règle reçoit ses quatre artefacts.

Indépendant de `US-00-06` (les règles de résolution de date) : les deux lots peuvent être menés
dans n'importe quel ordre, ou en parallèle sur des branches distinctes.

## État au démarrage

- `specs/README.md`, `specs/_templates/`, et `UC-14-deepest-folder-wins` comme exemple de référence
- Les six `group.md` de `RG-2` à `RG-7`, **avec leurs tables de règles** qui listent nommément les
  31 UC attendus et ce que chacun décide
- `tools/build_samples.py` — images dérivées et artefacts forgés

## Règles applicables

Identiques à `US-00-06` : `rule.md` d'abord, polarité obligatoire, une exclusion affirme un repli
et jamais une absence, l'exemple est choisi pour qu'une implémentation fausse échoue, aucun nom de
personne réelle.

## Livrables

| Groupe | Règles | Dont exclusions ⊘ |
|---|---|---|
| `RG-2` classification des fichiers | 5 | 1 (`UC-59`) |
| `RG-3` nommage cible | 5 | 0 |
| `RG-4` collisions | 2 | 0 |
| `RG-5` métadonnées | 6 | 1 (`UC-33`) |
| `RG-6` rangement | 3 | 1 (`UC-47`) |
| `RG-7` sûreté et réversibilité | 6 | 0 |

## Étapes

1. `T-00-07-01` `RG-2` classification. Commit.
2. `T-00-07-02` `RG-3` nommage cible. Commit.
3. `T-00-07-03` `RG-4` collisions. Commit.
4. `T-00-07-04` `RG-5` métadonnées. Commit.
5. `T-00-07-05` `RG-6` rangement. Commit.
6. `T-00-07-06` `RG-7` sûreté. Commit.
7. `T-00-07-07` Générer tous les `files/` et vérifier le manifeste.

## Points d'attention par groupe

**RG-2** — `UC-38` (un `.THM` survit tant que sa vidéo existe) est le jumeau de `UC-22` en
`RG-1.3`. Les deux facettes du finding #6 : dans `dvd-tools`, l'une disait que le `.THM` datait la
vidéo et l'autre l'envoyait à la corbeille — et le nettoyage passait en premier. Les séparer est
délibéré ; chaque `rule.md` doit renvoyer à l'autre dans sa section `## Scope`.

**RG-3** — `UC-41` (idempotence) est la règle qui rend l'outil sûr à relancer sur une archive
à moitié traitée, ce qui est exactement ce qui arrive quand un lot est interrompu. Son scénario
doit exercer un **deuxième passage**, pas seulement un premier.

**RG-4** — `UC-27` (départage par qualité) exige des échantillons de **résolutions différentes** :
c'est la raison pour laquelle Pillow est devenu prérequis de développement. Vérifier que les
images générées ont bien des dimensions distinctes, sans quoi la règle est inspécifiable.

**RG-5** — `UC-44` (écriture sans ré-encodage) se spécifie en affirmant que le **scan compressé
est identique au bit près** avant et après écriture. `tools/strip_exif.py` fait déjà cette
vérification sur le seed : s'en inspirer.
`UC-33` est une exclusion : son scénario affirme qu'un champ déjà rempli **conserve sa valeur**,
pas que l'écriture échoue.

**RG-6** — `UC-47` est une exclusion : en mode « à plat », les fichiers non datés **restent en
place**. Le scénario doit vérifier leur présence à leur emplacement d'origine.

**RG-7** — Ces six règles ne se spécifient pas comme les autres : elles portent sur des propriétés
d'exécution (atomicité, ordre d'écriture, confinement) plutôt que sur l'interprétation d'un
fichier. Leurs `rule.feature` décriront des scénarios d'interruption et de tentative d'évasion.
Rédiger l'énoncé et le scénario ; la façon de simuler une coupure relève de `US-08-04`, et il faut
l'écrire noir sur blanc dans le `rule.md` plutôt que de laisser croire que c'est couvert ici.

## Vérification

```bash
python tools/build_samples.py && python tools/build_samples.py --check
```

Puis, manuellement : quatre artefacts par UC, bloc `## Decision` complet avec polarité, et chaque
`rule.feature` nomme un fichier qui existe dans son `files/`.

## Vérification manuelle (STOP)

Relire les trois exclusions (`UC-59`, `UC-33`, `UC-47`) avec la même question qu'en `US-00-06` :
*« si on changeait d'avis demain, quel test deviendrait rouge ? »*

Puis vérifier que `UC-22` et `UC-38` se citent bien mutuellement : c'est la parade au finding #6,
et elle ne tient que si les deux règles se connaissent.

## Commit

Un commit par groupe :

```
docs(US-00-07): specify RG-2 file classification rules
docs(US-00-07): specify RG-3 target naming rules
docs(US-00-07): specify RG-4 collision rules
docs(US-00-07): specify RG-5 metadata rules
docs(US-00-07): specify RG-6 organizing rules
docs(US-00-07): specify RG-7 safety rules
```

## Ne pas faire

- Ne pas écrire une ligne de code de production.
- Ne pas écrire le pas-à-pas Python des scénarios : il arrive avec les lots d'implémentation.
- Ne pas toucher à `RG-1` : c'est `US-00-06`.
- Ne pas prétendre que `RG-7` est vérifiable en l'état : dire explicitement dans les `rule.md`
  que la simulation d'interruption relève de `US-08-04`.
