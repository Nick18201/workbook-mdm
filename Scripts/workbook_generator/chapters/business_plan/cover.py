import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from workbook_generator.config import PDFStyle
from workbook_generator.utils import cached_image_reader, cached_simpleSplit as simpleSplit
from workbook_generator.components import (
    draw_dot_grid,
    draw_branding_logo,
    draw_card,
    create_standard_summary_page,
)
from workbook_generator.forms import create_input_field


def create_business_plan_cover(c):
    """
    Page 1 : Couverture officielle haut de gamme pour le livret Mon Business Plan.
    Inclut :
    - Graphisme officiel MDM (Bande latérale, grille, illustration, logo, stamp)
    - Titre & sous-titre
    - Carte d'identité du projet (Nom/Prénom, Nom du projet, Date, Version)
    - Encart de pitch interactif : "Mon projet en une phrase"
    """
    width, height = A4

    # 1. Fond Nude & Dot Grid
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    draw_dot_grid(c, width, height)

    # 2. Bande latérale
    band_width = 1.75 * cm
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.rect(0, 0, band_width, height, fill=1, stroke=0)

    # 3. Logo & Marque Header
    content_x = band_width + 1.2 * cm
    content_w = width - content_x - 1.5 * cm

    logo_x = content_x
    logo_y = height - 2.0 * cm
    draw_branding_logo(c, logo_x, logo_y, size=28)

    # 4. Stamp Rouge officiel
    if os.path.exists(PDFStyle.PATH_STAMP):
        c.saveState()
        c.translate(width - 3.8 * cm, height - 3.0 * cm)
        c.rotate(-12)
        c.drawImage(
            cached_image_reader(PDFStyle.PATH_STAMP),
            -1.8 * cm,
            -1.8 * cm,
            width=3.6 * cm,
            height=3.6 * cm,
            mask="auto",
            preserveAspectRatio=True,
            anchor="c",
        )
        c.restoreState()

    # 5. Titre & Sous-titre
    y_header = height - 4.3 * cm
    c.setFont(PDFStyle.FONT_BRANDING, 26)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(content_x, y_header, "MON BUSINESS PLAN")

    c.setFont(PDFStyle.FONT_TITLE, 14)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(content_x, y_header - 0.75 * cm, "De l'idée au projet viable")

    c.setFont(PDFStyle.FONT_ITALIC, 10)
    c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
    c.drawString(
        content_x,
        y_header - 1.35 * cm,
        "Un carnet de travail pour structurer, tester et faire évoluer mon projet.",
    )

    # 6. Illustration centrale stylisée
    illu_h = 5.0 * cm
    illu_w = 10.5 * cm
    illu_y = y_header - 1.9 * cm - illu_h
    if os.path.exists(PDFStyle.PATH_ILLU_COVER):
        c.drawImage(
            cached_image_reader(PDFStyle.PATH_ILLU_COVER),
            content_x + (content_w - illu_w) / 2,
            illu_y,
            width=illu_w,
            height=illu_h,
            mask="auto",
            preserveAspectRatio=True,
            anchor="sw",
        )

    # 7. Carte d'identification du projet (AcroForm)
    form = c.acroForm
    card_h = 5.2 * cm
    card_y = illu_y - 0.55 * cm - card_h
    draw_card(c, content_x, card_y, content_w, card_h)

    # Titre de la carte
    c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(content_x + 0.6 * cm, card_y + card_h - 0.7 * cm, "INFORMATIONS DU PROJET")

    col_w = (content_w - 1.6 * cm) / 2.0
    col1_x = content_x + 0.6 * cm
    col2_x = col1_x + col_w + 0.4 * cm

    # Ligne 1 : Nom/Prénom & Nom du projet
    c.setFont(PDFStyle.FONT_BODY, 8.5)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(col1_x, card_y + card_h - 1.35 * cm, "PORTEUSE DU PROJET (NOM & PRÉNOM) :")
    c.drawString(col2_x, card_y + card_h - 1.35 * cm, "NOM OU INTITULÉ DU PROJET :")

    create_input_field(
        form,
        "bp_identite_nom_prenom",
        pos=(col1_x, card_y + card_h - 2.25 * cm),
        size=(col_w, 0.75 * cm),
        tooltip="Votre Nom et Prénom",
        fill_color=colors.white,
    )
    create_input_field(
        form,
        "bp_identite_nom_projet",
        pos=(col2_x, card_y + card_h - 2.25 * cm),
        size=(col_w, 0.75 * cm),
        tooltip="Nom de votre entreprise ou projet",
        fill_color=colors.white,
    )

    # Ligne 2 : Date & Version
    c.drawString(col1_x, card_y + card_h - 3.0 * cm, "DATE DE DÉBUT / SESSION :")
    c.drawString(col2_x, card_y + card_h - 3.0 * cm, "VERSION DU DOCUMENT :")

    create_input_field(
        form,
        "bp_identite_date_debut",
        pos=(col1_x, card_y + card_h - 3.90 * cm),
        size=(col_w, 0.75 * cm),
        tooltip="Ex : Septembre 2026",
        fill_color=colors.white,
    )
    create_input_field(
        form,
        "bp_identite_version",
        pos=(col2_x, card_y + card_h - 3.90 * cm),
        size=(col_w, 0.75 * cm),
        tooltip="Ex : Version 1.0 (Brouillon initial)",
        fill_color=colors.white,
    )

    # 8. Carte Pitch : "Mon projet en une phrase"
    pitch_card_h = 4.6 * cm
    pitch_card_y = card_y - pitch_card_h - 0.55 * cm
    draw_card(c, content_x, pitch_card_y, content_w, pitch_card_h)

    c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        content_x + 0.6 * cm,
        pitch_card_y + pitch_card_h - 0.7 * cm,
        "MON PROJET EN UNE PHRASE (PREMIÈRE INTUITION) :",
    )

    c.setFont(PDFStyle.FONT_ITALIC, 8.5)
    c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
    c.drawString(
        content_x + 0.6 * cm,
        pitch_card_y + pitch_card_h - 1.25 * cm,
        "« J'aimerais créer / développer... pour aider... à accomplir... »",
    )

    create_input_field(
        form,
        "bp_identite_pitch_intro",
        pos=(content_x + 0.6 * cm, pitch_card_y + 0.45 * cm),
        size=(content_w - 1.2 * cm, pitch_card_h - 1.9 * cm),
        tooltip="Formulez ici votre intuition première en 1 ou 2 phrases claires",
        multiline=True,
        fill_color=colors.white,
    )

    # Pied de page discret
    c.setFont(PDFStyle.FONT_BODY, 8)
    c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
    c.drawString(
        content_x,
        1.6 * cm,
        "Marge de Manœuvre • Programme d'Accompagnement et d'Émancipation Entrepreneuriale",
    )

    c.showPage()


