from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from workbook_generator.utils import cached_simpleSplit as simpleSplit

from workbook_generator.config import PDFStyle
from workbook_generator.components import (
    draw_page_background,
    draw_side_panel,
    draw_title,
    draw_page_decorations,
    create_standard_cover,
    create_standard_summary_page,
    create_standard_recap_page,
    draw_card,
)
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig
from workbook_generator.forms import create_input_field


def get_hex(color):
    if hasattr(color, "hexval"):
        val = color.hexval
        if callable(val):
            val = val()
        if val.startswith("#"):
            return val
        return f"#{val}"
    try:
        rgb = color.rgb()
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
    except Exception:
        return "#2F2EFA"


def draw_paragraph(c, text, pos, width, style):
    p = Paragraph(text, style)
    w, h = p.wrap(width, 1000)
    p.drawOn(c, pos[0], pos[1] - h)
    return h


def create_chap6_cover(c):
    """
    Cover Page for Chapter 6 : Phase d'exploration
    """
    create_standard_cover(c, "CHAPITRE 6 : PHASE D'EXPLORATION")


def create_concept_page(c):
    """
    Page 2 : Concept / Sommaire
    """
    points = [
        ("Sommaire :", ""),
        ("1.", "Récapitulatif de la séance précédente"),
        ("2.", "Votre cartographie personnelle"),
        ("3.", "Le retour de vos proches"),
        ("4.", "Sélectionner 10 métiers à explorer"),
        ("5.", "Fiches métiers - Pistes 'No Limit'"),
        ("6.", "Fiches métiers - Pistes 'Réalistes'"),
        ("7.", "Ressources utiles pour vos recherches"),
    ]
    create_standard_summary_page(
        c,
        "6",
        "CONCEPT",
        "Ce temps d'exploration vise à réunir vos pistes de réflexion professionnelle, à synthétiser vos caractéristiques personnelles (MBTI, valeurs, moteurs), et à les confronter aux suggestions de votre entourage pour ouvrir de nouvelles perspectives de métiers.",
        points,
    )


def create_recap_seance_page(c):
    """
    Page 3 : Récapitulatif de la séance précédente (Mes Valeurs)
    """
    intro_txt = "Prenez un moment pour revenir sur la séance précédente consacrée à l'exploration de vos valeurs. Cet exercice vous aide à consolider vos apprentissages avant d'entamer une nouvelle étape. Répondez spontanément."
    questions = [
        "Quelles sont les 3 valeurs non négociables qui guident vos choix aujourd'hui ?",
        "De quoi avez-vous besoin concrètement (conditions de travail) pour respecter ces valeurs ?",
        "Quelles tensions de valeurs (ex: liberté/sécurité) influencent le plus votre transition ?",
    ]
    create_standard_recap_page(
        c,
        "1. RÉCAPITULATIF (MES VALEURS)",
        intro_txt,
        questions,
    )


