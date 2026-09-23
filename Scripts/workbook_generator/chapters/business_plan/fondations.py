from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionItem,
    TextConfig,
)


def create_fondations_idee_page(c):
    """
    Page 3 : PARTIE 1 — Mon Idée de Projet
    De l'intention brute à une première formulation claire.
    """
    layout = PageLayout(
        c,
        "1.1 : MON IDÉE DE PROJET",
        config=LayoutConfig(part_title="1. POSER LES FONDATIONS"),
    )

    layout.add_text(
        "Une idée n'est pas encore un projet. Une idée est une intuition spontanée ou une aspiration personnelle ; "
        "un projet est un système organisé capable d'apporter une solution réelle à des personnes précises. "
        "Être capable d'expliquer son idée en mots simples est la première victoire de l'entrepreneure.",
        config=TextConfig(spacing_after=0.45 * cm),
    )

    questions = [
        QuestionItem(
            question="1. Mon idée aujourd'hui (Description libre)",
            form_field_id="bp_p3_idee_libre",
            subtitle="Décrivez librement et sans censure ce que vous aimeriez créer, proposer ou développer.",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="2. Mon projet en une phrase",
            form_field_id="bp_p3_projet_phrase",
            subtitle="Résumez l'essence : « J'aimerais créer / développer... pour aider... à... »",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
        QuestionItem(
            question="3. Pourquoi ce projet ? (Sens personnel & Déclic)",
            form_field_id="bp_p3_pourquoi_sens",
            subtitle="Qu'est-ce qui vous a donné cette idée ? Quel problème ou manque avez-vous observé ? Pourquoi ce projet compte-t-il pour vous ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    ]

    layout.add_questions_group(questions, min_box_height=2.8 * cm, max_box_height=4.8 * cm)
    layout.render()


def create_fondations_vision_page(c):
    """
    Page 4 : PARTIE 1 — Ma Vision du Projet à 3 Ans
    Projection à moyen/long terme via 4 quadrants d'alignement.
    """
    layout = PageLayout(
        c,
        "1.2 : MA VISION DU PROJET À 3 ANS",
        config=LayoutConfig(part_title="1. POSER LES FONDATIONS"),
    )

    layout.add_text(
        "Construire sa vision, c'est se donner un cap avant de plonger dans les détails opérationnels. "
        "Cette vision doit allier votre ambition de création et le respect de votre écologie personnelle.",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    cards = [
        {
            "title": "1. Mon Projet Idéal dans 3 Ans",
            "subtitle": "À quoi ressemble une journée type ? Quelle est la taille de l'activité ?",
            "field_id": "bp_p4_vision_ideal",
            "placeholder": "Décrivez votre quotidien, votre activité et vos clients idéaux...",
        },
        {
            "title": "2. Ce que j'aimerais avoir Construit",
            "subtitle": "Quels produits, services, réputation ou impact concret ?",
            "field_id": "bp_p4_vision_construit",
            "placeholder": "Vos accomplissements concrets d'ici 3 ans...",
        },
        {
            "title": "3. La Place dans ma Vie & mon Équilibre",
            "subtitle": "Quel temps de travail ? Quelle liberté ? Quel équilibre pro/perso ?",
            "field_id": "bp_p4_vision_vie",
            "placeholder": "Vos conditions de vie, votre rémunération cible, votre sérénité...",
        },
        {
            "title": "4. Ce que je refuse Absolument de Construire",
            "subtitle": "Quels pièges, contraintes ou compromis ne voulez-vous jamais accepter ?",
            "field_id": "bp_p4_vision_refus",
            "placeholder": "Vos limites non négociables et ce qui dénaturerait votre projet...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=7.6 * cm)
    layout.render()
