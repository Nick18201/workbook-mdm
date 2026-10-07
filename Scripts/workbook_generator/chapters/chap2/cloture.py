from workbook_generator.components import create_standard_engagement_page
from workbook_generator.templates import PageLayout, LayoutConfig, QuestionItem


def create_interview_page(c):
    """Bonus: interview of someone whose job or life inspires you."""
    layout = PageLayout(c, "Interview d'une personne *passionnée.*", config=LayoutConfig(part_title="Bonus · Interview"))
    layout.add_paragraphs(["Rencontrez une personne dont le métier ou la vie vous inspire."])
    layout.add_fields_card([
        [("Personne interviewée", "interview_nom"), ("Son métier, son activité", "interview_metier")],
    ])
    layout.add_questions_group([
        QuestionItem("Qu'aimez-vous le plus dans ce que vous faites ?", "interview_q1"),
        QuestionItem("Quelles sont les difficultés ou les contraintes cachées ?", "interview_q2"),
        QuestionItem("Quel conseil donneriez-vous à quelqu'un qui veut se lancer ?", "interview_q3"),
        QuestionItem("Ce que j'en retiens pour moi :", "interview_q4"),
    ])
    layout.render()


def create_livrable_page(c):
    """End of the workbook: the deliverable validated in session, and the commitments."""
    create_standard_engagement_page(
        c,
        "Fin de carnet",
        custom_lines=[
            "Je reconnais la valeur de chacune de mes expériences, y compris les plus difficiles.",
            "Je garde mes moteurs en tête pour évaluer chaque piste.",
            "Je décide de mes prochains choix en connaissance de cause.",
        ],
        livrable_title="Votre fil rouge professionnel",
        livrable_text="Votre analyse de parcours, vos moteurs, votre ligne de vie et votre arbre de vie, validés en séance.",
        field_prefix="livrable_chap2",
    )
