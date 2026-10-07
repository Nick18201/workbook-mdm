"""
Drawing primitives of the « Éditorial & Affirmé » art direction (DA-workbook.md, design-system/).

Coordinates are in points with the origin at the bottom left. Unless stated otherwise,
(x, y) is the baseline start of a text or the bottom-left corner of a shape, and a `top`
argument is the top of a text block. Every primitive restores the canvas state it changes
(colors, fonts, character spacing), so they can be chained freely.
"""

import functools
import io
import os
import re
from contextlib import contextmanager

from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from svglib.svglib import svg2rlg

from .config import PDFStyle
from .document_builder import document_pastel, document_style
from .utils import cached_simpleSplit, french_typography, split_words


# --- Text --------------------------------------------------------------------

def text_width(text, font, size, tracking=0.0):
    """Width of one line drawn by draw_text (tracking in em, added between characters)."""
    if not text:
        return 0.0
    text = french_typography(str(text))
    return pdfmetrics.stringWidth(text, font, size) + tracking * size * (len(text) - 1)


def draw_text(c, x, y, text, font, size, color, tracking=0.0, align="left"):
    """
    Draws one line of text and returns its width. The character spacing (PDF operator Tc)
    is part of the graphics state: it is restored here, otherwise it would leak into every
    text drawn afterwards. Every text primitive applies the French typography
    (utils.french_typography).
    """
    text = french_typography(str(text))
    width = text_width(text, font, size, tracking)
    if align == "center":
        x -= width / 2
    elif align == "right":
        x -= width
    c.saveState()
    t = c.beginText(x, y)
    t.setFont(font, size)
    if tracking:
        t.setCharSpace(tracking * size)
    t.setFillColor(color)
    t.textOut(text)
    c.drawText(t)
    c.restoreState()
    return width


def fit_text(text, font, size, max_width, tracking=0.0):
    """Shortens text with a visible '…' so that it fits max_width (never cuts silently)."""
    text = french_typography(str(text))
    if text_width(text, font, size, tracking) <= max_width:
        return text
    while text and text_width(text + "…", font, size, tracking) > max_width:
        text = text[:-1]
    return text.rstrip() + "…"


def wrap_text(text, font, size, max_width, tracking=0.0):
    """
    Splits text into lines of at most max_width (explicit line breaks are kept). A word
    wider than max_width gets a line of its own. A no-break space never breaks a line.
    """
    text = french_typography(str(text))
    if not tracking:
        lines = []
        for paragraph in str(text).split("\n"):
            lines.extend(cached_simpleSplit(paragraph, font, size, max_width) or [""])
        return lines

    lines = []
    for paragraph in str(text).split("\n"):
        words = split_words(paragraph)
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            candidate = f"{line} {word}"
            if text_width(candidate, font, size, tracking) <= max_width:
                line = candidate
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def first_baseline(top, size, leading):
    """Baseline of the first line of a text block whose top is `top`."""
    return top - (leading - size) / 2 - 0.8 * size


def draw_paragraph(c, text, x, top, width, font=None, size=None, color=None, leading=None,
                   tracking=0.0, align="left", max_lines=None):
    """
    Draws wrapped text below `top` and returns the height it takes (lines x leading).
    With max_lines, the last line ends with '…' when the text is longer.
    """
    font = font or PDFStyle.FONT_BODY
    size = size or PDFStyle.SIZE_BODY
    color = color or PDFStyle.COLOR_INK
    leading = leading or size * PDFStyle.LEADING_BODY
    lines = wrap_text(text, font, size, width, tracking)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines - 1] + [fit_text(" ".join(lines[max_lines - 1:]), font, size, width, tracking)]
    y = first_baseline(top, size, leading)
    anchor = {"center": x + width / 2, "right": x + width}.get(align, x)
    for line in lines:
        if line:
            draw_text(c, anchor, y, line, font, size, color, tracking, align)
        y -= leading
    return len(lines) * leading


