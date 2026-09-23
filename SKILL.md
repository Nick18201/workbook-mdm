---
name: workbook-generator
description: |
  Engine autonome de conception, génération et modification de livrets pédagogiques (workbooks) au format PDF avec ReportLab.
  Transforme des notes de séance brutes en livrets élégants, interactifs (AcroForm) et typographiquement parfaits en "One-Shot" sans chevauchement.

  4 modes d'action :
  1. CONCEPTION : Ingestion des notes brutes → structuration pédagogique, visual mapping vers les 8 gabarits standards, calibrage des longueurs de texte → génération de Wordbook/Conception_Workbook_Chapitre_X.md.
  2. COMPILATION (BUILD) : Lecture de la fiche de conception validée → création du module chapX/ modulaire → script racine main_generate_chapX.py → compilation et validation sans warning.
  3. MODIFICATION : Retouche ciblée d'un chapitre existant (texte, question, ajout/suppression de page, changement de thème indigo/earth) avec recalcul automatique des hauteurs.
  4. ENRICHISSEMENT DESIGN SYSTEM : Création de nouveaux gabarits dans components.py avec test unitaire dans test_all_templates.py.

  TOUJOURS utiliser ce skill quand l'utilisateur dit :
  • "crée le chapitre [X]", "conception du chapitre", "voici mes notes pour le chapitre", "structure ces notes de séance", "prépare le livret pour la séance [N]".
  • "compile le chapitre [X]", "génère le PDF du chapitre", "lance le build du workbook".
  • "modifie la question dans le chapitre [X]", "ajoute un exercice au chapitre", "change le thème en earth".
  • "ajoute un nouveau composant", "nouveau gabarit dans la boîte à outils".
---

# 🏗️ Architecture & Règles d'Or du Dépôt

L'agent DOIT respecter scrupuleusement les directives de [`Agent.md`](file:///c:/Users/nblum/LLM_LAB/PROJETS/mdm-workbook/Agent.md) :

1. **Règle absolue de modularité** :
   * Le paradigme "1 fichier = 1 chapitre" est **formellement interdit**.
   * La norme exclusive est : **1 dossier modulaire = 1 chapitre** (`Scripts/workbook_generator/chapters/chapX/`) contenant :
     - `__init__.py` : Routeur léger exportant les fonctions de rendu.
     - `intro.py` : Couverture, concept, récapitulatif.
     - `exercices.py` : Fonctions des pages d'exercices découpées.
     - (Optionnel) `cloture.py` ou fichiers thématiques spécifiques.
2. **Orchestration exclusive via `DocumentBuilder`** :
   * Tout script d'entrée racine (`Scripts/main_generate_chapX.py`) utilise `DocumentBuilder(output_path, theme)`.
   * Chaque page est ajoutée via `builder.add_page(create_<page>_page)`.
3. **Zéro dessin manuel empirique** :
   * Ne jamais coder de calculs $x, y$ hasardeux sur le canvas.
   * Utiliser systématiquement :
     - `PageLayout` et `layout.add_questions_group(questions)` pour les questions ouvertes auto-calibrées.
     - Les fonctions de haut niveau de `workbook_generator` (`create_standard_cover`, `create_standard_summary_page`, `create_standard_meteo_page`, `create_standard_quadrants_page`, `create_standard_two_columns_page`, `create_standard_engagement_page`, `create_closing_page`).
4. **Respect du Thème Graphique (`PDFStyle`)** :
   * Toujours utiliser les constantes de couleur (`PDFStyle.COLOR_ACCENT_BLUE`, `COLOR_ACCENT_RED`, `COLOR_CARD_CREME`, etc.) et de polices.
   * Permet le basculement instantané entre `--theme indigo` et `--theme earth`.
5. **Exécution depuis la racine du dépôt** :
   * Toujours lancer les commandes Python depuis la racine (`python Scripts/main_generate_chapX.py`) pour garantir la résolution des assets.

---

# 📚 Le Catalogue des 10 Gabarits Standards

