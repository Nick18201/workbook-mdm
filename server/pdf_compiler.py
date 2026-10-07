"""
Compiles a WorkbookSpec (JSON) into PDF bytes in-memory using ReportLab templates.
"""

import io
import os
import sys
from xml.sax.saxutils import escape

# Ensure Scripts/ is accessible in Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "Scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from workbook_generator import (
    DocumentBuilder,
    PageLayout,
    LayoutConfig,
    QuestionItem,
    QuestionConfig,
    TextConfig,
    create_cover_page,
    create_standard_summary_page,
    create_standard_meteo_page,
    create_standard_quadrants_page,
    create_standard_two_columns_page,
    create_standard_engagement_page,
    create_standard_enquete_page,
    create_standard_roadmap_page,
    create_closing_page,
)
from workbook_generator.components import as_title, split_chapter_label
from workbook_generator.primitives import plain_title
from workbook_generator.utils import strip_unsupported_glyphs
from .models import MAX_SCALE_STEPS, WorkbookSpec

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
    return min(height_cm, MAX_BLOCK_HEIGHT_CM) * 28.3465


def _scale_bounds(b_data):
    low = _as_number(b_data.get("min_val"), 0, int)
    high = _as_number(b_data.get("max_val"), 10, int)
    if not 0 < high - low <= MAX_SCALE_STEPS:
        return 0, 10
    return low, high


def _title(text, default=""):
    """A page title as shown: an all-caps title from the spec is set in sentence case."""
    text = " ".join(str(text or default).split())
    return text[:1] + text[1:].lower() if text.isupper() else text


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

    return WorkbookSpec.model_validate(clean(spec.model_dump()))


