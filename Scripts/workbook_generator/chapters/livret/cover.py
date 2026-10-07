from workbook_generator.components import create_cover_page


def create_livret_cover(c):
    """Cover of the skills booklet."""
    create_cover_page(
        c,
        "Votre portfolio *de compétences.*",
        eyebrow="Livret de compétences",
        tagline="Livret de compétences augmenté",
        promise="Vos compétences, prouvées par des faits.",
    )