| N° | Gabarit | Appel API (`workbook_generator`) | Usage |
|:---|:---|:---|:---|
| **1** | **Couverture** | `create_standard_cover(c, subtitle, title)` | Page de garde premium avec logo et marque |
| **2** | **Sommaire & Concept** | `create_standard_summary_page(c, num, title, intro, points)` | Fond indigo, filigrane géant, liste des jalons |
| **3** | **Questions Auto-Fit** | `PageLayout.add_questions_group(questions)` | 1 à 4 questions avec boîtes auto-dimensionnées |
| **4** | **Météo Intérieure** | `create_standard_meteo_page(c, title, part_title, ...)` | Émotions, jauge d'énergie 0-10, réflexion |
| **5** | **4 Quadrants / Matrice** | `create_standard_quadrants_page(c, title, part_title, data)` | Radar central vectoriel, 4 axes symétriques |
| **6** | **2 Colonnes Miroir** | `create_standard_two_columns_page(c, title, part_title, ...)` | Table comparative avec flèches relationnelles |
| **7** | **Enquête Réseau & Métier** | `create_standard_enquete_page(c, title, part_title, ...)` | Fiche contact + 3 axes qualitatifs (Customer Discovery) |
| **8** | **Feuille de Route 30·60·90** | `create_standard_roadmap_page(c, title, part_title, ...)` | 3 Paliers d'action avec objectifs, cases et KPI |
| **9** | **Engagement & Signature** | `create_standard_engagement_page(c, part_title, lines, title)` | Puces d'engagement + champ signature |
| **10** | **Clôture** | `create_closing_page(c, messages)` | Logo centré, félicitations et transition |

---

# 🧩 Le Système Atomique (Pages Composites Libres)

En complément des gabarits pleine page, `PageLayout` fournit des méthodes atomiques empilables pour composer des pages sur-mesure (`template: "composite"`) :

| Composant Atomique | Méthode Python | Usage & Paramètres |
|:---|:---|:---|
| **Callout** | `layout.add_callout(text, title, variant)` | Citation ou repère (variant: 'info', 'tip', 'quote') |
| **Grille de Cartes** | `layout.add_cards_grid(cards, columns, card_height)` | 2 ou 3 cartes d'analyse avec textareas AcroForm |
| **Jauge d'Échelle** | `layout.add_scale_gauge(label, min_val, max_val, min_label, max_label)` | Échelle 0-10 avec cases à cocher et bornes |
| **Checklist** | `layout.add_checklist(items, title, columns)` | Liste à cocher (1 ou 2 colonnes) avec interligne fluide |
| **Tableau** | `layout.add_table(headers, rows, col_widths)` | Tableau d'actions ou métriques avec cellules de saisie |
| **Stat Boxes** | `layout.add_stat_boxes(stats)` | 2 à 4 indicateurs KPI chiffrés |
| **Question** | `layout.add_question_block(question, field_id, config)` | Question ouverte avec boîte de saisie auto-ajustée |

> [!TIP]
> **Règle d'or de respiration visuelle : 2 à 3 composants par page maximum.**  
> Préserver toujours des zones blanches généreuses pour que la page reste aérée, claire et accueillante pour le bénéficiaire.

---

# 🚀 Procédures Opérationnelles par Mode

## Mode 1 : CONCEPTION (Notes Brutes → Fiche de Conception)

Ce mode est activé lorsque l'utilisateur fournit des notes, un compte-rendu de séance ou des idées en vrac.
**Objectif :** Réfléchir à la pédagogie, calibrer les longueurs de texte et figer la maquette avant d'écrire du code.

### Étapes d'exécution :
1. **Analyser les notes brutes** :
   * Extraire le thème principal, les objectifs pédagogiques et le nombre de pages estimé (idéalement 5 à 10 pages).
2. **Mapper chaque page vers le gabarit idéal** :
   * Page 1 : Couverture (Gabarit 1)
   * Page 2 : Sommaire / Intentions (Gabarit 2)
   * Page 3 : Météo & Climat (Gabarit 4) si besoin d'un ice-breaker
   * Pages d'exercices : Alterner entre Questions Auto-Fit (Gabarit 3), 4 Quadrants (Gabarit 5), et 2 Colonnes Miroir (Gabarit 6)
   * Page Avant-dernière : Engagement (Gabarit 7) ou synthèse
   * Dernière page : Clôture (Gabarit 8)
3. **Calibrer les textes (Budget de caractères)** :
   * Formuler des consignes claires, concises et engageantes.
   * Vérifier que les intitulés respectent les budgets (max 120 caractères par question).
