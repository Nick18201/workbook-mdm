from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionItem,
    QuestionConfig,
    TextConfig,
)


def create_cible_public_page(c):
    """
    Page 5 : PARTIE 2 — Les Personnes que je veux accompagner / servir
    Ne pas commencer par le produit, mais par les personnes concernées.
    """
    layout = PageLayout(
        c,
        "2.1 : MON PUBLIC CIBLE",
        config=LayoutConfig(part_title="2. COMPRENDRE À QUI JE M'ADRESSE"),
    )

    layout.add_text(
        "Ne commencez jamais par concevoir votre produit ou votre service : commencez par les personnes. "
        "Pour qui voulez-vous créer de la valeur ? Dans quelle situation concrète se trouvent-elles aujourd'hui, "
        "et qu'est-ce qui leur pèse réellement dans leur quotidien professionnel ou personnel ?",
        config=TextConfig(spacing_after=0.45 * cm),
    )

    questions = [
        QuestionItem(
            question="1. Qui sont les personnes que je veux accompagner / servir ?",
            form_field_id="bp_p5_qui_cible",
            subtitle="Précisez leur situation : statut, contexte de vie, activité, environnement...",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="2. Quels sont leurs besoins profonds et difficultés actuelles ?",
            form_field_id="bp_p5_besoins_difficultes",
            subtitle="Quelles épreuves ou irritants rencontrent-elles ? Que recherchent-elles en priorité ?",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
        QuestionItem(
            question="3. Que font-elles ou qu'utilisent-elles déjà aujourd'hui ?",
            form_field_id="bp_p5_solutions_actuelles",
            subtitle="Quelles alternatives ou solutions imparfaites bricolent-elles pour y répondre sans vous ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    ]

    layout.add_questions_group(questions, min_box_height=2.8 * cm, max_box_height=4.8 * cm)
    layout.render()


def create_cible_persona_page(c):
    """
    Page 6 : PARTIE 2 — Mon Persona Type & Matrice de Lucidité
    Fiche profil reproductible + Distinction Certitudes vs Hypothèses.
    """
    layout = PageLayout(
        c,
        "2.2 : FICHE PERSONA & MATRICE DE LUCIDITÉ",
        config=LayoutConfig(part_title="2. COMPRENDRE À QUI JE M'ADRESSE"),
    )

    layout.add_text(
        "Donnez un visage concret à votre public cible en dressant le portrait d'une personne type. "
        "Distinguez impérativement ce que vous observez de façon certaine de ce qui relève encore d'hypothèses à tester.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    # Grille 1 : Portrait du Persona
    persona_cards = [
        {
            "title": "Profil Type & Contexte",
            "subtitle": "Prénom fictif, âge, métier, contexte de vie et habitudes...",
            "field_id": "bp_p6_persona_profil",
            "placeholder": "Ex : Claire, 38 ans, cadre en quête de sens...",
        },
        {
            "title": "Freins, Craintes & Motivations",
            "subtitle": "Ce qui l'empêche d'agir vs ce qui la fait avancer...",
            "field_id": "bp_p6_persona_freins",
            "placeholder": "Peur de se tromper, manque de temps, désir d'autonomie...",
        },
    ]
    layout.add_cards_grid(persona_cards, columns=2, card_height=6.8 * cm)

    # Grille 2 : Matrice de Lucidité (Ce que je pense savoir vs Ce que je dois vérifier)
    lucidite_cards = [
        {
            "title": "Ce que je PENSE savoir (Mes Intuitions)",
            "subtitle": "Mes croyances spontanées sur ses attentes et son budget...",
            "field_id": "bp_p6_lucidite_pense",
            "placeholder": "Je pense qu'elle est prête à payer pour gagner du temps...",
        },
        {
            "title": "Ce que je DOIS encore Vérifier sur le terrain",
            "subtitle": "Les angles morts et questions à lui poser directement...",
            "field_id": "bp_p6_lucidite_verifier",
            "placeholder": "Vérifier si ce problème est une priorité budgétaire...",
        },
    ]
    layout.add_cards_grid(lucidite_cards, columns=2, card_height=6.8 * cm)

    layout.render()


def create_probleme_analyse_page(c):
    """
    Page 7 : PARTIE 3 — Quel Problème est-ce que je cherche à résoudre ?
    Analyse approfondie de la friction ou douleur.
    """
    layout = PageLayout(
        c,
        "3.1 : QUEL PROBLÈME RÉSOUDRE ?",
        config=LayoutConfig(part_title="3. LE BESOIN ET LE PROBLÈME"),
    )

    layout.add_text(
        "Un projet viable ne repose pas uniquement sur une bonne idée : il doit soulager un problème ou combler "
        "un manque réel, ressenti et prioritaire. Plus le problème est douloureux et fréquent, plus la solution a de la valeur.",
        config=TextConfig(spacing_after=0.45 * cm),
    )

    questions = [
        QuestionItem(
            question="1. Le problème que j'ai identifié (Description précise)",
            form_field_id="bp_p7_probleme_desc",
            subtitle="Quelle est la douleur, la frustration ou la perte de temps/argent constatée ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="2. Pour qui ce problème existe-t-il, à quelle fréquence et avec quelle importance ?",
            form_field_id="bp_p7_probleme_intensite",
            subtitle="Est-ce un problème vital, urgent, régulier ou secondaire ? Qui en souffre le plus ?",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
        QuestionItem(
            question="3. Comment font les personnes aujourd'hui et pourquoi les solutions actuelles ne suffisent-elles pas ?",
            form_field_id="bp_p7_probleme_limites",
            subtitle="Quels sont les manques des offres existantes (trop chères, impersonnelles, complexes...) ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    ]

    layout.add_questions_group(questions, min_box_height=2.8 * cm, max_box_height=4.8 * cm)
    layout.render()


def create_probleme_hypotheses_page(c):
    """
    Page 8 : PARTIE 3 — Mes Hypothèses à Vérifier sur le Terrain
    Tableau structuré d'hypothèses + retour d'enquête terrain.
    """
    layout = PageLayout(
        c,
        "3.2 : MES HYPOTHÈSES À VÉRIFIER",
        config=LayoutConfig(part_title="3. LE BESOIN ET LE PROBLÈME"),
    )

    layout.add_text(
        "Formulez vos hypothèses sous forme de paris à tester. L'enquête de terrain vous permettra de transformer "
        "des suppositions en certitudes opérationnelles ou d'ajuster votre approche avant d'engager des frais.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    headers = [
        "Hypothèse Clé",
        "Pourquoi je le pense ?",
        "Comment la tester concrètement ?",
        "Résultat / Observation",
    ]

    widths = [
        0.28 * layout.target_width,
        0.24 * layout.target_width,
        0.26 * layout.target_width,
        0.22 * layout.target_width,
    ]

    rows = [
        [
            {"field_id": "bp_p8_hyp1_texte", "placeholder": "Hypothèse 1 : Les personnes manquent de..."},
            {"field_id": "bp_p8_hyp1_pourquoi", "placeholder": "Vu dans 3 témoignages récents..."},
            {"field_id": "bp_p8_hyp1_comment", "placeholder": "Questionner 5 personnes cibles..."},
            {"field_id": "bp_p8_hyp1_resultat", "placeholder": "Confirmé / Invalidé : détails..."},
        ],
        [
            {"field_id": "bp_p8_hyp2_texte", "placeholder": "Hypothèse 2 : Elles sont prêtes à investir..."},
            {"field_id": "bp_p8_hyp2_pourquoi", "placeholder": "Car le coût du statu quo est fort..."},
            {"field_id": "bp_p8_hyp2_comment", "placeholder": "Demander quel budget elles consacrent..."},
            {"field_id": "bp_p8_hyp2_resultat", "placeholder": "Budget confirmé entre X et Y €..."},
        ],
        [
            {"field_id": "bp_p8_hyp3_texte", "placeholder": "Hypothèse 3 : Le format idéal est..."},
            {"field_id": "bp_p8_hyp3_pourquoi", "placeholder": "Manque de disponibilité en journée..."},
            {"field_id": "bp_p8_hyp3_comment", "placeholder": "Tester 2 créneaux en sondage..."},
            {"field_id": "bp_p8_hyp3_resultat", "placeholder": "Préférence nette pour le soir / visio..."},
        ],
        [
            {"field_id": "bp_p8_hyp4_texte", "placeholder": "Hypothèse 4 : Le canal de contact prioritaire est..."},
            {"field_id": "bp_p8_hyp4_pourquoi", "placeholder": "Présence active sur les réseaux pro..."},
            {"field_id": "bp_p8_hyp4_comment", "placeholder": "Publier un post d'accroche et mesurer..."},
            {"field_id": "bp_p8_hyp4_resultat", "placeholder": "Retours directs et intérêt validé..."},
        ],
    ]

    layout.add_table(headers, rows, col_widths=widths, field_prefix="tbl_hyp")

    layout.add_space(0.4 * cm)

    layout.add_question_block(
        "Ce que mes recherches et mes échanges de terrain m'ont appris",
        "bp_p8_enseignements_recherche",
        config=QuestionConfig(
            box_height=5.6 * cm,
            subtitle="Quels sont les retours majeurs, les surprises et les prises de conscience suite à vos premières investigations ?",
            example="Ex : J'ai découvert que le besoin n'était pas tant technique qu'émotionnel (besoin de réassurance et de cadre sécurisant).",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()
