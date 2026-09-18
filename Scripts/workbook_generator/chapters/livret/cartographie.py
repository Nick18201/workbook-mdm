from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)


def create_cartographie_metier_page(c):
    """
    P3.1 : SAVOIR-FAIRE MÉTIER & MÉTHODES D'ORGANISATION (Techniques et Méthodes).
    """
    layout = PageLayout(
        c,
        "P3.1 : SAVOIR-FAIRE MÉTIER & MÉTHODES",
        config=LayoutConfig(part_title="3. MA CARTOGRAPHIE DES COMPÉTENCES"),
    )

    layout.add_text(
        "Une compétence n'est pas un diplôme théorique : c'est votre capacité à combiner vos connaissances "
        "et vos réflexes pour agir avec pertinence face à une situation réelle. Regardons d'abord vos expertises "
        "de spécialité et vos méthodes pour structurer le travail.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "Mes Savoir-Faire Techniques & Cœur de Métier",
        "livret_p3_techniques",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Les outils, logiciels spécialisés, réglementations, calculs, normes et gestes professionnels "
            "que vous maîtrisez avec une grande aisance.",
            example="Ex : Modélisation réglementaire RE2020, logiciels thermiques et de CAO, analyse de plans de construction, métrés.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Mes Méthodes pour Structurer, Chiffrer & Résoudre",
        "livret_p3_methodes",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Comment vous y prenez-vous pour organiser un planning, vérifier la qualité, chiffrer un projet "
            "ou trouver l'origine d'un dysfonctionnement ?",
            example="Ex : Détection méthodique des goulets d'étranglement, fiabilisation des bases de données, suivi financier analytique.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()


def create_cartographie_humain_page(c):
    """
    P3.2 : COOPÉRATION & AGILITÉ D'APPRENTISSAGE (Relation et Adaptation).
    """
    layout = PageLayout(
        c,
        "P3.2 : COOPÉRATION & AGILITÉ D'APPRENTISSAGE",
        config=LayoutConfig(part_title="3. MA CARTOGRAPHIE DES COMPÉTENCES"),
    )

    layout.add_text(
        "Votre valeur professionnelle ne se limite pas à vos outils techniques. Elle repose tout autant "
        "sur votre manière d'entrer en relation avec les autres, de partager votre savoir et de continuer "
        "à évoluer face aux transformations permanentes de votre secteur.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "Ma Coopération, Écoute & Transmission",
        "livret_p3_relation",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Comment interagissez-vous au quotidien ? (Vulgariser des notions complexes pour des novices, "
            "apaiser des tensions, négocier avec bienveillance, transmettre).",
            example="Ex : Expliquer des contraintes thermiques avec des mots simples aux artisans sur le chantier, former un nouveau collègue.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Mon Agilité & ma Curiosité d'Apprendre",
        "livret_p3_apprentissage",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Comment réagissez-vous face à la nouveauté ? Racontez votre manière d'apprendre par vous-même "
            "et d'explorer des sujets inédits.",
            example="Ex : Veille continue sur les nouvelles réglementations, montée en compétence rapide en autodidacte sur un logiciel complexe.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()
