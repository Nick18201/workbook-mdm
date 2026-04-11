from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from ..config import PDFStyle
from ..components import (
    draw_page_background,
    draw_side_panel,
    draw_title,
    create_standard_cover,
    draw_page_decorations,
    create_standard_engagement_page,
    create_standard_summary_page,
)
from ..templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig
from ..forms import create_input_field, create_checkbox


def create_chap1_cover(c):
    """
    Cover Page for Chapter 1: L'État des Lieux.
    """
    create_standard_cover(c, "CHAPITRE 1 : L'ÉTAT DES LIEUX")


def create_engagement_page(c):
    """
    Page 1: Mon Engagement.
    Text heavy page with signature.
    """
    create_standard_engagement_page(c, "1. MON ENGAGEMENT")


def create_concept_page(c):
    """
    Page 2: Chapter Cover - 1. Concept
    Blue background, large watermark.
    """
    # Points
    points = [
        ("Sommaire :", ""),
        ("1.", "Mon Engagement"),
        ("2.", "Ma Météo Intérieure"),
        ("3.", "Ma Vision 360°"),
        ("4.", "Mon Objectif Boussole"),
        ("5.", "Le Sac à Dos"),
        ("6.", "Mon Héritage"),
        ("7.", "Image du Monde du Travail"),
        ("8.", "Mentors & Anti-Modèles"),
    ]

    create_standard_summary_page(c, "1", "CONCEPT", "", points)


def create_meteo_page(c):
    """
    Page 3: Ma Météo Intérieure.
    """
    width, height = A4
    draw_page_background(c, width, height)

    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm

    new_y = draw_title(c, "Mon État d'Esprit Actuel", pos=(text_x, text_top))

    form = c.acroForm

    y_opts = new_y - 0.5 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, y_opts, "Aujourd'hui, je me sens :")

    # Text input for "Émotion dominante" (Un mot pour décrire l'instant)
    create_input_field(
        form,
        "meteo_emotion_word",
        pos=(text_x + 5.5 * cm, y_opts - 5),
        size=(8 * cm, 20),
        tooltip="Un mot pour décrire l'instant",
    )

    options = ["Soleil ☀️", "Nuageux ☁️", "Pluvieux 🌧️", "Orageux ⛈️"]
    opt_x = text_x
    opt_y = y_opts - 1.5 * cm

    for opt in options:
        create_checkbox(
            form,
            f"meteo_{opt.split()[0]}",
            pos=(opt_x, opt_y),
            size=0.6 * cm,
            tooltip=opt,
        )
        c.drawString(opt_x + 1 * cm, opt_y + 0.15 * cm, opt)
        opt_x += 4 * cm

    y_energy = opt_y - 3 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, y_energy, "Mon niveau d'énergie :")

    # Labels
    c.setFont(PDFStyle.FONT_ITALIC, 9)
    c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
    c.drawString(text_x, y_energy - 0.5 * cm, "Épuisé (0)")
    c.drawRightString(text_x + 14 * cm, y_energy - 0.5 * cm, "Plein de vitalité (10)")

    # Draw a scale 0-10
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setLineWidth(1)
    c.line(text_x, y_energy - 1.5 * cm, text_x + 14 * cm, y_energy - 1.5 * cm)

    for i in range(11):
        x_mark = text_x + i * 1.4 * cm
        # Draw a small mark
        c.setLineWidth(0.5)
        c.line(x_mark, y_energy - 1.6 * cm, x_mark, y_energy - 1.4 * cm)

        # Draw the checkbox on the mark
        create_checkbox(
            form,
            f"meteo_energy_{i}",
            pos=(x_mark - 0.22 * cm, y_energy - 2.1 * cm),
            size=0.45 * cm,
            tooltip=f"Niveau {i}",
        )

        c.setFont(PDFStyle.FONT_BODY, 8)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawCentredString(x_mark, y_energy - 2.6 * cm, str(i))

    y_thought = y_energy - 4 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.drawString(text_x, y_thought, "Ce qui prend le plus de place dans ma tête :")

    create_input_field(
        form,
        "meteo_pensee",
        pos=(text_x, y_thought - 3 * cm),
        size=(width - text_x - 1 * cm, 2.5 * cm),
        tooltip="Pensée envahissante",
        multiline=True,
    )

    draw_page_decorations(
        c,
        width,
        height,
        part_title="1. Récapitulatif de la séance précédente",
        x_offset=card_margin,
    )
    c.showPage()


