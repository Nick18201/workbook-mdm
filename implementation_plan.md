# Plan Global de Refactorisation de la Codebase (Workbook MDM)

Suite à l'analyse de l'architecture (`Agent.md`) et de l'état actuel du code (`Scripts/`), ce document structure la refactorisation complète de tous les chapitres et du pipeline de génération. 

L'objectif est de transformer une série de fichiers monolithiques (certains dépassant les 800 lignes) et un système de génération répétitif en une architecture modulaire, pérenne et standardisée.

Ce chantier colossal est découpé en **4 plans d'implémentation successifs et indépendants**, prêts à être délégués à des agents IA asynchrones. Chaque agent devra s'approprier son plan, exécuter les tâches associées, et valider que tout fonctionne avant de marquer sa phase comme terminée.

---

## 🤖 Plan d'Implémentation 1 : Orchestration et Standardisation du Pipeline (Builder Pattern)

**Objectif :** Simplifier les scripts de génération principaux (`main_generate_*.py`) en centralisant la création et la gestion du flux PDF.

### Proposed Changes

#### [NEW] `Scripts/workbook_generator/document_builder.py` (ou intégration dans `utils.py`)
- Créer une classe `DocumentBuilder` (ou un module dédié) qui prend en charge l'instanciation de `canvas.Canvas`, la définition du thème (ex: 'indigo'), le logging, et l'enchaînement fluide des pages (ex: `builder.add_page(chapX.create_cover)`).
- Gérer l'ajout automatique de nouvelles pages en cas de débordement ou pour séparer les exercices.

#### [MODIFY] `Scripts/main_generate_*.py` (Tous les fichiers)
- Refactoriser l'intégralité des fichiers de génération (`main_generate_chap0.py` à `main_generate_chap4_v2.py`, ainsi que `main_generate_livret.py` et `main_generate_valeurs.py`) pour qu'ils instancient et utilisent le `DocumentBuilder`.
- Supprimer le code boilerplate redondant (les `print("Generating...")`, la gestion locale des erreurs, l'instanciation du canvas et de son format).

#### [MODIFY] `Agent.md`
- Mettre à jour la section architecture pour y intégrer le `DocumentBuilder` comme standard exclusif de l'orchestration des documents.

### Verification Plan
- Exécuter chaque script `main_generate_*.py` individuellement.
- Vérifier que les logs s'affichent correctement et qu'aucune erreur de compilation n'est générée.
- Valider la création réussie de tous les PDFs associés.

---

## 🤖 Plan d'Implémentation 2 : Refactorisation de l'Engine Layout (UI/UX)

**Objectif :** Éradiquer les positionnements manuels obsolètes et standardiser l'utilisation de la classe `PageLayout` sur les chapitres les plus anciens.

### Proposed Changes

#### [MODIFY] `Scripts/workbook_generator/chapters/chap0.py`
#### [MODIFY] `Scripts/workbook_generator/chapters/chap1.py`
#### [MODIFY] `Scripts/workbook_generator/chapters/chap3.py`
#### [MODIFY] `Scripts/workbook_generator/chapters/livret_competences.py`
- Scanner systématiquement ces fichiers et remplacer tous les appels bas niveau obsolètes (`c.drawString`, manipulation manuelle de `y_cursor`, appels directs à `form.textfield()`) par l'utilisation de `PageLayout`, `TextConfig`, et `QuestionConfig`.
- Corriger par la même occasion les warnings de débordement du curseur sur la marge inférieure.

### Verification Plan
- Générer les PDFs des chapitres modifiés (0, 1, 3, et livret).
- Vérification visuelle rigoureuse de l'alignement, des marges, et de la bonne configuration des champs de formulaires interactifs (AcroForm).

---

## 🤖 Plan d'Implémentation 3 : Modularisation des Chapitres Massifs (Chapitre 2 & 4)

**Objectif :** Restructurer les fichiers géants (`chap2.py`, `chap4.py`, `chap4_v2.py`) qui constituent des goulots d'étranglement en termes de maintenabilité.

### Proposed Changes

#### [NEW] `Scripts/workbook_generator/chapters/chap2/` (Dossier)
#### [DELETE] `Scripts/workbook_generator/chapters/chap2.py`
- Convertir le fichier unique en un dossier Python module.
- Intégrer un `__init__.py` exportant l'API du chapitre (les fonctions de création de page).
- Séparer en sous-fichiers : `intro.py`, `concept.py`, `exercices.py`, `cloture.py`.
- Repatrier intelligemment les fonctions isolées comme celles de `psycho_edu_chap2.py`.

#### [NEW] `Scripts/workbook_generator/chapters/chap4/` (Dossier)
#### [DELETE] `Scripts/workbook_generator/chapters/chap4.py`
- Découper en logique d'affaires : `intro.py`, `moteurs.py` (valeurs, verbes), `psychologie.py` (KMSI, Biographie), `archetypes.py`, `cloture.py`.

#### [NEW] `Scripts/workbook_generator/chapters/chap4_v2/` (Dossier)
#### [DELETE] `Scripts/workbook_generator/chapters/chap4_v2.py`
- Appliquer la même stratégie de découpage modulaire que pour `chap4`.

#### [MODIFY] `Scripts/main_generate_chap2.py`, `main_generate_chap4.py`, `main_generate_chap4_v2.py`
- Actualiser les imports pour assurer la compatibilité avec la nouvelle arborescence.

### Verification Plan
- Exécuter les générateurs des chapitres 2, 4 et 4_v2.
- S'assurer que le refactoring structurel produit des PDFs rigoureusement identiques à la version pré-refactoring.

---

## 🤖 Plan d'Implémentation 4 : Standardisation Architecturale Globale

**Objectif :** Généraliser le modèle de dossiers modulaires (introduit lors de la Phase 3) à l'intégralité du projet pour une homogénéité parfaite de l'architecture.

### Proposed Changes

#### [NEW] `Scripts/workbook_generator/chapters/chap0/` (Dossier)
#### [NEW] `Scripts/workbook_generator/chapters/chap1/` (Dossier)
#### [NEW] `Scripts/workbook_generator/chapters/chap3/` (Dossier)
#### [NEW] `Scripts/workbook_generator/chapters/valeurs/` (Dossier)
#### [NEW] `Scripts/workbook_generator/chapters/livret/` (Dossier)
#### [DELETE] `chap0.py`, `chap1.py`, `chap3.py`, `valeurs.py`, `livret_competences.py`
- Transformer les fichiers restants en modules-dossiers avec un `__init__.py` dédié. Même si certains fichiers sont courts, cette uniformisation garantira qu'aucune nouvelle fonctionnalité ne transformera ces modules en monolithes à l'avenir.

#### [MODIFY] `Agent.md`
- Refondre la documentation d'architecture pour interdire le paradigme "1 fichier = 1 chapitre" au profit d'un standard obligatoire : "1 dossier modulaire = 1 chapitre".

### Verification Plan
- Validation finale en lançant une compilation en lot ou via un script global sur l'ensemble de la codebase.
- Audit du dossier `chapters/` pour garantir la disparition totale de fichiers `.py` isolés à sa racine (tout doit être structuré en dossiers/sous-modules, à l'exception éventuelle de composants transverses très spécifiques).
