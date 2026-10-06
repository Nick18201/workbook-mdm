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
    draw_branding_logo,
)


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


def setup_programme_page(
    c,
    title="Votre parcours d'accompagnement",
    subtitle="Un parcours structuré en séances individuelles",
    page_num=2,
    total_pages=8,
    topic="Programme du bilan",
    card_margin=2.0 * cm,
):
    """
    Configure une page du Programme de Bilan de Compétences :
    - Fond Nude officiel, Dot Grid et subtiles vagues
    - Signature marginale verticale 'm a r g e   d e   m a n œ u v r e' dans la marge gauche
    - Panneau latéral blanc/crème avec ombre douce
    - En-tête professionnel : Titre de section à gauche, Marque et catégorie à droite
    - Pied de page normalisé : « margedemanoeuvre.fr • {topic} » à gauche, « Page {page_num} / {total_pages} » à droite
    """
    ensure_montserrat_family()
    width, height = A4

    # 1. Fond Nude et signature marginale
    draw_page_background(c, width, height, use_blobs=False)

    # 2. Grand panneau latéral blanc/crème
    draw_side_panel(c, card_margin, width, height)

    # 3. Zone de contenu intérieur
    content_x = card_margin + 0.9 * cm
    content_w = width - card_margin - 1.8 * cm

    # 4. En-tête de page
    header_top_y = height - 1.35 * cm
    c.saveState()

    # Gauche : Titre et sous-titre
    c.setFont(PDFStyle.FONT_TITLE, 14.5)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(content_x, header_top_y, title)

    if subtitle:
        c.setFont(PDFStyle.FONT_BODY, 9.2)
        c.setFillColor(colors.HexColor("#6B7280"))
        c.drawString(content_x, header_top_y - 0.48 * cm, subtitle)

    # Droite : Branding "marge de manœuvre" + "LE PROGRAMME"
    c.setFont(PDFStyle.FONT_BRANDING, 11)
    c.setFillColor(colors.HexColor("#1F2937"))
    c.drawRightString(width - 1.2 * cm, header_top_y, "marge de manœuvre")

    c.setFont(PDFStyle.FONT_TITLE, 7.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawRightString(width - 1.2 * cm, header_top_y - 0.42 * cm, "LE PROGRAMME")

    # Ligne de séparation en-tête
    sep_y = header_top_y - 0.85 * cm
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.7)
    c.line(content_x, sep_y, width - 1.2 * cm, sep_y)
    c.restoreState()

    # 5. Pied de page normalisé (sans tiret dans margedemanoeuvre.fr)
    footer_y = 1.25 * cm
    c.saveState()
    # Ligne fine au-dessus du footer
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.7)
    c.line(content_x, footer_y + 0.45 * cm, width - 1.2 * cm, footer_y + 0.45 * cm)

    # Texte gauche
    c.setFont(PDFStyle.FONT_BODY, 8.2)
    c.setFillColor(colors.HexColor("#6B7280"))
    c.drawString(content_x, footer_y, f"margedemanoeuvre.fr • {topic}")

    # Numérotation droite
    c.setFont(PDFStyle.FONT_BODY, 8.2)
    c.setFillColor(colors.HexColor("#6B7280"))
    c.drawRightString(width - 1.2 * cm, footer_y, f"Page {page_num} / {total_pages}")
    c.restoreState()

    # Curseur Y de départ sous l'en-tête
    start_y = sep_y - 0.50 * cm
    return content_x, content_w, start_y


