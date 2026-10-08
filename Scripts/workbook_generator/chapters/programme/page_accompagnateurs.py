from workbook_generator.config import PDFStyle

from .common import add_card, programme_layout


def create_programme_page_accompagnateurs(c):
    """The two consultants who designed the method and run the bilans."""
    layout = programme_layout(
        c, "Vos *accompagnateurs.*", "Vos accompagnateurs",
        lead="Des profils complémentaires alliant psychologie du travail et réalité du marché.",
    )
    add_card(
        layout,
        label="Psychologue du travail",
        title="Lysiane Brand",
        subtitle="Psychologue du travail · Consultante en bilan de compétences",
        items=[
            "<b>Déontologie & Confidentialité :</b> Soumise au code de déontologie des psychologues, Lysiane garantit "
            "une stricte confidentialité des échanges et documents produits, dans une posture de neutralité tout au "
            "long de votre accompagnement.",
            "<b>Expertise recrutement & marché :</b> 4 années d'expérience dans le secteur du recrutement (en "
            "entreprise et en cabinet) lui confèrent une solide connaissance du marché de l'emploi, de ses exigences "
            "et de ses opportunités réelles.",
            "<b>Outils & Méthodes :</b> Rompue aux techniques d'entretien approfondi, elle maîtrise les "
            "approches cliniques propres à sa formation. Elle a conçu et éprouvé le test des fonctionnements "
            "cognitifs utilisé pendant le bilan.",
        ],
        color=PDFStyle.COLOR_LILAC,
    )
    add_card(
        layout,
        label="Transformation & opérations",
        title="Nicolas Blum Ferracci",
        subtitle="Consultant en transformation · Associé & Responsable des opérations",
        items=[
            "<b>Dynamiques de transformation & conduite du changement :</b> Formé à la psychologie et rompu aux "
            "dynamiques de transformation, Nicolas accompagne les professionnels à des moments charnières de leur "
            "trajectoire. Consultant indépendant en transformation digitale et conduite du changement en entreprise, "
            "fort de 5 ans d’expérience en ESN, il dispose d’une compréhension fine des mutations organisationnelles "
            "et des réalités concrètes du monde professionnel.",
            "<b>Parcours hybride & culture de l'innovation :</b> Associé et responsable des opérations chez Marge de "
            "Manœuvre, il articule ses accompagnements autour d'un parcours hybride : l'expérience du recrutement et "
            "du terrain d'entreprise pour ancrer chaque démarche dans le réel, la rigueur du design d’expérience pour "
            "modéliser des parcours sur-mesure, et une culture continue de l’innovation pour ouvrir le champ des "
            "possibles.",
            "<b>Postures & leviers d'action :</b> En bilan de compétences, il aide chacun à faire le tri, à lever les "
            "blocages et à formaliser une trajectoire claire : valorisant la singularité de la personne, alignée avec "
            "les exigences du marché et lui redonnant toute sa capacité d’action.",
        ],
        color=PDFStyle.COLOR_SKY,
    )
    layout.render()