def paragraph_height(text, width, font=None, size=None, leading=None, tracking=0.0, max_lines=None):
    """Height draw_paragraph will take for this text."""
    font = font or PDFStyle.FONT_BODY
    size = size or PDFStyle.SIZE_BODY
    leading = leading or size * PDFStyle.LEADING_BODY
    n = len(wrap_text(text, font, size, width, tracking))
    if max_lines:
        n = min(n, max_lines)
    return n * leading


# --- Titles ------------------------------------------------------------------

_ACCENT = re.compile(r"\*([^*]+)\*")


def title_runs(title):
    """
    Splits a title into (text, is_accent) runs. *…* marks the accent (« Mon rapport
    *à l'argent.* »); without it, the last word is the accent, as in « Prenez de la *marge.* ».
    """
    title = french_typography(" ".join(split_words(title)))
    if _ACCENT.search(title):
        runs, pos = [], 0
        for match in _ACCENT.finditer(title):
            runs.append((title[pos:match.start()], False))
            runs.append((match.group(1), True))
            pos = match.end()
        runs.append((title[pos:], False))
        return [(text.replace("*", ""), accent) for text, accent in runs if text.replace("*", "").strip()]
    title = title.replace("*", "")
    head, _, last = title.rpartition(" ")
    return [(head, False), (last, True)] if head else [(last, True)]


def plain_title(title):
    """The title text without accent marks."""
    return " ".join(text.strip() for text, _ in title_runs(title))


def _greedy_lines(words, font, size, tracking, max_width):
    lines, line = [], []
    for word in words:
        candidate = line + [word]
        if line and text_width(" ".join(w for w, _ in candidate), font, size, tracking) > max_width:
            lines.append(line)
            line = [word]
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def _balanced_lines(words, font, size, tracking, max_width):
    """Greedy lines, then the narrowest width that keeps the same number of lines (text-wrap: balance)."""
    lines = _greedy_lines(words, font, size, tracking, max_width)
    if len(lines) < 2:
        return lines
    widest_word = max(text_width(w, font, size, tracking) for w, _ in words)
    low, high, best = max(widest_word, max_width / 2), max_width, lines
    for _ in range(10):
        mid = (low + high) / 2
        candidate = _greedy_lines(words, font, size, tracking, mid)
        if len(candidate) <= len(lines):
            best, high = candidate, mid
        else:
            low = mid
    return best


def heading_layout(title, max_width, size=None, font=None, tracking=None, min_size=None, max_lines=3, suffix=""):
    """
    Lines of a title: [(word, is_accent), ...] per line, and the font size used. The size
    shrinks (down to min_size) until the title fits in max_lines lines.
    """
    font = font or PDFStyle.FONT_HEADING
    size = size or PDFStyle.SIZE_TITLE_PAGE
    tracking = PDFStyle.TRACKING_TITLE if tracking is None else tracking
    min_size = min_size or size
    words = [(w, accent) for text, accent in title_runs(title) for w in split_words(text)]
    words += [(w, False) for w in split_words(suffix)]
    while True:
        lines = _balanced_lines(words, font, size, tracking, max_width)
        if len(lines) <= max_lines or size <= min_size:
            return lines, size
        size = max(min_size, size - 1)


