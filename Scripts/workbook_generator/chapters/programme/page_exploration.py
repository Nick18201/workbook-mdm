from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.components import draw_title, TitleStyle
from .common import (
    setup_workbook_programme_page,
    draw_workbook_highlight_box,
    get_workbook_styles,
)


def create_programme_page_3(c):
    """Page 3 : Étape B (Exploration) & Étape C (Concrétisation)."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="EXPLORATION & CONCRÉTISATION"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE ÉTAPE B : EXPLORATION
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "Étape B : Exploration",
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
        "Ouvrir le champ des possibles & dépasser l'autocensure",
    )
    y_cursor -= 0.75 * cm

    # -------------------------------------------------------------------------
    # 2. GÉNÉRATION ET TRI D'IDÉES
    # -------------------------------------------------------------------------
    style_item = ParagraphStyle(
        "ExploItemP3",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.2,
        leading=13.8,
        textColor=colors.HexColor("#222222"),
    )
    txt_idees = (
        "<b><font color='#2F2EFA'>· Génération et tri d'idées :</font></b> "
        "L'objectif est d'explorer sans autocensure des pistes de reconversion, d'évolution "
        "ou de réinvention. En confrontant vos aspirations à vos compétences transférables, vous ouvrez "
        "le champ des possibles pour faire émerger des scénarios professionnels alignés avec qui vous êtes."
    )
    p_idees = Paragraph(txt_idees, style_item)
    p_idees.wrap(target_width, 3 * cm)
    p_idees.drawOn(c, text_x, y_cursor - p_idees.height)
    y_cursor -= p_idees.height + 0.65 * cm

    # -------------------------------------------------------------------------
    # 3. CARTE LES 3 GRANDS AXES D'EXPLORATION (Aérée)
    # -------------------------------------------------------------------------
    card_pistes_h = 4.2 * cm
    card_pad_x = 0.8 * cm
    card_inner_w = target_width - 2 * card_pad_x

    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(
        text_x, y_cursor - card_pistes_h, target_width, card_pistes_h, 8, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_TITLE, 10.2)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x + card_pad_x,
        y_cursor - 0.65 * cm,
        "Dans cette démarche, trois grands axes peuvent être explorés :",
    )

    style_axe = ParagraphStyle(
        "AxeWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.0,
        leading=13.2,
        textColor=colors.HexColor("#222222"),
    )

    axes = [
        (
            "La reconversion",
            "pour changer de métier ou de secteur d'activité.",
            "#2F2EFA",
        ),
        (
            "La création ou reprise d'activité",
            "pour développer un projet entrepreneurial ou indépendant.",
            "#FF4D4D",
        ),
        (
            "L'évolution dans le même métier",
            "dans un autre environnement ou avec une posture renouvelée.",
            "#2F2EFA",
        ),
    ]

    axe_y = y_cursor - 0.95 * cm
    for titre_a, desc_a, col_a in axes:
        txt_a = f"<b><font color='{col_a}'>· {titre_a} :</font></b> {desc_a}"
        p_a = Paragraph(txt_a, style_axe)
        p_a.wrap(card_inner_w, 2 * cm)
        axe_y -= p_a.height + 0.16 * cm
        p_a.drawOn(c, text_x + card_pad_x, axe_y)

    c.restoreState()
    y_cursor -= card_pistes_h + 0.80 * cm

    # -------------------------------------------------------------------------
    # 4. ENCADRÉ NOTRE SPÉCIFICITÉ EXPLORATION
    # -------------------------------------------------------------------------
    callout_h = 1.95 * cm
    spec_txt = (
        "Chaque piste est <b>passée au crible de vos besoins réels</b> et de votre "
        "écologie personnelle, sans céder aux fantasmes de reconversion « miracle » "
        "qui s'avèrent parfois inadaptés."
    )
    draw_workbook_highlight_box(
        c,
        text_x,
        y_cursor - callout_h,
        target_width,
        callout_h,
        prefix="👉 NOTRE SPÉCIFICITÉ :",
        text=spec_txt,
        accent_color=PDFStyle.COLOR_ACCENT_RED,
        bg_color=PDFStyle.COLOR_BG_NUDE,
        font_size=9.2,
        leading=13.2,
    )
    y_cursor -= callout_h + 0.85 * cm

    # -------------------------------------------------------------------------
    # 5. LIGNE SÉPARATRICE FINE
    # -------------------------------------------------------------------------
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(text_x, y_cursor, text_x + target_width, y_cursor)
    y_cursor -= 0.75 * cm

    # -------------------------------------------------------------------------
    # 6. TITRE ÉTAPE C : CONCRÉTISATION
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "Étape C : Concrétisation",
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
        "Sécuriser le passage à l'action & valider sur le terrain",
    )
    y_cursor -= 0.75 * cm

    concretisation_items = [
        (
            "Confrontation au terrain",
            "L'enjeu est de valider la faisabilité du projet en le confrontant au marché. "
            "Grâce à des enquêtes terrain auprès de professionnels, une analyse fine des opportunités "
            "et des prérequis (financiers, compétences), vous confrontez l'idée à la réalité pour lever les doutes et confirmer votre choix.",
        ),
        (
            "Feuille de route stratégique",
            "L'objectif est de structurer un plan d'action réaliste et progressif (calendrier, étapes clés, "
            "plan de financement de la formation si nécessaire). Ce cadrage sécurise votre transition pour que le projet ne reste pas "
            "une intention, mais devienne une trajectoire concrète.",
        ),
        (
            "Synthèse officielle & Suivi à 6 mois",
            "Rédaction et remise du document de synthèse réglementaire, co-construit avec le coach, qui récapitule vos compétences, "
            "votre projet et les étapes de mise en œuvre. Un entretien de suivi est programmé à 6 mois pour faire le point sur vos avancées.",
        ),
    ]

    for titre_c, desc_c in concretisation_items:
        txt_bullet_c = (
            f"<b><font color='#2F2EFA'>· {titre_c} :</font></b> {desc_c}"
        )
        p_c = Paragraph(txt_bullet_c, style_item)
        p_c.wrap(target_width, 4 * cm)
        p_c.drawOn(c, text_x, y_cursor - p_c.height)
        y_cursor -= p_c.height + 0.65 * cm

    # -------------------------------------------------------------------------
    # 7. VOLUME HORAIRE
    # -------------------------------------------------------------------------
    c.setFont(PDFStyle.FONT_ITALIC, 9.0)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Suivant le bilan choisi et les besoins : 4h à 8h d'entretiens passés sur ces deux étapes.",
    )

    c.showPage()
