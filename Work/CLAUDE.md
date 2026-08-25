# Work — carnet de bord

Ce répertoire est le journal de travail du dépôt. Il ne contient **pas de code** : uniquement
l'intention, les décisions, les plans et l'historique. Le code vit dans `src/`, `tools/` et `specs/`.

Ce fichier décrit la façon de travailler. Il sert de **référence et de gabarit** pour toute
nouvelle tâche.

> **À ne pas confondre avec le [`CLAUDE.md` racine](../CLAUDE.md).** Celui-ci décrit *comment on
> organise le travail*. Celui de la racine décrit *les règles du produit* — architecture, sûreté
> des données, spécification par l'exemple. Une session lit les deux : la racine d'abord, la
> fiche de lot ensuite.

---

## Vocabulaire

| Terme       | Définition                                                                       |
|-------------|----------------------------------------------------------------------------------|
| **Feature** | Une intention de bout en bout, identifiée `F<nn>`. Ex. `F03 — Inventory`.          |
| **Lot**     | Une *user story*, identifiée `US-<nn>-<mm>`. Ex. `US-03-05`. Unité de livraison.   |
| **Tâche**   | Une étape dans un lot, `T-<nn>-<mm>-<pp>`. Vit dans la fiche, pas dans un fichier. |
| **Brief**   | L'intention brute, écrite avant analyse. Jamais réécrite après coup.               |
| **Plan**    | Le résultat de l'itération avec l'IA sur le brief. Découpe la feature en lots.     |

Règle centrale : **un lot = une session d'IA = au moins un commit = une pause de vérification
manuelle.** Une session neuve par lot, pour garder le contexte minimal. Chaque fiche de lot est
donc **autosuffisante** : lisible sans le plan global ni l'historique de conversation.

La numérotation est celle du produit, définie dans le [`CLAUDE.md` racine](../CLAUDE.md). On
n'en introduit pas une seconde ici.

---

## Structure

```
Work/
├── CLAUDE.md                       # ce fichier
├── roadmap.md                      # la vue programme : les dix features, leur ordre
├── todo.md                         # ce qui reste à faire — la vue de pilotage
├── history.md                      # ce qui est terminé, daté
├── F<nn>-<slug>/                   # une feature en cours
│   ├── overview.md                 # l'intention + le déroulé de la feature
│   └── Plan/
│       ├── F<nn>-plan.md           # le plan consolidé de la feature (référence)
│       ├── US-<nn>-<mm>-<titre>.md # une fiche par lot, autosuffisante
│       └── brief/                  # les entrées brutes et les versions intermédiaires
└── done/
    └── <année>/<JJ-MM>-<slug>/     # features clôturées, archivées
```

`roadmap.md` est un ajout par rapport à la pratique d'origine : le programme YAIT compte dix
features, et il faut un endroit pour leur ordre et leurs dépendances qui ne soit ni une fiche de
lot ni le plan d'une feature en particulier.

### Nommage

| Élément         | Règle                                              | Exemple                              |
|-----------------|----------------------------------------------------|--------------------------------------|
| Feature         | `F<nn>`, séquence du produit                        | `F03`                                |
| Dossier feature | `F<nn>-<slug>`                                      | `F03-inventory`                      |
| Fiche de lot    | `US-<nn>-<mm>-<titre en anglais kebab-case>.md`     | `US-03-05-folder-dates.md`           |
| Numéro de lot   | Sur 2 chiffres, à partir de `01`                    | `01`, `02`, … `22`                   |

Les slugs de dossier sont figés une fois créés : d'autres fichiers pointent dessus par lien
relatif. On ne les renomme pas pour corriger une coquille.

---

## Les trois états

`todo.md` et les fiches de lot utilisent trois marqueurs, et seulement trois :

| Marqueur | Sens        |
|----------|-------------|
| ⬜        | à faire     |
| ⌛        | en cours    |
| ✅        | terminé     |

`todo.md` est groupé par feature, une ligne par feature, les lots en sous-liste. `history.md` ne
reçoit que du ✅, avec la date au format `**(JJ/MM/AAAA)**` et un lien `[🔗](chemin)`.

