from workbook_generator.config import PDFStyle

from .common import add_card, add_deliverables, add_session_card, add_temps_band, programme_layout

TITLE = "Votre parcours *d'accompagnement.*"
LEAD = "Un parcours structuré en séances individuelles."


def _sessions(layout, sessions):
    for s in sessions:
        add_session_card(layout, s["badge"], s["title"], s["description"], s["objective"],
                         followup=s.get("is_followup", False))


def create_programme_page_deroule_1(c):
    """The bilan's flow, stage 1 « Comprendre » (part 1, sessions 1 to 3)."""
    layout = programme_layout(c, TITLE, "Déroulé · temps 1", lead=LEAD)
    add_card(
        layout,
        body="<b>10 séances individuelles en visio et un entretien de suivi à 6 mois (45 min)</b>, soit <b>13 h "
             "d'accompagnement</b> avec la personne qui vous accompagne, choisie lors du premier échange. Entre les "
             "séances, <b>7 carnets de bord guidés</b>.",
        color=PDFStyle.COLOR_SKY,
    )
    add_temps_band(
        layout, "01", "Temps 1 : comprendre", "Poser le sac à dos.",
        "<i>Comprendre ce qui vous fait avancer : votre point de départ, votre parcours réel, votre fonctionnement, "
        "votre rapport à l'argent et vos valeurs.</i>",
    )
    _sessions(layout, [
        {
            "badge": "S1",
            "title": "Faire le point sur votre situation actuelle",
            "description": (
                "On commence par revenir à l'essentiel. Votre état actuel, votre énergie, ce qui vous pèse, ce qui "
                "tient encore. On pose aussi le cadre de travail : vos attentes, la confidentialité, la façon dont "
                "nous avancerons ensemble."
            ),
            "objective": "clarifier votre point de départ et sortir du flou.",
        },
        {
            "badge": "S2",
            "title": "Comprendre ce qui vous a construit et l'impact de vos héritages",
            "description": (
                "Votre rapport au travail ne s'est pas fait au hasard. On explore votre environnement, les modèles "
                "que vous avez eus, les messages reçus. Ce qui a influencé vos choix, parfois sans que vous en ayez "
                "conscience. Cela permet de prendre du recul et de ne plus avancer en pilotage automatique."
            ),
            "objective": "identifier les influences qui orientent encore vos choix aujourd'hui.",
        },
        {
            "badge": "S3",
            "title": "Analyser et comprendre votre parcours",
            "description": (
                "Vous avez déjà des expériences, des compétences, des intuitions. On regarde votre travail réel, "
                "au-delà de la fiche de poste, pour identifier : ce que vous savez faire, ce que vous aimez "
                "réellement, et ce qui ne vous correspond plus."
            ),
            "objective": "faire émerger des lignes directrices et vos ressources réelles.",
        },
    ])
    layout.render()


def create_programme_page_deroule_2(c):
    """Stage 1 « Comprendre » (part 2, sessions 4 to 6) and its deliverables."""
    layout = programme_layout(c, TITLE, "Déroulé · temps 1 (suite)", lead=LEAD)
    add_temps_band(layout, "01", "Temps 1 : comprendre (suite)", "Approfondissement de l'introspection.")
    _sessions(layout, [
        {
            "badge": "S4",
            "title": "Comprendre votre fonctionnement (MBTI®)",
            "description": (
                "On travaille votre fonctionnement en profondeur. Avec le questionnaire officiel MBTI®, vous "
                "comprenez : comment vous prenez des décisions, ce qui vous stimule, ce qui vous fatigue, votre "
                "manière d'interagir. On le met en regard de votre vécu : les environnements qui vous conviennent, "
                "ceux qui vous épuisent."
            ),
            "objective": "obtenir une grille de lecture claire de votre fonctionnement et de vos facteurs d'usure.",
        },
        {
            "badge": "S5",
            "title": "Poser sans tabou votre rapport à l'argent",
            "description": (
                "On pose les chiffres de votre sécurité financière : vos 4 seuils financiers, le revenu vital et le "
                "revenu sécurisant, le délai de trésorerie que vous pouvez tenir. Une transition viable se calcule, "
                "sans précariser l'équilibre de votre foyer."
            ),
            "objective": "fixer le seuil de sécurité financière qui servira à arbitrer vos pistes.",
        },
        {
            "badge": "S6",
            "title": "Clarifier vos valeurs et vos moteurs",
            "description": (
                "Vous définissez ce qui compte vraiment pour vous aujourd'hui : vos priorités, vos limites, vos "
                "critères de satisfaction. Ce qui est essentiel, et ce que vous n'êtes plus prêt(e) à accepter. Ils "
                "deviennent une grille anti-compromis, avec des critères observables sur le terrain."
            ),
            "objective": "définir vos critères de choix pour un projet cohérent.",
        },
    ])
    add_deliverables(layout, "À l'issue du temps 1 (comprendre)", [
        "Profil MBTI® complet et analyse d'impact environnemental",
        "Cartographie de vos énergies de travail et facteurs d'usure",
        "Seuil de sécurité financière (les 4 seuils clés pour arbitrer vos choix)",
    ])
    layout.render()


