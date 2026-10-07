from workbook_generator.components import (
    create_cover_page,
    create_standard_recap_page,
    create_standard_summary_page,
)


def create_chap2_cover(c):
    """Cover of chapter 2: Mon parcours."""
    create_cover_page(c, "Mon *parcours.*", number=2, tagline="Bilan de compétences",
                      promise="Comprendre vos choix passés pour mieux décider.")


def create_concept_page(c):
    """Chapter opener: the objective of the workbook and its exercises."""
    intro_txt = (
        "Ce carnet relit votre parcours pour en dégager le fil rouge : ce que vous avez reçu, ce que vous avez "
        "construit, ce qui vous fait avancer. C'est la base pour décider de la suite."
    )
    exercises = [
        "À lire · Comprendre ses racines : l'habitus, le contrat familial, l'activité empêchée.",
        "Exercice 1 · Récapitulatif de la séance précédente.",
        "Exercice 2 · Analyse du parcours : vos expériences, une par une.",
        "Exercice 3 · Votre fil rouge et vos moteurs.",
        "Exercice 4 · Votre ligne de vie : sommets et vallées.",
        "Exercice 5 · Vos compétences de vie.",
        "Exercice 6 · Votre arbre de vie.",
        "Bonus · Interview d'une personne passionnée.",
    ]
    create_standard_summary_page(c, "2", "Relire *votre parcours.*", intro_txt, exercises)


def create_recap_seance_page(c):
    """Exercise 1: back on the previous session."""
    intro_txt = (
        "Revenez sur la séance précédente pour consolider ce que vous en retenez avant d'ouvrir une nouvelle "
        "étape. Répondez spontanément."
    )
    questions = [
        "Qu’est-ce que cette séance vous a permis de comprendre de plus sur vous-même ?",
        "Quels héritages ou messages reçus influencent encore vos choix professionnels aujourd’hui ?",
        "Parmi ces héritages, que voulez-vous garder, et que voulez-vous faire évoluer ?",
        "En quoi cela éclaire-t-il la suite de votre bilan et vos pistes ?",
    ]
    create_standard_recap_page(c, "Exercice 1 · Récapitulatif", intro_txt, questions)
