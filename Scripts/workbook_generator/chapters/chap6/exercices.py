from reportlab.lib.units import cm

from workbook_generator.primitives import pastel_cycle
from workbook_generator.templates import PageLayout, LayoutConfig, QuestionItem


def create_cartographie_page(c):
    """Exercise 2: one-page summary of what the bilan revealed."""
    layout = PageLayout(c, "Votre cartographie *personnelle.*",
                        config=LayoutConfig(part_title="Exercice 2 · Cartographie"))
    layout.add_paragraphs(["Résumez les éléments clés issus de vos séances de bilan."], spacing_after=0.45 * cm)
    layout.add_fields_card(
        [
            [("Type MBTI®", "carto_mbti", 0.85)],
            [("Ce que j'aime faire dans la vie", "carto_aime_faire", 4.2), ("Mes envies et objectifs", "carto_envies_objectifs", 4.2)],
            [("Mes points forts", "carto_points_forts", 4.2), ("Mes valeurs", "carto_valeurs", 4.2)],
            [("Mes besoins", "carto_besoins", 4.2), ("Mes sources de stress", "carto_stress", 4.2)],
        ],
        title="Ma cartographie",
    )
    layout.render()


def create_retours_proches_page(c):
    """Exercise 3: what your relatives suggest."""
    layout = PageLayout(c, "Le retour *de vos proches.*", config=LayoutConfig(part_title="Exercice 3 · Retour des proches"))
    layout.add_paragraphs([
        "Présentez votre cartographie à au moins 3 personnes de votre entourage, sans parler de vos pistes, et "
        "demandez-leur à quels métiers et secteurs elles pensent pour vous.",
    ], spacing_after=0.45 * cm)
    layout.add_questions_group([
        QuestionItem("Les secteurs et métiers suggérés par mes proches", "proches_suggestions"),
        QuestionItem("Ce que je pense de ces propositions", "proches_avis"),
        QuestionItem("Comment j'ai vécu cet exercice", "proches_vecu"),
    ])
    layout.render()


def create_pistes_intro_page(c):
    """Exercise 4: ten jobs to explore, five without limits and five realistic ones."""
    layout = PageLayout(c, "Dix métiers *à explorer.*", config=LayoutConfig(part_title="Exercice 4 · Pistes de métiers"))
    layout.add_paragraphs([
        "Pour avancer, notez 10 métiers en deux catégories : 5 pistes « no limit », sans tenir compte des "
        "contraintes, et 5 pistes réalistes, faisables concrètement aujourd'hui.",
    ], spacing_after=0.45 * cm)
    layout.add_numbered_lines(
        [
            ("5 métiers « no limit »", "index_piste_nl", "Sans tenir compte des contraintes"),
            ("5 métiers réalistes", "index_piste_r", "Concrètement faisables aujourd'hui"),
        ],
        count=5,
        line_height=1.2 * cm,
    )
    layout.add_annotation("Les pistes « no limit » disent souvent ce que vous cherchez vraiment.")
    layout.render()


def _fiches_pages(c, title, eyebrow, intro, prefix, kind):
    layout = PageLayout(c, title, config=LayoutConfig(part_title=eyebrow))
    layout.add_paragraphs([intro], spacing_after=0.45 * cm)
    pastels = pastel_cycle(c)
    for num in range(1, 6):
        layout.add_fields_card(
            [
                [("Intitulé du métier", f"{prefix}_intitule_{num}", 0.85)],
                [("Pourquoi ce métier vous attire", f"{prefix}_pourquoi_{num}", 2.4),
                 ("Missions et compétences utiles", f"{prefix}_missions_{num}", 2.4)],
            ],
            title=f"Piste {num} · {kind}",
            color=pastels[(num - 1) % 2],
        )
    layout.render()


def create_pistes_no_limit_page(c):
    """Exercise 5: job sheets for the « no limit » leads."""
    _fiches_pages(
        c, "Fiches métiers : *pistes « no limit ».*", "Exercice 5 · Pistes no limit",
        "Explorez vos pistes sans tenir compte des contraintes matérielles ou personnelles.", "nl", "no limit",
    )


def create_pistes_realistes_page(c):
    """Exercise 6: job sheets for the realistic leads."""
    _fiches_pages(
        c, "Fiches métiers : *pistes réalistes.*", "Exercice 6 · Pistes réalistes",
        "Explorez les pistes qui vous semblent concrètement faisables dans votre situation.", "r", "réaliste",
    )