def create_programme_page_deroule_3(c):
    """Stage 2 « Confronter » (sessions 7 and 8) and its deliverables."""
    layout = programme_layout(c, TITLE, "Déroulé · temps 2", lead=LEAD)
    add_temps_band(
        layout, "02", "Temps 2 : confronter", "Confronter l'idée au terrain.",
        "<i>Confronter vos pistes au marché : ouvrir les possibles, puis vérifier métiers, salaires et débouchés "
        "auprès de celles et ceux qui les exercent.</i>",
    )
    _sessions(layout, [
        {
            "badge": "S7",
            "title": "Explorer des métiers et des secteurs",
            "description": (
                "On ouvre le champ des possibles de manière structurée : 10 pistes qualifiées, 5 réalistes et 5 "
                "audacieuses, cohérentes avec votre profil, vos compétences et vos aspirations. Vous préparez les "
                "enquêtes terrain qui vont les mettre à l'épreuve."
            ),
            "objective": "faire émerger des pistes alignées avec votre profil.",
        },
        {
            "badge": "S8",
            "title": "Approfondir et confronter vos pistes",
            "description": (
                "On passe à une phase concrète. Vos pistes sont classées en trois familles de scénarios : pistes "
                "directes, passerelles courtes, angles morts. Vous lancez des enquêtes auprès de professionnels en "
                "poste et vérifiez salaires et débouchés dans votre bassin d'emploi."
            ),
            "objective": "confronter vos idées à la réalité et affiner vos projections.",
        },
    ])
    add_deliverables(layout, "À l'issue du temps 2 (confronter)", [
        "Matrice de faisabilité marché (adéquation compétences, marché, débouchés)",
        "3 scénarios professionnels documentés et comparés",
        "Retours d'enquêtes terrain auprès de professionnels en poste",
    ])
    layout.render()


def create_programme_page_deroule_4(c):
    """Stage 3 « Décider et agir » (sessions 9, 10, follow-up) and its deliverables."""
    layout = programme_layout(c, TITLE, "Déroulé · temps 3", lead=LEAD)
    add_temps_band(
        layout, "03", "Temps 3 : décider et agir", "Sécuriser le passage à l'action.",
        "<i>Repartir avec un plan daté : arbitrer, adapter votre carnet de route à votre projet, engager les "
        "premières actions.</i>",
    )
    _sessions(layout, [
        {
            "badge": "S9",
            "title": "Faire un choix cohérent avec votre introspection et le marché",
            "description": (
                "On fait des choix. On identifie les pistes prioritaires et les moyens d'y accéder. Votre carnet de "
                "route s'adapte ensuite à votre projet : formations et financements pour une reconversion, modèle "
                "économique et première offre pour une création, argumentaire de repositionnement pour une évolution "
                "interne."
            ),
            "objective": "passer d'une réflexion à un projet clair et réaliste.",
        },
        {
            "badge": "S10",
            "title": "Structurer la suite",
            "description": (
                "On fait la synthèse du travail réalisé. Vous repartez avec deux trajectoires complémentaires, une "
                "piste A (projet d'élan) et une piste B (refuge et tremplin), des premières actions à mener dans les "
                "7 jours, et le document de synthèse co-rédigé, qui n'appartient qu'à vous."
            ),
            "objective": "repartir avec une trajectoire claire sur les prochains mois.",
        },
        {
            "badge": "Suivi",
            "title": "On se revoit 6 mois après pour faire le point sur votre projet (45 min)",
            "description": (
                "Un entretien individuel de 45 min pour analyser vos avancées réelles, ajuster les démarches si "
                "besoin, lever les nouveaux blocages et consolider durablement la dynamique engagée."
            ),
            "objective": "consolider la dynamique et ajuster la trajectoire si nécessaire.",
            "is_followup": True,
        },
    ])
    add_deliverables(layout, "À l'issue du temps 3 (décider et agir)", [
        "Feuilles de route piste A (projet d'élan) et piste B (refuge et tremplin)",
        "Premières actions concrètes à mener sous 7 jours",
        "Document de synthèse officiel co-rédigé (confidentiel et strictement personnel)",
        "Entretien individuel de suivi à 6 mois inclus",
    ])
    layout.render()
