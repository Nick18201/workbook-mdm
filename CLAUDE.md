# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Generates interactive PDF workbooks (AcroForm fields, A4) with ReportLab for "Marge de Manœuvre" (MDM), a French career-coaching / bilan de compétences practice. All user-facing content (PDF text, LLM prompts, UI, docs) is in French and should stay French. `Agent.md` and `SKILL.md` at the repo root are the original (French) design rules and workflows; read them before larger changes.

## Commands

Always run from the repository root: asset paths resolve from `PDFStyle.PROJECT_DIR`, and the PDF output path is relative to the cwd. The virtualenv lives in the main checkout (`.venv`, Python 3.14); from a worktree under `.claude/worktrees/<name>/` it is `../../../.venv`.

```bash
python Scripts/main_generate_chap1.py --output Workbook_Chapitre_1.pdf
pip install -r requirements-dev.txt
python -m pytest tests
python -m pytest tests/test_pdf_compiler.py -k field_names
python Scripts/test_all_templates.py
python -m uvicorn server.app:app --port 8080 --reload
```

- Every `Scripts/main_generate_*.py` (chap0–chap6, `livret`, `business_plan`, `programme`) takes `--output`. Exit code 0 plus `PDF generated successfully: ...` means it built.
- `tests/` is the pytest suite (compiler and API; Gemini is faked by monkeypatching `gemini_service.genai.Client`). It needs `requirements-dev.txt` (pytest, pymupdf, httpx). There is no linter config.
- CI (`.github/workflows/tests.yml`, on pull requests and pushes to `main`) runs pytest and builds the 10 CLI documents on Python 3.14.
- Python 3.14 everywhere (local `.venv`, `python:3.14-slim` in Docker, CI). `requirements.txt` and `requirements-dev.txt` are lock files with every package pinned, for Windows and Linux alike. Edit the direct dependencies in `requirements.in` / `requirements-dev.in`, then regenerate both locks with the `uv pip compile ...` commands written at the top of each (`pip install uv` first), `requirements.txt` first since the dev lock is constrained by it.
- `Scripts/test_*.py` are not tests but showcase scripts that render `Test_*.pdf` at the repo root. `test_composite_page.py` also writes PNG previews to `previews/` (git-ignored).
- If `DocumentBuilder` raises `PermissionError: Cannot overwrite ...`, the target PDF is open in another program.
- Generated PDFs are git-ignored. `scratch/` holds committed page PNG previews.
- Deployment (Cloud Run via `Dockerfile`; `GEMINI_API_KEY` is injected from the Secret Manager secret `gemini-api-key`, never set as a plain env var) is covered in `server/DEPLOY_CLOUD_RUN.md`.

## Architecture

The same rendering library feeds two pipelines.