def draw_heading(c, title, x, top, max_width, size=None, font=None, color=None, accent_color=None,
                 tracking=None, min_size=None, max_lines=3, leading=None, suffix=""):
    """
    Draws a title in ink with its accent run (see title_runs) in coral, balanced over its
    lines. Bright coral text is only legible from 18 pt on cream or white: the default
    accent is PDFStyle.COLOR_TITLE_ACCENT (bright coral on the ivory pages) and coral-strong
    below 18 pt. `suffix` is appended without accent, e.g. " (suite)". Returns the bottom y
    of the block.
    """
    font = font or PDFStyle.FONT_HEADING
    tracking = PDFStyle.TRACKING_TITLE if tracking is None else tracking
    color = color or PDFStyle.COLOR_INK
    lines, size = heading_layout(title, max_width, size, font, tracking, min_size, max_lines, suffix)
    if accent_color is None:
        accent_color = PDFStyle.COLOR_TITLE_ACCENT if size >= 18 else PDFStyle.COLOR_CORAL_STRONG
    leading = leading or size * PDFStyle.LEADING_TITLE

    y = first_baseline(top, size, leading)
    for line in lines:
        cursor = x
        c.saveState()
        t = c.beginText(cursor, y)
        t.setFont(font, size)
        t.setCharSpace(tracking * size)
        for i, (word, accent) in enumerate(line):
            t.setFillColor(accent_color if accent else color)
            t.textOut(word if i == 0 else f" {word}")
        c.drawText(t)
        c.restoreState()
        y -= leading
    return top - len(lines) * leading


def heading_height(title, max_width, size=None, font=None, tracking=None, min_size=None, max_lines=3,
                   leading=None, suffix=""):
    """Height draw_heading will take."""
    lines, size = heading_layout(title, max_width, size, font, tracking, min_size, max_lines, suffix)
    return len(lines) * (leading or size * PDFStyle.LEADING_TITLE)


def draw_card_title(c, first, second, x, top, width, size=None):
    """
    Card title in two parts: the first in DM Sans 700 ink, the second in DM Sans italic
    400 blue (« Moteurs profonds et réalité économique / pour valider chaque décision »).
    Returns its height.
    """
    size = size or PDFStyle.SIZE_TITLE_CARD
    leading = size * 1.15
    tracking = PDFStyle.TRACKING_TITLE_CARD
    h = draw_paragraph(c, first, x, top, width, PDFStyle.FONT_HEADING_BOLD, size, PDFStyle.COLOR_INK, leading, tracking)
    if second:
        h += draw_paragraph(c, second, x, top - h, width, PDFStyle.FONT_HEADING_ITALIC, size, PDFStyle.COLOR_BLUE,
                            leading, tracking)
    return h


# --- Markers (PT Mono) -------------------------------------------------------

def draw_eyebrow(c, x, y, text, color=None, size=None, tracking=None, max_width=None, align="left"):
    """Eyebrow above a title: PT Mono, uppercase, wide tracking, ink-muted. Returns its width."""
    size = size or PDFStyle.SIZE_EYEBROW
    tracking = PDFStyle.TRACKING_EYEBROW if tracking is None else tracking
    text = str(text).upper()
    if max_width:
        text = fit_text(text, PDFStyle.FONT_LABEL, size, max_width, tracking)
    return draw_text(c, x, y, text, PDFStyle.FONT_LABEL, size, color or PDFStyle.COLOR_INK_MUTED, tracking, align)


def label_pill_size(text, size=None):
    size = size or PDFStyle.SIZE_LABEL
    width = text_width(str(text).upper(), PDFStyle.FONT_LABEL, size, PDFStyle.TRACKING_LABEL) + 2 * size
    return width, size * 1.33 + size


def draw_label_pill(c, x, y, text, variant="pastel", size=None, max_width=None):
    """
    Pill label (PT Mono, uppercase) with its bottom-left corner at (x, y). Variants:
    'pastel' (document pastel fill, blue text: on a white page), 'on_pastel' (white 70 %
    fill: on a pastel card), 'solid' (blue fill, white text). Returns (width, height).
    """
    size = size or PDFStyle.SIZE_LABEL
    text = str(text).upper()
    if max_width:
        text = fit_text(text, PDFStyle.FONT_LABEL, size, max_width - 2 * size, PDFStyle.TRACKING_LABEL)
    width, height = label_pill_size(text, size)
    fill, alpha, color = {
        "on_pastel": (PDFStyle.COLOR_SURFACE_CARD, 0.7, PDFStyle.COLOR_BLUE),
        "solid": (PDFStyle.COLOR_BLUE, 1, PDFStyle.COLOR_SURFACE_CARD),
    }.get(variant, (document_pastel(c), 1, PDFStyle.COLOR_BLUE))
    c.saveState()
    c.setFillColor(fill, alpha=alpha)
    c.roundRect(x, y, width, height, height / 2, stroke=0, fill=1)
    c.restoreState()
    draw_text(c, x + size, y + (height - 0.68 * size) / 2, text, PDFStyle.FONT_LABEL, size, color, PDFStyle.TRACKING_LABEL)
    return width, height


