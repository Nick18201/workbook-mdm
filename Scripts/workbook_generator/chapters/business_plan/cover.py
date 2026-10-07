from reportlab.lib.units import cm

from ...components import create_cover_page, create_standard_summary_page
from ...templates import PageLayout, LayoutConfig, QuestionItem


def create_business_plan_cover(c):
    """Cover of the business plan workbook."""
    create_cover_page(
        c,
        "Mon business *plan.*",
        eyebrow="Livret projet · entrepreneuriat",
        tagline="Créer ou reprendre une activité",
        promise="De l'idée au projet viable.",
    )


def create_business_plan_identity_page(c):
    """The project's identity card and its one-sentence pitch."""
    layout = PageLayout(c, "Votre projet *en bref.*", config=LayoutConfig(part_title="Fiche projet"))
    layout.add_paragraphs([
        "Un carnet de travail pour structurer, tester et faire évoluer votre projet. Commencez par l'identifier.",
    ], spacing_after=0.45 * cm)
    layout.add_fields_card(
        [
            [("Porteur ou porteuse du projet (nom et prénom)", "bp_identite_nom_prenom"),
             ("Nom ou intitulé du projet", "bp_identite_nom_projet")],
            [("Date de début", "bp_identite_date_debut"), ("Version du document", "bp_identite_version")],
        ],
        title="Informations du projet",
    )
    layout.add_questions_group([
        QuestionItem("Mon projet en une phrase (première intuition)", "bp_identite_pitch_intro",
                     subtitle="Formulez votre intuition de départ en une ou deux phrases claires."),
    ], max_box_height=5.0 * cm)
    layout.add_annotation("Cette phrase évoluera : c'est voulu.")
    layout.render()


def create_business_plan_summary(c):
    """Opener: the method in six stages."""
    points = [
        "1. Fondations et cible : clarifier l'idée, projeter la vision à 3 ans, comprendre les personnes visées.",
        "2. Problème et offre : identifier le vrai problème, poser les hypothèses, formuler l'offre et sa valeur.",
        "3. Marché et positionnement : étudier le marché, les concurrents et les alternatives, préparer le pitch.",
        "4. Modèle économique et vente : revenus, Business Model Canvas, prix, dix premiers clients.",
        "5. Moyens, finances et cadre : communication, ressources, statut juridique, prévisionnel, point mort.",
        "6. Test et synthèse : MVP, entretiens terrain, risques, feuille de route et synthèse finale.",
    ]
    create_standard_summary_page(
        c,
        "",
        "Construire votre *business plan.*",
        "Ce carnet vous accompagne pas à pas pour donner corps à votre projet. Rien n'est prérempli : vous suivez une "
        "boucle en six temps (comprendre, se questionner, chercher sur le terrain, écrire, décider, vérifier vos "
        "hypothèses) pour transformer une intuition en une entreprise viable et durable.",
        points,
    )
