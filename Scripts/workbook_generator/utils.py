import os
import re
import argparse
import functools
import reportlab.rl_config
from reportlab.lib.utils import simpleSplit, ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .config import PDFStyle

# Disable ASCII Base85 encoding for images to dramatically speed up PDF generation
reportlab.rl_config.useA85 = 0


# Cache the simpleSplit function to avoid redundant text wrapping calculations
# which are heavily used across chapters.
@functools.lru_cache(maxsize=2048)
def cached_simpleSplit(text, fontName, fontSize, maxWidth):
    return simpleSplit(text, fontName, fontSize, maxWidth)


def fit_font_size(text, font_name, size, max_width, min_size=6):
    """Largest font size <= size (down to min_size) at which text fits on one line of max_width."""
    while size > min_size and pdfmetrics.stringWidth(text, font_name, size) > max_width:
        size -= 0.5
    return max(size, min_size)


def ellipsize(text, font_name, size, max_width):
    """Shortens text with a visible '…' so that it fits max_width (never cuts silently)."""
    if pdfmetrics.stringWidth(text, font_name, size) <= max_width:
        return text
    while text and pdfmetrics.stringWidth(text + "…", font_name, size) > max_width:
        text = text[:-1]
    return text.rstrip() + "…"


# Spec text can land in a title, the body or an eyebrow: keep only what all three fonts draw
_TEXT_FONT_FILES = ("Manrope-Regular.ttf", "DMSans-Bold.ttf", "PTMono-Regular.ttf")


@functools.lru_cache(maxsize=1)
def _text_font_codepoints():
    codepoints = None
    for i, filename in enumerate(_TEXT_FONT_FILES):
        path = os.path.join(PDFStyle.FONTS_DIR, filename)
        if not os.path.exists(path):
            return None
        font_codepoints = set(TTFont(f"_glyph_probe_{i}", path).face.charToGlyph)
        codepoints = font_codepoints if codepoints is None else codepoints & font_codepoints
    return frozenset(codepoints)


def strip_unsupported_glyphs(text):
    """
    Removes characters the text fonts cannot draw (emojis, ✓, ☀, ◀…). ReportLab drops
    them silently, leaving gaps such as a stray leading space, so text coming from
    specs is cleaned up front. Text without such characters is returned unchanged.
    """
    codepoints = _text_font_codepoints()
    if codepoints is None or not text:
        return text
    cleaned = "".join(ch for ch in text if ord(ch) < 128 or ch.isspace() or ord(ch) in codepoints)
    if cleaned == text:
        return text
    return re.sub(r"[ \t]{2,}", " ", cleaned).strip()


# (registered name, file in assets/fonts, PDFStyle attribute, fallback when the file is missing)
_FONTS = [
    ("DMSans-ExtraBold", "DMSans-ExtraBold.ttf", "FONT_HEADING", "Helvetica-Bold"),
    ("DMSans-Bold", "DMSans-Bold.ttf", "FONT_HEADING_BOLD", "Helvetica-Bold"),
    ("DMSans-Italic", "DMSans-Italic.ttf", "FONT_HEADING_ITALIC", "Helvetica-Oblique"),
    ("Manrope-Regular", "Manrope-Regular.ttf", "FONT_BODY", "Helvetica"),
    ("Manrope-SemiBold", "Manrope-SemiBold.ttf", "FONT_BODY_BOLD", "Helvetica-Bold"),
    ("Manrope-ExtraBold", "Manrope-ExtraBold.ttf", "FONT_LOGO", "Helvetica-Bold"),
    ("PTMono-Regular", "PTMono-Regular.ttf", "FONT_LABEL", "Courier"),
    ("InstrumentSerif-Italic", "InstrumentSerif-Italic.ttf", "FONT_SERIF", "Times-Italic"),
    ("MaterialSymbolsOutlined", "MaterialSymbolsOutlined.ttf", "FONT_ICONS", None),
]


def register_fonts():
    """
    Registers the art direction fonts with ReportLab (Helvetica, Courier or Times when a
    file is missing; no icons without the Material Symbols file), and the font families
    that let paragraph markup such as <b> switch to the right weight.
    """
    for font_name, filename, style_attr, fallback in _FONTS:
        path = os.path.join(PDFStyle.FONTS_DIR, filename)
        name = fallback
        if font_name in pdfmetrics.getRegisteredFontNames():
            name = font_name
        elif os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, path))
                name = font_name
            except Exception as e:
                print(f"Warning: Could not register font {font_name}: {e}")
        setattr(PDFStyle, style_attr, name)

    s = PDFStyle
    families = {
        s.FONT_BODY: (s.FONT_BODY_BOLD, s.FONT_HEADING_ITALIC, s.FONT_BODY_BOLD),
        s.FONT_HEADING: (s.FONT_HEADING, s.FONT_HEADING_ITALIC, s.FONT_HEADING),
        s.FONT_HEADING_BOLD: (s.FONT_HEADING, s.FONT_HEADING_ITALIC, s.FONT_HEADING),
        s.FONT_HEADING_ITALIC: (s.FONT_HEADING_BOLD, s.FONT_HEADING_ITALIC, s.FONT_HEADING_BOLD),
        # PT Mono and Instrument Serif exist in one style only: no faux bold
        s.FONT_LABEL: (s.FONT_LABEL, s.FONT_LABEL, s.FONT_LABEL),
        s.FONT_SERIF: (s.FONT_SERIF, s.FONT_SERIF, s.FONT_SERIF),
    }
    for normal, (bold, italic, bold_italic) in families.items():
        if normal not in pdfmetrics.standardFonts:
            pdfmetrics.registerFontFamily(normal, normal=normal, bold=bold, italic=italic, boldItalic=bold_italic)

    # Former names used by the chapters until lot E5
    s.FONT_TITLE = s.FONT_HEADING
    s.FONT_SUBTITLE = s.FONT_HEADING_BOLD
    s.FONT_ITALIC = s.FONT_HEADING_ITALIC
    s.FONT_BRANDING = s.FONT_HEADING
    s.FONT_HAND = s.FONT_SERIF


# Cache ImageReader to avoid reloading and re-parsing identical images multiple times.
# This saves I/O and CPU time when the same image (like logos or repeated illustrations)
# is placed on multiple pages.
@functools.lru_cache(maxsize=128)
def cached_ImageReader(filepath):
    return ImageReader(filepath)

# Snake-case alias used by chapter and component modules
cached_image_reader = cached_ImageReader


def create_cli(description, default_output):
    """
    Sets up a standard command-line argument parser for generating PDFs.

    Args:
        description (str): Description of the script for the help message.
        default_output (str): The default output filename for the PDF.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--output",
        type=str,
        default=default_output,
        help="Le nom du fichier PDF généré.",
    )
    return parser.parse_args()