---

## Cycle de vie d'une tâche

1. **Brief** — l'intention écrite à la main dans `Plan/brief/`. Format libre, pas censé être complet.
2. **Planification** — itération avec l'IA. Elle doit d'abord **relever les zones d'ombre, les
   contradictions et les manquements** du brief avant de proposer quoi que ce soit. Chaque version
   du plan est conservée dans `brief/` : le cheminement fait partie de la trace.
3. **Découpage** — le plan consolidé produit une fiche par lot, autosuffisante.
4. **Réalisation** — un lot par session, un commit par lot, pause de vérification manuelle entre chaque.
5. **Clôture** — `overview.md` complété, dossier déplacé sous `done/<année>/`, ligne ajoutée dans
   `history.md`, ligne retirée de `todo.md`.

---

## Gabarit d'une fiche de lot

Le document d'exécution, remis tel quel à une session vierge. Structure imposée :

```
# US-<nn>-<mm> — <Titre>

> **Feature** F<nn> — <Titre feature> · **Lot <n>/<total>** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le CLAUDE.md racine.

## Objectif            # la user story, 1 à 3 phrases
## État au démarrage   # ce qui existe déjà, ce qui a été livré avant
## Règles applicables  # uniquement celles qui comptent pour CE lot
## Livrables           # arborescence ou liste de fichiers
## Étapes              # T-<nn>-<mm>-<pp>, numérotées, actionnables
## Vérification        # commandes + résultat attendu
## Vérification manuelle (STOP)   # ce que le porteur contrôle, lui
## Commit              # le message exact, Conventional Commits
## Ne pas faire        # les garde-fous de périmètre
```

---

## Règles pour Claude

- **Le périmètre du lot est la limite.** On ne déborde pas sur le lot suivant, même si c'est
  « juste deux lignes ». On s'arrête après le commit et la section « Vérification manuelle ».
- **Relever avant de proposer.** Sur un brief, on veut d'abord les zones d'ombre, les
  contradictions et ce qui manque — pas une solution qui aplanit les ambiguïtés en silence.
- **Vérifier les faits externes.** Versions de paquets, compatibilités, formats de fichiers : on
  interroge la source, on n'affirme pas de mémoire.
- **Dire ce qui n'est pas fait.** Une limite assumée et écrite vaut mieux qu'une garantie
  implicite. Si une vérification n'est pas automatisable, on l'écrit noir sur blanc au lieu de
  laisser croire qu'elle est couverte.
- **Tenir `todo.md` à jour** à chaque fin de lot.
- **Français** pour ce répertoire `Work/`. **Anglais** pour tout le reste : code, `docs/`,
  `specs/`, identifiants, titres de fichiers de lot, sujets **et corps** de commit — le dépôt est
  public.
- **Un squelette sans specs prévoit un test honnête, pas une suite vide.** Pour un lot qui livre
  un socle sans comportement, écrire un test sur ce qui existe réellement plutôt que d'attendre
  une suite vide verte.
- **Le pseudo-code illustratif dans un `.md` doit être syntaxiquement valide, ou sans langage.**
  Un bloc étiqueté `yaml` ou `python` qui ne parse pas se fait « corriger » silencieusement par
  un formateur, qui en change le sens. Fence sans langage pour du pseudo-code.

---

## Commits

Conventional Commits, sujet et corps en anglais — le dépôt est destiné à une publication publique.

```
<type>(<scope>): <sujet à l'impératif>

<corps optionnel qui explique le pourquoi>
```

| Type    | Usage                                     |
|---------|-------------------------------------------|
| `feat`  | nouvelle capacité                         |
| `fix`   | correction                                |
| `docs`  | documentation, dont ce répertoire `Work/` |
| `chore` | outillage, configuration                  |

Scope = l'identifiant du lot : `feat(US-00-04): …`. Pour le carnet de bord : `docs(work): …`.

Un tag annoté par lot livré, posé sur `main` : `US-00-04`.
