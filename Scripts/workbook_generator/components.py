"""
Full-page templates and shared blocks of the workbooks, in the « Éditorial & Affirmé »
art direction (DA-workbook.md, section 8): white pages, an eyebrow and a punctuated title
with a coral accent, pastel cards, fields bordered in `line-strong`, PT Mono folio.

Every page function ends its own page (c.showPage()). Long content continues on pages
titled "<title> (suite)", so nothing is drawn off the page.
"""

import re
from dataclasses import dataclass

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from .config import PDFStyle
from .document_builder import document_pastel
from .forms import create_input_field, create_checkbox, create_radio, reserve_field_name
from .primitives import (
    content_frame,
    draw_disc,
    draw_eyebrow,
    draw_field_box,
    draw_filled_arrow,
    draw_folio,
    draw_heading,
    draw_icon_badge,
    draw_label_pill,
    draw_logotype,
    draw_number,
    draw_paragraph,
    pastel_cycle,
    draw_pastel_card,
    draw_page_head,
    draw_rule,
    draw_signature,
    draw_stamp,
    draw_star_list,
    draw_text,
    first_baseline,
    heading_height,
    label_pill_size,
    paragraph_height,
    postit,
    stamp_size,
    star_list_height,
    text_width,
)
from .utils import fit_font_size, ellipsize

WIDTH, HEIGHT = A4


# --- Former helpers, restyled (the hand-drawn chapter pages use them until lot E5) ---

def draw_page_background(c, width, height, use_blobs=False):
    """Pages are white in the art direction: nothing to draw. Kept for the chapter pages."""


def draw_side_panel(c, x, page_width, page_height):
    """The side panel of the former art direction is gone: nothing to draw."""


def draw_page_header(c, part_title, width, height, x_offset=0):
    """Eyebrow at the top of the page."""
    if part_title:
        x, content_w = content_frame()
        draw_eyebrow(c, x, height - PDFStyle.EYEBROW_TOP, part_title, max_width=content_w)


def draw_page_footer(c, width, height, x_offset=0):
    """Folio at the bottom of the page."""
    draw_folio(c)


def draw_page_decorations(c, width, height, part_title=None, x_offset=0):
    """Eyebrow (when part_title is given) and folio, for pages that draw their own title."""
    draw_page_header(c, part_title, width, height, x_offset)
    draw_folio(c)


def draw_card(c, x, y, width, height):
    """Pastel card in the document's dominant pastel."""
    draw_pastel_card(c, x, y, width, height)


@dataclass
class TitleStyle:
    size: float = 24
    color: object = None  # titles are ink in the art direction; kept for the former callers


def draw_title(c, text, pos, available_width=None, style: TitleStyle = None):
    """
    Title whose first baseline is at pos (former API): ink with a coral accent on the
    last word. Returns the y one line below the title, as before.
    """
    style = style or TitleStyle()
    x, y = pos
    if available_width is None:
        available_width = WIDTH - x - PDFStyle.MARGIN_MAIN
    leading = style.size * PDFStyle.LEADING_TITLE
    top = y + (leading - style.size) / 2 + 0.8 * style.size
    bottom = draw_heading(c, text, x, top, available_width, size=style.size, min_size=style.size, max_lines=4)
    n_lines = round((top - bottom) / leading)
    return y - n_lines * style.size * 1.2


def draw_branding_logo(c, x, y, size=40, align="left"):
    """Logotype « marge / de manœuvre » (former API: size 40 = cover size)."""
    logo_size = size * 0.6
    if align == "center":
        x -= text_width("de manœuvre", PDFStyle.FONT_LOGO, logo_size, -0.05) / 2
    draw_logotype(c, x, y, size=logo_size)


def draw_fitted_text(c, text, x, y, max_width, font_name, size, min_size=None,
                     max_lines=2, leading=None, align="left"):
    """
    Draws text inside max_width instead of letting it run off: the font shrinks down to
    min_size, then the text wraps onto at most max_lines lines, the last one ending with
    a visible '…' if it is still too long. y is the first baseline (lines go downward);
    the fill color is the caller's. Returns (number of lines drawn, font size used).
    """
    size = fit_font_size(text, font_name, size, max_width, min_size or size)
    lines = simpleSplit(text, font_name, size, max_width) or [text]
    if len(lines) > max_lines:
        lines = lines[:max_lines - 1] + [" ".join(lines[max_lines - 1:])]
    lines = [ellipsize(line, font_name, size, max_width) for line in lines]
    leading = leading or size * 1.2

    c.setFont(font_name, size)
    for i, line in enumerate(lines):
        line_y = y - i * leading
        if align == "center":
            c.drawCentredString(x, line_y, line)
        elif align == "right":
            c.drawRightString(x, line_y, line)
        else:
            c.drawString(x, line_y, line)
    return len(lines), size


def draw_pause_badge(c, x, y, radius=0.4 * cm):
    """Draws the 'Pause' badge icon (circle with Play + Pause bars), in white."""
    c.saveState()
    c.setStrokeColor(PDFStyle.COLOR_SURFACE_CARD)
    c.setLineWidth(1.5)
    c.circle(x, y + 0.15 * cm, radius, fill=0, stroke=1)
    bar_width = 0.08 * cm
    bar_height = 0.3 * cm
    c.setFillColor(PDFStyle.COLOR_SURFACE_CARD)
    c.rect(x - 0.15 * cm, y, bar_width, bar_height, fill=1, stroke=0)
    p = c.beginPath()
    p.moveTo(x + 0.02 * cm, y)
    p.lineTo(x + 0.02 * cm, y + bar_height)
    p.lineTo(x + 0.22 * cm, y + bar_height / 2)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


# --- Shared blocks ------------------------------------------------------------

QUESTION_SIZE = PDFStyle.SIZE_TITLE_ELEMENT
QUESTION_LEADING = QUESTION_SIZE * 1.3
HINT_SIZE = PDFStyle.SIZE_BODY_SMALL
HINT_LEADING = HINT_SIZE * 1.45
QUESTION_GAP_TO_BOX = 6


def example_display(example):
    """Normalizes an example to the 'Exemple : …' form shown under a question."""
    ex_clean = str(example).strip()
    if ex_clean.lower().startswith("exemple :"):
        return ex_clean
    if ex_clean.lower().startswith("ex :"):
        return "Exemple :" + ex_clean[4:]
    if ex_clean.lower().startswith("ex:"):
        return "Exemple :" + ex_clean[3:]
    return f"Exemple : {ex_clean}"


QUESTION_PAD = 0.45 * cm


