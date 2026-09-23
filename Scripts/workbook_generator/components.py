import os
import math
from xml.sax.saxutils import escape
from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

from .config import PDFStyle
from .forms import create_input_field, create_checkbox
from .utils import cached_image_reader


def draw_page_background(c, width, height, use_blobs=False):
    """Refactored: Standard background with Nude color, Dot Grid, and Waves."""
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    if use_blobs:
        draw_background_blobs(c, width, height)
    else:
        draw_wavy_background(c, width, height)

    draw_dot_grid(c, width, height)


def draw_page_decorations(c, width, height, part_title=None, x_offset=0):
    """Draws Header (Logo + part title) and Footer (Page num) on top of the content."""
    if part_title is not None:
        draw_page_header(c, part_title, width, height, x_offset=x_offset)
    draw_page_footer(c, width, height, x_offset=x_offset)


def draw_wavy_background(c, width, height):
    """Draws subtle organic wave shapes in the background using XObjects for caching."""
    if not hasattr(c, "_wavy_cache"):
        c._wavy_cache = {}

    cache_key = (width, height)

    if cache_key not in c._wavy_cache:
        form_name = f"WavyBg_{len(c._wavy_cache)}"
        c.beginForm(form_name)

        c.setFillColor(PDFStyle.COLOR_BG_BLOB, alpha=0.4)  # Subtle darker nude / blob color

        # Top Left Wave
        p1 = c.beginPath()
        p1.moveTo(0, height)
        p1.curveTo(width * 0.3, height, width * 0.5, height * 0.85, 0, height * 0.65)
        c.drawPath(p1, fill=1, stroke=0)

        # Bottom Right Wave
        p2 = c.beginPath()
        p2.moveTo(width, 0)
        p2.curveTo(width * 0.7, 0, width * 0.5, height * 0.15, width, height * 0.35)
        c.drawPath(p2, fill=1, stroke=0)

        c.endForm()
        c._wavy_cache[cache_key] = form_name

    c.saveState()
    c.doForm(c._wavy_cache[cache_key])
    c.restoreState()


def draw_background_blobs(c, width, height):
    """Draws large soft organic blobs at Top-Right and Bottom-Left using XObjects for caching."""
    if not hasattr(c, "_blobs_cache"):
        c._blobs_cache = {}

    cache_key = (width, height, PDFStyle.COLOR_BG_BLOB)

    if cache_key not in c._blobs_cache:
        form_name = f"BlobsBg_{len(c._blobs_cache)}"
        c.beginForm(form_name)

        # Use the specifically defined pink blob color
        c.setFillColor(PDFStyle.COLOR_BG_BLOB, alpha=0.5)

        # Top Right Blob - slightly larger
        c.circle(width * 0.95, height * 0.92, 140, fill=1, stroke=0)

        # Bottom Blob - spans full width, starts higher, ends lower
        # We'll use a large ellipse for the bottom one
        # Moved center a bit higher (~15% of height) and made it very wide
        c.ellipse(
            -width * 0.2, -height * 0.1, width * 1.2, height * 0.35, fill=1, stroke=0
        )

        # Alternatively, use multiple circles to create a "wavy" fill at the bottom
        # but based on "traverser toute la largeur", a large horizontal ellipse or rect-to-curve is better.
        # Let's use a path for organic feel
        p = c.beginPath()
        p.moveTo(0, height * 0.25)  # Starts higher
        p.curveTo(
            width * 0.3, height * 0.3, width * 0.7, height * 0.1, width, height * 0.2
        )
        p.lineTo(width, 0)
        p.lineTo(0, 0)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

        c.endForm()
        c._blobs_cache[cache_key] = form_name

    c.saveState()
    c.doForm(c._blobs_cache[cache_key])
    c.restoreState()


def draw_page_header(c, part_title, width, height, x_offset=0):
    """Draws the standard header: small logo left, part title right."""
    c.saveState()
    # Left Logo - Shifted by x_offset + internal padding
    logo_y = height - 1.5 * cm
    draw_branding_logo(c, x_offset + 0.8 * cm, logo_y, size=12)

    # Right Part Title - Shifted from right edge
    if part_title:
        c.setFont(PDFStyle.FONT_TITLE, 10)
        c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
        c.drawRightString(width - 1.2 * cm, logo_y, part_title.upper())
    c.restoreState()


def draw_page_footer(c, width, height, x_offset=0):
    """Draws the standard footer: page number centered relative to the content area."""
    c.saveState()
    page_num = c.getPageNumber()
    c.setFont(PDFStyle.FONT_TITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)

    # Center relative to the panel if x_offset is provided
    content_area_center = x_offset + (width - x_offset) / 2.0
    c.drawCentredString(content_area_center, 1.5 * cm, str(page_num))
    c.restoreState()


def draw_dot_grid(c, width, height, color=PDFStyle.COLOR_ACCENT_BLUE, opacity=0.015):
    """
    Draws the signature Dot Grid using Form XObjects to dramatically improve performance
    and reduce output PDF size by caching the grid.
    """
    # Initialize cache dictionary on canvas object if it doesn't exist
    if not hasattr(c, "_dot_grid_cache"):
        c._dot_grid_cache = {}

    # Create a unique cache key based on dimensions, color, and opacity
    color_val = getattr(color, "hexval", color)
    cache_key = (width, height, color_val, opacity)

    if cache_key not in c._dot_grid_cache:
        # Use a simple, safe name for the XObject to avoid escaping issues
        form_name = f"DotGrid_{len(c._dot_grid_cache)}"
        c.beginForm(form_name)
        step = 25
        c.setFillColor(color, alpha=opacity)
        # Using a single path is faster than emitting individual circle operators
        p = c.beginPath()
        for x in range(0, int(width), step):
            for y in range(0, int(height), step):
                p.circle(x, y, 0.4)
        c.drawPath(p, fill=1, stroke=0)
        c.endForm()
        c._dot_grid_cache[cache_key] = form_name

    c.saveState()
    c.doForm(c._dot_grid_cache[cache_key])
    c.restoreState()


