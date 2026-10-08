from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle
from workbook_generator.primitives import (
    draw_icon,
    draw_label_pill,
    draw_paragraph,
    draw_rule,
    draw_text,
    draw_white_card,
    label_pill_size,
    paragraph_height,
    text_width,
)

from .common import BODY_LEADING, BODY_SIZE, CARD_GAP, PAD, add_bars, add_card, add_rich_text, programme_layout

SATISFACTION = [
    ("Qualité des échanges avec l'accompagnateur", "5,0 / 5", "up"),
    ("Qualité des informations du 1er entretien d'accueil", "4,9 / 5", "flat"),
    ("Articulation et logique du déroulé des séances", "4,9 / 5", "up"),
    ("Pertinence des supports pédagogiques (carnets et Notion)", "4,8 / 5", "up"),
    ("Pertinence des outils utilisés", "4,8 / 5", "flat"),
    ("Déroulement et organisation d'ensemble du bilan", "4,8 / 5", "flat"),
    ("Adéquation de la démarche à vos besoins et attentes", "4,7 / 5", "flat"),
]


def _satisfaction_table(layout, title):
    """Hot satisfaction scores: the criterion, its score in a blue pill and its trend."""
    c = layout.c
    x, w = layout.text_x, layout.target_width
    inner = w - 2 * PAD
    trend_w, score_w = 2.6 * cm, 1.9 * cm
    label_w = inner - trend_w - score_w - 0.6 * cm
    title_h = label_pill_size(title)[1] + 0.3 * cm
    rows_h = [max(0.7 * cm, paragraph_height(label, label_w, PDFStyle.FONT_BODY, BODY_SIZE, BODY_LEADING) + 0.25 * cm)
              for label, _, _ in SATISFACTION]
    h = 2 * PAD + title_h + sum(rows_h)
    layout._ensure_space(h)
    top = layout.y_cursor
    draw_white_card(c, x, top - h, w, h, radius=14)
    draw_label_pill(c, x + PAD, top - PAD - label_pill_size(title)[1], title, max_width=inner)
    t = top - PAD - title_h
    for i, ((label, score, trend), rh) in enumerate(zip(SATISFACTION, rows_h)):
        if i:
            draw_rule(c, x + PAD, x + w - PAD, t, color=PDFStyle.COLOR_INK, alpha=0.1)
        cy = t - rh / 2
        draw_paragraph(c, label, x + PAD, cy + paragraph_height(label, label_w, PDFStyle.FONT_BODY, BODY_SIZE,
                                                                  BODY_LEADING) / 2,
                       label_w, PDFStyle.FONT_BODY, BODY_SIZE, PDFStyle.COLOR_INK, BODY_LEADING)
        sx = x + PAD + label_w + 0.3 * cm
        c.saveState()
        c.setFillColor(PDFStyle.COLOR_BLUE)
        c.roundRect(sx, cy - 8, score_w, 16, 8, stroke=0, fill=1)
        c.restoreState()
        draw_text(c, sx + score_w / 2, cy - 3, score, PDFStyle.FONT_LABEL, 9, PDFStyle.COLOR_SURFACE_CARD, align="center")
        tx = sx + score_w + 0.3 * cm
        draw_icon(c, "trending_up" if trend == "up" else "trending_flat", tx + 6, cy, 13, PDFStyle.COLOR_BLUE)
        draw_text(c, tx + 15, cy - 3.2, "En hausse" if trend == "up" else "Stable", PDFStyle.FONT_BODY, BODY_SIZE,
                  PDFStyle.COLOR_INK_MUTED)
        t -= rh
    layout.y_cursor -= h + CARD_GAP


def create_programme_page_indicateurs_satisfaction(c):
    """Activity results, what became of the beneficiaries, and satisfaction (2025 session)."""
    layout = programme_layout(
        c, "Résultats *et satisfaction.*", "Résultats et satisfaction",
        lead="Données d’activité et retours des bénéficiaires consolidés (session 2025).",
    )
    layout.add_stat_boxes([
        {"value": "12", "label": "bilans terminés en 2025"},
        {"value": "15", "label": "bilans en cours"},
        {"value": "0", "label": "abandon : 100 % de complétion"},
        {"value": "100 %", "label": "entretiens de suivi à 6 mois réalisés"},
    ])
    add_bars(
        layout,
        [
            ("Réorientation radicale via une formation qualifiante (3 à 18 mois)", 4),
            ("Évolution en interne sur un poste différent", 3),
            ("Changement de métier avec formation sur le terrain", 2),
            ("Mobilité externe sur le même métier", 1),
            ("Maintien temporaire dans l'attente du montage de leur projet", 2),
        ],
        total=12,
        title="Devenir des 12 bénéficiaires finalisés",
    )
    add_rich_text(
        layout,
        "<b>Dynamique de transition :</b> seulement 4 bénéficiaires ont souhaité rester sur le même métier, tous en "
        "changeant de structure employeur.",
    )
    _satisfaction_table(layout, "Satisfaction à chaud · 10/12 répondants au 20 octobre 2025")
    add_card(
        layout,
        label="Engagement qualité & démarche Qualiopi",
        body="Ces résultats traduisent notre engagement constant pour un accompagnement d'excellence, rigoureux et "
             "humain. Chaque retour d'expérience est minutieusement analysé afin d'alimenter notre démarche "
             "d'amélioration continue.",
        color=PDFStyle.COLOR_SKY,
    )
    layout.render()
