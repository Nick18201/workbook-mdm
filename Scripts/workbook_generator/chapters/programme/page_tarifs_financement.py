import os

from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle
from workbook_generator.primitives import (
    draw_card_title,
    draw_eyebrow,
    draw_label_pill,
    draw_pastel_card,
    draw_text,
    draw_white_card,
    label_pill_size,
)
from workbook_generator.utils import cached_image_reader

from .common import CARD_GAP, PAD, _draw_items, _items_height, add_card, programme_layout, rich

INCLUS = [
    "<b>7 carnets de bord guidés</b> (vous les gardez définitivement)",
    "<b>L'espace Notion de ressources</b> accessible jusqu'au suivi à 6 mois",
    "<b>Le copilote IA</b> dédié pour challenger et nourrir vos réflexions",
    "<b>Le test des fonctionnements cognitifs</b> et sa restitution approfondie",
]
LOGOS = [
    (PDFStyle.PATH_LOGO_CPF, "CPF (MonCompteFormation)"),
    (PDFStyle.PATH_LOGO_FRANCE_TRAVAIL, "France Travail"),
    (PDFStyle.PATH_LOGO_QUALIOPI, "Qualiopi certifié"),
]


def _price_card(layout):
    """The single formula: what it contains, its price, and what is included."""
    c = layout.c
    x, w = layout.text_x, layout.target_width
    inner = w - 2 * PAD
    details, details_h = rich("10 séances individuelles de 1 h 20 en visio + entretien de suivi à 6 mois (40 min), "
                              "soit 14 h d'accompagnement", inner, color=PDFStyle.COLOR_INK_MUTED)
    pill_h = label_pill_size("Formule unique")[1]
    h = 2 * PAD + pill_h + 0.3 * cm + 16 + 0.15 * cm + details_h + 0.3 * cm + 44 + 0.2 * cm + 10 + 0.45 * cm \
        + 10 + 0.25 * cm + _items_height(INCLUS, inner)
    layout._ensure_space(h)
    top = layout.y_cursor
    draw_pastel_card(c, x, top - h, w, h, radius=16)
    t = top - PAD
    draw_label_pill(c, x + PAD, t - pill_h, "Formule unique", variant="solid")
    t -= pill_h + 0.3 * cm
    t -= draw_card_title(c, "Le bilan de compétences Marge de Manœuvre", None, x + PAD, t, inner, size=14) + 0.15 * cm
    details.drawOn(c, x + PAD, t - details_h)
    t -= details_h + 0.3 * cm
    draw_text(c, x + PAD, t - 38, "1 800 €", PDFStyle.FONT_LABEL, 44, PDFStyle.COLOR_BLUE)
    t -= 44 + 0.2 * cm
    draw_eyebrow(c, x + PAD, t - 8, "Net de taxes (TVA non applicable, art. 293 B du CGI)", max_width=inner)
    t -= 10 + 0.45 * cm
    draw_eyebrow(c, x + PAD, t - 8, "Inclus dans cet accompagnement", color=PDFStyle.COLOR_INK, max_width=inner)
    t -= 10 + 0.25 * cm
    _draw_items(c, INCLUS, x + PAD, t, inner)
    layout.y_cursor -= h + CARD_GAP


def _logos_row(layout):
    """The funders' and certification logos, each above its name."""
    c = layout.c
    x, w = layout.text_x, layout.target_width
    h = 2.6 * cm
    layout._ensure_space(h)
    top = layout.y_cursor
    draw_white_card(c, x, top - h, w, h, radius=14)
    col = w / len(LOGOS)
    for k, (path, label) in enumerate(LOGOS):
        cx = x + k * col + col / 2
        if os.path.exists(path):
            c.drawImage(cached_image_reader(path), cx - 1.6 * cm, top - 0.35 * cm - 1.4 * cm, width=3.2 * cm,
                        height=1.4 * cm, preserveAspectRatio=True, anchor="c", mask="auto")
        draw_eyebrow(c, cx, top - h + 0.45 * cm, label, size=PDFStyle.SIZE_FOLIO, align="center", max_width=col - 0.3 * cm)
    layout.y_cursor -= h + CARD_GAP


def create_programme_page_tarifs(c):
    """Price of the single formula, CPF funding and the legal mentions."""
    layout = programme_layout(
        c, "Formule *et financement.*", "Tarifs et financements",
        lead="Une formule unique, finançable par le CPF.",
    )
    _price_card(layout)
    add_card(
        layout,
        title="Comment financer votre bilan de compétences ?",
        body="En tant qu'<b>organisme certifié Qualiopi</b>, nos parcours répondent aux normes d'exigence de l'État.<br/>"
             "<b>Le CPF finance jusqu'à 1 600 € :</b> avec un solde suffisant, <b>il vous reste 200 € à charge</b>, "
             "quel que soit votre statut. Votre employeur, votre OPCO ou France Travail peuvent également les prendre "
             "en charge.",
        white=True,
    )
    _logos_row(layout)
    add_card(
        layout,
        body="« <i>La certification qualité a été délivrée au titre de la catégorie d'action suivante : "
             "<b>BILANS DE COMPÉTENCES</b>.</i> »<br/><br/>"
             "<b>Participation forfaitaire :</b> La participation forfaitaire de 150 € (décret n° 2024-394, montant "
             "porté à 150 € au 1er avril 2026 par le décret n° 2026-234) <b>est comprise dans les 200 € : elle ne "
             "s'ajoute pas</b>.",
        color=PDFStyle.COLOR_ALMOND,
    )
    layout.render()