def question_text_height(width, question, subtitle=None, example=None):
    """Height of a question card without its answer box (matches draw_question)."""
    width -= 2 * QUESTION_PAD
    h = paragraph_height(question, width, PDFStyle.FONT_HEADING_BOLD, QUESTION_SIZE, QUESTION_LEADING)
    if subtitle:
        h += 2 + paragraph_height(subtitle, width, PDFStyle.FONT_BODY, HINT_SIZE, HINT_LEADING)
    if example:
        h += 2 + paragraph_height(example_display(example), width, PDFStyle.FONT_HEADING_ITALIC, HINT_SIZE, HINT_LEADING)
    return h + QUESTION_GAP_TO_BOX + 2 * QUESTION_PAD


def draw_question(c, x, top, width, question, field_name, box_height, subtitle=None, example=None, tooltip="",
                  color=None):
    """
    A pastel card holding a question (DM Sans 700), its hint and example (ink-muted), then
    a white answer box bordered in line-strong with a multiline field. Returns the bottom y
    of the card.
    """
    total = question_text_height(width, question, subtitle, example) + box_height
    draw_pastel_card(c, x, top - total, width, total, color=color, radius=12)
    x += QUESTION_PAD
    width -= 2 * QUESTION_PAD
    y = top - QUESTION_PAD
    y -= draw_paragraph(c, question, x, y, width, PDFStyle.FONT_HEADING_BOLD, QUESTION_SIZE,
                        PDFStyle.COLOR_INK, QUESTION_LEADING)
    if subtitle:
        y -= 2
        y -= draw_paragraph(c, subtitle, x, y, width, PDFStyle.FONT_BODY, HINT_SIZE,
                            PDFStyle.COLOR_INK_MUTED, HINT_LEADING)
    if example:
        y -= 2
        y -= draw_paragraph(c, example_display(example), x, y, width, PDFStyle.FONT_HEADING_ITALIC, HINT_SIZE,
                            PDFStyle.COLOR_INK_MUTED, HINT_LEADING)
    y -= QUESTION_GAP_TO_BOX
    draw_answer_box(c, x, y - box_height, width, box_height, field_name, tooltip=tooltip or question)
    return top - total


def draw_answer_box(c, x, y, width, height, field_name, tooltip="", multiline=True, value="", font_size=None):
    """
    White rounded box bordered in line-strong, with a transparent form field on top.
    A prefilled multiline value is wrapped here: ReportLab draws the field's appearance
    one line per explicit line break, so a long line would be cut at the edge.
    """
    draw_field_box(c, x, y, width, height)
    pad = 3
    if value and multiline and font_size:
        # Form fields are drawn in Helvetica, ReportLab's default form font
        value = "\n".join(
            line for paragraph in str(value).split("\n")
            for line in (simpleSplit(paragraph, "Helvetica", font_size, width - 2 * pad - 6) or [""])
        )
    create_input_field(
        c.acroForm, field_name, pos=(x + pad, y + pad), size=(width - 2 * pad, height - 2 * pad),
        tooltip=tooltip, multiline=multiline, value=value, font_size=font_size, framed=False,
    )


SCALE_NUMBER_SIZE = 8


def choice_scale_height(with_labels):
    return SCALE_NUMBER_SIZE + 4 + 20 + (14 if with_labels else 0)


def draw_choice_scale(c, group, x, top, width, values, min_label="", max_label="", tooltip=""):
    """
    A single-choice scale as a row of pastilles: the value above each disc, one radio
    button per disc (reserve `group` once with reserve_field_name). Returns its height.
    """
    n = len(values)
    d = min(20, (width / max(n, 1)) * 0.75)
    step = (width - d) / (n - 1) if n > 1 else 0
    num_y = top - SCALE_NUMBER_SIZE
    disc_cy = num_y - 4 - 10
    for i, val in enumerate(values):
        cx = x + d / 2 + i * step
        draw_text(c, cx, num_y, str(val), PDFStyle.FONT_LABEL, SCALE_NUMBER_SIZE, PDFStyle.COLOR_INK_MUTED, align="center")
        c.saveState()
        c.setFillColor(PDFStyle.COLOR_SURFACE_CARD)
        c.setStrokeColor(PDFStyle.COLOR_LINE_STRONG)
        c.setLineWidth(PDFStyle.LINE_WIDTH_FIELD)
        c.circle(cx, disc_cy, d / 2, stroke=1, fill=1)
        c.restoreState()
        create_radio(
            c.acroForm, group, val, pos=(cx - d / 2 + 1, disc_cy - d / 2 + 1), size=d - 2,
            tooltip=f"{tooltip} : {val}" if tooltip else str(val), framed=False,
        )
    if min_label or max_label:
        label_y = disc_cy - d / 2 - 12
        half = width / 2 - 6
        if min_label:
            draw_text(c, x, label_y, ellipsize(str(min_label), PDFStyle.FONT_BODY, HINT_SIZE, half),
                      PDFStyle.FONT_BODY, HINT_SIZE, PDFStyle.COLOR_INK_MUTED)
        if max_label:
            draw_text(c, x + width, label_y, ellipsize(str(max_label), PDFStyle.FONT_BODY, HINT_SIZE, half),
                      PDFStyle.FONT_BODY, HINT_SIZE, PDFStyle.COLOR_INK_MUTED, align="right")
    return choice_scale_height(bool(min_label or max_label))


def _finish_page(c):
    draw_folio(c)
    c.showPage()


def _intro(c, text, x, top, width, size=None):
    """Lead paragraph under a page title, ink-muted. Returns its height (gap included)."""
    if not text:
        return 0
    size = size or PDFStyle.SIZE_BODY
    return draw_paragraph(c, str(text), x, top, width, PDFStyle.FONT_BODY, size, PDFStyle.COLOR_INK_MUTED) + 0.45 * cm


# --- Cover ---------------------------------------------------------------------

_CHAPTER_LABEL = re.compile(r"^\s*chapitre\s+(\d+)\s*[:·.\-–—]\s*(.+)$", re.IGNORECASE)


def split_chapter_label(label):
    """'CHAPITRE 4 : MON RAPPORT À L'ARGENT' -> ('4', 'MON RAPPORT À L'ARGENT'); (None, label) otherwise."""
    match = _CHAPTER_LABEL.match(str(label or ""))
    if match:
        return match.group(1), match.group(2).strip()
    return None, str(label or "").strip()


def as_title(text):
    """A former all-caps chapter name as a punctuated title: 'MON PARCOURS' -> 'Mon parcours.'"""
    text = " ".join(str(text).split())
    if text.isupper():
        text = text[:1] + text[1:].lower()
    if text and text[-1] not in ".!?…":
        text += "."
    return text


