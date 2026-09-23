from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)


def create_positionnement_identite_page(c):
    """
    Page 14 : PARTIE 7 — Comment veux-je être identifié ?
    Identité, univers, incarnant et posture relationnelle.
    """
    layout = PageLayout(
        c,
        "7.1 : IDENTITÉ & UNIVERS DE MARQUE",
        config=LayoutConfig(part_title="7. MON POSITIONNEMENT"),
    )

    layout.add_text(
        "Votre positionnement n'est pas un slogan : c'est la place singulière et nette que vous prenez dans l'esprit "
        "de votre communauté. Il guide votre manière de communiquer, votre tarif et la relation que vous nouez.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    cards = [
        {
            "title": "1. Si mon Projet était une Personne",
            "subtitle": "Comment serait-elle ? Quel ton ? Quelle énergie ? Quels traits ?",
            "field_id": "bp_p14_personnalite",
            "placeholder": "Ex : Bienveillante mais sans complaisance, structurée, rassurante, pétillante...",
        },
        {
            "title": "2. 3 à 5 Mots décrivant mon Univers",
            "subtitle": "Les termes signatures qui définissent l'ambiance et la vibration...",
            "field_id": "bp_p14_mots_univers",
            "placeholder": "Ex : Clarté, Empathie, Rigueur, Action, Émancipation...",
        },
        {
            "title": "3. Ce que je Veux Incarner vs Refuser",
            "subtitle": "Ce que vous défendez fièrement vs ce que vous refusez catégoriquement...",
            "field_id": "bp_p14_incarner_refuser",
            "placeholder": "J'incarne le respect du rythme, je refuse les promesses miracles et le marketing agressif...",
        },
        {
            "title": "4. Niveau de Gamme & Expérience Client",
            "subtitle": "Accessible, équitable, premium ? Quelle relation humaine privilégiée ?",
            "field_id": "bp_p14_gamme_relation",
            "placeholder": "Accompagnement de proximité sur-mesure, écoute intime et grande disponibilité...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=7.6 * cm)
    layout.render()


def create_positionnement_pitch_page(c):
    """
    Page 15 : PARTIE 7 — Ma Phrase de Positionnement
    Laboratoire d'itération en 3 versions + Décision retenue.
    """
    layout = PageLayout(
        c,
        "7.2 : LABORATOIRE DE PITCH",
        config=LayoutConfig(part_title="7. MON POSITIONNEMENT"),
    )

    layout.add_text(
        "Une phrase de positionnement percutante ne naît jamais du premier coup de plume. "
        "Testez trois approches différentes (descriptive, transformatrice, audacieuse) avant d'élire votre formulation phare.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    pitch_versions = [
        {
            "title": "Version 1 : Factuelle & Descriptive",
            "subtitle": "Sobre et directe : Ce que vous faites, pour qui et avec quel moyen...",
            "field_id": "bp_p15_pitch_v1",
            "placeholder": "Ex : Je propose du conseil en organisation pour les artisanes indépendantes...",
        },
        {
            "title": "Version 2 : Axée sur la Transformation",
            "subtitle": "Centrée sur le bénéfice vécu et le passage d'un état A à un état B...",
            "field_id": "bp_p15_pitch_v2",
            "placeholder": "Ex : J'aide les créatrices à retrouver 10h de sérénité par semaine sans sacrifier leur CA...",
        },
        {
            "title": "Version 3 : Audacieuse & Différenciante",
            "subtitle": "Votre parti-pris singulier qui prend le contre-pied des habitudes du marché...",
            "field_id": "bp_p15_pitch_v3",
            "placeholder": "Ex : L'accompagnement qui réconcilie performance entrepreneuriale et écologie du repos...",
        },
    ]

    layout.add_cards_grid(pitch_versions, columns=3, card_height=6.2 * cm)

    layout.add_space(0.35 * cm)

    layout.add_question_block(
        "La formulation que je retiens aujourd'hui :",
        "bp_p15_pitch_retenu",
        config=QuestionConfig(
            box_height=5.5 * cm,
            subtitle="La synthèse qui résonne avec justesse et que vous aurez fierté à prononcer lors de vos rencontres professionnelles.",
            example="Ex : J'aide les femmes en reconversion à bâtir un projet professionnel rentable qui respecte leur santé et leurs valeurs profondes.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()
