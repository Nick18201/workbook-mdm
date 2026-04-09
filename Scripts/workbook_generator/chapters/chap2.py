from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from ..config import PDFStyle
from ..components import (
    draw_page_background,
    draw_side_panel,
    draw_title,
    create_standard_cover,
    draw_page_decorations,
    create_standard_summary_page,
    create_standard_recap_page,
)
from ..forms import create_input_field
from ..utils import cached_simpleSplit as simpleSplit


def create_chap2_cover(c):
    """
    Cover Page for Chapter 2: Mes Racines.
    """
    create_standard_cover(c, "CHAPITRE 2 : MON PARCOURS")


def create_concept_page(c):
    """
    Page 2: Chapter Cover - 2. Concept (Missing originally)
    Blue background, large watermark.
    """
    points = [
        ("Sommaire :", ""),
        ("1.", "Récapitulatif de la séance précédente"),
        ("2.", "Analyse du Parcours (Expériences)"),
        ("3.", "Moteurs Fondamentaux & Schémas"),
        ("4.", "Ma Ligne de Vie (Montagnes Russes)"),
        ("5.", "Mes Compétences de Vie"),
        ("6.", "Mon Arbre de Vie"),
        ("Bonus.", "Interview Inspirante"),
    ]
    create_standard_summary_page(c, "2", "CONCEPT", "", points)


def create_recap_seance_page(c):
    """
    Page de récapitulatif de la séance précédente.
    """
    intro_txt = "Prenez un moment pour revenir sur nos précédents échanges. Cet exercice vous aide à consolider vos apprentissages avant d'entamer une nouvelle étape. Répondez spontanément."
    questions = [
        "Qu’est-ce que cette séance vous a permis de comprendre de plus sur vous-même ?",
        "Quels héritages ou messages reçus influencent encore vos choix professionnels aujourd’hui ?",
        "Parmi ces héritages, qu’est-ce que vous avez envie de garder, et qu’est-ce que vous avez envie de faire évoluer ?",
        "En quoi cela éclaire différemment la suite de votre bilan et vos pistes pour la suite ?",
    ]
    create_standard_recap_page(c, "1. RÉCAPITULATIF", intro_txt, questions)


