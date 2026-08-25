# US-00-04 — Sample generator, image derivatives

> **Feature** F00 — Specs corpus & pretotype · **Lot 4/22** · Statut : ⬜
> Fiche autosuffisante : ne pas lire le plan global.
> Lire d'abord le [`CLAUDE.md` racine](../../../CLAUDE.md).

## Objectif

Écrire le générateur qui fabrique, à partir de la photo seed, les images d'exemple décrites par
chaque règle : dimensions, qualité et champs EXIF injectés. Sans lui, aucune règle ne peut avoir
son répertoire `files/`, donc aucun test d'acceptance ne peut exister.

Ce lot ne traite **que** les dérivés d'image. Les artefacts forgés (AVI, MP4, zip, tronqués)
sont le lot suivant.

## État au démarrage

Livré par les lots précédents :

- `specs/_seed/river.jpg` — 900×403, **aucune métadonnée** (vérifiable par
  `python tools/strip_exif.py --check specs/_seed/river.jpg`)
- `specs/_templates/samples.yaml` — le format des recettes, avec ses commentaires
- `specs/README.md` — section « Sample recipes »
- `specs/RG-1-date-resolution/RG-1.2-folder-dates/UC-14-deepest-folder-wins/samples.yaml` —
  **la seule recette réelle existante**, à utiliser comme cible de mise au point
- `tools/strip_exif.py` — stdlib pure, contient déjà le découpage en segments JPEG

Rien d'autre : pas de `pyproject.toml`, pas de venv, pas de `src/`. Ils arrivent en F01.

## Règles applicables

- **Pillow est autorisé ici**, et c'est une décision arrêtée : Python n'a aucun codec JPEG en
  stdlib, donc sans Pillow pas de résolutions différentes, donc `UC-27` (départage des collisions
  par pixels puis taille) serait inspécifiable. Pillow est déjà une dépendance runtime gelée du
  projet : rien de neuf n'entre.
- **`tools/strip_exif.py` reste en stdlib pure.** Ne pas le réécrire avec Pillow : c'est la seule
  vérification qu'un relecteur externe fera sans environnement.
- **Le générateur est déterministe.** Deux exécutions produisent le même manifeste.
- **`--check` ne compare pas les octets** mais le manifeste (chemins, dimensions, EXIF) :
  l'encodeur JPEG de Pillow n'est pas stable d'une version à l'autre.
- **Jamais de fichier placé à la main dans `files/`.**

## Décision à acter en ouverture de lot

**Format des recettes : `samples.toml` plutôt que `samples.yaml` ?**

Python n'a pas de parseur YAML en stdlib, mais `tomllib` y est depuis la 3.11. Retenir TOML évite
une dépendance de plus pour un gain de lisibilité discutable sur des structures aussi plates.

Si la décision est retenue, elle impose un renommage dans **trois** endroits déjà commités :
`specs/README.md`, `specs/_templates/samples.yaml` et la recette de `UC-14`. Le faire en première
tâche du lot, dans un commit séparé.

Si elle est écartée, ajouter PyYAML aux dépendances de développement et poursuivre sans renommer.

## Livrables

```
tools/build_samples.py          le générateur
requirements-dev.txt            Pillow, et PyYAML seulement si TOML est écarté
specs/.../UC-14.../files/       le premier répertoire d'échantillons réellement généré
specs/.manifest.json            le manifeste consolidé
```

`requirements-dev.txt` est provisoire : `US-01-01` le remplacera par `pyproject.toml`. L'écrire
quand même, pour que le lot soit reproductible seul.

## Étapes

1. `T-00-04-01` Trancher le format de recette (voir ci-dessus) et, si TOML, renommer dans les
   trois fichiers concernés. Commit séparé.
2. `T-00-04-02` `requirements-dev.txt` avec Pillow. Créer le venv, installer.
3. `T-00-04-03` Lecture des recettes : parcourir `specs/**/UC-*/samples.*`, valider le schéma
   (`version`, `files[]`, champs autorisés), **échouer explicitement** sur un champ inconnu — une
   faute de frappe dans une recette ne doit pas produire silencieusement un échantillon absent.
4. `T-00-04-04` Dérivation d'image : ouvrir le seed, redimensionner à `width` (hauteur
   proportionnelle), encoder en JPEG à `quality`. Valeurs par défaut : largeur 320, qualité 70 —
   les pixels ne comptent presque jamais, le budget de taille si.
5. `T-00-04-05` Injection EXIF : construire le bloc à partir du mapping `exif` de la recette.
   Noms de tags lisibles (`DateTimeOriginal`, `DateTimeDigitized`, `Orientation`), jamais de codes
   numériques dans les recettes. `exif: {}` ou absent produit une image **sans aucun segment de
   métadonnée**.
6. `T-00-04-06` Création de l'arborescence : les `path` contiennent des répertoires, souvent avec
   accents, espaces et esperluettes. C'est le sujet de plusieurs règles ; ne pas les assainir.
7. `T-00-04-07` Écriture du manifeste consolidé `specs/.manifest.json` : pour chaque fichier, son
   chemin, ses dimensions, ses champs EXIF, sa taille. C'est lui que `--check` compare.
8. `T-00-04-08` Mode `--check` : régénérer dans un répertoire temporaire, comparer le manifeste,
   sortir 1 en cas d'écart en nommant les fichiers fautifs.
9. `T-00-04-09` Générer `files/` pour `UC-14` et vérifier que le répertoire est complet.

## Vérification

```bash
python tools/build_samples.py && python tools/build_samples.py --check && python tools/strip_exif.py --check specs/_seed/river.jpg
```

Attendu : la première commande crée
`specs/RG-1-date-resolution/RG-1.2-folder-dates/UC-14-deepest-folder-wins/files/2002-07-20 Wedding at Arras/18-07-2002/026-the-couple-and-the-mother.jpg`,
la deuxième sort 0, la troisième confirme que le seed n'a toujours aucune métadonnée.

**Contrôle supplémentaire à faire explicitement :** l'échantillon de `UC-14` a `exif: {}`, donc il
doit **lui aussi** passer `strip_exif.py --check`. Un générateur qui réinjecterait par défaut
l'EXIF du seed casserait la règle sans que rien ne l'annonce.

## Vérification manuelle (STOP)

- Ouvrir l'échantillon généré dans une visionneuse : l'image doit être lisible et reconnaissable.
- Vérifier sa taille sur disque : quelques kilo-octets, pas quelques dizaines.
- Vérifier que les accents du chemin s'affichent correctement dans l'Explorateur Windows.

## Commit

```
feat(US-00-04): generate image samples from the seed photograph
```

Corps : expliquer le choix de Pillow (aucun codec JPEG en stdlib, donc pas de résolutions
variables, donc `UC-27` inspécifiable), et que `--check` compare le manifeste et non les octets.

## Ne pas faire

- Ne pas forger d'AVI, de MP4, de zip ni de fichier tronqué : c'est `US-00-05`.
- Ne pas écrire de règle métier : c'est `US-00-06` / `US-00-07`.
- Ne pas créer `pyproject.toml`, `src/`, ni de configuration ruff/mypy/pytest : c'est `US-01-01`.
- Ne pas réécrire `tools/strip_exif.py` avec Pillow.
