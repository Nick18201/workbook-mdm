"""
Compiles a WorkbookSpec (JSON) into PDF bytes in-memory using ReportLab templates.
"""

import io
import os
import sys

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
    create_standard_cover,
    create_standard_summary_page,
    create_standard_meteo_page,
    create_standard_quadrants_page,
    create_standard_two_columns_page,
    create_standard_engagement_page,
    create_standard_enquete_page,
    create_standard_roadmap_page,
    create_closing_page,
)
from .models import WorkbookSpec


def compile_workbook_from_spec(spec: WorkbookSpec) -> bytes:
    """
    Compiles a WorkbookSpec object into in-memory PDF bytes.
    """
    buffer = io.BytesIO()
    builder = DocumentBuilder(output_path=buffer, theme=spec.theme)
    builder.set_title(f"{spec.chapter_title} - {spec.subtitle}")

    # Helper factories to avoid late-binding closure issues in loops
    def make_cover_renderer(page_obj):
        subtitle = str(
            page_obj.params.get(
                "subtitle", f"Chapitre {spec.chapter_num} : {spec.chapter_title}"
            )
            or f"Chapitre {spec.chapter_num} : {spec.chapter_title}"
        )
        title = str(
            page_obj.params.get("title", spec.subtitle)
            or spec.subtitle
            or "BILAN DE COMPÉTENCES & ALIGNEMENT"
        )
        return lambda c: create_standard_cover(c, subtitle=subtitle, title=title)

    def make_summary_renderer(page_obj):
        num_str = str(page_obj.params.get("num") or spec.chapter_num or "1")
        title = str(page_obj.title or spec.chapter_title or "SOMMAIRE")
        intro_text = str(
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
                points_list.append((f"{i+1}.", str(pt)))
        return lambda c: create_standard_summary_page(
            c, num_str, title, intro_text, points_list
        )

    def make_questions_renderer(page_obj):
        def _render(c):
            layout = PageLayout(
                c,
                page_obj.title or "Questions d'Approfondissement",
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
                                or f"p{spec.chapter_num}_q{i+1}"
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
                            form_field_id=f"p{spec.chapter_num}_q{i+1}",
                        )
                    )
            layout.add_questions_group(q_items)
            layout.render()

        return _render

    def make_meteo_renderer(page_obj):
        return lambda c: create_standard_meteo_page(
            c,
            title=page_obj.title or "Mon État d'Esprit Actuel",
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
            field_prefix=str(page_obj.params.get("field_prefix", "meteo")),
        )

    def make_quadrants_renderer(page_obj):
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
            title=page_obj.title or "Ma Vision 360°",
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
            field_prefix=str(page_obj.params.get("field_prefix", "vision")),
        )

    def make_two_columns_renderer(page_obj):
        rows = (
            page_obj.params.get("rows")
            or page_obj.params.get("rows_data")
            or page_obj.params.get("items")
        )
        if isinstance(rows, dict):
            rows = list(rows.values())

        return lambda c: create_standard_two_columns_page(
            c,
            title=page_obj.title or "Passerelle : Du Constat au Levier",
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
            field_prefix=str(page_obj.params.get("field_prefix", "twocol")),
        )

    def make_engagement_renderer(page_obj):
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
            or "Date et Signature :"
        )
        return lambda c: create_standard_engagement_page(
            c,
            part_title=page_obj.part_title or "MON ENGAGEMENT",
            custom_lines=lines,
            title=page_obj.title or "Mon Engagement",
            signature_label=sig_label,
        )

    def make_enquete_renderer(page_obj):
        questions = (
            page_obj.params.get("questions")
            or page_obj.params.get("items")
        )
        if isinstance(questions, dict):
            questions = list(questions.values())

        return lambda c: create_standard_enquete_page(
            c,
            title=page_obj.title or "Fiche Enquête Réseau & Métier",
            part_title=page_obj.part_title or "EXPLORATION DU TERRAIN",
            intro_text=page_obj.params.get("intro_text") or page_obj.params.get("intro"),
            questions=questions,
            field_prefix=str(page_obj.params.get("field_prefix", "enquete")),
        )

    def make_roadmap_renderer(page_obj):
        stages = (
            page_obj.params.get("stages")
            or page_obj.params.get("stages_data")
            or page_obj.params.get("paliers")
        )
        if isinstance(stages, dict):
            stages = list(stages.values())

        return lambda c: create_standard_roadmap_page(
            c,
            title=page_obj.title or "Feuille de Route 30 · 60 · 90 Jours",
            part_title=page_obj.part_title or "PLAN D'ACTION OPÉRATIONNEL",
            intro_text=page_obj.params.get("intro_text") or page_obj.params.get("intro"),
            stages_data=stages,
            field_prefix=str(page_obj.params.get("field_prefix", "roadmap")),
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
                page_obj.title,
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
                    cols = b_data.get("columns", 2)
                    c_h = (
                        (b_data.get("card_height_cm") * 28.3465)
                        if b_data.get("card_height_cm")
                        else None
                    )
                    prefix = b_data.get("field_prefix") or f"p{page_idx}_g{b_idx}"
                    layout.add_cards_grid(
                        cards, columns=cols, card_height=c_h, field_prefix=prefix
                    )
                elif b_type == "scale":
                    layout.add_scale_gauge(
                        label=b_data.get("label") or b_data.get("title") or "Évaluation :",
                        min_val=b_data.get("min_val", 0),
                        max_val=b_data.get("max_val", 10),
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
                    cols = b_data.get("columns", 1)
                    title = b_data.get("title")
                    prefix = b_data.get("field_prefix") or f"p{page_idx}_chk_{b_idx}"
                    layout.add_checklist(
                        items, title=title, columns=cols, field_prefix=prefix
                    )
                elif b_type == "table":
                    headers = b_data.get("headers") or b_data.get("columns") or [
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
                    b_h = (
                        (b_data.get("box_height_cm") * 28.3465)
                        if b_data.get("box_height_cm")
                        else (3.0 * 28.3465)
                    )
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
            builder.add_page(make_questions_renderer(page))
        elif tmpl == "meteo":
            builder.add_page(make_meteo_renderer(page))
        elif tmpl == "quadrants":
            builder.add_page(make_quadrants_renderer(page))
        elif tmpl == "two_columns":
            builder.add_page(make_two_columns_renderer(page))
        elif tmpl == "engagement":
            builder.add_page(make_engagement_renderer(page))
        elif tmpl == "enquete":
            builder.add_page(make_enquete_renderer(page))
        elif tmpl == "roadmap":
            builder.add_page(make_roadmap_renderer(page))
        elif tmpl == "closing":
            builder.add_page(make_closing_renderer(page))
        elif tmpl == "composite":
            builder.add_page(make_composite_renderer(page, page_idx))
        else:
            # Fallback to questions if unspecified
            builder.add_page(make_questions_renderer(page))

    builder.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
