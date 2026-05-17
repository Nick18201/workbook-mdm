from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.components import create_standard_cover
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)


def create_livret_cover(c):
    """
    Couverture du Livret de Compétences Augmenté.
    """
    create_standard_cover(
        c, "Portfolio Dynamique de Potentiel", title="LIVRET DE COMPÉTENCES AUGMENTÉ"
    )


def create_profil_page(c):
    """
    P1 : PROFIL (Qui je suis)
    """
    layout = PageLayout(
        c,
        "P1 : PROFIL (Qui je suis)",
        config=LayoutConfig(part_title="LIVRET DE COMPÉTENCES"),
    )

    layout.add_text(
        "Cartographie de votre identité professionnelle, au-delà de l'intitulé de poste.",
        config=TextConfig(spacing_after=1.0 * cm),
    )

    layout.add_question_block(
        "ADN : Valeurs & Moteurs",
        "profil_adn",
        config=QuestionConfig(
            box_height=3.5 * cm,
            subtitle="Quelles sont vos valeurs phares et ce qui vous donne de l'énergie ?",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Style : Mode de collaboration",
        "profil_style",
        config=QuestionConfig(
            box_height=3.5 * cm,
            subtitle="Décrivez votre type de personnalité (ex: MBTI) et vos conditions idéales de collaboration.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Boussole : Vision à 3-5 ans",
        "profil_boussole",
        config=QuestionConfig(
            box_height=3.5 * cm,
            subtitle="Vers quoi souhaitez-vous tendre professionnellement à moyen terme ?",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()


def create_parcours_page(c):
    """
    P2 : PARCOURS (D'où je viens)
    """
    layout = PageLayout(
        c,
        "P2 : PARCOURS (D'où je viens)",
        config=LayoutConfig(part_title="LIVRET DE COMPÉTENCES"),
    )

    layout.add_text(
        "Lecture narrative et analytique de votre expérience.",
        config=TextConfig(spacing_after=1.0 * cm),
    )

    layout.add_question_block(
        "Fil Rouge & Génogramme Pro",
        "parcours_fil",
        config=QuestionConfig(
            box_height=6.0 * cm,
            subtitle="Quel est le narratif qui relie vos expériences ? Quels héritages ont influencé vos choix ?",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Carte aux Trésors : Top Compétences",
        "parcours_competences",
        config=QuestionConfig(
            box_height=8.0 * cm,
            subtitle="Listez vos compétences clés (Hard & Soft) par niveau de maîtrise.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()


def create_preuves_page(c):
    """
    P3 : PREUVES (Ce que j'ai réalisé)
    """
    layout = PageLayout(
        c,
        "P3 : PREUVES (Réalisations)",
        config=LayoutConfig(part_title="LIVRET DE COMPÉTENCES"),
    )

    layout.add_text(
        "Sélection de Chef-d'œuvres et Faits Marquants illustrant l'approche STAR.",
        config=TextConfig(spacing_after=1.0 * cm),
    )

    layout.add_question_block(
        "Situation - Tâche - Action - Résultat (STAR)",
        "preuves_star",
        config=QuestionConfig(
            box_height=8.0 * cm,
            subtitle="Détaillez ici 1 à 2 réalisations majeures qui démontrent votre valeur.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Témoignages & Verbatim",
        "preuves_temoignages",
        config=QuestionConfig(
            box_height=6.0 * cm,
            subtitle="Citations de collègues, managers ou clients (issus d'un 360° par exemple).",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()


def create_potentiel_page(c):
    """
    P4 : POTENTIEL (Où je vais)
    """
    layout = PageLayout(
        c,
        "P4 : POTENTIEL (Où je vais)",
        config=LayoutConfig(part_title="LIVRET DE COMPÉTENCES"),
    )

    layout.add_text(
        "Projection vers l'avenir : adaptabilité et apprentissage (Learning Agility).",
        config=TextConfig(spacing_after=1.0 * cm),
    )

    layout.add_question_block(
        "Projet Cible & Transférabilité",
        "potentiel_projet",
        config=QuestionConfig(
            box_height=6.0 * cm,
            subtitle="Quel est l'environnement, la mission et la culture recherchés ? En quoi vos compétences y répondent ?",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Plan de Développement",
        "potentiel_dev",
        config=QuestionConfig(
            box_height=6.0 * cm,
            subtitle="Quelles compétences sont en cours d'acquisition ou prévues ?",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()
