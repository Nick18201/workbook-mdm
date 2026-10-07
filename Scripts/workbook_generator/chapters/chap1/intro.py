from workbook_generator.components import create_cover_page, create_standard_summary_page


def create_chap1_cover(c):
    """Cover of chapter 1: L'état des lieux."""
    create_cover_page(c, "L'état *des lieux.*", number=1, tagline="Bilan de compétences",
                      promise="Savoir d'où vous partez.")


def create_concept_page(c):
    """Chapter opener: the objective of the workbook and its exercises."""
    intro_txt = (
        "Ce carnet fixe votre point de départ : votre état d'esprit, l'équilibre de vos domaines de vie, "
        "l'objectif de votre bilan, et ce que vous avez reçu de votre milieu sur le travail. "
        "Il servira de référence pour mesurer le chemin parcouru."
    )
    exercises = [
        "Exercice 1 · Votre état d'esprit du moment.",
        "Exercice 2 · Votre vision à 360° : vos quatre domaines de vie.",
        "Exercice 3 · Votre objectif boussole : le cap prioritaire à 3 mois.",
        "Exercice 4 · Le sac à dos : ce que vous décidez de déposer.",
        "Exercice 5 · Votre héritage familial (matrice 3FVS).",
        "Exercice 6 · Votre image du travail, reçue et choisie.",
        "Exercice 7 · Vos mentors et vos anti-modèles.",
    ]
    create_standard_summary_page(c, "1", "Fixer votre point *de départ.*", intro_txt, exercises)