def draw_number(c, x, y, text, size=None, color=None):
    """Big chapter number in PT Mono blue; (x, y) is its baseline start. Returns its width."""
    size = size or PDFStyle.SIZE_NUMBER
    return draw_text(c, x, y, str(text), PDFStyle.FONT_LABEL, size, color or PDFStyle.COLOR_BLUE)


def draw_folio(c, label=None):
    """Page footer in PT Mono: « MARGE DE MANŒUVRE · CARNET 3/7 · P. 12 »."""
    label = document_style(c).folio if label is None else label
    parts = ["marge de manœuvre"] + ([str(label)] if label else []) + [f"p. {c.getPageNumber()}"]
    width, _ = A4
    draw_eyebrow(
        c, PDFStyle.MARGIN_MAIN, PDFStyle.FOLIO_Y, " · ".join(parts),
        size=PDFStyle.SIZE_FOLIO, tracking=PDFStyle.TRACKING_LABEL, max_width=width - 2 * PDFStyle.MARGIN_MAIN,
    )


# --- Cards and fields --------------------------------------------------------

def draw_pastel_card(c, x, y, w, h, color=None, radius=None):
    """Flat pastel card, no border nor shadow (document pastel by default)."""
    c.saveState()
    c.setFillColor(color or document_pastel(c))
    c.roundRect(x, y, w, h, PDFStyle.RADIUS_CARD if radius is None else radius, stroke=0, fill=1)
    c.restoreState()


def draw_white_card(c, x, y, w, h, radius=None):
    """White card with a thin `line` border."""
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_SURFACE_CARD)
    c.setStrokeColor(PDFStyle.COLOR_LINE)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, PDFStyle.RADIUS_CARD if radius is None else radius, stroke=1, fill=1)
    c.restoreState()


def draw_field_box(c, x, y, w, h, radius=None):
    """Area to fill in: white, 1 pt `line-strong` border (never `line`, too pale)."""
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_SURFACE_CARD)
    c.setStrokeColor(PDFStyle.COLOR_LINE_STRONG)
    c.setLineWidth(PDFStyle.LINE_WIDTH_FIELD)
    c.roundRect(x, y, w, h, min(PDFStyle.RADIUS_FIELD if radius is None else radius, h / 2), stroke=1, fill=1)
    c.restoreState()


def draw_rule(c, x1, x2, y, color=None, width=0.75, alpha=1.0, dash=None):
    """Horizontal rule (`line` by default)."""
    c.saveState()
    c.setStrokeColor(color or PDFStyle.COLOR_LINE, alpha=alpha)
    c.setLineWidth(width)
    if dash:
        c.setDash(*dash)
    c.line(x1, y, x2, y)
    c.restoreState()


def draw_disc(c, cx, cy, r, color, alpha=1.0):
    """Plain disc; a background disc may stick out of the page, which cuts it."""
    c.saveState()
    c.setFillColor(color, alpha=alpha)
    c.circle(cx, cy, r, stroke=0, fill=1)
    c.restoreState()


_PASTEL_ORDER = ("sky", "mint", "almond", "lilac", "blush")


def pastel_cycle(c):
    """The document pastel first, then the other card pastels (jasmine stays for post-its)."""
    dominant = document_pastel(c)
    return [dominant] + [PDFStyle.PASTELS[n] for n in _PASTEL_ORDER if PDFStyle.PASTELS[n] != dominant]


