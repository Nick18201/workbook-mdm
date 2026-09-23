from reportlab.lib.units import cm
from workbook_generator.components import (
    create_standard_cover,
    create_standard_summary_page,
    create_standard_recap_page,
)
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig


def create_chap3_cover(c):
    create_standard_cover(c, "CHAPITRE 3 : DÉCOUVERTE DE MES FONCTIONNEMENTS PROPRES")


def create_concept_page(c):
    points = [
        ("Sommaire :", ""),
        ("1.", "Récapitulatif de la séance précédente"),
        ("2.", "Introduction au livret 'découverte de mes fonctionnements propres'"),
        ("3.", "Mon Énergie et mon Environnement"),
        ("4.", "Mon Regard sur le Réel (L'Information)"),
        ("5.", "Ma Boussole Intérieure (Les Décisions)"),
        ("6.", "Mon Rapport au Temps et à l'Action"),
        ("7.", "Ma Zone d'Ombre"),
    ]
    create_standard_summary_page(c, "3", "CONCEPT", "", points)


def create_recap_seance_page(c):
    intro_txt = (
        "Prenez un moment pour revenir sur nos précédents échanges. Cet exercice "
        "vous aide à consolider vos apprentissages avant d'entamer une nouvelle étape. Répondez spontanément."
    )
    questions = [
        "Qu'est-ce que cette séance vous a permis de comprendre de plus sur vous-même ?",
        "Quels éléments de votre ligne de vie ou arbre de vie vous reviennent le plus en tête ?",
        "En quoi cela éclaire différemment la suite de votre bilan et vos pistes pour la suite ?",
    ]
    create_standard_recap_page(c, "1. RÉCAPITULATIF", intro_txt, questions)


def create_intro_page(c):
    """Page d'introduction sans bloc signature."""
    layout = PageLayout(
        c,
        "Mode d'Emploi de Moi-Même",
        config=LayoutConfig(part_title="2. INTRODUCTION"),
    )

    text_content = (
        "Considérez ce document comme un journal intime. Il n'y a pas de "
        "bonnes ou de mauvaises réponses, ni de questions pièges.\n\n"
        "Ce qui nous intéresse, ce n'est pas ce que vous savez faire "
        "(vos compétences), mais ce qui se passe dans votre tête et dans "
        "votre corps (votre énergie).\n\n"
        "Prenez le temps de détailler vos pensées. Racontez-nous "
        "le 'pourquoi' et le 'comment'. N'hésitez pas à utiliser des "
        "exemples de votre vie personnelle (famille, loisirs) autant que "
        "professionnelle."
    )

    layout.add_text(
        text_content, config=TextConfig(font_size=12, spacing_after=0.6 * cm)
    )

    layout.render()
