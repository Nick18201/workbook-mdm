from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle
from workbook_generator.templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig


def create_alignement_pages_part1(c):
    layout = PageLayout(
        c,
        "1. Mes expériences d'alignement (1/2)",
        config=LayoutConfig(part_title="1. ALIGNEMENT")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Identifier les situations professionnelles ou personnelles où vous vous êtes senti(e) à votre place.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3 * cm)
    )
    layout.add_text(
        "Repensez à trois situations (professionnelles, scolaires, associatives, personnelles) où vous étiez particulièrement aligné(e). En voici les deux premières :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Situation 1 - Décrivez brièvement le contexte (Quoi ? Qui ? Où ?) :",
        "align_sit1_desc",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Analyse 1 - Qu'est-ce qui vous donnait de l'énergie ? Qu'apportiez-vous ? Quelle valeur était respectée ?",
        "align_sit1_analyse",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Situation 2 - Décrivez brièvement le contexte (Quoi ? Qui ? Où ?) :",
        "align_sit2_desc",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Analyse 2 - Qu'est-ce qui vous donnait de l'énergie ? Qu'apportiez-vous ? Quelle valeur était respectée ?",
        "align_sit2_analyse",
        config=QuestionConfig(box_height=2.3 * cm),
    )

    layout.render()


def create_alignement_pages_part2(c):
    layout = PageLayout(
        c,
        "1. Mes expériences d'alignement (2/2)",
        config=LayoutConfig(part_title="1. ALIGNEMENT")
    )
    layout.add_text(
        "Voici la troisième situation d'alignement ainsi qu'un bilan global de cet exercice :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Situation 3 - Décrivez brièvement le contexte (Quoi ? Qui ? Où ?) :",
        "align_sit3_desc",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Analyse 3 - Qu'est-ce qui vous donnait de l'énergie ? Qu'apportiez-vous ? Quelle valeur était respectée ?",
        "align_sit3_analyse",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Synthèse - Valeurs possibles révélées par ces trois situations :",
        "align_valeurs_revelees",
        config=QuestionConfig(box_height=2.5 * cm),
    )

    layout.render()


def create_desalignement_pages_part1(c):
    layout = PageLayout(
        c,
        "2. Mes expériences de désalignement (1/2)",
        config=LayoutConfig(part_title="2. DÉSALIGNEMENT")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Comprendre quelle valeur importante a été bafouée ou ignorée dans des moments difficiles.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3 * cm)
    )
    layout.add_text(
        "Repensez à trois situations où vous vous êtes senti(e) en difficulté, frustré(e), vidé(e) ou en conflit intérieur :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Situation 1 - Décrivez la situation de désalignement ou de perte de sens :",
        "desalign_sit1_desc",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Analyse 1 - Qu'est-ce qui vous a dérangé ? Quelle limite a été franchie ? Quelle valeur était absente ou bafouée ?",
        "desalign_sit1_analyse",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Situation 2 - Décrivez la situation de désalignement ou de perte de sens :",
        "desalign_sit2_desc",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Analyse 2 - Qu'est-ce qui vous a dérangé ? Quelle limite a été franchie ? Quelle valeur était absente ou bafouée ?",
        "desalign_sit2_analyse",
        config=QuestionConfig(box_height=2.3 * cm),
    )

    layout.render()


def create_desalignement_pages_part2(c):
    layout = PageLayout(
        c,
        "2. Mes expériences de désalignement (2/2)",
        config=LayoutConfig(part_title="2. DÉSALIGNEMENT")
    )
    layout.add_text(
        "Voici la troisième situation de désalignement ainsi qu'un bilan global :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Situation 3 - Décrivez la situation de désalignement ou de perte de sens :",
        "desalign_sit3_desc",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Analyse 3 - Qu'est-ce qui vous a dérangé ? Quelle limite a été franchie ? Quelle valeur était absente ou bafouée ?",
        "desalign_sit3_analyse",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Synthèse - Valeurs absentes, empêchées ou bafouées révélées :",
        "desalign_valeurs_revelees",
        config=QuestionConfig(box_height=2.5 * cm),
    )

    layout.render()


def create_choix_difficiles_page1(c):
    layout = PageLayout(
        c,
        "3. Mes choix difficiles (1/2)",
        config=LayoutConfig(part_title="3. CHOIX DIFFICILES")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Révéler vos priorités profondes à travers des arbitrages complexes.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3 * cm)
    )
    layout.add_text(
        "Les valeurs apparaissent dans les choix difficiles car choisir implique de renoncer. Repensez à deux situations de choix complexes (ex: rester/partir, sécurité/risque, etc.) :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Choix difficile 1 - Quelle était la situation ?",
        "choix1_desc",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Options - Qu'est-ce que l'Option A et l'Option B permettaient chacune de préserver ?",
        "choix1_options",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Résolution - Qu'avez-vous choisi ? Qu'est-ce que cela a coûté et permis de respecter ?",
        "choix1_resolution",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Valeurs - Quelles valeurs étaient en conflit ?",
        "choix1_valeurs",
        config=QuestionConfig(box_height=1.5 * cm),
    )

    layout.render()


def create_choix_difficiles_page2(c):
    layout = PageLayout(
        c,
        "3. Mes choix difficiles (2/2)",
        config=LayoutConfig(part_title="3. CHOIX DIFFICILES")
    )
    layout.add_text(
        "Voici le second arbitrage complexe de votre parcours professionnel ou personnel :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Choix difficile 2 - Quelle était la situation ?",
        "choix2_desc",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Options - Qu'est-ce que l'Option A et l'Option B permettaient chacune de préserver ?",
        "choix2_options",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Résolution - Qu'avez-vous choisi ? Qu'est-ce que cela a coûté et permis de respecter ?",
        "choix2_resolution",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Valeurs - Quelles valeurs étaient en conflit ?",
        "choix2_valeurs",
        config=QuestionConfig(box_height=1.5 * cm),
    )

    layout.render()