def create_business_plan_summary(c):
    """
    Page 2 : Sommaire & Méthode de travail en 6 temps.
    Utilise le gabarit officiel create_standard_summary_page.
    """
    points = [
        (
            "1. Fondations & Cible",
            "Clarifier son idée, projeter sa vision à 3 ans et comprendre intimement les personnes à accompagner.",
        ),
        (
            "2. Problème & Offre",
            "Identifier la douleur réelle, poser ses hypothèses, formuler son offre concrète et sa proposition de valeur.",
        ),
        (
            "3. Marché & Positionnement",
            "Étudier l'écosystème, cartographier concurrents et alternatives, benchmark inspirant et pitch singulier.",
        ),
        (
            "4. Modèle Économique & Vente",
            "Monétisation, Business Model Canvas 9 blocs, tarification sous 3 angles et conquête des 10 premiers clients.",
        ),
        (
            "5. Moyens, Finances & Cadre",
            "Plan de communication, ressources requises, statut juridique, budget prévisionnel et seuil de rentabilité.",
        ),
        (
            "6. Expérimentation & Synthèse",
            "Lancement du MVP, interviews terrain, matrice des risques, feuille de route et Executive Summary final.",
        ),
    ]

    create_standard_summary_page(
        c,
        chapter_num_str="BP",
        chapter_title="CONSTRUIRE SON BUSINESS PLAN",
        intro_text="Ce carnet de travail vous accompagne pas à pas pour donner corps à votre projet. "
        "Ici, rien n'est pré-rempli : vous suivez la boucle d'apprentissage en 6 temps (Comprendre → Se questionner → "
        "Chercher sur le terrain → Écrire librement → Décider → Valider vos hypothèses) pour transformer une belle intuition "
        "en une entreprise viable, alignée et durable.",
        points_list=points,
    )
