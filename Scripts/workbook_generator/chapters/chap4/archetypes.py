from reportlab.lib.units import cm

from ...templates import PageLayout, LayoutConfig, QuestionItem

# (name, what money stands for, description, key question)
_TENDANCES = [
    ("Le sécuritaire", "l'argent comme protection",
     "L'argent sert d'abord à se sentir à l'abri, à anticiper et à éviter le manque.",
     "De quelle sécurité ai-je réellement besoin pour avancer sans me figer ?"),
    ("Le méritant", "l'argent comme preuve d'effort",
     "L'argent doit être gagné, justifié, mérité. Il est souvent associé au travail, à l'effort ou au sacrifice.",
     "Est-ce que je confonds ma valeur avec mon niveau d'effort ?"),
    ("L'indépendant", "l'argent comme liberté d'action",
     "L'argent représente l'autonomie : il permet de choisir, partir, décider, ne pas dépendre.",
     "Comment construire mon autonomie sans tout transformer en besoin de contrôle ?"),
    ("Le généreux", "l'argent comme lien",
     "L'argent sert à aider, offrir, soutenir, faire plaisir ou prendre soin des autres.",
     "Ma générosité respecte-t-elle aussi mes propres limites ?"),
    ("L'évitant", "l'argent comme inconfort",
     "L'argent est un sujet sensible, inconfortable ou chargé.",
     "Qu'est-ce que je cherche à ne pas ressentir quand j'évite l'argent ?"),
    ("L'ambitieux", "l'argent comme réussite",
     "L'argent représente la progression, la réussite, l'impact, la reconnaissance ou le changement de niveau.",
     "Mon ambition financière sert-elle ma vie, ou est-ce ma vie qui sert mon ambition ?"),
    ("Le plaisir", "l'argent comme expérience",
     "L'argent permet de vivre, de profiter, d'expérimenter et de se faire plaisir.",
     "Comment garder le plaisir sans compromettre ma sécurité future ?"),
    ("Le réparateur", "l'argent comme réparation",
     "L'argent répond à une ancienne insécurité, une injustice, une blessure sociale, familiale ou relationnelle.",
     "Quelle ancienne histoire mon rapport à l'argent essaie-t-il encore de réparer ?"),
]


def create_archetypes_v2_page(c):
    """Exercise 7: eight tendencies of what money stands for, then which ones apply."""
    layout = PageLayout(c, "Ce que l'argent *représente pour vous.*",
                        config=LayoutConfig(part_title="Exercice 7 · Tendances"))
    layout.add_paragraphs([
        "L'argent n'a pas la même signification pour tout le monde : sécurité, liberté, réussite, indépendance, "
        "plaisir, reconnaissance, ou réparation d'une ancienne insécurité.",
        "Ces tendances ne sont pas des cases. Elles aident à repérer vos réflexes dominants et les tensions qui "
        "pèsent sur vos choix. Une tendance est une ressource quand elle vous aide à faire des choix ajustés, et un "
        "frein quand elle vous pousse à agir contre vos besoins réels. Cochez celles qui vous correspondent.",
    ], spacing_after=0.45 * cm)
    cards = [
        {"title": name, "subtitle": stands_for, "text": text, "note": f"Question clé : {question}",
         "field_id": f"v2_arch_{i + 1}"}
        for i, (name, stands_for, text, question) in enumerate(_TENDANCES)
    ]
    layout.add_info_cards(cards[:4], columns=2, check_label="Me correspond")
    layout.page_break()
    layout.add_info_cards(cards[4:], columns=2, check_label="Me correspond")
    layout.add_questions_group([
        QuestionItem("Quelles tendances vous correspondent le plus aujourd'hui ? Lesquelles vous soutiennent, "
                     "lesquelles vous freinent ?", "v2_arch_choix"),
    ], max_box_height=5.0 * cm)
    layout.render()