def create_cover_page(c, title, number=None, eyebrow=None, tagline=None, promise=None):
    """
    Cover of a workbook: logotype, a pastel disc cut by the corner, the eyebrow, the big
    chapter number in PT Mono blue, the title with its coral accent (see primitives.title_runs),
    and the workbook's promise on a post-it.
    """
    x, width = content_frame()
    disc_cx, disc_cy, disc_r = WIDTH - 1.0 * cm, HEIGHT * 0.62, 9.5 * cm
    draw_disc(c, disc_cx, disc_cy, disc_r, document_pastel(c))
    # Small coral disc riding the edge of the big one, like a punctuation mark
    draw_disc(c, disc_cx - disc_r * 0.72, disc_cy + disc_r * 0.69, 0.55 * cm, PDFStyle.COLOR_CORAL)
    draw_logotype(c, x, HEIGHT - 2.6 * cm, size=16)

    if promise:
        note_w, note_size = 6.6 * cm, PDFStyle.SIZE_POSTIT
        note_h = paragraph_height(promise, note_w - 1.2 * cm, PDFStyle.FONT_SERIF, note_size, note_size * 1.3) + 1.3 * cm
        note_x, note_y = WIDTH - PDFStyle.MARGIN_MAIN - note_w - 0.6 * cm, HEIGHT * 0.5
        with postit(c, note_x, note_y, note_w, note_h, angle=-3):
            draw_paragraph(c, promise, 0.6 * cm, note_h - 0.65 * cm, note_w - 1.2 * cm,
                           PDFStyle.FONT_SERIF, note_size, PDFStyle.COLOR_INK, note_size * 1.3)

    # The eyebrow, number and title sit in the lower third, above the tagline
    title_w = width * 0.92
    title_size = 46
    title_h = heading_height(title, title_w, size=title_size, min_size=30, max_lines=3,
                             tracking=PDFStyle.TRACKING_TITLE_XL)
    title_top = 3.6 * cm + title_h
    if eyebrow is None:
        eyebrow = f"Carnet de bord · chapitre {number}" if number not in (None, "") else "Carnet de bord"
    if number not in (None, ""):
        number_size = 130
        number_y = title_top + 0.8 * cm
        draw_number(c, x - 5, number_y, str(number).zfill(2) if str(number).isdigit() else number, size=number_size)
        draw_eyebrow(c, x, number_y + number_size * 0.8, eyebrow, max_width=width)
    else:
        draw_eyebrow(c, x, title_top + 0.5 * cm, eyebrow, max_width=width)
    draw_heading(c, title, x, title_top, title_w, size=title_size, min_size=30, max_lines=3,
                 tracking=PDFStyle.TRACKING_TITLE_XL)

    if tagline:
        draw_rule(c, x, x + width, 2.35 * cm, color=PDFStyle.COLOR_INK, width=0.75)
        draw_eyebrow(c, x, 1.6 * cm, tagline, max_width=width)
    c.showPage()


def create_standard_cover(c, subtitle, title="BILAN DE COMPÉTENCES & ALIGNEMENT", promise=None):
    """
    Former cover API: subtitle is the chapter label ('CHAPITRE 4 : MON RAPPORT À L'ARGENT'),
    title the line shown at the bottom. See create_cover_page.
    """
    number, name = split_chapter_label(subtitle)
    create_cover_page(c, as_title(name), number=number, tagline=title, promise=promise)


# --- Chapter opener (former summary page) --------------------------------------

def _point_text(point):
    if isinstance(point, (tuple, list)):
        label = str(point[0]).strip() if len(point) > 0 else ""
        desc = str(point[1]).strip() if len(point) > 1 else ""
        if desc and re.fullmatch(r"[\d.)\s]*", label):
            return desc
        return f"{label} {desc}".strip()
    return str(point).strip()


def create_standard_summary_page(c, chapter_num_str, chapter_title, intro_text, points_list):
    """
    Chapter opener: eyebrow, big number, title, objective, then the exercises of the
    chapter as a star list in a pastel card (EXERCICES & PROTOCOLES).
    intro_text is rendered as ReportLab paragraph markup (<b>, <br/>...): callers passing
    untrusted text must escape it first, as server/pdf_compiler.py does.
    """
    x, width = content_frame()
    items = [t for t in (_point_text(p) for p in points_list or []) if t]
    eyebrow = f"Carnet de bord · chapitre {chapter_num_str}" if chapter_num_str else "Carnet de bord"
    number = str(chapter_num_str or "")
    number_size = 130
    title_w = width * 0.85
    inner_w = width - 2 * PDFStyle.CARD_PADDING

    intro = None
    intro_h = 0
    if intro_text:
        style = ParagraphStyle(
            "OpenerIntro", fontName=PDFStyle.FONT_BODY, fontSize=PDFStyle.SIZE_LEAD,
            leading=PDFStyle.SIZE_LEAD * 1.5, textColor=PDFStyle.COLOR_INK_MUTED,
        )
        intro = Paragraph(intro_text, style)
        _, intro_h = intro.wrap(width * 0.88, HEIGHT)

    # Like a magazine opener: the eyebrow and the big number at the top beside a pastel
    # disc, the title, objective and exercises low on the page when they are short enough
    page_top = HEIGHT - PDFStyle.EYEBROW_TOP
    draw_disc(c, WIDTH + 0.5 * cm, HEIGHT - 2.5 * cm, 7.0 * cm, document_pastel(c))
    draw_eyebrow(c, x, page_top, eyebrow, max_width=width * 0.6)
    y = page_top - 0.6 * cm
    if number:
        draw_number(c, x - 6, y - number_size * 0.75, number.zfill(2) if number.isdigit() else number, size=number_size)
        y -= number_size * 0.75 + 0.8 * cm

    block_h = heading_height(chapter_title, title_w, size=34, min_size=24, max_lines=3) + 0.45 * cm
    block_h += intro_h + 0.7 * cm if intro else 0
    block_h += _exercises_card_height(items, inner_w) if items else 0
    y = min(y, PDFStyle.CONTENT_BOTTOM + 1.0 * cm + block_h)
    y = draw_heading(c, chapter_title, x, y, title_w, size=34, min_size=24, max_lines=3) - 0.45 * cm
    if intro:
        intro.drawOn(c, x, y - intro_h)
        y -= intro_h + 0.7 * cm

    remaining = items
    first = True
    while remaining or first:
        page_items, remaining = _fit_star_items(remaining, width - 2 * PDFStyle.CARD_PADDING, y - PDFStyle.CONTENT_BOTTOM)
        if page_items:
            _draw_exercises_card(c, x, y, width, page_items)
        if remaining:
            _finish_page(c)
            y = draw_page_head(c, chapter_title, eyebrow=eyebrow, suffix="(suite)") - 0.6 * cm
        first = False
    _finish_page(c)


def _exercises_card_height(items, inner_w):
    _, pill_h = label_pill_size("Exercices & protocoles")
    return 2 * PDFStyle.CARD_PADDING + pill_h + 0.45 * cm + star_list_height(items, inner_w)


def _fit_star_items(items, inner_w, available):
    """As many items as fit in an exercises card of the available height (at least one)."""
    count = len(items)
    while count > 1 and _exercises_card_height(items[:count], inner_w) > available:
        count -= 1
    return items[:count], items[count:]