def draw_marginal_signature(c, height):
    """Draws vertical 'marge de manœuvre' signature on the left."""
    c.saveState()
    c.translate(1.2 * cm, height / 2)
    c.rotate(90)
    c.setFont(PDFStyle.FONT_BODY, 8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawCentredString(0, 0, "m a r g e   d e   m a n œ u v r e")
    c.restoreState()


def draw_card(c, x, y, width, height):
    """Draws a creme rounded card with shadow."""
    c.saveState()
    # Soft Shadow
    c.setFillColor(PDFStyle.COLOR_SHADOW, alpha=0.03)
    c.roundRect(x + 3, y - 3, width, height, PDFStyle.CARD_RADIUS, fill=1, stroke=0)
    # Card
    c.setFillColor(PDFStyle.COLOR_CARD_CREME)
    c.roundRect(x, y, width, height, PDFStyle.CARD_RADIUS, fill=1, stroke=0)
    c.restoreState()


def draw_side_panel(c, x, page_width, page_height):
    """Draws a creme panel extending to Top, Bottom, Right."""
    c.saveState()
    # Shadow (Left side only)
    c.setFillColor(PDFStyle.COLOR_SHADOW, alpha=0.05)
    c.rect(x - 3, 0, page_width - x + 3, page_height, fill=1, stroke=0)

    # Main Creme Panel
    c.setFillColor(PDFStyle.COLOR_CARD_CREME)
    c.rect(x, 0, page_width - x, page_height, fill=1, stroke=0)
    c.restoreState()


@dataclass
class LeafStyle:
    size: float = 50
    color: str = PDFStyle.COLOR_ACCENT_BLUE
    angle: float = 0
    alpha: float = 1.0


def draw_leaf(c, pos, style: LeafStyle = None):
    """Leaf decoration."""
    if style is None:
        style = LeafStyle()

    x, y = pos

    c.saveState()
    c.translate(x, y)
    c.rotate(style.angle)
    c.scale(style.size / 100.0, style.size / 100.0)
    p = c.beginPath()
    p.moveTo(0, 0)
    p.curveTo(30, 20, 50, 60, 0, 100)
    p.curveTo(-50, 60, -30, 20, 0, 0)
    if isinstance(style.color, colors.Color):
        r, g, b = style.color.red, style.color.green, style.color.blue
        c.setFillColorRGB(r, g, b, style.alpha)
    else:
        c.setFillColor(style.color)
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


@dataclass
class TitleStyle:
    size: float = 24
    color: str = PDFStyle.COLOR_ACCENT_BLUE


def draw_title(c, text, pos, available_width=None, style: TitleStyle = None):
    """Refactored: Standard H1 title. Returns the Y position after the title."""
    if style is None:
        style = TitleStyle()

    x, y = pos

    if available_width is None:
        width, _ = A4
        available_width = width - x - 2 * cm

    c.saveState()
    c.setFont(PDFStyle.FONT_TITLE, style.size)
    c.setFillColor(style.color)

    lines = simpleSplit(text, PDFStyle.FONT_TITLE, style.size, available_width)
    current_y = y

    for line in lines:
        c.drawString(x, current_y, line)
        current_y -= style.size * 1.2

    c.restoreState()

    # Return the position after the last line
    return current_y


def draw_branding_logo(c, x, y, size=40, align="left"):
    """
    Draws the 'marge de manœuvre' logo with underline.
    align: 'left' or 'center'
    """
    c.saveState()
    c.setFont(PDFStyle.FONT_BRANDING, size)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)

    line_height = size * 1.1  # Approx line height based on font size font

    # Calculate underline length adaptable to size
    length = 9 * cm * (size / 40.0)

    if align == "center":
        c.drawCentredString(x, y, "marge")
        c.drawCentredString(x, y - line_height, "de manœuvre")
    else:
        c.drawString(x, y, "marge")
        c.drawString(x, y - line_height, "de manœuvre")

    # Underline
    underline_y = y - line_height - 0.3 * cm
    c.setLineWidth(3 * (size / 40.0))
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)

    if align == "center":
        c.line(x - length / 2, underline_y, x + length / 2, underline_y)
    else:
        c.line(x, underline_y, x + length, underline_y)
    c.restoreState()


def create_closing_page(c, messages=None):
    """
    Standard Closing Page.
    """
    width, height = A4
    draw_page_background(c, width, height)

    # 1. Logo Centered
    logo_x = width / 2
    logo_y = height / 2 + 2.5 * cm

    draw_branding_logo(c, logo_x, logo_y, size=40, align="center")

    # 2. Encouraging Text (Auto-wrapped so long inspirational sentences never overflow)
    text_y = logo_y - 3.8 * cm
    wrap_w = width - 4.5 * cm

    if not messages:
        messages = [
            "Félicitations pour ce temps pris pour vous.",
            "Laissez infuser ces réflexions.",
            "À très vite pour la suite de votre exploration.",
        ]

    style_closing = ParagraphStyle(
        "ClosingText",
        fontName=PDFStyle.FONT_TITLE,
        fontSize=12,
        leading=18,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
        alignment=1,  # Centered
    )

    for msg in messages:
        msg_str = (msg.get("text") or str(msg)) if isinstance(msg, dict) else str(msg)
        if not msg_str.strip():
            continue
        p = Paragraph(escape(msg_str), style_closing)
        w, h = p.wrap(wrap_w, height)
        p.drawOn(c, (width - wrap_w) / 2, text_y - h)
        text_y -= h + 0.6 * cm

    c.showPage()



def draw_section_separator(c, x, y, width, color=PDFStyle.COLOR_ACCENT_BLUE):
    """
    Draws a simple separator line with a centered dot/symbol.
    """
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(1)

    # Line left
    c.line(x, y, x + width / 2 - 0.5 * cm, y)
    # Dot center
    c.setFillColor(color)
    c.circle(x + width / 2, y, 0.1 * cm, fill=1, stroke=0)
    # Line right
    c.line(x + width / 2 + 0.5 * cm, y, x + width, y)

    c.restoreState()


def draw_circular_stamp(c, x, y, text, radius=1.8 * cm):
    """Draws text curved around a central point, simulating a stamp."""
    c.saveState()
    c.translate(x, y)
    c.rotate(-15)  # slight tilt

    c.setFont(PDFStyle.FONT_TITLE, 8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)

    chars = text + " · "
    angle_step = 360 / len(chars)
    for i, char in enumerate(chars):
        c.saveState()
        angle = math.radians(i * angle_step)
        char_x = radius * math.sin(angle)
        char_y = radius * math.cos(angle)
        c.translate(char_x, char_y)
        c.rotate(-math.degrees(angle))
        c.drawCentredString(0, 0, char)
        c.restoreState()

    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1)
    # Simple placeholder shape in the center (hands/clap icon approximation)
    c.circle(0, 0.2 * cm, radius * 0.4, stroke=1, fill=0)
    c.line(-radius * 0.3, -0.1 * cm, radius * 0.3, -0.1 * cm)
    c.line(-radius * 0.2, -0.3 * cm, radius * 0.2, -0.3 * cm)

    c.restoreState()


