import os
from reportlab.lib import colors
from reportlab.lib.units import cm


class PDFStyle:
    """
    Tokens of the « Éditorial & Affirmé » art direction (DA-workbook.md, design-system/tokens.json),
    adapted to A4 print: a single palette, sizes in points.
    """

    # A. Colors
    # Neutrals
    COLOR_SURFACE = colors.HexColor("#FAF8F5")  # cream
    COLOR_SURFACE_CARD = colors.HexColor("#FFFFFF")  # white: pages, white cards, fields to fill in
    COLOR_SURFACE_ALT = colors.HexColor("#F1EBE6")  # linen
    COLOR_INK = colors.HexColor("#111111")  # main text, drawn strokes
    COLOR_INK_MUTED = colors.HexColor("#4A4844")  # secondary text, eyebrows
    COLOR_LINE = colors.HexColor("#E5E5EE")  # rules, white card border
    COLOR_LINE_STRONG = colors.HexColor("#8A8680")  # border of fields to fill in (3:1)

    # Brand
    COLOR_CORAL = colors.HexColor("#FF3B3B")  # decoration; as text, only at 18 pt and up, on white
    COLOR_CORAL_STRONG = colors.HexColor("#C22626")  # any small coral text, bullets, stamp
    COLOR_BLUE = colors.HexColor("#251FD3")  # second accent: title word, icons, big numbers

    # Every page is tinted off-white (DocumentBuilder), halfway between cream and linen;
    # white is for cards and fields to fill in. Bright coral title accents keep 3:1 on it
    # (from 18 pt); a page as dark as linen would need COLOR_TITLE_ACCENT = COLOR_CORAL_STRONG.
    COLOR_PAGE = colors.HexColor("#F6F2EE")
    COLOR_TITLE_ACCENT = COLOR_CORAL

    # Pastels: card backgrounds, post-its, background discs. Text on them stays ink.
    PASTELS = {
        "almond": colors.HexColor("#FFDDCB"),
        "jasmine": colors.HexColor("#FFEA8C"),
        "lilac": colors.HexColor("#E7E0FF"),
        "sky": colors.HexColor("#DDEAF9"),
        "mint": colors.HexColor("#D7F2E3"),
        "blush": colors.HexColor("#FFE2D9"),
    }
    COLOR_ALMOND = PASTELS["almond"]
    COLOR_JASMINE = PASTELS["jasmine"]  # kept for the post-it (deliverable)
    COLOR_LILAC = PASTELS["lilac"]
    COLOR_SKY = PASTELS["sky"]
    COLOR_MINT = PASTELS["mint"]
    COLOR_BLUSH = PASTELS["blush"]

    # Dominant pastel of each core workbook (chapters 0 to 6); lilac for any other document
    CARNET_PASTELS = {0: "lilac", 1: "sky", 2: "almond", 3: "mint", 4: "blush", 5: "lilac", 6: "sky"}
    DEFAULT_PASTEL = "lilac"

    # Former names, kept for the hand-drawn chapter pages until they are redone (lot E5)
    COLOR_BG_NUDE = COLOR_PAGE
    COLOR_WHITE = COLOR_SURFACE_CARD
    COLOR_FIELD_BG = COLOR_SURFACE_CARD
    COLOR_ACCENT_BLUE = COLOR_BLUE
    COLOR_ACCENT_RED = COLOR_CORAL_STRONG
    COLOR_ACCENT_YELLOW = COLOR_JASMINE
    COLOR_TEXT_MAIN = COLOR_INK
    COLOR_TEXT_SECONDARY = COLOR_INK_MUTED

    # B. Fonts (files in assets/fonts, see its README). register_fonts() swaps a name
    # for a Helvetica font when its file is missing.
    FONT_HEADING = "DMSans-ExtraBold"  # large titles (800)
    FONT_HEADING_BOLD = "DMSans-Bold"  # regular titles, card titles, questions (700)
    FONT_HEADING_ITALIC = "DMSans-Italic"  # second part of a title (italic 400)
    FONT_BODY = "Manrope-Regular"  # running text
    FONT_BODY_BOLD = "Manrope-SemiBold"  # bold within text (600)
    FONT_LOGO = "Manrope-ExtraBold"  # logotype (800)
    FONT_LABEL = "PTMono-Regular"  # markers: eyebrows, labels, numbers, folio. Never bold.
    FONT_SERIF = "InstrumentSerif-Italic"  # post-its, annotations. Never bold nor upright.
    FONT_ICONS = "MaterialSymbolsOutlined"  # icons, drawn by code point

    # Former names (chapters until lot E5), kept in sync by register_fonts()
    FONT_TITLE = FONT_HEADING
    FONT_SUBTITLE = FONT_HEADING_BOLD
    FONT_ITALIC = FONT_HEADING_ITALIC
    FONT_BRANDING = FONT_HEADING
    FONT_HAND = FONT_SERIF

    FONT_TITLE_FALLBACK = "Helvetica-Bold"
    FONT_BODY_FALLBACK = "Helvetica"
    FONT_ITALIC_FALLBACK = "Helvetica-Oblique"

    # C. Type scale for print (pt). No arbitrary sizes.
    SIZE_TITLE_COVER = 40
    SIZE_TITLE_PAGE = 28  # page title (titre-section)
    SIZE_TITLE_PAGE_MIN = 20  # a long title shrinks down to this before wrapping further
    SIZE_TITLE_BLOCK = 18  # chapter title, end-of-workbook title
    SIZE_TITLE_CARD = 13  # card title
    SIZE_TITLE_ELEMENT = 11.5  # question, list item, deliverable
    SIZE_LEAD = 12  # lead paragraph
    SIZE_BODY = 10.5
    SIZE_BODY_SMALL = 9.5  # smallest reading size
    SIZE_EYEBROW = 8.5  # eyebrow
    SIZE_LABEL = 8  # pill label
    SIZE_FOLIO = 7.5
    SIZE_NUMBER = 60  # big chapter number
    SIZE_POSTIT = 14
    SIZE_ANNOTATION = 15

    LEADING_BODY = 1.5
    LEADING_TITLE = 1.05
    TRACKING_TITLE = -0.03  # em
    TRACKING_TITLE_XL = -0.05
    TRACKING_TITLE_CARD = -0.02
    TRACKING_EYEBROW = 0.2
    TRACKING_LABEL = 0.14

    # D. Layout (pt)
    MARGIN_MAIN = 2.0 * cm  # left and right margins
    EYEBROW_TOP = 2.0 * cm  # from the top of the page to the eyebrow baseline
    CONTENT_BOTTOM = 2.0 * cm  # no block goes lower
    FOLIO_Y = 1.1 * cm
    GAP_BLOCK = 0.75 * cm  # entre deux blocs
    CARD_PADDING = 0.55 * cm

    RADIUS_CARD = 16
    RADIUS_FIELD = 8
    RADIUS_POSTIT = 1.5
    RADIUS_STAMP = 5
    CARD_RADIUS = RADIUS_CARD  # former name

    LINE_WIDTH_FIELD = 1
    LINE_WIDTH_ARROW = 1.3

    # E. Paths
    SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../Scripts
    PROJECT_DIR = os.path.dirname(SCRIPTS_DIR)

    FONTS_DIR = os.path.join(PROJECT_DIR, "assets", "fonts")
    ILLUS_DIR = os.path.join(PROJECT_DIR, "assets", "illustrations")

    # Illustrations of the former art direction, still used by some chapters (redone in lot E5)
    PATH_ILLU_COVER = os.path.join(ILLUS_DIR, "01a_ILLU.png")
    PATH_GUILLEMETS = os.path.join(ILLUS_DIR, "guillemets.png")
    PATH_STAMP = os.path.join(ILLUS_DIR, "stamp_rouge.png")
    PATH_PLUME_TEXTURE = os.path.join(ILLUS_DIR, "plume texture.png")
    PATH_PLANTE_BLEUE = os.path.join(ILLUS_DIR, "plante bleue copy.png")
    PATH_PLANTE_ROSE_OMBRE = os.path.join(ILLUS_DIR, "plante rose ombre copy.png")
    # Logos of the Programme brochure
    PATH_LOGO_CPF = os.path.join(ILLUS_DIR, "logo_cpf.png")
    PATH_LOGO_FRANCE_TRAVAIL = os.path.join(ILLUS_DIR, "logo_france_travail.png")
    PATH_LOGO_QUALIOPI = os.path.join(ILLUS_DIR, "logo_qualiopi.jpg")