def _draw_exercises_card(c, x, top, width, items):
    pad = PDFStyle.CARD_PADDING
    inner_w = width - 2 * pad
    h = _exercises_card_height(items, inner_w)
    draw_pastel_card(c, x, top - h, width, h)
    _, pill_h = draw_label_pill(c, x + pad, top - pad - label_pill_size("x")[1], "Exercices & protocoles", variant="on_pastel")
    draw_star_list(c, items, x + pad, top - pad - pill_h - 0.45 * cm, inner_w)
    return h


# --- End of the workbook ------------------------------------------------------

def create_standard_engagement_page(
    c,
    part_title,
    custom_lines=None,
    title="Votre livrable.",
    signature_label="Date de la séance",
    field_prefix="engagement",
    livrable_title=None,
    livrable_text=None,
):
    """
    End of the workbook: the deliverable on a jasmine post-it with the « Validé en séance »
    stamp, the session date and a validation box, then the commitments (custom_lines) as a
    checklist. signature_label names the date field (former signature block).
    """
    x, width = content_frame()
    form = c.acroForm
    y = draw_page_head(c, title or "Votre livrable.", eyebrow=part_title or "Fin de carnet") - 0.7 * cm

    lines = []
    for line in custom_lines or []:
        text = ((line.get("text") or line.get("line") or str(line)) if isinstance(line, dict) else str(line)).strip()
        if text:
            lines.append(text)

    # 1. The deliverable on a post-it, with the stamp
    livrable_title = livrable_title or "La synthèse de ce carnet"
    livrable_text = livrable_text or "À relire avec la personne qui vous accompagne lors de la prochaine séance."
    note_w = width * 0.62
    pad = 0.6 * cm
    inner = note_w - 2 * pad
    title_h = paragraph_height(livrable_title, inner, PDFStyle.FONT_HEADING_BOLD, 13, 13 * 1.3)
    text_h = paragraph_height(livrable_text, inner, PDFStyle.FONT_BODY, PDFStyle.SIZE_BODY)
    _, stamp_h = stamp_size()
    note_h = pad + 10 + 0.25 * cm + title_h + 0.15 * cm + text_h + 0.45 * cm + stamp_h + pad
    note_x, note_y = x + 0.2 * cm, y - note_h
    with postit(c, note_x, note_y, note_w, note_h, angle=-1):
        top = note_h - pad
        draw_eyebrow(c, pad, top - 8, "Livrable", tracking=PDFStyle.TRACKING_LABEL)
        top -= 10 + 0.25 * cm
        top -= draw_paragraph(c, livrable_title, pad, top, inner, PDFStyle.FONT_HEADING_BOLD, 13,
                              PDFStyle.COLOR_INK, 13 * 1.3)
        top -= 0.15 * cm
        draw_paragraph(c, livrable_text, pad, top, inner, PDFStyle.FONT_BODY, PDFStyle.SIZE_BODY, PDFStyle.COLOR_INK)
        stamp_w, _ = stamp_size()
        draw_stamp(c, pad + stamp_w / 2 + 2, pad + stamp_h / 2)

    # 2. Validation, beside the post-it
    side_x = note_x + note_w + 0.9 * cm
    side_w = x + width - side_x
    side_top = y - 0.2 * cm
    draw_eyebrow(c, side_x, side_top - 8, signature_label or "Date de la séance", max_width=side_w,
                 tracking=PDFStyle.TRACKING_LABEL)
    draw_answer_box(c, side_x, side_top - 0.45 * cm - 0.95 * cm, side_w, 0.95 * cm,
                    f"date_{field_prefix}", tooltip=signature_label or "Date de la séance", multiline=False)
    check_y = side_top - 0.45 * cm - 0.95 * cm - 0.85 * cm
    create_checkbox(form, f"valide_{field_prefix}", pos=(side_x, check_y), size=12, tooltip="Livrable validé en séance")
    draw_paragraph(c, "Livrable validé en séance", side_x + 18, check_y + 13, side_w - 18,
                   PDFStyle.FONT_BODY, PDFStyle.SIZE_BODY_SMALL, PDFStyle.COLOR_INK)

    # 3. Commitments
    y = note_y - 1.0 * cm
    if lines:
        draw_eyebrow(c, x, y - 8, "Mes engagements", max_width=width)
        y -= 8 + 0.45 * cm
        for i, text in enumerate(lines):
            h = paragraph_height(text, width - 20, PDFStyle.FONT_BODY, PDFStyle.SIZE_BODY)
            if y - h < PDFStyle.CONTENT_BOTTOM:
                _finish_page(c)
                y = draw_page_head(c, title or "Votre livrable.", eyebrow=part_title or "Fin de carnet",
                                   suffix="(suite)") - 0.7 * cm
            create_checkbox(form, f"{field_prefix}_{i + 1}", pos=(x, first_baseline(y, PDFStyle.SIZE_BODY, PDFStyle.SIZE_BODY * 1.5) - 2),
                            size=11, tooltip=text)
            y -= draw_paragraph(c, text, x + 20, y, width - 20) + 0.25 * cm
        y -= 0.75 * cm

    # 4. The rest of the page: notes to bring to the next session
    if y - PDFStyle.CONTENT_BOTTOM > 3.5 * cm:
        draw_eyebrow(c, x, y - 8, "Mes notes pour la prochaine séance", max_width=width)
        y -= 8 + 0.35 * cm
        draw_answer_box(c, x, PDFStyle.CONTENT_BOTTOM, width, y - PDFStyle.CONTENT_BOTTOM, f"notes_{field_prefix}",
                        tooltip="Mes notes pour la prochaine séance")
    _finish_page(c)


def create_closing_page(c, messages=None):
    """
    Back cover: the art direction's single big blue block (the moment of action), with
    jasmine and coral discs cut by its edges, the signature and a few lines in white.
    """
    x, width = content_frame()
    block_x, block_y, block_w, block_h = x, 2.2 * cm, width, HEIGHT - 4.4 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BLUE)
    c.roundRect(block_x, block_y, block_w, block_h, 24, stroke=0, fill=1)
    clip = c.beginPath()
    clip.roundRect(block_x, block_y, block_w, block_h, 24)
    c.clipPath(clip, stroke=0, fill=0)
    draw_disc(c, block_x + block_w, block_y + block_h, 6.5 * cm, PDFStyle.COLOR_JASMINE)
    draw_disc(c, block_x + 2.2 * cm, block_y, 1.6 * cm, PDFStyle.COLOR_CORAL)
    c.restoreState()

    y = HEIGHT * 0.5
    text = "marge de manœuvre"
    size = 34
    w = text_width(text, PDFStyle.FONT_LOGO, size, -0.05)
    draw_text(c, WIDTH / 2 - w / 2, y, text, PDFStyle.FONT_LOGO, size, PDFStyle.COLOR_SURFACE_CARD, -0.05)
    draw_disc(c, WIDTH / 2 + w / 2 + 0.04 * size + 0.085 * size, y + 0.085 * size, 0.085 * size, PDFStyle.COLOR_JASMINE)

    if messages is None:
        messages = [
            "Ce carnet reste le vôtre.",
            "Gardez-le à portée de main pour la prochaine séance.",
        ]
    y -= 1.4 * cm
    for msg in messages:
        text = (msg.get("text") or str(msg)) if isinstance(msg, dict) else str(msg)
        text = text.strip()
        if not text:
            continue
        y -= draw_paragraph(c, text, x + width * 0.1, y, width * 0.8, PDFStyle.FONT_BODY, PDFStyle.SIZE_LEAD,
                            PDFStyle.COLOR_SURFACE_CARD, align="center") + 0.15 * cm
    c.showPage()


