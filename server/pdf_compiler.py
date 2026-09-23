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
        subtitle = page_obj.params.get(
            "subtitle", f"Chapitre {spec.chapter_num} : {spec.chapter_title}"
        )
        title = page_obj.params.get("title", spec.subtitle)
        return lambda c: create_standard_cover(c, subtitle=subtitle, title=title)

    def make_summary_renderer(page_obj):
        num_str = str(page_obj.params.get("num", spec.chapter_num))
        title = page_obj.title
        intro_text = page_obj.params.get("intro_text", "")
        raw_points = page_obj.params.get("points", [])
        points_list = []
        for pt in raw_points:
            if isinstance(pt, dict):
                points_list.append((pt.get("label", ""), pt.get("desc", "")))
            elif isinstance(pt, (list, tuple)):
                points_list.append((str(pt[0]), str(pt[1]) if len(pt) > 1 else ""))
            else:
                points_list.append(str(pt))
        return lambda c: create_standard_summary_page(
            c, num_str, title, intro_text, points_list
        )

    def make_questions_renderer(page_obj):
        def _render(c):
            layout = PageLayout(
                c,
                page_obj.title,
                config=LayoutConfig(
                    part_title=page_obj.part_title
                    or f"{spec.chapter_num}. {page_obj.title.upper()}"
                ),
            )
            intro = page_obj.params.get("intro_text")
            if intro:
                layout.add_text(
                    intro, config=TextConfig(spacing_after=0.4 * 28.35)
                )

            raw_questions = page_obj.params.get("questions", [])
            q_items = []
            for i, q in enumerate(raw_questions):
                if isinstance(q, dict):
                    q_items.append(
                        QuestionItem(
                            question=q.get("question", ""),
                            form_field_id=q.get("field_id")
                            or f"p{spec.chapter_num}_q{i+1}",
                            subtitle=q.get("subtitle"),
                            example=q.get("example"),
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
            title=page_obj.title,
            part_title=page_obj.part_title,
            emotion_prompt=page_obj.params.get(
                "emotion_prompt", "Aujourd'hui, je me sens :"
            ),
            energy_prompt=page_obj.params.get(
                "energy_prompt", "Mon niveau d'énergie :"
            ),
            thought_prompt=page_obj.params.get(
                "thought_prompt", "Ce qui prend le plus de place dans ma tête :"
            ),
            field_prefix=page_obj.params.get("field_prefix", "meteo"),
        )

    def make_quadrants_renderer(page_obj):
        quads = page_obj.params.get("quadrants") or page_obj.params.get(
            "quadrants_data"
        )
        return lambda c: create_standard_quadrants_page(
            c,
            title=page_obj.title,
            part_title=page_obj.part_title,
            instruction=page_obj.params.get(
                "instruction",
                "Instruction : Pour chaque domaine, écrivez votre aspiration principale.",
            ),
            quadrants_data=quads,
            field_prefix=page_obj.params.get("field_prefix", "vision"),
        )

    def make_two_columns_renderer(page_obj):
        rows = page_obj.params.get("rows") or page_obj.params.get("rows_data")
        return lambda c: create_standard_two_columns_page(
            c,
            title=page_obj.title,
            part_title=page_obj.part_title,
            intro_text=page_obj.params.get("intro_text"),
            col1_header=page_obj.params.get("col1_header", "Situation / Défi"),
            col2_header=page_obj.params.get(
                "col2_header", "Enseignement / Compétence"
            ),
            rows_data=rows,
            field_prefix=page_obj.params.get("field_prefix", "twocol"),
        )

    def make_engagement_renderer(page_obj):
        return lambda c: create_standard_engagement_page(
            c,
            part_title=page_obj.part_title or "MON ENGAGEMENT",
            custom_lines=page_obj.params.get("lines"),
            title=page_obj.title,
            signature_label=page_obj.params.get(
                "signature_label", "Date et Signature :"
            ),
        )

    def make_enquete_renderer(page_obj):
        return lambda c: create_standard_enquete_page(
            c,
            title=page_obj.title or "Fiche Enquête Réseau & Métier",
            part_title=page_obj.part_title or "EXPLORATION DU TERRAIN",
            intro_text=page_obj.params.get("intro_text"),
            questions=page_obj.params.get("questions"),
            field_prefix=page_obj.params.get("field_prefix", "enquete"),
        )

    def make_roadmap_renderer(page_obj):
        return lambda c: create_standard_roadmap_page(
            c,
            title=page_obj.title or "Feuille de Route 30 · 60 · 90 Jours",
            part_title=page_obj.part_title or "PLAN D'ACTION OPÉRATIONNEL",
            intro_text=page_obj.params.get("intro_text"),
            stages_data=page_obj.params.get("stages") or page_obj.params.get("stages_data"),
            field_prefix=page_obj.params.get("field_prefix", "roadmap"),
        )

    def make_closing_renderer(page_obj):
        return lambda c: create_closing_page(c)

    def make_composite_renderer(page_obj):
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
                    cards = b_data.get("cards", [])
                    cols = b_data.get("columns", 2)
                    c_h = (
                        (b_data.get("card_height_cm") * 28.3465)
                        if b_data.get("card_height_cm")
                        else None
                    )
                    prefix = b_data.get("field_prefix", f"grid_{b_idx}")
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
                        field_id=b_data.get("field_id", f"scale_{b_idx}"),
                    )
                elif b_type == "checklist":
                    items = b_data.get("items", [])
                    cols = b_data.get("columns", 1)
                    title = b_data.get("title")
                    prefix = b_data.get("field_prefix", f"chk_{b_idx}")
                    layout.add_checklist(
                        items, title=title, columns=cols, field_prefix=prefix
                    )
                elif b_type == "table":
                    headers = b_data.get("headers", [])
                    rows = b_data.get("rows", [])
                    prefix = b_data.get("field_prefix", f"tbl_{b_idx}")
                    layout.add_table(headers, rows, field_prefix=prefix)
                elif b_type == "stat_boxes":
                    stats = b_data.get("stats", [])
                    layout.add_stat_boxes(stats)
                elif b_type == "question":
                    q_text = b_data.get("question") or b_data.get("text", "")
                    f_id = b_data.get("field_id", f"q_{b_idx}")
                    b_h = (
                        (b_data.get("box_height_cm") * 28.3465)
                        if b_data.get("box_height_cm")
                        else None
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
    for page in spec.pages:
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
            builder.add_page(make_composite_renderer(page))
        else:
            # Fallback to questions if unspecified
            builder.add_page(make_questions_renderer(page))

    builder.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
