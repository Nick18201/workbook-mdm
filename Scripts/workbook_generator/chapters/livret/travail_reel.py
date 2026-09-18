from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)


def create_travail_reel_coulisses_page(c):
    """
    P2.1 : LES COULISSES DU TRAVAIL RÉEL (Ce que la fiche de poste ne dit pas & bricolages).
    """
    layout = PageLayout(
        c,
        "P2.1 : LES COULISSES DU TRAVAIL RÉEL",
        config=LayoutConfig(part_title="2. LE TRAVAIL RÉEL & LES COULISSES"),
    )

    layout.add_text(
        "La fiche de poste officielle est souvent une vue très théorique du travail. "
        "Dans la réalité, pour que les projets aboutissent malgré les aléas, vous compensez les manques, "
        "vous inventez des solutions et vous rassurez les gens. C'est précisément dans ces régulations "
        "invisibles que s'exprime votre véritable valeur professionnelle.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "Ce que ma fiche de poste ne dit pas",
        "livret_p2_coulisses",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Les micro-décisions, arbitrages et ajustements indispensables que vous réalisez chaque semaine "
            "et qui n'étaient écrits sur aucun descriptif officiel de poste.",
            example="Ex : Anticiper les erreurs d'un logiciel, vulgariser des règles techniques pour des non-spécialistes, désamorcer des tensions.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Mes Astuces & Bricolages Ingénieux",
        "livret_p2_bricolages",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Les outils, raccourcis, matrices ou méthodes que vous avez créés ou adaptés vous-même "
            "pour fluidifier votre quotidien et gagner en efficacité.",
            example="Ex : Mise en place spontanée d'un tableau de chiffrage et d'aide à la saisie réduisant de moitié les délais administratifs.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()


def create_travail_reel_empeche_page(c):
    """
    P2.2 : MES DÉSIRS DE QUALITÉ & LE TRAVAIL CONTRARIÉ (Le travail empêché).
    """
    layout = PageLayout(
        c,
        "P2.2 : DÉSIRS DE QUALITÉ & TRAVAIL CONTRARIÉ",
        config=LayoutConfig(part_title="2. LE TRAVAIL RÉEL & LES COULISSES"),
    )

    layout.add_text(
        "La fatigue et la démotivation ne viennent presque jamais de la paresse, mais de ce que les ergonomes "
        "nomment le « travail empêché » : avoir à cœur de réaliser un travail de grande qualité, mais en être empêché "
        "par le manque de moyens, des délais intenables ou des règles déconnectées du terrain.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "Ce que j'aurais aimé accomplir avec fierté",
        "livret_p2_empeche",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Quelles missions ou gestes professionnels auriez-vous voulu soigner davantage si l'organisation "
            "ou les contraintes de votre précédent poste ne vous avaient pas freiné ?",
            example="Ex : Prendre le temps d'accompagner les acteurs sur le terrain plutôt que de devoir produire des calculs d'écran à la chaîne.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Mes Exigences de Qualité pour Demain",
        "livret_p2_exigences",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="De quelles conditions (autonomie, temps de réflexion, relations saines, impact concret) "
            "aurez-vous impérativement besoin dans votre futur métier pour être pleinement fier de votre geste ?",
            example="Ex : Avoir un impact environnemental visible, échanger avec un collectif de confiance, retrouver le plaisir du travail soigné.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()
