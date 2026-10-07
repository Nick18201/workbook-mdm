from workbook_generator.components import create_standard_engagement_page


def create_livrable_page(c):
    """End of the workbook: the deliverable validated in session, and the commitments."""
    create_standard_engagement_page(
        c,
        "Fin de carnet",
        custom_lines=[
            "Je réponds à partir de situations vécues, pas de ce que j'aimerais être.",
            "Je note les exemples qui me reviennent entre deux séances.",
            "J'apporte ce carnet rempli à la séance de restitution.",
        ],
        livrable_title="Votre mode d'emploi",
        livrable_text="Vos réponses sur l'énergie, l'information, les décisions et l'action, qui préparent la "
                      "restitution de votre profil MBTI® en séance.",
        field_prefix="livrable_chap3",
    )
