from reportlab.lib.units import cm

from workbook_generator import components
from workbook_generator.components import create_standard_summary_page, draw_answer_box
from workbook_generator.config import PDFStyle
from workbook_generator.primitives import draw_pastel_card, draw_text, text_width
from workbook_generator.templates import PageLayout, LayoutConfig, QuestionItem


def create_cover_page(c):
    components.create_cover_page(
        c, "Le *prélude.*", number=0, tagline="Bilan de compétences",
        promise="Poser le cadre, fixer le cap.",
    )


def create_summary_page(c):
    """Chapter opener: the objective of the workbook and its four exercises."""
    intro_txt = (
        "Ce premier carnet pose le cadre de travail, votre engagement et votre point de départ.<br/><br/>"
        "La question centrale de votre bilan : "
        "<b>quelle place voulez-vous donner au travail dans votre vie, et sous quelle forme ?</b>"
    )
    exercises = [
        "Exercice 1 · Mon engagement : le temps que vous investissez, et pour quel objectif.",
        "Exercice 2 · Faire le point : votre situation actuelle, en huit questions.",
        "Exercice 3 · Vos domaines de vie : votre satisfaction, domaine par domaine.",
        "Exercice 4 · Votre entourage : vos soutiens et les regards critiques.",
    ]
    create_standard_summary_page(c, "0", "Poser le cadre *du bilan.*", intro_txt, exercises)


def create_editorial_page_card(c):
    """Welcome page: what the workbooks are for, the four stages of the bilan, the Notion space."""
    layout = PageLayout(c, "Le mot *d'accueil.*", config=LayoutConfig(part_title="Ouverture"))
    layout.add_paragraphs([
        "Vous commencez un bilan de compétences : vous avez décidé de faire le point sur votre parcours "
        "professionnel et de passer à l’action.",
        "Ces carnets vous accompagnent tout au long du bilan. Ils rassemblent vos idées, vos constats et vos "
        "décisions. Vous les remplissez entre les séances, et nous les relisons ensemble.",
        "Le bilan alterne questionnaires, exercices pratiques et échanges en séance. Chaque exercice sert de "
        "support à nos entretiens. Ajoutez librement les questions ou les pistes qui vous semblent utiles.",
        "Pour travailler, réservez des moments calmes, sans interruption. Notez ce qui vous vient sans vous "
        "censurer : le tri se fait en séance.",
    ], size=PDFStyle.SIZE_LEAD)
    layout.add_heading("Les grandes lignes du bilan")
    layout.add_frise(
        [
            ("history", "Prendre du recul", "Choix passés"),
            ("psychology", "Explorer votre personnalité", "Forces, envies"),
            ("travel_explore", "Aller sur le terrain", "Métiers"),
            ("flag", "Décider et agir", "Plan d'action"),
        ],
        start_label="Aujourd'hui",
        end_label="Fin du bilan",
    )
    layout.add_callout(
        "Un espace Notion rassemble des ressources (sites, podcasts, articles), accessibles à tout moment "
        "pendant le bilan.",
        title="Entre les séances",
    )
    layout.render()


def create_intro_sense_page(c):
    """Introduction: why understanding your choices helps you decide."""
    layout = PageLayout(c, "Comprendre *pour décider.*", config=LayoutConfig(part_title="Introduction"))
    layout.add_paragraphs([
        "Savoir pourquoi vous faites ce que vous faites, c’est reprendre la main sur vos décisions "
        "professionnelles.",
        "La psychologie et la sociologie le montrent : une part de nos choix vient de notre histoire, de notre "
        "milieu et des modèles reçus, plus que d’une décision libre. Le bilan vous aide à faire la différence, "
        "pour décider en connaissance de cause.",
        "Nous partons d’un principe simple : chacun peut apprendre, s’adapter et changer. Chacun a aussi des "
        "facilités naturelles pour certaines tâches.",
        "Votre personnalité se construit tout au long de la vie, et elle vous distingue : aptitudes, points "
        "forts, goûts. C’est ce qui rend les rôles complémentaires dans une équipe.",
        "Le lien entre ce que vous êtes et ce que vous faites au quotidien peut pourtant se distendre. "
        "Fatigue, perte d’intérêt, tâches qui semblent inutiles, attentes qui changent : les raisons de faire "
        "le point sont nombreuses.",
    ], size=PDFStyle.SIZE_LEAD)
    layout.add_callout(
        "Vous aider à construire un projet professionnel réaliste, qui tienne compte de ce que vous êtes, du "
        "marché du travail, de votre salaire et de votre rythme de vie.",
        title="Notre objectif",
    )
    layout.add_annotation("C’est un objectif ambitieux. Ce carnet en est la première étape.")
    layout.render()


def create_form_page_card(c):
    """Exercise 1: the commitment (name, hours per week), the main goal and what you allow yourself."""
    layout = PageLayout(c, "Mon *engagement.*", config=LayoutConfig(part_title="Exercice 1 · Mon engagement"))
    form = c.acroForm
    x, width = layout.text_x, layout.target_width
    pad = PDFStyle.CARD_PADDING
    size = PDFStyle.SIZE_LEAD
    field_h = 0.85 * cm
    row_gap = 0.45 * cm
    card_h = 2 * pad + 2 * field_h + row_gap
    top = layout.y_cursor
    draw_pastel_card(c, x, top - card_h, width, card_h)

    # « Moi, [nom], je décide d'investir [n] heures par semaine dans mon bilan. »
    row_y = top - pad - field_h
    baseline = row_y + field_h / 2 - 0.35 * size
    w = draw_text(c, x + pad, baseline, "Moi,", PDFStyle.FONT_BODY, size, PDFStyle.COLOR_INK)
    name_x = x + pad + w + 0.25 * cm
    draw_answer_box(c, name_x, row_y, x + width - pad - name_x, field_h, "nom_complet", tooltip="Prénom Nom",
                    multiline=False)
    row_y -= field_h + row_gap
    baseline = row_y + field_h / 2 - 0.35 * size
    w = draw_text(c, x + pad, baseline, "je décide d'investir", PDFStyle.FONT_BODY, size, PDFStyle.COLOR_INK)
    hours_x = x + pad + w + 0.25 * cm
    draw_answer_box(c, hours_x, row_y, 1.6 * cm, field_h, "engagement_hebdo", tooltip="Nombre d'heures",
                    multiline=False)
    draw_text(c, hours_x + 1.6 * cm + 0.25 * cm, baseline, "heures par semaine dans mon bilan.",
              PDFStyle.FONT_BODY, size, PDFStyle.COLOR_INK)
    layout.y_cursor -= card_h + PDFStyle.GAP_BLOCK

    layout.add_questions_group([
        QuestionItem("Mon objectif principal :", "objectif_3_mois",
                     subtitle="Ce que vous voulez avoir obtenu à la fin du bilan."),
        QuestionItem("Je m'autorise à :", "permission_personnelle",
                     subtitle="Une piste ou une question que vous écartez d'habitude, et que vous décidez d'étudier."),
    ], max_box_height=5.5 * cm)

    # Hidden document metadata (type and version of the workbook)
    form.textfield(name="meta_doc_type", value="workbook_chap0", x=0, y=-10, width=0, height=0)
    form.textfield(name="meta_doc_version", value="2.0_da_editorial", x=0, y=-10, width=0, height=0)
    layout.render()