def draw_session_card(c, x, y, w, h, badge, title, description, objective, is_followup=False):
    """
    Dessine une carte de séance pédagogique harmonisée et lisible :
    - Badge stylisé à gauche (ex: S1, S2, Suivi)
    - Titre en gras
    - Description détaillée
    - Objectif clé dans un sous-bloc dédié en bas de carte
    """
    c.saveState()

    # Fond de carte arrondi
    bg_col = colors.HexColor("#FFFFFF") if not is_followup else colors.HexColor("#EFF6FF")
    border_col = colors.HexColor("#E5E7EB") if not is_followup else colors.HexColor("#BFDBFE")
    c.setFillColor(bg_col)
    c.setStrokeColor(border_col)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    # Badge séance à gauche
    badge_w = 1.05 * cm if not is_followup else 1.55 * cm
    badge_h = 0.85 * cm
    badge_x = x + 0.45 * cm
    badge_y = y + h - badge_h - 0.45 * cm

    badge_bg = PDFStyle.COLOR_ACCENT_RED if not is_followup else PDFStyle.COLOR_ACCENT_BLUE
    c.setFillColor(badge_bg)
    c.roundRect(badge_x, badge_y, badge_w, badge_h, 4, fill=1, stroke=0)

    c.setFont(PDFStyle.FONT_TITLE, 9.5 if not is_followup else 8.0)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.drawCentredString(badge_x + badge_w / 2.0, badge_y + 0.24 * cm, badge)

    # Zone de texte à droite du badge
    text_x = badge_x + badge_w + 0.45 * cm
    text_w = w - (text_x - x) - 0.45 * cm

    # Titre de la séance
    c.setFont(PDFStyle.FONT_TITLE, 10.0)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(text_x, y + h - 0.68 * cm, title)

    # Description (Paragraph avec wrap)
    style_desc = ParagraphStyle(
        "CardDesc",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.6,
        leading=12.4,
        textColor=colors.HexColor("#374151"),
    )
    p_desc = Paragraph(description, style_desc)
    avail_h = h - 2.0 * cm
    p_desc.wrap(text_w, avail_h)
    p_desc.drawOn(c, text_x, y + h - 0.95 * cm - p_desc.height)

    # Bloc Objectif stylisé en bas de carte
    obj_box_h = 0.80 * cm
    obj_box_y = y + 0.35 * cm
    c.setFillColor(colors.HexColor("#F9FAFB") if not is_followup else colors.HexColor("#DBEAFE"))
    c.setStrokeColor(colors.HexColor("#E5E7EB") if not is_followup else colors.HexColor("#BFDBFE"))
    c.setLineWidth(0.6)
    c.roundRect(text_x, obj_box_y, text_w, obj_box_h, 4, fill=1, stroke=1)

    accent_hex = PDFStyle.COLOR_ACCENT_BLUE.hexval() if hasattr(PDFStyle.COLOR_ACCENT_BLUE, "hexval") else "2F2EFA"
    if not accent_hex.startswith("#"):
        accent_hex = f"#{accent_hex}"

    style_obj = ParagraphStyle(
        "CardObj",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.2,
        leading=11.2,
        textColor=colors.HexColor(accent_hex),
    )
    txt_obj = f"<b><font color='#6B7280'>OBJECTIF :</font></b> {objective}"
    p_obj = Paragraph(txt_obj, style_obj)
    p_obj.wrap(text_w - 0.4 * cm, obj_box_h)
    p_obj.drawOn(c, text_x + 0.25 * cm, obj_box_y + (obj_box_h - p_obj.height) / 2.0)

    c.restoreState()


def draw_deliverables_card(c, x, y, w, h, title, items):
    """
    Dessine un encadré récapitulatif des livrables validés à la fin d'un temps.
    """
    c.saveState()
    # Fond doux teinté
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    # Accent latéral rouge
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.rect(x, y + 3, 3, h - 6, fill=1, stroke=0)

    # Titre des livrables
    c.setFont(PDFStyle.FONT_TITLE, 8.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(x + 0.6 * cm, y + h - 0.60 * cm, title)

    # Puces des livrables
    item_y = y + h - 0.95 * cm
    style_item = ParagraphStyle(
        "DelivItem",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.3,
        leading=11.6,
        textColor=colors.HexColor("#1F2937"),
    )

    for item in items:
        p = Paragraph(f"• <b>{item}</b>", style_item)
        p.wrap(w - 1.2 * cm, 1.0 * cm)
        p.drawOn(c, x + 0.6 * cm, item_y - p.height)
        item_y -= p.height + 0.15 * cm

    c.restoreState()


def create_closing_page(c):
    """Page de fin optionnelle."""
    width, height = A4
    draw_page_background(c, width, height)

    logo_x = width / 2
    logo_y = height / 2 + 2 * cm
    draw_branding_logo(c, logo_x, logo_y, size=40, align="center")

    text_y = logo_y - 4 * cm
    c.setFont(PDFStyle.FONT_TITLE, 14)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)

    messages = [
        "Merci pour votre confiance.",
        "Prenez contact pour démarrer votre bilan :",
        "margedemanoeuvre.fr • contact@margedemanoeuvre.fr",
    ]

    for msg in messages:
        c.drawCentredString(width / 2, text_y, msg)
        text_y -= 0.9 * cm

    c.showPage()
