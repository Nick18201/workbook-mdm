from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)


def create_profil_mbti_page(c):
    """
    P1.1 : MES PRÉFÉRENCES NATURELLES & MON STYLE (MBTI).
    """
    layout = PageLayout(
        c,
        "P1.1 : MES PRÉFÉRENCES NATURELLES (MBTI)",
        config=LayoutConfig(part_title="1. MON PROFIL & MON ÉCOLOGIE"),
    )

    layout.add_text(
        "Une préférence psychologique n'est ni un examen ni une étiquette qui vous enferme. "
        "C'est simplement la façon dont votre esprit aime fonctionner spontanément quand vous êtes détendu : "
        "comment vous puisez votre énergie, comment vous observez les situations, comment vous prenez vos décisions "
        "et comment vous préférez organiser votre quotidien.",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Mes Préférences Spontanées (ou mon type MBTI)",
        "livret_p1_mbti",
        config=QuestionConfig(
            box_height=4.7 * cm,
            subtitle="Vos 4 lettres (si exploré : ex. ISFJ, ENFP...) ou vos dominantes : Plutôt calme ou action partagée ? "
            "Détails concrets ou vision globale ? Logique rationnelle ou harmonie humaine ? Organisation posée ou flexibilité ?",
            example="Ex : ISFJ — Réfléchi, rigoureux, attentif aux personnes et aux faits concrets, besoin de calme pour préparer l'action.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Mes Forces Naturelles dans le Travail",
        "livret_p1_forces",
        config=QuestionConfig(
            box_height=4.7 * cm,
            subtitle="Grâce à cette manière d'être, quelle valeur ajoutée et quels atouts précieux apportez-vous "
            "spontanément à un collectif ou dans vos missions au quotidien ?",
            example="Ex : Mon sens du détail évite les erreurs critiques ; ma posture calme et mon écoute rassurent mes collègues et les partenaires.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()


def create_profil_ecologie_page(c):
    """
    P1.2 : MON ÉCOLOGIE D'ÉNERGIE & MON CLIMAT IDÉAL.
    """
    layout = PageLayout(
        c,
        "P1.2 : MON ÉCOLOGIE D'ÉNERGIE & CLIMAT IDÉAL",
        config=LayoutConfig(part_title="1. MON PROFIL & MON ÉCOLOGIE"),
    )

    layout.add_text(
        "Dans le travail, nous avons tous un « réservoir d'énergie ». Certaines tâches et ambiances rechargent "
        "naturellement vos batteries, tandis que d'autres vous demandent un effort d'adaptation coûteux. "
        "Construire une trajectoire épanouissante, c'est choisir un environnement respectueux de votre équilibre intérieur.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    layout.add_question_block(
        "Mon Climat de Travail Idéal",
        "livret_p1_climat",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Dans quel type d'ambiance, de rythme de travail, de style de management et de relations humaines "
            "donnez-vous le meilleur de vous-même ?",
            example="Ex : Une équipe bienveillante, un management qui fait confiance sans être directif, un rythme régulier sans urgences artificielles.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Ce qui Vide mes Batteries (Mes Signaux de Vigilance)",
        "livret_p1_couts",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Quelles sont les situations ou modes de fonctionnement qui vous épuisent rapidement ou vous pèsent lourdement ?",
            example="Ex : Les conflits ouverts non résolus, l'absence de consignes claires, le bruit permanent ou l'isolement complet sans échange.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()
