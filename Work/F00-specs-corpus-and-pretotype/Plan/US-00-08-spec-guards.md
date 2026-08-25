# US-00-08 — Spec guards in CI

> **Feature** F00 — Specs corpus & pretotype · **Lot 8/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md) puis [`specs/README.md`](../../../specs/README.md).

## Objectif

Écrire `tools/check_specs.py`, le garde-fou qui empêche le corpus de spécifications de pourrir, et
le brancher en intégration continue avec la vérification du corpus et le budget de taille.

Sans lui, rien n'oblige une règle à rester complète, ni un échantillon à rester référencé.

## État au démarrage

- Les 60 règles sont écrites (`US-00-06`, `US-00-07`), chacune avec ses quatre artefacts
- `tools/build_samples.py` avec son mode `--check`
- `tools/strip_exif.py` avec son mode `--check`
- Aucune CI n'existe encore : ce lot crée le premier workflow

## Règles applicables

- **Le contrôle échoue, il ne prévient pas.** Un avertissement dans un journal ne protège rien.
- **Chaque échec nomme le fichier fautif et la règle violée**, sans quoi le contributeur perd son
  temps à chercher.
- **Aucune dépendance nouvelle.** Analyse de texte et parcours de répertoires, en stdlib.

## Livrables

```
tools/check_specs.py                le vérificateur
.github/workflows/ci.yml            le workflow, Ubuntu et Windows
docs/00-project/10-decision-log.md  l'index dérivé, produit par check_specs.py
```

## Les invariants à vérifier

| # | Invariant | Motif |
|---|---|---|
| 1 | Tout `UC-*/` contient `rule.md`, `rule.feature`, `samples.*` et `files/` | La règle des quatre artefacts |
| 2 | Tout `rule.md` a un bloc `## Decision` complet | Sans rationale ni condition de réexamen, la décision n'en est pas une |
| 3 | La polarité vaut `Enforced` ou `Assumed exclusion`, **rien d'autre** | Pas de statut « à faire » : la commande refuse la valeur |
| 4 | Tout `rule.feature` a au moins un scénario | Une spécification sans exemple n'est pas exécutable |
| 5 | Tout fichier nommé dans un `.feature` existe dans le `files/` de sa règle | Le lien entre scénario et échantillon est le nom de fichier |
| 6 | Tout fichier de `files/` est nommé par au moins un `.feature` | Pas d'échantillon orphelin |
| 7 | Tout `UC` est référencé par au moins une fiche de lot ou un document `docs/` | Une règle que personne ne construit est morte |
| 8 | Le seed ne porte aucune métadonnée | Délégué à `strip_exif.py --check` |
| 9 | La taille totale de `specs/` reste sous le budget | À fixer dans ce lot ; proposer 2 Mo et le justifier |

L'invariant 7 mérite discussion : à ce stade, les fiches de lot de F01 à F09 n'existent pas
encore, donc **beaucoup d'UC ne seront référencés nulle part**. Deux options, à trancher en
ouverture de lot : n'appliquer l'invariant 7 qu'en avertissement pour l'instant, ou accepter une
liste d'exemptions décroissante. Choisir, et **écrire le choix** dans `check_specs.py` — pas le
contourner en silence.

## Étapes

1. `T-00-08-01` Parcours de `specs/`, en ignorant `_seed/` et `_templates/`.
2. `T-00-08-02` Invariants 1 à 4 : structure et bloc `Decision`.
3. `T-00-08-03` Invariants 5 et 6 : extraire les noms de fichiers cités dans les `.feature`
   (les chaînes entre guillemets des étapes `When … is inspected`), comparer aux `files/`.
4. `T-00-08-04` Invariant 7, selon l'option retenue.
5. `T-00-08-05` Invariant 9 : budget de taille.
6. `T-00-08-06` Génération de `docs/00-project/10-decision-log.md` : toutes les règles, leur
   polarité, leur date de décision et leur condition de réexamen, sur une page. **Index dérivé** :
   ajouter un en-tête disant qu'il est généré et que la vérité reste dans les `rule.md`.
7. `T-00-08-07` Workflow CI : Ubuntu **et** Windows. Installer les dépendances de développement,
   lancer `build_samples.py --check`, `strip_exif.py --check`, `check_specs.py`.
8. `T-00-08-08` Vérifier que la CI échoue réellement : casser volontairement une règle
   (supprimer un `rule.feature`, mettre une polarité invalide), constater le rouge, rétablir.

## Vérification

```bash
python tools/check_specs.py && python tools/build_samples.py --check && python tools/strip_exif.py --check specs/_seed/river.jpg
```

Attendu : sortie 0, et `docs/00-project/10-decision-log.md` régénéré avec les 60 règles, dont 15
exclusions.

L'étape 8 est la vraie vérification : **un garde-fou qu'on n'a jamais vu échouer n'est pas un
garde-fou.** Le faire, et le noter dans le corps du commit.

## Vérification manuelle (STOP)

- Lire `10-decision-log.md` en entier : c'est la première vue d'ensemble des 60 règles. Si une
  ligne `Revisit if` est vide ou creuse, la règle correspondante est à reprendre.
- Compter les exclusions : il doit y en avoir 15.
- Vérifier que la CI passe sur les deux systèmes, en particulier Windows où les chemins accentués
  du corpus sont un vrai test.

## Commit

```
chore(US-00-08): enforce specification invariants in CI
```

Corps : lister les invariants vérifiés, dire lequel est en avertissement et pourquoi, et
mentionner que l'échec du garde-fou a été constaté volontairement.

## Ne pas faire

- Ne pas écrire de code de production ni de test d'acceptance.
- Ne pas ajouter d'invariant qui ne serait pas vérifiable de façon déterministe — un contrôle
  intermittent en CI est pire que pas de contrôle.
- Ne pas faire de `10-decision-log.md` une source éditable à la main.