def create_vision_page(c):
    """
    Page 4: Ma Vision 'Boule à Facettes'.
    4 Quadrants.
    """
    width, height = A4
    # Side Panel (Full Height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    # Title
    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, "Ma Vision 360°", pos=(text_x, text_top))

    # Instruction
    c.setFont(PDFStyle.FONT_BODY, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(
        text_x,
        new_y - 0.2 * cm,
        "Instruction : Pour chaque domaine, écrivez une phrase de synthèse sur votre aspiration.",
    )

    # Center (Relative to panel)
    center_x = card_margin + (width - card_margin) / 2
    center_y = height / 2 - 2.5 * cm

    # Draw Axes
    c.setLineWidth(1)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)

    # Draw a circle to contain the axes visually (Radar chart style)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setFillColor(PDFStyle.COLOR_BG_BLOB)
    c.circle(center_x, center_y, 7 * cm, stroke=1, fill=1)

    c.setLineWidth(0.5)
    c.setFillColor(PDFStyle.COLOR_CARD_CREME)
    c.circle(center_x, center_y, 3.5 * cm, stroke=1, fill=1)  # Inner circle

    c.saveState()
    c.setDash(4, 4)
    c.line(center_x, center_y - 7 * cm, center_x, center_y + 7 * cm)  # Vertical
    c.line(center_x - 7 * cm, center_y, center_x + 7 * cm, center_y)  # Horizontal
    c.restoreState()

    # Quadrants Labels & Inputs
    # Strict labels from Markdown
    axes = [
        ("Professionnel (Sens, Mission, Salaire)", -1, 1),  # Top Left
        ("Personnel (Temps pour soi, Santé)", 1, 1),  # Top Right
        ("Social/Familial (Relations, Équilibre)", -1, -1),  # Bottom Left
        ("Hiérarchie/Structure (Besoin de cadre vs Liberté)", 1, -1),  # Bottom Right
    ]

    form = c.acroForm

    for title, dx, dy in axes:
        # Determine specific area center
        q_center_x = center_x + (dx * (3.5 * cm))
        q_center_y = center_y + (dy * (3.5 * cm))

        words = title.split("(")
        main_title = words[0].strip()
        sub_title = "(" + words[1] if len(words) > 1 else ""

        # Dimensions de la zone de saisie
        field_width = 5.8 * cm
        field_height = 1.8 * cm

        # Placement dynamique symétrique pour éviter les chevauchements
        if dy == 1:  # Haut
            text_y = center_y + 5.2 * cm
            f_y = center_y + 1.5 * cm
        else:  # Bas
            text_y = center_y - 5.0 * cm
            f_y = center_y - 3.3 * cm

        f_x = q_center_x - (field_width / 2)

        # Draw Text Background (Forme de 'pill' ou de badge arrondi)
        text_width = c.stringWidth(main_title, PDFStyle.FONT_BRANDING, 14)
        c.saveState()
        c.setFillColor(PDFStyle.COLOR_WHITE, alpha=0.95)
        c.setStrokeColor(PDFStyle.COLOR_WHITE, alpha=0)
        c.roundRect(
            q_center_x - text_width / 2 - 10,
            text_y - 5,
            text_width + 20,
            20,
            radius=10,
            fill=1,
            stroke=0,
        )
        c.restoreState()

        c.setFont(PDFStyle.FONT_BRANDING, 14)
        c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
        c.drawCentredString(q_center_x, text_y, main_title)

        if sub_title:
            sub_width = c.stringWidth(sub_title, PDFStyle.FONT_BODY, 10)
            c.saveState()
            c.setFillColor(PDFStyle.COLOR_WHITE, alpha=0.95)
            c.setStrokeColor(PDFStyle.COLOR_WHITE, alpha=0)
            c.roundRect(
                q_center_x - sub_width / 2 - 6,
                text_y - 0.5 * cm - 4,
                sub_width + 12,
                14,
                radius=7,
                fill=1,
                stroke=0,
            )
            c.restoreState()

            c.setFont(PDFStyle.FONT_BODY, 10)
            c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            c.drawCentredString(q_center_x, text_y - 0.5 * cm, sub_title)

        # Input Field: Centré dans le quadrant
        create_input_field(
            form,
            f"vision_{main_title.strip()}",
            pos=(f_x, f_y),
            size=(field_width, field_height),
            tooltip="Phrase de synthèse",
            multiline=True,
            fill_color=PDFStyle.COLOR_CARD_CREME,
        )

    draw_page_decorations(
        c,
        width,
        height,
        part_title="1. Récapitulatif de la séance précédente",
        x_offset=card_margin,
    )
    c.showPage()


