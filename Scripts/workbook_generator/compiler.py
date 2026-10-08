"""
Compiles a WorkbookSpec (spec.py) into a PDF: the single engine of the CLI documents
(the reference workbooks of workbooks/) and of the web app (Gemini, customization).
"""

import functools
import io
import json
import os
from xml.sax.saxutils import escape

from reportlab.lib.units import cm

from .components import (
    as_title,
    create_closing_page,
    create_cover_page,
    create_standard_engagement_page,
    create_standard_enquete_page,
    create_standard_meteo_page,
    create_standard_quadrants_page,
    create_standard_recap_page,
    create_standard_roadmap_page,
    create_standard_summary_page,
    create_standard_two_columns_page,
    split_chapter_label,
)
from .config import PDFStyle
from .document_builder import DocumentBuilder
from .primitives import plain_title
from . import spec as spec_module
from .spec import MAX_SCALE_STEPS, WorkbookSpec, data_carnet, load_workbook
from .templates import LayoutConfig, PageLayout, QuestionConfig, QuestionItem, TextConfig
from .utils import strip_unsupported_glyphs

MAX_BLOCK_HEIGHT_CM = 20


def _as_number(value, default, cast=float):
    """Numeric block value, or default: blocks given in params['blocks'] are not validated by BlockSpec."""
    try:
        return cast(value)
    except (TypeError, ValueError, OverflowError):
        return default


def _height_pt(height_cm, default=None):
    height_cm = _as_number(height_cm, None)
    if height_cm is None or not height_cm > 0:
        return default
    return min(height_cm, MAX_BLOCK_HEIGHT_CM) * cm


def _length_pt(value_cm, default=None):
    """A length of the spec (cm, 0 allowed) in points, or default."""
    value_cm = _as_number(value_cm, None)
    if value_cm is None or value_cm < 0:
        return default
    return min(value_cm, MAX_BLOCK_HEIGHT_CM) * cm


def _color(name):
    """A pastel ('sky') or a DA color ('coral_strong') by name; None for anything else."""
    if not isinstance(name, str):
        return None
    return PDFStyle.PASTELS.get(name) or getattr(PDFStyle, f"COLOR_{name.upper()}", None)


def _scale_bounds(b_data):
    low = _as_number(b_data.get("min_val"), 0, int)
    high = _as_number(b_data.get("max_val"), 10, int)
    if not 0 < high - low <= MAX_SCALE_STEPS:
        return 0, 10
    return low, high


# Inline tags a spec may use in ReportLab markup (the summary intro): bold, italic, line break
_SAFE_TAGS = ("<b>", "</b>", "<i>", "</i>", "<br/>")


def _safe_markup(text):
    """Spec text for ReportLab markup: everything escaped, except a few attribute-free tags."""
    text = escape(str(text))
    for tag in _SAFE_TAGS:
        text = text.replace(escape(tag), tag)
    return text


def _title(text, default=""):
    """A page title as shown: punctuated, an all-caps title from the spec in sentence case."""
    return as_title(str(text or default))


def _eyebrow(number, title, default=""):
    """Default eyebrow of a page: « 2. MON TITRE » (no final punctuation nor accent marks)."""
    return f"{number}. {plain_title(title or default).rstrip('.!?… ').upper()}"


