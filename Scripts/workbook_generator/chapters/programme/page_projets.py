from workbook_generator.config import PDFStyle

from .common import add_card, add_rich_text, programme_layout

TRAJECTOIRES = [
    {
        "tag": "Trajectoire 1 · module reconversion",
        "title": "Reconversion et bifurcation",
        "audience": "Pour changer de secteur, de fonction ou d'environnement de travail.",
        "points": [
            ("Sécurité financière", "vos droits (indemnités, Transitions Pro, maintien de salaire)."),
            ("Formation", "la formation la plus courte qui ouvre le métier, et son financement."),
            ("Terrain", "enquêtes et immersions auprès de personnes en poste."),
            ("Candidature", "CV de bifurcation, posture et récit d'entretien convaincant."),
        ],
        "deliverable": "Plan d'action sécurisé et enquêtes validées",
        "color": PDFStyle.COLOR_BLUSH,
    },
    {
        "tag": "Trajectoire 2 · module création",
        "title": "Création et reprise d'entreprise",
        "audience": "Pour lancer une activité indépendante ou reprendre une entreprise existante.",
        "points": [
            ("Modèle économique", "seuil de rentabilité calculé face à votre minimum vital."),
            ("Offre", "une première offre pilote testable sur le terrain sous 15 jours."),
            ("Posture", "fixer vos tarifs avec légitimité, poser vos limites."),
            ("Lancement", "choix du statut juridique, dispositifs ACRE/ARCE, premiers clients."),
        ],
        "deliverable": "Modèle économique et première offre, passés au crash-test de vos seuils",
        "color": PDFStyle.COLOR_SKY,
    },
    {
        "tag": "Trajectoire 3 · module évolution interne",
        "title": "Évolution interne et repositionnement",
        "audience": "Pour ne pas tout plaquer, mais refuser de continuer de la même manière.",
        "points": [
            ("Travail empêché", "repérer précisément ce qui bloque pour redéfinir votre poste."),
            ("Négociation", "un argumentaire solide pour l'entretien annuel, l'entretien de parcours professionnel "
                            "ou la mobilité interne."),
            ("Limites", "protéger votre charge mentale et rééquilibrer vos horaires."),
            ("Pouvoir d'agir", "reprendre durablement la main de l'intérieur."),
        ],
        "deliverable": "Argumentaire de repositionnement et plan de négociation",
        "color": PDFStyle.COLOR_MINT,
    },
]


def create_programme_page_projets(c):
    """The three projects the bilan leads to, with their key points and deliverable."""
    layout = programme_layout(
        c, "Trois projets, *trois trajectoires.*", "Bénéfices et trajectoires",
        lead="Les trois projets professionnels auxquels mène le bilan.",
    )
    add_rich_text(
        layout,
        "À l'opposé des approches théoriques de développement personnel, notre accompagnement est résolument "
             "orienté vers <b>le passage à l'action, l'arbitrage réaliste et la confrontation au terrain</b>. Chaque "
        "parcours converge vers l'un des trois projets d'aboutissement ci-dessous, chacun avec son module en fin de "
        "bilan :",
    )
    for t in TRAJECTOIRES:
        add_card(
            layout,
            label=t["tag"],
            title=t["title"],
            subtitle=t["audience"],
            items=[f"<b>{name} :</b> {text}" for name, text in t["points"]]
            + [f"<font color='#{PDFStyle.COLOR_BLUE.hexval()[2:]}'><b>Livrable clé :</b> {t['deliverable']}</font>"],
            color=t["color"],
        )
    layout.render()

