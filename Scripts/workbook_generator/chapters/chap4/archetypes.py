from reportlab.lib.units import cm

from ...config import PDFStyle
from ...templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig


def create_archetypes_v2_page(c):
    # Page 1
    layout = PageLayout(
        c,
        "Repérer ce que l'argent représente pour vous (1/2)",
        config=LayoutConfig(part_title="6. ARCHÉTYPES"),
    )
    layout.add_text(
        "L'argent n'a pas la même signification pour tout le monde. Pour certaines personnes, il représente d'abord la sécurité. Pour d'autres, la liberté, la réussite, l'indépendance, le plaisir, la reconnaissance ou encore la réparation d'une ancienne insécurité.",
        config=TextConfig(spacing_after=0.2 * cm),
    )
    layout.add_text(
        "Les profils ci-dessous ne sont pas des cases fixes. Ils servent à repérer vos tendances dominantes, vos automatismes et les tensions qui peuvent influencer vos choix professionnels.",
        config=TextConfig(spacing_after=0.2 * cm),
    )
    layout.add_text(
        "Prenez le temps de lire chaque tendance : elle peut être une ressource lorsqu'elle vous aide à faire des choix ajustés, mais peut aussi devenir limitante lorsqu'elle freine vos envies ou vous pousse à agir contre vos besoins réels.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    archs = [
        (
            "Le sécuritaire : l'argent comme protection",
            "L'argent sert d'abord à se sentir à l'abri, à anticiper et à éviter le manque.",
            "Question-clé : De quelle sécurité ai-je réellement besoin pour avancer sans me figer ?",
        ),
        (
            "Le méritant : l'argent comme preuve d'effort",
            "L'argent doit être gagné, justifié, mérité. Il est souvent associé au travail, à l'effort ou au sacrifice.",
            "Question-clé : Est-ce que je confonds ma valeur avec mon niveau d'effort ?",
        ),
        (
            "L'indépendant : l'argent comme liberté d'action",
            "L'argent représente l'autonomie. Il permet de choisir, partir, décider et ne pas dépendre.",
            "Question-clé : Comment construire mon autonomie sans tout transformer en obligation de contrôle ?",
        ),
        (
            "Le généreux : l'argent comme lien",
            "L'argent sert à aider, offrir, soutenir, faire plaisir ou prendre soin des autres.",
            "Question-clé : Est-ce que ma générosité respecte aussi mes propres limites ?",
        ),
    ]
    for title, desc, q_cle in archs:
        layout.add_text(
            title,
            config=TextConfig(
                style_choice="subtitle",
                color=PDFStyle.COLOR_ACCENT_BLUE,
                font_size=11,
                spacing_after=0.1 * cm,
            ),
        )
        layout.add_text(desc, config=TextConfig(font_size=10, spacing_after=0.1 * cm))
        layout.add_text(
            q_cle,
            config=TextConfig(
                style_choice="italic",
                color=PDFStyle.COLOR_TEXT_SECONDARY,
                font_size=10,
                spacing_after=0.4 * cm,
            ),
        )
    layout.render()

    # Page 2
    layout2 = PageLayout(
        c,
        "Repérer ce que l'argent représente pour vous (2/2)",
        config=LayoutConfig(part_title="6. ARCHÉTYPES"),
    )
    layout2.add_text(
        "Lisez la suite des profils et repérez ce qui résonne le plus pour vous, que ce soit dans l'aspect ressource ou dans l'aspect limitant.",
        config=TextConfig(spacing_after=0.5 * cm),
    )
    archs2 = [
        (
            "L'évitant : l'argent comme inconfort",
            "L'argent est un sujet sensible, inconfortable ou chargé.",
            "Question-clé : Qu'est-ce que je cherche à ne pas ressentir quand j'évite l'argent ?",
        ),
        (
            "L'ambitieux : l'argent comme réussite ou progression",
            "L'argent représente la progression, la réussite, l'impact, la reconnaissance ou le changement de niveau.",
            "Question-clé : Mon ambition financière est-elle au service de ma vie, ou est-ce ma vie qui sert mon ambition ?",
        ),
        (
            "Le plaisir : l'argent comme expérience",
            "L'argent permet de vivre, profiter, expérimenter et se faire plaisir.",
            "Question-clé : Comment garder le plaisir sans compromettre ma sécurité future ?",
        ),
        (
            "Le réparateur : l'argent comme réparation",
            "L'argent vient répondre à une ancienne insécurité, une injustice, une blessure sociale, familiale ou relationnelle.",
            "Question-clé : Quelle ancienne histoire mon rapport à l'argent essaie-t-il encore de réparer ?",
        ),
    ]
    for title, desc, q_cle in archs2:
        layout2.add_text(
            title,
            config=TextConfig(
                style_choice="subtitle",
                color=PDFStyle.COLOR_ACCENT_BLUE,
                font_size=11,
                spacing_after=0.1 * cm,
            ),
        )
        layout2.add_text(desc, config=TextConfig(font_size=10, spacing_after=0.1 * cm))
        layout2.add_text(
            q_cle,
            config=TextConfig(
                style_choice="italic",
                color=PDFStyle.COLOR_TEXT_SECONDARY,
                font_size=10,
                spacing_after=0.4 * cm,
            ),
        )

    layout2.add_question_block(
        "Quels archétypes vous correspondent le plus aujourd'hui ? Lesquels vous soutiennent, lesquels vous limitent ?",
        "v2_arch_choix",
        config=QuestionConfig(box_height=3.5 * cm),
    )
    layout2.render()
