# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Generates interactive PDF workbooks (AcroForm fields, A4) with ReportLab for "Marge de Manœuvre" (MDM), a French career-coaching / bilan de compétences practice. All user-facing content (PDF text, LLM prompts, UI, docs) is in French and should stay French. `Agent.md` and `SKILL.md` at the repo root are the original (French) design rules and workflows; read them before larger changes.

## Commands

Always run from the repository root: asset paths resolve from `PDFStyle.PROJECT_DIR`, and the PDF output path is relative to the cwd. The virtualenv lives in the main checkout (`.venv`, Python 3.14); from a worktree under `.claude/worktrees/<name>/` it is `../../../.venv`.

```bash
python Scripts/main_generate_chap1.py --theme earth --output Workbook_Chapitre_1.pdf
pip install -r requirements-dev.txt
python -m pytest tests
python -m pytest tests/test_pdf_compiler.py -k field_names
python Scripts/test_all_templates.py
python -m uvicorn server.app:app --port 8080 --reload
```

- Every `Scripts/main_generate_*.py` (chap0–chap6, `livret`, `business_plan`, `programme`) takes `--theme {indigo,earth}` and `--output`. Exit code 0 plus `PDF generated successfully: ...` means it built.
- `tests/` is the pytest suite (compiler and API; Gemini is faked by monkeypatching `gemini_service.genai.Client`). It needs `requirements-dev.txt` (pytest, pymupdf, httpx). There is no linter config.
- `Scripts/test_*.py` are not tests but showcase scripts that render `Test_*.pdf` at the repo root. `test_composite_page.py` also writes PNG previews to `previews/` (git-ignored).
- If `DocumentBuilder` raises `PermissionError: Cannot overwrite ...`, the target PDF is open in another program.
- Generated PDFs are git-ignored. `scratch/` holds committed page PNG previews.
- Deployment (Cloud Run via `Dockerfile`; `GEMINI_API_KEY` is injected from the Secret Manager secret `gemini-api-key`, never set as a plain env var) is covered in `server/DEPLOY_CLOUD_RUN.md`.

## Architecture

The same rendering library feeds two pipelines.

### 1. Rendering library: `Scripts/workbook_generator/`
- `DocumentBuilder(output_path, theme)` is the entry point for every document. It sets the theme, registers fonts from `assets/fonts` (falls back to Helvetica), and wraps the canvas. `output_path` can be a file path or a `BytesIO`. `add_page(fn, *args)` just calls `fn(canvas, *args)`.
- **Each page function must end its own page.** `PageLayout.render()` and the `create_standard_*` / `create_closing_page` helpers call `c.showPage()`. Hand-drawn pages must call it themselves. `add_page` does not.
- `config.PDFStyle` is global, mutable class state. `set_theme()` overwrites the `COLOR_*` attributes and `register_fonts()` overwrites the `FONT_*` attributes. Read `PDFStyle.X` at draw time, never cache it at import time, and never hard-code hex colors, or the indigo/earth switch breaks.
- `templates.PageLayout` is a vertical flow layout. You add blocks (`add_text`, `add_questions_group` for auto-sized question boxes, plus the atomic `add_callout`, `add_cards_grid`, `add_scale_gauge`, `add_checklist`, `add_table`, `add_stat_boxes`, `add_question_block`), then call `render()`. Prefer it over manual x/y math. The house style is 2–3 blocks per page with lots of white space.
- Nothing may run off the page. Each `add_*` calls `_ensure_space(height)`, which starts a continuation page titled `"<title> (suite)"` (and repeats table headers). `add_questions_group` packs questions page by page. The hand-drawn templates (`two_columns`, `enquete`, `roadmap`, `quadrants`) paginate the same way through their `_draw_*_page` helpers, which return the items left over. For single-line labels in fixed boxes, use `draw_fitted_text()` (shrinks, wraps, then a visible `…`).
- Montserrat has no emoji, ✓, ☀…: ReportLab drops them silently. Draw pictograms with `draw_symbol()` (ZapfDingbats, built into PDF viewers: ✔ ★ ➔ ✉ ☛) or vector helpers such as `draw_weather_icon()`. `pdf_compiler` cleans spec text with `utils.strip_unsupported_glyphs`.
- Single-choice scales are radio groups: reserve the group name once with `forms.reserve_field_name()`, then call `forms.create_radio()` per value.
- `components.py` holds the full-page templates (`create_standard_cover`, `_summary_page`, `_meteo_page`, `_quadrants_page`, `_two_columns_page`, `_enquete_page`, `_roadmap_page`, `_engagement_page`, `create_closing_page`) and the drawing primitives (backgrounds, side panel, cards, titles). `forms.py` holds the AcroForm field helpers. Public API is re-exported from `workbook_generator/__init__.py`.
- Performance helpers in `utils.py` (see `.jules/bolt.md`): `useA85 = 0`, `cached_simpleSplit`, `cached_image_reader` (snake_case; there is also an alias `cached_ImageReader`). Repeated backgrounds such as the dot grid and blobs are cached as Form XObjects (`beginForm` / `doForm`). Keep this pattern for anything drawn on every page.
- AcroForm field names must be unique across the whole PDF, since a reused id links the fields. `forms.create_input_field` / `create_checkbox` enforce this by suffixing repeats (`_2`, `_3`…), so always go through them rather than `form.textfield` directly.

