# US-00-22 — Pretotyping review (point d'arrêt)

> **Feature** F00 — Specs corpus & pretotype · **Lot 22/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Traverser le prototype, décider ce qui change, et **réordonner le backlog si nécessaire** avant
d'écrire la première ligne de code de production.

C'est le seul lot dont le livrable est une décision. C'est aussi un **point d'arrêt** : le
backlog de F01 à F09 n'est pas figé avant lui, et aucune fiche de lot n'a été écrite au-delà.

## État au démarrage

Tout F00 est livré :

- Le corpus d'échantillons, reproductible, avec ses 60 règles spécifiées
- `tools/check_specs.py` en CI, qui garantit que les règles restent complètes
- Les douze maquettes reliées en prototype navigable
- Aucune ligne de code de production, aucune API

## Règles applicables

- **Décider, pas contempler.** Une revue qui ne produit aucune décision n'a pas eu lieu.
- **Écrire ce qui n'est pas fait.** Une limite assumée vaut mieux qu'une garantie implicite.
- **Une décision qui change une règle passe par `specs/`**, pas par une note de revue. Si la revue
  invalide un comportement, la règle correspondante doit être modifiée ou supprimée dans la
  foulée — sinon la spécification et l'intention divergent dès le premier jour.

## Livrables

```
Work/F00-specs-corpus-and-pretotype/review.md    le journal de la revue
Work/todo.md                                      mis à jour si le backlog change
Work/roadmap.md                                   mis à jour si l'ordre des features change
Work/F00-specs-corpus-and-pretotype/overview.md   section « Résultat » complétée
```

Et, le cas échéant, les fiches de lot des features réordonnées.

## Ce qu'il faut examiner

**Sur les écrans**

1. Le parcours principal tient-il debout ? Y a-t-il un écran manquant, ou un écran de trop ?
2. L'écran de détail d'un média justifie-t-il vraiment le choix d'une date pour quelqu'un qui
   n'a pas écrit le code ? C'est la promesse différenciante du produit.
3. L'éditeur de métadonnées est-il meilleur que `csvedit.js`, ou seulement différent ?
4. La densité est-elle tenable sur les volumes réels ? Les maquettes montrent cinquante lignes ;
   l'inventaire en affichera des milliers.

**Sur la priorisation**

5. Le walking skeleton en lecture seule reste-t-il le bon premier lot de code ? Ce qu'on a vu
   change-t-il l'ordre F01 → F02 → F03 ?
6. `F07` (journal et annulation) doit-il vraiment précéder `F04` ? Le principe est posé — rien
   n'écrit avant que l'annulation existe — mais la revue est le moment de le confirmer ou de
   l'assumer autrement.
7. Certaines fonctionnalités vues à l'écran révèlent-elles une règle manquante dans `specs/` ?
   Une règle manquante découverte ici est une bonne nouvelle : elle coûte un fichier, pas un
   refactor.

**Sur les limites**

8. Qu'est-ce qui a été maquetté et qu'on ne saura pas construire simplement ? Le dire maintenant.
9. Quelles exclusions assumées la revue remet-elle en cause ? Le cas échéant : supprimer la règle
   négative, écrire la positive — la procédure est dans `specs/README.md`.

## Étapes

1. `T-00-22-01` Traverser le parcours principal, dans les deux thèmes, sur un écran large et un
   écran de portable.
2. `T-00-22-02` Répondre par écrit aux neuf questions ci-dessus dans `review.md`.
3. `T-00-22-03` Trancher : ce qui change, ce qui reste, ce qui est reporté.
4. `T-00-22-04` Répercuter dans `todo.md` et `roadmap.md`.
5. `T-00-22-05` Répercuter dans `specs/` toute décision qui change une règle.
6. `T-00-22-06` Compléter la section « Résultat » de `overview.md`.
7. `T-00-22-07` Clôturer la feature : déplacer le dossier sous `Work/done/2026/`, ajouter la
   ligne dans `history.md`, retirer celle de `todo.md`.

## Vérification

```bash
python tools/check_specs.py && python tools/build_samples.py --check
```

Si des règles ont bougé pendant la revue, les garde-fous doivent rester verts.

## Vérification manuelle (STOP)

C'est ce lot qui est, en entier, une vérification manuelle. Le seul contrôle qui compte :
`review.md` contient-il des décisions, ou seulement des observations ?

Une observation dit « la grille est dense ». Une décision dit « on garde la densité, et on ajoute
un mode aéré en option, noté comme `US-03-12` ».

## Commit

```
docs(US-00-22): record pretotyping review outcome
```

Corps : résumer les décisions prises et les changements de backlog qui en découlent.

## Ne pas faire

- Ne pas commencer F01. Le lot se termine à la clôture de la feature.
- Ne pas laisser une décision uniquement dans `review.md` : si elle change une règle, elle va
  dans `specs/` ; si elle change le backlog, elle va dans `todo.md`.
- Ne pas conclure la revue sans décision. Si vraiment rien ne change, l'écrire explicitement et
  dire pourquoi — c'est aussi un résultat.
