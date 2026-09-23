from reportlab.lib.units import cm
from workbook_generator.templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig


def create_chap1_energie(c):
    # Questions 1-3
    layout = PageLayout(
        c,
        "Mon Énergie et mon Environnement",
        config=LayoutConfig(part_title="3. MON ÉNERGIE"),
    )
    layout.add_text(
        "Ce chapitre explore comment vous vous rechargez et comment vous traitez l'information immédiate.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout.add_question_block(
        "1. Le vendredi soir : La semaine a été intense, remplie d'imprévus et d'interactions. Votre 'batterie sociale' est à plat. Décrivez la soirée ou le week-end idéal qui vous permettra d'être à 100% lundi matin. ",
        "mbti_q1",
        config=QuestionConfig(box_height=3.6 * cm),
    )

    layout.add_question_block(
        "2. L'interruption : Vous êtes plongé(e) dans une tâche qui demande de la concentration. Quelqu'un entre pour vous poser une question anodine. Décrivez votre réaction intérieure (agacement, soulagement, rupture du fil de pensée ?) et comment vous gérez la situation à l'extérieur.",
        "mbti_q2",
        config=QuestionConfig(box_height=3.6 * cm),
    )

    layout.add_question_block(
        "3. Le processus de pensée : Face à un problème complexe et nouveau, avez-vous instinctivement besoin d'en parler à voix haute avec quelqu'un pour que vos idées se mettent en place, ou avez-vous un besoin vital de vous isoler dans le silence pour structurer votre pensée avant d'en discuter ? Racontez une fois où vous avez dû faire l'inverse.",
        "mbti_q3",
        config=QuestionConfig(box_height=3.6 * cm),
    )

    layout.render()


