import os
import math
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.forms import create_input_field, create_checkbox
from workbook_generator.components import (
    draw_title,
    draw_page_decorations,
    draw_side_panel,
    draw_page_background,
    create_standard_meteo_page,
    create_standard_quadrants_page,
)

from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig

def create_meteo_page(c):
    """
    Page 3: Ma Météo Intérieure.
    """
    create_standard_meteo_page(
        c,
        title="Mon État d'Esprit Actuel",
        part_title="1. Récapitulatif de la séance précédente",
        field_prefix="meteo",
    )


def create_vision_page(c):
    """
    Page 4: Ma Vision 'Boule à Facettes'.
    4 Quadrants.
    """
    create_standard_quadrants_page(
        c,
        title="Ma Vision 360°",
        part_title="1. Récapitulatif de la séance précédente",
        instruction="Instruction : Pour chaque domaine, écrivez une phrase de synthèse sur votre aspiration.",
        quadrants_data=[
            ("Professionnel", "Sens, Mission, Salaire", "pro"),
            ("Personnel", "Temps pour soi, Santé", "perso"),
            ("Social/Familial", "Relations, Équilibre", "social"),
            ("Hiérarchie/Structure", "Besoin de cadre vs Liberté", "cadre"),
        ],
        field_prefix="vision",
    )




def create_boussole_page(c):
    """
    Page 5: Mon Objectif Boussole.
    """
    layout = PageLayout(
        c,
        "Mon Objectif Boussole",
        config=LayoutConfig(part_title="1. Récapitulatif de la séance précédente"),
    )

    # Visual Compass (Placeholder Circle)
    center_x = layout.text_x + layout.target_width / 2
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(3)
    c.circle(center_x, layout.y_cursor - 1.5 * cm, 1.5 * cm, fill=0, stroke=1)
    # North mark
    c.setFont(PDFStyle.FONT_BRANDING, 20)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawCentredString(center_x, layout.y_cursor - 1.5 * cm + 0.8 * cm, "N")

    layout.y_cursor -= 4.0 * cm

    # Main Goal Structure
    layout.add_question_block(
        "D'ici 3 mois, je veux avoir clarifié :",
        "boussole_enjeu",
        config=QuestionConfig(
            box_height=2.3 * cm,
            color_alternation=False,
        ),
    )

    layout.add_question_block(
        "Pour pouvoir :",
        "boussole_benefice",
        config=QuestionConfig(
            box_height=2.3 * cm,
            color_alternation=False,
        ),
    )

    # Success Indicator
    layout.add_question_block(
        "Je saurai que j'ai réussi quand :",
        "boussole_succes_preuve",
        config=QuestionConfig(
            box_height=3.2 * cm,
            color_alternation=False,
        ),
    )

    layout.render()




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
        config=QuestionConfig(box_height=3.5 * cm),
    )
    layout.add_question_block(
        "Je ne veux plus subir :",
        "sac_subir",
        config=QuestionConfig(box_height=3.5 * cm),
    )
    layout.add_question_block(
        "Ma plus grande peur est :",
        "sac_peur",
        config=QuestionConfig(box_height=3.5 * cm),
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
            box_height=3.8 * cm,
            subtitle="Quelles qualités, valeurs ou savoir-faire de ma famille sont des atouts ?",
        ),
    )

    layout.add_question_block(
        "2. VIGILANCES (Ce que je laisse / Schémas)",
        "heritage_vigilances",
        config=QuestionConfig(
            box_height=3.8 * cm,
            subtitle="Quels comportements ou croyances limitantes je décide de ne pas reproduire ?",
        ),
    )

    layout.add_question_block(
        "3. SOUHAITS & COMPTES (Mandats Familiaux)",
        "heritage_souhaits",
        config=QuestionConfig(
            box_height=3.8 * cm,
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
    layout = PageLayout(
        c,
        "Image du Monde du Travail",
        config=LayoutConfig(part_title="2. Mes héritages"),
    )

    # 1. Exploration Sensorielle & Emotionnelle
    layout.add_question_block(
        "1. Exploration Sensorielle & Emotionnelle",
        "image_sensorielle",
        config=QuestionConfig(
            box_height=2.2 * cm,
            subtitle="Fermez les yeux. Visualisez le lieu de travail de vos parents (ou figures parentales). Quelles sont les odeurs ? Les bruits ? La lumière ? L'ambiance générale ?",
            color_alternation=False,  # Use first color (blue)
        ),
    )

    # 2. L'Héritage Familial
    # Using layout.add_text to handle subtitle and spacing
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

    # 3. Changer de Regard
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

    # Col 1: Avant
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

    # Col 2: Futur
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
