from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionItem,
    QuestionConfig,
    TextConfig,
)


def create_communication_message_page(c):
    """
    Page 22 : PARTIE 12 — Communication : Mon Identité & mon Message
    Message central, messages secondaires, ton et lignes rouges.
    """
    layout = PageLayout(
        c,
        "12.1 : IDENTITÉ DE MESSAGE & TON",
        config=LayoutConfig(part_title="12. COMMUNICATION"),
    )

    layout.add_text(
        "Communiquer, ce n'est pas faire du bruit : c'est transmettre avec clarté votre vision du monde et vos convictions. "
        "Votre message doit être immédiatement reconnaissable et aligné avec votre voix authentique.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    questions = [
        QuestionItem(
            question="1. Mon message principal (L'idée directrice incontournable)",
            form_field_id="bp_p22_message_principal",
            subtitle="Quelle conviction fondamentale souhaitez-vous répéter avec constance à votre communauté ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="2. Mes messages secondaires et piliers de contenu",
            form_field_id="bp_p22_messages_secondaires",
            subtitle="Quels sont vos 3 grands thèmes de prédilection (ex : organisation, écologie personnelle, méthode...) ?",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
        QuestionItem(
            question="3. Mon ton d'expression & mes mots signatures",
            form_field_id="bp_p22_ton_expression",
            subtitle="Plutôt chaleureux et complice ? Structuré et directif ? Pédagogue et imagé ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="4. Ce que je refuse catégoriquement de communiquer (Mes Lignes Rouges)",
            form_field_id="bp_p22_refus_communication",
            subtitle="Les discours culpabilisants, les astuces miracles ou les codes marketing que vous rejetez fermement.",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    ]

    layout.add_questions_group(questions, min_box_height=2.2 * cm, max_box_height=3.4 * cm)
    layout.render()


def create_communication_plan_page(c):
    """
    Page 23 : PARTIE 12 — Mon Plan de Communication Opérationnel
    Tableau des canaux et contenus + engagement de régularité.
    """
    layout = PageLayout(
        c,
        "12.2 : PLAN DE COMMUNICATION OPÉRATIONNEL",
        config=LayoutConfig(part_title="12. COMMUNICATION"),
    )

    layout.add_text(
        "Mieux vaut un seul canal tenu avec une régularité exemplaire que cinq comptes de réseaux sociaux abandonnés. "
        "Calibrez votre plan de communication en fonction du temps dont vous disposez réellement chaque semaine.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    headers = [
        "Canal Choisi",
        "Objectif Visé",
        "Type de Contenu",
        "Fréquence",
        "Temps / Semaine",
    ]

    widths = [
        0.20 * layout.target_width,
        0.22 * layout.target_width,
        0.28 * layout.target_width,
        0.15 * layout.target_width,
        0.15 * layout.target_width,
    ]

    rows = [
        [
            {"field_id": "bp_p23_c1_nom", "placeholder": "LinkedIn"},
            {"field_id": "bp_p23_c1_obj", "placeholder": "Notoriété & autorité"},
            {"field_id": "bp_p23_c1_contenu", "placeholder": "Retours d'expérience, conseils"},
            {"field_id": "bp_p23_c1_freq", "placeholder": "2 posts / sem."},
            {"field_id": "bp_p23_c1_temps", "placeholder": "2h"},
        ],
        [
            {"field_id": "bp_p23_c2_nom", "placeholder": "Newsletter"},
            {"field_id": "bp_p23_c2_obj", "placeholder": "Lien intime & confiance"},
            {"field_id": "bp_p23_c2_contenu", "placeholder": "Réflexions approfondies"},
            {"field_id": "bp_p23_c2_freq", "placeholder": "Tous les 15 jours"},
            {"field_id": "bp_p23_c2_temps", "placeholder": "1h30"},
        ],
        [
            {"field_id": "bp_p23_c3_nom", "placeholder": "Réseau Local"},
            {"field_id": "bp_p23_c3_obj", "placeholder": "Recommandations"},
            {"field_id": "bp_p23_c3_contenu", "placeholder": "Déjeuners & ateliers"},
            {"field_id": "bp_p23_c3_freq", "placeholder": "1 fois / mois"},
            {"field_id": "bp_p23_c3_temps", "placeholder": "3h"},
        ],
        [
            {"field_id": "bp_p23_c4_nom", "placeholder": "Bouche-à-oreille"},
            {"field_id": "bp_p23_c4_obj", "placeholder": "Prescription directe"},
            {"field_id": "bp_p23_c4_contenu", "placeholder": "Échanges pairs & retours"},
            {"field_id": "bp_p23_c4_freq", "placeholder": "Continu"},
            {"field_id": "bp_p23_c4_temps", "placeholder": "1h"},
        ],
    ]

    layout.add_table(headers, rows, col_widths=widths, field_prefix="tbl_com")

    layout.add_space(0.4 * cm)

    cards = [
        {
            "title": "Mon Rythme de Publication Soutenable",
            "subtitle": "Quel rituel de création hebdomadaire pouvez-vous respecter avec plaisir ?",
            "field_id": "bp_p23_rituel_creation",
            "placeholder": "Ex : Bloquer le mardi matin pour rédiger l'ensemble des contenus de la quinzaine...",
        },
        {
            "title": "Le Message Clé d'Appel à l'Action (CTA)",
            "subtitle": "Vers quoi orientez-vous systématiquement vos lecteurs intéressés ?",
            "field_id": "bp_p23_call_to_action",
            "placeholder": "Ex : « Réservez votre séance d'alignement de 30 minutes offerte via mon calendrier en ligne »...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=6.8 * cm)
    layout.render()


def create_ressources_moyens_page(c):
    """
    Page 24 : PARTIE 13 — Les Ressources Nécessaires pour Démarrer
    Inventaire matériel, arbitrages logistiques et faire vs déléguer.
    """
    layout = PageLayout(
        c,
        "13.1 : RESSOURCES & ARBITRAGES",
        config=LayoutConfig(part_title="13. LES RESSOURCES NÉCESSAIRES"),
    )

    layout.add_text(
        "Faire l'inventaire précis de ce dont vous avez besoin pour exercer votre métier sereinement. "
        "Privilégiez la légèreté au démarrage : acheter uniquement l'indispensable, louer ou mutualiser le reste.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    layout.add_checklist(
        items=[
            ("Matériel informatique & téléphonie fiable", "bp_p24_chk_info"),
            ("Espace de travail calme (bureau ou tiers-lieu)", "bp_p24_chk_local"),
            ("Outils numériques (visio, compta, CRM, agenda)", "bp_p24_chk_outils"),
            ("Fournisseurs ou matières premières sécurisés", "bp_p24_chk_fournisseurs"),
            ("Accompagnement comptable & juridique dédié", "bp_p24_chk_compta"),
            ("Compétences techniques spécifiques à acquérir", "bp_p24_chk_competences"),
        ],
        title="RESSOURCES NÉCESSAIRES POUR DÉMARRER :",
        columns=2,
    )

    cards = [
        {
            "title": "1. Ce que j'AI DÉJÀ sous la main",
            "subtitle": "Matériel, compétences acquises, carnet d'adresses disponible...",
            "field_id": "bp_p24_ressources_dispo",
            "placeholder": "Ordinateur récent, réseau d'anciennes collègues, compétences rédactionnelles...",
        },
        {
            "title": "2. Ce qui me MANQUE impérativement",
            "subtitle": "Les investissements ou acquisitions prioritaires pour ouvrir...",
            "field_id": "bp_p24_ressources_manque",
            "placeholder": "Assurance pro, identité visuelle claire, logiciel de facturation conforme...",
        },
        {
            "title": "3. Acheter, Louer ou Mutualiser ?",
            "subtitle": "Quels arbitrages pour limiter vos charges fixes initiales ?",
            "field_id": "bp_p24_arbitrage_logistique",
            "placeholder": "Mutualiser un bureau 2 jours/semaine, utiliser des outils freemium au début...",
        },
        {
            "title": "4. Ce que je FAIS vs ce que je DÉLÈGUE",
            "subtitle": "Préservez votre énergie vitale pour votre cœur de valeur ajoutée...",
            "field_id": "bp_p24_faire_deleguer",
            "placeholder": "Je fais l'accompagnement et la com ; je délègue la déclaration fiscale et le webdesign...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=6.0 * cm)
    layout.render()


def create_ressources_competences_page(c):
    """
    Page 25 : PARTIE 14 — Moi, mes Compétences et mon Écosystème
    Tableau des compétences + identification des personnes ressources.
    """
    layout = PageLayout(
        c,
        "14.1 : COMPÉTENCES & ÉCOSYSTÈME",
        config=LayoutConfig(part_title="14. MOI ET LE PROJET"),
    )

    layout.add_text(
        "Vous êtes le premier actif de votre entreprise. Prendre la mesure de vos forces, identifier avec humilité "
        "vos axes de progression et vous entourer de personnes bienveillantes et compétentes est la clé de la longévité.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    headers = [
        "Domaine de Compétence",
        "Niveau Actuel (1 à 5)",
        "Importance Projet",
        "Plan de Montée en Compétences",
    ]

    widths = [
        0.28 * layout.target_width,
        0.18 * layout.target_width,
        0.18 * layout.target_width,
        0.36 * layout.target_width,
    ]

    rows = [
        [
            "Cœur de Métier / Expertise",
            {"field_id": "bp_p25_c1_niv", "placeholder": "5/5 (Maîtrisé)"},
            {"field_id": "bp_p25_c1_imp", "placeholder": "Vitale"},
            {"field_id": "bp_p25_c1_plan", "placeholder": "Veille continue et lectures spécialisées..."},
        ],
        [
            "Posture Commerciale & Vente",
            {"field_id": "bp_p25_c2_niv", "placeholder": "2/5 (À renforcer)"},
            {"field_id": "bp_p25_c2_imp", "placeholder": "Prioritaire"},
            {"field_id": "bp_p25_c2_plan", "placeholder": "Simulations d'entretiens et formation courte..."},
        ],
        [
            "Gestion & Suivi Financier",
            {"field_id": "bp_p25_c3_niv", "placeholder": "3/5 (Autonome)"},
            {"field_id": "bp_p25_c3_imp", "placeholder": "Importante"},
            {"field_id": "bp_p25_c3_plan", "placeholder": "Mise en place d'un tableau de bord mensuel..."},
        ],
        [
            "Organisation & Écologie de vie",
            {"field_id": "bp_p25_c4_niv", "placeholder": "4/5 (Avancée)"},
            {"field_id": "bp_p25_c4_imp", "placeholder": "Vitale"},
            {"field_id": "bp_p25_c4_plan", "placeholder": "Rituels de pause et sanctuarisation du repos..."},
        ],
    ]

    layout.add_table(headers, rows, col_widths=widths, field_prefix="tbl_comp")

    layout.add_space(0.4 * cm)

    cards = [
        {
            "title": "Mes Forces & Expériences Piliers",
            "subtitle": "Quels succès passés vous donnent une légitimité indiscutable ?",
            "field_id": "bp_p25_forces_legitimite",
            "placeholder": "10 ans d'expérience en gestion d'équipe, capacité d'écoute empathique, persévérance...",
        },
        {
            "title": "Mon Entourage Clé & Personnes Ressources",
            "subtitle": "De quelles personnes avez-vous besoin autour de vous ?",
            "field_id": "bp_p25_entourage_ressource",
            "placeholder": "Un pair pour binômer chaque quinzaine, une mentor bienveillante, mon expert-comptable...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=7.2 * cm)
    layout.render()


def create_juridique_cadre_page(c):
    """
    Page 26 : PARTIE 15 — Le Cadre Juridique, Fiscal & Administratif
    Statut, conformité, points validés et questions ouvertes.
    """
    layout = PageLayout(
        c,
        "15.1 : STRUCTURATION JURIDIQUE & FISCALE",
        config=LayoutConfig(part_title="15. LE CADRE JURIDIQUE"),
    )

    layout.add_text(
        "Le choix du statut juridique doit être au service de votre projet et de votre sécurité, jamais l'inverse. "
        "Faites le point sur les formes envisageables, les obligations réglementaires et les assurances obligatoires.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    layout.add_checklist(
        items=[
            ("Statut d'exercice (Micro-entreprise, SASU, EURL, Coopérative)", "bp_p26_chk_statut"),
            ("Assurance Responsabilité Civile Professionnelle (RC Pro)", "bp_p26_chk_rcpro"),
            ("Ouverture d'un compte bancaire professionnel dédié", "bp_p26_chk_banque"),
            ("Rédaction des Conditions Générales de Vente (CGV)", "bp_p26_chk_cgv"),
            ("Conformité RGPD & Mentions légales obligatoires", "bp_p26_chk_rgpd"),
            ("Adhésion à un médiateur de la consommation (si B2C)", "bp_p26_chk_mediateur"),
        ],
        title="OBLIGATIONS ADMINISTRATIVES ET LÉGALES :",
        columns=2,
    )

    questions = [
        QuestionItem(
            question="1. Le statut juridique retenu ou envisagé pour démarrer",
            form_field_id="bp_p26_statut_choisi",
            subtitle="Pourquoi ce choix ? (Simplicité de gestion, protection du patrimoine, cumul avec allocations...)",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="2. Ce que j'ai déjà vérifié auprès de professionnels fiables",
            form_field_id="bp_p26_verifications_faites",
            subtitle="Conseils reçus auprès d'un expert-comptable, de la BGE, de la CCI, de France Travail...",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
        QuestionItem(
            question="3. Les questions administratives ou fiscales en suspens",
            form_field_id="bp_p26_questions_juridiques",
            subtitle="Quels doutes restent à éclaircir avant la signature des statuts ou l'immatriculation ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    ]

    layout.add_questions_group(questions, min_box_height=2.8 * cm, max_box_height=4.4 * cm)
    layout.render()


def create_finances_depenses_page(c):
    """
    Page 27 : PARTIE 16 — Prévisionnel Financier : Dépenses & Charges
    Tableau des investissements de départ et charges mensuelles.
    """
    layout = PageLayout(
        c,
        "16.1 : DÉPENSES & CHARGES PRÉVISIONNELLES",
        config=LayoutConfig(part_title="16. PRÉVISIONNEL FINANCIER"),
    )

    layout.add_text(
        "Distinguez précisément vos investissements initiaux (ce que vous payez une fois pour démarrer) "
        "de vos charges mensuelles récurrentes (ce que l'entreprise doit payer chaque mois pour exister).",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    # Tableau 1 : Investissements de départ
    headers_inv = ["Dépense de Démarrage (Investissement)", "Montant Estimé (€)", "Devis / Source", "Vital dès le J1 ?"]
    widths_inv = [0.38 * layout.target_width, 0.20 * layout.target_width, 0.24 * layout.target_width, 0.18 * layout.target_width]
    rows_inv = [
        [
            {"field_id": "bp_p27_inv1_nom", "placeholder": "Frais d'immatriculation & statuts"},
            {"field_id": "bp_p27_inv1_mt", "placeholder": "150 €"},
            {"field_id": "bp_p27_inv1_src", "placeholder": "Greffe / INPI"},
            {"field_id": "bp_p27_inv1_vit", "placeholder": "Oui"},
        ],
        [
            {"field_id": "bp_p27_inv2_nom", "placeholder": "Identité visuelle & site web"},
            {"field_id": "bp_p27_inv2_mt", "placeholder": "600 €"},
            {"field_id": "bp_p27_inv2_src", "placeholder": "Graphiste indépendante"},
            {"field_id": "bp_p27_inv2_vit", "placeholder": "Oui"},
        ],
        [
            {"field_id": "bp_p27_inv3_nom", "placeholder": "Matériel professionnel & outils"},
            {"field_id": "bp_p27_inv3_mt", "placeholder": "800 €"},
            {"field_id": "bp_p27_inv3_src", "placeholder": "Devis matériel informatique"},
            {"field_id": "bp_p27_inv3_vit", "placeholder": "Non (phase 2)"},
        ],
        [
            {"field_id": "bp_p27_inv4_nom", "placeholder": "Trésorerie de sécurité initiale"},
            {"field_id": "bp_p27_inv4_mt", "placeholder": "1 500 €"},
            {"field_id": "bp_p27_inv4_src", "placeholder": "Épargne de précaution"},
            {"field_id": "bp_p27_inv4_vit", "placeholder": "Vitale"},
        ],
    ]
    layout.add_table(headers_inv, rows_inv, col_widths=widths_inv, field_prefix="tbl_inv")

    layout.add_space(0.35 * cm)

    # Tableau 2 : Charges récurrentes
    headers_ch = ["Nature de la Charge Mensuelle", "Montant Mensuel (€)", "Type (Fixe ou Variable)", "Optimisation possible ?"]
    widths_ch = [0.38 * layout.target_width, 0.20 * layout.target_width, 0.24 * layout.target_width, 0.18 * layout.target_width]
    rows_ch = [
        [
            {"field_id": "bp_p27_ch1_nom", "placeholder": "Assurance RC Pro & Protection"},
            {"field_id": "bp_p27_ch1_mt", "placeholder": "35 € / mois"},
            {"field_id": "bp_p27_ch1_type", "placeholder": "Fixe"},
            {"field_id": "bp_p27_ch1_opt", "placeholder": "Non négociable"},
        ],
        [
            {"field_id": "bp_p27_ch2_nom", "placeholder": "Logiciels & abonnements SaaS"},
            {"field_id": "bp_p27_ch2_mt", "placeholder": "60 € / mois"},
            {"field_id": "bp_p27_ch2_type", "placeholder": "Fixe"},
            {"field_id": "bp_p27_ch2_opt", "placeholder": "Paiement annuel (-20%)"},
        ],
        [
            {"field_id": "bp_p27_ch3_nom", "placeholder": "Cotisations sociales & bancaires"},
            {"field_id": "bp_p27_ch3_mt", "placeholder": "21% du CA"},
            {"field_id": "bp_p27_ch3_type", "placeholder": "Variable"},
            {"field_id": "bp_p27_ch3_opt", "placeholder": "ACRE 1ère année"},
        ],
        [
            {"field_id": "bp_p27_ch4_nom", "placeholder": "Frais bancaires & terminaux"},
            {"field_id": "bp_p27_ch4_mt", "placeholder": "25 € / mois"},
            {"field_id": "bp_p27_ch4_type", "placeholder": "Fixe"},
            {"field_id": "bp_p27_ch4_opt", "placeholder": "Banque pro en ligne"},
        ],
    ]
    layout.add_table(headers_ch, rows_ch, col_widths=widths_ch, field_prefix="tbl_charges")

    layout.add_space(0.35 * cm)

    layout.add_callout(
        "Règle de sécurité : Prévoyez toujours une marge d'imprévus de 15% à 20% sur vos dépenses de démarrage. "
        "La trésorerie est le poumon qui vous permet de vous installer sereinement sans angoisse du lendemain.",
        title="CONSEIL FINANCIER MARGE DE MANŒUVRE",
        variant="warning",
    )

    layout.render()


def create_finances_previsionnel_page(c):
    """
    Page 28 : PARTIE 16 — Prévisionnel Financier : Chiffre d'Affaires & Rentabilité
    Les 3 scénarios (prudent, réaliste, ambitieux) et le calcul du point mort.
    """
    layout = PageLayout(
        c,
        "16.2 : SCÉNARIOS DE CA & POINT MORT",
        config=LayoutConfig(part_title="16. PRÉVISIONNEL FINANCIER"),
    )

    layout.add_text(
        "Faire comprendre le raisonnement économique : Nombre de ventes × Prix moyen = Chiffre d'Affaires. "
        "Construire 3 scénarios pour préparer votre sérénité et calculer le seuil minimal de rentabilité.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    scenarios = [
        {
            "title": "Scénario 1 : Prudent (Démarrage)",
            "subtitle": "Hypothèses basses : 2 à 3 ventes / mois pour couvrir les charges fixes minimales...",
            "field_id": "bp_p28_scen_prudent",
            "placeholder": "Ex : 2 forfaits à 750 € = 1 500 € / mois de CA...",
        },
        {
            "title": "Scénario 2 : Réaliste (Vitesse de Croisière)",
            "subtitle": "Hypothèses moyennes à 12 mois : volume régulier et rémunération cible assurée...",
            "field_id": "bp_p28_scen_intermediaire",
            "placeholder": "Ex : 4 forfaits à 750 € + 2 ateliers = 3 500 € / mois de CA...",
        },
        {
            "title": "Scénario 3 : Ambitieux (Plein Régime)",
            "subtitle": "Hypothèses hautes : carnet de commandes plein, liste d'attente et partenariats...",
            "field_id": "bp_p28_scen_ambitieux",
            "placeholder": "Ex : 6 forfaits + formations d'entreprise = 5 500 € / mois de CA...",
        },
    ]

    layout.add_cards_grid(scenarios, columns=3, card_height=6.4 * cm)

    layout.add_space(0.35 * cm)

    layout.add_question_block(
        "Mon Seuil de Rentabilité & Salaire Cible (Point Mort)",
        "bp_p28_seuil_calcul",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Combien de prestations devez-vous impérativement vendre chaque mois pour couvrir vos charges et vous verser votre rémunération ?",
            example="Ex : Charges fixes (300 €) + Cotisations (700 €) + Salaire net cible (2 000 €) = 3 000 € de CA requis, soit 4 forfaits à 750 € par mois.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()


def create_finances_financement_page(c):
    """
    Page 29 : PARTIE 17 — Financer mon Projet
    Besoin total estimé (Stat Boxes) et tableau comparatif des sources de financement.
    """
    layout = PageLayout(
        c,
        "17.1 : PLAN DE FINANCEMENT INITIAL",
        config=LayoutConfig(part_title="17. FINANCER LE PROJET"),
    )

    layout.add_text(
        "Ne sous-estimez jamais le besoin en trésorerie de départ. Le montant à financer ne couvre pas seulement les achats : "
        "il doit sécuriser un matelas de 3 à 6 mois de charges pour vous permettre de prospecter l'esprit tranquille.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    stats = [
        {"value": "BESOIN INITIAL", "label": "Achats & Matériel", "color": PDFStyle.COLOR_ACCENT_BLUE},
        {"value": "TRÉSORERIE", "label": "Sécurité 3 à 6 mois", "color": PDFStyle.COLOR_ACCENT_RED},
        {"value": "TOTAL GLOBAL", "label": "À Financer au J1", "color": PDFStyle.COLOR_ACCENT_BLUE},
    ]
    layout.add_stat_boxes(stats)

    layout.add_space(0.2 * cm)

    headers = [
        "Source de Financement",
        "Montant Possible",
        "Conditions & Modalités",
        "Avantages & Contraintes",
    ]

    widths = [
        0.26 * layout.target_width,
        0.18 * layout.target_width,
        0.28 * layout.target_width,
        0.28 * layout.target_width,
    ]

    rows = [
        [
            {"field_id": "bp_p29_f1_src", "placeholder": "Apport personnel (épargne)"},
            {"field_id": "bp_p29_f1_mt", "placeholder": "3 000 €"},
            {"field_id": "bp_p29_f1_cond", "placeholder": "Disponible immédiatement"},
            {"field_id": "bp_p29_f1_av", "placeholder": "Zéro dette, liberté totale"},
        ],
        [
            {"field_id": "bp_p29_f2_src", "placeholder": "Maintien ARE / Versement ARCE"},
            {"field_id": "bp_p29_f2_mt", "placeholder": "Maintien mensuel"},
            {"field_id": "bp_p29_f2_cond", "placeholder": "Droits ouverts France Travail"},
            {"field_id": "bp_p29_f2_av", "placeholder": "Garantit les dépenses de vie"},
        ],
        [
            {"field_id": "bp_p29_f3_src", "placeholder": "Prêt d'honneur (Initiative / BGE)"},
            {"field_id": "bp_p29_f3_mt", "placeholder": "5 000 €"},
            {"field_id": "bp_p29_f3_cond", "placeholder": "Prêt à taux 0 sans garantie"},
            {"field_id": "bp_p29_f3_av", "placeholder": "Effet de levier précieux"},
        ],
        [
            {"field_id": "bp_p29_f4_src", "placeholder": "Financement participatif / Don"},
            {"field_id": "bp_p29_f4_mt", "placeholder": "2 000 €"},
            {"field_id": "bp_p29_f4_cond", "placeholder": "Campagne de 30 jours"},
            {"field_id": "bp_p29_f4_av", "placeholder": "Fédère la communauté dès le départ"},
        ],
    ]

    layout.add_table(headers, rows, col_widths=widths, field_prefix="tbl_financement")

    layout.add_space(0.35 * cm)

    layout.add_question_block(
        "Ma Décision de Financement pour le Démarrage",
        "bp_p29_decision_financement",
        config=QuestionConfig(
            box_height=4.8 * cm,
            subtitle="Quelle combinaison de financements retenez-vous pour sécuriser votre lancement sans prendre de risque inconsidéré ?",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()
