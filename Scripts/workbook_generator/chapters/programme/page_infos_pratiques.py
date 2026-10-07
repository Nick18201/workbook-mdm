from .common import add_card_row, programme_layout


def create_programme_page_infos_pratiques(c):
    """Practical information (Qualiopi indicator 1), as three rows of two cards."""
    layout = programme_layout(
        c, "Informations *pratiques.*", "Informations pratiques",
        lead="Modalités, délais d'accès et cadre réglementaire (indicateur 1 Qualiopi).",
    )
    add_card_row(layout, [
        {
            "label": "Prérequis",
            "body": "<b>Aucun prérequis</b> de diplôme, de niveau d'études, d'expérience professionnelle ou de "
                    "statut n'est exigé.<br/><br/>Le bilan de compétences est ouvert à toute personne active : "
                    "salariés du secteur privé, indépendants, agents publics et demandeurs d'emploi souhaitant faire "
                    "le point sur leur trajectoire.",
        },
        {
            "label": "Délais d'accès",
            "items": [
                "<b>Premier échange gratuit (30 min en visio) :</b> pour cerner vos attentes et valider l'adéquation.",
                "<b>Inscription sur MonCompteFormation :</b> validation en ligne de votre dossier.",
                "<b>Délai légal de rétractation :</b> un délai minimal de <b>14 jours ouvrés</b> est obligatoire "
                "entre votre inscription et la 1re séance pédagogique.",
            ],
        },
    ])
    add_card_row(layout, [
        {
            "label": "Modalités d'évaluation",
            "items": [
                "<b>Évaluation continue :</b> validation des livrables et des exercices pratiques à la fin de chaque "
                "séance.",
                "<b>Questionnaire de satisfaction :</b> évaluation anonyme à chaud en fin de parcours pour mesurer la "
                "qualité de l'accompagnement et l'atteinte de vos objectifs.",
                "<b>Entretien individuel de suivi à 6 mois (45 min) :</b> point d'étape sur la concrétisation de vos "
                "démarches.",
            ],
        },
        {
            "label": "Accessibilité & handicap",
            "body": "Notre démarche s'adapte à chacun : nous adaptons les rythmes, les supports et les formats "
                    "d'accompagnement.<br/><br/>Notre <b>référent handicap</b> étudie chaque situation pour organiser "
                    "les aménagements nécessaires ou vous orienter :<br/><br/><b>Nicolas Blum Ferracci</b><br/>"
                    "<b>nicolas.blumferracci@margedemanoeuvre.fr</b>",
        },
    ])
    add_card_row(layout, [
        {
            "label": "Contact & inscription",
            "body": "Pour poser vos questions, étudier vos possibilités de prise en charge ou convenir d'un premier "
                    "échange :",
            "items": [
                "<b>Email :</b> contact@margedemanoeuvre.fr",
                "<b>Contact direct :</b> nicolas.blumferracci@margedemanoeuvre.fr",
                "<b>Prise de rendez-vous en ligne :</b> margedemanoeuvre.fr/contact/",
            ],
        },
        {
            "label": "Confidentialité & propriété",
            "body": "Le document de synthèse officiel co-rédigé <b>n'appartient qu'à vous</b> et ne peut être "
                    "communiqué à aucun tiers sans votre accord explicite (art. L. 6313-4 du Code du travail).<br/><br/>"
                    "L'ensemble de vos échanges et réflexions est couvert par une <b>obligation stricte de secret et de "
                    "confidentialité</b>.",
        },
    ])
    layout.render()

