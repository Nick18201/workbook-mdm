"""
Building blocks of the Programme brochure (published on the website), in the art direction:
each page is a PageLayout (eyebrow pill, punctuated title, folio) whose blocks size
themselves to their text, written in ReportLab paragraph markup (<b>, <i>, <br/>).
"""

import re

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph

from workbook_generator.config import PDFStyle
from workbook_generator.primitives import (
    draw_card_title,
    draw_label_pill,
    draw_number,
    draw_paragraph,
    draw_pastel_card,
    draw_star,
    draw_text,
    draw_white_card,
    label_pill_size,
    paragraph_height,
    pastel_cycle,
)
from workbook_generator.templates import PageLayout, LayoutConfig
from workbook_generator.utils import french_typography

BODY_SIZE = PDFStyle.SIZE_BODY_SMALL  # dense reading text of the brochure (9.5 pt)
BODY_LEADING = BODY_SIZE * 1.42
PAD = 0.5 * cm
ITEM_GAP = 0.18 * cm
CARD_GAP = 0.35 * cm


def _hex(color):
    return "#" + color.hexval()[2:]


def markup(text):
    """Brochure text as paragraph markup in the DA: palette colors, no pictogram fonts, typography."""
    text = re.sub(r"<font name='ZapfDingbats'[^>]*>.*?</font>\s*", "", str(text))
    for old, new in (("#2F2EFA", PDFStyle.COLOR_BLUE), ("#DC2626", PDFStyle.COLOR_CORAL_STRONG),
                     ("#6B7280", PDFStyle.COLOR_INK_MUTED)):
        text = re.sub(old, _hex(new), text, flags=re.IGNORECASE)
    text = text.replace("seul(e)", "seul·e").replace("prêt(e)", "prêt·e")
    return french_typography(text)


def _style(size=BODY_SIZE, leading=None, color=None, name="ProgrammeText"):
    return ParagraphStyle(name, fontName=PDFStyle.FONT_BODY, fontSize=size, leading=leading or size * 1.42,
                          textColor=color or PDFStyle.COLOR_INK)


def rich(text, width, size=BODY_SIZE, color=None):
    """A wrapped Paragraph of brochure markup and its height."""
    p = Paragraph(markup(text), _style(size, color=color))
    _, h = p.wrap(width, 10000)
    return p, h


def _items_height(items, width, size=BODY_SIZE):
    indent = size * 1.6
    return sum(rich(item, width - indent, size)[1] for item in items) + ITEM_GAP * max(len(items) - 1, 0)


def _draw_items(c, items, x, top, width, size=BODY_SIZE):
    """Star-bulleted paragraphs of markup; returns their height."""
    indent = size * 1.6
    star = size * 0.85
    y = top
    for i, item in enumerate(items):
        p, h = rich(item, width - indent, size)
        baseline = y - (size * 1.42 - size) / 2 - 0.8 * size
        draw_star(c, x, baseline + 0.36 * size - star / 2, star)
        p.drawOn(c, x + indent, y - h)
        y -= h + (ITEM_GAP if i < len(items) - 1 else 0)
    return top - y


def programme_layout(c, title, eyebrow, lead=None):
    """A brochure page: the eyebrow pill, the title, then an ink-muted lead paragraph."""
    layout = PageLayout(c, title, config=LayoutConfig(part_title=eyebrow))
    if lead:
        layout.add_paragraphs([lead], color=PDFStyle.COLOR_INK_MUTED, spacing_after=0.4 * cm)
    return layout


def add_rich_text(layout, text, size=BODY_SIZE, color=None):
    """Running text in brochure markup (<b>, <i>…), without a card."""
    p, h = rich(text, layout.target_width, size, color)
    layout._ensure_space(h)
    p.drawOn(layout.c, layout.text_x, layout.y_cursor - h)
    layout.y_cursor -= h + 0.4 * cm
    return layout.y_cursor


def _card_height(width, label=None, title=None, subtitle=None, body=None, items=None):
    inner = width - 2 * PAD
    h = 2 * PAD
    if label:
        h += label_pill_size(label)[1] + 0.25 * cm
    if title:
        h += paragraph_height(title, inner, PDFStyle.FONT_HEADING_BOLD, PDFStyle.SIZE_TITLE_ELEMENT,
                              PDFStyle.SIZE_TITLE_ELEMENT * 1.15)
        if subtitle:
            h += paragraph_height(subtitle, inner, PDFStyle.FONT_HEADING_ITALIC, PDFStyle.SIZE_TITLE_ELEMENT,
                                  PDFStyle.SIZE_TITLE_ELEMENT * 1.15)
        h += 0.2 * cm
    if body:
        h += rich(body, inner)[1] + (0.2 * cm if items else 0)
    if items:
        h += _items_height(items, inner)
    return h