def create_boussole_page(c):
    """
    Page 5: Mon Objectif Boussole.
    """
    width, height = A4
    draw_page_background(c, width, height)

    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm

    new_y = draw_title(c, "Mon Objectif Boussole", pos=(text_x, text_top))

    form = c.acroForm

    # Visual Compass (Placeholder Circle)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(3)
    c.circle(width / 2, new_y - 1.5 * cm, 1.5 * cm, fill=0, stroke=1)
    # North mark
    c.setFont(PDFStyle.FONT_BRANDING, 20)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawCentredString(width / 2, new_y - 1.5 * cm + 0.8 * cm, "N")

    # Main Goal Structure
    # "D'ici 3 mois, je veux avoir clarifié [Enjeu principal] pour pouvoir [Bénéfice concret]."

    y_goal = new_y - 4.5 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 13)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, y_goal, "D'ici 3 mois, je veux avoir clarifié :")

    create_input_field(
        form,
        "boussole_enjeu",
        pos=(text_x, y_goal - 2 * cm),
        size=(width - text_x - 1 * cm, 1.5 * cm),
        tooltip="Enjeu principal",
        multiline=True,
    )

    y_benefit = y_goal - 3 * cm
    c.drawString(text_x, y_benefit, "Pour pouvoir :")

    create_input_field(
        form,
        "boussole_benefice",
        pos=(text_x, y_benefit - 2 * cm),
        size=(width - text_x - 1 * cm, 1.5 * cm),
        tooltip="Bénéfice concret",
        multiline=True,
    )

    # Success Indicator
    y_succes = y_benefit - 3.5 * cm
    c.drawString(text_x, y_succes, "Je saurai que j'ai réussi quand :")

    create_input_field(
        form,
        "boussole_succes_preuve",
        pos=(text_x, y_succes - 2.5 * cm),
        size=(width - text_x - 1 * cm, 2 * cm),
        tooltip="Preuve concrète",
        multiline=True,
    )

    draw_page_decorations(
        c,
        width,
        height,
        part_title="1. Récapitulatif de la séance précédente",
        x_offset=card_margin,
    )
    c.showPage()


