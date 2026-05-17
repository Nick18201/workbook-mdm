import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.forms import create_input_field
from workbook_generator.components import (
    create_standard_cover,
    draw_title,
    draw_page_decorations,
    draw_side_panel,

)
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig


def create_chap1_cover(c):
    """
    Cover Page for Chapter 1: L'État des Lieux.
    """
    create_standard_cover(
        c,
        "CHAPITRE 1",
        "L'État des Lieux",
        "Où j'en suis ? De quoi j'ai besoin ?",
        PDFStyle.COLOR_ACCENT_BLUE,
    )


def create_engagement_page(c):
    """
    Page 1: Mon Engagement.
    """
    layout = PageLayout(c, "Mon Engagement", config=LayoutConfig(part_title="INTRODUCTION"))

    intro_txt = (
        "Vous entamez aujourd'hui une démarche importante pour vous et votre avenir "
        "professionnel. Ce parcours est pensé pour vous "
        "guider pas à pas vers plus de clarté et d'alignement."
    )
    layout.add_text(intro_txt, config=TextConfig(spacing_after=1.0 * cm))

    layout.add_question_block(
        "Ce que j'attends de ce bilan :",
        "engagement_attentes",
        config=QuestionConfig(
            box_height=4 * cm,
            subtitle="(Clarté, confiance, nouveau départ...)",
        ),
    )

    layout.add_question_block(
        "Je m'engage vis-à-vis de moi-même à :",
        "engagement_moi_meme",
        config=QuestionConfig(
            box_height=4 * cm,
            subtitle="(Être honnête, prendre le temps, ne pas me juger...)",
        ),
    )

    layout.render()


def create_concept_page(c):
    """
    Page 2: Chapter Cover - 1. Concept
    """
    width, height = A4
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Title
    c.setFont(PDFStyle.FONT_BRANDING, 36)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(2 * cm, height - 3 * cm, "1. L'État des Lieux")

    # Subtitle
    c.setFont(PDFStyle.FONT_SUBTITLE, 18)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(2 * cm, height - 4.5 * cm, "Faire le point sur son point de départ.")

    # Body
    text_content = [
        "Sommaire :",
        "- Ma Météo Intérieure",
        "- Ma Vision 'Boule à Facettes'",
        "- Mon Objectif Boussole",
        "- Le Sac à Dos",
        "- Mon Héritage (3FVS)",
        "- Image du Monde du Travail",
        "- Mentors & Anti-Modèles",
    ]

    text_y = height - 6.5 * cm
    for i, line in enumerate(text_content):
        if i == 0:
            c.setFont(PDFStyle.FONT_SUBTITLE, 14)
            c.drawString(2 * cm, text_y, line)
            text_y -= 1.0 * cm
            c.setFont(PDFStyle.FONT_BODY, 12)
        else:
            c.drawString(2.5 * cm, text_y, line)
            text_y -= 0.7 * cm

    c.showPage()