def create_timeline_page(c):
    """
    Page: Ma Ligne de Vie.
    Vertical Layout.
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(
        c, "Ma Ligne de Vie (Les Montagnes Russes)", pos=(text_x, text_top)
    )

    c.setFont(PDFStyle.FONT_BODY, 10)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    desc_text = "Tracez la courbe de votre vie (pro/perso). Identifiez les moments forts (les sommets) et difficiles (les vallées). L'objectif est de comprendre ce qui vous ressource et vos apprentissages lors d'épreuves."
    from ..utils import cached_simpleSplit as simpleSplit

    text_y = new_y - 0.2 * cm
    for line in simpleSplit(
        desc_text, PDFStyle.FONT_BODY, 10, width - text_x - 1.0 * cm
    ):
        c.drawString(text_x, text_y, line)
        text_y -= 0.4 * cm

    # Main vertical line
    center_x = card_margin + (width - card_margin) / 2.0
    margin_top = text_y - 0.5 * cm
    margin_bottom = 3 * cm
    c.setStrokeColor(PDFStyle.COLOR_TEXT_SECONDARY)
    c.setLineWidth(2)
    c.line(center_x, margin_top, center_x, margin_bottom)

    # Arrow head at top
    c.line(center_x, margin_top, center_x - 0.2 * cm, margin_top - 0.5 * cm)
    c.line(center_x, margin_top, center_x + 0.2 * cm, margin_top - 0.5 * cm)

    # Nodes (Alternating)
    # 3 Sommets (Left), 2 Vallées (Right)

    form = c.acroForm

    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, margin_top + 0.5 * cm, "Les Sommets (Positifs)")

    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawRightString(
        width - 1.5 * cm, margin_top + 0.5 * cm, "Les Vallées (Apprentissages)"
    )

    positions = [
        ("Sommet 1", "left", margin_top - 2.5 * cm),
        ("Vallée 1", "right", margin_top - 6.0 * cm),
        ("Sommet 2", "left", margin_top - 9.5 * cm),
        ("Vallée 2", "right", margin_top - 13.0 * cm),
        ("Sommet 3", "left", margin_top - 16.5 * cm),
    ]

    for label, side, y_pos in positions:
        # Dot on line
        c.setFillColor(PDFStyle.COLOR_WHITE)
        c.setStrokeColor(PDFStyle.COLOR_TEXT_MAIN)
        c.circle(center_x, y_pos, 0.15 * cm, fill=1, stroke=1)

        # Connector
        c.setStrokeColor(PDFStyle.COLOR_TEXT_SECONDARY)
        c.setDash([2, 2])
        if side == "left":
            x_box = text_x
            c.line(center_x, y_pos, x_box + 7 * cm, y_pos)
        else:
            x_box = center_x + 1 * cm
            c.line(center_x, y_pos, x_box, y_pos)
        c.setDash([])

        # Input Box
        # Title placeholder
        c.setFont(PDFStyle.FONT_BODY, 10)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(x_box, y_pos + 1.2 * cm, f"{label} (Date + Quoi) :")

        create_input_field(
            form,
            f'timeline_{label.replace(" ", "_")}_titre',
            pos=(x_box, y_pos + 0.6 * cm),
            size=(7 * cm, 0.5 * cm),
        )

        c.drawString(
            x_box,
            y_pos + 0.2 * cm,
            "Ce que j'en retiens :" if "Vallée" in label else "Ce que j'ai aimé :",
        )
        create_input_field(
            form,
            f'timeline_{label.replace(" ", "_")}_desc',
            pos=(x_box, y_pos - 1.5 * cm),
            size=(7 * cm, 1.6 * cm),
            multiline=True,
        )

    draw_page_decorations(
        c, width, height, part_title="2. MON PARCOURS", x_offset=card_margin
    )
    c.showPage()


def create_skills_transfer_page(c):
    """
    Page: Mes Compétences de Vie.
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, "Mes Compétences de Vie", pos=(text_x, text_top))

    c.setFont(PDFStyle.FONT_BODY, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(
        text_x,
        new_y - 0.2 * cm,
        "Transformons votre vécu en capital. Je ne pars pas de zéro, je pars de mon expérience.",
    )

    # Explications supplémentaires
    c.setFont(PDFStyle.FONT_BODY, 9)
    c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)

    desc_lines = [
        "Cette page vise à traduire vos expériences personnelles ou professionnelles en compétences concrètes.",
        "Une expérience vécue (ex: organiser un événement familial) cache souvent des talents (ex: planification, gestion du stress).",
        "Ne sous-estimez aucune expérience. Même la gestion du quotidien développe des compétences clés.",
    ]
    y_desc = new_y - 0.8 * cm
    from ..utils import cached_simpleSplit as simpleSplit

    target_width = width - text_x - 1.0 * cm
    for line in desc_lines:
        for s in simpleSplit(line, PDFStyle.FONT_BODY, 9, target_width):
            c.drawString(text_x, y_desc, s)
            y_desc -= 0.4 * cm

    # Table Headers
    y_start = y_desc - 0.6 * cm
    center_x = text_x + target_width / 2.0
    col_width = (target_width / 2.0) - 1.0 * cm
    col1_x = text_x
    col2_x = center_x + 0.5 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(col1_x, y_start, "L'Expérience Vécue")
    c.drawString(col1_x, y_start - 0.5 * cm, "(Ex: Divorce, Voyage, Asso...)")

    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(col2_x, y_start, "Le Talent Caché / Compétence")
    c.drawString(col2_x, y_start - 0.5 * cm, "(Ex: Négociation, Logistique...)")

    form = c.acroForm

    # Rows
    y_row = y_start - 3.8 * cm
    row_height = 3.2 * cm

    themes = [
        "1. Vie familiale & personnelle (Ex: organisation, aidant, parents...)",
        "2. Défis & épreuves (Ex: santé, reconversion, chômage...)",
        "3. Engagements & loisirs (Ex: sport, association, art, bénévolat...)",
        "4. Voyages & découvertes (Ex: expatriation, année sabbatique...)",
        "5. Autre expérience marquante (Choix libre)",
    ]

    for i, theme in enumerate(themes):
        # Theme label
        c.setFont(PDFStyle.FONT_BODY, 9)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(col1_x, y_row + row_height - 0.5 * cm, theme)

        # Arrow between columns
        cx_arrow = center_x
        c.setStrokeColor(PDFStyle.COLOR_TEXT_SECONDARY)
        c.setLineWidth(1)
        arrow_y = y_row + (row_height - 1.0 * cm) / 2
        c.line(cx_arrow - 0.4 * cm, arrow_y, cx_arrow + 0.4 * cm, arrow_y)
        c.line(cx_arrow + 0.4 * cm, arrow_y, cx_arrow + 0.1 * cm, arrow_y + 0.1 * cm)
        c.line(cx_arrow + 0.4 * cm, arrow_y, cx_arrow + 0.1 * cm, arrow_y - 0.1 * cm)

        # Left Input
        create_input_field(
            form,
            f"skill_exp_{i+1}",
            pos=(col1_x, y_row),
            size=(col_width, row_height - 0.9 * cm),
            multiline=True,
            tooltip=theme,
        )

        # Right Input
        create_input_field(
            form,
            f"skill_talent_{i+1}",
            pos=(col2_x, y_row),
            size=(col_width, row_height - 0.9 * cm),
            multiline=True,
            tooltip=f"Talent {i+1}",
        )

        y_row -= row_height

    draw_page_decorations(
        c, width, height, part_title="2. MON PARCOURS", x_offset=card_margin
    )
    c.showPage()