# --- Hand-made touches -------------------------------------------------------

@contextmanager
def postit(c, x, y, w, h, color=None, angle=-2.0, tape=True):
    """
    Post-it (jasmine paper and washi tape) turned by `angle` degrees around its centre.
    The block runs in the post-it's own coordinates (origin at its bottom-left corner),
    so its content turns with it. No form field inside: fields ignore rotations.
    The blurred shadow of the site has no PDF equivalent and is left out.
    """
    c.saveState()
    try:
        c.translate(x + w / 2, y + h / 2)
        c.rotate(angle)
        c.translate(-w / 2, -h / 2)
        c.setFillColor(color or PDFStyle.COLOR_JASMINE)
        c.roundRect(0, 0, w, h, PDFStyle.RADIUS_POSTIT, stroke=0, fill=1)
        if tape:
            tape_w, tape_h = 40, 11
            c.saveState()
            c.translate(w / 2, h + 2)
            c.rotate(-1.5)
            c.setFillColor(PDFStyle.COLOR_SURFACE_ALT, alpha=0.9)
            c.setStrokeColor(PDFStyle.COLOR_LINE_STRONG, alpha=0.35)
            c.setLineWidth(0.6)
            c.setDash(1.5, 1.5)
            c.rect(-tape_w / 2, -tape_h / 2, tape_w, tape_h, stroke=1, fill=1)
            c.restoreState()
        yield
    finally:
        c.restoreState()


def draw_drawn_arrow(c, x, y, width=40, flip=False, angle=0, color=None):
    """
    Hand-drawn arrow of the site (a Bézier curve, then an open chevron), going from the
    bottom left to the top right of its box (x, y, width, width * 5/9); `flip` mirrors it
    to go towards the top left.
    """
    s = width / 90.0
    c.saveState()
    c.translate(x + (width if flip else 0), y)
    c.rotate(angle)
    c.scale(-s if flip else s, s)
    c.setStrokeColor(color or PDFStyle.COLOR_INK)
    c.setLineWidth(PDFStyle.LINE_WIDTH_ARROW / s)
    c.setLineCap(1)
    c.setLineJoin(1)
    p = c.beginPath()
    # SVG viewBox 0 0 90 50 with y going down: y becomes 50 - y
    p.moveTo(4, 6)
    p.curveTo(24, 10, 52, 20, 80, 38)
    p.moveTo(70, 42)
    p.lineTo(81, 39)
    p.lineTo(76, 29)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def draw_annotation(c, x, top, text, width, size=None, angle=-2.5):
    """Handwritten-like note in Instrument Serif italic, slightly turned. Returns its height."""
    size = size or PDFStyle.SIZE_ANNOTATION
    leading = size * 1.3
    height = paragraph_height(text, width, PDFStyle.FONT_SERIF, size, leading)
    c.saveState()
    c.translate(x, top - height / 2)
    c.rotate(angle)
    draw_paragraph(c, text, 0, height / 2, width, PDFStyle.FONT_SERIF, size, PDFStyle.COLOR_INK, leading)
    c.restoreState()
    return height


def draw_filled_arrow(c, x, y, width=14, color=None):
    """The site's solid arrow (buttons, action links), pointing right; (x, y) bottom-left."""
    s = width / 20.0
    pts = [(19.046, 6.7487), (12.3238, 0.0791), (12.3238, 4.8971), (0.3711, 4.8971),
           (0.3711, 8.6068), (12.3238, 8.6068), (12.3238, 13.4183)]
    c.saveState()
    c.setFillColor(color or PDFStyle.COLOR_CORAL_STRONG)
    p = c.beginPath()
    for i, (px, py) in enumerate(pts):
        (p.moveTo if i == 0 else p.lineTo)(x + px * s, y + (14 - py) * s)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


