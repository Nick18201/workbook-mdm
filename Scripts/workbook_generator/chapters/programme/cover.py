import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle
from workbook_generator.document_builder import document_pastel
from workbook_generator.primitives import (
    content_frame,
    draw_disc,
    draw_eyebrow,
    draw_heading,
    draw_label_pill,
    draw_logotype,
    draw_paragraph,
    draw_rule,
    draw_white_card,
    heading_height,
    postit,
)
from workbook_generator.utils import cached_image_reader

from .common import rich

WIDTH, HEIGHT = A4


def create_programme_cover(c):
    """
    Cover of the Programme brochure: logotype, the title with its accent, who designed the
    method, « 100 % à distance » on a post-it, the Qualiopi certification and the contact.
    """
    x, width = content_frame()
    disc_cx, disc_cy, disc_r = WIDTH - 1.0 * cm, HEIGHT * 0.64, 9.0 * cm
    draw_disc(c, disc_cx, disc_cy, disc_r, document_pastel(c))
    draw_disc(c, disc_cx - disc_r * 0.72, disc_cy + disc_r * 0.69, 0.55 * cm, PDFStyle.COLOR_CORAL)
    draw_logotype(c, x, HEIGHT - 2.6 * cm, size=16)
    draw_label_pill(c, x, HEIGHT - 4.3 * cm, "Bilan de compétences", variant="solid")

    note_w = 6.4 * cm
    with postit(c, WIDTH - PDFStyle.MARGIN_MAIN - note_w - 0.4 * cm, HEIGHT * 0.53, note_w, 2.1 * cm, angle=-3):
        draw_paragraph(c, "100 % à distance, en visio, partout en France.", 0.6 * cm, 2.1 * cm - 0.6 * cm,
                       note_w - 1.2 * cm, PDFStyle.FONT_SERIF, PDFStyle.SIZE_POSTIT, PDFStyle.COLOR_INK,
                       PDFStyle.SIZE_POSTIT * 1.3)

    # Title and lead in the lower half, above the Qualiopi card
    title = "Votre bilan de compétences *sur mesure.*"
    title_w = width * 0.9
    lead = ("Un accompagnement individuel <b>conçu par une psychologue du travail et un consultant en "
            "transformation</b>, pour repenser votre vie professionnelle et passer à l'action.")
    lead_p, lead_h = rich(lead, width * 0.85, size=PDFStyle.SIZE_LEAD, color=PDFStyle.COLOR_INK_MUTED)
    card_h = 3.6 * cm
    card_y = 2.8 * cm
    title_h = heading_height(title, title_w, size=42, min_size=30, max_lines=3, tracking=PDFStyle.TRACKING_TITLE_XL)
    title_top = card_y + card_h + 1.0 * cm + lead_h + 0.6 * cm + title_h
    draw_eyebrow(c, x, title_top + 0.5 * cm, "Le programme · document d'information 2026", max_width=width)
    bottom = draw_heading(c, title, x, title_top, title_w, size=42, min_size=30, max_lines=3,
                          tracking=PDFStyle.TRACKING_TITLE_XL)
    lead_p.drawOn(c, x, bottom - 0.6 * cm - lead_h)

    # Qualiopi certification
    draw_white_card(c, x, card_y, width, card_h, radius=14)
    pad = 0.5 * cm
    text_x = x + pad
    if os.path.exists(PDFStyle.PATH_LOGO_QUALIOPI):
        c.drawImage(cached_image_reader(PDFStyle.PATH_LOGO_QUALIOPI), x + pad, card_y + pad, width=3.4 * cm,
                    height=card_h - 2 * pad, preserveAspectRatio=True, anchor="w", mask="auto")
        text_x = x + pad + 3.9 * cm
    text_w = x + width - pad - text_x
    t = card_y + card_h - pad
    draw_eyebrow(c, text_x, t - 8, "Organisme certifié Qualiopi", color=PDFStyle.COLOR_CORAL_STRONG, max_width=text_w)
    t -= 8 + 0.3 * cm
    t -= draw_paragraph(c, "Bilans de compétences", text_x, t, text_w, PDFStyle.FONT_HEADING_BOLD, 13,
                        PDFStyle.COLOR_INK, 15) + 0.15 * cm
    legal, legal_h = rich("La certification qualité a été délivrée au titre de la catégorie d'action suivante : "
                          "<b>BILANS DE COMPÉTENCES</b>. Processus certifié par la République française.", text_w,
                          size=8.5, color=PDFStyle.COLOR_INK_MUTED)
    legal.drawOn(c, text_x, t - legal_h)

    draw_rule(c, x, x + width, 2.15 * cm, color=PDFStyle.COLOR_INK, width=0.75)
    draw_eyebrow(c, x, 1.45 * cm, "margedemanoeuvre.fr · contact@margedemanoeuvre.fr", max_width=width)
    c.showPage()