def compile_workbook_from_spec(spec: WorkbookSpec) -> bytes:
    """
    Compiles a WorkbookSpec object into in-memory PDF bytes.
    """
    # Gemini or the coach may write emojis: ReportLab would drop them and leave gaps
    spec = _without_unsupported_glyphs(spec)
    buffer = io.BytesIO()
    # Generated workbooks are not numbered core workbooks: the folio shows their title
    builder = DocumentBuilder(output_path=buffer, folio=plain_title(spec.chapter_title))
    builder.set_title(f"{spec.chapter_title} - {spec.subtitle}")

    # Helper factories to avoid late-binding closure issues in loops
    def make_cover_renderer(page_obj):
        params = page_obj.params
        # 'subtitle' holds the chapter label, e.g. "Chapitre 4 : Mon rapport à l'argent"
        label = str(params.get("subtitle") or f"Chapitre {spec.chapter_num} : {spec.chapter_title}")
        number, name = split_chapter_label(label)
        if number is None and not params.get("subtitle"):
            number = spec.chapter_num
        number = params.get("number", params.get("num", number))
        title = str(params.get("cover_title") or params.get("heading") or as_title(name or spec.chapter_title))
        tagline = str(params.get("title") or spec.subtitle or "")
        promise = params.get("promise") or params.get("promesse") or params.get("tagline")
        return lambda c: create_cover_page(
            c, title, number=number, tagline=tagline, promise=str(promise) if promise else None
        )

    def make_summary_renderer(page_obj):
        num_str = str(page_obj.params.get("num") or spec.chapter_num or "1")
        title = _title(page_obj.title or spec.chapter_title, "Au programme")
        # The summary intro is rendered as ReportLab markup: escape it so spec text
        # (LLM or user) cannot inject <img>/<a> tags or break the parser
        intro_text = escape(str(
            page_obj.params.get("intro_text")
            or page_obj.params.get("intro")
            or ""
        ))
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
                points_list.append((f"{i+1}.", str(pt)))
        return lambda c: create_standard_summary_page(
            c, num_str, title, intro_text, points_list
        )

    def make_questions_renderer(page_obj, page_idx):
        def _render(c):
            layout = PageLayout(
                c,
                _title(page_obj.title, "Questions d'approfondissement"),
                config=LayoutConfig(
                    part_title=page_obj.part_title
                    or f"{spec.chapter_num}. {(page_obj.title or 'QUESTIONS').upper()}"
                ),
            )
            intro = page_obj.params.get("intro_text") or page_obj.params.get("intro")
            if intro:
                layout.add_text(
                    str(intro), config=TextConfig(spacing_after=0.4 * 28.35)
                )

            raw_questions = (
                page_obj.params.get("questions")
                or page_obj.params.get("items")
                or []
            )
            if isinstance(raw_questions, dict):
                raw_questions = list(raw_questions.values())
            q_items = []
            for i, q in enumerate(raw_questions):
                if isinstance(q, dict):
                    q_text = (
                        q.get("question")
                        or q.get("text")
                        or q.get("title")
                        or q.get("label")
                        or f"Question {i+1}"
                    )
                    q_items.append(
                        QuestionItem(
                            question=str(q_text),
                            form_field_id=str(
                                q.get("field_id")
                                or f"p{page_idx}_q{i+1}"
                            ),
                            subtitle=str(q.get("subtitle")) if q.get("subtitle") else None,
                            example=str(q.get("example") or q.get("ex")) if (q.get("example") or q.get("ex")) else None,
                            color=q.get("color"),
                        )
                    )
                else:
                    q_items.append(
                        QuestionItem(
                            question=str(q),
                            form_field_id=f"p{page_idx}_q{i+1}",
                        )
                    )
            layout.add_questions_group(q_items)
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
        return lambda c: create_standard_engagement_page(
            c,
            part_title=page_obj.part_title or "Fin de carnet",
            custom_lines=lines,
            title=_title(page_obj.title, "Votre livrable."),
            signature_label=sig_label,
            field_prefix=str(params.get("field_prefix", f"p{page_idx}_engagement")),
            livrable_title=str(livrable_title) if livrable_title else None,
            livrable_text=str(livrable_text) if livrable_text else None,
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
            layout = PageLayout(
                c,
                _title(page_obj.title),
                config=LayoutConfig(
                    part_title=page_obj.part_title
                    or f"{spec.chapter_num}. {page_obj.title.upper()}"
                ),
            )
            raw_blocks = getattr(page_obj, "blocks", None) or page_obj.params.get("blocks", [])
            for b_idx, block in enumerate(raw_blocks):
                b_data = (
                    block.model_dump()
                    if hasattr(block, "model_dump")
                    else (
                        block.dict()
                        if hasattr(block, "dict")
                        else (block if isinstance(block, dict) else {})
                    )
                )
                b_type = b_data.get("type", "")

                if b_type == "callout":
                    layout.add_callout(
                        text=b_data.get("text", ""),
                        title=b_data.get("title"),
                        variant=b_data.get("variant", "info"),
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
                    layout.add_cards_grid(
                        cards, columns=cols, card_height=c_h, field_prefix=prefix
                    )
                elif b_type == "scale":
                    min_val, max_val = _scale_bounds(b_data)
                    layout.add_scale_gauge(
                        label=b_data.get("label") or b_data.get("title") or "Évaluation :",
                        min_val=min_val,
                        max_val=max_val,
                        min_label=b_data.get("min_label", ""),
                        max_label=b_data.get("max_label", ""),
                        field_id=b_data.get("field_id") or f"p{page_idx}_scale_{b_idx}",
                    )
                elif b_type == "checklist":
                    items = b_data.get("items") or b_data.get("checklist") or [
                        "Premier point d'action posé",
                        "Échange ou confirmation planifié",
                        "Alignement personnel validé"
                    ]
                    cols = _as_number(b_data.get("columns"), 1, int)
                    title = b_data.get("title")
                    prefix = b_data.get("field_prefix") or f"p{page_idx}_chk_{b_idx}"
                    layout.add_checklist(
                        items, title=title, columns=cols, field_prefix=prefix
                    )
                elif b_type == "table":
                    headers = b_data.get("headers")
                    # 'columns' is also BlockSpec's int column count: only a list can stand in for headers
                    if not headers and isinstance(b_data.get("columns"), list):
                        headers = b_data["columns"]
                    headers = headers or [
                        "Critère / Thématique",
                        "Observation terrain",
                        "Impact & Décision"
                    ]
                    rows = b_data.get("rows") or [
                        ["1. Faisabilité & Cap", "Observations recueillies", "Maintenir"],
                        ["2. Valeur & Adhésion", "Observations recueillies", "Ajuster"],
                    ]
                    prefix = b_data.get("field_prefix") or f"p{page_idx}_tbl_{b_idx}"
                    layout.add_table(headers, rows, field_prefix=prefix)
                elif b_type == "stat_boxes":
                    stats = b_data.get("stats", [])
                    layout.add_stat_boxes(stats)
                elif b_type == "question":
                    q_text = b_data.get("question") or b_data.get("text", "")
                    f_id = b_data.get("field_id") or f"p{page_idx}_q_{b_idx}"
                    b_h = _height_pt(b_data.get("box_height_cm"), default=3.0 * 28.3465)
                    cfg = QuestionConfig(
                        subtitle=b_data.get("subtitle"),
                        example=b_data.get("example"),
                        box_height=b_h,
                    )
                    layout.add_question_block(q_text, f_id, config=cfg)
                elif b_type == "text":
                    layout.add_text(b_data.get("text", ""))

            layout.render()

        return _render

    # Route each page to its renderer
    for page_idx, page in enumerate(spec.pages, start=1):
        tmpl = page.template
        if tmpl == "cover":
            builder.add_page(make_cover_renderer(page))
        elif tmpl == "summary":
            builder.add_page(make_summary_renderer(page))
        elif tmpl == "questions":
            builder.add_page(make_questions_renderer(page, page_idx))
        elif tmpl == "meteo":
            builder.add_page(make_meteo_renderer(page, page_idx))
        elif tmpl == "quadrants":
            builder.add_page(make_quadrants_renderer(page, page_idx))
        elif tmpl == "two_columns":
            builder.add_page(make_two_columns_renderer(page, page_idx))
        elif tmpl == "engagement":
            builder.add_page(make_engagement_renderer(page, page_idx))
        elif tmpl == "enquete":
            builder.add_page(make_enquete_renderer(page, page_idx))
        elif tmpl == "roadmap":
            builder.add_page(make_roadmap_renderer(page, page_idx))
        elif tmpl == "closing":
            builder.add_page(make_closing_renderer(page))
        elif tmpl == "composite":
            builder.add_page(make_composite_renderer(page, page_idx))
        else:
            # Fallback to questions if unspecified
            builder.add_page(make_questions_renderer(page, page_idx))

    builder.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
