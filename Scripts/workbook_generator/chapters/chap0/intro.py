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
    draw_page_footer,

)
from workbook_generator.utils import cached_image_reader
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig


def create_cover_page(c):
    create_standard_cover(c, "CHAPITRE 0 : LE PRÉLUDE")


def create_summary_page(c):
    """Page: Au Programme."""
    intro_txt = (
        "Vous entamez aujourd’hui une démarche importante pour vous et votre avenir "
        "professionnel. Prendre le temps de s’arrêter, de réfléchir à ses besoins, à ses forces "
        "et à ses aspirations est un cadeau que l’on se fait. Ce parcours est pensé pour vous "
        "guider pas à pas vers plus de clarté et d’alignement."
    )
    items = [
        ("Le Prélude :", "Où j'en suis ? De quoi j'ai besoin ?"),
        ("Chapitre 1 :", "Définir son boussole, ses piliers et sa vision."),
        ("Chapitre 2 :", "Explorer son histoire et sa psychologie."),
        ("Chapitre 3 :", "Découvrir ses fonctionnements propres."),
        ("Chapitre 4 :", "Mettre en action et avancer."),
    ]

    layout = PageLayout(c, "Au Programme", config=LayoutConfig(part_title="INTRODUCTION"))
    layout.add_text(intro_txt)

    for title, subtitle in items:
        # Tweak the cursor to leave room for a small decorative box
        start_y = layout.y_cursor
        c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE, alpha=0.1)
        c.rect(layout.text_x, start_y - 1 * cm, 0.4 * cm, 1 * cm, fill=1, stroke=0)

        c.setFont(PDFStyle.FONT_BRANDING, 14)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(layout.text_x + 0.8 * cm, start_y - 0.5 * cm, title)

        c.setFont(PDFStyle.FONT_BODY, 11)
        c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
        c.drawString(layout.text_x + 0.8 * cm, start_y - 0.9 * cm, subtitle)

        layout.y_cursor -= 1.5 * cm

    layout.render()


def create_editorial_page_card(c):
    """Page: Édito avec carte."""
    width, height = A4

    # Background
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Central Card
    margin = 2 * cm
    card_width = width - (2 * margin)
    card_height = height - (3 * margin)
    card_x = margin
    card_y = 1.5 * margin

    # Draw Shadow
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_SHADOW)
    c.rect(
        card_x + 0.3 * cm,
        card_y - 0.3 * cm,
        card_width,
        card_height,
        fill=1,
        stroke=0,
    )
    c.restoreState()

    # Draw Main Card
    c.setFillColor(PDFStyle.COLOR_WHITE)
    c.rect(card_x, card_y, card_width, card_height, fill=1, stroke=0)
    c.setStrokeColor(PDFStyle.COLOR_LINE)
    c.setLineWidth(0.5)
    c.rect(card_x, card_y, card_width, card_height, fill=0, stroke=1)

    # Content Area
    content_x = card_x + 1.5 * cm
    content_y = card_y + card_height - 2 * cm
    content_w = card_width - 3 * cm

    c.setFont(PDFStyle.FONT_BRANDING, 22)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(content_x, content_y, "Le mot de l'équipe")
    content_y -= 1.5 * cm

    style_body = ParagraphStyle(
        "EditoBody",
        fontName=PDFStyle.FONT_BODY,
        fontSize=11,
        leading=16,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
    )

    text_blocks = [
        "Bienvenue dans ce parcours d'exploration.",
        "Nous avons conçu ce workbook comme un compagnon de route. Il n'est pas "
        "là pour vous donner des réponses toutes faites, mais pour vous aider à "
        "poser les bonnes questions.",
        "Prenez le temps. Ce n'est pas une course. Si une question vous bloque, "
        "laissez-la de côté et revenez-y plus tard. Votre rythme est le bon.",
        "Nous vous souhaitons une belle découverte de vous-même.",
    ]

    for block in text_blocks:
        p = Paragraph(block, style_body)
        w, h = p.wrap(content_w, height)
        p.drawOn(c, content_x, content_y - h)
        content_y -= h + 0.5 * cm

    # Signature
    signature_y = card_y + 2 * cm
    c.setFont(PDFStyle.FONT_BRANDING, 14)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawRightString(card_x + card_width - 1.5 * cm, signature_y, "L'équipe MDM")

    draw_page_footer(c, 3, width, height)
    c.showPage()


