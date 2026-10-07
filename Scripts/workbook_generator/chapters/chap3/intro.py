from workbook_generator.components import (
    create_cover_page,
    create_standard_recap_page,
    create_standard_summary_page,
)
from workbook_generator.config import PDFStyle
from workbook_generator.templates import PageLayout, LayoutConfig


def create_chap3_cover(c):
    """Cover of chapter 3: Mes fonctionnements propres."""
    create_cover_page(c, "Mes fonctionnements *propres.*", number=3, tagline="Bilan de compétences · MBTI®",
                      promise="Comment vous travaillez le mieux.")


def create_concept_page(c):
    """Chapter opener: the objective of the workbook and its exercises."""
    intro_txt = (
        "Ce carnet explore votre façon de fonctionner : où vous puisez votre énergie, ce que vous remarquez en "
        "premier, comment vous décidez, votre rapport au temps et vos réactions sous pression. "
        "Il prépare la restitution de votre profil MBTI®."
    )
    exercises = [
        "Exercice 1 · Récapitulatif de la séance précédente.",
        "Exercice 2 · Votre énergie et votre environnement (questions 1 à 3).",
        "Exercice 3 · Votre regard sur le réel : l'information (questions 4 à 7).",
        "Exercice 4 · Vos décisions (questions 8 à 11).",
        "Exercice 5 · Votre rapport au temps et à l'action (questions 12 à 15).",
        "Exercice 6 · Votre zone d'ombre (questions 16 et 17).",
    ]
    create_standard_summary_page(c, "3", "Votre mode *d'emploi.*", intro_txt, exercises)


def create_recap_seance_page(c):
    """Exercise 1: back on the previous session."""
    intro_txt = (
        "Revenez sur la séance précédente pour consolider ce que vous en retenez avant d'ouvrir une nouvelle "
        "étape. Répondez spontanément."
    )
    questions = [
        "Qu'est-ce que cette séance vous a permis de comprendre de plus sur vous-même ?",
        "Quels éléments de votre ligne de vie ou de votre arbre de vie vous reviennent le plus en tête ?",
        "En quoi cela éclaire-t-il la suite de votre bilan et vos pistes ?",
    ]
    create_standard_recap_page(c, "Exercice 1 · Récapitulatif", intro_txt, questions)


def create_intro_page(c):
    """How to answer the questionnaire, and its five dimensions as a timeline."""
    layout = PageLayout(c, "Avant de *commencer.*", config=LayoutConfig(part_title="Introduction"))
    layout.add_paragraphs([
        "Il n'y a ni bonne ni mauvaise réponse, ni question piège.",
        "Ce qui nous intéresse ici, ce n'est pas ce que vous savez faire (vos compétences), mais ce qui se passe "
        "dans votre tête et dans votre corps (votre énergie).",
        "Détaillez vos réponses : racontez le « pourquoi » et le « comment ». Prenez vos exemples dans votre vie "
        "personnelle (famille, loisirs) autant que professionnelle.",
    ], size=PDFStyle.SIZE_LEAD)
    layout.add_heading("Cinq dimensions, dix-sept questions")
    layout.add_frise(
        [
            ("battery_charging_full", "L'énergie", "Q. 1 à 3"),
            ("visibility", "L'information", "Q. 4 à 7"),
            ("balance", "Les décisions", "Q. 8 à 11"),
            ("schedule", "Le temps et l'action", "Q. 12 à 15"),
            ("dark_mode", "La zone d'ombre", "Q. 16 et 17"),
        ],
    )
    layout.add_callout(
        "Vos réponses préparent la restitution de votre profil MBTI® en séance : apportez ce carnet rempli.",
        title="Pour la séance",
    )
    layout.render()
