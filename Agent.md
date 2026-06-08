# Contexte et Architecture du Projet "Workbook MDM" (Livret de Compétences)

Ce document sert de référence technique pour tout agent IA (ou développeur) intervenant sur le dépôt.

## 🏗️ Architecture Actuelle
Le projet génère des livrets pédagogiques au format PDF ("workbooks") dynamiquement via Python et la librairie `reportlab`. L'architecture est modulaire, isolant les contenus de la structure visuelle.

- **`Scripts/main_generate_*.py`** : Les scripts d'entrée orchestrant la création d'un PDF. Ils parsènt les arguments en ligne de commande et orchestrent l'ordre de création de chaque page dans le chapitre en utilisant exclusivement `DocumentBuilder`.
- **`Scripts/workbook_generator/`** : Le cœur graphique et applicatif :
  - `document_builder.py` : Contient la classe `DocumentBuilder` qui est le standard exclusif pour l'orchestration des documents (instanciation du canvas, gestion des accès fichiers, application du thème et enregistrement des polices).
  - `components.py` : Fonctions générant des éléments réutilisables (titres, couvertures, bas de page).
  - `config.py` : Constantes globales, charte graphique (couleurs, polices, marges).
  - `templates.py` & `forms.py` : Gabarits visuels plus complexes et réutilisables.
  - `utils.py` : Utilitaires (notamment `create_cli` pour parser les arguments CLI).
  - **`chapters/`** : L'arborescence des chapitres. **Règle stricte et absolue : Le paradigme "1 fichier = 1 chapitre" est formellement interdit. La norme architecturale exclusive est : 1 dossier modulaire = 1 chapitre.** Tout nouveau développement devra respecter cette règle de découplage (avec un `__init__.py` jouant le rôle de routeur léger qui exporte l'API publique).
    - Exemples : `chap0/`, `chap1/`, `chap2/`, `chap3/`, `chap4/`, `livret/`, `valeurs/`.
    - La logique de positionnement et de génération pour chaque page ou groupe d'exercices doit être scindée en sous-fichiers (ex: `intro.py`, `exercices.py`, `main.py`).
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
> - Lors de la création d'une nouvelle page : créez la fonction dans le module de chapitre correspondant en respectant l'arborescence, mais importez/réutilisez au maximum les briques de `components.py` et `templates.py`.
> - N'ouvrez pas directement le canvas aux imports bas niveaux si ce n'est pas nécessaire, passez par les helpers.
> - Aucune action destructrice ou écrasement de `assets/` sans validation utilisateur.
