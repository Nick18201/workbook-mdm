from reportlab.lib.units import cm

from workbook_generator.components import create_standard_engagement_page
from workbook_generator.primitives import pastel_cycle
from workbook_generator.templates import PageLayout, LayoutConfig

TENSIONS_LIST = [
    "Liberté / sécurité",
    "Réussite / équilibre",
    "Bienveillance / affirmation de soi",
    "Stimulation / stabilité",
    "Autonomie / appartenance",
    "Reconnaissance / discrétion",
    "Sens / rémunération",
    "Engagement / protection de soi",
    "Créativité / cadre",
    "Ambition / qualité de vie",
    "Loyauté / besoin de changement",
    "Responsabilité / légèreté",
]


def create_tensions_page(c):
    """Exercise 8: tick the tensions between values, then detail the two strongest."""
    layout = PageLayout(c, "Vos tensions *de valeurs.*", config=LayoutConfig(part_title="Exercice 8 · Tensions · 10 min"))
    layout.add_paragraphs([
        "Deux valeurs importantes pour vous peuvent entrer en contradiction. Cochez les tensions qui vous parlent, "
        "puis détaillez les deux plus présentes dans votre parcours.",
    ], spacing_after=0.45 * cm)
    layout.add_checklist_cards([("Tensions possibles", TENSIONS_LIST)], columns=1, field_prefix="tension_chk",
                               item_columns=3)
    pastels = pastel_cycle(c)
    for i in (1, 2):
        layout.add_fields_card(
            [
                [("Les deux valeurs en tension, et les situations où elle apparaît", f"tension{i}_situations", 1.5)],
                [("Arbitrage : la valeur que vous privilégiez, celle que vous sacrifiez", f"tension{i}_arbitrage", 1.5)],
                [("Équilibre : le compromis à rechercher", f"tension{i}_equilibre", 1.5)],
            ],
            title=f"Tension {i}",
            color=pastels[i % 2],
        )
    layout.render()


def create_synthese_page(c):
    """Exercise 9: sentences to complete, summing up what counts."""
    layout = PageLayout(c, "Synthèse.", config=LayoutConfig(part_title="Exercice 9 · Synthèse · 10 min"))
    layout.add_paragraphs([
        "Complétez ces phrases pour résumer ce qui compte vraiment pour vous. Elles guideront la suite de votre projet.",
    ], spacing_after=0.45 * cm)
    layout.add_fields_card(
        [
            [("Ce qui compte vraiment pour moi au travail, c'est :", "synthese_compte_travail", 1.2)],
            [("Je me sens aligné·e quand :", "synthese_aligne_quand", 1.2)],
            [("Je perds de l'énergie quand :", "synthese_perte_energie", 1.2)],
            [("Mes 3 valeurs non négociables sont :", "synthese_non_nego", 1.2)],
            [("Pour les respecter, j'ai besoin de :", "synthese_besoins_nego", 1.2)],
            [("Dans mon futur projet, je veux davantage :", "synthese_davantage", 1.2)],
            [("Dans mon futur projet, je veux moins :", "synthese_moins", 1.2)],
        ],
        question_labels=True,
    )
    layout.render()


def create_livrable_page(c):
    """End of the workbook: the deliverable validated in session, and the commitments."""
    create_standard_engagement_page(
        c,
        "Fin de carnet",
        custom_lines=[
            "J'évalue chaque piste à l'aune de mes 3 valeurs non négociables.",
            "Je repère les situations où l'une de mes valeurs est mise à mal.",
            "J'emporte ma liste de conditions de travail en entretien.",
        ],
        livrable_title="Vos valeurs non négociables",
        livrable_text="Vos 3 valeurs non négociables, traduites en conditions de travail, validées en séance.",
        field_prefix="livrable_chap5",
    )