def create_chap2_information(c):
    # Questions 4-7 sur deux pages (4-5 puis 6-7)
    layout1 = PageLayout(
        c,
        "Mon Regard sur le Réel (L'Information) - 1/2",
        config=LayoutConfig(part_title="4. LE RÉEL"),
    )
    layout1.add_text(
        "Ce chapitre explore ce que votre cerveau remarque en premier et comment il apprend.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout1.add_question_block(
        "4. L'exercice de l'objet : Choisissez un objet du quotidien près de vous (une table, une tasse, un stylo). Décrivez-le-moi en 4 ou 5 phrases. Laissez libre cours à vos pensées : que voyez-vous, à quoi sert-il, que vous évoque-t-il ? (Écrivez vraiment tout ce qui vous passe par la tête en le regardant).",
        "mbti_q4",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout1.add_question_block(
        "5. Le grand saut : On vous demande de réaliser une tâche manuelle ou technique que vous n'avez jamais faite (monter un meuble complexe, cuisiner un plat étranger, utiliser un nouveau logiciel). Quel est votre premier réflexe ? Qu'est-ce qui vous frustre le plus dans l'apprentissage ?",
        "mbti_q5",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout1.render()

    layout2 = PageLayout(
        c,
        "Mon Regard sur le Réel (L'Information) - 2/2",
        config=LayoutConfig(part_title="4. LE RÉEL"),
    )
    layout2.add_question_block(
        "6. La conversation ennuyeuse : Pensez à une discussion lors d'un repas qui vous a profondément ennuyé(e) ou fait 'décrocher' mentalement. De quoi parlaient les gens ?",
        "mbti_q6",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout2.add_question_block(
        "7. La machine à voyager dans le temps : Projetez-vous dans 5 ans, dans votre vie idéale. Ne me donnez pas juste un titre de poste : décrivez-moi l'ambiance de votre journée. Qu'est-ce qui vous rend fier(e) ?",
        "mbti_q7",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout2.render()


def create_chap3_decisions(c):
    # Questions 8-11
    layout1 = PageLayout(
        c,
        "Ma Boussole Intérieure (Les Décisions) - 1/2",
        config=LayoutConfig(part_title="5. MES DÉCISIONS"),
    )
    layout1.add_text(
        "Ce chapitre explore vos critères pour trancher et juger une situation.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout1.add_question_block(
        "8. Le choix difficile : Vous devez organiser un événement avec des places très limitées. Vous devez exclure une personne de votre cercle (pro ou perso). Comment prenez-vous la décision ? Décrivez votre malaise intérieur face à ce choix.",
        "mbti_q8",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout1.add_question_block(
        "9. Le cadeau embarrassant : Un(e) ami(e) très proche vous offre un vêtement que vous trouvez vraiment laid. Il/elle vous demande avec enthousiasme si vous l'aimez. Que répondez-vous spontanément et pourquoi ? Qu'est-ce qui est le plus important pour vous ?",
        "mbti_q9",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout1.render()

    layout2 = PageLayout(
        c,
        "Ma Boussole Intérieure (Les Décisions) - 2/2",
        config=LayoutConfig(part_title="5. MES DÉCISIONS"),
    )
    layout2.add_question_block(
        "10. L'arbitre : Deux collègues ou amis se disputent violemment. L'ambiance est gâchée. Qu'est-ce qui vous dérange le plus ? Comment intervenez-vous ?",
        "mbti_q10",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout2.add_question_block(
        "11. La critique : Pensez à la dernière fois qu'on vous a fait une critique qui vous a blessé(e). Qu'est-ce qui a été le plus dur à avaler ?",
        "mbti_q11",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout2.render()


def create_chap4_temps(c):
    # Questions 12-15
    layout1 = PageLayout(
        c,
        "Mon Rapport au Temps et à l'Action - 1/2",
        config=LayoutConfig(part_title="6. MON ACTION"),
    )
    layout1.add_text(
        "Ce chapitre explore votre besoin de structure face à l'inconnu.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout1.add_question_block(
        "12. La page blanche : Vous vous réveillez un samedi matin avec absolument rien de prévu pour les deux prochains jours. Que ressentez vous ?",
        "mbti_q12",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout1.add_question_block(
        "13. L'adrénaline de la limite : Pensez à un projet important que vous deviez rendre à une date précise. De quoi avez vous besoin pour être efficace ?",
        "mbti_q13",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout1.render()

    layout2 = PageLayout(
        c,
        "Mon Rapport au Temps et à l'Action - 2/2",
        config=LayoutConfig(part_title="6. MON ACTION"),
    )
    layout2.add_question_block(
        "14. L'organisation des vacances : Vous partez deux semaines à l'étranger. À quel point votre voyage est-il préparé ? Si un événement annule votre programme de la journée, trouvez-vous cela excitant ou profondément agaçant ?",
        "mbti_q14",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout2.add_question_block(
        "15. La conclusion vs L'exploration : Qu'est-ce qui vous donne le plus de satisfaction : le moment où l'on brainstorme, ouvre toutes les possibilités et découvre de nouvelles idées, ou le moment où l'on tranche, ferme les dossiers et raye les tâches de la 'To-Do list' ?",
        "mbti_q15",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout2.render()


def create_chap5_ombre(c):
    # Questions 16-17
    layout = PageLayout(
        c, "Ma Zone d'Ombre", config=LayoutConfig(part_title="7. MA ZONE D'OMBRE")
    )
    layout.add_text(
        "Ce chapitre explore comment vous réagissez quand vous êtes poussé(e) dans vos retranchements.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout.add_question_block(
        "16. Le point de rupture : Tout le monde a un 'mauvais côté' quand il est sous l'emprise d'un stress extrême ou d'une immense fatigue. Racontez-moi à quoi vous ressemblez dans ces moments-là. Devenez-vous tyrannique et cassant ? Hyper-émotif(ve) et susceptible ? Obsédé(e) par des détails insignifiants ? Ou impulsif(ve) et imprudent(e) ?",
        "mbti_q16",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout.add_question_block(
        "17. L'insomnie (Bonus) : Il est 3 heures du matin, vous n'arrivez pas à dormir car votre cerveau tourne à plein régime. Sur quoi boucle-t-il ?",
        "mbti_q17",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout.render()
