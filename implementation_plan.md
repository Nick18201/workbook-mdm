# Workbook Chapitre 4 – Valeurs, Moteurs et Relation à l'Argent

Create a new Chapter 4 PDF workbook following the established project patterns, based on the conception document and all exercise files in `Wordbook/Chapter 4/`.

## Proposed Changes

### Chapter Module

#### [NEW] [chap4.py](file:///c:/Users/nblum/LLM_LAB/PROJETS/workbook-mdm/Scripts/workbook_generator/chapters/chap4.py)

Following the exact same pattern as `chap3.py` (imports from `..config`, `..components`, `..templates`, `..forms`), this file will contain all page-generation functions for the 8 pages defined in the conception document:

| Function | Page | Content Source |
|---|---|---|
| `create_chap4_cover(c)` | Cover | `create_standard_cover()` – "CHAPITRE 4 : VALEURS, MOTEURS ET RELATION À L'ARGENT" |
| `create_concept_page(c)` | Sommaire | `create_standard_summary_page()` – 8-item table of contents |
| `create_recap_seance_page(c)` | Page 1: Récapitulatif | `create_standard_recap_page()` – 3 questions about previous session (MBTI) |
| `create_valeurs_page(c)` | Page 2: Moteurs Profonds | `PageLayout` – Schwarz values (3 values + examples + heritage + conflict) + action verbs (preferred + disliked), from `Exercice_Valeurs_Schwarz.md` & `Exercice_Verbes_Action.md`. Split across 2 pages (2a: Values, 2b: Verbs) |
| `create_psycho_edu_page(c)` | Intro page | Psycho-education introduction text from `Psycho_Education_Financiere.md` & `Module_Psychologie_Economique.md` – explaining the Money Scripts framework before the quiz |
| `create_kmsi_pages(c)` | Page 3: Money Script Quiz | Custom layout – 4 Likert-scale sections (Avoidance, Worship, Status, Vigilance) with checkbox scales from `Exercice_Inventaire_Croyances.md`. Spans 2 pages |
| `create_biographie_page(c)` | Page 4: Biographie Financière | `PageLayout` with question blocks – First memory, adolescence, belief analysis from `Exercice_Biographie_Financiere.md` |
| `create_dialogue_page(c)` | Page 5: Lettre à l'Argent | Custom layout – Large textarea for the letter ("Cher Argent...") + structured prompts from `Exercice_Dialogue_Argent.md` |
| `create_archetypes_page(c)` | Page 6: Archétypes Sacrés | Custom layout – Top 3 selection + action plan from `Exercice_Archetypes_Sacres.md` |
| `create_mindset_surplus_page(c)` | Page 6 cont: Mindset de Surplus | `PageLayout` – Scarcity vs Surplus diagnostic + 3 generosity actions + projection question from `Exercice_Mindset_Surplus.md` |
| `create_cartographie_page(c)` | Page 7: Cartographie Personnelle | Custom 2-column layout – Synthesis dashboard (Profile, Moteurs, Besoins, Objectifs, Feedback) from `Modele_Cartographie_Personnelle.md` |
| `create_exploration_page(c)` | Page 8: Travail Inter-Session | `PageLayout` – 3 career exploration tracks with fields for "why" and "doubts" |

> [!NOTE]
> Some pages will be split across multiple physical PDF pages when content is too dense for a single A4 page (e.g., Values/Verbs, KMSI quiz, Archetypes + Surplus mindset). This follows the pattern used in `chap2.py` and `chap3.py`.

---

### Main Script

#### [NEW] [main_generate_chap4.py](file:///c:/Users/nblum/LLM_LAB/PROJETS/workbook-mdm/Scripts/main_generate_chap4.py)

Same structure as `main_generate_chap3.py`:
- Import `chap4` module + `PDFStyle`, `register_fonts`, `create_closing_page`
- `generate_workbook_chap4()` function calling each page function in order
- CLI with `--theme` and `--output` arguments
- Default output: `Workbook_Chapitre_4.pdf`

## Open Questions

> [!IMPORTANT]
> **Theme**: The default theme for the existing chapters varies (`earth` for chap3). Should Chapter 4 also default to `earth` theme, or would you like a different default?

> [!IMPORTANT]
> **Psycho-education page**: The conception document mentions a "psycho-education" introduction before the financial quiz. The content from `Psycho_Education_Financiere.md` and `Module_Psychologie_Economique.md` is informational (no form fields). Should I include this as a read-only text page (like the intro pages in chap0/chap3), or skip it?

## Verification Plan

### Automated Tests
- Run `python Scripts/main_generate_chap4.py` and verify PDF generation completes without errors
- Verify the output file `Workbook_Chapitre_4.pdf` exists and can be opened
