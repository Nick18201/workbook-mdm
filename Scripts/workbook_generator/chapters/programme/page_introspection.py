from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.components import draw_title, TitleStyle
from .common import (
    setup_workbook_programme_page,
    draw_workbook_highlight_box,
    get_workbook_styles,
)


def create_programme_page_2(c):
    """Page 2 : 1. Présentation de la Méthode & Étape A (Introspection)."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="MÉTHODE & DÉROULÉ DU BILAN"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE H1 : 1. PRÉSENTATION DE LA MÉTHODE & DÉROULÉ DU BILAN
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "1. Présentation de la Méthode & Déroulé",
        pos=(text_x, y_cursor),
        available_width=target_width,
        style=TitleStyle(size=18, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    y_cursor -= 0.30 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Un cheminement en 3 étapes articulé aux phases légales du Bilan de Compétences",
    )
    y_cursor -= 0.75 * cm

    # -------------------------------------------------------------------------
    # 2. LES 3 PHASES RÉGLEMENTAIRES (CADRE LÉGAL)
    # -------------------------------------------------------------------------
    txt_phases_legal = (
        "Chaque bilan de compétences respecte les <b>3 phases réglementaires du Code du travail</b> : "
        "la <b>Phase Préliminaire</b> (analyse de la demande, définition du déroulement et des outils), "
        "la <b>Phase d’Investigation</b> (exploration approfondie du profil, des compétences et confrontation des scénarios) "
        "et la <b>Phase de Conclusion</b> (co-construction de la synthèse écrite et du plan d'action)."
    )
    style_legal = ParagraphStyle(
        "LegalP2",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.5,
        leading=14.4,
        textColor=colors.HexColor("#222222"),
    )
    p_legal = Paragraph(txt_phases_legal, style_legal)
    p_legal.wrap(target_width, 4 * cm)
    p_legal.drawOn(c, text_x, y_cursor - p_legal.height)
    y_cursor -= p_legal.height + 0.85 * cm

    # -------------------------------------------------------------------------
    # 3. SECTION ÉTAPE A : INTROSPECTION (UN TRAVAIL EN PROFONDEUR)
    # -------------------------------------------------------------------------
    c.setFont(PDFStyle.FONT_TITLE, 13)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x, y_cursor, "Étape A : Introspection (Un travail en profondeur)"
    )
    y_cursor -= 0.70 * cm

    introspection_items = [
        (
            "Héritages & Identité",
            "L'enjeu est de conscientiser les injonctions familiales, croyances et modèles qui ont dicté vos choix jusqu'ici. "
            "En faisant le tri dans ce bagage pour ne garder que les forces utiles, le but est de vous libérer des attentes extérieures "
            "pour reprendre le contrôle de votre trajectoire sans culpabilité.",
        ),
        (
            "Analyse du parcours et fil rouge",
            "L'objectif est de dépasser la simple chronologie de votre CV pour comprendre la logique profonde de vos bifurcations. "
            "En identifiant les compétences clés que vous avez mobilisées, ce que vous voulez conserver et ce que vous refusez désormais de revivre, "
            "vous transformez vos expériences passées en un tremplin cohérent.",
        ),
        (
            "Moteurs & Motivation",
            "L'enjeu est d'identifier ce qui vous anime réellement au-delà de la compétence technique : vos valeurs fondamentales, "
            "vos leviers de motivation et vos conditions d'épanouissement. Cette clarté sert de boussole pour éviter les erreurs d'aiguillage "
            "et choisir des environnements qui nourrissent durablement votre énergie.",
        ),
    ]

    style_intro_item = ParagraphStyle(
        "IntroItemP2",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.2,
        leading=13.8,
        textColor=colors.HexColor("#222222"),
    )

    for titre_item, desc_item in introspection_items:
        txt_bullet = (
            f"<b><font color='#2F2EFA'>· {titre_item} :</font></b> {desc_item}"
        )
        p_item = Paragraph(txt_bullet, style_intro_item)
        p_item.wrap(target_width, 4 * cm)
        p_item.drawOn(c, text_x, y_cursor - p_item.height)
        y_cursor -= p_item.height + 0.70 * cm

    # -------------------------------------------------------------------------
    # 4. ENCADRÉ NOTRE SPÉCIFICITÉ SUR CETTE PHASE
    # -------------------------------------------------------------------------
    y_cursor -= 0.30 * cm
    callout_h = 1.95 * cm
    spec_txt = (
        "Le bilan est construit avec une <b>orientation en psychologie du travail</b>. "
        "C'est ce qui nous pousse à creuser cette partie vraiment en profondeur pour garantir, "
        "par la suite, la construction d'un <b>projet solide, sain et de qualité</b>."
    )
    draw_workbook_highlight_box(
        c,
        text_x,
        y_cursor - callout_h,
        target_width,
        callout_h,
        prefix="👉 NOTRE SPÉCIFICITÉ SUR CETTE PHASE :",
        text=spec_txt,
        accent_color=PDFStyle.COLOR_ACCENT_RED,
        bg_color=PDFStyle.COLOR_BG_NUDE,
        font_size=9.2,
        leading=13.2,
    )
    y_cursor -= callout_h + 0.65 * cm

    # -------------------------------------------------------------------------
    # 5. VOLUME HORAIRE
    # -------------------------------------------------------------------------
    c.setFont(PDFStyle.FONT_ITALIC, 9.0)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Suivant le bilan choisi et les besoins : 4h à 7h d'entretiens passés sur cette phase.",
    )

    c.showPage()