def draw_pause_badge(c, x, y, radius=0.4 * cm):
    """Draws the 'Pause' badge icon (circle with Play + Pause bars)."""
    c.saveState()

    # Circle
    c.setStrokeColor(PDFStyle.COLOR_WHITE)
    c.setLineWidth(1.5)
    c.circle(x, y + 0.15 * cm, radius, fill=0, stroke=1)

    # Pause bars
    bar_width = 0.08 * cm
    bar_height = 0.3 * cm
    c.setFillColor(PDFStyle.COLOR_WHITE)
    c.rect(x - 0.15 * cm, y, bar_width, bar_height, fill=1, stroke=0)

    # Play triangle
    p = c.beginPath()
    p.moveTo(x + 0.02 * cm, y)
    p.lineTo(x + 0.02 * cm, y + bar_height)
    p.lineTo(x + 0.22 * cm, y + bar_height / 2)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    c.restoreState()


def create_standard_cover(c, subtitle, title="BILAN DE COMPÉTENCES & ALIGNEMENT"):
    """
    Standard Cover Page generator for Workbooks.
    """
    width, height = A4

    # 1. Background Nude + Grid
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    draw_dot_grid(c, width, height)

    # 1b. Blue Side Band (Left)
    band_width = 1.75 * cm
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.rect(0, 0, band_width, height, fill=1, stroke=0)

    # A. Illustration Principale (Cover)
    if os.path.exists(PDFStyle.PATH_ILLU_COVER):
        content_width = width - band_width
        img_width = content_width * 0.75
        center_x = band_width + (content_width - img_width) / 2

        c.drawImage(
            cached_image_reader(PDFStyle.PATH_ILLU_COVER),
            center_x,
            height * 0.10,
            width=img_width,
            height=height * 0.5,
            mask="auto",
            preserveAspectRatio=True,
            anchor="sw",
        )
    else:
        # Fallback
        c.setFillColor(PDFStyle.COLOR_WHITE)
        c.circle(width * 0.35, height * 0.55, 160, fill=1, stroke=0)

    # 2b. Marque Header
    logo_x = band_width + 1.5 * cm
    logo_y = height - 3 * cm
    draw_branding_logo(c, logo_x, logo_y, size=40)

    # 2c. Stamp Rouge
    if os.path.exists(PDFStyle.PATH_STAMP):
        c.saveState()
        c.translate(width - 4 * cm, 4 * cm)
        c.rotate(-15)
        c.drawImage(
            cached_image_reader(PDFStyle.PATH_STAMP),
            -2 * cm,
            -2 * cm,
            width=4 * cm,
            height=4 * cm,
            mask="auto",
            preserveAspectRatio=True,
            anchor="c",
        )
        c.restoreState()

    # 3. Titres
    max_text_width = width - band_width - 40 - 1 * cm

    c.setFont(PDFStyle.FONT_BODY, 14)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    title_lines = simpleSplit(title, PDFStyle.FONT_BODY, 14, max_text_width)

    y_text = height - 210
    for line in title_lines:
        c.drawRightString(width - 40, y_text, line)
        y_text -= 16

    y_text -= 14  # Extra space between title and subtitle

    c.setFont(PDFStyle.FONT_TITLE, 18)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    subtitle_lines = simpleSplit(subtitle, PDFStyle.FONT_TITLE, 18, max_text_width)

    for line in subtitle_lines:
        c.drawRightString(width - 40, y_text, line)
        y_text -= 20

    c.showPage()


# --- STANDARD HARMONIZED COMPONENTS ---


def create_standard_summary_page(
    c, chapter_num_str, chapter_title, intro_text, points_list
):
    """
    Standard Summary Page: Blue Background, large watermark number, and list of points.
    """
    width, height = A4

    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Faint Grid
    draw_dot_grid(c, width, height, color=PDFStyle.COLOR_WHITE, opacity=0.1)

    # Watermark
    c.saveState()
    c.setFont(PDFStyle.FONT_BRANDING, 160)
    c.setFillColor(PDFStyle.COLOR_WHITE, alpha=0.12)
    c.drawString(1.5 * cm, height - 9 * cm, f"{chapter_num_str}.")
    c.restoreState()

    start_y = height - 10 * cm
    c.setFont(PDFStyle.FONT_BRANDING, 32)
    c.setFillColor(PDFStyle.COLOR_WHITE)

    title_lines = simpleSplit(chapter_title, PDFStyle.FONT_BRANDING, 32, width - 5 * cm)
    current_y = start_y
    for line in title_lines:
        c.drawString(2.5 * cm, current_y, line)
        current_y -= 40

    text_y = current_y - 1 * cm  # Add space after the title

    if intro_text:
        style_body = ParagraphStyle(
            "SummaryBody",
            fontName=PDFStyle.FONT_BODY,
            fontSize=11,
            leading=15,
            textColor=colors.white,
            alignment=TA_JUSTIFY,
        )
        p_intro = Paragraph(intro_text, style_body)
        w, h = p_intro.wrap(width - 5 * cm, height)
        p_intro.drawOn(c, 2.5 * cm, text_y - h)
        text_y -= h + 1 * cm

    wrap_w = width - 5.5 * cm
    style_point = ParagraphStyle(
        "SummaryPoint",
        fontName=PDFStyle.FONT_BODY,
        fontSize=11.5,
        leading=16,
        textColor=colors.white,
    )

    # Render points with auto-wrapping so they never bleed off the right edge
    for point in points_list:
        if isinstance(point, (tuple, list)):
            label = str(point[0]) if len(point) > 0 else ""
            desc = str(point[1]) if len(point) > 1 else ""
            p_text = f'<b><font name="{PDFStyle.FONT_TITLE}">{escape(label)}</font></b>&nbsp;&nbsp;{escape(desc)}'
        else:
            p_text = f'<b><font name="{PDFStyle.FONT_TITLE}">{escape(str(point))}</font></b>'
        p_pt = Paragraph(p_text, style_point)
        w, h = p_pt.wrap(wrap_w, height)
        p_pt.drawOn(c, 2.5 * cm, text_y - h)
        text_y -= h + 0.65 * cm

    # Decor (Plume)
    if os.path.exists(PDFStyle.PATH_PLUME_TEXTURE):
        c.saveState()
        c.translate(width - 1 * cm, height - 3 * cm)
        c.rotate(30)
        c.drawImage(
            cached_image_reader(PDFStyle.PATH_PLUME_TEXTURE),
            0,
            0,
            width=5 * cm,
            height=5 * cm,
            mask="auto",
            preserveAspectRatio=True,
            anchor="ne",
        )
        c.restoreState()

    c.showPage()


