import math
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.forms import create_input_field
from workbook_generator.forms import create_checkbox
from workbook_generator.components import (
    draw_title,
    draw_page_decorations,
    draw_side_panel,

    draw_dot_grid,
)
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig


def _draw_emotion_section(c, form, text_x, y_pos):
    y_opts = y_pos - 0.5 * cm
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, y_pos, "A. Mon Émotion Dominante")

    emotions = ["Joie", "Colère", "Peur", "Tristesse", "Surprise", "Dégoût"]
    col_width = 3.0 * cm
    for i, emo in enumerate(emotions):
        x_emo = text_x + (i % 3) * col_width
        y_emo = y_opts - (i // 3) * 0.8 * cm
        create_checkbox(
            form,
            f"meteo_emo_{emo}",
            pos=(x_emo, y_emo - 0.2 * cm),


        )
        c.setFont(PDFStyle.FONT_BODY, 10)
        c.drawString(x_emo + 0.6 * cm, y_emo, emo)
    return y_opts - 1.6 * cm


def _draw_energy_scale(c, form, text_x, y_pos):
    y_energy = y_pos
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.drawString(text_x, y_energy, "B. Mon Niveau d'Énergie (0-10)")

    # Ligne d'échelle
    y_line = y_energy - 1.0 * cm
    c.setStrokeColor(PDFStyle.COLOR_LINE)
    c.line(text_x + 1 * cm, y_line, text_x + 11 * cm, y_line)

    for i in range(11):
        x_tick = text_x + 1 * cm + i * 1 * cm
        c.circle(x_tick, y_line, 0.15 * cm, fill=1, stroke=0)
        c.setFont(PDFStyle.FONT_BODY, 8)
        c.drawCentredString(x_tick, y_line - 0.5 * cm, str(i))
        create_checkbox(
            form,
            f"meteo_energie_{i}",
            pos=(x_tick - 0.15 * cm, y_line - 0.15 * cm),


        )
    return y_line - 1.0 * cm


def _draw_thought_input(c, form, text_x, y_pos, width):
    y_thought = y_pos
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.drawString(text_x, y_thought, "C. Ma Pensée Polluante du moment")
    create_input_field(
        form,
        "meteo_pensee",
        pos=(text_x, y_thought - 2.5 * cm),
        size=(width - 2 * text_x, 2.0 * cm),
        multiline=True,
    )
    return y_thought - 3.5 * cm


def create_meteo_page(c):
    """
    Page 3: Ma Météo Intérieure.
    """
    width, height = A4
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, "Ma Météo Intérieure", pos=(text_x, text_top))

    c.setFont(PDFStyle.FONT_BODY, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, new_y - 0.2 * cm, "Comment je me sens ici et maintenant ?")

    form = c.acroForm
    y_pos = new_y - 1.5 * cm

    y_pos = _draw_emotion_section(c, form, text_x, y_pos)
    y_pos -= 0.5 * cm
    y_pos = _draw_energy_scale(c, form, text_x, y_pos)
    y_pos -= 0.5 * cm
    y_pos = _draw_thought_input(c, form, text_x, y_pos, width)

    draw_page_decorations(
        c,
        width,
        height,
        part_title="1. Récapitulatif de la séance précédente",
        x_offset=card_margin,
    )
    c.showPage()


def _draw_radar_background(c, center_x, center_y):
    """Draws the radar chart background (circles and dashed axes)."""
    c.setStrokeColor(PDFStyle.COLOR_LINE)
    c.setFillColor(PDFStyle.COLOR_LINE)
    for r in [2 * cm, 4 * cm, 6 * cm]:
        c.setDash()
        c.circle(center_x, center_y, r, stroke=1, fill=0)

    # Diagonal Axes
    c.setDash(2, 2)
    c.line(
        center_x - 6 * cm * math.cos(math.pi / 4),
        center_y - 6 * cm * math.sin(math.pi / 4),
        center_x + 6 * cm * math.cos(math.pi / 4),
        center_y + 6 * cm * math.sin(math.pi / 4),
    )
    c.line(
        center_x - 6 * cm * math.cos(math.pi / 4),
        center_y + 6 * cm * math.sin(math.pi / 4),
        center_x + 6 * cm * math.cos(math.pi / 4),
        center_y - 6 * cm * math.sin(math.pi / 4),
    )
    c.setDash()


def _draw_quadrant(c, form, title, dx, dy, center_x, center_y):
    """Draws a single quadrant including labels, backgrounds, and input fields."""
    q_center_x = center_x + dx * 4.5 * cm
    q_center_y = center_y + dy * 4.5 * cm

    field_width = 7.0 * cm
    field_height = 2.0 * cm

    f_x = q_center_x - field_width / 2
    f_y = q_center_y - field_height / 2

    # Draw colored background box
    c.setFillColor(PDFStyle.COLOR_CARD_CREME)
    c.setStrokeColor(PDFStyle.COLOR_LINE)
    c.roundRect(f_x, f_y, field_width, field_height, 4, fill=1, stroke=1)

    main_title = title.split(" (")[0]
    sub_title = title.split(" (")[1].replace(")", "") if "(" in title else ""

    text_y = f_y + field_height + 0.8 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawCentredString(q_center_x, text_y, main_title)

    if sub_title:
        c.setFont(PDFStyle.FONT_BODY, 8)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawCentredString(q_center_x, text_y - 0.5 * cm, sub_title)

    create_input_field(
        form,
        f"vision_{main_title}",
        pos=(f_x, f_y),
        size=(field_width, field_height),
        tooltip="Phrase de synthèse",
        multiline=True,
        fill_color=PDFStyle.COLOR_CARD_CREME,
    )


