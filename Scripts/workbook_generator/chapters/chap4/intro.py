from reportlab.lib.units import cm

from ...config import PDFStyle
from ...components import (
    create_standard_cover,
    create_standard_summary_page,
    create_standard_recap_page,
)


def create_chap4_v2_cover(c):
    """
    Cover Page for Chapter 4 (v2) : Mon rapport à l'argent
    """
    create_standard_cover(c, "CHAPITRE 4 : MON RAPPORT À L'ARGENT")


def create_concept_page(c):
    """
    Page 2 : Concept (v2)
    """
    points = [
        ("Sommaire :", ""),
        ("1.", "Votre situation actuelle"),
        ("2.", "Votre histoire avec l'argent"),
        ("3.", "Vos premières expériences"),
        ("4.", "Argent et projet professionnel"),
        ("5.", "Identifier votre minimum financier acceptable"),
        ("6.", "Repérer ce que l'argent représente pour vous (Archétypes)"),
        ("7.", "Synthèse"),
    ]
    create_standard_summary_page(
        c,
        "4",
        "CONCEPT",
        "Ce temps d'exploration vise à repérer la manière dont votre rapport à l'argent influence vos choix professionnels : besoin de sécurité, capacité à prendre des risques, rapport à la rémunération, négociation, ambition, liberté, peur du manque ou sentiment de légitimité. L'objectif n'est pas d'analyser en profondeur votre gestion financière, mais d'identifier les éléments qui peuvent soutenir ou freiner votre projet professionnel.",
        points,
    )


def create_recap_seance_page(c):
    intro_txt = "Prenez un moment pour revenir sur la restitution de votre profil MBTI lors de la dernière séance. Cet exercice vous aide à consolider ces apprentissages avant d'explorer vos moteurs profonds."
    questions = [
        "Quelles sont les forces naturelles de votre profil MBTI dans lesquelles vous vous reconnaissez le plus ?",
        "Comment ce mode de fonctionnement (énergie, information, décision, action) s'illustre-t-il dans votre quotidien ?",
        "En quoi la compréhension de votre profil change-t-elle votre regard sur vous-même ou sur vos interactions ?",
    ]
    create_standard_recap_page(
        c, "1. RÉCAPITULATIF (MON PROFIL MBTI)", intro_txt, questions
    )
