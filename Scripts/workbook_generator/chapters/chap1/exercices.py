from reportlab.lib.units import cm

from workbook_generator.components import create_standard_meteo_page, create_standard_quadrants_page
from workbook_generator.templates import PageLayout, LayoutConfig, QuestionConfig, QuestionItem


def create_meteo_page(c):
    """Exercise 1: the inner weather."""
    create_standard_meteo_page(
        c,
        title="Votre état d'esprit *du moment.*",
        part_title="Exercice 1 · Météo",
        field_prefix="meteo",
    )


def create_vision_page(c):
    """Exercise 2: the four life domains as quadrants."""
    create_standard_quadrants_page(
        c,
        title="Votre vision *à 360°.*",
        part_title="Exercice 2 · Vision à 360°",
        instruction="Pour chaque domaine, écrivez une phrase de synthèse sur ce que vous visez.",
        quadrants_data=[
            ("Professionnel", "Missions, utilité, salaire", "pro"),
            ("Personnel", "Temps pour soi, santé", "perso"),
            ("Social et familial", "Relations, rythme de vie", "social"),
            ("Cadre et autonomie", "Besoin de cadre ou de liberté", "cadre"),
        ],
        field_prefix="vision",
    )


def create_boussole_page(c):
    """Exercise 3: the compass objective, its benefit and its success criterion."""
    layout = PageLayout(c, "Votre objectif *boussole.*", config=LayoutConfig(part_title="Exercice 3 · Objectif boussole"))
    layout.add_paragraphs([
        "Formulez le cap prioritaire de votre bilan, puis la façon dont vous vérifierez que vous l’avez atteint.",
    ], spacing_after=0.45 * cm)
    layout.add_questions_group([
        QuestionItem("D'ici 3 mois, je veux avoir clarifié :", "boussole_enjeu"),
        QuestionItem("Pour pouvoir :", "boussole_benefice"),
        QuestionItem("Je saurai que j'ai réussi quand :", "boussole_succes_preuve",
                     subtitle="Une situation concrète, observable dans votre quotidien."),
    ], max_box_height=5.0 * cm)
    layout.render()


def create_sac_a_dos_page(c):
    """Exercise 4: what you decide to put down."""
    layout = PageLayout(c, "Le sac à dos : *ce que je dépose.*", config=LayoutConfig(part_title="Exercice 4 · Sac à dos"))
    layout.add_paragraphs(["Allégez le sac à dos. Aujourd’hui, je décide de déposer :"], spacing_after=0.45 * cm)
    for question, field_id in (
        ("Je lâche cette idée reçue :", "sac_croyance"),
        ("Je ne veux plus subir :", "sac_subir"),
        ("Ma plus grande peur est :", "sac_peur"),
    ):
        layout.add_question_block(question, field_id, config=QuestionConfig(box_height=3.6 * cm))
    layout.add_annotation("… et je décide de la regarder en face.")
    layout.render()


def create_heritage_page(c):
    """Exercise 5: the family inheritance (3FVS matrix: strengths, cautions, wishes)."""
    layout = PageLayout(c, "Votre héritage *familial.*", config=LayoutConfig(part_title="Exercice 5 · Héritages"))
    layout.add_paragraphs([
        "Identifiez ce que vous avez reçu, pour décider de ce que vous en faites (matrice 3FVS).",
    ], spacing_after=0.45 * cm)
    for question, field_id, hint in (
        ("1. Forces : ce que je garde", "heritage_forces",
         "Quelles qualités, valeurs ou savoir-faire de ma famille sont des atouts ?"),
        ("2. Vigilances : ce que je laisse", "heritage_vigilances",
         "Quels comportements ou idées reçues je décide de ne pas reproduire ?"),
        ("3. Souhaits et comptes : les attentes familiales", "heritage_souhaits",
         "Qu'est-ce qu'on voulait pour moi ? À qui ai-je l'impression de devoir quelque chose ?"),
    ):
        layout.add_question_block(question, field_id, config=QuestionConfig(box_height=3.3 * cm, subtitle=hint))
    layout.add_annotation("On ne trahit pas ses origines en choisissant sa propre voie. On les honore différemment.")
    layout.render()


def create_work_image_page(c):
    """Exercise 6: the image of work received from the family, and the one you choose."""
    layout = PageLayout(c, "Votre image *du travail.*", config=LayoutConfig(part_title="Exercice 6 · Image du travail"))
    layout.add_question_block(
        "1. Exploration sensorielle et émotionnelle",
        "image_sensorielle",
        config=QuestionConfig(
            box_height=2.2 * cm,
            subtitle="Fermez les yeux. Visualisez le lieu de travail de vos parents (ou des personnes qui vous ont "
                     "élevé). Les odeurs ? Les bruits ? La lumière ? L’ambiance générale ?",
        ),
    )
    layout.add_heading("2. L’héritage familial")
    layout.add_fields_card([
        [("Le travail de vos parents ou grands-parents", "image_metiers", 1.3)],
        [("Leur relation au travail (plaisir, souffrance, ennui…)", "image_relation", 1.3)],
        [("L’effet de leur travail sur la vie de famille (stress, absences, argent…)", "image_impact_famille", 1.3)],
        [("Leur influence sur vos choix (encouragements, dissuasions…)", "image_influence_choix", 1.3)],
    ])
    layout.add_heading("3. Changer de regard")
    layout.add_fields_card([
        [("5 mots associés au travail (héritage)", "image_mots_heritage", 3.0),
         ("5 mots pour mon futur travail (choix)", "image_mots_futur", 3.0)],
    ])
    layout.render()


def create_mentors_page(c):
    """Exercise 7: role models and anti-models."""
    layout = PageLayout(c, "Vos mentors *et anti-modèles.*", config=LayoutConfig(part_title="Exercice 7 · Modèles"))
    layout.add_questions_group([
        QuestionItem("Mes mentors (inspirations)", "mentors_positif",
                     subtitle="Qui est votre modèle professionnel, réel ou fictif, et pourquoi ? (J’admire X pour…)"),
        QuestionItem("Mes anti-modèles (repoussoirs)", "mentors_negatif",
                     subtitle="Quels comportements ou situations refusez-vous de reproduire ? (Je ne veux pas reproduire…)"),
    ])
    layout.render()
