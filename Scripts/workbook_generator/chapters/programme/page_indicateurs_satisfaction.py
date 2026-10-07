from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from .common import setup_programme_page


def create_programme_page_indicateurs_satisfaction(c):
    """
    Page 12 : Indicateurs de Résultats & Enquête de Satisfaction (Session 2025).
    Données consolidées d'activité, taux de complétion 100 %, devenir et retours bénéficiaires.
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Indicateurs de résultats & Satisfaction",
        subtitle="Données d'activité et retours bénéficiaires consolidés (session 2025)",
        page_num=12,
        total_pages=12,
        topic="Résultats & Satisfaction",
    )

    pad_x = 0.75 * cm
    inner_w = content_w - 2 * pad_x

    style_item = ParagraphStyle(
        "IndItemText",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.3,
        leading=12.2,
        textColor=colors.HexColor("#222222"),
    )

    col_gap = 0.6 * cm
    col_w = (inner_w - col_gap) / 2.0

    # -------------------------------------------------------------------------
    # 1. CARTE 1 : ACTIVITÉ & DEVENIR DES BÉNÉFICIAIRES (2 COLONNES)
    # -------------------------------------------------------------------------
    card_act_h = 8.6 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setLineWidth(0.8)
    c.roundRect(content_x, y_cursor - card_act_h, content_w, card_act_h, 6, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 9.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        content_x + pad_x,
        y_cursor - 0.65 * cm,
        "Indicateurs d’activité & Devenir des bénéficiaires accompagnés :",
    )

    # Colonne Gauche : Chiffres d'activité
    txt_act = (
        "• <b>Bilans réalisés en 2025 :</b><br/>"
        "  - <b>12 bilans terminés</b> avec succès.<br/>"
        "  - <b>15 bilans en cours</b> de réalisation.<br/>"
        "  - <b>0 abandon / interruption :</b> 100 % de complétion.<br/><br/>"
        "• <b>Suivi post-bilan :</b><br/>"
        "  - <b>100 %</b> des entretiens de suivi à 6 mois réalisés.<br/><br/>"
        "• <b>Dynamique de transition :</b><br/>"
        "  Seulement 4 bénéficiaires ont souhaité rester sur le même métier (tous en changeant de structure employeur)."
    )
    p_act = Paragraph(txt_act, style_item)
    p_act.wrap(col_w, 6.8 * cm)
    p_act.drawOn(c, content_x + pad_x, y_cursor - 1.05 * cm - p_act.height)

    # Séparation verticale
    sep_x = content_x + pad_x + col_w + (col_gap / 2.0)
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(sep_x, y_cursor - 0.85 * cm, sep_x, y_cursor - card_act_h + 0.60 * cm)

    # Colonne Droite : Typologie des issues
    txt_dev = (
        "• <b>Devenir des 12 bénéficiaires finalisés :</b><br/><br/>"
        "  - <b>4 personnes (33 %) :</b> réorientation radicale via une formation qualifiante (3 à 18 mois).<br/>"
        "  - <b>3 personnes (25 %) :</b> évolution en interne sur un poste différent.<br/>"
        "  - <b>2 personnes (17 %) :</b> changement de métier avec formation sur le terrain.<br/>"
        "  - <b>1 personne (8 %) :</b> mobilité externe sur le même métier.<br/>"
        "  - <b>2 personnes (17 %) :</b> maintien temporaire dans l'attente du montage de leur projet."
    )
    p_dev = Paragraph(txt_dev, style_item)
    p_dev.wrap(col_w, 6.8 * cm)
    p_dev.drawOn(c, sep_x + (col_gap / 2.0), y_cursor - 1.05 * cm - p_dev.height)

    c.restoreState()
    y_cursor -= card_act_h + 0.50 * cm

    # -------------------------------------------------------------------------
    # 2. CARTE 2 : ENQUÊTE DE SATISFACTION À CHAUD
    # -------------------------------------------------------------------------
    card_sat_h = 7.4 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.0)
    c.roundRect(content_x, y_cursor - card_sat_h, content_w, card_sat_h, 6, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 9.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawCentredString(
        content_x + content_w / 2.0,
        y_cursor - 0.65 * cm,
        "Indicateurs de satisfaction à chaud (10/12 répondants au 20 octobre 2025) :",
    )

    questions = [
        (
            "Qualité des échanges avec l'accompagnateur",
            "5,0 / 5",
            "↗ En hausse",
        ),
        (
            "Qualité des informations du 1er entretien d'accueil",
            "4,9 / 5",
            "= Stable",
        ),
        (
            "Articulation et logique du déroulé des séances",
            "4,9 / 5",
            "↗ En hausse",
        ),
        (
            "Pertinence des supports pédagogiques (Carnets & Notion)",
            "4,8 / 5",
            "↗ En hausse",
        ),
        (
            "Pertinence des outils utilisés (MBTI®, Hexa3D, exercices)",
            "4,8 / 5",
            "= Stable",
        ),
        (
            "Déroulement et organisation d'ensemble du bilan",
            "4,8 / 5",
            "= Stable",
        ),
        (
            "Adéquation de la démarche à vos besoins et attentes",
            "4,7 / 5",
            "= Stable",
        ),
    ]

    table_x = content_x + 1.2 * cm
    badge_x = table_x + 9.2 * cm
    trend_x = table_x + 11.4 * cm

    row_y = y_cursor - 1.45 * cm
    row_step = 0.80 * cm

    for q_label, q_score, q_trend in questions:
        # Intitulé
        c.setFont(PDFStyle.FONT_BODY, 8.5)
        c.setFillColor(colors.HexColor("#222222"))
        c.drawString(table_x, row_y, f"• {q_label}")

        # Badge note
        badge_w = 1.7 * cm
        badge_h = 0.44 * cm
        badge_y = row_y - 0.08 * cm

        c.setFillColor(colors.HexColor("#FFEAE8"))
        c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
        c.setLineWidth(0.7)
        c.roundRect(badge_x, badge_y, badge_w, badge_h, badge_h / 2.0, fill=1, stroke=1)

        c.setFont(PDFStyle.FONT_TITLE, 7.8)
        c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
        c.drawCentredString(badge_x + badge_w / 2.0, badge_y + 0.11 * cm, q_score)

        # Tendance
        c.setFont(PDFStyle.FONT_ITALIC, 7.8)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(trend_x, row_y, q_trend)

        row_y -= row_step

    c.restoreState()
    y_cursor -= card_sat_h + 0.50 * cm

    # -------------------------------------------------------------------------
    # 3. ENCADRÉ 3 : ENGAGEMENT QUALITÉ & QUALIOPI
    # -------------------------------------------------------------------------
    qualite_h = 2.4 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.8)
    c.roundRect(content_x, y_cursor - qualite_h, content_w, qualite_h, 6, fill=1, stroke=1)

    style_qualite = ParagraphStyle(
        "QualiteText",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.2,
        leading=12.2,
        textColor=PDFStyle.COLOR_ACCENT_BLUE,
    )
    txt_qualite = (
        "<b>⭐ ENGAGEMENT QUALITÉ & DÉMARCHE QUALIOPI :</b><br/>"
        "Ces résultats traduisent notre engagement constant pour un accompagnement d'excellence, rigoureux et humain. "
        "Chaque retour d'expérience est minutieusement analysé afin d'alimenter notre démarche d'amélioration continue."
    )
    p_qual = Paragraph(txt_qualite, style_qualite)
    p_qual.wrap(inner_w, 2.0 * cm)
    p_qual.drawOn(c, content_x + pad_x, y_cursor - 0.40 * cm - p_qual.height)

    c.restoreState()
    c.showPage()


# Alias
create_programme_page_9 = create_programme_page_indicateurs_satisfaction
