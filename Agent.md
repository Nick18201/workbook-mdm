# Contexte et Architecture du Projet "Workbook MDM" (Livret de Compétences)

Ce document sert de référence technique pour tout agent IA (ou développeur) intervenant sur le dépôt.

## 🏗️ Architecture Actuelle
Le projet génère des livrets pédagogiques au format PDF ("workbooks") dynamiquement via Python et la librairie `reportlab`. L'architecture est modulaire, isolant les contenus de la structure visuelle.

- **`Scripts/main_generate_chapX.py`** : Les scripts d'entrée orchestrant la création d'un PDF. Ils instancient le document et appellent l'ordre de création de chaque page dans le chapitre.
- **`Scripts/workbook_generator/`** : Le cœur graphique et applicatif :
  - `components.py` : Fonctions générant des éléments réutilisables (titres, couvertures, bas de page).
  - `config.py` : Constantes globales, charte graphique (couleurs, polices, marges).
  - `templates.py` & `forms.py` : Gabarits visuels plus complexes et réutilisables.
  - `utils.py` : Utilitaires (notamment `register_fonts` pour charger les polices).
  - `chapters/` (ex: `chap1.py`) : Sous-modules dédiés contenant la logique de positionnement pour chaque page / exercice d'un chapitre spécifique.
- **`assets/`** : Contient les `fonts/` (polices TrueType/OpenType) et `illustrations/` (images, schémas).
- **Fichiers racines** : Entrées PDF statiques (ex: `Workbook_Chapitre_1.pdf`) ou temporaires.

## 📝 Conventions de Nommage
- **Fichiers & Dossiers** : Principalement en `snake_case` (ex: `main_generate_chap1.py`, `workbook_generator`).
- **Génération de Pages** : Le format standard d'une fonction de rendu de page est `create_<nom_de_la_page>_page(c)` (ex: `create_concept_page(c)`).
- **Variables Canvas** : L'instance `reportlab.pdfgen.canvas.Canvas` responsable du dessin de la page doit toujours être nommée `c` et passée pour premier argument.
- **Positionnement Y** : Lors de calculs de layouts verticaux, la variable contenant la hauteur courante est invariablement nommée `y_pos`.
- **Fichiers en Sortie** : `Workbook_Chapitre_<N>.pdf`.

## 🛠️ Instructions de Build et d'Exécution
1. **Environnement virtuel** : Travaillez dans le `.venv` existant (`.venv\Scripts\activate` sous Windows).
2. **Dépendances** : Les scripts dépendent de packages tels que `reportlab`. Si un import venait à manquer, effectuez un `pip install`.
3. **Arborescence d'Exécution** : Lancez toujours les scripts depuis la **racine du dépôt** (pour que le ciblage des `assets/` et la sauvegarde des Pdfs se fassent au bon endroit).
4. **Tester / Compiler un chapitre** :
   ```bash
   python Scripts/main_generate_chap1.py
   ```
   *Astuce : Le lancement direct d'un script dans `Scripts/` ajoutera automatiquement le sous-dossier au `sys.path`, permettant la résolution des imports `from workbook_generator.xxx ...`.*

> **Directives IA :**
> - Lors de la création d'une nouvelle page : créez la fonction dans le `chapX.py` correspondant, mais importez/réutilisez au maximum les briques de `components.py`.
> - N'ouvrez pas directement le canvas aux imports bas niveaux si ce n'est pas nécessaire, passez par les helpers.
> - Aucune action destructrice ou écrasement de `assets/` sans validation utilisateur.
