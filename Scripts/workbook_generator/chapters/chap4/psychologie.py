from reportlab.lib.units import cm

from ...templates import PageLayout, LayoutConfig, QuestionItem


def create_situation_actuelle_page(c):
    """Exercise 2: the current financial situation."""
    layout = PageLayout(c, "Votre situation *actuelle.*", config=LayoutConfig(part_title="Exercice 2 · Situation actuelle"))
    layout.add_paragraphs(["Commencez par observer votre situation actuelle, simplement et concrètement."],
                          spacing_after=0.45 * cm)
    layout.add_questions_group([
        QuestionItem("Aujourd'hui, vous sentez-vous plutôt en sécurité, en tension ou en vigilance financière ?", "v2_sit_1"),
        QuestionItem("Votre situation économique vous laisse-t-elle une marge de manœuvre pour évoluer "
                     "professionnellement, ou vous donne-t-elle le sentiment d'être contraint·e ?", "v2_sit_2"),
        QuestionItem("Quel niveau de sécurité financière vous semble nécessaire pour envisager un changement ?", "v2_sit_3"),
    ])
    layout.render()


def create_histoire_argent_page(c):
    """Exercise 3: the history with money, then money, gender and roles."""
    layout = PageLayout(c, "Votre histoire *avec l'argent.*", config=LayoutConfig(part_title="Exercice 3 · Histoire"))
    layout.add_paragraphs([
        "Votre rapport à l'argent s'est construit à partir de votre histoire familiale, sociale et personnelle.",
    ], spacing_after=0.45 * cm)
    layout.add_questions_group([
        QuestionItem("Dans quel environnement économique avez-vous grandi ?", "v2_hist_1"),
        QuestionItem("Dans votre famille, l'argent était-il associé à la sécurité, au stress, à la réussite, au mérite, "
                     "au conflit, au plaisir ou à la liberté ? Était-ce un sujet tabou ?", "v2_hist_2"),
        QuestionItem("Qui gagnait, gérait et décidait de l'argent ? Avez-vous grandi avec le sentiment d'avoir assez, "
                     "pas assez, ou de devoir faire attention ?", "v2_hist_3"),
        QuestionItem("Avez-vous observé de grandes différences de moyens dans votre entourage ? Ont-elles créé de la "
                     "gêne, de l'envie, de la culpabilité ou un besoin de réussir ?", "v2_hist_4"),
    ])
    layout.page_break()
    layout.add_heading("Argent, genre et rapports femmes-hommes")
    layout.add_questions_group([
        QuestionItem("Avez-vous observé des rapports d'autonomie ou de dépendance financière, notamment entre femmes "
                     "et hommes ? Avaient-ils la même liberté financière ?", "v2_hist_genre_1"),
        QuestionItem("Avez-vous reçu, directement ou non, des messages différents sur ce qu'une femme ou un homme "
                     "pouvait attendre, demander, gagner ou dépenser ?", "v2_hist_genre_2"),
        QuestionItem("Avez-vous observé des situations où l'argent créait un rapport de pouvoir, de protection, de "
                     "contrôle ou de dépendance dans le couple ou la famille ?", "v2_hist_genre_3"),
    ])
    layout.render()


def create_premieres_experiences_page(c):
    """Exercise 4: the first experiences with money, and common received ideas."""
    layout = PageLayout(c, "Vos premières expériences *financières.*",
                        config=LayoutConfig(part_title="Exercice 4 · Premières expériences"))
    layout.add_paragraphs([
        "Certaines premières expériences laissent une empreinte durable sur la manière de gagner, dépenser, "
        "demander ou sécuriser l'argent.",
    ], spacing_after=0.45 * cm)
    layout.add_callout(
        "« Il faut travailler dur pour mériter son argent. » « Il ne faut dépendre de personne. » « L'argent crée "
        "des conflits. » « Je dois assurer pour les autres. » « Je ne suis pas légitime à demander plus. »",
        title="Idées reçues fréquentes",
        variant="quote",
    )
    layout.add_questions_group([
        QuestionItem("Avez-vous reçu de l'argent de poche ? Si oui, comment l'utilisiez-vous ? Était-il donné "
                     "librement, ou fallait-il le mériter ?", "v2_exp_1"),
        QuestionItem("Quand avez-vous commencé à gagner de l'argent par vous-même ? Que représentait ce premier "
                     "argent : liberté, fierté, sécurité, nécessité, obligation ?", "v2_exp_2"),
        QuestionItem("Aviez-vous plutôt tendance à dépenser, économiser, partager, cacher ou offrir ?", "v2_exp_3"),
        QuestionItem("Avez-vous un souvenir marquant lié à l'argent : manque, réussite, comparaison, conflit, honte, "
                     "dépendance, fierté ?", "v2_exp_4"),
    ])
    layout.render()