# --- Recap of the previous session ----------------------------------------------

def create_standard_recap_page(c, part_title, intro_txt, questions):
    """Recap of the previous session: an intro, then one answer box per question."""
    x, width = content_frame()
    title = "Récapitulatif de la séance précédente."
    y = draw_page_head(c, title, eyebrow=part_title) - 0.5 * cm
    y -= _intro(c, intro_txt, x, y, width)

    questions = list(questions or [])
    texts = [question_text_height(width, q) for q in questions]
    gap = 0.6 * cm
    available = y - PDFStyle.CONTENT_BOTTOM - sum(texts) - gap * max(len(questions) - 1, 0)
    box_h = max(2.2 * cm, min(4.6 * cm, available / max(len(questions), 1)))
    for i, question in enumerate(questions):
        if y - texts[i] - box_h < PDFStyle.CONTENT_BOTTOM:
            _finish_page(c)
            y = draw_page_head(c, title, eyebrow=part_title, suffix="(suite)") - 0.5 * cm
        y = draw_question(c, x, y, width, question, f"recap_q{i + 1}", box_h) - gap
    _finish_page(c)


# --- Inner weather ------------------------------------------------------------------

_WEATHER = [("Soleil", "sunny"), ("Nuageux", "partly_cloudy_day"), ("Pluvieux", "rainy"), ("Orageux", "thunderstorm")]


def create_standard_meteo_page(
    c,
    title="Mon état d'esprit actuel.",
    part_title=None,
    emotion_prompt="Aujourd'hui, je me sens :",
    energy_prompt="Mon niveau d'énergie :",
    thought_prompt="Ce qui prend le plus de place dans ma tête :",
    field_prefix="meteo",
):
    """
    Inner weather check-in: a word for the mood and four weather boxes (icons), the energy
    level from 0 to 10 (pastilles, a single choice), and a large box for what fills the mind.
    """
    x, width = content_frame()
    form = c.acroForm
    y = draw_page_head(c, title, eyebrow=part_title) - 0.6 * cm
    pad, gap = QUESTION_PAD, 0.4 * cm
    inner_x, inner_w = x + pad, width - 2 * pad
    pastels = pastel_cycle(c)

    def prompt_h(text):
        return paragraph_height(text, inner_w, PDFStyle.FONT_HEADING_BOLD, QUESTION_SIZE, QUESTION_LEADING) + QUESTION_GAP_TO_BOX

    def draw_prompt(text, top):
        return draw_paragraph(c, text, inner_x, top, inner_w, PDFStyle.FONT_HEADING_BOLD, QUESTION_SIZE,
                              PDFStyle.COLOR_INK, QUESTION_LEADING) + QUESTION_GAP_TO_BOX

    # 1. Mood: a word, then four weather boxes
    badge = 1.15 * cm
    card_h = 2 * pad + prompt_h(emotion_prompt) + 0.95 * cm + 0.5 * cm + badge
    draw_pastel_card(c, x, y - card_h, width, card_h, color=pastels[0], radius=12)
    t = y - pad
    t -= draw_prompt(emotion_prompt, t)
    draw_answer_box(c, inner_x, t - 0.95 * cm, inner_w, 0.95 * cm, f"{field_prefix}_emotion_word",
                    tooltip="Un mot pour décrire l'instant", multiline=False)
    t -= 0.95 * cm + 0.5 * cm
    col_w = inner_w / len(_WEATHER)
    for i, (label, icon) in enumerate(_WEATHER):
        col_x = inner_x + i * col_w
        create_checkbox(form, f"{field_prefix}_{label}", pos=(col_x, t - badge / 2 - 6), size=12, tooltip=label)
        draw_icon_badge(c, col_x + 20 + badge / 2, t - badge / 2, icon, diameter=badge, on_pastel=True)
        draw_text(c, col_x + 20 + badge + 6, t - badge / 2 - 3.5, label, PDFStyle.FONT_BODY, PDFStyle.SIZE_BODY,
                  PDFStyle.COLOR_INK)
    y -= card_h + gap

    # 2. Energy from 0 to 10
    scale_h = choice_scale_height(True)
    card_h = 2 * pad + prompt_h(energy_prompt) + scale_h
    draw_pastel_card(c, x, y - card_h, width, card_h, color=pastels[1], radius=12)
    t = y - pad
    t -= draw_prompt(energy_prompt, t)
    group = reserve_field_name(form, f"{field_prefix}_energy")
    draw_choice_scale(c, group, inner_x, t, inner_w, list(range(11)), "Épuisé (0)", "Plein d'énergie (10)", tooltip="Niveau")
    y -= card_h + gap

    # 3. What fills the mind: the rest of the page
    card_h = max(3.0 * cm + 2 * pad + prompt_h(thought_prompt), y - PDFStyle.CONTENT_BOTTOM)
    draw_pastel_card(c, x, y - card_h, width, card_h, color=pastels[0], radius=12)
    t = y - pad
    t -= draw_prompt(thought_prompt, t)
    draw_answer_box(c, inner_x, y - card_h + pad, inner_w, t - (y - card_h + pad), f"{field_prefix}_pensee",
                    tooltip="Pensée envahissante ou intention")
    _finish_page(c)


# --- Four quadrants -------------------------------------------------------------

def _quadrant_item(item, field_prefix):
    if isinstance(item, (tuple, list)):
        title = str(item[0]) if item else ""
        sub = str(item[1]) if len(item) > 1 and item[1] else ""
        fid = item[2] if len(item) > 2 else f"{field_prefix}_{title}"
    elif isinstance(item, dict):
        title = str(item.get("title", ""))
        sub = str(item.get("subtitle", "") or "")
        fid = item.get("field_id") or f"{field_prefix}_{title}"
    else:
        title, sub, fid = str(item), "", f"{field_prefix}_{item}"
    return title, sub, fid


