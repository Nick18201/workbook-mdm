from workbook_generator.components import (
    create_cover_page,
    create_standard_recap_page,
    create_standard_summary_page,
)


def create_chap6_cover(c):
    """Cover of chapter 6: Phase d'exploration."""
    create_cover_page(c, "Phase *d'exploration.*", number=6, tagline="Bilan de compétences",
                      promise="Des pistes confrontées au réel.")


def create_concept_page(c):
    """Chapter opener: the objective of the workbook and its exercises."""
    intro_txt = (
        "Ce carnet rassemble vos pistes professionnelles, résume ce que vous savez de vous (profil MBTI®, valeurs, "
        "moteurs) et le confronte aux idées de votre entourage, pour ouvrir et tester des pistes de métiers."
    )
    exercises = [
        "Exercice 1 · Récapitulatif : vos valeurs.",
        "Exercice 2 · Votre cartographie personnelle.",
        "Exercice 3 · Le retour de vos proches.",
        "Exercice 4 · Dix métiers à explorer.",
        "Exercice 5 · Fiches métiers : les pistes « no limit ».",
        "Exercice 6 · Fiches métiers : les pistes réalistes.",
        "Ressources · Pour vos recherches.",
    ]
    create_standard_summary_page(c, "6", "Explorer *des pistes.*", intro_txt, exercises)


def create_recap_seance_page(c):
    """Exercise 1: back on the values session."""
    intro_txt = (
        "Revenez sur la séance consacrée à vos valeurs, pour consolider ce que vous en retenez avant d'ouvrir une "
        "nouvelle étape. Répondez spontanément."
    )
    questions = [
        "Quelles sont les 3 valeurs non négociables qui guident vos choix aujourd'hui ?",
        "De quoi avez-vous besoin concrètement (conditions de travail) pour respecter ces valeurs ?",
        "Quelles tensions de valeurs (par exemple liberté / sécurité) pèsent le plus sur votre transition ?",
    ]
    create_standard_recap_page(c, "Exercice 1 · Récapitulatif valeurs", intro_txt, questions)
