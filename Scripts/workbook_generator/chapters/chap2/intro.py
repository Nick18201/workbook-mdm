from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from ...config import PDFStyle
from ...components import (
    create_standard_cover,
    create_standard_summary_page,
    create_standard_recap_page,
)


def create_chap2_cover(c):
    """
    Cover Page for Chapter 2: Mes Racines.
    """
    create_standard_cover(c, "CHAPITRE 2 : MON PARCOURS")


def create_concept_page(c):
    """
    Page 2: Chapter Cover - 2. Concept
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
