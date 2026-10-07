import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.components import (
    draw_page_background,
    draw_dot_grid,
    draw_branding_logo,
    cached_image_reader,
)
from .common import ensure_montserrat_family


def create_programme_cover(c):
    """
    Page 1 : Couverture officielle du Programme de Bilan de Compétences.
    Conforme aux directives :
    - « conçu par une psychologue du travail et un consultant en transformation »
    - « Bilans de compétences » dans l'encadré Qualiopi
    - « 100 % à distance, en visio, partout en France »
    - Pied de page : « margedemanoeuvre.fr • contact@margedemanoeuvre.fr »
    """
    ensure_montserrat_family()
    width, height = A4

    # 1. Fond Nude élégant + Grille de points
    draw_page_background(c, width, height, use_blobs=False)

    # 1b. Bande latérale gauche distinctive
    band_w = 1.6 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.rect(0, 0, band_w, height, fill=1, stroke=0)

    # Signature marginale verticale dans la bande gauche
    c.translate(0.95 * cm, height / 2.0)
    c.rotate(90)
    c.setFont(PDFStyle.FONT_BODY, 8)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.drawCentredString(0, 0, "m a r g e   d e   m a n œ u v r e")
    c.restoreState()

    content_x = band_w + 1.6 * cm
    content_w = width - band_w - 3.2 * cm

    # 2. En-tête de la couverture
    logo_y = height - 2.8 * cm
    draw_branding_logo(c, content_x, logo_y, size=32)

    # Badge "BILAN DE COMPÉTENCES" en haut à droite
    badge_w = 4.8 * cm
    badge_h = 0.85 * cm
    badge_x = width - 1.6 * cm - badge_w
    badge_y = logo_y - 0.15 * cm

    c.saveState()
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.0)
    c.roundRect(badge_x, badge_y, badge_w, badge_h, 12, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 8.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawCentredString(
        badge_x + badge_w / 2.0, badge_y + 0.26 * cm, "BILAN DE COMPÉTENCES"
    )
    c.restoreState()

    # 3. Hero central
    y_hero = height - 7.5 * cm

    # Petit accent décoratif rouge
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.roundRect(content_x, y_hero, 2.5 * cm, 0.18 * cm, 2, fill=1, stroke=0)
    c.restoreState()
    y_hero -= 1.0 * cm

    # Grand Titre
    c.saveState()
    c.setFont(PDFStyle.FONT_BRANDING, 28)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(content_x, y_hero, "Votre Bilan de")
    y_hero -= 1.15 * cm

    c.setFont(PDFStyle.FONT_BRANDING, 32)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(content_x, y_hero, "Compétences")
    y_hero -= 1.15 * cm

    c.setFont(PDFStyle.FONT_BRANDING, 28)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(content_x, y_hero, "sur-mesure")
    c.restoreState()
    y_hero -= 1.4 * cm

    # Paragraphe de sous-titre
    txt_intro = (
        "Un accompagnement individuel <b>conçu par une psychologue du travail et un consultant "
        "en transformation</b> pour repenser sereinement votre vie professionnelle."
    )
    style_intro = ParagraphStyle(
        "CoverIntro",
        fontName=PDFStyle.FONT_BODY,
        fontSize=11.0,
        leading=16.5,
        textColor=colors.HexColor("#374151"),
    )
    p_intro = Paragraph(txt_intro, style_intro)
    p_intro.wrap(content_w, 4 * cm)
    p_intro.drawOn(c, content_x, y_hero - p_intro.height)
    y_hero -= p_intro.height + 0.9 * cm

    # Mention "100 % à distance, en visio, partout en France"
    pill_w = content_w
    pill_h = 1.15 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(content_x, y_hero - pill_h, pill_w, pill_h, 6, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 10.0)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(content_x + 0.5 * cm, y_hero - 0.72 * cm, "100 % à distance, en visio, partout en France")
    c.restoreState()
    y_hero -= pill_h + 1.4 * cm

    # 4. Encadré Qualiopi
    box_q_w = content_w
    box_q_h = 4.2 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.setLineWidth(1.0)
    c.roundRect(content_x, y_hero - box_q_h, box_q_w, box_q_h, 8, fill=1, stroke=1)

    # Intérieur encadré Qualiopi
    q_pad = 0.6 * cm
    has_logo_q = os.path.exists(PDFStyle.PATH_LOGO_QUALIOPI)

    if has_logo_q:
        try:
            reader_q = cached_image_reader(PDFStyle.PATH_LOGO_QUALIOPI)
            c.drawImage(
                reader_q,
                content_x + q_pad,
                y_hero - box_q_h + q_pad,
                width=3.2 * cm,
                height=box_q_h - 2 * q_pad,
                preserveAspectRatio=True,
                anchor="w",
            )
        except Exception:
            has_logo_q = False

    text_q_x = content_x + (4.2 * cm if has_logo_q else q_pad)
    text_q_w = box_q_w - (4.4 * cm if has_logo_q else 2 * q_pad)

    # Titre badge
    c.setFont(PDFStyle.FONT_TITLE, 8.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(text_q_x, y_hero - 0.95 * cm, "ORGANISME CERTIFIÉ QUALIOPI")

    # Catégorie officielle
    c.setFont(PDFStyle.FONT_BRANDING, 13)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(text_q_x, y_hero - 1.65 * cm, "Bilans de compétences")

    # Mention détaillée
    txt_q_legal = (
        "La certification qualité a été délivrée au titre de la catégorie d'action suivante : "
        "<b>BILANS DE COMPÉTENCES</b>. Processus certifié par la République Française."
    )
    style_q_legal = ParagraphStyle(
        "QualiopiLegal",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor("#64748B"),
    )
    p_ql = Paragraph(txt_q_legal, style_q_legal)
    p_ql.wrap(text_q_w, 2.2 * cm)
    p_ql.drawOn(c, text_q_x, y_hero - box_q_h + 0.45 * cm)
    c.restoreState()

    # 5. Pied de page Couverture
    footer_y = 1.35 * cm
    c.saveState()
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.7)
    c.line(content_x, footer_y + 0.45 * cm, width - 1.6 * cm, footer_y + 0.45 * cm)

    c.setFont(PDFStyle.FONT_BODY, 8.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(content_x, footer_y, "margedemanoeuvre.fr • contact@margedemanoeuvre.fr")

    c.drawRightString(width - 1.6 * cm, footer_y, "Document d'information 2026")
    c.restoreState()

    c.showPage()
