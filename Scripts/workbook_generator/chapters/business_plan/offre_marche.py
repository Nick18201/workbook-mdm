from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionItem,
    QuestionConfig,
    TextConfig,
)


def create_offre_definition_page(c):
    """
    Page 9 : PARTIE 4 — Ce que je propose
    Définition claire du produit / service et périmètre (inclus vs non inclus).
    """
    layout = PageLayout(
        c,
        "4.1 : CE QUE JE PROPOSE CONCRÈTEMENT",
        config=LayoutConfig(part_title="4. MON OFFRE"),
    )

    layout.add_text(
        "Transformer le besoin identifié en une solution tangible, désirable et sécurisante pour la cliente. "
        "Être précise sur ce qui est fourni permet de vendre avec assurance et d'éviter les surcharges futures.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    layout.add_question_block(
        "Mon Produit / Service & l'Expérience vécue",
        "bp_p9_offre_description",
        config=QuestionConfig(
            box_height=4.2 * cm,
            subtitle="À quoi sert-il concrètement ? Que reçoit la personne ? Quelle expérience relationnelle lui faites-vous vivre ?",
            example="Ex : Un accompagnement individuel en 5 séances avec livret d'exercices et support WhatsApp entre les séances.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    cards = [
        {
            "title": "Ce qui est RIGOUREUSEMENT INCLUS",
            "subtitle": "Temps dédié, livrables, accès, ressources partagées...",
            "field_id": "bp_p9_offre_inclus",
            "placeholder": "Ex : 5 séances de 1h30, livret personnalisé, compte-rendu écrit après chaque séance...",
        },
        {
            "title": "Ce qui N'EST PAS INCLUS (Périmètre)",
            "subtitle": "Limites saines, conditions préalables, hors périmètre...",
            "field_id": "bp_p9_offre_exclus",
            "placeholder": "Ex : Disponibilité les week-ends, interventions d'urgence, prise en charge juridique ou comptable...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=7.0 * cm)
    layout.render()


def create_offre_valeur_page(c):
    """
    Page 10 : PARTIE 4 — Ma Proposition de Valeur
    Question centrale, différenciation et formulation du pitch promesse.
    """
    layout = PageLayout(
        c,
        "4.2 : MA PROPOSITION DE VALEUR",
        config=LayoutConfig(part_title="4. MON OFFRE"),
    )

    layout.add_callout(
        "« Pourquoi une personne choisirait-elle votre projet plutôt qu'une autre solution ou plutôt que de ne rien faire ? »",
        title="LA QUESTION PIVOT DU BUSINESS PLAN",
        variant="tip",
    )

    layout.add_space(0.2 * cm)

    questions = [
        QuestionItem(
            question="1. Le Bénéfice Principal & les Bénéfices Secondaires",
            form_field_id="bp_p10_benefices",
            subtitle="Quel est le résultat tangible promis ? Quels sont les bénéfices émotionnels (sérénité, fierté, clarté) ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="2. Ce qui rend mon approche unique et singulière",
            form_field_id="bp_p10_approche_differente",
            subtitle="Qu'est-ce qui vous distingue (votre histoire, votre méthode, votre énergie, votre éthique) ?",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
        QuestionItem(
            question="3. Formule de Pitch : Mon énoncé de valeur",
            form_field_id="bp_p10_pitch_promesse",
            subtitle="Complétez : « J'accompagne [Cible] qui rencontrent [Problème] grâce à [Solution], contrairement à [Alternatives]. »",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    ]

    layout.add_questions_group(questions, min_box_height=2.8 * cm, max_box_height=4.6 * cm)
    layout.render()


def create_marche_tendances_page(c):
    """
    Page 11 : PARTIE 5 — Mon Marché & ses Grandes Évolutions
    Secteur, tendances favorables/fragilisantes et conformité.
    """
    layout = PageLayout(
        c,
        "5.1 : MON MARCHÉ & TENDANCES",
        config=LayoutConfig(part_title="5. ÉTUDIER LE MARCHÉ"),
    )

    layout.add_text(
        "Comprendre dans quel environnement vous vous inscrivez. Les tendances sociétales, technologiques ou réglementaires "
        "peuvent constituer des vents porteurs puissants ou des obstacles à anticiper dès maintenant.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    layout.add_question_block(
        "Dans quel marché et secteur d'activité est-ce que je me situe ?",
        "bp_p11_marche_secteur",
        config=QuestionConfig(
            box_height=3.2 * cm,
            subtitle="Définissez votre domaine (ex : coaching pro, artisanat d'art, services aux familles, formation, bien-être...).",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    tendances_cards = [
        {
            "title": "Tendances Favorables (Vents porteurs)",
            "subtitle": "Quelles évolutions sociétales ou technologiques favorisent votre projet ?",
            "field_id": "bp_p11_tendances_favorables",
            "placeholder": "Ex : Besoin croissant de déconnexion, quête de sens, essor du télétravail...",
        },
        {
            "title": "Tendances Fragilisantes (Risques du marché)",
            "subtitle": "Quels changements économiques ou concurrentiels peuvent fragiliser l'activité ?",
            "field_id": "bp_p11_tendances_risques",
            "placeholder": "Ex : Baisse du pouvoir d'achat, saturation d'un canal, montée de solutions IA gratuites...",
        },
    ]
    layout.add_cards_grid(tendances_cards, columns=2, card_height=5.6 * cm)

    layout.add_question_block(
        "Quelles réglementations, normes ou obligations dois-je impérativement connaître ?",
        "bp_p11_reglementations",
        config=QuestionConfig(
            box_height=3.2 * cm,
            subtitle="Diplômes requis, normes ERP, RGPD, médiation de la consommation, assurances spécifiques...",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()


def create_marche_concurrents_page(c):
    """
    Page 12 : PARTIE 5 — Mes Concurrents et Alternatives
    Les 4 familles d'acteurs et fiche d'analyse comparative de 2 concurrents.
    """
    layout = PageLayout(
        c,
        "5.2 : CONCURRENTS & ALTERNATIVES",
        config=LayoutConfig(part_title="5. ÉTUDIER LE MARCHÉ"),
    )

    layout.add_text(
        "Ne limitez jamais votre veille aux concurrents directs : intégrez les concurrents indirects, les solutions bricolées "
        "et surtout le choix n°1 de beaucoup de prospects : l'inaction (« ne rien faire »).",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    layout.add_checklist(
        items=[
            ("Concurrents directs : même offre, même cible", "bp_p12_chk_directs"),
            ("Concurrents indirects : offre différente pour même besoin", "bp_p12_chk_indirects"),
            ("Alternatives : méthodes maison, systèmes D, livres, tutos", "bp_p12_chk_alternatives"),
            ("L'Inaction : ne rien changer et subir la situation", "bp_p12_chk_inaction"),
        ],
        title="LES 4 FAMILLES D'ACTEURS À OBSERVER :",
        columns=2,
    )

    cards = [
        {
            "title": "Acteur / Concurrent Clé n°1",
            "subtitle": "Nom, offre, tarifs, forces observées et limites...",
            "field_id": "bp_p12_concurrent_1",
            "placeholder": "Nom : ...\nOffre & Prix : ...\nForces : ...\nCe que je peux apprendre ou faire différemment : ...",
        },
        {
            "title": "Acteur / Alternative Clé n°2",
            "subtitle": "Nom, offre, tarifs, forces observées et limites...",
            "field_id": "bp_p12_concurrent_2",
            "placeholder": "Nom : ...\nOffre & Prix : ...\nForces : ...\nCe que je peux apprendre ou faire différemment : ...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=10.0 * cm)
    layout.render()


def create_marche_benchmark_page(c):
    """
    Page 13 : PARTIE 6 — Benchmark & Projets Inspirants
    Tableau comparatif multicritères + Synthèse décisionnelle.
    """
    layout = PageLayout(
        c,
        "6.1 : BENCHMARK & INSPIRATIONS",
        config=LayoutConfig(part_title="6. S'INSPIRER DE PROJETS EXISTANTS"),
    )

    layout.add_text(
        "Observez des projets inspirants en France, en Europe ou au Québec. "
        "L'objectif n'est pas de copier mais de comprendre ce qui fonctionne et de révéler votre propre singularité.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    headers = [
        "Projet Inspirant (Nom & Lieu)",
        "Concept & Public Visé",
        "Offre & Modèle Économique",
        "Particularité / Force",
    ]

    widths = [
        0.25 * layout.target_width,
        0.25 * layout.target_width,
        0.26 * layout.target_width,
        0.24 * layout.target_width,
    ]

    rows = [
        [
            {"field_id": "bp_p13_bench1_nom", "placeholder": "Projet A (ex : École libre...)"},
            {"field_id": "bp_p13_bench1_concept", "placeholder": "Accompagnement de..."},
            {"field_id": "bp_p13_bench1_modele", "placeholder": "Abonnement mensuel..."},
            {"field_id": "bp_p13_bench1_force", "placeholder": "Communauté très active..."},
        ],
        [
            {"field_id": "bp_p13_bench2_nom", "placeholder": "Projet B (ex : Agence éthique...)"},
            {"field_id": "bp_p13_bench2_concept", "placeholder": "Ateliers collectifs..."},
            {"field_id": "bp_p13_bench2_modele", "placeholder": "Forfait sur devis..."},
            {"field_id": "bp_p13_bench2_force", "placeholder": "Marque forte et engagée..."},
        ],
        [
            {"field_id": "bp_p13_bench3_nom", "placeholder": "Projet C (ex : Tiers-lieu rural...)"},
            {"field_id": "bp_p13_bench3_concept", "placeholder": "Événements & espace partagé..."},
            {"field_id": "bp_p13_bench3_modele", "placeholder": "Hybride (public + privé)..."},
            {"field_id": "bp_p13_bench3_force", "placeholder": "Partenariats locaux solides..."},
        ],
        [
            {"field_id": "bp_p13_bench4_nom", "placeholder": "Projet D (ex : Plateforme atelier...)"},
            {"field_id": "bp_p13_bench4_concept", "placeholder": "Vente directe & transmission..."},
            {"field_id": "bp_p13_bench4_modele", "placeholder": "Modèle mixte créateur..."},
            {"field_id": "bp_p13_bench4_force", "placeholder": "Identité visuelle remarquable..."},
        ],
    ]

    layout.add_table(headers, rows, col_widths=widths, field_prefix="tbl_bench")

    layout.add_space(0.35 * cm)

    questions = [
        QuestionItem(
            question="Les idées fortes que je retiens et que je pourrais adapter",
            form_field_id="bp_p13_idees_adaptees",
            subtitle="Quelles bonnes pratiques découvrez-vous chez ces pionniers ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="Ce que je ne veux SURTOUT PAS reproduire",
            form_field_id="bp_p13_idees_refusees",
            subtitle="Quels écueils, lourdeurs ou manques observez-vous chez eux que vous refusez ?",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    ]

    layout.add_questions_group(questions, min_box_height=2.8 * cm, max_box_height=4.2 * cm)
    layout.render()
