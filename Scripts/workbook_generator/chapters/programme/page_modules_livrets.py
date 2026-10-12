from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle

from .common import add_card, add_card_row, add_rich_text, programme_layout

BLUE = "#" + PDFStyle.COLOR_BLUE.hexval()[2:]

MODULES = [
    {
        "label": "Reconversion",
        "title": "Changer de métier.",
        "subtitle": "1 h 45 d'écriture",
        "body": "La formation la plus courte qui vous ouvre le métier, son financement selon votre situation, "
                "votre calendrier et votre candidature.",
        "deliverable": "votre plan d'action sécurisé.",
        "color": PDFStyle.COLOR_BLUSH,
    },
    {
        "label": "Création",
        "title": "Créer votre activité.",
        "subtitle": "2 h d'écriture",
        "body": "Votre offre et votre prix, votre point mort face à vos seuils, votre financement et un premier test "
                "sur le terrain, en 15 jours au plus.",
        "deliverable": "votre modèle économique et votre première offre.",
        "color": PDFStyle.COLOR_SKY,
    },
    {
        "label": "Évolution interne",
        "title": "Évoluer de l'intérieur.",
        "subtitle": "1 h 45 d'écriture",
        "body": "Votre demande et ce qu'elle apporte à l'entreprise, vos preuves, vos conditions, vos interlocuteurs, "
                "le bon moment et les objections.",
        "deliverable": "votre argumentaire et votre plan de négociation.",
        "color": PDFStyle.COLOR_MINT,
    },
]

LIVRETS = [
    {
        "label": "Pour une création",
        "title": "Mon business plan",
        "subtitle": "De l'idée au projet viable.",
        "body": "Il approfondit le module création en six parties : vos fondations et votre cible, le problème et "
                "votre offre, le marché, le modèle économique et la vente, vos moyens et vos finances, le test et la "
                "décision. Il traite aussi la reprise d'une entreprise.",
        "items": ["<b>Écriture :</b> 15 h, dont 7 h 20 pour une première version."],
    },
    {
        "label": "Pour tout autre projet",
        "title": "Le livret de compétences",
        "subtitle": "Votre portfolio.",
        "body": "Vos compétences, prouvées par des faits : votre façon de travailler, vos savoir-faire et leurs "
                "niveaux, trois récits d'action, vos compétences transférables, une présentation prête pour un entretien et "
                "votre portfolio en une page.",
        "items": ["<b>Écriture :</b> 3 h 05, en trois parties."],
    },
]


def create_programme_page_modules_livrets(c):
    """What the project adds to the carnet de route: its module (sessions 9 to 10), then a livret for afterwards."""
    layout = programme_layout(
        c, "Un module, *puis un livret.*", "Modules et livrets",
        lead="Ce que votre projet ajoute à votre carnet de route.",
    )
    add_rich_text(
        layout,
        "En séance 9, vous choisissez votre piste A. Si votre projet est une reconversion, une création ou une "
        "évolution interne, <b>un module s'ajoute à votre carnet de route</b> : vous le préparez avant la séance 10, qui le "
        "travaille avec vous. À la fin du bilan, <b>un livret vous est remis pour la suite</b>, selon votre projet. "
        "Vous gardez définitivement modules et livrets.",
    )
    layout.add_heading("Le module de votre projet, entre les séances 9 et 10")
    layout.y_cursor -= 0.2 * cm
    add_card_row(layout, [
        {
            "label": m["label"],
            "title": m["title"],
            "subtitle": m["subtitle"],
            "body": f"{m['body']}<br/><br/><font color='{BLUE}'><b>Livrable :</b> {m['deliverable']}</font>",
        }
        for m in MODULES
    ], colors=[m["color"] for m in MODULES])
    layout.y_cursor -= 0.25 * cm
    layout.add_heading("Votre livret pour la suite, remis à la fin du bilan")
    layout.y_cursor -= 0.2 * cm
    # Each livret in its own pastel: lilac for the business plan, almond for the livret de compétences
    add_card_row(layout, LIVRETS, colors=[PDFStyle.COLOR_LILAC, PDFStyle.COLOR_ALMOND])
    add_card(
        layout,
        white=True,
        body="<b>Travail personnel :</b> le module s'ajoute aux 10 à 20 h de travail personnel du bilan. Le livret se "
             "travaille en autonomie, après le bilan : son temps d'écriture ne compte ni dans les 14 h "
             "d'accompagnement ni dans le travail personnel du bilan.",
    )
    layout.render()
