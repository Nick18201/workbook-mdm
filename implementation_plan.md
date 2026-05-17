# Plan de Refactorisation de la Codebase (Workbook MDM)

Suite à l'analyse de l'architecture décrite dans `Agent.md` et de l'état actuel du code (notamment `chap4.py` qui dépasse les 700 lignes et l'erreur d'import relatif levée lors de l'exécution de sous-modules), voici un plan de refactorisation pour rendre la codebase plus pérenne, lisible et modulaire.

## User Review Required

> [!IMPORTANT]
> Merci de valider si vous souhaitez appliquer l'ensemble de ces chantiers (notamment le Builder Pattern qui modifie la structure des `main.py`), ou si vous préférez commencer uniquement par la modularisation des dossiers de chapitres.

## Open Questions

> [!NOTE]
> Le module `schwartz_pvq.py` a été créé séparément. Souhaitez-vous le laisser à la racine de `chapters/` comme un module global (réutilisable), ou l'intégrer dans le sous-dossier `chap4/` ?

## Proposed Changes

### 1. Modularisation des Chapitres (Dossiers au lieu de fichiers uniques)

Le modèle "1 fichier = 1 chapitre" défini dans `Agent.md` n'est plus viable pour des chapitres denses.

- **Création de sous-dossiers** : Transformer `chap4.py` en un dossier `chapters/chap4/`.
- **Découpage logique** :
  - `chapters/chap4/__init__.py` : Facade pour exporter toutes les fonctions de génération.
  - `chapters/chap4/intro.py` : (Cover, Concept, Recap MBTI).
  - `chapters/chap4/moteurs.py` : (Valeurs, Verbes d'action).
  - `chapters/chap4/psychologie.py` : (Psycho-éduc, KMSI, Impact KMSI, Biographie financière).
  - `chapters/chap4/archetypes.py` : (Dialogue avec l'argent, Archétypes, Mindset Surplus, Synthèse).
  - `chapters/chap4/cloture.py` : (Cartographie, Exploration).
- Ce même traitement pourra être appliqué ultérieurement à `chap2.py` (qui fait aussi plus de 800 lignes).

### 2. Standardisation UI (Généralisation du `PageLayout`)

- Parcourir les modules découpés pour s'assurer que **100% des nouvelles pages** utilisent `PageLayout`, `TextConfig`, et `QuestionConfig` introduits récemment.
- Retirer les appels locaux de type `c.drawString()` ou la gestion manuelle du `y_cursor` là où le layout engine peut faire le travail. Cela réduira la duplication de code et empêchera les textes de déborder en bas de page (comme indiqué dans les warnings du terminal).

### 3. Amélioration de l'Orchestration (Builder Pattern)

Actuellement, `main_generate_chap4.py` appelle manuellement une vingtaine de fonctions, avec des `print()` répétitifs :
```python
print("Generating Cover...")
chap4.create_chap4_cover(c)
```
- **Création d'un utilitaire `DocumentBuilder`** (dans `utils.py` ou `components.py`) qui prend en charge le logging, la gestion des erreurs, et l'enchaînement des pages.
- Le `main_generate_chapX.py` deviendra plus déclaratif.

### 4. Mise à jour de `Agent.md`

#### [MODIFY] `Agent.md`
- Mettre à jour la section **Architecture Actuelle** pour refléter la possibilité d'utiliser des sous-dossiers `chapX/` pour les chapitres complexes.
- Ajouter une section sur le **Moteur de Layout** (`PageLayout`) en tant que standard obligatoire pour la création de pages.
- Préciser la cause des erreurs d'imports relatifs pour éviter que de futurs agents (ou développeurs) essaient d'exécuter `python chapters/chapX.py` directement.

## Verification Plan

### Automated Tests
- Lancer `python Scripts/main_generate_chap4.py` après la refactorisation pour s'assurer que le fichier `Workbook_Chapitre_4.pdf` est généré avec succès.
- Vérifier les logs du terminal pour s'assurer que les avertissements de débordement de marge (ex: `Form field 'kmsi_hmw' might overflow bottom margin`) sont résolus grâce à l'ajustement des `box_height` avec `PageLayout`.

### Manual Verification
- Ouvrir le PDF généré et vérifier que l'ordre des pages, le design, et le bon fonctionnement des champs de formulaire interactifs sont intacts.