_STAR_CURVES = [
    ((8.6, 5.2), (10.8, 7.4), (16, 8)),
    ((10.8, 8.6), (8.6, 10.8), (8, 16)),
    ((7.4, 10.8), (5.2, 8.6), (0, 8)),
    ((5.2, 7.4), (7.4, 5.2), (8, 0)),
]


def draw_star(c, x, y, size, color=None):
    """Four-pointed star bullet in a size x size box whose bottom-left corner is (x, y)."""
    s = size / 16.0
    c.saveState()
    c.setFillColor(color or PDFStyle.COLOR_CORAL_STRONG)
    p = c.beginPath()
    p.moveTo(x + 8 * s, y + 16 * s)
    for curve in _STAR_CURVES:
        (x1, y1), (x2, y2), (x3, y3) = curve
        p.curveTo(x + x1 * s, y + (16 - y1) * s, x + x2 * s, y + (16 - y2) * s, x + x3 * s, y + (16 - y3) * s)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def star_list_height(items, width, size=None):
    size = size or PDFStyle.SIZE_BODY
    leading, gap = size * 1.375, size * 0.75
    text_w = width - size * 1.6
    return sum(paragraph_height(str(item), text_w, PDFStyle.FONT_BODY, size, leading) for item in items) + gap * (len(items) - 1)


def draw_star_list(c, items, x, top, width, size=None, color=None):
    """List with coral-strong star bullets (the exercises of a workbook). Returns its height."""
    size = size or PDFStyle.SIZE_BODY
    leading, gap = size * 1.375, size * 0.75
    star = size * 0.85
    text_x = x + size * 1.6
    y = top
    for i, item in enumerate(items):
        if i:
            y -= gap
        baseline = first_baseline(y, size, leading)
        draw_star(c, x, baseline + 0.36 * size - star / 2, star)
        y -= draw_paragraph(c, str(item), text_x, y, x + width - text_x, PDFStyle.FONT_BODY, size,
                            color or PDFStyle.COLOR_INK, leading)
    return top - y


def stamp_size(text="Validé en séance", size=None):
    size = size or PDFStyle.SIZE_LABEL
    text_w = text_width(str(text).upper(), PDFStyle.FONT_LABEL, size, 0.1)
    return text_w + 2.9 * size + 1.4 * size, size * 2.6


def draw_stamp(c, cx, cy, text="Validé en séance", size=None, angle=-4):
    """« Validé en séance » stamp: coral-strong border and text, check icon, turned by -4°."""
    size = size or PDFStyle.SIZE_LABEL
    w, h = stamp_size(text, size)
    c.saveState()
    c.translate(cx, cy)
    c.rotate(angle)
    c.setStrokeColor(PDFStyle.COLOR_CORAL_STRONG)
    c.setLineWidth(1.5)
    c.roundRect(-w / 2, -h / 2, w, h, PDFStyle.RADIUS_STAMP, stroke=1, fill=0)
    icon = size * 1.4
    draw_icon(c, "check", -w / 2 + 1.45 * size + icon / 2 - 0.4 * size, 0, icon, PDFStyle.COLOR_CORAL_STRONG)
    draw_text(c, -w / 2 + 1.45 * size + icon, -0.34 * size, str(text).upper(), PDFStyle.FONT_LABEL, size,
              PDFStyle.COLOR_CORAL_STRONG, 0.1)
    c.restoreState()
    return w, h


# --- Icons -------------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def _icon_codepoints():
    path = os.path.join(PDFStyle.FONTS_DIR, "MaterialSymbolsOutlined.codepoints")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return {name: chr(int(code, 16)) for name, code in (line.split() for line in f if line.strip())}


def has_icon(name):
    return bool(PDFStyle.FONT_ICONS) and name in _icon_codepoints()


