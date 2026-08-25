# US-00-06 — Write the RG-1 rules (date resolution)

> **Feature** F00 — Specs corpus & pretotype · **Lot 6/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md) puis [`specs/README.md`](../../../specs/README.md).

## Objectif

Écrire les **29 règles de RG-1**, le cœur métier : comment une date de prise de vue est résolue,
et pourquoi telle source l'emporte sur telle autre. Chaque règle reçoit ses quatre artefacts.

C'est le lot le plus dense de la feature. **Il peut être découpé en quatre sessions**, une par
sous-groupe (`RG-1.1`, `RG-1.2`, `RG-1.3`, `RG-1.4`), avec un commit par sous-groupe. Les
sous-groupes sont indépendants entre eux.

## État au démarrage

- `specs/README.md` — le mode d'emploi, le vocabulaire de pas Gherkin, le format des recettes
- `specs/_templates/` — les quatre gabarits
- `specs/RG-1-date-resolution/` — les cinq `group.md` déjà écrits, **avec leurs tables de règles**
  qui listent nommément les 29 UC attendus et ce que chacun décide
- `UC-14-deepest-folder-wins` — **l'exemple de référence complet**, à lire avant d'écrire le
  premier `rule.md`
- `tools/build_samples.py` — sait produire images dérivées et artefacts forgés

## Règles applicables

- **`rule.md` d'abord.** Si la section `## Why` ne peut pas être écrite, la règle n'est pas prête.
  Le pourquoi est ce qui survivra : dans cinq ans personne ne se souviendra de la raison, et le
  code ne la dira pas.
- **Polarité obligatoire** dans le bloc `## Decision` : `Enforced` ▶ ou `Assumed exclusion` ⊘.
  Pas de troisième état, pas de « à faire ».
- **Une exclusion affirme un repli, jamais une absence.** `UC-09` ne dit pas « on ne sait pas lire
  les epoch » ; il dit « un horodatage epoch est ignoré, et la date vient du répertoire parent ».
- **Tout scénario qui résout une date affirme sa source.** Une bonne date obtenue pour une
  mauvaise raison est un bug en sursis.
- **Choisir l'exemple pour qu'une implémentation fausse ne puisse pas passer.** Voir `UC-14` :
  les deux dossiers datés divergent, et le plus proche est *antérieur* — un code qui prendrait le
  maximum, le minimum ou la première correspondance échouera.
- **Aucun nom de personne réelle.** Les cas de l'archive privée sont transposés en formulation
  neutre.

## Livrables

29 répertoires `UC-<nn>-<slug>/`, chacun avec `rule.md`, `rule.feature`, `samples.*` et `files/`.

Répartition, telle que fixée par les `group.md` déjà en place :

| Sous-groupe | Règles | Dont exclusions ⊘ |
|---|---|---|
| `RG-1.1` dates dans le nom de fichier | 10 | 0 |
| `RG-1.2` dates portées par les répertoires | 4 | 1 (`UC-16`) |
| `RG-1.3` dates lues dans le contenu | 9 | 3 (`UC-54`, `UC-55`, `UC-58`) |
| `RG-1.4` arbitrage et refus | 10 | 6 (`UC-08`, `UC-09`, `UC-37`, `UC-56`, `UC-57`, `UC-60`) |

`UC-14` existe déjà ; il ne reste que son `files/`, produit par le générateur.

## Étapes

1. `T-00-06-01` Lire `UC-14` en entier, puis `specs/README.md`. Ne pas commencer avant.
2. `T-00-06-02` `RG-1.1` — les dix règles de lecture du nom de fichier. Commit.
3. `T-00-06-03` `RG-1.2` — les quatre règles de répertoire. Commit.
4. `T-00-06-04` `RG-1.3` — les neuf règles de lecture du contenu. C'est ici que les artefacts
   forgés du lot précédent servent. Commit.
5. `T-00-06-05` `RG-1.4` — les dix règles d'arbitrage, dont six exclusions. Écrire `UC-36`
   (l'échelle de priorité complète) **en dernier** : il ne peut se rédiger qu'une fois les autres
   sources décrites. Commit.
6. `T-00-06-06` Générer tous les `files/` et vérifier le manifeste.

## Points d'attention par sous-groupe

**RG-1.1** — Les motifs générateurs (WhatsApp, Android, Screenshot, Windows Phone) sont
mécaniques et se ressemblent : résister à la tentation de les fusionner en une règle unique. Ils
ont des cycles de vie différents et disparaîtront séparément.

**RG-1.2** — `UC-16` (`2006-2` n'est pas février 2006) est une exclusion : son scénario doit
affirmer que la date obtenue est **l'année seule**, pas qu'aucune date n'est trouvée.

**RG-1.3** — `UC-22` (le `.THM` date la vidéo) a un jumeau en `RG-2` : `UC-38` (le `.THM` n'est
pas un déchet). Les deux facettes du finding #6. Écrire `UC-22` ici en renvoyant explicitement à
`UC-38` dans la section `## Scope`.

**RG-1.4** — Les six exclusions sont le cœur de la valeur de ce lot. Chacune doit citer
l'observation qui l'a motivée. Pour `UC-09`, l'observation est documentée : un horodatage epoch
décodait à la veille pour une photographie vieille de quinze ans. Pour `UC-37`, sur une
arborescence recopiée le `mtime` vaut la date de copie et rangerait des photos de 2011 dans le
mois courant.

## Vérification

```bash
python tools/build_samples.py && python tools/build_samples.py --check
```

Puis manuellement, jusqu'à ce que `check_specs.py` existe (`US-00-08`) :

- chaque `UC-*/` contient bien quatre artefacts ;
- chaque `rule.md` a un bloc `## Decision` complet, avec une polarité et une ligne `Revisit if`
  qui dit quelque chose de concret ;
- chaque `rule.feature` nomme un fichier qui existe réellement dans son `files/`.

## Vérification manuelle (STOP)

Relire les six exclusions de `RG-1.4` en se demandant, pour chacune : *« si on changeait d'avis
demain, quel test deviendrait rouge ? »* Si la réponse n'est pas évidente, le scénario affirme
une absence au lieu d'un repli, et il faut le réécrire.

## Commit

Un commit par sous-groupe :

```
docs(US-00-06): specify RG-1.1 filename date rules
docs(US-00-06): specify RG-1.2 folder date rules
docs(US-00-06): specify RG-1.3 content date rules
docs(US-00-06): specify RG-1.4 arbitration rules
```

## Ne pas faire

- Ne pas écrire une ligne de code de production. Aucune implémentation, aucun `src/`.
- Ne pas écrire les tests d'acceptance eux-mêmes : les `.feature` sont la spécification, leur
  pas-à-pas Python arrive avec `US-03-02` et suivants.
- Ne pas toucher aux groupes `RG-2` à `RG-7` : c'est `US-00-07`.
- Ne pas modifier le vocabulaire de pas Gherkin sans mettre à jour `specs/README.md` dans le
  même commit.
