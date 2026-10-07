from reportlab.lib.units import cm

from workbook_generator.templates import PageLayout, LayoutConfig, QuestionItem


def create_faire_le_point_pages(c):
    """Exercise 2: eight questions on the current situation, four per page."""
    questions = [
        ("Comment je me sens actuellement ?", "feeling"),
        ("Quel a été le déclencheur de ce bilan ?", "trigger"),
        ("De quoi j’ai besoin en ce moment ?", "needs"),
        ("Qu’ai-je fait jusqu’à présent pour remédier à cette situation ?", "actions_taken"),
        ("Qu’est-ce que je n’ai pas encore changé ? Pourquoi ?", "not_changed"),
        ("Quels avantages ai-je à garder la situation telle quelle ?", "secondary_benefits"),
        ("Quels besoins sont insatisfaits dans ma vie aujourd’hui ?", "unmet_needs"),
        ("Quelles actions concrètes puis-je mettre en place ?", "concrete_actions"),
    ]
    items = [QuestionItem(q, f"s1_point_{key}") for q, key in questions]

    layout = PageLayout(c, "Faire le point *sur votre situation.*",
                        config=LayoutConfig(part_title="Exercice 2 · Faire le point"))
    layout.add_paragraphs([
        "Le début d’un bilan est le bon moment pour appuyer sur pause. Difficile de réfléchir à vos besoins et à "
        "vos envies quand la routine, la surcharge de travail ou l’ennui prennent toute la place.",
    ], spacing_after=0.45 * cm)
    layout.add_questions_group(items[:4], max_box_height=4.5 * cm)
    layout.page_break()
    layout.add_questions_group(items[4:], max_box_height=4.5 * cm)
    layout.render()


def create_domaines_de_vie_page(c):
    """Exercise 3: a 1-10 satisfaction scale per life domain, then the analysis."""
    layout = PageLayout(c, "Vos domaines *de vie.*", config=LayoutConfig(part_title="Exercice 3 · Domaines de vie"))
    layout.add_paragraphs([
        "Votre vie se compose de plusieurs domaines qui pèsent les uns sur les autres. Noter votre satisfaction "
        "dans chacun d’eux donne une photographie de votre équilibre actuel.",
        "Pour chaque domaine, cochez une note de 1 (très peu satisfait·e) à 10 (pleinement satisfait·e).",
    ], spacing_after=0.45 * cm)
    domains = [
        "1. Argent, finances",
        "2. Impact, utilité",
        "3. Temps pour soi, engagements",
        "4. Famille",
        "5. Santé, énergie",
        "6. Lieu de vie, environnement",
        "7. Loisirs, passions",
        "8. Travail, carrière",
    ]
    layout.add_rating_grid(
        [(d, f"s1_domaine_note_{i + 1}") for i, d in enumerate(domains)], "s1_domaine_note",
        min_label="1 · Très peu satisfait·e", max_label="10 · Pleinement satisfait·e",
    )
    layout.add_questions_group([
        QuestionItem(
            "Analyse de votre équilibre", "s1_domaine_reflexion",
            subtitle="Quels domaines sont les plus satisfaisants ? Les moins satisfaisants ? Quel est l’impact de "
                     "votre travail actuel, positif comme négatif, sur les autres domaines ?",
        ),
    ])
    layout.render()


def create_entourage_page(c):
    """Exercise 4: the people who support the project and those who may doubt it."""
    layout = PageLayout(c, "Votre *entourage.*", config=LayoutConfig(part_title="Exercice 4 · Entourage"))
    layout.add_paragraphs([
        "Votre projet ne se construit pas seul. Votre entourage, proche ou plus lointain, pèse sur vos "
        "décisions. Repérer vos alliés et les sources de tension possibles vous aide à sécuriser votre projet.",
    ], spacing_after=0.45 * cm)
    layout.add_questions_group([
        QuestionItem("Soutien, conseil en positif", "s1_entourage_soutiens",
                     subtitle="Qui peut vous soutenir ou vous conseiller utilement dans cette démarche ?"),
        QuestionItem("Regard négatif ou inquiétude des proches", "s1_entourage_freins",
                     subtitle="Qui pourrait exprimer des doutes, des craintes ou un regard critique ?"),
    ])
    layout.render()