def _draw_card(c, x, top, width, height, label=None, title=None, subtitle=None, body=None, items=None, color=None,
               white=False):
    if white:
        draw_white_card(c, x, top - height, width, height, radius=14)
    else:
        draw_pastel_card(c, x, top - height, width, height, color=color, radius=14)
    inner = width - 2 * PAD
    t = top - PAD
    if label:
        _, pill_h = draw_label_pill(c, x + PAD, t - label_pill_size(label)[1], label,
                                    variant="pastel" if white else "on_pastel", max_width=inner)
        t -= pill_h + 0.25 * cm
    if title:
        t -= draw_card_title(c, title, subtitle, x + PAD, t, inner, size=PDFStyle.SIZE_TITLE_ELEMENT) + 0.2 * cm
    if body:
        p, h = rich(body, inner)
        p.drawOn(c, x + PAD, t - h)
        t -= h + (0.2 * cm if items else 0)
    if items:
        _draw_items(c, items, x + PAD, t, inner)


def add_card(layout, label=None, title=None, subtitle=None, body=None, items=None, color=None, white=False):
    """A full-width card: an optional pill label, a two-part title, a paragraph and star items."""
    h = _card_height(layout.target_width, label, title, subtitle, body, items)
    layout._ensure_space(h)
    _draw_card(layout.c, layout.text_x, layout.y_cursor, layout.target_width, h, label, title, subtitle, body, items,
               color, white)
    layout.y_cursor -= h + CARD_GAP
    return layout.y_cursor


def add_card_row(layout, cards, colors=None):
    """Cards side by side, as tall as the tallest. cards: dicts of add_card arguments."""
    gap = 0.4 * cm
    n = len(cards)
    w = (layout.target_width - gap * (n - 1)) / n
    h = max(_card_height(w, **card) for card in cards)
    layout._ensure_space(h)
    pastels = colors or pastel_cycle(layout.c)
    for k, card in enumerate(cards):
        card = dict(card)
        card.setdefault("color", pastels[k % len(pastels)])
        _draw_card(layout.c, layout.text_x + k * (w + gap), layout.y_cursor, w, h, **card)
    layout.y_cursor -= h + CARD_GAP
    return layout.y_cursor


def add_temps_band(layout, number, title, motto, intro=None):
    """The banner of a stage of the bilan: big PT Mono number, title, motto and one sentence."""
    c = layout.c
    x, w = layout.text_x, layout.target_width
    text_x = x + 2.4 * cm
    inner = x + w - PAD - text_x
    intro_p, intro_h = rich(intro, inner, color=PDFStyle.COLOR_INK_MUTED) if intro else (None, 0)
    h = max(2.2 * cm, 2 * PAD + 16 + 0.15 * cm + intro_h)
    layout._ensure_space(h)
    top = layout.y_cursor
    draw_pastel_card(c, x, top - h, w, h, radius=14)
    draw_number(c, x + PAD - 2, top - h / 2 - 15, number, size=44)
    t = top - PAD
    tw = draw_text(c, text_x, t - 12, title, PDFStyle.FONT_HEADING_BOLD, 13, PDFStyle.COLOR_INK)
    if motto:
        draw_text(c, text_x + tw + 0.3 * cm, t - 12, motto, PDFStyle.FONT_SERIF, 13, PDFStyle.COLOR_INK)
    if intro_p:
        intro_p.drawOn(c, text_x, t - 16 - 0.15 * cm - intro_h)
    layout.y_cursor -= h + CARD_GAP
    return layout.y_cursor