def create_standard_quadrants_page(
    c,
    title="Ma vision à 360°.",
    part_title=None,
    instruction="Pour chaque domaine, écrivez une phrase de synthèse sur votre aspiration.",
    quadrants_data=None,
    field_prefix="vision",
):
    """
    Four domains as a 2 x 2 grid of pastel cards, each with its answer box.
    quadrants_data: tuples (title, keywords, field_id) or dicts {title, subtitle, field_id}.
    Beyond 4 quadrants, the remaining ones continue on pages titled "(suite)".
    """
    if not quadrants_data:
        quadrants_data = [
            ("Professionnel", "Sens, mission, salaire", "pro"),
            ("Personnel", "Temps pour soi, santé", "perso"),
            ("Social et familial", "Relations, équilibre", "social"),
            ("Cadre de travail", "Besoin de cadre ou de liberté", "cadre"),
        ]
    quadrants_data = list(quadrants_data)
    for start in range(0, len(quadrants_data), 4):
        _draw_quadrants_page(
            c, title, part_title, instruction if start == 0 else None,
            quadrants_data[start:start + 4], field_prefix, suffix="(suite)" if start else "",
        )


def _draw_quadrants_page(c, title, part_title, instruction, quadrants_data, field_prefix, suffix=""):
    x, width = content_frame()
    y = draw_page_head(c, title, eyebrow=part_title, suffix=suffix) - 0.6 * cm
    y -= _intro(c, instruction, x, y, width)

    gap = 0.45 * cm
    card_w = (width - gap) / 2
    card_h = (y - PDFStyle.CONTENT_BOTTOM - gap) / 2
    pad = PDFStyle.CARD_PADDING
    inner = card_w - 2 * pad
    pastels = pastel_cycle(c)
    for i, item in enumerate(quadrants_data):
        q_title, sub, fid = _quadrant_item(item, field_prefix)
        cx = x + (i % 2) * (card_w + gap)
        top = y - (i // 2) * (card_h + gap)
        draw_pastel_card(c, cx, top - card_h, card_w, card_h, color=pastels[i % len(pastels)])
        t = top - pad
        t = draw_heading(c, q_title, cx + pad, t, inner, size=PDFStyle.SIZE_TITLE_CARD, min_size=10,
                         font=PDFStyle.FONT_HEADING_BOLD, tracking=PDFStyle.TRACKING_TITLE_CARD, max_lines=2,
                         accent_color=PDFStyle.COLOR_INK)
        if sub:
            t -= 2 + draw_paragraph(c, sub, cx + pad, t - 2, inner, PDFStyle.FONT_BODY, HINT_SIZE,
                                    PDFStyle.COLOR_INK_MUTED, HINT_LEADING, max_lines=2)
        t -= 0.3 * cm
        draw_answer_box(c, cx + pad, top - card_h + pad, inner, t - (top - card_h + pad), fid, tooltip=f"Synthèse {q_title}")
    _finish_page(c)


# --- Two columns ----------------------------------------------------------------

def create_standard_two_columns_page(
    c,
    title,
    part_title=None,
    intro_text=None,
    col1_header="Situation / Expérience",
    col2_header="Enseignement / Compétence",
    rows_data=None,
    field_prefix="twocol",
):
    """
    Two-column comparison: for each row, a label then two answer boxes joined by an arrow.
    rows_data: labels, tuples (label, left tip, right tip) or dicts (label, left/right...).
    Rows that do not fit continue on pages titled "(suite)", headers repeated.
    """
    if not rows_data:
        rows_data = [
            "1. Première situation marquante",
            "2. Deuxième situation marquante",
            "3. Troisième situation marquante",
            "4. Autre élément clé",
        ]

    # Global indexes keep field ids stable and unique across continuation pages
    remaining = list(enumerate(rows_data))
    first = True
    while remaining:
        remaining = _draw_two_columns_page(
            c, title, part_title, intro_text if first else None, col1_header, col2_header,
            remaining, field_prefix, suffix="" if first else "(suite)",
        )
        first = False


def _two_columns_row(i, item):
    if isinstance(item, str):
        return item, item, f"Enseignement {i+1}"
    if isinstance(item, dict):
        left_tip = (item.get("left") or item.get("col1") or item.get("left_tooltip")
                    or item.get("situation") or item.get("croyance") or "")
        right_tip = (item.get("right") or item.get("col2") or item.get("right_tooltip") or item.get("solution")
                     or item.get("levier") or item.get("enseignement") or f"Enseignement {i+1}")
        label = item.get("label") or item.get("title")
        if not label:
            label = f"{i+1}. {(left_tip[:40] + '...') if len(left_tip) > 40 else left_tip}" if left_tip else f"Point {i+1}"
        return str(label), str(left_tip), str(right_tip)
    if isinstance(item, (tuple, list)):
        label = str(item[0]) if item else f"Point {i+1}"
        return label, str(item[1]) if len(item) > 1 else label, str(item[2]) if len(item) > 2 else f"Enseignement {i+1}"
    return str(item), str(item), f"Enseignement {i+1}"


def _draw_two_columns_page(c, title, part_title, intro_text, col1_header, col2_header, rows, field_prefix, suffix=""):
    """Draws as many rows as fit on one page and returns the rows left for the next one."""
    x, width = content_frame()
    y = draw_page_head(c, title, eyebrow=part_title, suffix=suffix) - 0.6 * cm
    y -= _intro(c, intro_text, x, y, width)

    arrow_w = 0.9 * cm
    pad = 0.4 * cm
    col_w = (width - 2 * pad - arrow_w) / 2
    col2_x = x + pad + col_w + arrow_w
    head_size = 10.5
    head_lead = head_size * 1.25
    h1 = draw_paragraph(c, col1_header, x + pad, y, col_w, PDFStyle.FONT_HEADING_BOLD, head_size, PDFStyle.COLOR_INK,
                        head_lead, max_lines=2)
    h2 = draw_paragraph(c, col2_header, col2_x, y, col_w, PDFStyle.FONT_HEADING_BOLD, head_size, PDFStyle.COLOR_BLUE,
                        head_lead, max_lines=2)
    y -= max(h1, h2) + 0.2 * cm
    draw_rule(c, x, x + width, y, color=PDFStyle.COLOR_LINE_STRONG, width=0.75)
    y -= 0.45 * cm

    label_size, label_lead = PDFStyle.SIZE_BODY_SMALL, PDFStyle.SIZE_BODY_SMALL * 1.35
    min_box, max_box, row_gap = 1.5 * cm, 5.0 * cm, 0.45 * cm
    available = y - PDFStyle.CONTENT_BOTTOM

    def label_h(row):
        return 2 * pad + paragraph_height(_two_columns_row(*row)[0], width - 2 * pad, PDFStyle.FONT_BODY_BOLD,
                                          label_size, label_lead, max_lines=2)

    page_rows, used = [], 0
    for row in rows:
        need = label_h(row) + 4 + min_box + row_gap
        if page_rows and used + need > available:
            break
        page_rows.append(row)
        used += need
    rest = rows[len(page_rows):]
    labels_total = sum(label_h(r) + 4 + row_gap for r in page_rows)
    box_h = max(min_box, min(max_box, (available - labels_total) / max(len(page_rows), 1)))

    for row in page_rows:
        i, item = row
        label, left_tip, right_tip = _two_columns_row(i, item)
        row_h = label_h(row) + 4 + box_h
        draw_pastel_card(c, x, y - row_h, width, row_h, radius=12)
        y -= pad
        y -= draw_paragraph(c, label, x + pad, y, width - 2 * pad, PDFStyle.FONT_BODY_BOLD, label_size, PDFStyle.COLOR_INK,
                            label_lead, max_lines=2) + 4
        draw_answer_box(c, x + pad, y - box_h, col_w, box_h, f"{field_prefix}_col1_{i+1}", tooltip=left_tip)
        draw_answer_box(c, col2_x, y - box_h, col_w, box_h, f"{field_prefix}_col2_{i+1}", tooltip=right_tip)
        draw_filled_arrow(c, x + pad + col_w + (arrow_w - 12) / 2, y - box_h / 2 - 4, width=12)
        y -= box_h + pad + row_gap

    _finish_page(c)
    return rest


# --- Field survey (enquête) -------------------------------------------------------

def create_standard_enquete_page(
    c,
    title="Fiche enquête réseau et métier.",
    part_title="Exploration du terrain",
    intro_text="Interrogez un professionnel ou un pair pour confronter vos hypothèses à la réalité du terrain, sans chercher à vendre.",
    questions=None,
    field_prefix="enquete",
):
    """
    Field survey sheet: the contact card (name, role, company, date), then one answer box
    per question. Questions that do not fit continue on pages titled "(suite)".
    """
    if not questions:
        questions = [
            ("1. Besoins et difficultés réelles",
             "Quelles difficultés majeures cette personne rencontre-t-elle au quotidien ?"),
            ("2. Solutions actuelles et limites",
             "Que fait-elle aujourd'hui pour y répondre ? Qu'est-ce qui lui manque ?"),
            ("3. Conseils et contacts",
             "Quels conseils, quel avis sur votre projet, quels autres contacts vous a-t-elle donnés ?"),
        ]

    remaining = list(enumerate(questions))
    first = True
    while remaining:
        remaining = _draw_enquete_page(
            c, title, part_title, intro_text if first else None, remaining, field_prefix,
            with_contact_card=first, suffix="" if first else "(suite)",
        )
        first = False


def _enquete_question(i, q):
    if isinstance(q, (tuple, list)):
        return (str(q[0]) if q else f"Question {i+1}"), (str(q[1]) if len(q) > 1 else "")
    if isinstance(q, dict):
        return (str(q.get("title") or q.get("question") or q.get("label") or f"Question {i+1}"),
                str(q.get("subtitle") or q.get("desc") or q.get("description") or ""))
    return str(q), ""


def _draw_enquete_page(c, title, part_title, intro_text, questions, field_prefix, with_contact_card, suffix=""):
    """Draws as many questions as fit on one page and returns the ones left for the next one."""
    x, width = content_frame()
    y = draw_page_head(c, title, eyebrow=part_title, suffix=suffix) - 0.6 * cm
    y -= _intro(c, intro_text, x, y, width)

    if with_contact_card:
        pad = PDFStyle.CARD_PADDING
        col_gap = 0.45 * cm
        col_w = (width - 2 * pad - col_gap) / 2
        field_h = 0.8 * cm
        row_h = 9 + 0.2 * cm + field_h
        card_h = 2 * pad + 2 * row_h + 0.35 * cm
        draw_pastel_card(c, x, y - card_h, width, card_h)
        fields = [
            ("Interlocuteur (nom, prénom)", "contact_nom"), ("Fonction, rôle", "contact_role"),
            ("Entreprise, secteur", "contact_ent"), ("Date et contexte de l'échange", "contact_date"),
        ]
        for k, (label, key) in enumerate(fields):
            fx = x + pad + (k % 2) * (col_w + col_gap)
            ftop = y - pad - (k // 2) * (row_h + 0.35 * cm)
            draw_eyebrow(c, fx, ftop - 7, label, size=PDFStyle.SIZE_LABEL, tracking=PDFStyle.TRACKING_LABEL,
                         max_width=col_w)
            draw_answer_box(c, fx, ftop - row_h, col_w, field_h, f"{field_prefix}_{key}", tooltip=label, multiline=False)
        y -= card_h + 0.75 * cm

    gap = 0.6 * cm
    min_box = 2.2 * cm
    available = y - PDFStyle.CONTENT_BOTTOM
    texts = [question_text_height(width, *_enquete_question(i, q)) for i, q in questions]
    count, used = 0, 0
    for t in texts:
        if count and used + t + min_box > available:
            break
        used += t + min_box + gap
        count += 1
    page_questions, rest = questions[:count], questions[count:]
    box_h = max(min_box, min(6.5 * cm, (available - sum(texts[:count]) - gap * (count - 1)) / max(count, 1)))

    for i, q in page_questions:
        q_title, q_sub = _enquete_question(i, q)
        y = draw_question(c, x, y, width, q_title, f"{field_prefix}_q_{i+1}", box_h, subtitle=q_sub or None) - gap

    _finish_page(c)
    return rest


# --- Roadmap ----------------------------------------------------------------------

def _as_action_list(actions):
    """Normalizes roadmap actions (Gemini may send a single string or dicts) into a list of labels."""
    if isinstance(actions, str):
        actions = [actions]
    labels = []
    for action in actions or []:
        if isinstance(action, dict):
            action = action.get("label") or action.get("text") or action.get("action") or action.get("title") or ""
        labels.append(str(action))
    return labels or ["Action 1", "Action 2", "Action 3"]


ROADMAP_ACTION_H = 0.95 * cm
ROADMAP_ACTION_GAP = 0.2 * cm


def _roadmap_stage_height(n_actions):
    """Card height for a stage listing n_actions actions (3 rows at least)."""
    head = PDFStyle.CARD_PADDING + 18 + 0.45 * cm
    actions = 9 + 0.25 * cm + max(n_actions, 3) * (ROADMAP_ACTION_H + ROADMAP_ACTION_GAP)
    return head + actions + PDFStyle.CARD_PADDING


def create_standard_roadmap_page(
    c,
    title="Feuille de route à 30, 60 et 90 jours.",
    part_title="Plan d'action",
    intro_text="Découpez votre passage à l'action en trois paliers, avec un objectif, un résultat observable et des actions datées.",
    stages_data=None,
    field_prefix="roadmap",
):
    """
    Roadmap in stages: each stage card has its period (blue pill) and focus, the objective
    and the observable result on the left, the priority actions with check boxes on the
    right (the card grows beyond 3 actions). Stages that do not fit continue on pages
    titled "(suite)".
    """
    if not stages_data:
        stages_data = [
            {
                "period": "Palier 1 · 0 à 30 jours",
                "theme": "Consolider et tester",
                "default_obj": "Valider l'intérêt du marché et tester l'offre pilote auprès de 5 pairs.",
                "actions": [
                    "Mener 5 entretiens d'enquête terrain ciblés",
                    "Formaliser la proposition de valeur sur 1 page",
                    "Identifier et contacter 2 premiers prospects",
                ],
                "default_kpi": "5 entretiens menés et 1 retour d'intérêt concret",
            },
            {
                "period": "Palier 2 · 30 à 60 jours",
                "theme": "Structurer et sécuriser",
                "default_obj": "Poser le cadre juridique, fixer les tarifs et préparer le lancement.",
                "actions": [
                    "Valider le statut juridique et les aides de transition (ARE, ARCE)",
                    "Fixer la grille tarifaire et le modèle de devis",
                    "Annoncer le lancement à son réseau",
                ],
                "default_kpi": "Cadre juridique validé et 3 devis envoyés",
            },
            {
                "period": "Palier 3 · 60 à 90 jours",
                "theme": "Lancer et développer",
                "default_obj": "Signer les premières missions, recueillir des retours et caler son rythme.",
                "actions": [
                    "Signer et réaliser la première mission pilote",
                    "Recueillir une recommandation client",
                    "Faire le bilan d'étape et ajuster les priorités du trimestre",
                ],
                "default_kpi": "Premier chiffre d'affaires encaissé et premier avis client obtenu",
            },
        ]

    stages = []
    for i, stage in enumerate(stages_data):
        if isinstance(stage, dict):
            stages.append((i, {
                "period": str(stage.get("period") or stage.get("palier") or f"Palier {i+1}"),
                "theme": str(stage.get("theme") or stage.get("title") or ""),
                "obj": str(stage.get("default_obj") or stage.get("obj") or stage.get("objective") or stage.get("objectif") or ""),
                "actions": _as_action_list(stage.get("actions") or stage.get("items")),
                "kpi": str(stage.get("default_kpi") or stage.get("kpi") or stage.get("resultat") or ""),
            }))
        else:
            stages.append((i, {"period": f"Palier {i+1}", "theme": str(stage), "obj": "",
                               "actions": _as_action_list(None), "kpi": ""}))

    first = True
    while stages:
        stages = _draw_roadmap_page(c, title, part_title, intro_text if first else None, stages, field_prefix,
                                    suffix="" if first else "(suite)")
        first = False


def _draw_roadmap_page(c, title, part_title, intro_text, stages, field_prefix, suffix=""):
    """Draws as many stages as fit on one page and returns the ones left for the next one."""
    x, width = content_frame()
    form = c.acroForm
    y = draw_page_head(c, title, eyebrow=part_title, suffix=suffix) - 0.6 * cm
    y -= _intro(c, intro_text, x, y, width)

    gap = 0.45 * cm
    available = y - PDFStyle.CONTENT_BOTTOM
    page_stages, used = [], 0
    for stage in stages:
        h = _roadmap_stage_height(len(stage[1]["actions"]))
        if page_stages and used + h > available:
            break
        page_stages.append(stage)
        used += h + gap
    rest = stages[len(page_stages):]

    pad = PDFStyle.CARD_PADDING
    for i, stage in page_stages:
        stage_h = _roadmap_stage_height(len(stage["actions"]))
        draw_pastel_card(c, x, y - stage_h, width, stage_h)

        # Header: period in a blue pill, then the stage's focus
        top = y - pad
        pill_w, pill_h = draw_label_pill(c, x + pad, top - 18, stage["period"], variant="solid", max_width=width * 0.45)
        if stage["theme"]:
            theme_x = x + pad + pill_w + 0.35 * cm
            draw_text(c, theme_x, top - 18 + (pill_h - 9) / 2 + 1.2,
                      ellipsize(stage["theme"], PDFStyle.FONT_HEADING_BOLD, 11.5, x + width - pad - theme_x),
                      PDFStyle.FONT_HEADING_BOLD, 11.5, PDFStyle.COLOR_INK)
        top -= 18 + 0.45 * cm

        # Left column: objective and observable result
        left_w = width * 0.4 - pad
        right_x = x + pad + left_w + 0.6 * cm
        right_w = x + width - pad - right_x
        block_h = (top - (y - stage_h + pad) - 2 * (9 + 0.25 * cm) - 0.35 * cm) / 2
        t = top
        for label, key, value in (("Cap et objectif", "obj", stage["obj"]), ("Résultat observable", "kpi", stage["kpi"])):
            draw_eyebrow(c, x + pad, t - 7, label, size=PDFStyle.SIZE_LABEL, tracking=PDFStyle.TRACKING_LABEL,
                         max_width=left_w)
            t -= 9 + 0.25 * cm
            draw_answer_box(c, x + pad, t - block_h, left_w, block_h, f"{field_prefix}_s{i+1}_{key}",
                            tooltip=value, value=value, font_size=8.5)
            t -= block_h + 0.35 * cm
        c.saveState()
        c.setStrokeColor(PDFStyle.COLOR_INK, alpha=0.15)
        c.setLineWidth(0.75)
        c.setDash(2, 2)
        c.line(right_x - 0.3 * cm, top, right_x - 0.3 * cm, y - stage_h + pad)
        c.restoreState()

        # Right column: actions with check boxes
        actions = stage["actions"]
        label = f"{len(actions)} actions prioritaires" if len(actions) > 1 else "Action prioritaire"
        draw_eyebrow(c, right_x, top - 7, label, size=PDFStyle.SIZE_LABEL, tracking=PDFStyle.TRACKING_LABEL,
                     max_width=right_w)
        t = top - 9 - 0.25 * cm
        for a_idx, act_label in enumerate(actions):
            box_y = t - ROADMAP_ACTION_H
            create_checkbox(form, f"{field_prefix}_s{i+1}_chk_{a_idx+1}", pos=(right_x, box_y + (ROADMAP_ACTION_H - 11) / 2),
                            size=11, tooltip=f"Cocher l'action {a_idx+1}")
            draw_answer_box(c, right_x + 18, box_y, right_w - 18, ROADMAP_ACTION_H,
                            f"{field_prefix}_s{i+1}_act_{a_idx+1}", tooltip=act_label, value=act_label, font_size=8)
            t -= ROADMAP_ACTION_H + ROADMAP_ACTION_GAP

        y -= stage_h + gap

    _finish_page(c)
    return rest
