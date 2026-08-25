# US-00-02 - Seed photograph

> **Feature** F00 - Specs corpus & pretotype - **Lot 2/22** - Statut : ✅ **(25/08/2026)**
> Fiche rétrospective : le lot est livré, tag `US-00-02`.

## Objectif

Intégrer la photo seed dont dérivera tout le corpus, dépouillée de ses métadonnées.

## Ce qui a été livré

- `specs/_seed/river.jpg` - 900×403, aucune métadonnée
- `specs/_seed/README.md` - provenance, inventaire de ce qui a été retiré, comment vérifier
- `specs/LICENSE` - CC0
- `tools/strip_exif.py` - stdlib pure, avec `--check` pour la CI

## Ce que contenait réellement l'image

| Segment | Taille | Contenu |
|---|---|---|
| APP1 Exif | 144 o | `Orientation`, `DateTimeOriginal` et `DateTimeDigitized` (2022-07-19 12:01:05), sous-secondes |
| APP1 XMP | 434 o | `exif:DateTimeOriginal`, un uuid Adobe |

**Ni GPS, ni marque, ni modèle, ni numéro de série** - l'image avait déjà été redimensionnée
avant intégration. La mise en garde initiale sur les données personnelles était trop large.

La raison de dépouiller reste entière, et c'était la plus solide des deux : un
`DateTimeOriginal` résiduel se propagerait dans **chaque** échantillon dérivé et ferait dépendre
les tests d'une donnée qui n'apparaît nulle part dans les `samples.yaml`.

## Vérification effectuée

Indépendamment de l'assertion interne de l'outil : sha256 du scan compressé identique avant et
après (`ca11682d...`, 88 309 octets), dimensions inchangées, EOI intact.

## Décisions prises

1. **`strip_exif.py` en stdlib pure.** Il n'a pas besoin de codec : il ne fait que reconstruire
   des segments d'en-tête. C'est la seule vérification qu'un relecteur externe voudra faire sans
   installer quoi que ce soit.
2. **Refus d'écrire si le scan change.** L'outil compare avant d'écrire et échoue plutôt que de
   produire une image ré-encodée. C'est la garantie `UC-44` appliquée à l'outil lui-même.
3. **Écriture via fichier temporaire + `os.replace`**, comme l'application le devra.
4. **CC0 pour le corpus.** MIT est une licence logicielle et ne convient pas à une photographie.
   Le texte intégral du *legal code* n'est pas transcrit : la dédicace identifie CC0 1.0 et
   renvoie au texte canonique, pour ne pas restituer un document juridique de mémoire.

## Traces

Commit `c9c410e`. Tag `US-00-02`.