def add_session_card(layout, badge, title, description, objective, followup=False):
    """A session: a pill badge (S1…), its title, what happens, and its objective."""
    c = layout.c
    x, w = layout.text_x, layout.target_width
    badge_w = 1.5 * cm if followup else 1.1 * cm
    text_x = x + PAD + badge_w + 0.4 * cm
    inner = x + w - PAD - text_x
    title_h = paragraph_height(title, inner, PDFStyle.FONT_HEADING_BOLD, PDFStyle.SIZE_TITLE_ELEMENT,
                               PDFStyle.SIZE_TITLE_ELEMENT * 1.2)
    desc_p, desc_h = rich(description, inner)
    obj_p, obj_h = rich(f"<font color='{_hex(PDFStyle.COLOR_BLUE)}'><b>Objectif :</b> {objective}</font>", inner)
    h = 2 * PAD + title_h + 0.15 * cm + desc_h + 0.25 * cm + obj_h
    layout._ensure_space(h)
    top = layout.y_cursor
    if followup:
        draw_pastel_card(c, x, top - h, w, h, color=PDFStyle.COLOR_SKY, radius=14)
    else:
        draw_white_card(c, x, top - h, w, h, radius=14)
    pill_h = 0.75 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BLUE)
    c.roundRect(x + PAD, top - PAD - pill_h, badge_w, pill_h, pill_h / 2, stroke=0, fill=1)
    c.restoreState()
    draw_text(c, x + PAD + badge_w / 2, top - PAD - pill_h / 2 - 3.5, badge, PDFStyle.FONT_LABEL, 10,
              PDFStyle.COLOR_SURFACE_CARD, align="center")
    t = top - PAD
    t -= draw_paragraph(c, title, text_x, t, inner, PDFStyle.FONT_HEADING_BOLD, PDFStyle.SIZE_TITLE_ELEMENT,
                        PDFStyle.COLOR_INK, PDFStyle.SIZE_TITLE_ELEMENT * 1.2) + 0.15 * cm
    desc_p.drawOn(c, text_x, t - desc_h)
    t -= desc_h + 0.25 * cm
    obj_p.drawOn(c, text_x, t - obj_h)
    layout.y_cursor -= h + PDFStyle.GAP_BLOCK * 0.5
    return layout.y_cursor


def add_deliverables(layout, title, items):
    """The deliverables validated at the end of a stage, on a jasmine card."""
    return add_card(layout, label="Livrables validés", title=title, items=items, color=PDFStyle.COLOR_JASMINE)


def add_bars(layout, rows, total, title=None):
    """A light bar chart in a white card: rows of (label, count) out of total, with the share."""
    c = layout.c
    x, w = layout.text_x, layout.target_width
    inner = w - 2 * PAD
    label_w = inner * 0.5
    bar_x = x + PAD + label_w + 0.3 * cm
    bar_w = inner - label_w - 0.3 * cm - 2.2 * cm
    row_h = 0.62 * cm
    title_h = (label_pill_size(title)[1] + 0.3 * cm) if title else 0
    label_hs = [paragraph_height(label, label_w, PDFStyle.FONT_BODY, BODY_SIZE, BODY_LEADING) for label, _ in rows]
    h = 2 * PAD + title_h + sum(max(row_h, lh) for lh in label_hs) + 0.1 * cm * (len(rows) - 1)
    layout._ensure_space(h)
    top = layout.y_cursor
    draw_white_card(c, x, top - h, w, h, radius=14)
    t = top - PAD
    if title:
        draw_label_pill(c, x + PAD, t - label_pill_size(title)[1], title, max_width=inner)
        t -= title_h
    for (label, count), lh in zip(rows, label_hs):
        rh = max(row_h, lh)
        draw_paragraph(c, label, x + PAD, t, label_w, PDFStyle.FONT_BODY, BODY_SIZE, PDFStyle.COLOR_INK, BODY_LEADING)
        cy = t - min(rh, BODY_LEADING) / 2 - 1
        c.saveState()
        c.setFillColor(PDFStyle.COLOR_LINE)
        c.roundRect(bar_x, cy - 4, bar_w, 8, 4, stroke=0, fill=1)
        c.setFillColor(PDFStyle.COLOR_BLUE)
        c.roundRect(bar_x, cy - 4, max(8, bar_w * count / total), 8, 4, stroke=0, fill=1)
        c.restoreState()
        share = round(100 * count / total)
        draw_text(c, x + w - PAD, cy - 3.5, f"{count} · {share} %", PDFStyle.FONT_LABEL, 9, PDFStyle.COLOR_BLUE,
                  align="right")
        t -= rh + 0.1 * cm
    layout.y_cursor -= h + CARD_GAP
    return layout.y_cursor
