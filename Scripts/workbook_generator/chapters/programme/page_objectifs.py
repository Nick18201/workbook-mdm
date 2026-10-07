from workbook_generator.config import PDFStyle

from .common import add_card, add_rich_text, programme_layout


def create_programme_page_objectifs(c):
    """
    Objectives and regulatory frame: the 3 legal phases of the Labour Code (R. 6313-4 to
    R. 6313-8), the skills aimed at, the free first meeting and the official summary document.
    """
    layout = programme_layout(
        c, "Objectifs *et cadre réglementaire.*", "Le programme · objectifs",
        lead="Les 3 phases légales et le développement de votre pouvoir d'agir.",
    )
    add_rich_text(
        layout,
        "L'enjeu du bilan de compétences est de déterminer <b>quelle place accorder au travail dans votre "
        "existence</b> afin de réaligner ce que vous faites au quotidien avec qui vous êtes vraiment. En explorant "
        "votre fonctionnement, vos choix passés et vos valeurs, la démarche permet de déconstruire les schémas "
        "inconscients pour <b>décider en connaissance de cause</b>, reprendre votre pouvoir d'agir et concrétiser "
        "un projet professionnel réaliste et durable.",
    )
    add_card(
        layout,
        label="Code du travail · art. R. 6313-4 à R. 6313-8",
        title="Les 3 phases légales obligatoires",
        items=[
            "<b>1. Phase préliminaire :</b> Confirmer l'engagement du bénéficiaire, analyser la nature de ses besoins, "
            "définir conjointement les conditions de déroulement du bilan et présenter les outils mobilisés.",
            "<b>2. Phase d'investigation :</b> Explorer en profondeur le parcours, les motivations et les compétences "
            "(savoirs, savoir-faire, savoir-être). Identifier les perspectives d'évolution et confronter les "
            "scénarios aux réalités du marché de l'emploi.",
            "<b>3. Phase de conclusion :</b> S'approprier les résultats de l'investigation, recenser les facteurs de "
            "réussite du projet, co-construire un plan d'action réaliste et finaliser le document de synthèse écrit.",
            "<b>Document ressource officiel :</b> La synthèse écrite co-construite remise à l'issue de la phase de "
            "conclusion représente un livrable officiel confidentiel, propriété exclusive du bénéficiaire "
            "(art. L. 6313-4 du Code du travail).",
        ],
    )
    add_card(
        layout,
        title="Compétences visées & finalités de l'accompagnement",
        white=True,
        items=[
            "<b>Vision claire & Alignement :</b> Développer une connaissance lucide de son fonctionnement, de ses "
            "compétences et de ses motivations profondes. Clarifier ses valeurs et poser des critères de choix non "
            "négociables.",
            "<b>Analyse du marché & Employabilité :</b> Développer la capacité à analyser les dynamiques d'embauche et "
            "opportunités professionnelles, détecter les compétences recherchées et identifier les dispositifs de "
            "formation adaptés.",
            "<b>Satisfaction & Pouvoir d'agir :</b> Se rendre pleinement autonome dans la gestion de sa carrière, lever "
            "les freins psychologiques, sécuriser financièrement sa transition et engager des actions concrètes "
            "vérifiées sur le terrain.",
        ],
    )
    add_card(
        layout,
        title="Premier échange gratuit (30 à 45 min en visio)",
        body="Présentation détaillée de l'accompagnement, analyse de votre situation, clarification de vos objectifs "
             "et vérification de l'adéquation mutuelle avant tout engagement.<br/><br/>"
             "<i>Le contenu du programme est ajustable après cet échange en fonction de vos besoins spécifiques et du "
             "travail déjà mené dans d'autres cadres.</i>",
        color=PDFStyle.COLOR_ALMOND,
    )
    layout.render()

