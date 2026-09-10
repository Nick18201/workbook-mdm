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


def create_programme_page_9(c):
    """Page 9 : 7. Indicateurs de Résultats & Satisfaction 2025."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="RÉSULTATS & SATISFACTION"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE H1 : 7. INDICATEURS DE RÉSULTATS & SATISFACTION
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "7. Indicateurs de Résultats & Satisfaction",
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
        "Données d'activité et retours bénéficiaires consolidés au 20 octobre 2025",
    )
    y_cursor -= 0.75 * cm

    pad_x = 0.8 * cm
    col_w = (target_width - 2 * pad_x - 0.8 * cm) / 2.0

    style_item = ParagraphStyle(
        "IndItemWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=13.0,
        textColor=colors.HexColor("#222222"),
    )

    # -------------------------------------------------------------------------
    # 2. CARTE 1 : ACTIVITÉ 2025 & DEVENIR DES BÉNÉFICIAIRES (Aérée)
    # -------------------------------------------------------------------------
    card_act_h = 8.6 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(
        text_x, y_cursor - card_act_h, target_width, card_act_h, 8, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_TITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.70 * cm,
        "Indicateurs d’activité & Devenir des bénéficiaires (au 20/10/2025) :",
    )

    # Colonne Gauche : Chiffres d'activité
    txt_act = (
        "· <b>Bilans réalisés en 2025 :</b><br/>"
        "  - <b>12 bilans terminés</b> avec succès en 2025.<br/>"
        "  - <b>15 bilans en cours</b> (6 en phase finale, 2 en démarrage).<br/>"
        "  - <b>0 interruption :</b> 100% de complétion, aucun abandon.<br/><br/>"
        "· <b>Suivi post-bilan :</b><br/>"
        "  - <b>100%</b> des séances de suivi à 6 mois effectuées.<br/><br/>"
        "· <b>Dynamique de transition :</b><br/>"
        "  Seulement 4 personnes ont souhaité continuer le même métier (toutes en changeant de structure)."
    )
    p_act = Paragraph(txt_act, style_item)
    p_act.wrap(col_w, 6.5 * cm)
    p_act.drawOn(c, text_x + pad_x, y_cursor - 1.05 * cm - p_act.height)

    # Séparation verticale
    sep_x = text_x + pad_x + col_w + 0.4 * cm
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(
        sep_x,
        y_cursor - 0.50 * cm,
        sep_x,
        y_cursor - card_act_h + 0.50 * cm,
    )

    # Colonne Droite : Typologie des issues (sur 12 bilans finalisés)
    txt_dev = (
        "· <b>Devenir des 12 bénéficiaires accompagnés :</b><br/><br/>"
        "  - <b>4 personnes (33%) :</b> réorientation radicale via une formation qualifiante (durées de 3 à 18 mois).<br/>"
        "  - <b>3 personnes (25%) :</b> évolution en interne sur un poste différent.<br/>"
        "  - <b>2 personnes (17%) :</b> changement de métier avec formation sur le terrain.<br/>"
        "  - <b>1 personne (8%) :</b> mobilité externe sur le même métier.<br/>"
        "  - <b>2 personnes (17%) :</b> maintien de poste temporaire dans l'attente du montage de leur projet personnel."
    )
    p_dev = Paragraph(txt_dev, style_item)
    p_dev.wrap(col_w, 6.5 * cm)
    p_dev.drawOn(c, sep_x + 0.4 * cm, y_cursor - 1.05 * cm - p_dev.height)

    c.restoreState()
    y_cursor -= card_act_h + 0.75 * cm

    # -------------------------------------------------------------------------
    # 3. CARTE 2 : ENQUÊTE DE SATISFACTION (Centrée horizontalement et verticalement)
    # -------------------------------------------------------------------------
    card_sat_h = 7.45 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.0)
    c.roundRect(
        text_x, y_cursor - card_sat_h, target_width, card_sat_h, 8, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_TITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawCentredString(
        text_x + target_width / 2.0,
        y_cursor - 0.75 * cm,
        "Indicateurs de satisfaction à chaud (10/12 répondants au 20/10/2025) :",
    )

    # Grille de 7 critères de satisfaction
    questions = [
        (
            "Qualité des échanges avec l'accompagnatrice",
            "5,0 / 5",
            "↗ En hausse (vs 4,9)",
        ),
        (
            "Qualité des informations du 1er entretien d'accueil",
            "4,9 / 5",
            "= Stable",
        ),
        (
            "Articulation et logique du déroulé des séances",
            "4,9 / 5",
            "↗ En hausse (vs 4,75)",
        ),
        (
            "Pertinence des supports pédagogiques (Livret & Notion)",
            "4,8 / 5",
            "↗ En hausse (vs 4,6)",
        ),
        (
            "Pertinence des outils utilisés (MBTI, Hexa3D, exercices)",
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

    # Positionnement centré dans la carte
    table_x = text_x + 1.35 * cm
    badge_x = table_x + 9.15 * cm
    trend_x = table_x + 11.40 * cm

    row_y = y_cursor - 1.55 * cm
    row_step = 0.82 * cm

    for q_label, q_score, q_trend in questions:
        # Intitulé
        c.setFont(PDFStyle.FONT_BODY, 8.8)
        c.setFillColor(colors.HexColor("#222222"))
        c.drawString(table_x, row_y, f"· {q_label}")

        # Note en badge rouge/crème
        badge_w = 1.8 * cm
        badge_h = 0.46 * cm
        badge_y = row_y - 0.10 * cm

        c.setFillColor(colors.HexColor("#FFEAE8"))
        c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
        c.setLineWidth(0.7)
        c.roundRect(
            badge_x, badge_y, badge_w, badge_h, badge_h / 2.0, fill=1, stroke=1
        )

        c.setFont(PDFStyle.FONT_TITLE, 8.2)
        c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
        c.drawCentredString(
            badge_x + badge_w / 2.0, badge_y + 0.11 * cm, q_score
        )

        # Tendance
        c.setFont(PDFStyle.FONT_ITALIC, 8.0)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(trend_x, row_y, q_trend)

        row_y -= row_step

    c.restoreState()
    y_cursor -= card_sat_h + 0.85 * cm

    # -------------------------------------------------------------------------
    # 4. ENCADRÉ ENGAGEMENT QUALITÉ & QUALIOPI (Aéré)
    # -------------------------------------------------------------------------
    qualite_h = 2.4 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#CBD0FA"))
    c.setLineWidth(0.8)
    c.roundRect(
        text_x, y_cursor - qualite_h, target_width, qualite_h, 6, fill=1, stroke=1
    )

    style_qualite = ParagraphStyle(
        "QualiteWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.6,
        leading=12.6,
        textColor=PDFStyle.COLOR_ACCENT_BLUE,
    )
    txt_qualite = (
        "<b>🌟 ENGAGEMENT QUALITÉ & DÉMARCHE QUALIOPI :</b><br/>"
        "Ces résultats reflètent une rigueur méthodologique constante et un accompagnement centré sur l'humain. "
        "Les retours d'expérience sont analysés à chaque session dans le cadre du processus d'amélioration continue."
    )
    p_qual = Paragraph(txt_qualite, style_qualite)
    p_qual.wrap(target_width - 2 * pad_x, 2.0 * cm)
    p_qual.drawOn(c, text_x + pad_x, y_cursor - 0.40 * cm - p_qual.height)

    c.restoreState()

    c.showPage()
