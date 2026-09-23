from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle
from workbook_generator.components import (
    create_standard_cover,
    create_standard_summary_page,
)
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig


def create_valeurs_cover(c):
    create_standard_cover(c, "CHAPITRE 5 : MES VALEURS ET MOTEURS PROFONDS")


def create_concept_page(c):
    points = [
        ("Sommaire :", ""),
        ("1.", "Mes Expériences d'Alignement"),
        ("2.", "Mes Expériences de Désalignement"),
        ("3.", "Mes Choix Difficiles"),
        ("4.", "Liste de Valeurs pour s'aider à nommer"),
        ("5.", "Hiérarchiser mes Valeurs"),
        ("6.", "Incarner ses Valeurs Non Négociables"),
        ("7.", "Traduire ses Valeurs en Conditions de Travail"),
        ("8.", "Mes Tensions de Valeurs"),
        ("9.", "Synthèse Finale"),
    ]
    create_standard_summary_page(c, "5", "VALEURS", "", points)


def create_intro_page(c):
    layout = PageLayout(
        c,
        "Comprendre ses valeurs",
        config=LayoutConfig(part_title="INTRODUCTION")
    )
    
    layout.add_text(
        "Ce workbook vous aide à identifier ce qui compte profondément pour vous dans votre vie professionnelle.",
        config=TextConfig(font_size=12, spacing_after=0.6 * cm, style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE)
    )
    
    layout.add_text(
        "Les valeurs ne sont pas seulement des idées abstraites. Elles se repèrent dans les situations où vous vous sentez :",
        config=TextConfig(font_size=11, spacing_after=0.4 * cm)
    )
    
    sentiments = [
        "• motivé(e) ;",
        "• fier(e) ;",
        "• utile ;",
        "• libre ;",
        "• reconnu(e) ;",
        "• en confiance ;"
    ]
    for s in sentiments:
        layout.add_text(
            s,
            config=TextConfig(font_size=11, spacing_after=0.2 * cm, color=PDFStyle.COLOR_ACCENT_RED, style_choice="subtitle")
        )
        
    layout.add_text(
        "mais aussi frustré(e), en colère, vidé(e), empêché(e) ou en conflit intérieur.",
        config=TextConfig(font_size=11, spacing_after=0.6 * cm)
    )
    
    layout.add_text(
        "L’objectif n’est pas de choisir les valeurs qui semblent les plus “belles” ou les plus attendues, mais d’identifier celles qui influencent réellement vos choix, votre énergie et votre rapport au travail.",
        config=TextConfig(font_size=11, spacing_after=0.5 * cm, style_choice="italic", color=PDFStyle.COLOR_TEXT_SECONDARY)
    )
    
    layout.render()
