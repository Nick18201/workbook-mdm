from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle
from workbook_generator.templates import PageLayout, LayoutConfig


def create_psycho_edu_pages(c):
    """
    Reading pages « Comprendre ses racines »: the habitus, the sense of illegitimacy, the
    implicit family contract, impeded activity, then three tools (continues over pages).
    """
    layout = PageLayout(c, "Comprendre *ses racines.*", config=LayoutConfig(part_title="À lire · Mon parcours"))
    layout.add_paragraphs([
        "Lister vos savoir-faire ne suffit pas pour décider de la suite. Vous n'êtes pas une somme de compétences "
        "techniques : vous êtes aussi le résultat d'une histoire.",
        "Votre façon de travailler, votre rapport à l'argent, à l'autorité ou à la réussite ont été façonnés par "
        "votre famille et votre milieu d'origine. Ces pages vous aident à repérer ces « bagages invisibles » et à "
        "faire le tri : ce que vous gardez, et ce que vous laissez de côté pour votre projet.",
    ], size=PDFStyle.SIZE_LEAD)

    layout.add_heading("1. Le « sac à dos » social (l'habitus)")
    layout.add_paragraphs([
        "L'habitus, c'est votre manière spontanée de réagir, de parler, de vous tenir, héritée de vos parents et "
        "de votre milieu social. Il agit comme un logiciel installé depuis l'enfance.",
        "Quand vous changez de milieu professionnel (d'une famille d'ouvriers à un poste de cadre, ou l'inverse), "
        "ce logiciel peut créer un décalage : une gêne diffuse, l'impression de porter un costume mal taillé.",
    ])

    layout.add_heading("Le sentiment d'illégitimité")
    layout.add_paragraphs([
        "« Un jour, ils vont se rendre compte que je ne suis pas à la hauteur. » Cette pensée signale souvent un "
        "conflit lié au changement de milieu social, ce que la sociologie appelle la névrose de classe. Ce n'est "
        "pas une maladie.",
        "• Vous réussissez mieux que vos parents : vous pouvez ressentir de la culpabilité, la peur de vous "
        "éloigner d'eux.",
        "• Votre situation est moins prestigieuse que la leur : vous pouvez ressentir de la honte.",
        "Ce sentiment a des effets concrets : il peut vous retenir de demander une augmentation, ou vous pousser "
        "au surmenage.",
    ])

    layout.add_heading("2. Le contrat familial implicite")
    layout.add_paragraphs([
        "Chaque famille tient un « livre de comptes » invisible : ce que l'on pense devoir à ses parents.",
        "• Les loyautés invisibles : il arrive de s'arrêter juste avant le but, pour ne pas dépasser ses parents. "
        "L'échec devient une façon de leur rester fidèle.",
        "• La réparation : avez-vous choisi votre métier par goût, ou pour réparer une histoire familiale "
        "(injustice, maladie) ?",
        "• Le mythe familial : « Chez nous, on est des intellectuels », « Chez nous, on est solidaires… ». Un projet "
        "qui contredit ce mythe rencontre des résistances, chez vous comme autour de vous.",
    ])

    layout.add_heading("3. Souffrance et plaisir au travail")
    layout.add_paragraphs([
        "Travailler, ce n'est pas seulement exécuter une tâche : c'est y mettre du sien. Quand vous ne pouvez pas "
        "faire votre travail « bien », selon vos propres critères, vous en souffrez. La psychologie du travail "
        "parle d'activité empêchée.",
        "Cette souffrance n'est pas une faiblesse : elle montre que vous tenez à la qualité de votre travail. "
        "L'enjeu est de la transformer en pouvoir d'agir, c'est-à-dire de retrouver une marge de manœuvre.",
    ])

    layout.add_heading("4. Trois outils pour votre bilan")
    layout.add_paragraphs([
        "Trois outils pour faire le tri dans votre héritage et décider en connaissance de cause.",
    ])
    for heading, text in (
        ("A. Vos appuis dans l'histoire familiale",
         "Au-delà de l'arbre généalogique officiel, repérez les personnes qui vous ont donné confiance ou transmis "
         "des repères solides. Appuyez-vous sur elles plutôt que sur celles qui vous ont jugé."),
        ("B. Le roman familial",
         "Repérez les répétitions et les phrases qui reviennent (« Il faut souffrir pour réussir »). Les "
         "identifier, c'est les empêcher de décider à votre place."),
        ("C. L'objectif : réussir sans trahir",
         "Vous avez le droit de changer, de réussir, de gagner de l'argent, sans renier votre famille. La "
         "question devient : comment garder ses valeurs (courage, honnêteté) sous une forme qui vous appartient ? "
         "C'est la différenciation : rester en lien, tout en décidant pour vous-même."),
    ):
        layout.add_heading(heading, size=PDFStyle.SIZE_TITLE_ELEMENT)
        layout.add_paragraphs([text], spacing_after=0.45 * cm)
    layout.add_callout("Repérer ces héritages, c'est reprendre la main sur vos choix.", title="À retenir")
    layout.render()
