from reportlab.lib.units import cm

from ...templates import PageLayout, LayoutConfig, QuestionItem


def create_argent_projet_pro_page(c):
    """Exercise 5: money and the professional project."""
    layout = PageLayout(c, "L'argent *et votre projet.*", config=LayoutConfig(part_title="Exercice 5 · Argent et projet"))
    layout.add_paragraphs([
        "Dans un bilan de compétences, l'enjeu est de comprendre comment l'argent influence vos choix professionnels.",
    ], spacing_after=0.45 * cm)
    layout.add_questions_group([
        QuestionItem("Votre revenu actuel vous semble-t-il cohérent avec votre contribution ? Vous sentez-vous "
                     "suffisamment reconnu·e financièrement ?", "v2_pro_1"),
        QuestionItem("Avez-vous déjà renoncé à une envie professionnelle pour des raisons financières ? Ou accepté un "
                     "poste surtout pour l'argent ?", "v2_pro_2"),
        QuestionItem("Avez-vous du mal à demander une augmentation, négocier, fixer un prix ou parler de "
                     "rémunération ? Associez-vous gagner de l'argent et beaucoup travailler ?", "v2_pro_3"),
    ])
    layout.page_break()
    layout.add_questions_group([
        QuestionItem("Votre besoin de sécurité entre-t-il parfois en tension avec votre besoin d'utilité, de liberté "
                     "ou d'évolution ?", "v2_pro_4"),
        QuestionItem("Votre genre, votre éducation ou votre histoire familiale influencent-ils votre manière de "
                     "demander, négocier, gagner ou assumer votre ambition financière ? Qu'est-ce que vous n'osez pas "
                     "demander, viser ou négocier aujourd'hui ?", "v2_pro_5"),
    ])
    layout.render()


def create_minimum_financier_page(c):
    """Exercise 6: the acceptable financial minimum, then the figures to keep."""
    layout = PageLayout(c, "Votre minimum *financier.*", config=LayoutConfig(part_title="Exercice 6 · Minimum financier"))
    layout.add_paragraphs([
        "Dans une réorientation, clarifiez le revenu en dessous duquel le projet deviendrait trop insécurisant ou "
        "difficile à tenir.",
    ], spacing_after=0.45 * cm)
    layout.add_questions_group([
        QuestionItem("Quel revenu mensuel minimum vous permettrait de couvrir vos charges essentielles ?", "v2_min_1"),
        QuestionItem("Quel montant vous permettrait de rester suffisamment serein·e pendant une transition ?", "v2_min_2"),
        QuestionItem("Quel revenu cible souhaitez-vous atteindre à terme ?", "v2_min_3"),
    ])
    layout.page_break()
    layout.add_questions_group([
        QuestionItem("Pendant combien de temps pourriez-vous accepter une baisse temporaire de revenus ?", "v2_min_4"),
        QuestionItem("Quelles concessions seraient acceptables, et lesquelles ne le seraient pas ?", "v2_min_5"),
        QuestionItem("Cette piste professionnelle permet-elle d'atteindre votre minimum financier, tout de suite ou à "
                     "moyen terme ?", "v2_min_6"),
    ])
    layout.render()

    layout = PageLayout(c, "Vos seuils *en chiffres.*", config=LayoutConfig(part_title="Exercice 6 · Minimum financier"))
    layout.add_paragraphs([
        "Reportez ici vos chiffres : ils serviront à évaluer chaque piste professionnelle.",
    ], spacing_after=0.45 * cm)
    layout.add_fields_card([
        [("Mon minimum vital mensuel", "v2_min_comp_1", 1.5), ("Mon minimum sécurisant mensuel", "v2_min_comp_2", 1.5)],
        [("Mon revenu cible", "v2_min_comp_3", 1.5), ("Durée acceptable d'une baisse de revenus", "v2_min_comp_4", 1.5)],
        [("Seuil en dessous duquel je ne souhaite pas descendre", "v2_min_comp_5", 1.5)],
    ], title="Mes seuils")
    layout.add_annotation("Un chiffre concret rassure plus qu'une impression.")
    layout.render()