### 2. Static CLI documents: `Scripts/main_generate_*.py` + `chapters/<name>/`
- Rule from `Agent.md`: **one folder per chapter, never one file per chapter.** Each `chapters/<name>/` has an `__init__.py` that only re-exports page functions, plus split modules (`intro.py`, `exercices.py`, `cloture.py`, thematic files). `chapters/` itself has no `__init__.py` (namespace package).
- Conventions: page functions are named `create_<page>_page(c)`, the canvas is always `c` as the first argument, and the running vertical cursor is `y_pos`.
- The `main_generate_*.py` script lists page order via `builder.add_page(...)`. The scripts add `Scripts/` to `sys.path` so `from workbook_generator...` resolves.
- `chapters/programme/` (the Qualiopi programme/pricing brochure) is laid out by hand on `setup_programme_page()` from `programme/common.py`, not on `PageLayout`. Page order is set in `main_generate_programme.py`; the `create_programme_page_N` aliases in `programme/__init__.py` follow it. After building, `main_generate_programme.py` also copies the PDF into a sibling `../marge-de-manoeuvre/public/documents/` repo if that folder exists.

### 3. Web app: `server/` (FastAPI + Gemini)
- Flow: raw coaching notes → `gemini_service.parse_notes_with_gemini` → a `models.WorkbookSpec` (pages, each with a `template` + `params`, or `composite` + `blocks`) → `pdf_compiler.compile_workbook_from_spec` → PDF bytes.
- Gemini calls go through `_generate_json`, which tries each model of `GEMINI_MODELS` (env var, comma-separated, default `gemini-3.8-flash` alone) on a client cached per API key, with a `GEMINI_TIMEOUT_S` timeout (default 120 s; a parse takes ~30 s). The three service functions return a `GenerationResult(value, fallback_reason)`: when there is no `GEMINI_API_KEY` (`no_api_key`) or every model fails (`model_error`), the value comes from a heuristic mock. `app.py` exposes this as `X-MDM-Generation: ai|fallback` and `X-MDM-Fallback-Reason` headers, which the UI shows as a warning banner.
- Endpoints in `app.py`: `/api/parse`, `/api/iterate` (refine a spec from feedback), `/api/customize` (adapt a predefined workbook to a beneficiary), `/api/templates[/{id}]`, `/api/compile`, `/api/quick-generate`. The UI is a single file, `server/templates/index.html`. `.env` at the root or in `server/` is auto-loaded.
- In production the service sits behind IAP (Cloud Run `iap-enabled`, access limited to `domain:margedemanoeuvre.fr`); the app itself has no authentication. There is no CORS middleware: the UI is same-origin.
- Input sizes are bounded by the `MAX_*` constants in `models.py` (text lengths, pages, blocks per page, list items and text length anywhere in a spec, scale span). Beyond them the API answers 422, and `app.py` turns validation errors into a French string `detail` that the UI shows as is. A 500 never carries the exception text (it is logged instead).
- `pdf_compiler.py` maps each template name to a `workbook_generator` function and is deliberately lenient with param aliases (e.g. `points`/`steps`/`items`), because the specs come from an LLM. Keep that tolerance. It is also the trust boundary: spec text that reaches ReportLab paragraph markup (the summary intro) must be escaped there, and default field ids are prefixed with the page index (`p{page_idx}_…`).
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
