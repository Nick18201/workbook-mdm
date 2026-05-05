import os
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


def draw_image_with_form(
    c,
    image_path,
    x,
    y,
    width,
    height,
    anchor="c",
    mask="auto",
    preserveAspectRatio=True,
):
    """
    Draws an image using Form XObjects to cache it at a specific size.
    This prevents ReportLab from re-embedding the image and re-emitting drawing
    operators for identical images (like repeated backgrounds or logos).
    """
    if not hasattr(c, "_image_form_cache"):
        c._image_form_cache = {}

    # Key includes all arguments that affect the generated XObject content
    # Note: anchor does not affect the XObject content (it's drawn at 0,0 inside),
    # but rather how it's positioned, EXCEPT drawImage handles anchor internally
    # by shifting the image inside the bounding box. So anchor must be in the key.
    cache_key = (image_path, width, height, anchor, mask, preserveAspectRatio)

    if cache_key not in c._image_form_cache:
        form_name = f"ImgForm_{len(c._image_form_cache)}"
        c.beginForm(form_name)
        img = cached_ImageReader(image_path)
        # We always draw at (0, 0) inside the form's local coordinate system
        c.drawImage(
            img,
            0,
            0,
            width=width,
            height=height,
            mask=mask,
            preserveAspectRatio=preserveAspectRatio,
            anchor=anchor,
        )
        c.endForm()
        c._image_form_cache[cache_key] = form_name

    c.saveState()
    c.translate(x, y)
    c.doForm(c._image_form_cache[cache_key])
    c.restoreState()