def create_cartographie_page(c):
    """
    Page 4 : Votre Cartographie Personnelle
    """
    layout = PageLayout(
        c,
        "Votre Cartographie Personnelle",
        config=LayoutConfig(part_title="2. CARTOGRAPHIE PERSONNELLE"),
    )
    layout.add_text(
        "Prenez le temps de résumer les éléments de réflexion issus de vos séances de bilan.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    y = layout.y_cursor
    x = layout.text_x
    w = layout.target_width

    # 1. Top row: MBTI card taking full width
    card_h = 2.0 * cm

    draw_card(c, x, y - card_h, w, card_h)

    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "TYPE MBTI :")

    create_input_field(
        layout.form,
        "carto_mbti",
        pos=(x + 0.3 * cm, y - 1.7 * cm),
        size=(w - 0.6 * cm, 1.0 * cm),
        multiline=True,
    )

    y = y - card_h - 0.4 * cm

    # 2. Two columns of cards (3 rows)
    col_w = (w - 0.5 * cm) / 2
    col_h = 5.2 * cm

    # Row 1
    # Left: J'aime faire
    draw_card(c, x, y - col_h, col_w, col_h)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "CE QUE J'AIME FAIRE DANS LA VIE :")
    create_input_field(
        layout.form,
        "carto_aime_faire",
        pos=(x + 0.3 * cm, y - col_h + 0.2 * cm),
        size=(col_w - 0.6 * cm, col_h - 0.8 * cm),
        multiline=True,
    )

    # Right: Envies & Objectifs
    draw_card(c, x + col_w + 0.5 * cm, y - col_h, col_w, col_h)
    c.drawString(x + col_w + 0.8 * cm, y - 0.5 * cm, "MES ENVIES ET OBJECTIFS :")
    create_input_field(
        layout.form,
        "carto_envies_objectifs",
        pos=(x + col_w + 0.8 * cm, y - col_h + 0.2 * cm),
        size=(col_w - 0.6 * cm, col_h - 0.8 * cm),
        multiline=True,
    )

    y = y - col_h - 0.4 * cm

    # Row 2
    # Left: Points forts
    draw_card(c, x, y - col_h, col_w, col_h)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "MES POINTS FORTS :")
    create_input_field(
        layout.form,
        "carto_points_forts",
        pos=(x + 0.3 * cm, y - col_h + 0.2 * cm),
        size=(col_w - 0.6 * cm, col_h - 0.8 * cm),
        multiline=True,
    )

    # Right: Valeurs
    draw_card(c, x + col_w + 0.5 * cm, y - col_h, col_w, col_h)
    c.drawString(x + col_w + 0.8 * cm, y - 0.5 * cm, "MES VALEURS :")
    create_input_field(
        layout.form,
        "carto_valeurs",
        pos=(x + col_w + 0.8 * cm, y - col_h + 0.2 * cm),
        size=(col_w - 0.6 * cm, col_h - 0.8 * cm),
        multiline=True,
    )

    y = y - col_h - 0.4 * cm

    # Row 3
    # Left: Besoins
    draw_card(c, x, y - col_h, col_w, col_h)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "MES BESOINS :")
    create_input_field(
        layout.form,
        "carto_besoins",
        pos=(x + 0.3 * cm, y - col_h + 0.2 * cm),
        size=(col_w - 0.6 * cm, col_h - 0.8 * cm),
        multiline=True,
    )

    # Right: Sources de stress
    draw_card(c, x + col_w + 0.5 * cm, y - col_h, col_w, col_h)
    c.drawString(x + col_w + 0.8 * cm, y - 0.5 * cm, "MES SOURCES DE STRESS :")
    create_input_field(
        layout.form,
        "carto_stress",
        pos=(x + col_w + 0.8 * cm, y - col_h + 0.2 * cm),
        size=(col_w - 0.6 * cm, col_h - 0.8 * cm),
        multiline=True,
    )

    layout.render()


def create_retours_proches_page(c):
    """
    Page 5 : Le retour de mes proches
    """
    layout = PageLayout(
        c,
        "Le retour de mes proches",
        config=LayoutConfig(part_title="3. RETOUR DE MES PROCHES"),
    )
    layout.add_text(
        "Présentez votre cartographie à au moins 3 personnes de votre entourage (sans parler de vos pistes) et interrogez-les sur les métiers et secteurs auxquels ils pensent.",
        config=TextConfig(spacing_after=0.3 * cm),
    )
    layout.add_question_block(
        "Propositions de secteurs et métiers suggérés par mes proches :",
        "proches_suggestions",
        config=QuestionConfig(box_height=4.8 * cm),
    )
    layout.add_question_block(
        "Qu'est-ce que je pense de ces différentes propositions ?",
        "proches_avis",
        config=QuestionConfig(box_height=3.6 * cm),
    )
    layout.add_question_block(
        "Comment j'ai vécu cet exercice ?",
        "proches_vecu",
        config=QuestionConfig(box_height=3.6 * cm),
    )
    layout.render()