def create_standard_engagement_page(
    c,
    part_title,
    custom_lines=None,
    title="Pacte d'Action & d'Engagement",
    signature_label="Date et Signature :",
):
    """
    Standard Engagement Page: Balanced commitment card with checkmarks and an anchored signature card.
    """
    width, height = A4
    draw_page_background(c, width, height)

    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    content_w = width - text_x - 1.8 * cm
    text_top = height - 4.2 * cm

    new_y = draw_title(c, title, pos=(text_x, text_top), available_width=content_w)

    lines = (
        custom_lines
        if custom_lines
        else [
            "Je m'engage aujourd'hui à prendre ce temps pour moi avec sincérité.",
            "À regarder ma situation avec honnêteté et bienveillance.",
            "À accepter de ne pas avoir toutes les réponses tout de suite.",
            "À explorer, tester concrètement et avancer pas à pas.",
            "Ce travail est pour moi, et je décide de m'y investir pleinement.",
        ]
    )

    clean_lines = []
    for line in lines:
        l_str = (
            (line.get("text") or line.get("line") or str(line))
            if isinstance(line, dict)
            else str(line)
        ).strip()
        if l_str:
            clean_lines.append(l_str)

    # 1. Commitment Card in upper-mid section
    card_y_top = new_y - 0.8 * cm
    style_item = ParagraphStyle(
        "EngageItem",
        fontName=PDFStyle.FONT_BODY,
        fontSize=10.5,
        leading=15,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
    )

    # Calculate total height of items
    item_paragraphs = []
    total_items_h = 0
    item_wrap_w = content_w - 1.6 * cm
    for l_text in clean_lines:
        p = Paragraph(f'<font color="{PDFStyle.COLOR_ACCENT_BLUE}" name="{PDFStyle.FONT_TITLE}">✓</font>&nbsp;&nbsp;{escape(l_text)}', style_item)
        _, h = p.wrap(item_wrap_w, height)
        item_paragraphs.append((p, h))
        total_items_h += h + 0.35 * cm

    card_pad = 0.6 * cm
    card_h = total_items_h + 2 * card_pad + 0.4 * cm
    card_y = card_y_top - card_h

    draw_card(c, text_x, card_y, content_w, card_h)

    # Render items inside card
    curr_item_y = card_y_top - card_pad
    for p, h in item_paragraphs:
        p.drawOn(c, text_x + 0.8 * cm, curr_item_y - h)
        curr_item_y -= (h + 0.35 * cm)

    # 2. Anchored Signature Block at bottom
    sig_block_y = 3.6 * cm
    sig_block_h = 3.2 * cm
    draw_card(c, text_x, sig_block_y, content_w, sig_block_h)

    # Left: Date & Lieu
    c.saveState()
    c.setFont(PDFStyle.FONT_SUBTITLE, 9)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x + 0.6 * cm, sig_block_y + sig_block_h - 0.7 * cm, "DATE & LIEU :")
    c.restoreState()

    half_w = (content_w - 1.6 * cm) / 2
    form = c.acroForm
    create_input_field(
        form,
        "date_lieu_engagement",
        pos=(text_x + 0.6 * cm, sig_block_y + 0.5 * cm),
        size=(half_w, 1.3 * cm),
        tooltip="Fait à ..., le ...",
        fill_color=PDFStyle.COLOR_WHITE,
    )

    # Right: Signature
    sig_x = text_x + 0.6 * cm + half_w + 0.4 * cm
    c.saveState()
    c.setFont(PDFStyle.FONT_SUBTITLE, 9)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(sig_x, sig_block_y + sig_block_h - 0.7 * cm, "SIGNATURE DU BÉNÉFICIAIRE :")
    c.restoreState()

    create_input_field(
        form,
        "signature_engagement",
        pos=(sig_x, sig_y := sig_block_y + 0.5 * cm),
        size=(half_w, 1.3 * cm),
        tooltip="Votre Signature",
        fill_color=PDFStyle.COLOR_WHITE,
    )

    draw_page_decorations(c, width, height, part_title=part_title, x_offset=card_margin)
    c.showPage()


