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
    """Page 4 : 2. Organisation Pratique & Moyens Pédagogiques."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="ORGANISATION & PÉDAGOGIE"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE H1 : 2. ORGANISATION PRATIQUE & MOYENS PÉDAGOGIQUES
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "2. Organisation Pratique & Moyens Pédagogiques",
        pos=(text_x, y_cursor),
        available_width=target_width,
        style=TitleStyle(size=18, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    y_cursor -= 0.30 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Modalités d'accompagnement, outils exclusifs et travail inter-séances",
    )
    y_cursor -= 0.75 * cm

    pad_x = 0.85 * cm

    # -------------------------------------------------------------------------
    # 2. ENCADRÉ 1 : MOYENS TECHNIQUES ET PÉDAGOGIQUES (Aéré)
    # -------------------------------------------------------------------------
    moyens_h = 8.6 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(
        text_x, y_cursor - moyens_h, target_width, moyens_h, 8, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.65 * cm,
        "Moyens techniques, pédagogiques & outils exclusifs :",
    )

    style_moyen_item = ParagraphStyle(
        "MoyenItemWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=13.0,
        textColor=colors.HexColor("#222222"),
    )

    col_w = (target_width - 2 * pad_x - 0.8 * cm) / 2.0

    # Colonne Gauche : Entretiens & Supports
    txt_col1 = (
        "· <b>Entretiens individuels de 1h à 2h :</b> exploration approfondie des étapes du bilan (présentiel ou distanciel, espacés de 1 à 2 semaines).<br/><br/>"
        "· <b>Fiche d’accueil :</b> remplie au 1er RDV pour réaliser l'analyse du besoin et définir le contexte précis de la demande.<br/><br/>"
        "· <b>Livret d’accompagnement :</b> support complet pour réaliser le travail personnel en toute autonomie.<br/><br/>"
        "· <b>Enquêtes-métiers :</b> confrontation au terrain et rencontres de professionnels en activité."
    )
    p_col1 = Paragraph(txt_col1, style_moyen_item)
    p_col1.wrap(col_w, 7.5 * cm)
    p_col1.drawOn(c, text_x + pad_x, y_cursor - 0.95 * cm - p_col1.height)

    # Séparation verticale
    sep_x = text_x + pad_x + col_w + 0.4 * cm
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(
        sep_x,
        y_cursor - 0.50 * cm,
        sep_x,
        y_cursor - moyens_h + 0.50 * cm,
    )

    # Colonne Droite : Outils, Tests & Assistance
    txt_col2 = (
        "· <b>Site Notion ressource :</b> bibliothèque exclusive d'articles, podcasts, vidéos et fiches méthodologiques.<br/><br/>"
        "· <b>Tests certifiés :</b> inventaire d'intérêts professionnels (Hexa3D) et questionnaire de personnalité (MBTI).<br/><br/>"
        "· <b>Exercices de créativité :</b> cartes projectives et grilles d'aide à la décision.<br/><br/>"
        "· <b>Assistance pédagogique :</b> échanges continus par email / téléphone, réponse sous 48h ouvrées maximum."
    )
    p_col2 = Paragraph(txt_col2, style_moyen_item)
    p_col2.wrap(col_w, 7.5 * cm)
    p_col2.drawOn(
        c, sep_x + 0.4 * cm, y_cursor - 0.95 * cm - p_col2.height
    )

    c.restoreState()
    y_cursor -= moyens_h + 0.55 * cm

    # -------------------------------------------------------------------------
    # 3. ENCADRÉ 2 : ORGANISATION DU TRAVAIL INTER-SÉANCES
    # -------------------------------------------------------------------------
    inter_h = 6.6 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.0)
    c.roundRect(
        text_x, y_cursor - inter_h, target_width, inter_h, 8, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.65 * cm,
        "Organisation & réalisation du travail inter-séances :",
    )

    style_inter = ParagraphStyle(
        "InterTxtWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.0,
        leading=13.6,
        textColor=colors.HexColor("#222222"),
    )
    txt_inter = (
        "· <b>Rythme des séances :</b> Le bilan de compétences se partage entre des entretiens réguliers espacés d'environ 2 semaines (présentiel ou distanciel) et des temps dédiés de travail personnel.<br/><br/>"
        "· <b>Supports et ressources remis :</b> Ce travail s'appuie sur les exercices du <b>livret d'accompagnement</b> et le <b>site Notion ressource</b> mis à disposition dès la signature du contrat à l'issue de la première séance.<br/><br/>"
        "· <b>Consignes personnalisées :</b> L'accompagnateur explique le contenu des ressources et donne des consignes orales claires à chaque entretien sur les exercices et tests à explorer entre les séances."
    )
    p_inter = Paragraph(txt_inter, style_inter)
    p_inter.wrap(target_width - 2 * pad_x, 5.5 * cm)
    p_inter.drawOn(c, text_x + pad_x, y_cursor - 0.95 * cm - p_inter.height)

    c.restoreState()
    y_cursor -= inter_h + 0.55 * cm

    # -------------------------------------------------------------------------
    # 4. ENCADRÉ 3 : ASSISTANCE PÉDAGOGIQUE & CADRE DÉONTOLOGIQUE
    # -------------------------------------------------------------------------

    c.setFont(PDFStyle.FONT_TITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, y_cursor, "Cadre de confiance")
    y_cursor -= 0.50 * cm

    assist_h = 4.4 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#CBD0FA"))
    c.setLineWidth(0.8)
    c.roundRect(
        text_x, y_cursor - assist_h, target_width, assist_h, 6, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_TITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.65 * cm,
        "Assistance pédagogique continue & Engagement déontologique :",
    )

    style_assist = ParagraphStyle(
        "AssistTxtWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=13.0,
        textColor=colors.HexColor("#222222"),
    )
    txt_assist = (
        "· <b>Accompagnement et réactivité :</b> L’assistance pédagogique et technique est assurée directement par votre accompagnateur par email ou téléphone. Réponse garantie dans un délai maximum de 48h ouvrées.<br/><br/>"
        "· <b>Cadre de confiance & Confidentialité :</b> Respect absolu du secret professionnel, neutralité bienveillante et adhésion au code de déontologie des psychologues."
    )
    p_assist = Paragraph(txt_assist, style_assist)
    p_assist.wrap(target_width - 2 * pad_x, 3.5 * cm)
    p_assist.drawOn(c, text_x + pad_x, y_cursor - 0.95 * cm - p_assist.height)

    c.restoreState()

    c.showPage()
