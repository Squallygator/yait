# [F00] Specs corpus & pretotype

Fabriquer le corpus d'échantillons et les maquettes d'écran **avant toute ligne de code de
production**, pour que les tests soient exécutables partout et que l'ergonomie soit jugée sur
pièces avant qu'on s'engage.

## Contexte

YAIT réécrit `dvd-tools`, trois CLI *vibe-codées* dont l'audit a produit 36 findings — 5 pouvant
détruire des photos irremplaçables, 3 rendant le mode simulation mensonger. Le défaut de fond
n'était aucun de ces bugs pris isolément : c'était **l'absence de tests**, elle-même rendue
impossible par un domaine non isolable et par des fixtures qui n'existaient que sur une machine.

F00 s'attaque à cette racine avant tout le reste :

- **Un corpus reproductible.** Toutes les images dérivent d'une seule photo seed embarquée au
  dépôt ; les vidéos, archives et fichiers abîmés sont forgés octet par octet. N'importe qui peut
  lancer les tests sans l'archive privée, qui contient des noms de personnes et des événements
  familiaux et ne sera jamais commitée.
- **Des règles avant du code.** Chaque comportement est une règle sous `specs/`, avec son énoncé,
  son exemple et son test. Y compris les comportements qu'on décide de **ne pas** implémenter :
  ce sont des exclusions assumées, avec un test vert affirmant le repli.
- **Des maquettes avant l'API.** Pretotyping : on regarde les écrans, on peut rebattre la
  priorisation, et seulement ensuite on construit.

## Planification

À partir de l'intention décrite dans [`brief/yait-origin.md`](Plan/brief/yait-origin.md), itération
avec Claude jusqu'au plan approuvé → [`brief/plan-v3-approved.md`](Plan/brief/plan-v3-approved.md),
puis découpage en 22 lots → [`F00-plan.md`](Plan/F00-plan.md).

Trois itérations, chacune déclenchée par une objection :

1. **v1** — durcissement de `dvd-tools` en place. Abandonné : l'utilisateur a préféré repartir
   d'une application neuve.
2. **v2** — architecture YAIT complète, corpus décrit par un `manifest.yaml` unique générant les
   scénarios Gherkin. **Objection retenue :** le manifeste serait devenu un mastodonte, et surtout
   il aurait fait d'un fichier technique de fixtures la source de vérité fonctionnelle.
3. **v3** — la règle métier devient la source. Un répertoire autonome par règle, quatre artefacts,
   rien de généré depuis rien. **Seconde objection retenue :** un cas identifié mais non traité ne
   doit pas apparaître comme un manque mais comme une **règle négative assumée**, testée, dont le
   revirement futur produira nécessairement un test rouge et une règle à supprimer.

## Décisions

1. **Numérotation du produit conservée dans `Work/`** — `F<nn>` / `US-<nn>-<mm>` / `T-<nn>-<mm>-<pp>`.
   La pratique du carnet de bord est importée d'un autre projet, sa numérotation ne l'est pas :
   une seule séquence d'identifiants, c'était une exigence explicite.
2. **Pillow devient prérequis de développement** pour le générateur d'échantillons.
   Python n'a aucun codec JPEG en stdlib : sans Pillow, impossible de produire des résolutions
   différentes, donc impossible de spécifier `UC-27` (départage des collisions par pixels puis
   taille). Pillow est déjà une dépendance runtime gelée, donc rien de neuf n'entre au projet, et
   le générateur fabrique les fixtures dont dépendent *tous* les tests : y minimiser le code
   maison vaut mieux que de pouvoir l'exécuter sans rien installer.
   **Réserve :** `tools/strip_exif.py` reste en stdlib pure — c'est la seule vérification qu'un
   relecteur externe voudra faire sans environnement.
3. **Le corpus est commité**, la régénération ne l'est pas. « Lancer les tests sur une machine
   nue » est la propriété qui compte ; « reconstruire le corpus sur une machine nue » ne l'est pas,
   puisque seul un contributeur modifiant une règle a besoin de régénérer — et il a déjà le venv.
4. **Le seed est intégralement dépouillé de ses métadonnées.** Un `DateTimeOriginal` résiduel se
   propagerait dans chaque échantillon dérivé et ferait dépendre les tests d'une donnée invisible
   dans les `samples.yaml`.
5. **`specs/` sous CC0**, le code sous MIT. MIT est une licence logicielle et ne convient pas à
   une photographie.
6. **`US-00-22` est un point d'arrêt.** Les fiches de lot de F01 à F09 ne sont pas écrites : la
   revue de pretotyping peut réordonner le backlog, et écrire maintenant des fiches qu'elle peut
   invalider serait du travail jeté.

## Résultat

En cours. Voir [`../todo.md`](../todo.md) pour l'avancement et [`../history.md`](../history.md)
pour ce qui est livré.
