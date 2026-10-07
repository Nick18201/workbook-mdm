from reportlab.lib.units import cm

from workbook_generator.templates import PageLayout, LayoutConfig, QuestionItem

# Each scenario: (number and name, situation, field id)
_ENERGIE = [
    ("1. Le vendredi soir",
     "La semaine a été intense, pleine d'imprévus et d'échanges. Votre « batterie sociale » est à plat. Décrivez "
     "la soirée ou le week-end idéal qui vous permettra d'être en forme lundi matin.", "mbti_q1"),
    ("2. L'interruption",
     "Vous êtes plongé·e dans une tâche qui demande de la concentration. Quelqu'un entre pour vous poser une "
     "question anodine. Décrivez votre réaction intérieure (agacement, soulagement, fil de pensée rompu ?) et "
     "ce que vous faites.", "mbti_q2"),
    ("3. Le processus de pensée",
     "Face à un problème complexe et nouveau, avez-vous besoin d'en parler à voix haute pour mettre vos idées en "
     "place, ou de vous isoler dans le silence pour structurer votre pensée avant d'en discuter ? Racontez une "
     "fois où vous avez dû faire l'inverse.", "mbti_q3"),
]
_INFORMATION = [
    ("4. L'exercice de l'objet",
     "Choisissez un objet du quotidien près de vous (une table, une tasse, un stylo). Décrivez-le en 4 ou 5 "
     "phrases : ce que vous voyez, à quoi il sert, ce qu'il vous évoque. Écrivez tout ce qui vous passe par la "
     "tête en le regardant.", "mbti_q4"),
    ("5. Le grand saut",
     "On vous demande une tâche manuelle ou technique que vous n'avez jamais faite (monter un meuble complexe, "
     "cuisiner un plat étranger, utiliser un nouveau logiciel). Quel est votre premier réflexe ? Qu'est-ce qui "
     "vous frustre le plus dans l'apprentissage ?", "mbti_q5"),
    ("6. La conversation ennuyeuse",
     "Pensez à une discussion, lors d'un repas, qui vous a profondément ennuyé·e ou fait « décrocher ». De quoi "
     "parlaient les gens ?", "mbti_q6"),
    ("7. La machine à voyager dans le temps",
     "Projetez-vous dans 5 ans, dans votre vie idéale. Pas seulement un titre de poste : décrivez l'ambiance de "
     "votre journée. Qu'est-ce qui vous rend fier ou fière ?", "mbti_q7"),
]
_DECISIONS = [
    ("8. Le choix difficile",
     "Vous organisez un événement aux places très limitées et devez exclure une personne de votre cercle, "
     "professionnel ou personnel. Comment prenez-vous la décision ? Décrivez votre malaise face à ce choix.",
     "mbti_q8"),
    ("9. Le cadeau embarrassant",
     "Une personne très proche vous offre un vêtement que vous trouvez vraiment laid, et vous demande avec "
     "enthousiasme s'il vous plaît. Que répondez-vous spontanément, et pourquoi ? Qu'est-ce qui compte le plus "
     "pour vous ?", "mbti_q9"),
    ("10. L'arbitre",
     "Deux collègues ou amis se disputent violemment, l'ambiance est gâchée. Qu'est-ce qui vous dérange le plus ? "
     "Comment intervenez-vous ?", "mbti_q10"),
    ("11. La critique",
     "Pensez à la dernière critique qui vous a blessé·e. Qu'est-ce qui a été le plus dur à accepter ?", "mbti_q11"),
]
_TEMPS = [
    ("12. La page blanche",
     "Vous vous réveillez un samedi matin sans rien de prévu pour les deux prochains jours. Que ressentez-vous ?",
     "mbti_q12"),
    ("13. L'adrénaline de l'échéance",
     "Pensez à un projet important à rendre à une date précise. De quoi avez-vous besoin pour être efficace ?",
     "mbti_q13"),
    ("14. L'organisation des vacances",
     "Vous partez deux semaines à l'étranger. Jusqu'où votre voyage est-il préparé ? Si un événement annule le "
     "programme de la journée, est-ce stimulant ou profondément agaçant ?", "mbti_q14"),
    ("15. Conclure ou explorer",
     "Qu'est-ce qui vous satisfait le plus : le moment où l'on cherche des idées et ouvre toutes les "
     "possibilités, ou le moment où l'on tranche, ferme les dossiers et raye les tâches de la liste ?", "mbti_q15"),
]
_OMBRE = [
    ("16. Le point de rupture",
     "Chacun a un « mauvais côté » sous l'effet d'un stress extrême ou d'une grande fatigue. À quoi "
     "ressemblez-vous dans ces moments-là ? Tyrannique et cassant·e ? Très émotif·ve et susceptible ? Obsédé·e "
     "par des détails ? Impulsif·ve et imprudent·e ?", "mbti_q16"),
    ("17. L'insomnie (bonus)",
     "Il est 3 heures du matin, vous n'arrivez pas à dormir : votre cerveau tourne à plein régime. Sur quoi "
     "boucle-t-il ?", "mbti_q17"),
]


def _questions_pages(c, title, eyebrow, intro, questions, per_page):
    """One exercise: its intro, then the scenarios, per_page per page, boxes sharing the height."""
    layout = PageLayout(c, title, config=LayoutConfig(part_title=eyebrow))
    layout.add_paragraphs([intro], spacing_after=0.4 * cm)
    items = [QuestionItem(name, field_id, subtitle=situation) for name, situation, field_id in questions]
    for start in range(0, len(items), per_page):
        if start:
            layout.page_break()
        layout.add_questions_group(items[start:start + per_page])
    layout.render()


def create_chap1_energie(c):
    _questions_pages(c, "Votre énergie *et votre environnement.*", "Exercice 2 · Énergie",
                     "Comment vous vous rechargez, et comment vous traitez l'information immédiate.", _ENERGIE, 3)


def create_chap2_information(c):
    _questions_pages(c, "Votre regard *sur le réel.*", "Exercice 3 · Information",
                     "Ce que votre cerveau remarque en premier, et comment il apprend.", _INFORMATION, 2)


def create_chap3_decisions(c):
    _questions_pages(c, "Vos *décisions.*", "Exercice 4 · Décisions",
                     "Vos critères pour trancher et juger une situation.", _DECISIONS, 2)


def create_chap4_temps(c):
    _questions_pages(c, "Votre rapport au temps *et à l'action.*", "Exercice 5 · Temps et action",
                     "Votre besoin de structure face à l'inconnu.", _TEMPS, 2)


def create_chap5_ombre(c):
    _questions_pages(c, "Votre zone *d'ombre.*", "Exercice 6 · Zone d'ombre",
                     "Comment vous réagissez quand vous êtes poussé·e dans vos retranchements.", _OMBRE, 2)
