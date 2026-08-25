# US-00-01 - Repository bootstrap

> **Feature** F00 - Specs corpus & pretotype - **Lot 1/22** - Statut : ✅ **(25/08/2026)**
> Fiche rétrospective : le lot est livré, tag `US-00-01`.

## Objectif

Poser le dépôt public et son contrat de projet, avant tout autre fichier.

## Ce qui a été livré

| Fichier | Rôle |
|---|---|
| `CLAUDE.md` | Le contrat de projet : architecture non négociable, sûreté des données, spécification par l'exemple, conventions, dépendances gelées |
| `README.md` | Ce qu'est YAIT et ses engagements de conception |
| `CONTRIBUTING.md` | Workflow Feature/US/Task, comment modifier une règle métier |
| `LICENSE` | MIT |
| `.gitignore` | Posé **au tout premier commit**, avant tout autre fichier |
| `.gitattributes` | Fins de ligne et binaires |

## Décisions prises

1. **`.gitignore` en premier.** Le finding #25 de l'audit `dvd-tools` : dix fichiers `.pyc`
   étaient commités faute de `.gitignore` initial. L'ordre des commits est la parade.
2. **`.gitattributes` ajouté après coup**, sur avertissement CRLF de Git. La CI tournant sur
   Ubuntu **et** Windows, sans normalisation chaque diff porterait du bruit de fins de ligne.
   Les lanceurs `.ps1` gardent CRLF pour rester exécutables depuis l'Explorateur.

## Traces

Commits `9c20952`, `e4f2f89`. Tag `US-00-01`.
