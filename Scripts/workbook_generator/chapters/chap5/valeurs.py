from reportlab.lib.units import cm

from workbook_generator.templates import PageLayout, LayoutConfig, QuestionConfig, QuestionItem

CATEGORIES_VALEURS = [
    {
        "title": "Liberté et autonomie",
        "values": ["Autonomie", "Liberté", "Indépendance", "Créativité", "Marge de manœuvre", "Responsabilité", "Choix",
                   "Souplesse", "Authenticité", "Initiative"],
    },
    {
        "title": "Sécurité et stabilité",
        "values": ["Sécurité", "Stabilité", "Prévisibilité", "Cadre clair", "Protection", "Fiabilité", "Continuité",
                   "Sérénité", "Équilibre", "Confort"],
    },
    {
        "title": "Réussite et reconnaissance",
        "values": ["Réussite", "Progression", "Ambition", "Excellence", "Compétence", "Reconnaissance", "Statut",
                   "Légitimité", "Impact", "Fierté"],
    },
    {
        "title": "Relation et coopération",
        "values": ["Bienveillance", "Entraide", "Écoute", "Loyauté", "Respect", "Coopération", "Confiance", "Harmonie",
                   "Soutien", "Qualité relationnelle"],
    },
    {
        "title": "Justice et utilité sociale",
        "values": ["Justice", "Équité", "Inclusion", "Égalité", "Utilité sociale", "Sens", "Contribution", "Engagement",
                   "Éthique", "Responsabilité sociale"],
    },
    {
        "title": "Stimulation et apprentissage",
        "values": ["Nouveauté", "Défi", "Apprentissage", "Curiosité", "Exploration", "Variété", "Mouvement", "Intensité",
                   "Expérimentation", "Évolution"],
    },
    {
        "title": "Plaisir et qualité de vie",
        "values": ["Plaisir", "Joie", "Légèreté", "Beauté", "Esthétique", "Confort de vie", "Temps pour soi", "Vitalité",
                   "Spontanéité", "Simplicité"],
    },
    {
        "title": "Cadre, règles et transmission",
        "values": ["Rigueur", "Discipline", "Respect du cadre", "Tradition", "Transmission", "Fiabilité", "Méthode",
                   "Structure", "Engagement", "Sens du devoir"],
    },
    {
        "title": "Influence et pouvoir d'agir",
        "values": ["Influence", "Leadership", "Décision", "Pouvoir d'agir", "Autorité", "Responsabilité", "Pilotage",
                   "Capacité à transformer", "Capacité à orienter", "Maîtrise"],
    },
]


def create_liste_valeurs_page(c):
    """Exercise 4: tick the values that come back in your story, by category."""
    layout = PageLayout(c, "Nommer *ce qui compte.*", config=LayoutConfig(part_title="Exercice 4 · Liste de valeurs · 10 min"))
    layout.add_paragraphs([
        "À partir de vos situations d'alignement, de désalignement et de vos choix difficiles, cochez les valeurs "
        "qui reviennent régulièrement dans votre parcours.",
    ], spacing_after=0.45 * cm)
    layout.add_checklist_cards([(cat["title"], cat["values"]) for cat in CATEGORIES_VALEURS], columns=3,
                               field_prefix="valeur")
    layout.render()


def create_hierarchiser_valeurs_page(c):
    """Exercise 5: from ten values to five, then to three non-negotiable ones."""
    layout = PageLayout(c, "Hiérarchiser *vos valeurs.*", config=LayoutConfig(part_title="Exercice 5 · Hiérarchie · 10 min"))
    layout.add_paragraphs([
        "Parmi les valeurs cochées, réduisez progressivement votre choix pour dégager celles qui guident votre vie "
        "professionnelle.",
    ], spacing_after=0.45 * cm)
    layout.add_questions_group([
        QuestionItem("1. Mes 10 valeurs importantes", "hierarchie_10_valeurs",
                     subtitle="Les 10 valeurs qui reviennent le plus dans votre parcours."),
        QuestionItem("2. Mes 5 valeurs prioritaires", "hierarchie_5_valeurs",
                     subtitle="Les 5 plus fortes parmi les 10."),
        QuestionItem("3. Mes 3 valeurs non négociables", "hierarchie_3_valeurs",
                     subtitle="Les 3 plus vitales parmi les 5."),
    ], max_box_height=3.4 * cm)
    layout.add_callout(
        "Une valeur non négociable est une valeur qui, si elle manque durablement dans votre travail, risque "
        "d'entraîner une perte de motivation et d'énergie.",
        title="À retenir",
    )
    layout.render()


def _create_incarner_valeur_page(c, num):
    layout = PageLayout(c, "Incarner vos valeurs *non négociables.*",
                        config=LayoutConfig(part_title=f"Exercice 6 · Valeur {num} sur 3 · 5 min"))
    layout.add_paragraphs(["Traduisez chaque valeur clé en ressentis, en actions et en besoins concrets."],
                          spacing_after=0.45 * cm)
    layout.add_fields_card([[(f"Valeur non négociable n° {num}", f"incarner_val_{num}_name", 0.9)]])
    layout.add_questions_group([
        QuestionItem("1. Comment cette valeur se manifeste-t-elle concrètement dans mon travail ?", f"incarner_val_{num}_q1"),
        QuestionItem("2. Dans quelles situations passées l'ai-je déjà vécue ?", f"incarner_val_{num}_q2"),
        QuestionItem("3. Qu'est-ce que je ressens quand elle est respectée, ou absente ?", f"incarner_val_{num}_q3"),
        QuestionItem("4. De quoi ai-je besoin concrètement pour qu'elle existe dans mon futur travail ?",
                     f"incarner_val_{num}_q4"),
    ])
    layout.render()


def create_incarner_valeur_1_page(c):
    _create_incarner_valeur_page(c, 1)


def create_incarner_valeur_2_page(c):
    _create_incarner_valeur_page(c, 2)


def create_incarner_valeur_3_page(c):
    _create_incarner_valeur_page(c, 3)


def create_conditions_travail_page(c):
    """Exercise 7: observable criteria to assess future jobs."""
    layout = PageLayout(c, "Vos valeurs en *conditions de travail.*",
                        config=LayoutConfig(part_title="Exercice 7 · Conditions de travail · 10 min"))
    layout.add_paragraphs([
        "Formulez des critères concrets et observables, pour évaluer vos futurs postes ou projets.",
    ], spacing_after=0.45 * cm)
    layout.add_question_block(
        "1. Pour respecter mes valeurs, j'ai besoin d'un environnement où…",
        "conditions_positives",
        config=QuestionConfig(
            box_height=6.5 * cm,
            example="je peux organiser mon travail avec autonomie ; les relations sont respectueuses ; les objectifs "
                    "sont clairs ; je peux apprendre régulièrement ; je me sens utile ; le rythme est soutenable.",
        ),
    )
    layout.add_question_block(
        "2. Pour respecter mes valeurs, j'ai besoin d'éviter les environnements où…",
        "conditions_negatives",
        config=QuestionConfig(
            box_height=6.5 * cm,
            example="tout est contrôlé ; les priorités changent sans cesse ; il y a peu de reconnaissance ; les "
                    "relations sont froides ou compétitives ; la pression est permanente ; il n'y a pas d'évolution.",
        ),
    )
    layout.render()
