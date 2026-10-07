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


@functools.lru_cache(maxsize=1)
def _body_font_codepoints():
    path = os.path.join(PDFStyle.FONTS_DIR, "Montserrat-Regular.ttf")
    if not os.path.exists(path):
        return None
    return frozenset(TTFont("_glyph_probe", path).face.charToGlyph)


def strip_unsupported_glyphs(text):
    """
    Removes characters the Montserrat fonts cannot draw (emojis, ✓, ☀…). ReportLab drops
    them silently, leaving gaps such as a stray leading space, so text coming from
    specs is cleaned up front. Text without such characters is returned unchanged.
    """
    codepoints = _body_font_codepoints()
    if codepoints is None or not text:
        return text
    cleaned = "".join(ch for ch in text if ord(ch) < 128 or ch.isspace() or ord(ch) in codepoints)
    if cleaned == text:
        return text
    return re.sub(r"[ \t]{2,}", " ", cleaned).strip()


def register_fonts():
    """Registers fonts with ReportLab, falling back to Helvetica if needed."""
    # Defaults
    PDFStyle.FONT_TITLE = PDFStyle.FONT_TITLE_FALLBACK
    PDFStyle.FONT_BODY = PDFStyle.FONT_BODY_FALLBACK
    PDFStyle.FONT_ITALIC = PDFStyle.FONT_ITALIC_FALLBACK

    try:
        os.makedirs(PDFStyle.FONTS_DIR, exist_ok=True)
    except OSError:
        pass

    # Font Mapping: (Name, Filename, StyleAttr)
    font_map = [
        ("Montserrat-Bold", "Montserrat-Bold.ttf", "FONT_TITLE"),
        ("Montserrat-Black", "Montserrat-Black.ttf", "FONT_BRANDING"),
        ("Montserrat-Regular", "Montserrat-Regular.ttf", "FONT_BODY"),
        ("Montserrat-Italic", "Montserrat-Italic.ttf", "FONT_ITALIC"),
        ("AmaticSC-Regular", "AmaticSC-Regular.ttf", "FONT_HAND"),
        ("Caveat-Regular", "Caveat-Regular.ttf", "FONT_HAND"),
        ("Montserrat-SemiBold", "Montserrat-SemiBold.ttf", "FONT_SUBTITLE"),
    ]

    for font_name, filename, style_attr in font_map:
        path = os.path.join(PDFStyle.FONTS_DIR, filename)
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, path))
                # Update class attributes based on successful registration
                if style_attr == "FONT_TITLE":
                    PDFStyle.FONT_TITLE = font_name
                if style_attr == "FONT_BRANDING":
                    PDFStyle.FONT_BRANDING = font_name
                if style_attr == "FONT_BODY":
                    PDFStyle.FONT_BODY = font_name
                if style_attr == "FONT_ITALIC":
                    PDFStyle.FONT_ITALIC = font_name
                if style_attr == "FONT_HAND":
                    PDFStyle.FONT_HAND = font_name
                if style_attr == "FONT_SUBTITLE":
                    PDFStyle.FONT_SUBTITLE = font_name
            except Exception as e:
                print(f"Warning: Could not register font {font_name}: {e}")


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
        "--theme",
        choices=PDFStyle.THEMES,
        default="indigo",
        help="Le thème de couleurs à utiliser.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=default_output,
        help="Le nom du fichier PDF généré.",
    )
    return parser.parse_args()
