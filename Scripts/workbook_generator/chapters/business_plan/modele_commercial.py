from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionItem,
    QuestionConfig,
    TextConfig,
)


def create_modele_revenus_page(c):
    """
    Page 16 : PARTIE 8 — Mon Modèle Économique : Comment mon projet gagne-t-il de l'argent ?
    Panorama des modèles, qui paie, pour quoi et à quel moment.
    """
    layout = PageLayout(
        c,
        "8.1 : SOURCES DE REVENUS & MODÈLE",
        config=LayoutConfig(part_title="8. MON MODÈLE ÉCONOMIQUE"),
    )

    layout.add_text(
        "Votre modèle économique explique comment votre projet crée de la valeur, la délivre et en capture une partie "
        "pour assurer sa viabilité financière. Un modèle sain diversifie intelligemment ses rentrées sans s'éparpiller.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    layout.add_checklist(
        items=[
            ("Vente unitaire de produit / prestation", "bp_p16_chk_vente"),
            ("Abonnement / Forfait mensuel récurrent", "bp_p16_chk_abo"),
            ("Accompagnement / Pack sur devis", "bp_p16_chk_pack"),
            ("Financement public / Aides / Subventions", "bp_p16_chk_public"),
            ("Partenariats / Apport d'affaires", "bp_p16_chk_partenariat"),
            ("Modèle hybride (Particuliers + Entreprises)", "bp_p16_chk_hybride"),
        ],
        title="SOURCES DE REVENUS ENVISAGÉES :",
        columns=2,
    )

    questions = [
        QuestionItem(
            question="1. Mes sources de revenus prioritaires et secondaires",
            form_field_id="bp_p16_sources_revenus",
            subtitle="Quelle offre génère le cœur de vos revenus ? Quelles sont les rentrées complémentaires ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="2. Quelle personne ou organisation paie concrètement ?",
            form_field_id="bp_p16_qui_paie",
            subtitle="La personne accompagnée elle-même, son employeur (B2B), une caisse de retraite, un OPCO...",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
        QuestionItem(
            question="3. Pour quoi paie-t-elle et à quel moment du parcours ?",
            form_field_id="bp_p16_quand_paie",
            subtitle="Acompte à la commande (30%), solde à la livraison, prélèvement mensuel, paiement en 3x...",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    ]

    layout.add_questions_group(questions, min_box_height=2.4 * cm, max_box_height=3.8 * cm)
    layout.render()


def create_modele_canvas_page(c):
    """
    Page 17 : PARTIE 8 — Mon Business Model Canvas Interactif
    Grille ordonnée en 9 blocs avec zones de saisie AcroForm.
    """
    layout = PageLayout(
        c,
        "8.2 : BUSINESS MODEL CANVAS INTERACTIF",
        config=LayoutConfig(part_title="8. MON MODÈLE ÉCONOMIQUE"),
    )

    layout.add_text(
        "La vue d'ensemble synthétique de votre écosystème en 9 blocs interdépendants. "
        "Remplissez chaque bloc avec des mots-clés percutants pour tester la cohérence globale de votre édifice.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    canvas_blocks = [
        # Ligne 1
        {
            "title": "1. Segments Clients",
            "subtitle": "Pour qui créez-vous de la valeur ?",
            "field_id": "bp_p17_canvas_segments",
            "placeholder": "Cibles prioritaires, personas...",
        },
        {
            "title": "2. Proposition de Valeur",
            "subtitle": "Quelle promesse unique délivrez-vous ?",
            "field_id": "bp_p17_canvas_valeur",
            "placeholder": "Bénéfice clé, transformation...",
        },
        {
            "title": "3. Relations Clients",
            "subtitle": "Quel lien entretenez-vous ?",
            "field_id": "bp_p17_canvas_relations",
            "placeholder": "Coaching direct, communauté...",
        },
        # Ligne 2
        {
            "title": "4. Canaux de Vente",
            "subtitle": "Comment vous faites-vous connaître ?",
            "field_id": "bp_p17_canvas_canaux",
            "placeholder": "Réseaux, site, bouche-à-oreille...",
        },
        {
            "title": "5. Activités Clés",
            "subtitle": "Quelles actions devez-vous réussir ?",
            "field_id": "bp_p17_canvas_activites",
            "placeholder": "Production, accompagnement, com...",
        },
        {
            "title": "6. Ressources Clés",
            "subtitle": "De quoi avez-vous besoin pour tourner ?",
            "field_id": "bp_p17_canvas_ressources",
            "placeholder": "Matériel, compétences, temps...",
        },
        # Ligne 3
        {
            "title": "7. Partenaires Clés",
            "subtitle": "Qui sont vos alliés stratégiques ?",
            "field_id": "bp_p17_canvas_partenaires",
            "placeholder": "Prescripteurs, pairs, mentors...",
        },
        {
            "title": "8. Structure de Coûts",
            "subtitle": "Quelles sont vos dépenses majeures ?",
            "field_id": "bp_p17_canvas_couts",
            "placeholder": "Charges fixes, outils, sous-traitance...",
        },
        {
            "title": "9. Flux de Revenus",
            "subtitle": "Comment rentre l'argent dans l'entreprise ?",
            "field_id": "bp_p17_canvas_revenus",
            "placeholder": "Tarifs forfaits, récurrence, marge...",
        },
    ]

    layout.add_cards_grid(canvas_blocks, columns=3, card_height=5.3 * cm)
    layout.render()


def create_commercial_offres_page(c):
    """
    Page 18 : PARTIE 9 — Mon Offre Commerciale : Produits & Services
    Tableau des offres + Architecture de gamme.
    """
    layout = PageLayout(
        c,
        "9.1 : GRILLE DES OFFRES & FORMULES",
        config=LayoutConfig(part_title="9. MON OFFRE COMMERCIALE"),
    )

    layout.add_text(
        "Structurez vos prestations sous forme d'une gamme claire : une offre phare (qui concentre vos efforts), "
        "des offres complémentaires pour enrichir la relation, et vos idées d'offres futures à garder pour plus tard.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    headers = [
        "Offre / Formule",
        "Public Cible",
        "Contenu Clé",
        "Prix Envisagé",
        "Marge / Rentabilité",
    ]

    widths = [
        0.22 * layout.target_width,
        0.20 * layout.target_width,
        0.28 * layout.target_width,
        0.15 * layout.target_width,
        0.15 * layout.target_width,
    ]

    rows = [
        [
            {"field_id": "bp_p18_o1_nom", "placeholder": "Formule Découverte"},
            {"field_id": "bp_p18_o1_cible", "placeholder": "Débutantes..."},
            {"field_id": "bp_p18_o1_contenu", "placeholder": "Audit de 2h + mémo"},
            {"field_id": "bp_p18_o1_prix", "placeholder": "180 €"},
            {"field_id": "bp_p18_o1_marge", "placeholder": "Forte"},
        ],
        [
            {"field_id": "bp_p18_o2_nom", "placeholder": "Accompagnement Phare"},
            {"field_id": "bp_p18_o2_cible", "placeholder": "En reconversion..."},
            {"field_id": "bp_p18_o2_contenu", "placeholder": "Programme 3 mois"},
            {"field_id": "bp_p18_o2_prix", "placeholder": "950 €"},
            {"field_id": "bp_p18_o2_marge", "placeholder": "Très bonne"},
        ],
        [
            {"field_id": "bp_p18_o3_nom", "placeholder": "Atelier Collectif"},
            {"field_id": "bp_p18_o3_cible", "placeholder": "Groupe (6 pers)"},
            {"field_id": "bp_p18_o3_contenu", "placeholder": "Journée immersive"},
            {"field_id": "bp_p18_o3_prix", "placeholder": "150 € / pers"},
            {"field_id": "bp_p18_o3_marge", "placeholder": "Excellente"},
        ],
        [
            {"field_id": "bp_p18_o4_nom", "placeholder": "Option / Suivi Long Terme"},
            {"field_id": "bp_p18_o4_cible", "placeholder": "Anciennes clientes..."},
            {"field_id": "bp_p18_o4_contenu", "placeholder": "Entretien mensuel de suivi"},
            {"field_id": "bp_p18_o4_prix", "placeholder": "90 € / mois"},
            {"field_id": "bp_p18_o4_marge", "placeholder": "Excellente"},
        ],
    ]

    layout.add_table(headers, rows, col_widths=widths, field_prefix="tbl_offres")

    layout.add_space(0.35 * cm)

    cards = [
        {
            "title": "Mon Offre Phare (Core Offer)",
            "subtitle": "L'offre signature sur laquelle vous concentrez 80% de votre énergie commerciale...",
            "field_id": "bp_p18_offre_phare",
            "placeholder": "Pourquoi cette offre est votre fer de lance ? À quel problème n°1 répond-elle ?",
        },
        {
            "title": "Mes Offres Complémentaires & Futures",
            "subtitle": "Ce que vous proposerez dans un second temps (cross-sell, montée en gamme, produits digitaux)...",
            "field_id": "bp_p18_offres_futures",
            "placeholder": "Idées à mûrir sans vous disperser lors des premiers mois...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=8.0 * cm)
    layout.render()


def create_commercial_prix_page(c):
    """
    Page 19 : PARTIE 10 — Comment fixer mes prix ?
    Les 3 angles, les 4 repères et l'argumentaire de confiance.
    """
    layout = PageLayout(
        c,
        "10.1 : COMMENT FIXER MES PRIX ?",
        config=LayoutConfig(part_title="10. MES PRIX"),
    )

    layout.add_text(
        "Fixer ses prix est souvent un moment de doute. Pourtant, un prix juste se calcule à l'intersection de 3 angles : "
        "1. Vos coûts réels (le plancher vital) • 2. La valeur perçue (la transformation vécue) • 3. Le marché (la concurrence).",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    tarifs_repères = [
        {
            "title": "1. Prix Plancher (Minimum Vital)",
            "subtitle": "En-dessous de ce prix, vous travaillez à perte ou sacrifiez votre santé...",
            "field_id": "bp_p19_prix_plancher",
            "placeholder": "Ex : 450 € minimum par prestation...",
        },
        {
            "title": "2. Prix Cible (Idéal & Rentable)",
            "subtitle": "Le tarif juste qui rémunère votre expertise et finance votre sérénité...",
            "field_id": "bp_p19_prix_cible",
            "placeholder": "Ex : 750 € par prestation...",
        },
        {
            "title": "3. Prix Plafond (Audacieux)",
            "subtitle": "Le prix maximal justifiable si vous ajoutez un accompagnement sur-mesure...",
            "field_id": "bp_p19_prix_plafond",
            "placeholder": "Ex : 1 200 € en formule premium...",
        },
        {
            "title": "4. Prix Observés sur le Marché",
            "subtitle": "Les fourchettes pratiquées par les acteurs comparables...",
            "field_id": "bp_p19_prix_marche",
            "placeholder": "Ex : Entre 500 € et 900 € selon l'expérience...",
        },
    ]

    layout.add_cards_grid(tarifs_repères, columns=2, card_height=4.0 * cm)

    layout.add_space(0.25 * cm)

    layout.add_question_block(
        "Pourquoi mon prix est-il cohérent, juste et pleinement légitime ?",
        "bp_p19_justification_prix",
        config=QuestionConfig(
            box_height=3.2 * cm,
            subtitle="Écrivez vos arguments clés pour assumer vos tarifs avec sérénité et sans baisser vos prix par peur.",
            example="Ex : Mon tarif reflète un suivi individuel sans compromis, un gain de plusieurs mois d'errance pour la cliente et une disponibilité réelle.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.render()


def create_commercial_acquisition_page(c):
    """
    Page 20 : PARTIE 11 — Commercialisation : Trouver mes Premiers Clients
    Canaux d'acquisition et plan concret pour décrocher les 10 premiers clients.
    """
    layout = PageLayout(
        c,
        "11.1 : TROUVER MES PREMIERS CLIENTS",
        config=LayoutConfig(part_title="11. COMMERCIALISATION"),
    )

    layout.add_text(
        "Attendre que les clients arrivent par magie ne fonctionne pas. Pour lancer la machine, il faut choisir "
        "2 à 3 canaux d'acquisition prioritaires et concentrer ses efforts sur l'obtention de ses 10 premiers clients.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    layout.add_checklist(
        items=[
            ("Bouche-à-oreille & Réseau proche", "bp_p20_chk_reseau"),
            ("Réseaux sociaux (LinkedIn, Instagram)", "bp_p20_chk_social"),
            ("Prescripteurs & Partenaires recommandants", "bp_p20_chk_prescripteurs"),
            ("Événements, ateliers & salons locaux", "bp_p20_chk_salons"),
            ("Site web & Référencement (SEO)", "bp_p20_chk_site"),
            ("Démarchage direct & Prise de contact qualifiée", "bp_p20_chk_direct"),
        ],
        title="CANAUX D'ACQUISITION PRIVILÉGIÉS :",
        columns=2,
    )

    questions = [
        QuestionItem(
            question="1. Mes 2 à 3 canaux prioritaires & Justification",
            form_field_id="bp_p20_canaux_choisis",
            subtitle="Pourquoi ces canaux correspondent-ils à votre personnalité et aux habitudes de vos clientes ?",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
        QuestionItem(
            question="2. Comment vais-je obtenir mes 10 premiers clients ?",
            form_field_id="bp_p20_dix_premiers_clients",
            subtitle="Détaillez vos actions directes : liste de 20 contacts tièdes, appel découverte, offre pilote à prix doux...",
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
        QuestionItem(
            question="3. Comment transformer un premier contact intéressé en cliente engagée ?",
            form_field_id="bp_p20_conversion_contact",
            subtitle="Quel est votre rituel d'échange : appel d'alignement de 30 min, diagnostic offert, proposition personnalisée...",
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    ]

    layout.add_questions_group(questions, min_box_height=2.4 * cm, max_box_height=3.8 * cm)
    layout.render()


def create_commercial_parcours_page(c):
    """
    Page 21 : PARTIE 11 — Le Parcours Client en 7 Étapes
    Visualisation et actions concrètes de la Découverte à la Recommandation.
    """
    layout = PageLayout(
        c,
        "11.2 : LE PARCOURS CLIENT EN 7 ÉTAPES",
        config=LayoutConfig(part_title="11. COMMERCIALISATION"),
    )

    layout.add_text(
        "Le voyage de votre cliente commence bien avant l'achat et se poursuit bien après la prestation : "
        "Découverte → Intérêt → Contact → Achat → Expérience → Fidélisation → Recommandation.",
        config=TextConfig(spacing_after=0.35 * cm),
    )

    headers = [
        "Jalon du Parcours",
        "Ce que vit & ressent la cliente",
        "Ce que je dois faire / délivrer",
    ]

    widths = [
        0.28 * layout.target_width,
        0.36 * layout.target_width,
        0.36 * layout.target_width,
    ]

    rows = [
        [
            "1. Découverte & Intérêt",
            {"field_id": "bp_p21_r1_client", "placeholder": "Elle voit un post, ressent de la curiosité et se sent comprise..."},
            {"field_id": "bp_p21_r1_action", "placeholder": "Publier un contenu à forte valeur, inviter à un échange..."},
        ],
        [
            "2. Contact & Décision",
            {"field_id": "bp_p21_r2_client", "placeholder": "Elle hésite, a besoin de réassurance et de clarté sur le prix..."},
            {"field_id": "bp_p21_r2_action", "placeholder": "Mener un appel d'alignement bienveillant, envoyer une proposition claire..."},
        ],
        [
            "3. Expérience Vécue",
            {"field_id": "bp_p21_r3_client", "placeholder": "Elle se sent écoutée, accompagnée et observe des progrès réels..."},
            {"field_id": "bp_p21_r3_action", "placeholder": "Délivrer avec exigence, envoyer les outils, maintenir le lien régulier..."},
        ],
        [
            "4. Clôture & Ambassadrice",
            {"field_id": "bp_p21_r4_client", "placeholder": "Elle est fière du chemin parcouru et veut en parler autour d'elle..."},
            {"field_id": "bp_p21_r4_action", "placeholder": "Séance bilan, recueil de témoignage écrit/vidéo, proposition de suite..."},
        ],
    ]

    layout.add_table(headers, rows, col_widths=widths, field_prefix="tbl_parcours")

    layout.add_space(0.4 * cm)

    cards = [
        {
            "title": "Le Moment Clé d'Enchantement (Effet Whaou)",
            "subtitle": "Quelle attention inattendue allez-vous lui offrir pour marquer les esprits ?",
            "field_id": "bp_p21_enchantement",
            "placeholder": "Ex : Un livret d'accueil imprimé envoyé par courrier, une synthèse sur-mesure...",
        },
        {
            "title": "La Mécanique de Recommandation",
            "subtitle": "Comment inciterez-vous vos clientes satisfaites à parler de vous ?",
            "field_id": "bp_p21_recommandation",
            "placeholder": "Ex : Programme de parrainage bienveillant, demande d'avis Google systématique...",
        },
    ]

    layout.add_cards_grid(cards, columns=2, card_height=6.8 * cm)
    layout.render()
