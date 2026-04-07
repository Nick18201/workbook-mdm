import os
from reportlab.lib import colors
from reportlab.lib.units import cm

class PDFStyle:
    # A. Palette de Couleurs
    COLOR_BG_NUDE = colors.HexColor("#FFF0E6")       # Fond Papier
    COLOR_ACCENT_BLUE = colors.HexColor("#2F2EFA")   # Indigo Électrique (Primary)
    COLOR_ACCENT_RED = colors.HexColor("#FF4D4D")    # Rouge Vif (Secondary)
    COLOR_ACCENT_YELLOW = colors.HexColor("#FFEB3B") # Jaune Soleil (Tertiary)
    COLOR_WHITE = colors.HexColor("#FFFFFF")         # Blanc Pur
    COLOR_TEXT_MAIN = colors.HexColor("#2F2EFA")     # Indigo Électrique (Formerly Gunmetal)
    COLOR_TEXT_SECONDARY = colors.HexColor("#2F2EFA") # Gris Souris
    COLOR_SUCCESS = colors.HexColor("#2E7D32")       # Vert Succès
    COLOR_FIELD_BG = colors.HexColor("#F0F4FF")      # Fond Bleu Clair pour champs de texte
    COLOR_CARD_CREME = colors.HexColor("#FFF8F2")    # Couleur Crème pour les cartes/blocs
    COLOR_BG_BLOB = colors.HexColor("#FADADD")       # Zones roses plus prononcées

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
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # .../MDM programme/
    
    # Correcting path to match user file structure from previous context
    # User listed: c:\Users\nblum\LLM_LAB\PROJETS\MDM programme\00_Gestion_Projet\Scripts
    # So assets should be in 00_Gestion_Projet/assets? 
    # Original script: os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
    # Means assets is at 00_Gestion_Projet/assets
    
    SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # .../Scripts
    PROJECT_DIR = os.path.dirname(SCRIPTS_DIR) # .../00_Gestion_Projet

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