def create_standard_recap_page(c, part_title, intro_txt, questions):
    """
    Standard Recap Page.
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    target_width = width - card_margin - 2.0 * cm

    new_y = draw_title(
        c, "Récapitulatif de la séance précédente", pos=(text_x, height - 4.0 * cm)
    )

    c.setFont(PDFStyle.FONT_BODY, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    text_y = new_y - 0.5 * cm
    for line in simpleSplit(intro_txt, PDFStyle.FONT_BODY, 11, target_width):
        c.drawString(text_x, text_y, line)
        text_y -= 0.5 * cm

    form = c.acroForm
    y_cursor = text_y - 0.5 * cm

    # Calculate uniform box height depending on the number of questions.
    max_y_cursor = y_cursor
    min_y_cursor = 3.2 * cm  # Avoid overlap with footer decorations (~2.0 cm)
    available_space = max_y_cursor - min_y_cursor

    # Estimated space per question: title (max 2 lines) -> ~1.2cm, margin -> 0.4cm.
    # Total fixed taken per question ~ 1.8cm.
    if len(questions) > 0:
        box_height = max(
            (available_space - (len(questions) * 1.8 * cm)) / len(questions), 2.8 * cm
        )
        box_height = min(box_height, 4.6 * cm)  # Generous cap for open reflection
    else:
        box_height = 4.2 * cm

    for i, question in enumerate(questions):
        # Color alternation for rhythm
        color = PDFStyle.COLOR_ACCENT_BLUE if i % 2 == 0 else PDFStyle.COLOR_ACCENT_RED

        text_obj = c.beginText(text_x, y_cursor)
        text_obj.setFont(PDFStyle.FONT_SUBTITLE, 11)
        text_obj.setFillColor(color)
        lines = simpleSplit(question, PDFStyle.FONT_SUBTITLE, 11, target_width)
        for line in lines:
            text_obj.textLine(line)
        c.drawText(text_obj)

        y_cursor -= len(lines) * 0.5 * cm + 0.3 * cm

        create_input_field(
            form,
            f"recap_q{i+1}",
            pos=(text_x, y_cursor - box_height),
            size=(target_width, box_height),
            multiline=True,
        )

        y_cursor -= box_height + 0.8 * cm  # Using 0.8cm strict gap between elements

    draw_page_decorations(c, width, height, part_title=part_title, x_offset=card_margin)
    c.showPage()


def create_standard_meteo_page(
    c,
    title="Mon État d'Esprit Actuel",
    part_title=None,
    emotion_prompt="Aujourd'hui, je me sens :",
    energy_prompt="Mon niveau d'énergie :",
    thought_prompt="Ce qui prend le plus de place dans ma tête :",
    field_prefix="meteo",
):
    """
    Standard Ice-Breaker / Inner Weather Page.
    Includes:
    - Emotion prompt with word field & 4 checkboxes (Soleil, Nuageux, Pluvieux, Orageux)
    - Energy slider 0 to 10
    - Large reflection multiline textfield
    """
    width, height = A4
    draw_page_background(c, width, height)

    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm

    y_pos = draw_title(c, title, pos=(text_x, text_top))
    form = c.acroForm

    # 1. Emotion section
    y_opts = y_pos - 0.5 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, y_opts, emotion_prompt)

    prompt_width = c.stringWidth(emotion_prompt, PDFStyle.FONT_SUBTITLE, 12)
    create_input_field(
        form,
        f"{field_prefix}_emotion_word",
        pos=(text_x + prompt_width + 0.5 * cm, y_opts - 5),
        size=(width - (text_x + prompt_width + 2.0 * cm), 20),
        tooltip="Un mot pour décrire l'instant",
    )

    options = ["Soleil ☀️", "Nuageux ☁️", "Pluvieux 🌧️", "Orageux ⛈️"]
    opt_x = text_x
    opt_y = y_opts - 1.5 * cm

    for opt in options:
        opt_key = opt.split()[0]
        create_checkbox(
            form,
            f"{field_prefix}_{opt_key}",
            pos=(opt_x, opt_y),
            size=0.6 * cm,
            tooltip=opt,
        )
        c.drawString(opt_x + 1 * cm, opt_y + 0.15 * cm, opt)
        opt_x += 3.8 * cm

    y_pos = opt_y - 2.0 * cm

    # 2. Energy scale
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, y_pos, energy_prompt)

    c.setFont(PDFStyle.FONT_ITALIC, 9)
    c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
    c.drawString(text_x, y_pos - 0.5 * cm, "Épuisé (0)")
    c.drawRightString(text_x + 14 * cm, y_pos - 0.5 * cm, "Plein de vitalité (10)")

    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setLineWidth(1)
    c.line(text_x, y_pos - 1.5 * cm, text_x + 14 * cm, y_pos - 1.5 * cm)

    for i in range(11):
        x_mark = text_x + i * 1.4 * cm
        c.setLineWidth(0.5)
        c.line(x_mark, y_pos - 1.6 * cm, x_mark, y_pos - 1.4 * cm)

        create_checkbox(
            form,
            f"{field_prefix}_energy_{i}",
            pos=(x_mark - 0.22 * cm, y_pos - 2.1 * cm),
            size=0.45 * cm,
            tooltip=f"Niveau {i}",
        )

        c.setFont(PDFStyle.FONT_BODY, 8)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawCentredString(x_mark, y_pos - 2.6 * cm, str(i))

    y_pos = y_pos - 4.0 * cm

    # 3. Thought reflection
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, y_pos, thought_prompt)

    box_h = 5.0 * cm
    create_input_field(
        form,
        f"{field_prefix}_pensee",
        pos=(text_x, y_pos - box_h - 0.5 * cm),
        size=(width - text_x - 1.5 * cm, box_h),
        tooltip="Pensée envahissante ou intention",
        multiline=True,
    )

    draw_page_decorations(
        c, width, height, part_title=part_title, x_offset=card_margin
    )
    c.showPage()


def create_standard_quadrants_page(
    c,
    title="Ma Vision 360°",
    part_title=None,
    instruction="Instruction : Pour chaque domaine, écrivez une phrase de synthèse sur votre aspiration.",
    quadrants_data=None,
    field_prefix="vision",
):
    """
    Standard 4-Quadrant / Matrix Page.
    quadrants_data is a list of 4 tuples or dicts:
    [
        ("Professionnel", "Sens, Mission, Salaire", "pro"),
        ("Personnel", "Temps pour soi, Santé", "perso"),
        ("Social / Relationnel", "Relations, Équilibre", "social"),
        ("Cadre & Autonomie", "Besoin de liberté", "cadre")
    ]
    """
    width, height = A4
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, title, pos=(text_x, text_top))

    if instruction:
        c.setFont(PDFStyle.FONT_BODY, 11)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(text_x, new_y - 0.2 * cm, instruction)

    center_x = card_margin + (width - card_margin) / 2
    center_y = height / 2 - 2.5 * cm

    # Draw Radar Background
    c.setLineWidth(1)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setFillColor(PDFStyle.COLOR_BG_BLOB)
    c.circle(center_x, center_y, 7 * cm, stroke=1, fill=1)

    c.setLineWidth(0.5)
    c.setFillColor(PDFStyle.COLOR_CARD_CREME)
    c.circle(center_x, center_y, 3.5 * cm, stroke=1, fill=1)

    c.saveState()
    c.setDash(4, 4)
    c.line(center_x, center_y - 7 * cm, center_x, center_y + 7 * cm)
    c.line(center_x - 7 * cm, center_y, center_x + 7 * cm, center_y)
    c.restoreState()

    if not quadrants_data:
        quadrants_data = [
            ("Professionnel", "Sens, Mission, Salaire", "pro"),
            ("Personnel", "Temps pour soi, Santé", "perso"),
            ("Social/Familial", "Relations, Équilibre", "social"),
            ("Hiérarchie/Structure", "Besoin de cadre vs Liberté", "cadre"),
        ]

    # Grid positions: (dx, dy)
    positions = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
    form = c.acroForm

    for item, (dx, dy) in zip(quadrants_data, positions):
        if isinstance(item, (tuple, list)):
            main_title = item[0]
            sub_title = f"({item[1]})" if len(item) > 1 and item[1] else ""
            fid = item[2] if len(item) > 2 else f"{field_prefix}_{main_title}"
        elif isinstance(item, dict):
            main_title = item.get("title", "")
            sub = item.get("subtitle", "")
            sub_title = f"({sub})" if sub else ""
            fid = item.get("field_id", f"{field_prefix}_{main_title}")
        else:
            main_title = str(item)
            sub_title = ""
            fid = f"{field_prefix}_{main_title}"

        q_center_x = center_x + (dx * (3.5 * cm))
        field_width = 5.8 * cm
        field_height = 1.8 * cm

        if dy == 1:
            text_y = center_y + 5.2 * cm
            f_y = center_y + 1.5 * cm
        else:
            text_y = center_y - 5.0 * cm
            f_y = center_y - 3.3 * cm

        f_x = q_center_x - (field_width / 2)

        # Title pill badge
        text_width = c.stringWidth(main_title, PDFStyle.FONT_BRANDING, 14)
        c.saveState()
        c.setFillColor(PDFStyle.COLOR_WHITE, alpha=0.95)
        c.roundRect(
            q_center_x - text_width / 2 - 10,
            text_y - 5,
            text_width + 20,
            20,
            radius=10,
            fill=1,
            stroke=0,
        )
        c.restoreState()

        c.setFont(PDFStyle.FONT_BRANDING, 14)
        c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
        c.drawCentredString(q_center_x, text_y, main_title)

        if sub_title:
            sub_width = c.stringWidth(sub_title, PDFStyle.FONT_BODY, 9)
            c.saveState()
            c.setFillColor(PDFStyle.COLOR_WHITE, alpha=0.95)
            c.roundRect(
                q_center_x - sub_width / 2 - 6,
                text_y - 0.5 * cm - 4,
                sub_width + 12,
                14,
                radius=7,
                fill=1,
                stroke=0,
            )
            c.restoreState()

            c.setFont(PDFStyle.FONT_BODY, 9)
            c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            c.drawCentredString(q_center_x, text_y - 0.5 * cm, sub_title)

        create_input_field(
            form,
            fid,
            pos=(f_x, f_y),
            size=(field_width, field_height),
            tooltip=f"Synthèse {main_title}",
            multiline=True,
            fill_color=PDFStyle.COLOR_CARD_CREME,
        )

    draw_page_decorations(
        c, width, height, part_title=part_title, x_offset=card_margin
    )
    c.showPage()


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
    Standard Two-Column Comparative Page (Mirror Table).
    rows_data is a list of labels or tuples:
    [
        "1. Vie personnelle & familiale",
        "2. Épreuves & défis surmontés",
        "3. Engagements & loisirs",
        "4. Réussites marquantes",
    ]
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, title, pos=(text_x, text_top))

    target_width = width - text_x - 1.0 * cm

    if intro_text:
        c.setFont(PDFStyle.FONT_BODY, 10)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        text_y = new_y - 0.3 * cm
        for line in simpleSplit(intro_text, PDFStyle.FONT_BODY, 10, target_width):
            c.drawString(text_x, text_y, line)
            text_y -= 0.45 * cm
        y_start = text_y - 0.5 * cm
    else:
        y_start = new_y - 0.8 * cm

    # Headers
    col1_x = text_x
    col2_x = text_x + target_width / 2.0 + 0.5 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(col1_x, y_start, col1_header)

    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(col2_x, y_start, col2_header)

    if not rows_data:
        rows_data = [
            "1. Première situation marquante",
            "2. Deuxième situation marquante",
            "3. Troisième situation marquante",
            "4. Autre élément clé",
        ]

    n_rows = max(len(rows_data), 1)
    center_x = text_x + target_width / 2.0
    col_width = (target_width / 2.0) - 1.0 * cm
    form = c.acroForm

    min_safe_y = 2.8 * cm
    available_h = (y_start - 0.8 * cm) - min_safe_y
    row_height = max(min(available_h / n_rows, 3.5 * cm), 2.4 * cm)

    y_row = y_start - 0.8 * cm - row_height

    for i, item in enumerate(rows_data):
        if isinstance(item, str):
            row_label = item
            left_tip = row_label
            right_tip = f"Enseignement {i+1}"
        elif isinstance(item, dict):
            left_tip = (
                item.get("left")
                or item.get("col1")
                or item.get("left_tooltip")
                or item.get("situation")
                or item.get("croyance")
                or ""
            )
            right_tip = (
                item.get("right")
                or item.get("col2")
                or item.get("right_tooltip")
                or item.get("solution")
                or item.get("levier")
                or item.get("enseignement")
                or f"Enseignement {i+1}"
            )
            row_label = item.get("label") or item.get("title")
            if not row_label:
                if left_tip:
                    truncated = (left_tip[:40] + "...") if len(left_tip) > 40 else left_tip
                    row_label = f"{i+1}. {truncated}"
                else:
                    row_label = f"Point {i+1}"
        elif isinstance(item, (tuple, list)):
            row_label = str(item[0]) if len(item) > 0 else f"Point {i+1}"
            left_tip = str(item[1]) if len(item) > 1 else row_label
            right_tip = str(item[2]) if len(item) > 2 else f"Enseignement {i+1}"
        else:
            row_label = str(item)
            left_tip = row_label
            right_tip = f"Enseignement {i+1}"

        # Row label
        c.setFont(PDFStyle.FONT_BODY, 9)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(col1_x, y_row + row_height - 0.4 * cm, row_label)

        # Arrow between columns
        cx_arrow = center_x
        c.setStrokeColor(PDFStyle.COLOR_TEXT_SECONDARY)
        c.setLineWidth(1)
        arrow_y = y_row + (row_height - 0.8 * cm) / 2
        c.line(cx_arrow - 0.35 * cm, arrow_y, cx_arrow + 0.35 * cm, arrow_y)
        c.line(cx_arrow + 0.35 * cm, arrow_y, cx_arrow + 0.1 * cm, arrow_y + 0.1 * cm)
        c.line(cx_arrow + 0.35 * cm, arrow_y, cx_arrow + 0.1 * cm, arrow_y - 0.1 * cm)

        # Left Input
        create_input_field(
            form,
            f"{field_prefix}_col1_{i+1}",
            pos=(col1_x, y_row),
            size=(col_width, row_height - 0.8 * cm),
            multiline=True,
            tooltip=left_tip,
        )

        # Right Input
        create_input_field(
            form,
            f"{field_prefix}_col2_{i+1}",
            pos=(col2_x, y_row),
            size=(col_width, row_height - 0.8 * cm),
            multiline=True,
            tooltip=right_tip,
        )

        y_row -= row_height

    draw_page_decorations(
        c, width, height, part_title=part_title, x_offset=card_margin
    )
    c.showPage()


def create_standard_enquete_page(
    c,
    title="Fiche Enquête Réseau & Métier",
    part_title="EXPLORATION DU TERRAIN",
    intro_text="Interrogez un professionnel ou un pair pour confronter vos hypothèses à la réalité de terrain sans chercher à vendre.",
    questions=None,
    field_prefix="enquete",
):
    """
    Gabarit standard d'enquête terrain / Customer Discovery.
    1. Carte d'identité de l'échange (Nom, Fonction, Entreprise, Date)
    2. 3 blocs d'analyse qualitative avec boîtes interactives généreuses.
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, title, pos=(text_x, text_top))
    target_width = width - text_x - 1.0 * cm
    form = c.acroForm

    if intro_text:
        c.setFont(PDFStyle.FONT_BODY, 10)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        text_y = new_y - 0.25 * cm
        for line in simpleSplit(intro_text, PDFStyle.FONT_BODY, 10, target_width):
            c.drawString(text_x, text_y, line)
            text_y -= 0.42 * cm
        y_cursor = text_y - 0.35 * cm
    else:
        y_cursor = new_y - 0.6 * cm

    # 1. Contact Info Card (2.2 cm height)
    contact_card_h = 2.2 * cm
    draw_card(c, text_x, y_cursor - contact_card_h, target_width, contact_card_h)

    col_w = (target_width - 0.8 * cm) / 2.0
    half1_x = text_x + 0.3 * cm
    half2_x = text_x + 0.3 * cm + col_w + 0.2 * cm

    # Labels and fields row 1
    c.setFont(PDFStyle.FONT_SUBTITLE, 8.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(half1_x, y_cursor - 0.45 * cm, "INTERLOCUTEUR (NOM, PRÉNOM) :")
    c.drawString(half2_x, y_cursor - 0.45 * cm, "FONCTION / RÔLE :")

    create_input_field(
        form,
        f"{field_prefix}_contact_nom",
        pos=(half1_x, y_cursor - 1.05 * cm),
        size=(col_w, 0.55 * cm),
        fill_color=colors.white,
    )
    create_input_field(
        form,
        f"{field_prefix}_contact_role",
        pos=(half2_x, y_cursor - 1.05 * cm),
        size=(col_w, 0.55 * cm),
        fill_color=colors.white,
    )

    # Labels and fields row 2
    c.drawString(half1_x, y_cursor - 1.35 * cm, "ENTREPRISE / SECTEUR :")
    c.drawString(half2_x, y_cursor - 1.35 * cm, "DATE & CONTEXTE DE L'ÉCHANGE :")

    create_input_field(
        form,
        f"{field_prefix}_contact_ent",
        pos=(half1_x, y_cursor - 1.95 * cm),
        size=(col_w, 0.55 * cm),
        fill_color=colors.white,
    )
    create_input_field(
        form,
        f"{field_prefix}_contact_date",
        pos=(half2_x, y_cursor - 1.95 * cm),
        size=(col_w, 0.55 * cm),
        fill_color=colors.white,
    )

    y_cursor -= (contact_card_h + 0.4 * cm)

    # 2. Three Analytical Question Cards
    if not questions:
        questions = [
            (
                "1. Besoins & Douleurs réelles",
                "Quelles difficultés majeures ou irritants cette personne rencontre-t-elle au quotidien ?",
            ),
            (
                "2. Solutions actuelles & Limites",
                "Que fait-elle aujourd'hui pour y répondre ? Quels sont ses freins ou manques ?",
            ),
            (
                "3. Pépites & Recommandations",
                "Quels conseils clés, avis sur votre idée ou autres contacts vous a-t-elle recommandés ?",
            ),
        ]

    n_q = max(len(questions), 1)
    min_safe_y = 2.8 * cm
    gap = 0.35 * cm
    available_h = (y_cursor - min_safe_y) - (n_q - 1) * gap
    card_h = max(available_h / n_q, 4.0 * cm)

    for i, q in enumerate(questions):
        if isinstance(q, (tuple, list)):
            q_title = str(q[0]) if len(q) > 0 else f"Question {i+1}"
            q_sub = str(q[1]) if len(q) > 1 else ""
        elif isinstance(q, dict):
            q_title = q.get("title") or q.get("question") or q.get("label") or f"Question {i+1}"
            q_sub = q.get("subtitle") or q.get("desc") or q.get("description") or ""
        else:
            q_title = str(q)
            q_sub = ""

        draw_card(c, text_x, y_cursor - card_h, target_width, card_h)

        # Header bar in card
        c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
        c.setFillColor(PDFStyle.COLOR_ACCENT_RED if i == 0 else PDFStyle.COLOR_ACCENT_BLUE)
        c.drawString(text_x + 0.35 * cm, y_cursor - 0.5 * cm, q_title.upper())

        if q_sub:
            c.setFont(PDFStyle.FONT_ITALIC, 8.5)
            c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
            c.drawString(text_x + 0.35 * cm, y_cursor - 0.85 * cm, q_sub)
            input_y = y_cursor - card_h + 0.25 * cm
            input_h = card_h - 1.25 * cm
        else:
            input_y = y_cursor - card_h + 0.25 * cm
            input_h = card_h - 0.9 * cm

        create_input_field(
            form,
            f"{field_prefix}_q_{i+1}",
            pos=(text_x + 0.35 * cm, input_y),
            size=(target_width - 0.7 * cm, input_h),
            multiline=True,
            fill_color=colors.white,
        )

        y_cursor -= (card_h + gap)

    draw_page_decorations(c, width, height, part_title=part_title, x_offset=card_margin)
    c.showPage()


def create_standard_roadmap_page(
    c,
    title="Feuille de Route 30 · 60 · 90 Jours",
    part_title="PLAN D'ACTION OPÉRATIONNEL",
    intro_text="Découpez votre mise en action en trois jalons progressifs pour ancrer des victoires rapides et structurer votre lancement.",
    stages_data=None,
    field_prefix="roadmap",
):
    """
    Gabarit standard Feuille de Route / Timeline d'action (3 Paliers).
    Chaque palier comprend :
    - En-tête avec Pill Badge de couleur (Palier) + Thème de cap
    - Filet séparateur interne
    - Colonne Gauche (42%) : Cap & Objectif clé + Livrable / KPI
    - Colonne Droite (58%) : 3 Actions prioritaires avec cases à cocher parfaitement aérées
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, title, pos=(text_x, text_top))
    target_width = width - text_x - 1.0 * cm
    form = c.acroForm

    if intro_text:
        c.setFont(PDFStyle.FONT_BODY, 10)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        text_y = new_y - 0.25 * cm
        for line in simpleSplit(intro_text, PDFStyle.FONT_BODY, 10, target_width):
            c.drawString(text_x, text_y, line)
            text_y -= 0.42 * cm
        y_cursor = text_y - 0.35 * cm
    else:
        y_cursor = new_y - 0.6 * cm

    if not stages_data:
        stages_data = [
            {
                "period": "PALIER 1 · 0 À 30 JOURS",
                "theme": "CONSOLIDER & TESTER",
                "default_obj": "Valider l'intérêt du marché et tester l'offre pilote auprès de 5 pairs.",
                "actions": [
                    "Mener 5 entretiens d'enquête terrain ciblés",
                    "Formaliser la proposition de valeur sur 1 page",
                    "Identifier et contacter 2 premiers prospects cibles",
                ],
                "default_kpi": "5 entretiens qualifiés menés et 1 retour d'intérêt concret",
            },
            {
                "period": "PALIER 2 · 30 À 60 JOURS",
                "theme": "STRUCTURER & SÉCURISER",
                "default_obj": "Poser le cadre juridique, formaliser les tarifs et préparer le lancement.",
                "actions": [
                    "Valider le statut juridique et les aides de transition (ARE/ARCE)",
                    "Fixer la grille tarifaire et créer le modèle de proposition/devis",
                    "Activer son réseau relationnel (e-mail d'annonce de lancement)",
                ],
                "default_kpi": "Cadre juridique validé et 3 devis/propositions envoyés",
            },
            {
                "period": "PALIER 3 · 60 À 90 JOURS",
                "theme": "LANCER & DÉVELOPPER",
                "default_obj": "Signer les premières missions, recueillir des retours et caler son rythme.",
                "actions": [
                    "Signer et délivrer la première mission pilote avec succès",
                    "Recueillir un témoignage ou une recommandation client",
                    "Faire le bilan d'étape et ajuster ses priorités pour le trimestre",
                ],
                "default_kpi": "Premier chiffre d'affaires encaissé et premier avis client obtenu",
            },
        ]

    min_safe_y = 2.8 * cm
    n_stages = max(len(stages_data), 1)
    gap = 0.4 * cm
    available_h = (y_cursor - min_safe_y) - (n_stages - 1) * gap
    stage_h = min(max(available_h / n_stages, 5.0 * cm), 5.3 * cm)

    colors_header = [
        PDFStyle.COLOR_ACCENT_BLUE,
        PDFStyle.COLOR_ACCENT_RED,
        PDFStyle.COLOR_SUCCESS,
    ]

    for i, stage in enumerate(stages_data):
        if isinstance(stage, dict):
            period = stage.get("period") or stage.get("palier") or f"PALIER {i+1}"
            st_theme = stage.get("theme") or stage.get("title") or ""
            def_obj = stage.get("default_obj") or stage.get("obj") or stage.get("objective") or stage.get("objectif") or ""
            actions = stage.get("actions") or stage.get("items") or ["Action 1", "Action 2", "Action 3"]
            def_kpi = stage.get("default_kpi") or stage.get("kpi") or stage.get("resultat") or ""
        else:
            period = f"PALIER {i+1}"
            st_theme = str(stage)
            def_obj = ""
            actions = ["Action 1", "Action 2", "Action 3"]
            def_kpi = ""
        h_color = colors_header[i % len(colors_header)]

        # 1. Main White Card Container with subtle border
        c.saveState()
        c.setFillColor(PDFStyle.COLOR_WHITE)
        c.setStrokeColor(PDFStyle.COLOR_LINE)
        c.setLineWidth(0.6)
        c.roundRect(text_x, y_cursor - stage_h, target_width, stage_h, 6, fill=1, stroke=1)
        c.restoreState()

        # 2. Top Header inside Card:
        # A. Pill Badge on the left
        pill_w = 4.8 * cm
        pill_h = 0.55 * cm
        pill_x = text_x + 0.35 * cm
        pill_y = y_cursor - 0.72 * cm

        c.saveState()
        c.setFillColor(h_color)
        c.roundRect(pill_x, pill_y, pill_w, pill_h, radius=pill_h / 2.0, fill=1, stroke=0)
        c.setFont(PDFStyle.FONT_BRANDING, 8.5)
        c.setFillColor(PDFStyle.COLOR_WHITE)
        c.drawCentredString(pill_x + pill_w / 2.0, pill_y + 0.16 * cm, period.upper())
        c.restoreState()

        # B. Focus Theme text next to the pill
        if st_theme:
            c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
            c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            c.drawString(pill_x + pill_w + 0.4 * cm, pill_y + 0.16 * cm, st_theme.upper())

        # C. Thin horizontal divider line
        line_y = y_cursor - 0.9 * cm
        c.saveState()
        c.setStrokeColor(PDFStyle.COLOR_LINE)
        c.setLineWidth(0.4)
        c.line(text_x + 0.35 * cm, line_y, text_x + target_width - 0.35 * cm, line_y)
        c.restoreState()

        # 3. Two-Column Layout below divider line
        # Left column (Objectif & KPI): 42% width (~6.8 cm)
        # Right column (3 Actions): 58% width (~9.2 cm)
        sep_x = text_x + 7.2 * cm
        c.saveState()
        c.setStrokeColor(PDFStyle.COLOR_LINE)
        c.setLineWidth(0.4)
        c.setDash(2, 2)
        c.line(sep_x, line_y - 0.15 * cm, sep_x, y_cursor - stage_h + 0.25 * cm)
        c.restoreState()

        left_x = text_x + 0.35 * cm
        left_w = sep_x - left_x - 0.35 * cm

        right_x = sep_x + 0.35 * cm
        right_w = text_x + target_width - right_x - 0.35 * cm

        # --- LEFT COLUMN ---
        # Objectif Clé
        c.setFont(PDFStyle.FONT_SUBTITLE, 7.5)
        c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
        c.drawString(left_x, line_y - 0.35 * cm, "🎯 CAP & OBJECTIF DU PALIER :")

        create_input_field(
            form,
            f"{field_prefix}_s{i+1}_obj",
            pos=(left_x, line_y - 1.85 * cm),
            size=(left_w, 1.35 * cm),
            multiline=True,
            tooltip=def_obj,
            fill_color=PDFStyle.COLOR_CARD_CREME,
        )

        # Indicateur de succès (KPI)
        c.drawString(left_x, line_y - 2.25 * cm, "🏁 RÉSULTAT OBSERVABLE (KPI) :")

        create_input_field(
            form,
            f"{field_prefix}_s{i+1}_kpi",
            pos=(left_x, line_y - 3.85 * cm),
            size=(left_w, 1.45 * cm),
            multiline=True,
            tooltip=def_kpi,
            fill_color=PDFStyle.COLOR_CARD_CREME,
        )

        # --- RIGHT COLUMN ---
        c.setFont(PDFStyle.FONT_SUBTITLE, 7.5)
        c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
        c.drawString(right_x, line_y - 0.35 * cm, "✅ 3 ACTIONS PRIORITAIRES :")

        chk_size = 11
        for a_idx, act_label in enumerate(actions[:3]):
            box_h = 0.85 * cm
            box_y = line_y - (1.40 * cm + a_idx * 1.10 * cm)

            create_checkbox(
                form,
                f"{field_prefix}_s{i+1}_chk_{a_idx+1}",
                pos=(right_x, box_y + 0.15 * cm),
                size=chk_size,
                tooltip=f"Cocher action {a_idx+1}",
            )

            create_input_field(
                form,
                f"{field_prefix}_s{i+1}_act_{a_idx+1}",
                pos=(right_x + 0.55 * cm, box_y),
                size=(right_w - 0.55 * cm, box_h),
                multiline=True,
                tooltip=act_label,
                fill_color=PDFStyle.COLOR_CARD_CREME,
            )

        y_cursor -= (stage_h + gap)

    draw_page_decorations(c, width, height, part_title=part_title, x_offset=card_margin)
    c.showPage()


