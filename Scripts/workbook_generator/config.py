import os
from reportlab.lib import colors
from reportlab.lib.units import cm


class PDFStyle:
    THEMES = ["earth", "indigo"]

    # Initialisation des variables de couleurs pour le type hinting ou l'accès avant set_theme (optionnel mais plus sûr)
    COLOR_BG_NUDE = colors.HexColor("#FFFCE8")
    COLOR_ACCENT_BLUE = colors.HexColor("#D19B8D")
    COLOR_ACCENT_RED = colors.HexColor("#8D6257")
    COLOR_ACCENT_YELLOW = colors.HexColor("#BFAF94")
    COLOR_WHITE = colors.HexColor("#FFFFFF")
    COLOR_TEXT_MAIN = colors.HexColor("#8D6257")
    COLOR_TEXT_SECONDARY = colors.HexColor("#A27164")
    COLOR_SUCCESS = colors.HexColor("#6F926D")
    COLOR_FIELD_BG = colors.HexColor("#F2F7F1")
    COLOR_CARD_CREME = colors.HexColor("#FAF7F2")
    COLOR_BG_BLOB = colors.HexColor("#FDE8DB")
    COLOR_SHADOW = colors.HexColor("#79544A")
    COLOR_LINE = colors.HexColor("#D19B8D")

    @classmethod
    def set_theme(cls, theme_name="earth"):
        """Sets the active color palette."""
        palettes = {
            "indigo": {
                "COLOR_BG_NUDE": "#FFF0E6",
                "COLOR_ACCENT_BLUE": "#2F2EFA",
                "COLOR_ACCENT_RED": "#FF4D4D",
                "COLOR_ACCENT_YELLOW": "#FFEB3B",
                "COLOR_WHITE": "#FFFFFF",
                "COLOR_TEXT_MAIN": "#2F2EFA",
                "COLOR_TEXT_SECONDARY": "#2F2EFA",
                "COLOR_SUCCESS": "#2E7D32",
                "COLOR_FIELD_BG": "#F0F4FF",
                "COLOR_CARD_CREME": "#FFF8F2",
                "COLOR_BG_BLOB": "#FADADD",
                "COLOR_SHADOW": "#2F2EFA",
                "COLOR_LINE": "#2F2EFA",
            },
            "earth": {
                "COLOR_BG_NUDE": "#FFFCE8",
                "COLOR_ACCENT_BLUE": "#D19B8D",
                "COLOR_ACCENT_RED": "#8D6257",
                "COLOR_ACCENT_YELLOW": "#BFAF94",
                "COLOR_WHITE": "#FFFFFF",
                "COLOR_TEXT_MAIN": "#8D6257",
                "COLOR_TEXT_SECONDARY": "#A27164",
                "COLOR_SUCCESS": "#6F926D",
                "COLOR_FIELD_BG": "#F2F7F1",
                "COLOR_CARD_CREME": "#FAF7F2",
                "COLOR_BG_BLOB": "#FDE8DB",
                "COLOR_SHADOW": "#79544A",
                "COLOR_LINE": "#D19B8D",
            },
        }

        palette = palettes.get(theme_name, palettes["earth"])
        for attr, hex_val in palette.items():
            setattr(cls, attr, colors.HexColor(hex_val))

    # B. Typography
    FONT_TITLE = "Montserrat-Black"
    FONT_SUBTITLE = "Montserrat-Bold"
    FONT_BODY = "Montserrat-Regular"
    FONT_ITALIC = "Montserrat-Italic"
    FONT_HAND = "Caveat-Regular"
    FONT_BRANDING = "Montserrat-Black"

    # Fallback Fonts
    FONT_TITLE_FALLBACK = "Helvetica-Bold"
    FONT_BODY_FALLBACK = "Helvetica"
    FONT_ITALIC_FALLBACK = "Helvetica-Oblique"

    # Dimensions
    MARGIN_MAIN = 2.0 * cm
    CARD_RADIUS = 10

    # Paths
    # Assuming this file is in 00_Gestion_Projet/Scripts/workbook_generator/config.py
    # Assets are in 00_Gestion_Projet/assets (Up 2 levels)
    # Original script was in 00_Gestion_Projet/Scripts, so assets were "../assets"

    # Current structure:
    # .../Scripts/workbook_generator/config.py
    # .../assets

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )  # .../MDM programme/

    # Correcting path to match user file structure from previous context
    # User listed: c:\Users\nblum\LLM_LAB\PROJETS\MDM programme\00_Gestion_Projet\Scripts
    # So assets should be in 00_Gestion_Projet/assets?
    # Original script: os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
    # Means assets is at 00_Gestion_Projet/assets

    SCRIPTS_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )  # .../Scripts
    PROJECT_DIR = os.path.dirname(SCRIPTS_DIR)  # .../00_Gestion_Projet

    FONTS_DIR = os.path.join(PROJECT_DIR, "assets", "fonts")
    ILLUS_DIR = os.path.join(PROJECT_DIR, "assets", "illustrations")

    # Illustration Paths
    PATH_ILLU_COVER = os.path.join(ILLUS_DIR, "01a_ILLU.png")
    PATH_GUILLEMETS = os.path.join(ILLUS_DIR, "guillemets.png")
    PATH_FLECHE = os.path.join(ILLUS_DIR, "fleche.png")
    PATH_STAMP = os.path.join(ILLUS_DIR, "stamp_rouge.png")
    PATH_BRINDILLE_1 = os.path.join(ILLUS_DIR, "brindilles1_blanc.png")
    PATH_BRINDILLE_2 = os.path.join(ILLUS_DIR, "brindilles2_blanc.png")
    PATH_PLUME_TEXTURE = os.path.join(ILLUS_DIR, "plume texture.png")
    PATH_PLANTE_BLEUE = os.path.join(ILLUS_DIR, "plante bleue copy.png")
    PATH_PLANTE_ROSE_OMBRE = os.path.join(ILLUS_DIR, "plante rose ombre copy.png")