def draw_icon(c, name, cx, cy, size, color=None):
    """
    Draws a Material Symbols Outlined icon (e.g. 'menu_book', 'flag') centred on (cx, cy);
    size is the icon box. Does nothing if the icon font or the name is missing.
    """
    char = _icon_codepoints().get(name)
    if not char or not PDFStyle.FONT_ICONS:
        return
    c.saveState()
    c.setFillColor(color or PDFStyle.COLOR_BLUE)
    c.setFont(PDFStyle.FONT_ICONS, size)
    # The glyphs are drawn in a one-em square standing on the baseline
    c.drawString(cx - size / 2, cy - size / 2, char)
    c.restoreState()


def draw_icon_badge(c, cx, cy, name, diameter=26, on_pastel=False, color=None, fill=None):
    """
    Icon in a disc: white at 70 % on a pastel card, the document pastel on a white page.
    The icon is blue by default.
    """
    c.saveState()
    if fill is not None:
        c.setFillColor(fill)
    elif on_pastel:
        c.setFillColor(PDFStyle.COLOR_SURFACE_CARD, alpha=0.7)
    else:
        c.setFillColor(document_pastel(c))
    c.circle(cx, cy, diameter / 2, stroke=0, fill=1)
    c.restoreState()
    draw_icon(c, name, cx, cy, diameter * 0.56, color)


def draw_frise(c, x, y, width, steps, start_label="", end_label="", background=None):
    """
    Timeline: a dotted ink line at 25 % from a dot to a triangle, with an icon badge per
    step (pastel disc ringed with the background color), its title and its marker below.
    steps: [(icon, title, marker), ...]. y is the line's height. Returns the height used
    below the line.
    """
    background = background or PDFStyle.COLOR_PAGE
    badge = 30
    c.saveState()
    c.setStrokeColor(PDFStyle.COLOR_INK, alpha=0.25)
    c.setLineWidth(1.5)
    c.setDash(3, 3)
    c.line(x + 6, y, x + width - 8, y)
    c.restoreState()
    draw_disc(c, x + 4.5, y, 4.5, PDFStyle.COLOR_INK)
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_INK)
    p = c.beginPath()
    p.moveTo(x + width - 9, y + 5)
    p.lineTo(x + width, y)
    p.lineTo(x + width - 9, y - 5)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()
    if start_label:
        draw_eyebrow(c, x, y + badge / 2 + 10, start_label, size=PDFStyle.SIZE_FOLIO)
    if end_label:
        draw_eyebrow(c, x + width, y + badge / 2 + 10, end_label, size=PDFStyle.SIZE_FOLIO, align="right")

    n = max(len(steps), 1)
    col = (width - 30) / n
    lowest = y
    pastels = [PDFStyle.COLOR_LILAC, PDFStyle.COLOR_SKY, PDFStyle.COLOR_MINT, PDFStyle.COLOR_ALMOND]
    for i, (icon, title, marker) in enumerate(steps):
        cx = x + 24 + i * col + badge / 2
        draw_disc(c, cx, y, badge / 2 + 4, background)  # ring of the background color
        draw_icon_badge(c, cx, y, icon, diameter=badge, fill=pastels[i % len(pastels)], color=PDFStyle.COLOR_INK)
        top = y - badge / 2 - 10
        top -= draw_paragraph(c, title, cx - badge / 2, top, col - 10, PDFStyle.FONT_HEADING_BOLD, 10, PDFStyle.COLOR_INK,
                              12.5)
        if marker:
            draw_eyebrow(c, cx - badge / 2, top - 10, marker, size=PDFStyle.SIZE_FOLIO, color=PDFStyle.COLOR_BLUE,
                         max_width=col - 10)
            top -= 14
        lowest = min(lowest, top)
    return y - lowest


# --- Illustration ------------------------------------------------------------

