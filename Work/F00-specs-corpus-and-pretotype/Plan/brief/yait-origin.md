# Brief d'origine — YAIT

> Intention brute, transcrite de la conversation du 25/08/2026. Non réécrite après coup.
> Le brief n'est pas censé être complet : les zones d'ombre ont été levées en planification.

---

## Le déclencheur

Après un audit critique de `dvd-tools` (trois CLI vibe-codées : `dvdphotos.py`, `dvdmeta.py`,
`csvedit.js`), décision de ne pas réparer mais de repartir d'une application neuve.

## L'intention

> Changement de stratégie : nouvelle app YAIT (aka YetAnotherImageTools)
>
> Je veux mettre en place une nouvelle architecture 100% python from scratch dans un nouveau
> répertoire. L'idée est d'avoir une IHM unique depuis le navigateur et de passer par une petite
> api pour réaliser les différents traitements déjà proposés par DVDTools.
>
> À l'usage, l'utilisateur va lancer une CLI dans son bash par exemple `yait.sh` :
> - lancer une page web dans le navigateur qui fera office d'IHM
> - lancer un service type webApi en tâche de fond qui servira de backend
>
> L'utilisateur sélectionne le dossier qui contient les photos sur son poste.
> Choisit la fonctionnalité à appliquer.
>
> L'IHM va proposer les fonctionnalités que les CLI existantes mais avec une meilleure ergonomie
> et les adaptations qui seront nécessaires ou souhaitables. Chaque fonctionnalité sera un appel
> de service de la webAPI avec des paramètres (similaire aux options d'un appel CLI).
>
> **Au programme (non exhaustif)**
>
> Modifications des photos
> - Extraction des propriétés des photos/vidéos existantes, avec proposition de modification
>   → équivalent de csvedit (on peut garder l'IHM)
> - Application des modifications
>
> Réorganisation en fonction des propriétés des photos
> - Renommage de fichiers selon un pattern défini (on pourra définir plusieurs patterns dans le futur)
> - Réorganisation en sous-répertoires (Organize)
> - ou mise à plat de la structure de répertoires (Flat)
>
> Je veux que le travail soit proche d'une réalisation faite par un développeur fullstack Python
> expérimenté, adepte du DDD et des pratiques du software craftsmanship.
> Je veux que toute fonctionnalité de l'API soit testée et documentée (norme OpenAPI).
> On lancera tout uniquement en local (pas de vocation à héberger les services sur le cloud,
> restons simple pour le moment).
> Étudier l'utilisation de docker plutôt qu'un lancement via une CLI.
>
> Je veux un nouveau plan détaillé, ordonné, type Project/Feature/US (en plusieurs fichiers MD)
> avec maquettes html du rendu des écrans et les tests d'acceptance écrits en se basant sur des
> exemples réels existants (le plus exhaustif possible).
> Utilise toutes les remarques/recommandations que tu as émises précédemment.
>
> L'exécution sera lancée US par US (ou par lot d'US) dans des sessions de Claude Code séparées.
> Un nouveau repo Git sera nécessaire, une branche par US, un tag par US, plusieurs commits autorisés.

## Compléments apportés en cours de planification

- Dépôt dans `C:\Repo\yait`, destiné à une **publication publique sur GitHub sous MIT** —
  d'où toute la documentation et les écrans **en anglais**.
- **Pretotyping** : les maquettes doivent arriver tôt dans le lotissement, pour pouvoir revoir la
  priorisation avant de s'engager.
- Les images d'exemple sont **générées depuis une photo personnelle unique** et embarquées au
  dépôt, pour que les tests soient exécutables quelle que soit la machine.
- Les cas identifiés mais non traités doivent l'être **explicitement comme une règle assumée, pas
  comme une règle manquante** : « si un jour on doit prendre en compte un cas qu'on a identifié
  mais initialement ignoré, il y aura forcément un test rouge et une règle existante à supprimer ».
- Adoption de la pratique de carnet de bord `Work/` d'un autre projet, chaque fiche de lot devant
  être lançable dans une session vierge sans autre information.

## Arbitrages tranchés en planification

| Question | Réponse |
|---|---|
| Docker ou lanceur natif ? | Natif seulement, Docker réétudié plus tard |
| Comment désigner le dossier photo ? | Saisie / collage du chemin |
| Pile front-end ? | Vanilla ESM zéro-build |
| Périmètre du premier lot de code ? | Walking skeleton en lecture seule |
