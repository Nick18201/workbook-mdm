from reportlab.lib.units import cm

from ...config import PDFStyle
from ...templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig


def create_situation_actuelle_page(c):
    layout = PageLayout(
        c,
        "Votre situation actuelle",
        config=LayoutConfig(part_title="1. VOTRE SITUATION ACTUELLE"),
    )
    layout.add_text(
        "Commencez par observer votre situation actuelle de manière simple et concrète.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    layout.add_question_block(
        "Aujourd'hui, vous sentez-vous plutôt en sécurité, en tension ou en vigilance financière ?",
        "v2_sit_1",
        config=QuestionConfig(box_height=4 * cm),
    )

    layout.add_question_block(
        "Votre situation économique vous laisse-t-elle une marge de manœuvre pour évoluer professionnellement, ou vous donne-t-elle le sentiment d'être contraint ?",
        "v2_sit_2",
        config=QuestionConfig(box_height=4 * cm),
    )

    layout.add_question_block(
        "Quel niveau de sécurité financière vous semble nécessaire pour envisager un changement ?",
        "v2_sit_3",
        config=QuestionConfig(box_height=4 * cm),
    )
    layout.render()


def create_histoire_argent_page(c):
    layout = PageLayout(
        c,
        "Votre histoire avec l'argent",
        config=LayoutConfig(part_title="2. VOTRE HISTOIRE AVEC L'ARGENT"),
    )
    layout.add_text(
        "Votre rapport à l'argent s'est construit à partir de votre histoire familiale, sociale et personnelle.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    layout.add_question_block(
        "Dans quel environnement économique avez-vous grandi ?",
        "v2_hist_1",
        config=QuestionConfig(box_height=3 * cm),
    )
    layout.add_question_block(
        "Dans votre famille, l'argent était-il associé à la sécurité, au stress, à la réussite, au mérite, au conflit, au plaisir ou à la liberté ? Était-ce un sujet tabou ?",
        "v2_hist_2",
        config=QuestionConfig(box_height=3 * cm),
    )
    layout.add_question_block(
        "Qui gagnait, gérait et décidait de l'argent ? Avez-vous grandi avec le sentiment d'avoir assez, pas assez, ou de devoir faire attention ?",
        "v2_hist_3",
        config=QuestionConfig(box_height=3 * cm),
    )
    layout.add_question_block(
        "Avez-vous observé des différences importantes de moyens dans votre entourage ? Ont-elles créé de la gêne, de l'envie, de la culpabilité ou un besoin de réussir ?",
        "v2_hist_4",
        config=QuestionConfig(box_height=3 * cm),
    )
    layout.render()

    # Page 2: Genre et rapports femmes-hommes
    layout2 = PageLayout(
        c,
        "Argent, genre et rapports femmes-hommes",
        config=LayoutConfig(part_title="2. VOTRE HISTOIRE AVEC L'ARGENT"),
    )
    layout2.add_question_block(
        "Avez-vous observé des rapports d'autonomie ou de dépendance financière, notamment entre femmes et hommes ? Avaient-ils la même liberté financière ?",
        "v2_hist_genre_1",
        config=QuestionConfig(box_height=4 * cm),
    )
    layout2.add_question_block(
        "Avez-vous reçu, directement ou indirectement, des messages différents sur ce qu'une femme ou un homme pouvait attendre, demander, gagner ou dépenser ?",
        "v2_hist_genre_2",
        config=QuestionConfig(box_height=4 * cm),
    )
    layout2.add_question_block(
        "Avez-vous observé des situations où l'argent créait un rapport de pouvoir, de protection, de contrôle ou de dépendance dans le couple ou la famille ?",
        "v2_hist_genre_3",
        config=QuestionConfig(box_height=4 * cm),
    )
    layout2.render()


def create_premieres_experiences_page(c):
    layout = PageLayout(
        c,
        "Vos premières expériences financières",
        config=LayoutConfig(part_title="3. VOS PREMIÈRES EXPÉRIENCES"),
    )
    layout.add_text(
        "Certaines premières expériences laissent une empreinte durable dans la manière de gagner, dépenser, demander ou sécuriser l'argent.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    layout.add_question_block(
        "Avez-vous reçu de l'argent de poche ? Si oui, comment l'utilisiez-vous ? Était-ce de l'argent donné librement ou fallait-il le mériter ?",
        "v2_exp_1",
        config=QuestionConfig(box_height=2.5 * cm),
    )
    layout.add_question_block(
        "Quand avez-vous commencé à gagner de l'argent par vous-même ? Que représentait ce premier argent gagné : liberté, fierté, sécurité, nécessité, obligation ?",
        "v2_exp_2",
        config=QuestionConfig(box_height=2.5 * cm),
    )
    layout.add_question_block(
        "Aviez-vous plutôt tendance à dépenser, économiser, partager, cacher ou offrir ?",
        "v2_exp_3",
        config=QuestionConfig(box_height=2.5 * cm),
    )
    layout.add_question_block(
        "Avez-vous un souvenir marquant lié à l'argent : manque, réussite, comparaison, conflit, honte, dépendance, fierté ?",
        "v2_exp_4",
        config=QuestionConfig(box_height=2.5 * cm),
    )

    layout.add_text(
        "Exemples de croyances possibles :",
        config=TextConfig(
            style_choice="subtitle",
            color=PDFStyle.COLOR_ACCENT_BLUE,
            spacing_after=0.1 * cm,
        ),
    )
    layout.add_text(
        "« Il faut travailler dur pour mériter son argent. » • « Il ne faut dépendre de personne. » • « L'argent crée des conflits. » • « Je dois assurer pour les autres. » • « Je ne suis pas légitime à demander plus. »",
        config=TextConfig(font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY),
    )
    layout.render()
