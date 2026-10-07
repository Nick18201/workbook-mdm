from workbook_generator.components import create_standard_engagement_page


def create_livrable_page(c):
    """End of the workbook: the deliverable validated in session, and the commitments."""
    create_standard_engagement_page(
        c,
        "Fin de carnet",
        custom_lines=[
            "Je réserve chaque semaine les heures que j'ai décidé d'investir.",
            "Je réponds sans me censurer : le tri se fait en séance.",
            "J'apporte ce carnet à chaque séance.",
        ],
        livrable_title="Votre engagement et votre point de départ",
        livrable_text="Votre engagement, votre situation actuelle et vos domaines de vie, relus ensemble en séance.",
        field_prefix="livrable_chap0",
    )