def create_sac_a_dos_page(c):
    """
    Page 6: Le Sac à Dos.
    Specific prompts from Markdown.
    """
    layout = PageLayout(
        c,
        "Ce que je dépose aujourd'hui",
        config=LayoutConfig(part_title="1. Récapitulatif de la séance précédente"),
    )
    layout.add_text(
        "Allégeons le sac à dos. Je décide de déposer :",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout.add_question_block(
        "Je lâche cette croyance :",
        "sac_croyance",
        config=QuestionConfig(box_height=2.5 * cm),
    )
    layout.add_question_block(
        "Je ne veux plus subir :",
        "sac_subir",
        config=QuestionConfig(box_height=2.5 * cm),
    )
    layout.add_question_block(
        "Ma plus grande peur est :",
        "sac_peur",
        config=QuestionConfig(box_height=2.5 * cm),
    )

    layout.add_text(
        "...et je décide de la regarder en face.",
        config=TextConfig(style_choice="italic"),
    )

    layout.render()


def create_heritage_page(c):
    """
    Page: Mon Héritage (3FVS - Genogramme Simplifié).
    Focus: Transmissions, Loyautés, Mandats.
    """
    layout = PageLayout(
        c,
        "Mon Héritage (Matrice 3FVS)",
        config=LayoutConfig(part_title="2. Mes héritages"),
    )
    layout.add_text(
        "Identifiez ce que vous avez reçu pour décider de ce que vous en faites.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout.add_question_block(
        "1. FORCES (Ce que je garde / Résilience)",
        "heritage_forces",
        config=QuestionConfig(
            box_height=3.5 * cm,
            subtitle="Quelles qualités, valeurs ou savoir-faire de ma famille sont des atouts ?",
        ),
    )

    layout.add_question_block(
        "2. VIGILANCES (Ce que je laisse / Schémas)",
        "heritage_vigilances",
        config=QuestionConfig(
            box_height=3.5 * cm,
            subtitle="Quels comportements ou croyances limitantes je décide de ne pas reproduire ?",
        ),
    )

    layout.add_question_block(
        "3. SOUHAITS & COMPTES (Mandats Familiaux)",
        "heritage_souhaits",
        config=QuestionConfig(
            box_height=3.5 * cm,
            subtitle="Qu'est-ce qu'on voulait pour moi ? A qui ai-je l'impression de devoir quelque chose ?",
        ),
    )

    # Note bas de page
    c.setFont(PDFStyle.FONT_ITALIC, 10)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawCentredString(
        A4[0] / 2,
        2 * cm,
        "On ne trahit pas ses origines en choisissant sa propre voie. On les honore différemment.",
    )

    layout.render()


def create_work_image_page(c):
    """
    Page: Image du Monde du Travail.
    Based on Exercice_Image_Travail.md
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    new_y = draw_title(c, "Image du Monde du Travail", pos=(text_x, height - 4.0 * cm))

    form = c.acroForm
    y_cursor = new_y - 0.5 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, y_cursor, "1. Exploration Sensorielle & Emotionnelle")

    y_cursor -= 0.8 * cm
    c.setFont(PDFStyle.FONT_BODY, 10)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(
        text_x,
        y_cursor,
        "Fermez les yeux. Visualisez le lieu de travail de vos parents (ou figures parentales).",
    )
    y_cursor -= 0.5 * cm
    c.drawString(
        text_x,
        y_cursor,
        "Quelles sont les odeurs ? Les bruits ? La lumière ? L'ambiance générale ?",
    )

    y_cursor -= 2.6 * cm
    create_input_field(
        form,
        "image_sensorielle",
        pos=(text_x, y_cursor),
        size=(width - text_x - 1.5 * cm, 2.2 * cm),
        multiline=True,
        tooltip="Décrivez l'ambiance sensorielle du travail de vos parents...",
    )

    y_cursor -= 1.2 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(text_x, y_cursor, "2. L'Héritage Familial")

    questions = [
        (
            "Quel était le travail de vos parents / grands-parents ?",
            "image_metiers",
            1.2 * cm,
        ),
        (
            "Quelle était leur relation au travail ? (Plaisir, Souffrance, Ennui...)",
            "image_relation",
            1.2 * cm,
        ),
        (
            "Comment leur travail influençait-il la vie de famille ? (Stress, Absences, Argent...)",
            "image_impact_famille",
            1.2 * cm,
        ),
        (
            "Comment ont-ils influencé vos choix ? (Encouragements, Dissuasions...)",
            "image_influence_choix",
            1.2 * cm,
        ),
    ]

    y_cursor -= 0.8 * cm
    for q_text, q_id, q_height in questions:
        c.setFont(PDFStyle.FONT_BODY, 10)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(text_x, y_cursor, q_text)
        y_cursor -= q_height + 0.2 * cm
        create_input_field(
            form,
            q_id,
            pos=(text_x, y_cursor),
            size=(width - text_x - 1.5 * cm, q_height),
            multiline=True,
        )
        y_cursor -= 0.6 * cm

    # Split into 2 columns
    y_cursor -= 0.8 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, y_cursor + 0.5 * cm, "3. Changer de Regard")

    col_width = (width - text_x - 1.5 * cm) / 2 - 0.5 * cm

    # Col 1: Avant
    c.setFont(PDFStyle.FONT_ITALIC, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, y_cursor, "5 Mots associés au travail (Héritage) :")
    create_input_field(
        form,
        "image_mots_heritage",
        pos=(text_x, y_cursor - 2.5 * cm),
        size=(col_width, 2.2 * cm),
        multiline=True,
    )

    # Col 2: Futur
    right_col_x = text_x + col_width + 1 * cm
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)  # alternating visual!
    c.drawString(right_col_x, y_cursor, "5 Mots pour mon futur travail (Désir) :")
    create_input_field(
        form,
        "image_mots_futur",
        pos=(right_col_x, y_cursor - 2.5 * cm),
        size=(col_width, 2.2 * cm),
        multiline=True,
    )

    draw_page_decorations(
        c, width, height, part_title="2. Mes héritages", x_offset=card_margin
    )
    c.showPage()


def create_mentors_page(c):
    """
    Page: Mentors & Anti-Modèles.
    """
    layout = PageLayout(
        c, "Mentors & Anti-Modèles", config=LayoutConfig(part_title="2. Mes héritages")
    )
    layout.add_question_block(
        "Mes Mentors (Inspirations)",
        "mentors_positif",
        config=QuestionConfig(
            box_height=6.0 * cm,
            subtitle="Qui est votre héros professionnel (réel ou fictif) et pourquoi ? (J'admire X pour...)",
        ),
    )

    layout.add_question_block(
        "Mes Anti-Modèles (Repoussoirs)",
        "mentors_negatif",
        config=QuestionConfig(
            box_height=6.0 * cm,
            subtitle="Quels sont les comportements ou situations que vous refusez de reproduire ? (Je ne veux pas reproduire...)",
        ),
    )

    layout.render()
