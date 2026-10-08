# Contexte et Architecture du Projet "Workbook MDM" (Livret de Compétences)

Ce document sert de référence technique pour tout agent IA (ou développeur) intervenant sur le dépôt.

## 🏗️ Architecture Actuelle
Le projet génère des livrets pédagogiques au format PDF ("workbooks", ou carnets de bord) dynamiquement via Python et la librairie `reportlab`. L'architecture est modulaire, isolant les contenus de la structure visuelle.

- **`workbooks/`** : Le contenu des carnets (`chap0.json` à `chap6.json`), du livret et du business plan, un fichier JSON par document au format `WorkbookSpec` (`spec.py`). C'est la **source unique** des PDF et de l'app web : l'app propose ces mêmes fichiers à la personnalisation, et un livret créé dans l'app s'exporte en JSON pour rejoindre ce dossier.
- **`Scripts/main_generate_*.py`** : Les scripts d'entrée. Chacun compile un fichier de `workbooks/` avec `workbook_generator.compiler` ; seul le programme (`main_generate_programme.py`) assemble encore ses pages en Python avec `DocumentBuilder`.
- **`Scripts/workbook_generator/`** : Le cœur graphique et applicatif :
  - `document_builder.py` : Contient la classe `DocumentBuilder` qui est le standard exclusif pour l'orchestration des documents (instanciation du canvas, gestion des accès fichiers, enregistrement des polices, pastel dominant et folio du carnet, fond ivoire des pages).
  - `config.py` : `PDFStyle`, les tokens de la direction artistique (couleurs, polices, échelle typographique, marges).
  - `primitives.py` : Les briques de la DA (titre ponctué avec mot d'accent, sourcil, étiquette pilule, cartes, post-it, tampon, icônes, frise, folio…).
  - `components.py` : Les gabarits pleine page (couverture, ouverture de carnet, météo, quadrants, deux colonnes, enquête, feuille de route, fin de carnet, 4e de couverture) et les blocs partagés (question, zone de réponse, échelle).
  - `templates.py` : `PageLayout`, la mise en page en flux vertical et ses blocs empilables (questions, encarts, fiches de champs, listes, grilles…), avec pages « (suite) » automatiques.
  - `forms.py` : Champs AcroForm (texte, cases, boutons radio), aux noms uniques.
  - `drawn_blocks.py` : Les blocs dessinés comme des illustrations (ligne de vie, arbre de vie).
  - `spec.py` : Le format déclaratif d'un document (`WorkbookSpec`, `PageSpec`, `BlockSpec`) et la lecture des fichiers de `workbooks/`.
  - `compiler.py` : Le moteur unique qui transforme une spécification en PDF, pour la ligne de commande comme pour l'app web.
  - `utils.py` : Utilitaires (typographie française automatique, `create_cli` pour parser les arguments CLI, caches).
  - **`chapters/programme/`** : La brochure du programme publiée sur le site, seul document resté en Python (avec ses blocs propres dans `common.py`). Règle : un dossier par document, scindé en sous-fichiers, jamais un fichier unique.
- **`assets/`** : Contient les `fonts/` (DM Sans, Manrope, PT Mono, Instrument Serif, Material Symbols Outlined, avec leurs licences) et `illustrations/` (`couverture.svg`, l'illustration des couvertures, et les logos CPF, France Travail, Qualiopi).
- **`DA-workbook.md` et `design-system/`** : La direction artistique « Éditorial & Affirmé » (couleurs, typographie, éléments signature, ton et vocabulaire). Toute page doit s'y conformer.
- **Fichiers racines** : Entrées PDF statiques (ex: `Workbook_Chapitre_1.pdf`) ou temporaires, ignorées par git.

## 📝 Conventions de Nommage
- **Fichiers & Dossiers** : Principalement en `snake_case` (ex: `main_generate_chap1.py`, `workbook_generator`).
- **Génération de Pages** : Le format standard d'une fonction de rendu de page est `create_<nom_de_la_page>_page(c)` (ex: `create_concept_page(c)`).
- **Variables Canvas** : L'instance `reportlab.pdfgen.canvas.Canvas` responsable du dessin de la page doit toujours être nommée `c` et passée pour premier argument.
- **Positionnement Y** : Lors de calculs de layouts verticaux, la variable contenant la hauteur courante est invariablement nommée `y_pos`.
- **Fichiers en Sortie** : `Workbook_Chapitre_<N>.pdf`.

## 🎨 Direction artistique et ton
- **Une seule palette** : fond ivoire, cartes pastel, zones à remplir blanches bordées en `line-strong`, titres à l'encre dont le dernier mot (ou les `*mots marqués*`) est en corail, repères en PT Mono. Jamais de couleur codée en dur : toujours `PDFStyle`.
- **Chaque carnet** : couverture avec sa promesse sur un post-it, ouverture (objectif et liste « Exercice N · … »), pages d'exercice, puis la fin de carnet (post-it LIVRABLE et tampon « Validé en séance ») avant la 4e de couverture.
- **Ton (section 7 de la DA)** : vouvoiement, phrases courtes et concrètes, titres ponctués en casse de phrase. Jamais « coach » (dire « consultant en transformation » ou « la personne qui vous accompagne »), pas de registre de développement personnel, jamais « présentiel », aucun chiffre sans source.
- **Typographie française** : automatique au rendu (espaces insécables, guillemets « », œ), via `utils.french_typography`.

## 🛠️ Instructions de Build et d'Exécution
1. **Environnement virtuel** : Travaillez dans le `.venv` existant (`.venv\Scripts\activate` sous Windows), installé depuis `requirements-dev.txt`.
2. **Dépendances** : Les versions sont figées dans `requirements.txt` / `requirements-dev.txt` (voir `CLAUDE.md` pour les régénérer).
3. **Arborescence d'Exécution** : Lancez toujours les scripts depuis la **racine du dépôt** (pour que le ciblage des `assets/` et la sauvegarde des Pdfs se fassent au bon endroit).
4. **Tester / Compiler un chapitre** :
   ```bash
   python Scripts/main_generate_chap1.py
   ```
   *Astuce : Le lancement direct d'un script dans `Scripts/` ajoutera automatiquement le sous-dossier au `sys.path`, permettant la résolution des imports `from workbook_generator.xxx ...`.*
5. **Vérifier** : `python -m pytest tests` (dont `tests/test_cli_documents.py`, qui construit les carnets et vérifie que rien ne sort de la page), et la planche `python Scripts/test_all_templates.py`.

> **Directives IA :**
> - Lors de la création d'une nouvelle page d'un carnet : ajoutez-la au fichier JSON du document dans `workbooks/` (un gabarit, ou une page `composite` faite de blocs). Un composant inédit se code dans `templates.py` ou `components.py`, puis s'ajoute à `spec.py` et à `compiler.py`.
> - N'ouvrez pas directement le canvas aux imports bas niveaux si ce n'est pas nécessaire, passez par les helpers.
> - Aucune action destructrice ou écrasement de `assets/` sans validation utilisateur.
