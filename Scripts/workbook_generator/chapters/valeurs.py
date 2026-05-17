from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from ..config import PDFStyle
from ..components import (
    create_standard_cover,
    create_standard_summary_page,
)
from ..templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig
from ..forms import create_checkbox

def create_valeurs_cover(c):
    create_standard_cover(c, "WORKBOOK : MES VALEURS ET MOTEURS PROFONDS")

def create_concept_page(c):
    points = [
        ("Sommaire :", ""),
        ("1.", "Les 10 Valeurs de Schwartz (Référence)"),
        ("2.", "Le Questionnaire PVQ-21"),
        ("3.", "Questions de Validation & Personnalité Pro"),
        ("4.", "Mes Moteurs Profonds (Valeurs)"),
        ("5.", "Mes Moteurs Profonds (Verbes d'Action)"),
    ]
    create_standard_summary_page(c, "V", "VALEURS", "", points)

def create_valeurs_page(c):
    layout = PageLayout(
        c,
        "Mes Moteurs Profonds (Valeurs)",
        config=LayoutConfig(part_title="2A. MES MOTEURS PROFONDS")
    )
    layout.add_text(
        "⏱ ~15 min | 🎯 Identifier vos valeurs fondamentales pour mieux comprendre vos choix",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text(
        "Vivre en accord avec ses valeurs nourrit l'Estime de Soi. Vivre en désaccord la détruit. À partir de la liste de valeurs de Schwarz, identifiez celles qui sont fondamentales pour vous.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout.add_question_block(
        "1. Identification : Illustrez vos 3 valeurs principales par un exemple de votre vie :",
        "valeurs_q1",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "2. Héritage : De qui avez-vous reçu ces valeurs ?",
        "valeurs_q2",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "3. Conflits de Valeurs : Identifiez un moment de conflit intérieur. Quelles étaient les valeurs en présence et comment ce conflit s'est-il résolu ?",
        "valeurs_q3",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Bilan : Ce que cet exercice m'apprend sur mes moteurs profonds et ce que ces conflits disent de positif sur moi :",
        "valeurs_q4",
        config=QuestionConfig(box_height=3.0 * cm),
    )

    layout.render()


def create_verbes_page(c):
    layout = PageLayout(
        c,
        "Mes Moteurs Profonds (Verbes d'Action)",
        config=LayoutConfig(part_title="2B. MES MOTEURS PROFONDS")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Repérer les actions qui vous donnent de l'énergie au quotidien",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text(
        "Quels sont les verbes qui vous mettent en mouvement ? Voici quelques exemples par catégorie :",
        config=TextConfig(spacing_after=0.3 * cm),
    )
    
    categories = [
        "• Organiser : Planifier, gérer, coordonner, structurer...",
        "• Communiquer : Transmettre, écouter, interviewer, rédiger...",
        "• Créer : Concevoir, imaginer, innover, adapter...",
        "• Aider : Conseiller, soigner, guider, éclairer...",
        "• Analyser : Rechercher, étudier, observer, évaluer...",
        "• Diriger : Décider, manager, piloter, entreprendre..."
    ]
    for cat in categories:
        layout.add_text(cat, config=TextConfig(font_size=10, style_choice="italic", color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.1 * cm))
    layout.y_cursor -= 0.2 * cm

    layout.add_question_block(
        "1. Les verbes que je préfère (Ceux que j'aime conjuguer au quotidien) :",
        "verbes_q1",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "2. Les verbes que j'aime le moins (Ceux qui m'épuisent) :",
        "verbes_q2",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Analyse : Quel lien faites-vous avec vos expériences passées et votre profil MBTI ?",
        "verbes_q3",
        config=QuestionConfig(box_height=3.0 * cm),
    )

    layout.render()