def create_pistes_intro_page(c):
    """
    Page 6 : Les Premières Pistes de Métiers (Index / Introduction)
    """
    layout = PageLayout(
        c,
        "Premières pistes de métiers",
        config=LayoutConfig(part_title="4. PISTES DE MÉTIERS"),
    )
    layout.add_text(
        "Pour avancer, explorez 10 métiers répartis en deux catégories : 5 pistes 'no limit' (sans contraintes) et 5 pistes 'réalistes' (faisables concrètement).",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    y = layout.y_cursor
    x = layout.text_x
    w = layout.target_width

    card_w = (w - 0.6 * cm) / 2
    card_h = 13.0 * cm

    # Draw cards
    draw_card(c, x, y - card_h, card_w, card_h)
    draw_card(c, x + card_w + 0.6 * cm, y - card_h, card_w, card_h)

    # Headers inside cards
    c.setFont(PDFStyle.FONT_SUBTITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(x + 0.4 * cm, y - 0.6 * cm, "5 MÉTIERS 'NO LIMIT'")
    c.drawString(x + card_w + 1.0 * cm, y - 0.6 * cm, "5 MÉTIERS 'RÉALISTES'")

    # Subtitles
    c.setFont(PDFStyle.FONT_ITALIC, 8)
    c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
    c.drawString(x + 0.4 * cm, y - 1.0 * cm, "Sans tenir compte des contraintes")
    c.drawString(x + card_w + 1.0 * cm, y - 1.0 * cm, "Concrètement faisables aujourd'hui")

    # Render 5 text inputs in each
    input_h = 1.2 * cm
    gap = 0.5 * cm
    start_y_inputs = y - 2.4 * cm

    for i in range(5):
        curr_y = start_y_inputs - i * (input_h + gap)

        # Left card items
        c.setFont(PDFStyle.FONT_BODY, 9)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(x + 0.4 * cm, curr_y + 0.4 * cm, f"{i+1}.")
        create_input_field(
            layout.form,
            f"index_piste_nl_{i+1}",
            pos=(x + 0.9 * cm, curr_y),
            size=(card_w - 1.3 * cm, input_h),
            fill_color=colors.white
        )

        # Right card items
        c.drawString(x + card_w + 1.0 * cm, curr_y + 0.4 * cm, f"{i+1}.")
        create_input_field(
            layout.form,
            f"index_piste_r_{i+1}",
            pos=(x + card_w + 1.5 * cm, curr_y),
            size=(card_w - 1.9 * cm, input_h),
            fill_color=colors.white
        )

    layout.render()


def _draw_fiche_block(layout, c, num, prefix, y, w):
    """
    Renders a structured fiche block containing field inputs.
    Returns the final Y cursor coordinate.
    """
    c.setFont(PDFStyle.FONT_SUBTITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(layout.text_x, y - 0.4 * cm, f"PISTE {num} :")

    # Input field for Intitulé du métier
    create_input_field(
        layout.form,
        f"{prefix}_intitule_{num}",
        pos=(layout.text_x + 2.0 * cm, y - 0.5 * cm),
        size=(w - 2.0 * cm, 0.6 * cm),
        fill_color=colors.white
    )

    y = y - 0.8 * cm

    # Draw two side-by-side cards for Pourquoi and Missions/Compétences
    col_w = (w - 0.4 * cm) / 2
    card_h = 4.5 * cm

    # Card 1: Pourquoi
    draw_card(c, layout.text_x, y - card_h, col_w, card_h)
    c.setFont(PDFStyle.FONT_BODY, 8)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(layout.text_x + 0.2 * cm, y - 0.35 * cm, "Pourquoi ce métier vous attire :")
    create_input_field(
        layout.form,
        f"{prefix}_pourquoi_{num}",
        pos=(layout.text_x + 0.2 * cm, y - 4.3 * cm),
        size=(col_w - 0.4 * cm, 3.8 * cm),
        multiline=True,
        fill_color=colors.white
    )

    # Card 2: Missions & Compétences
    draw_card(c, layout.text_x + col_w + 0.4 * cm, y - card_h, col_w, card_h)
    c.drawString(layout.text_x + col_w + 0.6 * cm, y - 0.35 * cm, "Missions & Compétences utiles :")
    create_input_field(
        layout.form,
        f"{prefix}_missions_{num}",
        pos=(layout.text_x + col_w + 0.6 * cm, y - 4.3 * cm),
        size=(col_w - 0.4 * cm, 3.8 * cm),
        multiline=True,
        fill_color=colors.white
    )

    return y - card_h


def create_pistes_no_limit_1_page(c):
    """
    Page 7 : Pistes No Limit 1, 2, 3
    """
    layout = PageLayout(
        c,
        "Fiches Métiers : Pistes 'No Limit' (1/2)",
        config=LayoutConfig(part_title="4. PISTES DE MÉTIERS - NO LIMIT"),
    )
    layout.add_text(
        "Sélectionnez des pistes sans prendre en compte les contraintes matérielles ou personnelles.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    y = layout.y_cursor
    w = layout.target_width

    y = _draw_fiche_block(layout, c, 1, "nl", y, w)
    y = y - 0.4 * cm
    y = _draw_fiche_block(layout, c, 2, "nl", y, w)
    y = y - 0.4 * cm
    y = _draw_fiche_block(layout, c, 3, "nl", y, w)

    layout.render()


def create_pistes_no_limit_2_page(c):
    """
    Page 8 : Pistes No Limit 4, 5
    """
    layout = PageLayout(
        c,
        "Fiches Métiers : Pistes 'No Limit' (2/2)",
        config=LayoutConfig(part_title="4. PISTES DE MÉTIERS - NO LIMIT"),
    )
    layout.add_text(
        "Explorez les deux dernières pistes de la catégorie 'No Limit'.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    y = layout.y_cursor
    w = layout.target_width

    y = _draw_fiche_block(layout, c, 4, "nl", y, w)
    y = y - 0.5 * cm
    y = _draw_fiche_block(layout, c, 5, "nl", y, w)

    layout.render()


def create_pistes_realistes_1_page(c):
    """
    Page 9 : Pistes Réalistes 1, 2, 3
    """
    layout = PageLayout(
        c,
        "Fiches Métiers : Pistes 'Réalistes' (1/2)",
        config=LayoutConfig(part_title="4. PISTES DE MÉTIERS - RÉALISTES"),
    )
    layout.add_text(
        "Sélectionnez des pistes qui vous semblent plus concrètement faisables dans votre situation.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    y = layout.y_cursor
    w = layout.target_width

    y = _draw_fiche_block(layout, c, 1, "r", y, w)
    y = y - 0.4 * cm
    y = _draw_fiche_block(layout, c, 2, "r", y, w)
    y = y - 0.4 * cm
    y = _draw_fiche_block(layout, c, 3, "r", y, w)

    layout.render()


def create_pistes_realistes_2_page(c):
    """
    Page 10 : Pistes Réalistes 4, 5
    """
    layout = PageLayout(
        c,
        "Fiches Métiers : Pistes 'Réalistes' (2/2)",
        config=LayoutConfig(part_title="4. PISTES DE MÉTIERS - RÉALISTES"),
    )
    layout.add_text(
        "Explorez les deux dernières pistes de la catégorie 'Réalistes'.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    y = layout.y_cursor
    w = layout.target_width

    y = _draw_fiche_block(layout, c, 4, "r", y, w)
    y = y - 0.5 * cm
    y = _draw_fiche_block(layout, c, 5, "r", y, w)

    layout.render()


def create_ressources_page(c):
    """
    Page 11 : Ressources utiles pour vos recherches
    """
    layout = PageLayout(
        c,
        "Ressources utiles pour vos recherches",
        config=LayoutConfig(part_title="5. RESSOURCES UTILES"),
    )
    layout.add_text(
        "Voici quelques ressources recommandées pour explorer les métiers et enrichir vos fiches pratiques.",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    y = layout.y_cursor
    x = layout.text_x
    w = layout.target_width

    # Link Style
    style = ParagraphStyle(
        "RessourcesParagraphStyle",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9,
        leading=13,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
    )
    link_color = get_hex(PDFStyle.COLOR_TEXT_MAIN)

    # Card 1: Témoignages & Podcasts
    h1 = 2.8 * cm
    draw_card(c, x, y - h1, w, h1)
    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "DÉCOUVRIR LE QUOTIDIEN DES MÉTIERS (AUDIOS / VIDÉOS)")
    
    t1 = f'• <a href="https://podcast.ausha.co/into-the-job"><font color="{link_color}"><b><u>Into the Job</u></b></font></a> (podcast) : Témoignages concrets sur le quotidien professionnel.'
    draw_paragraph(c, t1, (x + 0.3 * cm, y - 1.2 * cm), w - 0.6 * cm, style)
    
    t2 = f'• <a href="https://www.youtube.com/c/Maintenantjaimelelundi/playlists"><font color="{link_color}"><b><u>Maintenant j\'aime le lundi</u></b></font></a> (YouTube) : Découvrir des parcours, des reconversions et des métiers.'
    draw_paragraph(c, t2, (x + 0.3 * cm, y - 2.0 * cm), w - 0.6 * cm, style)

    y = y - h1 - 0.4 * cm

    # Card 2: Fiches Métiers
    h2 = 5.2 * cm
    draw_card(c, x, y - h2, w, h2)
    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "CONSULTER DES FICHES MÉTIERS COMPLÈTES")
    
    t3 = f'• <a href="https://www.apec.fr/tous-nos-metiers.html"><font color="{link_color}"><b><u>APEC</u></b></font></a> : Utile pour les métiers cadres, les fonctions supports et le management.'
    draw_paragraph(c, t3, (x + 0.3 * cm, y - 1.1 * cm), w - 0.6 * cm, style)
    
    t4 = f'• <a href="https://www.cadremploi.fr/editorial/conseils/fiches-metiers.html"><font color="{link_color}"><b><u>Cadremploi</u></b></font></a> : Vision synthétique des missions, compétences et salaires.'
    draw_paragraph(c, t4, (x + 0.3 * cm, y - 1.9 * cm), w - 0.6 * cm, style)
    
    t5 = f'• <a href="https://www.onisep.fr/decouvrir-les-metiers"><font color="{link_color}"><b><u>ONISEP</u></b></font></a> : Informations sur les formations, les secteurs et les débouchés.'
    draw_paragraph(c, t5, (x + 0.3 * cm, y - 2.7 * cm), w - 0.6 * cm, style)
    
    t6 = f'• <a href="https://www.cidj.com/metiers/metiers-par-centres-d-interets"><font color="{link_color}"><b><u>CIDJ</u></b></font></a> : Exploration de listes de métiers classées par centres d\'intérêt.'
    draw_paragraph(c, t6, (x + 0.3 * cm, y - 3.5 * cm), w - 0.6 * cm, style)
    
    t7 = f'• <a href="https://candidat.pole-emploi.fr/metierscope/centres-interet"><font color="{link_color}"><b><u>MétierScope (Pôle Emploi)</u></b></font></a> : Recherche de métiers par goût et état du marché.'
    draw_paragraph(c, t7, (x + 0.3 * cm, y - 4.3 * cm), w - 0.6 * cm, style)

    y = y - h2 - 0.4 * cm

    # Card 3: Notion Link
    h3 = 1.8 * cm
    draw_card(c, x, y - h3, w, h3)
    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "VOTRE SITE DE TRANSITION Notion")
    
    t8 = f'• Retrouvez toutes vos ressources et guides pratiques sur : <a href="https://www.notion.so/Vos-ressources-aca96b6474d04acd9eaafa92523df7a6"><font color="{link_color}"><b><u>Vos ressources Notion</u></b></font></a>.'
    draw_paragraph(c, t8, (x + 0.3 * cm, y - 1.1 * cm), w - 0.6 * cm, style)
    layout.render()
