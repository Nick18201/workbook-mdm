from reportlab.lib.units import cm

from workbook_generator.primitives import pastel_cycle
from workbook_generator.templates import PageLayout, LayoutConfig, QuestionItem


def _situations(c, title, eyebrow, intro, situation_label, analysis_label, prefix, synthesis):
    """Three situation sheets (context, analysis), then the values they reveal."""
    layout = PageLayout(c, title, config=LayoutConfig(part_title=eyebrow))
    layout.add_paragraphs(intro, spacing_after=0.45 * cm)
    pastels = pastel_cycle(c)
    for i in range(1, 4):
        layout.add_fields_card(
            [
                [(situation_label, f"{prefix}_sit{i}_desc", 2.2)],
                [(analysis_label, f"{prefix}_sit{i}_analyse", 3.0)],
            ],
            title=f"Situation {i}",
            color=pastels[(i - 1) % 2],
        )
    layout.add_questions_group([QuestionItem(synthesis[0], synthesis[1])], max_box_height=4.0 * cm)
    layout.render()


def create_alignement_pages(c):
    """Exercise 1: three situations where you felt in the right place."""
    _situations(
        c, "Vos expériences *d'alignement.*", "Exercice 1 · Alignement · 10 min",
        [
            "Identifiez les situations où vous vous êtes senti·e à votre place.",
            "Repensez à trois situations (professionnelles, scolaires, associatives, personnelles) où vous étiez "
            "particulièrement aligné·e.",
        ],
        "Le contexte : quoi, qui, où",
        "Ce qui vous donnait de l'énergie, ce que vous apportiez, la valeur respectée",
        "align",
        ("Synthèse : les valeurs que révèlent ces trois situations", "align_valeurs_revelees"),
    )


def create_desalignement_pages(c):
    """Exercise 2: three situations of frustration or inner conflict."""
    _situations(
        c, "Vos expériences *de désalignement.*", "Exercice 2 · Désalignement · 10 min",
        [
            "Comprenez quelle valeur importante a été ignorée ou bafouée dans des moments difficiles.",
            "Repensez à trois situations où vous vous êtes senti·e en difficulté, frustré·e, vidé·e ou en conflit "
            "intérieur.",
        ],
        "La situation de désalignement",
        "Ce qui vous a dérangé, la limite franchie, la valeur absente ou bafouée",
        "desalign",
        ("Synthèse : les valeurs absentes, empêchées ou bafouées", "desalign_valeurs_revelees"),
    )


def create_choix_difficiles_page(c):
    """Exercise 3: two difficult choices and the values in conflict."""
    layout = PageLayout(c, "Vos choix *difficiles.*", config=LayoutConfig(part_title="Exercice 3 · Choix difficiles · 10 min"))
    layout.add_paragraphs([
        "Les valeurs apparaissent dans les choix difficiles, parce que choisir, c'est renoncer. Repensez à deux "
        "choix complexes (rester ou partir, sécurité ou risque…).",
    ], spacing_after=0.45 * cm)
    pastels = pastel_cycle(c)
    for i in (1, 2):
        layout.add_fields_card(
            [
                [("La situation", f"choix{i}_desc", 1.5)],
                [("Ce que l'option A et l'option B permettaient chacune de préserver", f"choix{i}_options", 1.5)],
                [("Ce que vous avez choisi, ce que cela a coûté et permis de respecter", f"choix{i}_resolution", 1.5)],
                [("Les valeurs en conflit", f"choix{i}_valeurs", 1.0)],
            ],
            title=f"Choix difficile {i}",
            color=pastels[(i - 1) % 2],
        )
    layout.render()