def create_analysis_parcours_pages(c):
    """
    Pages: Analyse du Parcours & des Moteurs.
    1 & 2. Blocs d'Expériences (Pro, Etudes, Perso)
    3. Bilan & Moteurs (Schémas et Moteurs)
    """
    width, height = A4
    form = c.acroForm
    card_margin = 2 * cm

    # --- PAGES 1 & 2: BLOCS D'EXPERIENCES ---
    for page_num in range(2):
        draw_page_background(c, width, height)
        draw_side_panel(c, card_margin, width, height)

        text_x = card_margin + 1.0 * cm
        text_top = height - 4.0 * cm
        new_y = draw_title(c, "Analyse du Parcours", pos=(text_x, text_top))

        c.setFont(PDFStyle.FONT_BODY, 10)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        if page_num == 0:
            intro_txt = "Détaillez chaque expérience significative (emploi, stage, bénévolat). Cet inventaire vous servira de socle pour repérer vos réussites et analyser ce que vous souhaitez retrouver ou éviter à l'avenir."
            text_y = new_y - 0.2 * cm
            from ..utils import cached_simpleSplit as simpleSplit

            for line in simpleSplit(
                intro_txt, PDFStyle.FONT_BODY, 10, width - text_x - 1.0 * cm
            ):
                c.drawString(text_x, text_y, line)
                text_y -= 0.4 * cm
            y_cursor = text_y - 0.5 * cm
        else:
            y_cursor = new_y - 0.5 * cm

        for block_idx in range(2):
            global_exp_idx = page_num * 2 + block_idx + 1

            # Draw block Background/Border
            c.setStrokeColor(
                PDFStyle.COLOR_ACCENT_BLUE
                if block_idx == 0
                else PDFStyle.COLOR_ACCENT_RED
            )
            c.setLineWidth(1)

            box_x = text_x
            box_w = width - text_x - 1.0 * cm
            c.roundRect(box_x, y_cursor - 9.5 * cm, box_w, 10 * cm, 0.5 * cm)

            c.setFont(PDFStyle.FONT_SUBTITLE, 11)
            c.setFillColor(
                PDFStyle.COLOR_ACCENT_BLUE
                if block_idx == 0
                else PDFStyle.COLOR_ACCENT_RED
            )
            c.drawString(box_x + 0.5 * cm, y_cursor, f"Expérience {global_exp_idx}")

            # Inputs
            # Ligne 1: Titre / Année
            c.setFont(PDFStyle.FONT_BODY, 9)
            c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            c.drawString(
                box_x + 0.5 * cm,
                y_cursor - 0.8 * cm,
                "Titre de poste et entreprise (ou Sujet d'étude) :",
            )
            create_input_field(
                form,
                f"exp_{global_exp_idx}_titre",
                pos=(box_x + 0.5 * cm, y_cursor - 1.7 * cm),
                size=(10 * cm, 0.7 * cm),
            )

            c.drawString(box_x + 11 * cm, y_cursor - 0.8 * cm, "Année(s) :")
            create_input_field(
                form,
                f"exp_{global_exp_idx}_annee",
                pos=(box_x + 11 * cm, y_cursor - 1.7 * cm),
                size=(box_w - 11.5 * cm, 0.7 * cm),
            )

            # Ligne 2: Missions & Compétences (2 columns)
            col_w = (box_w - 1.5 * cm) / 2
            col1_x = box_x + 0.5 * cm
            col2_x = box_x + 1 * cm + col_w

            c.drawString(
                col1_x, y_cursor - 2.5 * cm, "Fiche de poste / Missions principales :"
            )
            create_input_field(
                form,
                f"exp_{global_exp_idx}_missions",
                pos=(col1_x, y_cursor - 4.8 * cm),
                size=(col_w, 2.1 * cm),
                multiline=True,
            )

            c.drawString(
                col2_x,
                y_cursor - 2.5 * cm,
                "Compétences développées (Tech / Softskills) :",
            )
            create_input_field(
                form,
                f"exp_{global_exp_idx}_competences",
                pos=(col2_x, y_cursor - 4.8 * cm),
                size=(col_w, 2.1 * cm),
                multiline=True,
            )

            # Ligne 3: Aimé / Pas Aimé (2 columns)
            c.drawString(col1_x, y_cursor - 5.6 * cm, "Ce que j'ai aimé :")
            create_input_field(
                form,
                f"exp_{global_exp_idx}_aime",
                pos=(col1_x, y_cursor - 7.9 * cm),
                size=(col_w, 2.1 * cm),
                multiline=True,
            )

            c.drawString(col2_x, y_cursor - 5.6 * cm, "Ce que je n'ai pas aimé :")
            create_input_field(
                form,
                f"exp_{global_exp_idx}_paime",
                pos=(col2_x, y_cursor - 7.9 * cm),
                size=(col_w, 2.1 * cm),
                multiline=True,
            )

            y_cursor -= 10.5 * cm

        draw_page_decorations(
            c, width, height, part_title="2. MON PARCOURS", x_offset=card_margin
        )
        c.showPage()

    # --- PAGE 3: BILAN & MOTEURS ---
    draw_page_background(c, width, height)
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, "Analyse Transversale & Moteurs", pos=(text_x, text_top))

    # Introduction Text to the Approach
    text_y = new_y - 0.2 * cm
    c.setFont(PDFStyle.FONT_BODY, 10)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)

    intro_lines = [
        "Maintenant que nous avons balayé vos différentes expériences, prenons de la hauteur.",
        "L'objectif est de dépasser la chronologie pour comprendre votre logique interne.",
        "",
        "Cette analyse sert à identifier votre 'fil rouge' :",
    ]

    target_width = width - text_x - 1.0 * cm

    for line in intro_lines:
        c.drawString(text_x, text_y, line)
        text_y -= 0.5 * cm

    y_cursor = text_y - 0.5 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(text_x, y_cursor, "1. Mes Schémas (Mon Fil Rouge)")

    y_cursor -= 0.8 * cm
    c.setFont(PDFStyle.FONT_BODY, 10)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)

    schema_question = "En regardant votre parcours global, quelles répétitions ou schémas observez-vous ?"
    schema_ex = "(Ex: Choisir souvent sous la pression, rechercher l'expertise, aller au clash au bout d'un an, etc.)"

    # We use simpleSplit to respect borders
    from ..utils import cached_simpleSplit as simpleSplit

    for s in simpleSplit(schema_question, PDFStyle.FONT_BODY, 10, target_width):
        c.drawString(text_x, y_cursor, s)
        y_cursor -= 0.4 * cm
    for s in simpleSplit(schema_ex, PDFStyle.FONT_BODY, 10, target_width):
        c.drawString(text_x, y_cursor, s)
        y_cursor -= 0.4 * cm

    y_cursor -= 3.7 * cm
    create_input_field(
        form,
        "bilan_schemas",
        pos=(text_x, y_cursor),
        size=(target_width, 3.5 * cm),
        multiline=True,
    )

    y_cursor -= 1.5 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, y_cursor, "2. Mes Moteurs Fondamentaux")
    y_cursor -= 0.6 * cm
    c.setFont(PDFStyle.FONT_ITALIC, 10)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(
        text_x, y_cursor, "Qu'est-ce qui vous fait intimement avancer durablement ?"
    )
    y_cursor -= 0.5 * cm

    moteurs_ex = "(Ex: Indépendance, Sécurité financière, Apprendre, Altruisme, Compétition, Rôle d'expert...)"
    for s in simpleSplit(moteurs_ex, PDFStyle.FONT_ITALIC, 10, target_width):
        c.drawString(text_x, y_cursor, s)
        y_cursor -= 0.4 * cm

    y_cursor -= 1.2 * cm
    for i in range(1, 6):
        c.drawString(text_x, y_cursor + 0.2 * cm, f"{i}.")
        create_input_field(
            form,
            f"moteur_{i}",
            pos=(text_x + 0.6 * cm, y_cursor),
            size=(target_width - 0.6 * cm, 0.7 * cm),
        )
        y_cursor -= 1.0 * cm

    draw_page_decorations(
        c, width, height, part_title="2. MON PARCOURS", x_offset=card_margin
    )
    c.showPage()


