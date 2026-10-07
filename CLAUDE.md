# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Generates interactive PDF workbooks (AcroForm fields, A4) with ReportLab for "Marge de Manœuvre" (MDM), a French career-coaching / bilan de compétences practice. All user-facing content (PDF text, LLM prompts, UI, docs) is in French and should stay French. `Agent.md` and `SKILL.md` at the repo root are the original (French) design rules and workflows; read them before larger changes.

## Commands

Always run from the repository root: asset paths resolve from `PDFStyle.PROJECT_DIR`, and the PDF output path is relative to the cwd. The virtualenv lives in the main checkout (`.venv`, Python 3.14); from a worktree under `.claude/worktrees/<name>/` it is `../../../.venv`.

```bash
python Scripts/main_generate_chap1.py --theme earth --output Workbook_Chapitre_1.pdf
python Scripts/test_all_templates.py
python Scripts/test_composite_page.py
python -m uvicorn server.app:app --port 8080 --reload
```

- Every `Scripts/main_generate_*.py` (chap0–chap6, `livret`, `business_plan`, `programme`) takes `--theme {indigo,earth}` and `--output`. Exit code 0 plus `PDF generated successfully: ...` means it built.
- There is no pytest suite and no linter config. The "tests" are scripts that render showcase PDFs (`Test_All_Templates.pdf`, `Test_Composite_Page.pdf`, `Test_Spec_Composite.pdf`) at the repo root. `test_composite_page.py` also needs `pymupdf` (not in `requirements.txt`) and writes PNG previews to a hard-coded `C:\Users\nblum\.gemini\...` folder. `chapters/programme/render_inspect.py` does the same.
- If `DocumentBuilder` exits with "Cannot overwrite", the target PDF is open in another program.
- Generated PDFs are git-ignored. `scratch/` holds committed page PNG previews.
- Deployment (Cloud Run via `Dockerfile`, `GEMINI_API_KEY` env var) is covered in `server/DEPLOY_CLOUD_RUN.md`.

## Architecture

The same rendering library feeds two pipelines.

### 1. Rendering library: `Scripts/workbook_generator/`
- `DocumentBuilder(output_path, theme)` is the entry point for every document. It sets the theme, registers fonts from `assets/fonts` (falls back to Helvetica), and wraps the canvas. `output_path` can be a file path or a `BytesIO`. `add_page(fn, *args)` just calls `fn(canvas, *args)`.
- **Each page function must end its own page.** `PageLayout.render()` and the `create_standard_*` / `create_closing_page` helpers call `c.showPage()`. Hand-drawn pages must call it themselves. `add_page` does not.
- `config.PDFStyle` is global, mutable class state. `set_theme()` overwrites the `COLOR_*` attributes and `register_fonts()` overwrites the `FONT_*` attributes. Read `PDFStyle.X` at draw time, never cache it at import time, and never hard-code hex colors, or the indigo/earth switch breaks.
- `templates.PageLayout` is a vertical flow layout. You add blocks (`add_text`, `add_questions_group` for auto-sized question boxes, plus the atomic `add_callout`, `add_cards_grid`, `add_scale_gauge`, `add_checklist`, `add_table`, `add_stat_boxes`, `add_question_block`), then call `render()`. Prefer it over manual x/y math. The house style is 2–3 blocks per page with lots of white space.
- `components.py` holds the full-page templates (`create_standard_cover`, `_summary_page`, `_meteo_page`, `_quadrants_page`, `_two_columns_page`, `_enquete_page`, `_roadmap_page`, `_engagement_page`, `create_closing_page`) and the drawing primitives (backgrounds, side panel, cards, titles). `forms.py` holds the AcroForm field helpers. Public API is re-exported from `workbook_generator/__init__.py`.
- Performance helpers in `utils.py` (see `.jules/bolt.md`): `useA85 = 0`, `cached_simpleSplit`, `cached_image_reader` (snake_case; there is also an alias `cached_ImageReader`). Repeated backgrounds such as the dot grid and blobs are cached as Form XObjects (`beginForm` / `doForm`). Keep this pattern for anything drawn on every page.
- AcroForm field names must be unique across the whole PDF. Reusing an id links the fields.

### 2. Static CLI documents: `Scripts/main_generate_*.py` + `chapters/<name>/`
- Rule from `Agent.md`: **one folder per chapter, never one file per chapter.** Each `chapters/<name>/` has an `__init__.py` that only re-exports page functions, plus split modules (`intro.py`, `exercices.py`, `cloture.py`, thematic files). `chapters/` itself has no `__init__.py` (namespace package).
- Conventions: page functions are named `create_<page>_page(c)`, the canvas is always `c` as the first argument, and the running vertical cursor is `y_pos`.
- The `main_generate_*.py` script lists page order via `builder.add_page(...)`. The scripts add `Scripts/` to `sys.path` so `from workbook_generator...` resolves.
- `chapters/programme/` (the Qualiopi programme/pricing brochure) is laid out by hand on `setup_programme_page()` from `programme/common.py`, not on `PageLayout`. Several `page_*.py` files there are not wired into `programme/__init__.py` or `main_generate_programme.py`. Check the router before editing a page. After building, `main_generate_programme.py` also copies the PDF into a sibling `../marge-de-manoeuvre/public/documents/` repo if that folder exists.

### 3. Web app: `server/` (FastAPI + Gemini)
- Flow: raw coaching notes → `gemini_service.parse_notes_with_gemini` (google-genai, JSON mode, model fallback list, then a heuristic mock spec if there is no `GEMINI_API_KEY` or the call fails) → a `models.WorkbookSpec` (pages, each with a `template` + `params`, or `composite` + `blocks`) → `pdf_compiler.compile_workbook_from_spec` → PDF bytes.
- Endpoints in `app.py`: `/api/parse`, `/api/iterate` (refine a spec from feedback), `/api/customize` (adapt a predefined workbook to a beneficiary), `/api/templates[/{id}]`, `/api/compile`, `/api/quick-generate`. The UI is a single file, `server/templates/index.html`. `.env` at the root or in `server/` is auto-loaded.
- `pdf_compiler.py` maps each template name to a `workbook_generator` function and is deliberately lenient with param aliases (e.g. `points`/`steps`/`items`), because the specs come from an LLM. Keep that tolerance.
- `predefined_workbooks.py` holds hand-written `WorkbookSpec` versions of chap0–6 and the business plan. They are a **separate copy** of the content in `chapters/`, not generated from it, so content edits in one pipeline do not reach the other.

### Adding a new page template or atomic block
These pieces must stay in sync:
1. The function in `components.py` (or a `PageLayout.add_*` method in `templates.py`).
2. The export in `workbook_generator/__init__.py`.
3. The `Literal` in `PageSpec.template` or `BlockSpec.type` in `server/models.py`.
4. The dispatch branch in `server/pdf_compiler.py`.
5. The template/param documentation inside `SYSTEM_PROMPT` in `server/gemini_service.py`, so Gemini can emit it.
6. A showcase page in `Scripts/test_all_templates.py`.

## Guardrails from `Agent.md`
- Do not overwrite or delete anything in `assets/` without user confirmation.
- Reuse `components.py` / `templates.py` helpers rather than drawing directly on the canvas.
