from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.components import draw_title, TitleStyle
from .common import (
    setup_workbook_programme_page,
    get_workbook_styles,
)


def create_programme_page_4(c):
    """Page 4 : 4. Modalités Financières (CPF), Inscription & Contact."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="MODALITÉS & INSCRIPTION"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE H1 : 4. MODALITÉS FINANCIÈRES & INSCRIPTION
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "4. Modalités Financières & Inscription",
        pos=(text_x, y_cursor),
        available_width=target_width,
        style=TitleStyle(size=18, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    y_cursor -= 0.20 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Financement à 100%, démarches administratives simplifiées et accompagnement",
    )
    y_cursor -= 0.65 * cm

    # -------------------------------------------------------------------------
    # 2. BLOC FINANCEMENT CPF (ENCADRÉ DÉDIÉ)
    # -------------------------------------------------------------------------
    cpf_card_h = 2.5 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(
        text_x, y_cursor - cpf_card_h, target_width, cpf_card_h, 8, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_TITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + 0.5 * cm,
        y_cursor - 0.55 * cm,
        "Financement CPF (Compte Personnel de Formation) :",
    )

    style_cpf = ParagraphStyle(
        "CpfStyleWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=12.6,
        textColor=colors.HexColor("#222222"),
    )

    txt_cpf = (
        "· <b>Tous nos formats sont 100% finançables</b> par votre Compte Personnel de Formation (CPF).<br/>"
        "· <b>Reste à charge zéro</b> si votre solde CPF est suffisant (hors participation forfaitaire "
        "obligatoire de 102,23 € en vigueur depuis mai 2024, applicable sauf exceptions)."
    )
    p_cpf = Paragraph(txt_cpf, style_cpf)
    p_cpf.wrap(target_width - 1.0 * cm, 1.8 * cm)
    p_cpf.drawOn(c, text_x + 0.5 * cm, y_cursor - 0.72 * cm - p_cpf.height)
    c.restoreState()

    y_cursor -= cpf_card_h + 0.85 * cm

    # -------------------------------------------------------------------------
    # 3. AUTRES FINANCEMENTS POSSIBLES
    # -------------------------------------------------------------------------
    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, y_cursor, "Autres financements possibles :")
    y_cursor -= 0.45 * cm

    autres_financements = [
        (
            "Plan de développement des compétences",
            "Prise en charge intégrale ou partielle par votre employeur.",
        ),
        (
            "Financement OPCO",
            "Pour les indépendants, professions libérales et chefs d'entreprise.",
        ),
        (
            "Financement personnel",
            "Facilités de paiement en 3 à 4 fois sans frais.",
        ),
    ]

    for titre_f, desc_f in autres_financements:
        txt_f = f"<b><font color='#2F2EFA'>· {titre_f} :</font></b> {desc_f}"
        p_f = Paragraph(txt_f, styles["bullet"])
        p_f.wrap(target_width, 2 * cm)
        p_f.drawOn(c, text_x, y_cursor - p_f.height)
        y_cursor -= p_f.height + 0.30 * cm

    y_cursor -= 0.55 * cm

    # -------------------------------------------------------------------------
    # 4. DÉLAI D'ACCÈS, INSCRIPTION & ACCESSIBILITÉ
    # -------------------------------------------------------------------------
    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(text_x, y_cursor, "Délai d'accès et inscription :")
    y_cursor -= 0.45 * cm

    delais_items = [
        (
            "Inscription possible toute l'année",
            "Entrées et sorties permanentes selon vos disponibilités.",
        ),
        (
            "Premier entretien préalable d'information gratuit",
            "Échange téléphonique ou visio de 30 à 45 min sans engagement.",
        ),
        (
            "Démarrage sous 14 jours ouvrés",
            "Après validation de votre dossier CPF (respect du délai légal de rétractation).",
        ),
        (
            "Accessibilité handicap",
            "Parcours adaptable aux personnes en situation de handicap (nous contacter pour étudier les aménagements nécessaires).",
        ),
    ]

    for titre_d, desc_d in delais_items:
        txt_d = f"<b><font color='#2F2EFA'>· {titre_d} :</font></b> {desc_d}"
        p_d = Paragraph(txt_d, styles["bullet"])
        p_d.wrap(target_width, 2 * cm)
        p_d.drawOn(c, text_x, y_cursor - p_d.height)
        y_cursor -= p_d.height + 0.30 * cm

    y_cursor -= 0.70 * cm

    # -------------------------------------------------------------------------
    # 5. GRAND ENCADRÉ CONTACT & ÉCHANGE GRATUIT
    # -------------------------------------------------------------------------
    contact_box_h = 3.8 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.2)
    c.roundRect(
        text_x, y_cursor - contact_box_h, target_width, contact_box_h, 8, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_BRANDING, 14.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + 0.5 * cm,
        y_cursor - 0.75 * cm,
        "« Prêt(e) à faire le point ? Échangeons ensemble ! »",
    )

    c.setFont(PDFStyle.FONT_BODY, 9.2)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawString(
        text_x + 0.5 * cm,
        y_cursor - 1.25 * cm,
        "Premier entretien préalable d'information gratuit et sans engagement (30 à 45 min).",
    )

    style_details = ParagraphStyle(
        "ContactDetailsWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.2,
        leading=14.0,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
    )
    txt_details = (
        "<b>Cabinet Marge de Manœuvre</b> — <b>Lysiane Brand</b><br/>"
        "Consultante en évolution professionnelle & psychologue du travail<br/>"
        "📞 <b>06 74 55 20 22</b>   ·   ✉️ <b>contact@margedemanœuvre.fr</b>   ·   🌐 <b>margedemanoeuvre.fr</b>"
    )
    p_det = Paragraph(txt_details, style_details)
    p_det.wrap(target_width - 1.0 * cm, 2 * cm)
    p_det.drawOn(c, text_x + 0.5 * cm, y_cursor - contact_box_h + 0.40 * cm)
    c.restoreState()

    c.showPage()
