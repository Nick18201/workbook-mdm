from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle
from workbook_generator.templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig
from workbook_generator.forms import create_checkbox


TENSIONS_LIST = [
    "Liberté / sécurité",
    "Réussite / équilibre",
    "Bienveillance / affirmation de soi",
    "Stimulation / stabilité",
    "Autonomie / appartenance",
    "Reconnaissance / discrétion",
    "Sens / rémunération",
    "Engagement / protection de soi",
    "Créativité / cadre",
    "Ambition / qualité de vie",
    "Loyauté / besoin de changement",
    "Responsabilité / légereté"
]


def create_tensions_page1(c):
    layout = PageLayout(
        c,
        "8. Mes tensions de valeurs (1/2)",
        config=LayoutConfig(part_title="8. TENSIONS DE VALEURS")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Repérer les contradictions internes entre des valeurs importantes pour vous.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3 * cm)
    )
    layout.add_text(
        "Certaines valeurs peuvent être importantes pour vous tout en entrant en contradiction. Cochez les tensions qui vous parlent :",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    start_x = layout.text_x
    start_y = layout.y_cursor
    form = c.acroForm

    # Draw 12 tensions in 2 columns
    for idx, tension in enumerate(TENSIONS_LIST):
        col = idx % 2
        row = idx // 2
        x = start_x if col == 0 else start_x + layout.target_width / 2.0
        y = start_y - row * 0.55 * cm

        create_checkbox(
            form,
            f"tension_chk_{idx}",
            pos=(x, y),
            size=10,
            tooltip=f"Cocher la tension {tension}"
        )
        
        c.saveState()
        c.setFont(PDFStyle.FONT_BODY, 9)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(x + 0.5 * cm, y + 0.05 * cm, tension)
        c.restoreState()

    # Move cursor below checklist
    layout.y_cursor = start_y - 6 * 0.55 * cm - 0.5 * cm

    layout.add_text(
        "Choisissez les deux tensions les plus présentes dans votre parcours. Voici le détail de la première :",
        config=TextConfig(style_choice="subtitle", font_size=10, color=PDFStyle.COLOR_ACCENT_RED, spacing_after=0.3 * cm)
    )

    layout.add_question_block(
        "Tension 1 - Quelles sont les deux valeurs en tension ? Dans quelles situations cela apparaît-il ?",
        "tension1_situations",
        config=QuestionConfig(box_height=2.7 * cm),
    )
    layout.add_question_block(
        "Arbitrage - Quelle valeur avez-vous tendance à privilégier ? Laquelle sacrifiez-vous ?",
        "tension1_arbitrage",
        config=QuestionConfig(box_height=2.7 * cm),
    )
    layout.add_question_block(
        "Équilibre - Quel meilleur équilibre ou compromis constructif pourriez-vous rechercher ?",
        "tension1_equilibre",
        config=QuestionConfig(box_height=2.7 * cm),
    )

    layout.render()


def create_tensions_page2(c):
    layout = PageLayout(
        c,
        "8. Mes tensions de valeurs (2/2)",
        config=LayoutConfig(part_title="8. TENSIONS DE VALEURS")
    )
    layout.add_text(
        "Détaillez ici la seconde tension de valeurs identifiée dans votre vie professionnelle :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Tension 2 - Quelles sont les deux valeurs en tension ? Dans quelles situations cela apparaît-il ?",
        "tension2_situations",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Arbitrage - Quelle valeur avez-vous tendance à privilégier ? Laquelle sacrifiez-vous ?",
        "tension2_arbitrage",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Équilibre - Quel meilleur équilibre ou compromis constructif pourriez-vous rechercher ?",
        "tension2_equilibre",
        config=QuestionConfig(box_height=3.0 * cm),
    )

    layout.render()


def create_synthese_page(c):
    layout = PageLayout(
        c,
        "Synthèse finale",
        config=LayoutConfig(part_title="SYNTHÈSE FINALE")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Rassembler vos conclusions pour guider la suite de votre projet de transition.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3 * cm)
    )
    layout.add_text(
        "Complétez les phrases suivantes pour résumer ce qui compte profondément pour vous :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    prompts = [
        ("Ce qui compte vraiment pour moi au travail, c'est :", "synthese_compte_travail", 0.8 * cm),
        ("Je me sens aligné(e) quand :", "synthese_aligne_quand", 0.8 * cm),
        ("Je perds de l'énergie quand :", "synthese_perte_energie", 0.8 * cm),
        ("Mes 3 valeurs non négociables sont :", "synthese_non_nego", 0.8 * cm),
        ("Pour les respecter, j'ai besoin de :", "synthese_besoins_nego", 0.8 * cm),
        ("Dans mon futur projet pro, je veux davantage :", "synthese_davantage", 0.8 * cm),
        ("Dans mon futur projet pro, je veux moins :", "synthese_moins", 0.8 * cm),
    ]

    for question, field_id, height in prompts:
        layout.add_question_block(
            question,
            field_id,
            config=QuestionConfig(box_height=height, color_alternation=True)
        )

    layout.render()
