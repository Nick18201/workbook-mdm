from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)


def create_boussole_regard_page(c):
    """
    P6.1 : MON REGARD SUR DEMAIN & MES ZONES DE LIBERTÉ (Anticipation & Pouvoir de choix).
    """
    layout = PageLayout(
        c,
        "P6.1 : REGARD SUR DEMAIN & MES CHOIX",
        config=LayoutConfig(part_title="6. MA BOUSSOLE DE PROJECTION"),
    )

    layout.add_text(
        "Construire sa trajectoire, c'est d'abord lever les yeux du guidon, observer ce qui bouge "
        "dans le monde du travail et reprendre le volant de ses décisions personnelles au lieu de subir "
        "passivement les événements.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "Ce qui m'appelle dans l'Avenir (Mon Regard)",
        "livret_p6_regard",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Quelles évolutions sociétales, écologiques ou techniques résonnent avec vos valeurs "
            "et vous donnent envie de participer et d'agir ?",
            example="Ex : La transition énergétique des territoires, la transmission des savoirs aux bâtisseurs, la sobriété d'usage.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Ce que je décide Moi-Même (Mon Pouvoir de Choix)",
        "livret_p6_choix",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Quelles décisions sur votre vie professionnelle et votre équilibre personnel vous appartiennent en propre "
            "et ne dépendent que de vous ?",
            example="Ex : Fixer ma limite stricte de temps de trajet, décider de mon niveau d'implication, refuser un management désincarné.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()


def create_boussole_confiance_page(c):
    """
    P6.2 : CURIOSITÉS D'EXPLORATION & CONFIANCE (Enquêtes et Réussites d'ancrage).
    """
    layout = PageLayout(
        c,
        "P6.2 : CURIOSITÉS & SOCLE DE CONFIANCE",
        config=LayoutConfig(part_title="6. MA BOUSSOLE DE PROJECTION"),
    )

    layout.add_text(
        "Pour s'orienter sans angoisse, il faut mener des enquêtes simples sur le terrain et se rappeler "
        "que vous avez déjà surmonté des transitions ou des apprentissages difficiles par le passé.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "Ce que j'ai Envie d'Explorer (Mes Curiosités Métiers)",
        "livret_p6_curiosite",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Quels métiers, structures ou professionnels en poste avez-vous envie d'interviewer "
            "pour découvrir la réalité concrète de leur quotidien ?",
            example="Ex : Solliciter un formateur technique en CFA et un chargé de mission énergie en collectivité pour 20 minutes d'échange.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Mes Victoires Passées (Mon Socle de Confiance)",
        "livret_p6_confiance",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Sur quelle difficulté, reconversion ou étape antérieure déjà traversée avec succès vous appuyez-vous aujourd'hui ?",
            example="Ex : Avoir validé un diplôme d'ingénieur après un BTS en apprenant tout sur le tas avec discipline et méthode.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()