4. **Rédiger le fichier de conception** :
   * Sauvegarder dans `Wordbook/Conception_Workbook_Chapitre_X.md`.
5. **Arrêt obligatoire (Point de synchronisation)** :
   * Présenter la synthèse des pages proposées à l'utilisateur et lui demander explicitement sa validation avant de lancer la compilation.

---

## Mode 2 : COMPILATION (Fiche Validée → PDF Final)

Ce mode est activé dès que l'utilisateur valide la conception.

### Étapes d'exécution :
1. **Créer l'arborescence modulaire** :
   * Créer le dossier `Scripts/workbook_generator/chapters/chapX/`.
   * Créer `__init__.py` exportant les fonctions de pages.
   * Créer `intro.py` (couverture, sommaire, récap).
   * Créer `exercices.py` (pages d'exercices utilisant les gabarits standards).
2. **Créer le script d'entrée CLI** :
   * Créer `Scripts/main_generate_chapX.py` :
     ```python
     from workbook_generator.utils import create_cli
     from workbook_generator.document_builder import DocumentBuilder
     from workbook_generator.chapters import chapX
     from workbook_generator.components import create_closing_page

     def generate_workbook_chapX(output_filename="Workbook_Chapitre_X.pdf", theme="indigo"):
         builder = DocumentBuilder(output_path=output_filename, theme=theme)
         builder.set_title("MDM - Workbook Chapitre X")
         
         builder.add_page(chapX.create_chapX_cover)
         builder.add_page(chapX.create_concept_page)
         # ... ajouter chaque page ...
         builder.add_page(create_closing_page)
         
         builder.save()

     if __name__ == "__main__":
         args = create_cli("Générer le chapitre X PDF.", "Workbook_Chapitre_X.pdf")
         generate_workbook_chapX(output_filename=args.output, theme=args.theme)
     ```
3. **Exécuter la compilation** :
   * Lancer la commande : `python Scripts/main_generate_chapX.py`.
4. **Vérification automatique** :
   * S'assurer du code de retour 0.
   * Si ReportLab émet une erreur de permission (PDF ouvert), informer poliment l'utilisateur.
   * Livrer le lien direct vers le fichier PDF généré.

---

## Mode 3 : MODIFICATION D'UN CHAPITRE EXISTANT

Ce mode est activé lorsque l'utilisateur demande d'ajuster un chapitre existant.

### Étapes d'exécution :
1. **Localiser précisément la page cible** :
   * Examiner `Scripts/main_generate_chapX.py` pour voir quelles fonctions sont appelées et dans quel fichier elles résident.
2. **Appliquer la modification** :
   * Modifier le texte ou la question.
   * Grâce à `PageLayout.add_questions_group()`, les dimensions des boîtes se réajustent automatiquement.
3. **Recompiler et vérifier** :
   * Exécuter `python Scripts/main_generate_chapX.py`.
   * Vérifier que la génération réussit.

---

## Mode 4 : ENRICHISSEMENT DE LA BOÎTE À OUTILS

Ce mode est activé lorsqu'un exercice nécessite un composant visuel inédit.

### Étapes d'exécution :
1. **Coder le composant dans `Scripts/workbook_generator/components.py`** :
   * Utiliser les constantes de `PDFStyle`.
   * Gérer les formulaires via `create_input_field` ou `create_checkbox`.
   * Respecter le suivi de curseur vertical (`return new_y_pos`).
2. **Exporter dans `Scripts/workbook_generator/__init__.py`**.
3. **Valider dans `Scripts/test_all_templates.py`** :
   * Ajouter une page de test pour le nouveau composant.
   * Exécuter `python Scripts/test_all_templates.py` et vérifier le rendu.
4. **Utiliser dans le chapitre**.

---

# 🛡️ Checklist Qualité Avant Livraison

Avant d'annoncer à l'utilisateur que son PDF est prêt :
* [ ] Le script a retourné le code de sortie `0`.
* [ ] La règle 1 dossier = 1 chapitre est respectée (pas de script monolithique).
* [ ] Aucune variable $y$ calculée à l'aveugle : utilisation stricte des helpers ou d'Auto-Fit.
* [ ] Les champs AcroForm ont des identifiants uniques.
* [ ] Le lien cliquable vers le PDF est fourni dans la réponse.
