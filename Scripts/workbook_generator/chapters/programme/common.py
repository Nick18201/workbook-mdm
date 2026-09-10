import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.fonts import addMapping

from workbook_generator.config import PDFStyle
from workbook_generator.components import (
    draw_page_background,
    draw_side_panel,
    draw_page_header,
    draw_page_footer,
    draw_title,
    TitleStyle,
    create_standard_cover,
    draw_branding_logo,
)


def create_programme_cover(c):
    """Couverture officielle du Programme conforme à la charte des Workbooks."""
    create_standard_cover(
        c,
        subtitle="PROGRAMME DÉTAILLÉ & MÉTHODE",
        title="BILAN DE COMPÉTENCES & ALIGNEMENT",
    )


def create_programme_closing_page(c):
    """Page de fin dédiée au Programme — texte neutre et professionnel."""
    width, height = A4
    draw_page_background(c, width, height)

    # Logo centré
    logo_x = width / 2
    logo_y = height / 2 + 2 * cm
    draw_branding_logo(c, logo_x, logo_y, size=40, align="center")

    # Texte neutre adapté au programme
    text_y = logo_y - 4 * cm
    c.setFont(PDFStyle.FONT_TITLE, 14)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)

    messages = [
        "Merci pour votre attention.",
        "Pour toute question, n'hésitez pas à nous contacter.",
    ]

    for msg in messages:
        c.drawCentredString(width / 2, text_y, msg)
        text_y -= 1.0 * cm

    c.showPage()


# Alias pour compatibilité avec l'import existant
create_closing_page = create_programme_closing_page


def ensure_montserrat_family():
    """Assure le mapping des variantes bold et italic pour Montserrat dans ReportLab."""
    try:
        addMapping("montserrat", 0, 0, "Montserrat-Regular")
        addMapping("montserrat", 1, 0, "Montserrat-Bold")
        addMapping("montserrat", 0, 1, "Montserrat-Italic")
        addMapping("montserrat", 1, 1, "Montserrat-Bold")
        addMapping("montserrat-regular", 0, 0, "Montserrat-Regular")
        addMapping("montserrat-regular", 1, 0, "Montserrat-Bold")
        addMapping("montserrat-regular", 0, 1, "Montserrat-Italic")
        addMapping("montserrat-regular", 1, 1, "Montserrat-Bold")
    except Exception:
        pass


def setup_workbook_programme_page(c, part_title="BILAN DE COMPÉTENCES"):
    """
    Configure la page dans le respect strict de la charte graphique des Workbooks :
    - Fond Nude + Dot Grid + Vagues subtiles
    - Signature marginale verticale 'm a r g e   d e   m a n œ u v r e' dans la bande gauche
    - Panneau latéral Crème (Side Panel) avec ombre portée douce
    - En-tête officiel : Logo Marge de Manœuvre à gauche, Titre de partie à droite en rouge
    - Pied de page officiel : Numéro de page centré en rouge
    """
    ensure_montserrat_family()
    width, height = A4
    card_margin = 2.0 * cm

    # 1. Fond Nude et signature marginale
    draw_page_background(c, width, height, use_blobs=False)

    # 2. Grand panneau latéral crème
    draw_side_panel(c, card_margin, width, height)

    # 3. En-tête (Logo + Part Title)
    draw_page_header(c, part_title, width, height, x_offset=card_margin)

    # 4. Pied de page (numérotation commençant à 1 sur la première page de contenu)
    c.saveState()
    raw_page = c.getPageNumber()
    content_page_num = max(1, raw_page - 1)
    c.setFont(PDFStyle.FONT_TITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    content_area_center = card_margin + (width - card_margin) / 2.0
    c.drawCentredString(content_area_center, 1.5 * cm, str(content_page_num))
    c.restoreState()

    text_x = card_margin + 1.0 * cm  # 3.0 cm
    target_width = width - card_margin - 2.0 * cm  # ~17.1 cm
    start_y = height - 3.8 * cm

    return text_x, target_width, start_y


def draw_workbook_highlight_box(
    c,
    x,
    y,
    w,
    h,
    prefix="👉 NOTRE SPÉCIFICITÉ :",
    text="",
    accent_color=PDFStyle.COLOR_ACCENT_RED,
    bg_color=PDFStyle.COLOR_FIELD_BG,
    font_size=9.5,
    leading=13.5,
):
    """Dessine un bloc de mise en avant avec le fond caractéristique des workbooks."""
    c.saveState()
    # Fond doux arrondi
    c.setFillColor(bg_color)
    c.setStrokeColor(accent_color)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    # Barre latérale gauche accentuée
    c.setFillColor(accent_color)
    c.rect(x, y + 4, 4, h - 8, fill=1, stroke=0)

    # Texte formaté
    color_hex = (
        accent_color.hexval()
        if hasattr(accent_color, "hexval")
        else "#FF4D4D"
    )
    if not color_hex.startswith("#"):
        color_hex = f"#{color_hex}"

    style = ParagraphStyle(
        "HighlightStyle",
        fontName=PDFStyle.FONT_BODY,
        fontSize=font_size,
        leading=leading,
        textColor=colors.HexColor("#2C2C2C"),
    )
    full_html = f"<b><font color='{color_hex}'>{prefix}</font></b> {text}"
    p = Paragraph(full_html, style)
    p.wrap(w - 0.8 * cm, h)
    p.drawOn(c, x + 0.5 * cm, y + (h - p.height) / 2.0)
    c.restoreState()


def get_workbook_styles():
    """Styles typographiques standardisés conformes aux workbooks."""
    return {
        "title_h1": TitleStyle(size=20, color=PDFStyle.COLOR_ACCENT_BLUE),
        "subtitle": TitleStyle(size=12, color=PDFStyle.COLOR_ACCENT_BLUE),
        "body": ParagraphStyle(
            "WkBody",
            fontName=PDFStyle.FONT_BODY,
            fontSize=9.8,
            leading=14.2,
            textColor=PDFStyle.COLOR_TEXT_MAIN,
        ),
        "body_dark": ParagraphStyle(
            "WkBodyDark",
            fontName=PDFStyle.FONT_BODY,
            fontSize=9.8,
            leading=14.2,
            textColor=colors.HexColor("#222222"),
        ),
        "body_italic": ParagraphStyle(
            "WkBodyItalic",
            fontName=PDFStyle.FONT_BODY,
            fontSize=9.5,
            leading=13.8,
            textColor=colors.HexColor("#555555"),
        ),
        "bullet": ParagraphStyle(
            "WkBullet",
            fontName=PDFStyle.FONT_BODY,
            fontSize=9.5,
            leading=13.6,
            textColor=colors.HexColor("#222222"),
        ),
        # --- Styles harmonisés pour les cartes du programme ---
        "card_item": ParagraphStyle(
            "WkCardItem",
            fontName=PDFStyle.FONT_BODY,
            fontSize=9.0,
            leading=13.4,
            textColor=colors.HexColor("#222222"),
        ),
        "card_item_small": ParagraphStyle(
            "WkCardItemSmall",
            fontName=PDFStyle.FONT_BODY,
            fontSize=8.8,
            leading=12.8,
            textColor=colors.HexColor("#222222"),
        ),
    }

