from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)


def create_recit_contexte_page(c):
    """
    P5.1 : ARRÊT SUR IMAGE - LE DÉCOR, LA DIFFICULTÉ & LE DÉCLIC (Situation & Observation).
    """
    layout = PageLayout(
        c,
        "P5.1 : ARRÊT SUR IMAGE (DÉCOR & DÉCLIC)",
        config=LayoutConfig(part_title="5. ARRÊT SUR IMAGE (RÉCIT D'ACTION)"),
    )

    layout.add_text(
        "Pour ancrer la confiance en sa valeur, rien ne remplace le souvenir d'un moment réel où votre intervention "
        "a fait la différence. Choisissez une situation vécue (même simple ou modeste) où un imprévu ou un problème "
        "s'est posé, et où vous avez su agir avec pertinence.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "1. La Situation de Départ & le Défi Inattendu",
        "livret_p5_situation",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Où étiez-vous ? Quelle était la mission initiale, et quel obstacle, anomalie ou urgence est survenu ?",
            example="Ex : Bloqué sur un dossier complexe à 48h de l'échéance finale avec un calcul non-conforme et un client sous pression.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "2. Le Déclic & ce que vous avez Observé",
        "livret_p5_declic",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="À quel micro-signal précis (un chiffre anormal, une hésitation, un détail matériel) "
            "avez-vous compris qu'il fallait intervenir sans attendre ?",
            example="Ex : En lisant les plans de structure, j'ai repéré immédiatement un pont thermique oublié que personne n'avait décelé.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()


def create_recit_impact_page(c):
    """
    P5.2 : ARRÊT SUR IMAGE - MES ACTIONS & MA FIERTÉ (Actions & Résultats).
    """
    layout = PageLayout(
        c,
        "P5.2 : MES ACTIONS PAS À PAS & MA FIERTÉ",
        config=LayoutConfig(part_title="5. ARRÊT SUR IMAGE (RÉCIT D'ACTION)"),
    )

    layout.add_text(
        "Ce qui fait votre compétence réelle, ce ne sont pas de grands concepts abstraits, mais la suite précise "
        "de vos gestes, de vos décisions et de vos paroles. Décrivez la scène comme si vous revoyiez un film au ralenti.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "3. Ce que VOUS avez fait Pas à Pas (Actions & Choix)",
        "livret_p5_action",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Qu'avez-vous fait concrètement ? (Vos gestes, arbitrages, paroles, outils ou personnes mobilisés). "
            "Privilégiez le « Comment » plutôt que la théorie.",
            example="Ex : J'ai isolé les variables critiques, appelé le projeteur pour convenir d'une variante et rédigé une note technique vulgarisée.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "4. L'Impact Positif & votre Sentiment de Fierté",
        "livret_p5_resultat",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Quels ont été les effets concrets et mesurables pour le projet, le client ou l'équipe ? "
            "De quoi êtes-vous le plus fier dans votre réaction ?",
            example="Ex : Dossier validé dans les délais sans surcoût, client rassuré et reconnaissant, fierté d'avoir trouvé une solution élégante.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()