@functools.lru_cache(maxsize=8)
def _cover_drawing(pastel_hex):
    """The cover SVG as a ReportLab drawing, its placeholder lilac turned into pastel_hex."""
    with open(PDFStyle.PATH_COVER_ILLUSTRATION, encoding="utf-8") as f:
        svg = f.read()
    svg = re.sub(re.escape(PDFStyle.COVER_ILLUSTRATION_PASTEL), pastel_hex, svg, flags=re.IGNORECASE)
    return svg2rlg(io.BytesIO(svg.encode("utf-8")))


def draw_cover_illustration(c):
    """
    The cover illustration (assets/illustrations/couverture.svg, the work table seen from
    above) across the top 500 pt of the page, in the document pastel. It leaves the top left
    corner to the logotype and the bottom left to the promise post-it.
    """
    drawing = _cover_drawing("#" + document_pastel(c).hexval()[2:])
    renderPDF.draw(drawing, c, 0, A4[1] - drawing.height)


# --- Brand -------------------------------------------------------------------

def draw_logotype(c, x, y, size=14, color=None):
    """
    « marge / de manœuvre » on two lines (Manrope 800, lowercase, tight), underlined by a
    thick rule. (x, y) is the baseline of « marge ». Returns the bottom y of the rule.
    """
    color = color or PDFStyle.COLOR_INK
    line_gap = 0.9 * size
    draw_text(c, x, y, "marge", PDFStyle.FONT_LOGO, size, color, -0.05)
    draw_text(c, x, y - line_gap, "de manœuvre", PDFStyle.FONT_LOGO, size, color, -0.05)
    rule_top = y - line_gap - 0.42 * size
    c.saveState()
    c.setFillColor(color)
    c.rect(x, rule_top - 0.2 * size, 4.8 * size, 0.2 * size, stroke=0, fill=1)
    c.restoreState()
    return rule_top - 0.2 * size


def draw_signature(c, x, y, size=36, color=None, align="left"):
    """« marge de manœuvre » on one line, ended by the coral dot. Returns its width."""
    text = "marge de manœuvre"
    width = text_width(text, PDFStyle.FONT_LOGO, size, -0.05)
    dot = 0.17 * size
    total = width + 0.04 * size + dot
    if align == "center":
        x -= total / 2
    elif align == "right":
        x -= total
    draw_text(c, x, y, text, PDFStyle.FONT_LOGO, size, color or PDFStyle.COLOR_INK, -0.05)
    draw_disc(c, x + width + 0.04 * size + dot / 2, y + dot / 2, dot / 2, PDFStyle.COLOR_CORAL)
    return total


# --- Page frame --------------------------------------------------------------

def content_frame():
    """(x, width) of the content column of a page."""
    width, _ = A4
    return PDFStyle.MARGIN_MAIN, width - 2 * PDFStyle.MARGIN_MAIN


def draw_page_head(c, title, eyebrow=None, suffix="", title_size=None, min_size=None):
    """
    Top of a content page: the eyebrow (sourcil) then the page title with its accent.
    Returns the y under the title, where the content starts.
    """
    page_w, height = A4
    x, width = content_frame()
    # A jasmine disc cut by the top right corner; the title stays clear of it
    draw_disc(c, page_w + 0.6 * 28.3465, height + 0.6 * 28.3465, 3.6 * 28.3465, PDFStyle.COLOR_JASMINE)
    title_w = width - 2.6 * 28.3465
    top = height - PDFStyle.EYEBROW_TOP
    if eyebrow:
        # The exercise marker is a pill label (« EXERCICE 2 · 20 MIN »)
        _, pill_h = draw_label_pill(c, x, top - 6, eyebrow, max_width=title_w)
        top -= 6 + 0.4 * 28.3465
    else:
        top += 0.25 * 28.3465
    if not title:
        return top
    return draw_heading(
        c, title, x, top, title_w,
        size=title_size or PDFStyle.SIZE_TITLE_PAGE,
        min_size=min_size or PDFStyle.SIZE_TITLE_PAGE_MIN,
        max_lines=2, suffix=suffix,
    )