def create_vision_page(c):
    """
    Page 4: Ma Vision 'Boule à Facettes'.
    """
    width, height = A4
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(c, "Ma Vision 360°", pos=(text_x, text_top))

    c.setFont(PDFStyle.FONT_BODY, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(
        text_x,
        new_y - 0.2 * cm,
        "Instruction : Pour chaque domaine, écrivez une phrase de synthèse sur votre aspiration.",
    )

    center_x = card_margin + (width - card_margin) / 2
    center_y = height / 2 - 2.5 * cm

    _draw_radar_background(c, center_x, center_y)

    axes = [
        ("Professionnel (Sens, Mission, Salaire)", -1, 1),
        ("Personnel (Temps pour soi, Santé)", 1, 1),
        ("Social/Familial (Relations, Équilibre)", -1, -1),
        ("Hiérarchie/Structure (Besoin de cadre vs Liberté)", 1, -1),
    ]

    form = c.acroForm

    for title, dx, dy in axes:
        _draw_quadrant(c, form, title, dx, dy, center_x, center_y)

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
    layout = PageLayout(
        c,
        "Mon Objectif Boussole",
        config=LayoutConfig(part_title="1. Récapitulatif de la séance précédente"),
    )

    center_x = layout.text_x + layout.target_width / 2
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(3)
    c.circle(center_x, layout.y_cursor - 1.5 * cm, 1.5 * cm, fill=0, stroke=1)
    c.setFont(PDFStyle.FONT_BRANDING, 20)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawCentredString(center_x, layout.y_cursor - 1.5 * cm + 0.8 * cm, "N")

    layout.y_cursor -= 4.0 * cm

    layout.add_question_block(
        "D'ici 3 mois, je veux avoir clarifié :",
        "boussole_enjeu",
        config=QuestionConfig(
            box_height=1.5 * cm,
            color_alternation=False,
        ),
    )

    layout.add_question_block(
        "Pour pouvoir :",
        "boussole_benefice",
        config=QuestionConfig(
            box_height=1.5 * cm,
            color_alternation=False,
        ),
    )

    layout.add_question_block(
        "Je saurai que j'ai réussi quand :",
        "boussole_succes_preuve",
        config=QuestionConfig(
            box_height=2.0 * cm,
            color_alternation=False,
        ),
    )

    layout.render()


def create_sac_a_dos_page(c):
    """
    Page 6: Le Sac à Dos.
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
    """
    layout = PageLayout(
        c,
        "Image du Monde du Travail",
        config=LayoutConfig(part_title="2. Mes héritages"),
    )

    layout.add_question_block(
        "1. Exploration Sensorielle & Emotionnelle",
        "image_sensorielle",
        config=QuestionConfig(
            box_height=2.2 * cm,
            subtitle="Fermez les yeux. Visualisez le lieu de travail de vos parents (ou figures parentales). Quelles sont les odeurs ? Les bruits ? La lumière ? L'ambiance générale ?",
            color_alternation=False,
        ),
    )

    layout.add_text(
        "2. L'Héritage Familial",
        config=TextConfig(
            style_choice="subtitle",
            font_size=12,
            color=PDFStyle.COLOR_ACCENT_RED,
            spacing_after=0.3 * cm,
        ),
    )

    questions = [
        ("Quel était le travail de vos parents / grands-parents ?", "image_metiers"),
        (
            "Quelle était leur relation au travail ? (Plaisir, Souffrance, Ennui...)",
            "image_relation",
        ),
        (
            "Comment leur travail influençait-il la vie de famille ? (Stress, Absences, Argent...)",
            "image_impact_famille",
        ),
        (
            "Comment ont-ils influencé vos choix ? (Encouragements, Dissuasions...)",
            "image_influence_choix",
        ),
    ]

    for q_text, q_id in questions:
        layout.add_question_block(
            q_text,
            q_id,
            config=QuestionConfig(
                box_height=1.2 * cm,
                color_alternation=False,
                color=PDFStyle.COLOR_TEXT_MAIN,
            ),
        )

    layout.add_text(
        "3. Changer de Regard",
        config=TextConfig(
            style_choice="subtitle",
            font_size=12,
            color=PDFStyle.COLOR_ACCENT_BLUE,
            spacing_after=0.3 * cm,
        ),
    )

    col_width = (layout.target_width - 1.0 * cm) / 2

    c.setFont(PDFStyle.FONT_ITALIC, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        layout.text_x, layout.y_cursor, "5 Mots associés au travail (Héritage) :"
    )
    create_input_field(
        layout.form,
        "image_mots_heritage",
        pos=(layout.text_x, layout.y_cursor - 2.5 * cm),
        size=(col_width, 2.2 * cm),
        multiline=True,
    )

    right_col_x = layout.text_x + col_width + 1 * cm
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        right_col_x, layout.y_cursor, "5 Mots pour mon futur travail (Désir) :"
    )
    create_input_field(
        layout.form,
        "image_mots_futur",
        pos=(right_col_x, layout.y_cursor - 2.5 * cm),
        size=(col_width, 2.2 * cm),
        multiline=True,
    )

    layout.y_cursor -= 2.5 * cm

    layout.render()


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
