import os
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.components import cached_image_reader
from .common import setup_programme_page


def create_programme_page_tarifs(c):
    """
    Page 7 : Formule & Financement.
    - Sous-titre : « Une formule unique, finançable par le CPF »
    - Formule unique : 1 800 € net de taxes, « 10 séances individuelles + suivi à 6 mois, 13 h »
    - Inclusions : 7 carnets de bord, espace Notion, copilote IA, questionnaire MBTI® officiel
    - Prise en charge CPF jusqu'à 1 600 € et reste à charge 200 €
    - Mention Qualiopi : BILANS DE COMPÉTENCES
    - Participation forfaitaire 150 € comprise dans les 200 €
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Formule & Financement",
        subtitle="Une formule unique, finançable par le CPF",
        page_num=10,
        total_pages=12,
        topic="Tarifs et Financements",
    )

    # -------------------------------------------------------------------------
    # 1. GRANDE CARTE : LA FORMULE UNIQUE (1 800 €)
    # -------------------------------------------------------------------------
    card1_h = 8.8 * cm
    c.saveState()

    # Fond de carte blanc avec bordure soignée
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.2)
    c.roundRect(content_x, y_cursor - card1_h, content_w, card1_h, 8, fill=1, stroke=1)

    # Pastille en haut "FORMULE UNIQUE ⭐"
    badge_w = 4.2 * cm
    badge_h = 0.75 * cm
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.roundRect(content_x + (content_w - badge_w) / 2.0, y_cursor - 0.40 * cm, badge_w, badge_h, 4, fill=1, stroke=0)
    c.setFont(PDFStyle.FONT_TITLE, 8.0)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.drawCentredString(content_x + content_w / 2.0, y_cursor - 0.16 * cm, "FORMULE UNIQUE")

    # Titre de la formule
    c.setFont(PDFStyle.FONT_TITLE, 14.0)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawCentredString(content_x + content_w / 2.0, y_cursor - 1.25 * cm, "Le Bilan de Compétences Marge de Manœuvre")

    # Format & Volume horaire
    c.setFont(PDFStyle.FONT_BODY, 9.5)
    c.setFillColor(colors.HexColor("#4B5563"))
    c.drawCentredString(
        content_x + content_w / 2.0,
        y_cursor - 1.80 * cm,
        "10 séances individuelles en visio + entretien de suivi à 6 mois (45 min), soit 13 h d'accompagnement",
    )

    # Bloc Prix central mis en valeur
    price_box_y = y_cursor - 3.70 * cm
    price_box_h = 1.65 * cm
    c.setFillColor(colors.HexColor("#F9FAFB"))
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.roundRect(content_x + 2.0 * cm, price_box_y, content_w - 4.0 * cm, price_box_h, 6, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_BRANDING, 22)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawCentredString(content_x + content_w / 2.0, price_box_y + 0.65 * cm, "1 800 €")

    c.setFont(PDFStyle.FONT_BODY, 8.2)
    c.setFillColor(colors.HexColor("#6B7280"))
    c.drawCentredString(
        content_x + content_w / 2.0,
        price_box_y + 0.22 * cm,
        "Net de taxes (TVA non applicable, art. 293 B du CGI)",
    )

    # Inclusions complètes
    inclus_y = price_box_y - 0.50 * cm
    c.setFont(PDFStyle.FONT_TITLE, 9.0)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(content_x + 0.8 * cm, inclus_y, "🎁 INCLUS DANS CET ACCOMPAGNEMENT :")

    style_inclus = ParagraphStyle(
        "TarifInclus",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.6,
        leading=12.5,
        textColor=colors.HexColor("#374151"),
    )
    txt_inclus = (
        "• <b>7 carnets de bord guidés</b> (vous les gardez définitivement)<br/>"
        "• <b>L'espace Notion de ressources</b> accessible jusqu'au suivi à 6 mois<br/>"
        "• <b>Le copilote IA</b> dédié pour challenger et nourrir vos réflexions<br/>"
        "• <b>Le questionnaire MBTI® officiel</b> et sa restitution approfondie"
    )
    p_inclus = Paragraph(txt_inclus, style_inclus)
    p_inclus.wrap(content_w - 1.6 * cm, 2.5 * cm)
    p_inclus.drawOn(c, content_x + 0.8 * cm, inclus_y - p_inclus.height - 0.25 * cm)

    c.restoreState()
    y_cursor -= card1_h + 0.55 * cm

    # -------------------------------------------------------------------------
    # 2. CARTE FINANCEMENT CPF & QUALIOPI
    # -------------------------------------------------------------------------
    card2_h = 10.8 * cm
    c.saveState()

    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(content_x, y_cursor - card2_h, content_w, card2_h, 8, fill=1, stroke=1)

    # Titre section financement
    c.setFont(PDFStyle.FONT_TITLE, 11.5)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawCentredString(
        content_x + content_w / 2.0, y_cursor - 0.70 * cm, "Comment financer votre bilan de compétences ?"
    )

    # Paragraphe explicatif Qualiopi et CPF
    style_fin = ParagraphStyle(
        "FinText",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.6,
        leading=12.8,
        textColor=colors.HexColor("#374151"),
        alignment=1,  # Centré
    )
    txt_fin = (
        "En tant qu'<b>organisme certifié Qualiopi</b>, nos parcours répondent aux normes d'exigence de l'État.<br/>"
        "<b>Le CPF finance jusqu'à 1 600 € :</b> avec un solde suffisant, <b>il vous reste 200 € à charge</b>, "
        "quel que soit votre statut. Votre employeur, votre OPCO ou France Travail peuvent également les prendre en charge."
    )
    p_fin = Paragraph(txt_fin, style_fin)
    p_fin.wrap(content_w - 1.4 * cm, 3.0 * cm)
    p_fin.drawOn(c, content_x + 0.7 * cm, y_cursor - 1.05 * cm - p_fin.height)

    # Logos partenaires (CPF, France Travail, Qualiopi)
    logo_bar_y = y_cursor - 1.05 * cm - p_fin.height - 1.8 * cm
    logo_gap = 1.0 * cm
    col_logo_w = (content_w - 2 * logo_gap) / 3.0

    logos_to_draw = [
        {"path": PDFStyle.PATH_LOGO_CPF, "label": "CPF (MonCompteFormation)"},
        {"path": PDFStyle.PATH_LOGO_FRANCE_TRAVAIL, "label": "France Travail"},
        {"path": PDFStyle.PATH_LOGO_QUALIOPI, "label": "Qualiopi Certifié"},
    ]

    for i, lg in enumerate(logos_to_draw):
        lx = content_x + i * (col_logo_w + logo_gap)
        if os.path.exists(lg["path"]):
            try:
                reader = cached_image_reader(lg["path"])
                c.drawImage(
                    reader,
                    lx + (col_logo_w - 3.0 * cm) / 2.0,
                    logo_bar_y,
                    width=3.0 * cm,
                    height=1.25 * cm,
                    preserveAspectRatio=True,
                    anchor="c",
                )
            except Exception:
                pass
        c.setFont(PDFStyle.FONT_BODY, 7.5)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawCentredString(lx + col_logo_w / 2.0, logo_bar_y - 0.35 * cm, lg["label"])

    # Séparation discrète
    sep_y = logo_bar_y - 0.70 * cm
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.6)
    c.line(content_x + 1.0 * cm, sep_y, content_x + content_w - 1.0 * cm, sep_y)

    # Mentions légales obligatoires Qualiopi et Décret
    style_leg = ParagraphStyle(
        "LegalFin",
        fontName=PDFStyle.FONT_BODY,
        fontSize=7.8,
        leading=11.2,
        textColor=colors.HexColor("#64748B"),
        alignment=1,  # Centré
    )
    txt_leg = (
        "« <i>La certification qualité a été délivrée au titre de la catégorie d'action suivante : "
        "<b>BILANS DE COMPÉTENCES</b>.</i> »<br/><br/>"
        "<b>Participation forfaitaire :</b> La participation forfaitaire de 150 € (décret n° 2024-394, "
        "montant porté à 150 € au 1er avril 2026 par le décret n° 2026-234) "
        "<b>est comprise dans les 200 € : elle ne s'ajoute pas</b>."
    )
    p_leg = Paragraph(txt_leg, style_leg)
    p_leg.wrap(content_w - 1.6 * cm, 3.5 * cm)
    p_leg.drawOn(c, content_x + 0.8 * cm, sep_y - p_leg.height - 0.30 * cm)

    c.restoreState()
    c.showPage()