def create_tree_of_life_page(c):
    """
    New Page: L'Arbre de Vie.
    Distinct from Genogramme.
    Structure: Racines, Sol, Tronc, Branches, Feuilles, Fruits.
    Improved UI/UX with organic drawing and full explanatory text.
    v3: Layout Fixes preventing overlaps.
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, "Mon Arbre de Vie", pos=(text_x, text_top))

    # --- 1. INTRO & OBJECTIF ---
    y_cursor = new_y - 0.2 * cm

    # Objectif styling
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setFont(PDFStyle.FONT_SUBTITLE, 11)
    c.drawString(text_x, y_cursor, "Objectif :")

    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.setFont(PDFStyle.FONT_BODY, 10)
    obj_text = (
        "Restaurer votre identité narrative. Cet exercice permet de voir que les épreuves (trauma, échec...) "
        "ne sont que des cicatrices sur l'écorce, et non l'arbre tout entier. "
        "Renseignez : racines (origine), sol (besoins), tronc (forces), branches (projets), feuilles (soutiens), fruits (réussites)."
    )
    # Simple wrapping
    text_obj_x = text_x + 2.0 * cm
    text_obj = c.beginText(text_obj_x, y_cursor)
    text_obj.setFont(PDFStyle.FONT_BODY, 10)
    text_obj.setTextOrigin(text_obj_x, y_cursor)
    from ..utils import cached_simpleSplit as simpleSplit

    # Constrain width to avoid hitting right margin
    target_width = width - text_obj_x - 1.0 * cm
    lines = simpleSplit(obj_text, PDFStyle.FONT_BODY, 10, target_width)
    for line in lines:
        text_obj.textLine(line)
    c.drawText(text_obj)

    # --- 2. LAYOUT COORDINATES ---
    center_x = card_margin + (width - card_margin) / 2.0
    cx = center_x

    # Ground Level (Base of trunk)
    ground_y = 4.0 * cm

    # Trunk
    trunk_width_base = 4 * cm
    trunk_width_top = 3.5 * cm
    trunk_height = 8 * cm
    trunk_top_y = ground_y + trunk_height  # 12cm

    # Crown (Branches area)
    crown_top_y = height - 7.0 * cm  # Leave space for header

    form = c.acroForm

    # --- 3. ORGANIC TREE DRAWING ---
    c.saveState()
    c.setStrokeColor(PDFStyle.COLOR_TEXT_SECONDARY)
    c.setLineWidth(1.5)
    c.setLineJoin(1)
    c.setLineCap(1)

    # A. Sol (Uneven ground) - Draw first to be behind roots if needed, or foundation
    p = c.beginPath()
    p.moveTo(cx - 8 * cm, ground_y)
    # Gentle hills
    p.curveTo(
        cx - 5 * cm,
        ground_y + 0.5 * cm,
        cx - 2 * cm,
        ground_y - 0.5 * cm,
        cx,
        ground_y - 0.2 * cm,
    )
    p.curveTo(
        cx + 2 * cm,
        ground_y + 0.4 * cm,
        cx + 5 * cm,
        ground_y - 0.3 * cm,
        cx + 8 * cm,
        ground_y,
    )
    c.drawPath(p, stroke=1, fill=0)

    # B. Racines (Roots) - Below ground
    # Central Root
    p = c.beginPath()
    p.moveTo(cx, ground_y - 0.2 * cm)
    p.curveTo(
        cx - 0.5 * cm,
        ground_y - 1.0 * cm,
        cx + 0.5 * cm,
        ground_y - 1.8 * cm,
        cx,
        ground_y - 2.5 * cm,
    )
    c.drawPath(p, stroke=1, fill=0)
    # Left Root
    p = c.beginPath()
    p.moveTo(cx - 1.5 * cm, ground_y)
    p.curveTo(
        cx - 2 * cm,
        ground_y - 0.8 * cm,
        cx - 3.5 * cm,
        ground_y - 1.2 * cm,
        cx - 5 * cm,
        ground_y - 2.0 * cm,
    )
    c.drawPath(p, stroke=1, fill=0)
    # Right Root
    p = c.beginPath()
    p.moveTo(cx + 1.5 * cm, ground_y)
    p.curveTo(
        cx + 2 * cm,
        ground_y - 0.8 * cm,
        cx + 3.5 * cm,
        ground_y - 1.2 * cm,
        cx + 5 * cm,
        ground_y - 2.0 * cm,
    )
    c.drawPath(p, stroke=1, fill=0)

    # C. Tronc (Trunk) - Wide and solid
    p = c.beginPath()
    # Left side
    p.moveTo(cx - 1.8 * cm, ground_y)
    p.curveTo(
        cx - 1.5 * cm,
        ground_y + 3 * cm,
        cx - 1.5 * cm,
        ground_y + 6 * cm,
        cx - 1.8 * cm,
        trunk_top_y,
    )
    # Right side
    p.moveTo(cx + 1.8 * cm, ground_y)
    p.curveTo(
        cx + 1.5 * cm,
        ground_y + 3 * cm,
        cx + 1.5 * cm,
        ground_y + 6 * cm,
        cx + 1.8 * cm,
        trunk_top_y,
    )
    c.drawPath(p, stroke=1, fill=0)

    # Textures/Cicatrices
    c.setLineWidth(0.5)
    c.arc(
        cx - 0.5 * cm,
        ground_y + 2 * cm,
        cx + 0.5 * cm,
        ground_y + 2.8 * cm,
        startAng=160,
        extent=50,
    )
    c.arc(
        cx + 0.2 * cm,
        ground_y + 5 * cm,
        cx + 1.0 * cm,
        ground_y + 5.6 * cm,
        startAng=200,
        extent=40,
    )

    # D. Crown Branches - Supporting the boxes
    c.setLineWidth(1.5)

    # Left Branch (Holds Leaves Box) -> Aim for (cx-7cm, top_y+4)
    p = c.beginPath()
    p.moveTo(cx - 1.8 * cm, trunk_top_y)
    p.curveTo(
        cx - 4 * cm,
        trunk_top_y + 2 * cm,
        cx - 6 * cm,
        trunk_top_y + 1 * cm,
        cx - 7 * cm,
        trunk_top_y + 4 * cm,
    )
    c.drawPath(p, stroke=1, fill=0)

    # Right Branch (Holds Fruits Box) -> Aim for (cx+7cm, top_y+4)
    p = c.beginPath()
    p.moveTo(cx + 1.8 * cm, trunk_top_y)
    p.curveTo(
        cx + 4 * cm,
        trunk_top_y + 2 * cm,
        cx + 6 * cm,
        trunk_top_y + 1 * cm,
        cx + 7 * cm,
        trunk_top_y + 4 * cm,
    )
    c.drawPath(p, stroke=1, fill=0)

    # Center Branch (Holds Branches/Projects Box) -> Aim for Top Center
    p = c.beginPath()
    p.moveTo(cx, trunk_top_y)  # Start slightly lower
    p.curveTo(
        cx - 2 * cm,
        trunk_top_y + 3 * cm,
        cx + 2 * cm,
        trunk_top_y + 5 * cm,
        cx,
        crown_top_y - 2 * cm,
    )
    c.drawPath(p, stroke=1, fill=0)

    c.restoreState()

    # --- 4. INPUT ZONES & LABELS ---

    def draw_zone(
        title, subtitle, x, y, w, h, align="left", color_title=PDFStyle.COLOR_TEXT_MAIN
    ):
        # Draw background for better readability over lines? No, looks cleaner transparent if placed well.

        # Title
        c.setFont(PDFStyle.FONT_SUBTITLE, 10)
        c.setFillColor(color_title)

        # Calculate text anchor positions
        if align == "center":
            tx, ty = x + w / 2, y + h + 0.6 * cm
            sx, sy = x + w / 2, y + h + 0.2 * cm
            c.drawCentredString(tx, ty, title)
            c.setFont(PDFStyle.FONT_ITALIC, 9)
            c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
            c.drawCentredString(sx, sy, subtitle)
        elif align == "right":
            tx, ty = x + w, y + h + 0.6 * cm
            sx, sy = x + w, y + h + 0.2 * cm
            c.drawRightString(tx, ty, title)
            c.setFont(PDFStyle.FONT_ITALIC, 9)
            c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
            c.drawRightString(sx, sy, subtitle)
        else:
            tx, ty = x, y + h + 0.6 * cm
            sx, sy = x, y + h + 0.2 * cm
            c.drawString(tx, ty, title)
            c.setFont(PDFStyle.FONT_ITALIC, 9)
            c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
            c.drawString(sx, sy, subtitle)

        create_input_field(
            form,
            f"arbre_{title.split()[1].lower()}",
            pos=(x, y),
            size=(w, h),
            multiline=True,
        )

    # Position: y=1.0cm to y=3.3cm
    draw_zone(
        "1. RACINES",
        "Mon histoire, mes origines...",
        cx - 4.5 * cm,
        1.0 * cm,
        9 * cm,
        2.3 * cm,
        align="center",
        color_title=PDFStyle.COLOR_ACCENT_RED,
    )

    # Position: y=3.5cm to y=6.0cm, Left side.
    draw_zone(
        "2. SOL",
        "Mes besoins actuels",
        cx - 8.5 * cm,
        3.5 * cm,
        5 * cm,
        2.5 * cm,
        align="left",
    )

    # Position: y=6cm to y=10.0cm centered on trunk.
    # Widen box slightly to fit trunk width approx
    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawCentredString(cx, 10.6 * cm, "3. TRONC")
    c.setFont(PDFStyle.FONT_ITALIC, 9)
    c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
    c.drawCentredString(cx, 10.2 * cm, "Compétences & Valeurs")

    # Field overlaps the trunk drawing significantly, but that's okay, it's the "content" of the trunk.
    create_input_field(
        form,
        "arbre_tronc",
        pos=(cx - 2.2 * cm, 6.0 * cm),
        size=(4.4 * cm, 4 * cm),
        multiline=True,
    )

    # Position: y=13.5cm approx.
    draw_zone(
        "5. FEUILLES",
        "Club de Vie (Soutiens)",
        cx - 8.5 * cm,
        trunk_top_y + 1.5 * cm,
        5.5 * cm,
        3 * cm,
        align="left",
    )

    # Position: y=13.5cm approx
    draw_zone(
        "6. FRUITS",
        "Cadeaux & Réussites",
        cx + 3.0 * cm,
        trunk_top_y + 1.5 * cm,
        5.5 * cm,
        3 * cm,
        align="right",
    )

    # Position: y=18cm approx.
    draw_zone(
        "4. BRANCHES",
        "Projets & Rêves",
        cx - 4.5 * cm,
        trunk_top_y + 6.0 * cm,
        9 * cm,
        2.5 * cm,
        align="center",
        color_title=PDFStyle.COLOR_ACCENT_BLUE,
    )

    draw_page_decorations(c, width, height, part_title="BONUS", x_offset=card_margin)
    c.showPage()


def create_interview_page(c):
    """
    New Page: Interview avec une personne passionnée (Bonus).
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(
        c, "Interview avec une personne passionnée", pos=(text_x, text_top)
    )

    c.setFont(PDFStyle.FONT_BODY, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(
        text_x,
        new_y - 0.2 * cm,
        "Rencontrez quelqu'un qui a un métier ou une vie qui vous inspire.",
    )

    form = c.acroForm
    y_cursor = new_y - 1.2 * cm

    col1_x = text_x
    col2_x = text_x + 8.0 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(col1_x, y_cursor, "Personne interviewée :")
    create_input_field(
        form,
        "interview_nom",
        pos=(col1_x, y_cursor - 0.8 * cm),
        size=(7.0 * cm, 0.6 * cm),
    )

    c.drawString(col2_x, y_cursor, "Son métier / Activité :")
    create_input_field(
        form,
        "interview_metier",
        pos=(col2_x, y_cursor - 0.8 * cm),
        size=(width - col2_x - 1.5 * cm, 0.6 * cm),
    )

    y_cursor -= 2 * cm

    questions = [
        ("Qu'aimez-vous le plus dans ce que vous faites ?", "interview_q1", 2.5 * cm),
        (
            "Quelles sont les difficultés ou contraintes cachées ?",
            "interview_q2",
            2.5 * cm,
        ),
        (
            "Quel conseil donneriez-vous à quelqu'un qui veut se lancer ?",
            "interview_q3",
            2.5 * cm,
        ),
        ("Ce que j'en retiens pour moi (Mon ressenti) :", "interview_q4", 3.5 * cm),
    ]

    for q_text, q_id, q_height in questions:
        c.setFont(PDFStyle.FONT_SUBTITLE, 11)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(text_x, y_cursor, q_text)
        y_cursor -= q_height + 0.4 * cm
        create_input_field(
            form,
            q_id,
            pos=(text_x, y_cursor),
            size=(width - text_x - 1.5 * cm, q_height),
            multiline=True,
        )
        y_cursor -= 0.6 * cm

    draw_page_decorations(c, width, height, part_title="BONUS", x_offset=card_margin)
    c.showPage()
