from workbook_generator.components import (
    create_cover_page,
    create_standard_recap_page,
    create_standard_summary_page,
)


def create_chap4_v2_cover(c):
    """Cover of chapter 4: Mon rapport à l'argent."""
    create_cover_page(c, "Mon rapport *à l'argent.*", number=4, tagline="Bilan de compétences",
                      promise="Un salaire et un rythme de vie sécurisés.")


def create_concept_page(c):
    """Chapter opener: the objective of the workbook and its exercises."""
    intro_txt = (
        "Ce carnet repère comment votre rapport à l'argent influence vos choix professionnels : besoin de "
        "sécurité, prise de risque, rémunération, négociation, ambition, liberté, peur du manque, légitimité. "
        "Il ne s'agit pas d'analyser votre gestion financière, mais d'identifier ce qui peut soutenir ou freiner "
        "votre projet."
    )
    exercises = [
        "Exercice 1 · Récapitulatif : votre profil MBTI®.",
        "Exercice 2 · Votre situation actuelle.",
        "Exercice 3 · Votre histoire avec l'argent.",
        "Exercice 4 · Vos premières expériences financières.",
        "Exercice 5 · Argent et projet professionnel.",
        "Exercice 6 · Votre minimum financier acceptable.",
        "Exercice 7 · Ce que l'argent représente pour vous : huit tendances.",
        "Exercice 8 · Synthèse.",
    ]
    create_standard_summary_page(c, "4", "Ce que l'argent *pèse dans vos choix.*", intro_txt, exercises)


def create_recap_seance_page(c):
    """Exercise 1: back on the MBTI® profile presented in the previous session."""
    intro_txt = (
        "Revenez sur la restitution de votre profil MBTI® lors de la dernière séance, pour consolider ce que vous "
        "en retenez avant d'explorer votre rapport à l'argent."
    )
    questions = [
        "Dans quelles forces naturelles de votre profil MBTI® vous reconnaissez-vous le plus ?",
        "Comment ce mode de fonctionnement (énergie, information, décision, action) se voit-il dans votre quotidien ?",
        "En quoi la compréhension de votre profil change-t-elle votre regard sur vous-même ou sur vos relations ?",
    ]
    create_standard_recap_page(c, "Exercice 1 · Récapitulatif MBTI®", intro_txt, questions)
