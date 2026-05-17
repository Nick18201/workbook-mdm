from reportlab.lib.units import cm

from ...config import PDFStyle
from ...templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig


def create_argent_projet_pro_page(c):
    # Page 1
    layout = PageLayout(
        c,
        "Argent et projet professionnel (1/2)",
        config=LayoutConfig(part_title="4. ARGENT ET PROJET PROFESSIONNEL"),
    )
    layout.add_text(
        "Dans un bilan de compétences, l'enjeu est surtout de comprendre comment l'argent influence vos choix professionnels.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    layout.add_question_block(
        "Votre revenu actuel vous semble-t-il cohérent avec votre contribution ? Vous sentez-vous suffisamment reconnu financièrement ?",
        "v2_pro_1",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout.add_question_block(
        "Avez-vous déjà renoncé à une envie professionnelle pour des raisons financières ? Ou accepté un poste principalement pour l'argent ?",
        "v2_pro_2",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout.add_question_block(
        "Avez-vous du mal à demander une augmentation, négocier, fixer un prix ou parler de rémunération ? Associez-vous le fait de gagner de l'argent au fait de beaucoup travailler ?",
        "v2_pro_3",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout.render()

    # Page 2
    layout2 = PageLayout(
        c,
        "Argent et projet professionnel (2/2)",
        config=LayoutConfig(part_title="4. ARGENT ET PROJET PROFESSIONNEL"),
    )
    layout2.add_question_block(
        "Votre besoin de sécurité est-il parfois en tension avec votre besoin de sens, de liberté ou d'évolution ?",
        "v2_pro_4",
        config=QuestionConfig(box_height=5.0 * cm),
    )
    layout2.add_question_block(
        "Votre genre, votre éducation ou votre histoire familiale influencent-ils votre manière de demander, négocier, gagner ou assumer votre ambition financière ? Qu'est-ce que vous n'osez pas demander, viser ou négocier aujourd'hui ?",
        "v2_pro_5",
        config=QuestionConfig(box_height=5.0 * cm),
    )
    layout2.render()


def create_minimum_financier_page(c):
    # Page 1
    layout = PageLayout(
        c,
        "Identifier votre minimum financier acceptable (1/3)",
        config=LayoutConfig(part_title="5. MINIMUM FINANCIER"),
    )
    layout.add_text(
        "Dans une réorientation, il est utile de clarifier le revenu minimum en dessous duquel le projet deviendrait trop insécurisant ou difficile à tenir.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    layout.add_question_block(
        "Quel revenu mensuel minimum vous permettrait de couvrir vos charges essentielles ?",
        "v2_min_1",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout.add_question_block(
        "Quel montant vous permettrait de rester suffisamment serein pendant une transition ?",
        "v2_min_2",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout.add_question_block(
        "Quel revenu cible souhaitez-vous atteindre à terme ?",
        "v2_min_3",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout.render()

    # Page 2
    layout2 = PageLayout(
        c,
        "Identifier votre minimum financier acceptable (2/3)",
        config=LayoutConfig(part_title="5. MINIMUM FINANCIER"),
    )
    layout2.add_question_block(
        "Pendant combien de temps pourriez-vous accepter une baisse temporaire de revenus ?",
        "v2_min_4",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout2.add_question_block(
        "Quelles concessions seraient acceptables, et lesquelles ne le seraient pas ?",
        "v2_min_5",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout2.add_question_block(
        "Cette piste professionnelle permet-elle d'atteindre votre minimum financier, immédiatement ou à moyen terme ?",
        "v2_min_6",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout2.render()

    # Page 3
    layout3 = PageLayout(
        c,
        "Identifier votre minimum financier acceptable (3/3)",
        config=LayoutConfig(part_title="5. MINIMUM FINANCIER"),
    )
    layout3.add_text(
        "À compléter :",
        config=TextConfig(
            style_choice="subtitle",
            font_size=11,
            color=PDFStyle.COLOR_ACCENT_BLUE,
            spacing_after=0.2 * cm,
        ),
    )
    layout3.add_question_block(
        "Mon minimum vital mensuel :",
        "v2_min_comp_1",
        config=QuestionConfig(box_height=2.0 * cm),
    )
    layout3.add_question_block(
        "Mon minimum sécurisant mensuel :",
        "v2_min_comp_2",
        config=QuestionConfig(box_height=2.0 * cm),
    )
    layout3.add_question_block(
        "Mon revenu cible :",
        "v2_min_comp_3",
        config=QuestionConfig(box_height=2.0 * cm),
    )
    layout3.add_question_block(
        "Durée acceptable d'une baisse de revenus :",
        "v2_min_comp_4",
        config=QuestionConfig(box_height=2.0 * cm),
    )
    layout3.add_question_block(
        "Seuil en dessous duquel je ne souhaite pas descendre :",
        "v2_min_comp_5",
        config=QuestionConfig(box_height=2.0 * cm),
    )
    layout3.render()