def create_intro_sense_page(c):
    """Page: Introduction 'Mettre du sens'."""
    layout = PageLayout(c, "Mettre du Sens", config=LayoutConfig(part_title="INTRODUCTION"))

    intro_txt = (
        "Mettre du sens dans sa vie professionnelle, ce n'est pas nécessairement "
        "sauver le monde. C'est trouver un alignement entre ce que l'on fait, "
        "ce que l'on est, et ce que l'on valorise."
    )
    layout.add_text(intro_txt, config=TextConfig(style_choice="italic", spacing_after=1*cm))

    items = [
        "1. Comprendre son fonctionnement personnel et professionnel.",
        "2. Identifier ses besoins profonds et ses valeurs motrices.",
        "3. Définir une vision claire de ce que l'on souhaite construire.",
        "4. Mettre en place des actions concrètes pour s'en approcher."
    ]

    for item in items:
        layout.add_text(item, config=TextConfig(spacing_after=0.5*cm))

    layout.render()


def create_form_page_card(c):
    """Page: Mon Engagement (Formulaire)."""
    width, height = A4
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    form = c.acroForm

    # Central Card
    margin = 2 * cm
    card_width = width - (2 * margin)
    card_height = height - (3 * margin)
    card_x = margin
    card_y = 1.5 * margin

    # Draw Shadow
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_SHADOW)
    c.rect(card_x + 0.3 * cm, card_y - 0.3 * cm, card_width, card_height, fill=1, stroke=0)
    c.restoreState()

    # Draw Main Card
    c.setFillColor(PDFStyle.COLOR_WHITE)
    c.rect(card_x, card_y, card_width, card_height, fill=1, stroke=0)
    c.setStrokeColor(PDFStyle.COLOR_LINE)
    c.setLineWidth(0.5)
    c.rect(card_x, card_y, card_width, card_height, fill=0, stroke=1)

    content_x = card_x + 1.5 * cm
    content_y = card_y + card_height - 2 * cm
    content_w = card_width - 3 * cm

    c.setFont(PDFStyle.FONT_BRANDING, 22)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(content_x, content_y, "Mon Engagement")
    content_y -= 1.5 * cm

    intro_txt = (
        "Je m'engage à être honnête envers moi-même tout au long de ce parcours, "
        "à m'accorder le temps nécessaire pour la réflexion, et à accueillir "
        "mes découvertes avec bienveillance."
    )

    style_body = ParagraphStyle(
        "EngBody",
        fontName=PDFStyle.FONT_BODY,
        fontSize=11,
        leading=16,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
        alignment=TA_JUSTIFY,
    )
    p = Paragraph(intro_txt, style_body)
    w, h = p.wrap(content_w, height)
    p.drawOn(c, content_x, content_y - h)
    content_y -= h + 2 * cm

    # Form Fields
    c.setFont(PDFStyle.FONT_BODY, 11)
    c.drawString(content_x, content_y, "Fait à :")
    create_input_field(
        form,
        "s0_engagement_lieu",
        pos=(content_x + 1.5 * cm, content_y - 0.1 * cm),
        size=(6 * cm, 0.6 * cm),
    )

    c.drawString(content_x + 8 * cm, content_y, "Le :")
    create_input_field(
        form,
        "s0_engagement_date",
        pos=(content_x + 9 * cm, content_y - 0.1 * cm),
        size=(4 * cm, 0.6 * cm),
    )

    content_y -= 1.5 * cm
    c.drawString(content_x, content_y, "Signature :")
    create_input_field(
        form,
        "s0_engagement_signature",
        pos=(content_x + 2 * cm, content_y - 1 * cm),
        size=(10 * cm, 2 * cm),
        multiline=True,
    )

    draw_page_footer(c, 5, width, height)
    c.showPage()
