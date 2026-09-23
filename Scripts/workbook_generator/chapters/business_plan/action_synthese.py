from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)
from workbook_generator.components import (
    create_standard_roadmap_page,
    create_standard_engagement_page,
)


def create_action_mvp_page(c):
    """
    Page 30 : PARTIE 18 — Tester avant de se lancer : MVP & Enquête Terrain
    Minimum Viable Product, critères de suite/pivot et enseignements d'interviews.
    """
    layout = PageLayout(
        c,
        "18.1 : EXPÉRIMENTATION MVP & ENQUÊTE",
        config=LayoutConfig(part_title="18. TESTER AVANT DE SE LANCER"),
    )

    layout.add_callout(
        "« Quelle est la plus petite version de mon projet que je peux tester en moins de 30 jours et à moindre coût ? »",
        title="LE PRINCIPE DU MINIMUM VIABLE PRODUCT (MVP)",
        variant="tip",
    )

    layout.add_space(0.2 * cm)

    cards = [
        {
            "title": "1. Mon MVP (Expérimentation Minimale)",
            "subtitle": "Que pouvez-vous tester immédiatement ? Avec qui ? Sous quel format léger ?",
            "field_id": "bp_p30_mvp_definition",
            "placeholder": "Ex : Proposer 3 ateliers pilotes gratuits ou à prix libre auprès de 5 connaissances cibles...",
        },
        {
            "title": "2. Critères de Décision (Continuer ou Pivoter)",
            "subtitle": "Quel résultat vous encouragera à foncer ? Quel retour vous fera réajuster ?",
            "field_id": "bp_p30_mvp_criteres",
            "placeholder": "Si au moins 2 personnes recommandent l'atelier sans hésiter, je valide l'offre...",
        },
        {
            "title": "3. Mon Guide d'Interviews Terrain",
            "subtitle": "Qui interroger ? Quelles questions neutres poser pour comprendre sans vendre ?",
            "field_id": "bp_p30_interviews_guide",
            "placeholder": "« Racontez-moi la dernière fois où vous avez rencontré ce problème... Comment avez-vous fait ? »...",
        },
        {
            "title": "4. Ce que mes Tests m'ont Appris (Surprises)",
            "subtitle": "Quels retours inattendus confirment ou bousculent vos certitudes de départ ?",
            "field_id": "bp_p30_interviews_surprises",
            "placeholder": "J'ai découvert qu'elles demandent surtout un modèle prêt à l'emploi plutôt que de la théorie...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=7.0 * cm)
    layout.render()


def create_action_risques_page(c):
    """
    Page 31 : PARTIE 19 — Risques et Incertitudes & les 5 Hypothèses Vitales
    Matrice des risques et analyse des 5 conditions sine qua non de réussite.
    """
    layout = PageLayout(
        c,
        "19.1 : RISQUES & HYPOTHÈSES VITALES",
        config=LayoutConfig(part_title="19. RISQUES ET INCERTITUDES"),
    )

    layout.add_text(
        "Être lucide sur ses vulnérabilités n'est pas être pessimiste : c'est se donner les moyens d'y faire face sereinement. "
        "Formalisez vos plans de secours et identifiez les 5 vérités sans lesquelles votre projet s'arrête.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    headers = [
        "Risque Majeur Identifié",
        "Gravité & Probabilité",
        "Mesure de Prévention",
        "Plan B de Secours",
    ]

    widths = [
        0.28 * layout.target_width,
        0.20 * layout.target_width,
        0.26 * layout.target_width,
        0.26 * layout.target_width,
    ]

    rows = [
        [
            {"field_id": "bp_p31_r1_nom", "placeholder": "Démarrage commercial plus lent que prévu"},
            {"field_id": "bp_p31_r1_grav", "placeholder": "Forte / Moyenne"},
            {"field_id": "bp_p31_r1_prev", "placeholder": "Constituer 6 mois de trésorerie"},
            {"field_id": "bp_p31_r1_planb", "placeholder": "Missions ponctuelles de sous-traitance"},
        ],
        [
            {"field_id": "bp_p31_r2_nom", "placeholder": "Fatigue / surcharge mentale"},
            {"field_id": "bp_p31_r2_grav", "placeholder": "Moyenne / Forte"},
            {"field_id": "bp_p31_r2_prev", "placeholder": "Bloquer un jour off par semaine"},
            {"field_id": "bp_p31_r2_planb", "placeholder": "Réduire le nombre de clientes actives"},
        ],
        [
            {"field_id": "bp_p31_r3_nom", "placeholder": "Évolution réglementaire défavorable"},
            {"field_id": "bp_p31_r3_grav", "placeholder": "Moyenne / Faible"},
            {"field_id": "bp_p31_r3_prev", "placeholder": "Veille syndicale et juridique"},
            {"field_id": "bp_p31_r3_planb", "placeholder": "Adapter la prestation en conseil pur"},
        ],
        [
            {"field_id": "bp_p31_r4_nom", "placeholder": "Baisse temporaire de motivation / doutes"},
            {"field_id": "bp_p31_r4_grav", "placeholder": "Faible / Fréquente"},
            {"field_id": "bp_p31_r4_prev", "placeholder": "Binôme d'action & mentorat bimensuel"},
            {"field_id": "bp_p31_r4_planb", "placeholder": "Prendre 3 jours de recul et relire ma vision"},
        ],
    ]

    layout.add_table(headers, rows, col_widths=widths, field_prefix="tbl_risques")

    layout.add_space(0.4 * cm)

    layout.add_question_block(
        "Les 5 Hypothèses Vitales (Ce qui DOIT être vrai pour réussir)",
        "bp_p31_hypotheses_vitales",
        config=QuestionConfig(
            box_height=5.6 * cm,
            subtitle="Quelles sont les 5 conditions indispensables dont dépend la survie de votre projet ? Comment les surveiller ?",
            example="1. Les clientes reconnaissent ce problème comme urgent • 2. Elles ont le budget disponible • 3. Mon canal LinkedIn génère 2 leads/mois • 4. Je délivre en 5h max • 5. Mon écologie de vie est préservée.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()


def create_action_roadmap_page(c):
    """
    Page 32 : PARTIE 20 — Mon Plan d'Action : Feuille de Route
    Utilise le gabarit officiel create_standard_roadmap_page en 3 paliers progressifs.
    """
    stages = [
        {
            "period": "PALIER 1 · 0 À 30 JOURS",
            "theme": "CADRAGE & TERRAIN",
            "default_obj": "Valider l'intérêt du marché et tester l'offre pilote auprès de 5 pairs.",
            "actions": [
                "Mener 5 entretiens d'enquête terrain ciblés sans chercher à vendre",
                "Formaliser la fiche de l'offre pilote et la grille tarifaire",
                "Contacter 10 personnes du réseau tiède pour annoncer la démarche",
            ],
            "default_kpi": "5 entretiens qualifiés menés et 2 personnes prêtes à tester",
        },
        {
            "period": "PALIER 2 · 30 À 90 JOURS",
            "theme": "LANCEMENT DU MVP",
            "default_obj": "Délivrer les premières prestations pilotes et sécuriser le cadre légal.",
            "actions": [
                "Finaliser l'immatriculation et l'assurance professionnelle (RC Pro)",
                "Accompagner 3 clientes pilotes et recueillir leurs témoignages écrits",
                "Lancer la communication régulière sur mon canal prioritaire",
            ],
            "default_kpi": "3 clientes accompagnées avec succès et 2 recommandations obtenues",
        },
        {
            "period": "PALIER 3 · 3 À 6 MOIS",
            "theme": "CONSOLIDATION & CROISIÈRE",
            "default_obj": "Atteindre le seuil de rentabilité mensuel et pérenniser la méthode.",
            "actions": [
                "Signer 3 à 4 nouveaux accompagnements au tarif plein",
                "Nouer 2 partenariats stratégiques de prescription",
                "Faire le premier bilan financier et ajuster le tableau de bord",
            ],
            "default_kpi": "Chiffre d'affaires mensuel stable supérieur à mon point mort",
        },
    ]

    create_standard_roadmap_page(
        c,
        title="Feuille de Route : Mes Prochains Jalons",
        part_title="20. MON PLAN D'ACTION",
        intro_text="Découpez votre lancement en trois paliers temporels clairs pour ancrer des victoires rapides et garder le cap sans dispersion.",
        stages_data=stages,
        field_prefix="bp_p32_road",
    )


def create_synthese_executive_page(c):
    """
    Page 33 : PARTIE 21 — Le Business Plan Final : Executive Summary
    La fiche d'impact en 1 page synthétisant tout le projet pour des tiers (banques, partenaires, jurys).
    """
    layout = PageLayout(
        c,
        "21.1 : EXECUTIVE SUMMARY (SYNTHÈSE)",
        config=LayoutConfig(part_title="21. SYNTHÈSE DU BUSINESS PLAN"),
    )

    layout.add_text(
        "L'Executive Summary est le condensé exécutif de votre projet. C'est la page que lira en premier un partenaire, "
        "un financeur ou un mentor pour évaluer la clarté, l'alignement et la solidité de votre démarche.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    summary_cards = [
        {
            "title": "1. Le Projet & sa Raison d'Être",
            "subtitle": "Nom du projet, mission centrale et déclic personnel...",
            "field_id": "bp_p33_exec_projet",
            "placeholder": "Présentation concise du projet et de la mission sociétale...",
        },
        {
            "title": "2. La Cible & le Problème Résolu",
            "subtitle": "Pour qui ? Quelle douleur majeure et fréquente comblez-vous ?",
            "field_id": "bp_p33_exec_cible",
            "placeholder": "Profil type de cliente et difficulté quotidienne résolue...",
        },
        {
            "title": "3. L'Offre & la Proposition de Valeur",
            "subtitle": "Vos prestations phares et ce qui rend votre approche unique...",
            "field_id": "bp_p33_exec_offre",
            "placeholder": "Formules proposées, promesse et singularité concurrentielle...",
        },
        {
            "title": "4. Le Marché & les Opportunités",
            "subtitle": "Secteur porteur, tendances favorables et positionnement clé...",
            "field_id": "bp_p33_exec_marche",
            "placeholder": "Taille de marché, vents porteurs et différenciation...",
        },
        {
            "title": "5. Modèle Économique & Chiffres Clés",
            "subtitle": "Prix moyen, seuil de rentabilité et CA prévisionnel an 1...",
            "field_id": "bp_p33_exec_finances",
            "placeholder": "Prix forfaits, point mort mensuel et scénario cible...",
        },
        {
            "title": "6. Besoin de Financement & Échéance Clé",
            "subtitle": "Montant recherché, statut juridique et date de lancement...",
            "field_id": "bp_p33_exec_besoins",
            "placeholder": "Besoin de démarrage, apport personnel et prochain jalon...",
        },
    ]

    layout.add_cards_grid(summary_cards, columns=2, card_height=5.7 * cm)
    layout.render()


def create_engagement_signature_page(c):
    """
    Page 34 : PARTIE 22 — Mon Pacte d'Engagement d'Entrepreneure
    Pacte officiel avec signature interactive AcroForm.
    """
    lignes_engagement = [
        "Je m'engage à faire confiance à mon intuition tout en confrontant mes hypothèses au terrain avec lucidité.",
        "À regarder mes chiffres, mes devis et mes finances avec honnêteté, sans fuite ni déni.",
        "À accepter l'imperfection des débuts et à tester vite pour apprendre avec bienveillance.",
        "À poser des limites saines pour préserver mon énergie vitale, ma santé et mon équilibre de vie.",
        "À incarner fièrement la valeur de mon travail et à faire grandir mon projet pas à pas avec audace.",
    ]

    create_standard_engagement_page(
        c,
        part_title="22. ENGAGEMENT & PASSAGE À L'ACTION",
        custom_lines=lignes_engagement,
        title="Mon Pacte d'Action & d'Audace",
        signature_label="Fait à ..., le ... et Signature :",
    )
