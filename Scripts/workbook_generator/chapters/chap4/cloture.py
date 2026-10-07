from ...components import create_standard_engagement_page
from ...templates import PageLayout, LayoutConfig, QuestionItem


def create_synthese_v2_page(c):
    """Exercise 8: synthesis."""
    layout = PageLayout(c, "Synthèse.", config=LayoutConfig(part_title="Exercice 8 · Synthèse"))
    layout.add_questions_group([
        QuestionItem("Si vous aviez plus d'argent, qu'est-ce que cela changerait vraiment pour vous ?", "v2_synth_1"),
        QuestionItem("Qu'est-ce qui vous fait le plus peur dans le manque d'argent ? Et qu'est-ce qui pourrait vous "
                     "mettre mal à l'aise dans le fait de gagner davantage ?", "v2_synth_2"),
        QuestionItem("À partir de quoi vous sentez-vous « assez » en sécurité ? Cet « assez » correspond-il à un chiffre "
                     "concret, ou plutôt à une sensation difficile à atteindre ?", "v2_synth_3"),
    ])
    layout.render()


def create_livrable_page(c):
    """End of the workbook: the deliverable validated in session, and the commitments."""
    create_standard_engagement_page(
        c,
        "Fin de carnet",
        custom_lines=[
            "Je garde mes seuils chiffrés en tête pour évaluer chaque piste.",
            "Je parle de rémunération sans m'en excuser.",
            "Je vérifie qu'une piste atteint mon minimum, tout de suite ou à moyen terme.",
        ],
        livrable_title="Vos seuils financiers",
        livrable_text="Votre minimum vital, votre revenu cible et ce que l'argent représente pour vous, validés en séance.",
        field_prefix="livrable_chap4",
    )
