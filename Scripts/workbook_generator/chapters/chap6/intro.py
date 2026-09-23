from workbook_generator.components import (
    create_standard_cover,
    create_standard_summary_page,
    create_standard_recap_page,
)


def create_chap6_cover(c):
    """
    Cover Page for Chapter 6 : Phase d'exploration
    """
    create_standard_cover(c, "CHAPITRE 6 : PHASE D'EXPLORATION")


def create_concept_page(c):
    """
    Page 2 : Concept / Sommaire
    """
    points = [
        ("Sommaire :", ""),
        ("1.", "Récapitulatif de la séance précédente"),
        ("2.", "Votre cartographie personnelle"),
        ("3.", "Le retour de vos proches"),
        ("4.", "Sélectionner 10 métiers à explorer"),
        ("5.", "Fiches métiers - Pistes 'No Limit'"),
        ("6.", "Fiches métiers - Pistes 'Réalistes'"),
        ("7.", "Ressources utiles pour vos recherches"),
    ]
    create_standard_summary_page(
        c,
        "6",
        "CONCEPT",
        "Ce temps d'exploration vise à réunir vos pistes de réflexion professionnelle, à synthétiser vos caractéristiques personnelles (MBTI, valeurs, moteurs), et à les confronter aux suggestions de votre entourage pour ouvrir de nouvelles perspectives de métiers.",
        points,
    )


def create_recap_seance_page(c):
    """
    Page 3 : Récapitulatif de la séance précédente (Mes Valeurs)
    """
    intro_txt = "Prenez un moment pour revenir sur la séance précédente consacrée à l'exploration de vos valeurs. Cet exercice vous aide à consolider vos apprentissages avant d'entamer une nouvelle étape. Répondez spontanément."
    questions = [
        "Quelles sont les 3 valeurs non négociables qui guident vos choix aujourd'hui ?",
        "De quoi avez-vous besoin concrètement (conditions de travail) pour respecter ces valeurs ?",
        "Quelles tensions de valeurs (ex: liberté/sécurité) influencent le plus votre transition ?",
    ]
    create_standard_recap_page(
        c,
        "1. RÉCAPITULATIF (MES VALEURS)",
        intro_txt,
        questions,
    )
