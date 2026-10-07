from .common import add_card, add_card_row, programme_layout


def create_programme_page_organisation_pedagogie(c):
    """How the bilan is organised: means and tools, work between sessions, support and ethics."""
    layout = programme_layout(
        c, "Organisation *et moyens pédagogiques.*", "Organisation et moyens",
        lead="Modalités d'accompagnement, outils exclusifs et travail inter-séances.",
    )
    add_card_row(layout, [
        {
            "label": "Moyens et outils",
            "items": [
                "<b>Entretiens 100 % en visio :</b> séances individuelles de 1 h 20, espacées de 1 à 2 semaines, "
                "avec le même accompagnateur tout au long du bilan.",
                "<b>7 carnets de bord guidés :</b> supports structurés pas à pas pour mener votre travail personnel "
                "en toute autonomie (conservés à vie).",
                "<b>Copilote IA exclusif :</b> un assistant interactif conçu pour challenger vos réflexions, stimuler "
                "votre créativité et vous guider dans vos exercices.",
                "<b>Enquêtes-métiers terrain :</b> confrontation au réel et rencontres de professionnels en activité "
                "grâce à des guides d'entretien ciblés.",
            ],
        },
        {
            "label": "Ressources et tests",
            "items": [
                "<b>Espace Notion ressource :</b> bibliothèque exclusive d'articles, podcasts, vidéos et fiches "
                "repères accessible jusqu'au suivi à 6 mois.",
                "<b>Tests certifiés :</b> questionnaire officiel <b>MBTI®</b> (Myers-Briggs) et inventaire d'intérêts "
                "professionnels (Hexa3D).",
                "<b>Exercices de créativité :</b> cartes projectives, matrices décisionnelles et grilles d'arbitrage "
                "anti-compromis.",
                "<b>Assistance pédagogique réactive :</b> suivi continu par email et téléphone, réponse garantie sous "
                "48 h ouvrées maximum.",
            ],
        },
    ])
    add_card(
        layout,
        title="Organisation et réalisation du travail inter-séances",
        white=True,
        items=[
            "<b>Rythme et alternance :</b> Le bilan alterne des entretiens réguliers en visio et des temps dédiés de "
            "travail personnel : 10 à 20 h en tout selon les personnes, soit environ 1 h 30 à 3 h par carnet, en plus "
            "des 14 h d'accompagnement.",
            "<b>Supports accessibles en continu :</b> Vos exercices s'appuient sur vos carnets guidés et l'espace "
            "Notion ressource, disponibles dès la formalisation de votre parcours.",
            "<b>Consignes personnalisées :</b> À l'issue de chaque séance, votre accompagnateur formule des consignes "
            "claires et adapte les exercices à votre charge mentale et à vos priorités du moment.",
        ],
    )
    add_card(
        layout,
        title="Assistance continue et engagement déontologique",
        items=[
            "<b>Assistance pédagogique et technique réactive :</b> Tout au long du parcours, vous n'êtes jamais "
            "seul(e). Votre accompagnateur référent répond à vos questions par email ou par téléphone dans un délai "
            "garanti de <b>48 h ouvrées</b>.",
            "<b>Cadre de confiance absolu :</b> Respect strict du secret professionnel (Code du travail, "
            "art. L. 6313-4), posture de neutralité et protection intégrale de vos données personnelles. Les bilans "
            "menés par Lysiane Brand, psychologue du travail, relèvent en outre du code de déontologie des "
            "psychologues.",
        ],
    )
    layout.render()

