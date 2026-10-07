from workbook_generator.components import create_standard_engagement_page


def create_livrable_page(c):
    """End of the workbook: the deliverable validated in session, and the commitments."""
    create_standard_engagement_page(
        c,
        "Fin de carnet",
        custom_lines=[
            "Je garde mon objectif boussole sous les yeux.",
            "Je dépose ce qui ne m'appartient plus, et je le note quand cela revient.",
            "Je teste au moins une action concrète entre deux séances.",
        ],
        livrable_title="Votre état des lieux",
        livrable_text="Votre vision à 360°, votre objectif boussole et vos héritages, validés en séance.",
        field_prefix="livrable_chap1",
    )