### 1. Rendering library: `Scripts/workbook_generator/`
- The art direction is « Éditorial & Affirmé » (`DA-workbook.md`, `design-system/`): linen pages (`PDFStyle.COLOR_PAGE`, #F1EBE6, painted under each page by the canvas `DocumentBuilder` creates, so page functions never draw a background; on linen the title accent is coral-strong, `COLOR_TITLE_ACCENT`), an eyebrow or pill label then a punctuated title whose last word (or `*marked words*`) is coral, pastel cards, white answer boxes bordered in `line-strong`, PT Mono folio. One palette only.
- Tone (DA section 7): vouvoiement, short affirmative sentences, punctuated sentence-case titles; never « coach » (say « consultant en transformation » or « la personne qui vous accompagne »), no personal-development wording (« quête de sens », « croyances limitantes », « syndrome de l'imposteur »…), never « présentiel », no unsourced figure. The Gemini prompts share these rules (`TONE_RULES` in `gemini_service.py`).
- `DocumentBuilder(output_path, pastel=None, folio="", carnet=None)` is the entry point for every document. It registers fonts from `assets/fonts` (falls back to Helvetica, Courier, Times) and wraps the canvas. `carnet=N` (0–6) sets the dominant pastel (`PDFStyle.CARNET_PASTELS`) and the folio « carnet N/7 »; other documents pass a short `folio`. These per-document settings live on the canvas (`document_style(c)`, `document_pastel(c)`), not on `PDFStyle`. `output_path` can be a file path or a `BytesIO`. `add_page(fn, *args)` just calls `fn(canvas, *args)`.
- **Each page function must end its own page.** `PageLayout.render()` and the `create_standard_*` / `create_closing_page` helpers call `c.showPage()`. Hand-drawn pages must call it themselves. `add_page` does not.
- `config.PDFStyle` holds the tokens: colors (`COLOR_INK`, `COLOR_CORAL_STRONG`, `PASTELS`…), the print type scale (`SIZE_*`), layout values. Former names (`COLOR_ACCENT_BLUE`, `FONT_TITLE`…) are aliases kept for the hand-drawn chapter pages until lot E5. `register_fonts()` overwrites the `FONT_*` attributes (fallbacks), so read `PDFStyle.X` at draw time and never hard-code hex colors.
- `templates.PageLayout` is a vertical flow layout. You add blocks (`add_text`, `add_questions_group` for auto-sized question boxes, plus the atomic `add_callout`, `add_cards_grid`, `add_scale_gauge`, `add_checklist`, `add_table`, `add_stat_boxes`, `add_question_block`), then call `render()`. Prefer it over manual x/y math. The house style is 2–3 blocks per page with lots of white space.
- Nothing may run off the page. Each `add_*` calls `_ensure_space(height)`, which starts a continuation page titled `"<title> (suite)"` (and repeats table headers). `add_questions_group` packs questions page by page. The hand-drawn templates (`two_columns`, `enquete`, `roadmap`, `quadrants`) paginate the same way through their `_draw_*_page` helpers, which return the items left over. For single-line labels in fixed boxes, use `draw_fitted_text()` (shrinks, wraps, then a visible `…`).
- `primitives.py` holds the art direction's building blocks: `draw_text` (tracking, always reset: PDF `Tc` leaks into later text otherwise), `draw_paragraph`, `draw_heading` (accent title), `draw_eyebrow`, `draw_label_pill`, `draw_number`, cards, `draw_field_box`, `postit()` (a context manager), `draw_drawn_arrow`, `draw_star_list`, `draw_stamp`, `draw_icon` / `draw_icon_badge` (Material Symbols Outlined by name), `draw_frise`, `draw_logotype`, `draw_signature`, `draw_folio`, `draw_page_head`.
- The fonts have no emoji, ✓, ☀, ◀…: ReportLab drops them silently. Draw pictograms as icons (`draw_icon`) or vectors (stars, arrows). `pdf_compiler` cleans spec text with `utils.strip_unsupported_glyphs` (characters missing from Manrope, DM Sans or PT Mono). No font has the narrow no-break space U+202F: use U+00A0.
- French typography is automatic: every text primitive (and the summary intro, table cells) goes through `utils.french_typography` (no-break space before `: ; ! ?`, inside « », between a number and its unit; "…" → « … »; oe → œ in cœur, œuvre…; MBTI → MBTI®), which leaves markup tags, entities and URLs alone. Line wrapping never breaks at U+00A0: split words with `utils.split_words` / `cached_simpleSplit`, never `str.split()`.
- Single-choice scales are radio groups: reserve the group name once with `forms.reserve_field_name()`, then call `forms.create_radio()` per value.
- `components.py` holds the full-page templates (`create_cover_page` and the former `create_standard_cover`, the chapter opener `create_standard_summary_page`, `_meteo_page`, `_quadrants_page`, `_two_columns_page`, `_enquete_page`, `_roadmap_page`, the end of workbook `create_standard_engagement_page` with the deliverable post-it and stamp, the blue back cover `create_closing_page`) and shared blocks (`draw_question`, `draw_answer_box`, `draw_choice_scale`). Former helpers (`draw_page_background`, `draw_side_panel`, `draw_title`, `draw_card`…) keep their signatures for the chapters. `forms.py` holds the AcroForm field helpers: `framed=False` gives a transparent field to lay over a drawn box; fields ignore canvas transforms, so never put one inside a rotated post-it. Public API is re-exported from `workbook_generator/__init__.py`.
- Performance helpers in `utils.py` (see `.jules/bolt.md`): `useA85 = 0`, `cached_simpleSplit`, `cached_image_reader` (snake_case; there is also an alias `cached_ImageReader`). Cache anything heavy drawn on every page as a Form XObject (`beginForm` / `doForm`).
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