def _without_unsupported_glyphs(spec: WorkbookSpec) -> WorkbookSpec:
    """Removes characters the PDF fonts cannot draw (emojis, ✓…) from every text of the spec."""

    def clean(value):
        if isinstance(value, str):
            return strip_unsupported_glyphs(value)
        if isinstance(value, dict):
            return {k: clean(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return type(value)(clean(v) for v in value)
        return value

    return WorkbookSpec.model_validate(clean(spec.model_dump(exclude_unset=True)))


def _question_items(raw_questions, prefix):
    """QuestionItem list from spec questions (dicts or plain texts)."""
    if isinstance(raw_questions, dict):
        raw_questions = list(raw_questions.values())
    items = []
    for i, q in enumerate(raw_questions or []):
        if hasattr(q, "model_dump"):
            q = q.model_dump()
        if isinstance(q, dict):
            q_text = q.get("question") or q.get("text") or q.get("title") or q.get("label") or f"Question {i + 1}"
            example = q.get("example") or q.get("ex")
            items.append(QuestionItem(
                question=str(q_text),
                form_field_id=str(q.get("field_id") or f"{prefix}{i + 1}"),
                subtitle=str(q.get("subtitle")) if q.get("subtitle") else None,
                example=str(example) if example else None,
                box_height=_height_pt(q.get("box_height_cm")),
            ))
        else:
            items.append(QuestionItem(question=str(q), form_field_id=f"{prefix}{i + 1}"))
    return items


# --- Reports between carnets ---------------------------------------------------------

def _carnet_name(carnet):
    return "carnet de route" if carnet == PDFStyle.CARNET_ROUTE else f"carnet {carnet}"


@functools.lru_cache(maxsize=64)
def _file_carnet(path, mtime):
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("carnet")


@functools.lru_cache(maxsize=16)
def _file_data_pages(path, mtime):
    with open(path, encoding="utf-8") as f:
        return workbook_data_pages(WorkbookSpec.model_validate(json.load(f)))


def reference_data_pages(carnet):
    """
    Where each data id of a carnet's reference workbook (workbooks/, the file whose
    'carnet' is this one) is written: {data_id: page}. Empty when there is no such file.
    Cached until the file changes.
    """
    folder = spec_module.WORKBOOKS_DIR
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if name.endswith(".json") and _file_carnet(path, os.path.getmtime(path)) == carnet:
            return _file_data_pages(path, os.path.getmtime(path))
    return {}


def _origin(data_id, pages_of=None):
    """« carnet 4 · p. 12 », or « carnet 4 » when the page is unknown (pages_of: carnet -> {data_id: page})."""
    try:
        carnet = data_carnet(data_id)
    except (ValueError, IndexError):
        return ""
    page = (pages_of(carnet) if pages_of else {}).get(data_id)
    return f"{_carnet_name(carnet)} · p. {page}" if page else _carnet_name(carnet)


def _report_lines(items, page_idx, b_idx, pages_of):
    lines = []
    for k, item in enumerate(items or [], start=1):
        item = list(item) if isinstance(item, (list, tuple)) else [str(item)]
        item += [None] * (4 - len(item))
        label, data_id, field_id, height_cm = item[:4]
        lines.append((
            str(label or ""),
            _origin(data_id, pages_of) if data_id else "",
            str(field_id or f"p{page_idx}_report_{b_idx}_{k}"),
            min(_as_number(height_cm, 0), MAX_BLOCK_HEIGHT_CM) or None,
        ))
    return lines


def _add_block(layout, b_data, page_idx, b_idx, pages_of=None):
    """
    Adds one spec block to the page: one PageLayout.add_* call (see BlockSpec). pages_of
    resolves the origin of reports (carnet -> {data_id: page}); without it, a report
    names the carnet only.
    """
    b_type = b_data.get("type", "")

    def given(*keys):
        """The keyword arguments the block sets, in the PageLayout names."""
        return {k: b_data[k] for k in keys if b_data.get(k) is not None}

    if b_type == "callout":
        layout.add_callout(
            text=b_data.get("text", ""),
            title=b_data.get("title"),
            variant=b_data.get("variant") or "info",
            height=_height_pt(b_data.get("height_cm")),
        )
    elif b_type == "cards_grid":
        cards = b_data.get("cards") or b_data.get("items") or []
        if not cards:
            cards = [
                {"title": "1. Constat ou Observation clé", "subtitle": "Ce que vous avez perçu ou appris"},
                {"title": "2. Décision ou Piste d'action", "subtitle": "Ce que vous choisissez de poser"},
            ]
        cols = _as_number(b_data.get("columns"), 2, int)
        c_h = _height_pt(b_data.get("card_height_cm"))
        prefix = b_data.get("field_prefix") or f"p{page_idx}_g{b_idx}"
        layout.add_cards_grid(cards, columns=cols, card_height=c_h, field_prefix=prefix)
    elif b_type == "scale":
        min_val, max_val = _scale_bounds(b_data)
        layout.add_scale_gauge(
            label=b_data.get("label") or b_data.get("title") or "Évaluation :",
            min_val=min_val,
            max_val=max_val,
            min_label=b_data.get("min_label") or "",
            max_label=b_data.get("max_label") or "",
            field_id=b_data.get("field_id") or f"p{page_idx}_scale_{b_idx}",
        )
    elif b_type == "checklist":
        items = b_data.get("items") or b_data.get("checklist") or [
            "Premier point d'action posé",
            "Échange ou confirmation planifié",
            "Alignement personnel validé",
        ]
        cols = _as_number(b_data.get("columns"), 1, int)
        prefix = b_data.get("field_prefix") or f"p{page_idx}_chk_{b_idx}"
        layout.add_checklist(items, title=b_data.get("title"), columns=cols, field_prefix=prefix)
    elif b_type == "table":
        headers = b_data.get("headers")
        # 'columns' is also BlockSpec's int column count: only a list can stand in for headers
        if not headers and isinstance(b_data.get("columns"), list):
            headers = b_data["columns"]
        headers = headers or ["Critère / Thématique", "Observation terrain", "Impact & Décision"]
        rows = b_data.get("rows") or [
            ["1. Faisabilité & Cap", "Observations recueillies", "Maintenir"],
            ["2. Valeur & Adhésion", "Observations recueillies", "Ajuster"],
        ]
        widths = b_data.get("col_widths_cm")
        col_widths = [_length_pt(w, 0) for w in widths] if isinstance(widths, list) else None
        prefix = b_data.get("field_prefix") or f"p{page_idx}_tbl_{b_idx}"
        layout.add_table(headers, rows, col_widths=col_widths, field_prefix=prefix,
                         field_height=_height_pt(b_data.get("field_height_cm")))
    elif b_type == "stat_boxes":
        layout.add_stat_boxes(b_data.get("stats") or [])
    elif b_type == "question":
        q_text = b_data.get("question") or b_data.get("text", "")
        f_id = b_data.get("field_id") or f"p{page_idx}_q_{b_idx}"
        cfg = QuestionConfig(
            subtitle=b_data.get("subtitle"),
            example=b_data.get("example"),
            box_height=_height_pt(b_data.get("box_height_cm"), default=3.0 * cm),
        )
        layout.add_question_block(q_text, f_id, config=cfg)
    elif b_type == "text":
        cfg = TextConfig(
            style_choice=b_data.get("style") or "body",
            font_size=b_data.get("font_size"),
            color=_color(b_data.get("color")),
            spacing_after=_length_pt(b_data.get("spacing_after_cm"), 0.5 * cm),
            align=b_data.get("align") or "left",
        )
        layout.add_text(b_data.get("text", ""), config=cfg)
    elif b_type == "questions_group":
        kwargs = {}
        for key in ("min_box_height", "max_box_height", "safe_bottom_margin"):
            value = _length_pt(b_data.get(f"{key}_cm"))
            if value is not None:
                kwargs[key] = value
        layout.add_questions_group(_question_items(b_data.get("questions"), f"p{page_idx}_b{b_idx}_q"), **kwargs)
    elif b_type == "heading":
        layout.add_heading(b_data.get("text", ""), color=_color(b_data.get("color")), size=b_data.get("size"))
    elif b_type == "paragraphs":
        kwargs = given("size")
        if b_data.get("gap_cm") is not None:
            kwargs["gap"] = _length_pt(b_data["gap_cm"], 0.3 * cm)
        if b_data.get("spacing_after_cm") is not None:
            kwargs["spacing_after"] = _length_pt(b_data["spacing_after_cm"])
        layout.add_paragraphs([str(p) for p in b_data.get("items") or []], color=_color(b_data.get("color")),
                              **kwargs)
    elif b_type == "star_list":
        kwargs = given("size")
        if b_data.get("spacing_after_cm") is not None:
            kwargs["spacing_after"] = _length_pt(b_data["spacing_after_cm"])
        layout.add_star_list([str(p) for p in b_data.get("items") or []], **kwargs)
    elif b_type == "annotation":
        layout.add_annotation(b_data.get("text", ""), **given("arrow", "width_ratio"))
    elif b_type == "frise":
        layout.add_frise(b_data.get("steps") or [], start_label=b_data.get("start_label") or "",
                         end_label=b_data.get("end_label") or "")
    elif b_type == "fields_card":
        kwargs = given("title", "hint", "question_labels")
        if b_data.get("field_height_cm") is not None:
            kwargs["field_height"] = _height_pt(b_data["field_height_cm"], 0.85 * cm)
        layout.add_fields_card(b_data.get("rows") or [], color=_color(b_data.get("color")), **kwargs)
    elif b_type == "numbered_lines":
        kwargs = given("count", "start")
        if b_data.get("line_height_cm") is not None:
            kwargs["line_height"] = _height_pt(b_data["line_height_cm"], 0.8 * cm)
        layout.add_numbered_lines(b_data.get("cards") or [], **kwargs)
    elif b_type == "rating_grid":
        layout.add_rating_grid(
            b_data.get("items") or [],
            b_data.get("field_prefix") or f"p{page_idx}_rating_{b_idx}",
            values=b_data.get("values"),
            min_label=b_data.get("min_label") or "",
            max_label=b_data.get("max_label") or "",
            title=b_data.get("title"),
        )
    elif b_type == "info_cards":
        layout.add_info_cards(b_data.get("cards") or [], columns=_as_number(b_data.get("columns"), 2, int),
                              check_label=b_data.get("check_label"))
    elif b_type == "link_card":
        layout.add_link_card(b_data.get("title") or "", b_data.get("links") or [], color=_color(b_data.get("color")))
    elif b_type == "checklist_cards":
        layout.add_checklist_cards(
            b_data.get("groups") or [],
            columns=_as_number(b_data.get("columns"), 2, int),
            field_prefix=b_data.get("field_prefix") or f"p{page_idx}_chk_{b_idx}",
            item_columns=_as_number(b_data.get("item_columns"), 1, int),
        )
    elif b_type == "fill_in_card":
        kwargs = given("size")
        if b_data.get("field_height_cm") is not None:
            kwargs["field_height"] = _height_pt(b_data["field_height_cm"], 0.85 * cm)
        layout.add_fill_in_card(b_data.get("rows") or [], **kwargs)
    elif b_type == "life_line":
        layout.add_life_line(b_data.get("items") or [], headers=b_data.get("headers"),
                             field_prefix=b_data.get("field_prefix") or f"p{page_idx}_vie_{b_idx}")
    elif b_type == "tree_of_life":
        zones = [list(z) + [None] * (3 - len(z)) if isinstance(z, (list, tuple)) else [str(z), "", None]
                 for z in (b_data.get("items") or [])][:6]
        zones += [["", "", None]] * (6 - len(zones))
        zones = [[str(title or ""), str(hint or ""), field_id or f"p{page_idx}_arbre_{b_idx}_{k}"]
                 for k, (title, hint, field_id) in enumerate((z[:3] for z in zones), start=1)]
        layout.add_tree_of_life(zones, annotation=b_data.get("text"))
    elif b_type == "protocol":
        layout.add_protocol(b_data.get("text"))
    elif b_type == "anchor":
        layout.add_anchor(b_data.get("field_id") or f"p{page_idx}_ancrage_{b_idx}")
    elif b_type == "contrast_example":
        layout.add_contrast_example(
            b_data.get("surface") or "",
            b_data.get("exploitable") or b_data.get("text") or "",
            title=b_data.get("title"),
        )
    elif b_type == "energy":
        layout.add_energy_check(b_data.get("field_prefix") or f"p{page_idx}_meteo_{b_idx}")
    elif b_type == "report":
        layout.add_report(_report_lines(b_data.get("items"), page_idx, b_idx, pages_of), title=b_data.get("title"),
                          columns=_as_number(b_data.get("columns"), 1, int))
    elif b_type == "space":
        layout.add_space(_length_pt(b_data.get("height_cm"), 0))
    elif b_type == "page_break":
        layout.page_break()


def compile_workbook_from_spec(spec: WorkbookSpec, output_path=None) -> bytes:
    """
    Compiles a WorkbookSpec into a PDF: returns its bytes, or writes it to output_path
    (a file path) and returns None. Reports name the page of their data: in the reference
    workbook of the carnet it comes from, or in this document for its own data.
    """
    own = {}
    if spec.carnet is not None and any(
        data_carnet(item[1]) == spec.carnet
        for page in spec.pages for block in page.blocks or [] if block.type == "report"
        for item in block.items or []
    ):
        own = workbook_data_pages(spec)

    def pages_of(carnet):
        return own if carnet == spec.carnet else reference_data_pages(carnet)

    return _compile(spec, output_path, pages_of)[0]


def workbook_data_pages(spec: WorkbookSpec) -> dict:
    """Where each data id of the spec is written once compiled: {data_id: page}."""
    return _compile(spec, io.BytesIO(), None)[1]


def _compile(spec: WorkbookSpec, output_path, pages_of):
    """Compiles the spec; returns (PDF bytes or None, {data_id: page})."""
    # Gemini or the consultant may write emojis: ReportLab would drop them and leave gaps
    spec = _without_unsupported_glyphs(spec)
    data_pages = {}
    buffer = io.BytesIO() if output_path is None else None
    short_title = plain_title(spec.chapter_title).rstrip(".!?… ")
    # A carnet of the bilan shows « carnet N/7 »; other workbooks their folio, or their title
    folio = spec.folio or ("" if spec.carnet is not None else short_title)
    builder = DocumentBuilder(output_path=buffer or output_path, pastel=spec.pastel, folio=folio, carnet=spec.carnet)
    builder.set_title(spec.pdf_title or f"{short_title} - {spec.subtitle}")

    # Helper factories to avoid late-binding closure issues in loops
    def make_cover_renderer(page_obj):
        params = page_obj.params
        # 'subtitle' holds the carnet label, e.g. "Carnet 4 : Mon rapport à l'argent"
        label = str(params.get("subtitle") or f"Carnet {spec.chapter_num} : {spec.chapter_title}")
        number, name = split_chapter_label(label)
        if number is None and not params.get("subtitle"):
            number = spec.chapter_num
        number = params.get("number", params.get("num", number))
        title = str(params.get("cover_title") or params.get("heading") or as_title(name or spec.chapter_title))
        tagline = str(params.get("tagline") or params.get("title") or spec.subtitle or "")
        promise = params.get("promise") or params.get("promesse")
        eyebrow = params.get("eyebrow")
        return lambda c: create_cover_page(
            c, title, number=number, eyebrow=str(eyebrow) if eyebrow else None, tagline=tagline,
            promise=str(promise) if promise else None,
        )

    def make_summary_renderer(page_obj):
        # An explicit empty or null 'num' shows no number (a workbook outside the carnets)
        num = page_obj.params["num"] if "num" in page_obj.params else (spec.chapter_num or "1")
        num_str = "" if num is None else str(num)
        title = _title(page_obj.title or spec.chapter_title, "Au programme")
        # The summary intro is rendered as ReportLab markup: escape it so spec text
        # (LLM or user) cannot inject <img>/<a> tags or break the parser
        intro_text = _safe_markup(
            page_obj.params.get("intro_text")
            or page_obj.params.get("intro")
            or ""
        )
        raw_points = (
            page_obj.params.get("points")
            or page_obj.params.get("steps")
            or page_obj.params.get("items")
            or []
        )
        if isinstance(raw_points, dict):
            raw_points = list(raw_points.values())
        points_list = []
        for i, pt in enumerate(raw_points):
            if isinstance(pt, dict):
                lbl = str(pt.get("num") or pt.get("label") or f"{i+1}.")
                if not lbl.endswith("."):
                    lbl = f"{lbl}."
                title_part = str(pt.get("title") or pt.get("name") or "")
                desc_part = str(pt.get("desc") or pt.get("description") or pt.get("subtitle") or "")
                if title_part and desc_part:
                    full_desc = f"{title_part} : {desc_part}"
                else:
                    full_desc = title_part or desc_part or str(pt)
                points_list.append((lbl, full_desc))
            elif isinstance(pt, (list, tuple)):
                points_list.append(
                    (str(pt[0]) if len(pt) > 0 else f"{i+1}.", str(pt[1]) if len(pt) > 1 else "")
                )
            else:
                # A plain text is a whole exercise line (« Exercice 1 · … »)
                points_list.append(str(pt))
        params = page_obj.params
        duration = params.get("duration") or params.get("duree")
        split = params.get("split") or params.get("decoupage")
        return lambda c: create_standard_summary_page(
            c, num_str, title, intro_text, points_list,
            duration=str(duration) if duration else None, split=str(split) if split else None,
        )

    def make_recap_renderer(page_obj):
        questions = page_obj.params.get("questions") or page_obj.params.get("items") or []
        if isinstance(questions, dict):
            questions = list(questions.values())
        questions = [str(q.get("question") or q.get("text") or "") if isinstance(q, dict) else str(q)
                     for q in questions]
        return lambda c: create_standard_recap_page(
            c,
            page_obj.part_title if page_obj.part_title is not None else "Récapitulatif",
            page_obj.params.get("intro_text") or page_obj.params.get("intro"),
            questions,
        )

    def make_questions_renderer(page_obj, page_idx):
        def _render(c):
            layout = PageLayout(
                c,
                _title(page_obj.title, "Questions d'approfondissement"),
                config=LayoutConfig(
                    part_title=page_obj.part_title or _eyebrow(spec.chapter_num, page_obj.title, "Questions")
                ),
            )
            intro = page_obj.params.get("intro_text") or page_obj.params.get("intro")
            if intro:
                layout.add_text(
                    str(intro), config=TextConfig(spacing_after=0.4 * 28.35)
                )
            raw_questions = page_obj.params.get("questions") or page_obj.params.get("items") or []
            layout.add_questions_group(_question_items(raw_questions, f"p{page_idx}_q"))
            layout.render()

        return _render

    def make_meteo_renderer(page_obj, page_idx):
        return lambda c: create_standard_meteo_page(
            c,
            title=_title(page_obj.title, "Mon état d'esprit actuel."),
            part_title=page_obj.part_title or "1. MÉTÉO DU MOMENT",
            emotion_prompt=str(
                page_obj.params.get("emotion_prompt")
                or page_obj.params.get("weather_title")
                or "Aujourd'hui, je me sens :"
            ),
            energy_prompt=str(
                page_obj.params.get("energy_prompt")
                or page_obj.params.get("scale_title")
                or "Mon niveau d'énergie :"
            ),
            thought_prompt=str(
                page_obj.params.get("thought_prompt")
                or page_obj.params.get("notes_placeholder")
                or page_obj.params.get("prompt")
                or "Ce qui prend le plus de place dans ma tête :"
            ),
            field_prefix=str(page_obj.params.get("field_prefix", f"p{page_idx}_meteo")),
        )

    def make_quadrants_renderer(page_obj, page_idx):
        quads = (
            page_obj.params.get("quadrants")
            or page_obj.params.get("quadrants_data")
            or page_obj.params.get("axes")
            or page_obj.params.get("piliers")
        )
        if not quads and any(
            k in page_obj.params
            for k in ("top_left", "top_right", "bottom_left", "bottom_right")
        ):
            quads = [
                page_obj.params.get("top_left", {}),
                page_obj.params.get("top_right", {}),
                page_obj.params.get("bottom_left", {}),
                page_obj.params.get("bottom_right", {}),
            ]
        elif isinstance(quads, dict):
            quads = list(quads.values())

        return lambda c: create_standard_quadrants_page(
            c,
            title=_title(page_obj.title, "Ma vision à 360°."),
            part_title=page_obj.part_title,
            instruction=str(
                page_obj.params.get(
                    "instruction",
                    page_obj.params.get(
                        "subtitle",
                        "Instruction : Pour chaque domaine, écrivez votre aspiration principale.",
                    ),
                )
            ),
            quadrants_data=quads,
            field_prefix=str(page_obj.params.get("field_prefix", f"p{page_idx}_vision")),
        )

    def make_two_columns_renderer(page_obj, page_idx):
        rows = (
            page_obj.params.get("rows")
            or page_obj.params.get("rows_data")
            or page_obj.params.get("items")
        )
        if isinstance(rows, dict):
            rows = list(rows.values())

        return lambda c: create_standard_two_columns_page(
            c,
            title=_title(page_obj.title, "Du constat au levier."),
            part_title=page_obj.part_title,
            intro_text=page_obj.params.get("intro_text") or page_obj.params.get("intro"),
            col1_header=str(
                page_obj.params.get("col1_header")
                or page_obj.params.get("left_header")
                or "Situation / Défi"
            ),
            col2_header=str(
                page_obj.params.get("col2_header")
                or page_obj.params.get("right_header")
                or "Enseignement / Compétence"
            ),
            rows_data=rows,
            field_prefix=str(page_obj.params.get("field_prefix", f"p{page_idx}_twocol")),
        )

    def make_engagement_renderer(page_obj, page_idx):
        lines = (
            page_obj.params.get("lines")
            or page_obj.params.get("custom_lines")
            or page_obj.params.get("points")
            or page_obj.params.get("commitments")
            or page_obj.params.get("engagements")
        )
        if isinstance(lines, dict):
            lines = list(lines.values())

        sig_label = str(
            page_obj.params.get("signature_label")
            or page_obj.params.get("signature_text")
            or "Date de la séance"
        )
        params = page_obj.params
        livrable_title = params.get("livrable_title") or params.get("deliverable_title") or params.get("livrable")
        livrable_text = params.get("livrable_text") or params.get("deliverable_text") or params.get("deliverable")
        zones = params.get("zones")
        if isinstance(zones, dict):
            zones = list(zones.values())
        zones = [str(z) for z in zones] if isinstance(zones, list) else None
        return lambda c: create_standard_engagement_page(
            c,
            part_title=page_obj.part_title or "Fin de carnet",
            custom_lines=lines,
            title=_title(page_obj.title, "Votre livrable."),
            signature_label=sig_label,
            field_prefix=str(params.get("field_prefix", f"p{page_idx}_engagement")),
            livrable_title=str(livrable_title) if livrable_title else None,
            livrable_text=str(livrable_text) if livrable_text else None,
            zones=zones,
            pistes=params.get("pistes") is True,
        )

    def make_enquete_renderer(page_obj, page_idx):
        questions = (
            page_obj.params.get("questions")
            or page_obj.params.get("items")
        )
        if isinstance(questions, dict):
            questions = list(questions.values())

        return lambda c: create_standard_enquete_page(
            c,
            title=_title(page_obj.title, "Fiche enquête réseau et métier."),
            part_title=page_obj.part_title or "EXPLORATION DU TERRAIN",
            intro_text=page_obj.params.get("intro_text") or page_obj.params.get("intro"),
            questions=questions,
            field_prefix=str(page_obj.params.get("field_prefix", f"p{page_idx}_enquete")),
        )

    def make_roadmap_renderer(page_obj, page_idx):
        stages = (
            page_obj.params.get("stages")
            or page_obj.params.get("stages_data")
            or page_obj.params.get("paliers")
        )
        if isinstance(stages, dict):
            stages = list(stages.values())

        return lambda c: create_standard_roadmap_page(
            c,
            title=_title(page_obj.title, "Feuille de route à 30, 60 et 90 jours."),
            part_title=page_obj.part_title or "PLAN D'ACTION OPÉRATIONNEL",
            intro_text=page_obj.params.get("intro_text") or page_obj.params.get("intro"),
            stages_data=stages,
            field_prefix=str(page_obj.params.get("field_prefix", f"p{page_idx}_roadmap")),
        )

    def make_closing_renderer(page_obj):
        messages = (
            page_obj.params.get("messages")
            or page_obj.params.get("closing_messages")
        )
        if not messages and (
            page_obj.params.get("message") or page_obj.params.get("submessage")
        ):
            messages = [
                m
                for m in [
                    page_obj.params.get("message"),
                    page_obj.params.get("submessage"),
                ]
                if m
            ]
        return lambda c: create_closing_page(c, messages=messages)

    def make_composite_renderer(page_obj, page_idx=1):
        def _render(c):
            # An empty part_title means no eyebrow; a missing one gets « N. TITRE »
            part_title = page_obj.part_title
            if part_title is None:
                part_title = _eyebrow(spec.chapter_num, page_obj.title)
            layout = PageLayout(c, _title(page_obj.title), config=LayoutConfig(part_title=part_title))
            raw_blocks = getattr(page_obj, "blocks", None) or page_obj.params.get("blocks", [])
            for b_idx, block in enumerate(raw_blocks):
                if hasattr(block, "model_dump"):
                    b_data = block.model_dump(exclude_unset=True)
                    b_data.setdefault("type", block.type)
                else:
                    b_data = block if isinstance(block, dict) else {}
                layout.block_page = None
                _add_block(layout, b_data, page_idx, b_idx, pages_of)
                if b_data.get("data_id"):
                    data_pages.setdefault(b_data["data_id"], layout.block_page or c.getPageNumber())
            layout.render()

        return _render

    renderers = {
        "cover": lambda page, idx: make_cover_renderer(page),
        "summary": lambda page, idx: make_summary_renderer(page),
        "recap": lambda page, idx: make_recap_renderer(page),
        "questions": make_questions_renderer,
        "meteo": make_meteo_renderer,
        "quadrants": make_quadrants_renderer,
        "two_columns": make_two_columns_renderer,
        "engagement": make_engagement_renderer,
        "enquete": make_enquete_renderer,
        "roadmap": make_roadmap_renderer,
        "closing": lambda page, idx: make_closing_renderer(page),
        "composite": make_composite_renderer,
    }
    for page_idx, page in enumerate(spec.pages, start=1):
        if page.data_id:
            data_pages.setdefault(page.data_id, builder.canvas.getPageNumber())
        # Unknown templates fall back to a page of questions
        builder.add_page(renderers.get(page.template, make_questions_renderer)(page, page_idx))

    builder.save()
    if buffer is None:
        return None, data_pages
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes, data_pages


def build_reference_workbook(workbook_id, output_path):
    """Compiles the reference workbook workbooks/<workbook_id>.json into output_path (a path or a BytesIO)."""
    compile_workbook_from_spec(load_workbook(workbook_id), output_path)
