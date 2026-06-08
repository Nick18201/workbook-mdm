"""
Module PVQ-21 de Schwartz — Questionnaire de Valeurs, Validation & Personnalité Pro.

Ce module implémente :
1. Page de référence des 10 valeurs universelles de Schwartz
2. Le PVQ-21 (Portrait Values Questionnaire — 21 items)
3. Questions de validation (Désirabilité Sociale, Faking Bad, Infréquence)
4. Traits de personnalité professionnels (6 dimensions × 2 items)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig
from workbook_generator.forms import create_checkbox


# =============================================================================
# DONNÉES
# =============================================================================

SCHWARTZ_VALUES = [
    ("Autonomie", "Liberté de pensée et d'action, créativité, curiosité, indépendance."),
    ("Stimulation", "Recherche de nouveauté, de défis, d'excitation dans la vie."),
    ("Hédonisme", "Plaisir personnel, gratification sensorielle, joie de vivre."),
    ("Réussite", "Succès personnel, démonstration de compétence, ambition."),
    ("Pouvoir", "Statut social, prestige, contrôle sur les ressources et les personnes."),
    ("Sécurité", "Stabilité, harmonie, protection de soi et de ses proches."),
    ("Conformité", "Respect des normes sociales, obéissance, autodiscipline."),
    ("Tradition", "Respect des coutumes, humilité, acceptation de son lot dans la vie."),
    ("Bienveillance", "Préserver le bien-être des proches, loyauté, honnêteté."),
    ("Universalisme", "Compréhension, tolérance, justice sociale, protection de la nature."),
]

PVQ21_ITEMS = [
    # (id, texte, valeur associée)
    ("pvq_01", "Penser à de nouvelles idées et être créatif est important pour cette personne. Elle aime faire les choses à sa façon, de manière originale.", "Autonomie"),
    ("pvq_02", "Elle trouve important d'être riche. Elle veut avoir beaucoup d'argent et posséder des choses chères.", "Pouvoir"),
    ("pvq_03", "Elle pense que c'est important que chaque individu dans le monde soit traité de manière égale. Elle croit que tout le monde devrait avoir des chances égales dans la vie.", "Universalisme"),
    ("pvq_04", "Elle trouve important de montrer de quoi elle est capable. Elle veut que les gens admirent ce qu'elle fait.", "Réussite"),
    ("pvq_05", "Vivre dans un environnement sécurisant est important pour elle. Elle évite tout ce qui pourrait mettre sa sécurité en danger.", "Sécurité"),
    ("pvq_06", "Elle aime les surprises et recherche toujours de nouvelles choses à faire. Elle pense qu'il est important de faire beaucoup de choses différentes dans la vie.", "Stimulation"),
    ("pvq_07", "Elle croit que les gens devraient faire ce qu'on leur dit. Elle pense que les gens devraient suivre les règles à tout moment, même quand personne ne les regarde.", "Conformité"),
    ("pvq_08", "Elle trouve important d'écouter les gens qui sont différents d'elle. Même quand elle n'est pas d'accord avec eux, elle tient tout de même à les comprendre.", "Universalisme"),
    ("pvq_09", "Être humble et modeste est important pour elle. Elle essaie de ne pas attirer l'attention sur elle.", "Tradition"),
    ("pvq_10", "Avoir du bon temps est important pour elle. Elle aime bien se faire plaisir.", "Hédonisme"),
    ("pvq_11", "Elle trouve important de prendre ses propres décisions sur ce qu'elle fait. Elle aime être libre et ne pas dépendre des autres.", "Autonomie"),
    ("pvq_12", "C'est très important pour elle d'aider les gens autour d'elle. Elle désire prendre soin de leur bien-être.", "Bienveillance"),
    ("pvq_13", "Avoir beaucoup de succès est important pour elle. Elle espère que les gens reconnaîtront ses réussites.", "Réussite"),
    ("pvq_14", "Elle trouve très important que le gouvernement garantisse la sécurité contre tous les dangers. Elle veut que l'État soit fort pour défendre ses citoyens.", "Sécurité"),
    ("pvq_15", "Elle recherche l'aventure et aime prendre des risques. Elle veut avoir une vie palpitante.", "Stimulation"),
    ("pvq_16", "Elle trouve important de toujours se comporter correctement. Elle veut éviter de faire des choses que les gens trouveraient mal.", "Conformité"),
    ("pvq_17", "Elle trouve important d'obtenir le respect des autres. Elle veut que les gens fassent ce qu'elle dit.", "Pouvoir"),
    ("pvq_18", "Elle trouve important d'être loyale envers ses amis. Elle veut se dévouer pour les personnes qui lui sont proches.", "Bienveillance"),
    ("pvq_19", "Elle croit fermement que l'on devrait se préoccuper de la nature. Protéger l'environnement est important pour elle.", "Universalisme"),
    ("pvq_20", "Les traditions sont importantes pour elle. Elle essaie de suivre les coutumes qui lui ont été transmises par sa religion ou sa famille.", "Tradition"),
    ("pvq_21", "Elle recherche toutes les occasions de s'amuser. C'est important pour elle de faire des choses qui lui donnent du plaisir.", "Hédonisme"),
]

VALIDATION_ITEMS_FAKING_GOOD = [
    ("val_fg_01", "Je n'ai jamais prononcé le moindre mensonge, même pour éviter de blesser quelqu'un."),
    ("val_fg_02", "Il ne m'est jamais arrivé d'être en retard à un rendez-vous ou de repousser une échéance."),
    ("val_fg_03", "Je ne ressens absolument jamais de jalousie ou d'envie face au succès fulgurant d'un collègue."),
    ("val_fg_04", "Je suis capable de rester concentré(e) à 100% sur mon travail toute la journée, sans jamais me laisser distraire."),
]

VALIDATION_ITEMS_FAKING_BAD = [
    ("val_fb_01", "J'ai souvent l'impression que la plupart des choses que j'entreprends finissent par échouer."),
    ("val_fb_02", "Je me sens régulièrement incapable de faire face aux responsabilités basiques de mon quotidien."),
    ("val_fb_03", "Je pense sincèrement n'avoir aucune compétence ou talent utile à apporter à une équipe professionnelle."),
    ("val_fb_04", "La moindre remarque constructive sur mon travail me fait douter de ma valeur globale en tant que personne."),
]

VALIDATION_ITEMS_INFREQUENCY = [
    ("val_inf_01", "Il m'arrive régulièrement de ne pas dormir pendant une semaine complète sans ressentir de fatigue."),
    ("val_inf_02", "Je suis capable de lire un livre de 300 pages en moins de dix secondes."),
]

PERSONALITY_DIMENSIONS = [
    {
        "name": "Affirmation de soi",
        "items": [
            ("pers_assert_01", "Je n'hésite pas à prendre la parole pour exprimer mon désaccord, même si je sais que mon opinion est impopulaire.", False),
            ("pers_assert_02", "Face à un conflit au travail, j'ai tendance à faire des concessions rapidement pour ramener la paix.", True),
        ],
    },
    {
        "name": "Résilience et Énergie",
        "items": [
            ("pers_resil_01", "Face à un échec inattendu ou un obstacle majeur, je retrouve très rapidement ma motivation pour essayer autre chose.", False),
            ("pers_resil_02", "J'ai un niveau d'énergie naturel qui me permet d'assumer des journées de travail très intenses sans m'épuiser facilement.", False),
        ],
    },
    {
        "name": "Sang-froid et Gestion du stress",
        "items": [
            ("pers_compo_01", "Je reste calme et lucide face aux urgences, sans laisser mon stress déborder sur les autres.", False),
            ("pers_compo_02", "Les petits imprévus ou les changements de programme de dernière minute ont tendance à m'irriter fortement.", True),
        ],
    },
    {
        "name": "Orientation collective",
        "items": [
            ("pers_group_01", "Je suis beaucoup plus performant(e) et stimulé(e) lorsque je travaille en étroite collaboration avec d'autres personnes.", False),
            ("pers_group_02", "Je préfère de loin prendre mes décisions seul(e) plutôt que de devoir consulter un groupe et chercher un consensus.", True),
        ],
    },
    {
        "name": "Éthique de travail et Conscience pro.",
        "items": [
            ("pers_ethic_01", "Je m'investis souvent bien au-delà de ce qui m'est strictement demandé pour m'assurer que le résultat final est parfait.", False),
            ("pers_ethic_02", "J'ai parfois du mal à suivre des procédures strictes et je préfère improviser pour arriver au résultat plus vite.", True),
        ],
    },
    {
        "name": "Pensée Radicale / Ouverture",
        "items": [
            ("pers_radic_01", "Je remets souvent en question les méthodes traditionnelles, car je suis convaincu(e) qu'il y a toujours une façon nouvelle et meilleure de faire les choses.", False),
            ("pers_radic_02", "Je préfère appliquer des méthodes qui ont fait leurs preuves depuis longtemps plutôt que de tester de nouvelles approches risquées.", True),
        ],
    },
]


# =============================================================================
# HELPER : Dessiner des items Likert avec checkboxes 1-6
# =============================================================================

def _draw_likert_items(layout, items, show_number=True, start_number=1):
    """
    Dessine une série d'items avec échelle de Likert 1-6 (checkboxes).

    Args:
        layout: PageLayout instance (cursor y est mis à jour)
        items: list of (field_id, text) or (field_id, text, extra_info)
        show_number: whether to prefix with item number
        start_number: first item number
    """
    c = layout.c
    form = c.acroForm

    for idx, item in enumerate(items):
        field_id = item[0]
        text = item[1]
        item_num = start_number + idx

        # Check if we need a page break (leave room for scale + spacing)
        if layout.y_cursor < 4.5 * cm:
            layout.render()
            # Start a new continuation page
            layout.__init__(
                c,
                layout.title + " (suite)",
                config=LayoutConfig(part_title=layout.part_title),
            )

        # Draw question text
        display_text = f"{item_num}. {text}" if show_number else text
        layout.add_text(
            display_text,
            config=TextConfig(font_size=10, spacing_after=0.1 * cm),
        )

        # Draw scale 1 to 6
        scale_y = layout.y_cursor - 0.15 * cm
        start_x = layout.text_x

        for score in range(1, 7):
            x_pos = start_x + (score - 1) * 1.5 * cm
            create_checkbox(
                form,
                f"{field_id}_{score}",
                pos=(x_pos, scale_y),
                size=0.4 * cm,
            )
            c.setFont(PDFStyle.FONT_BODY, 8)
            c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            c.drawString(x_pos + 0.6 * cm, scale_y + 0.1 * cm, str(score))

        layout.y_cursor -= 1.0 * cm


# =============================================================================
# PAGE 1 : Référence des 10 valeurs de Schwartz
# =============================================================================

def create_schwartz_reference_page(c):
    """Page de référence : les 10 valeurs universelles de Schwartz en 2 colonnes."""
    layout = PageLayout(
        c,
        "Les 10 Valeurs Universelles de Schwartz",
        config=LayoutConfig(part_title="1. VALEURS DE SCHWARTZ"),
    )

    layout.add_text(
        "Le modèle de Shalom Schwartz identifie 10 valeurs fondamentales, organisées "
        "en un cercle où les valeurs proches sont compatibles et les valeurs opposées "
        "entrent en tension. Ce cadre sert de référence pour l'ensemble des exercices "
        "qui suivent.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    # Layout en 2 colonnes
    col_width = (layout.target_width - 1.0 * cm) / 2  # gap de 1cm entre colonnes
    col1_x = layout.text_x
    col2_x = layout.text_x + col_width + 1.0 * cm

    y_start = layout.y_cursor - 0.3 * cm
    line_height_name = 0.5 * cm
    line_height_desc = 0.45 * cm
    block_spacing = 0.6 * cm

    for i, (name, desc) in enumerate(SCHWARTZ_VALUES):
        col_idx = i % 2  # 0 = left, 1 = right
        row_idx = i // 2

        x = col1_x if col_idx == 0 else col2_x
        y = y_start - row_idx * (line_height_name + line_height_desc + block_spacing)

        # Value name (bold, accent color)
        c.setFont(PDFStyle.FONT_SUBTITLE, 11)
        color = PDFStyle.COLOR_ACCENT_BLUE if i % 2 == 0 else PDFStyle.COLOR_ACCENT_RED
        c.setFillColor(color)
        c.drawString(x, y, f"• {name}")

        # Description (body, secondary)
        c.setFont(PDFStyle.FONT_BODY, 9)
        c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
        # Wrap description within column width
        from workbook_generator.utils import cached_simpleSplit as simpleSplit
        desc_lines = simpleSplit(desc, PDFStyle.FONT_BODY, 9, col_width - 0.5 * cm)
        desc_y = y - line_height_name
        for dl in desc_lines:
            c.drawString(x + 0.3 * cm, desc_y, dl)
            desc_y -= line_height_desc

    # Update cursor to below the grid
    total_rows = (len(SCHWARTZ_VALUES) + 1) // 2
    layout.y_cursor = y_start - total_rows * (line_height_name + line_height_desc + block_spacing) - 0.5 * cm

    # Note de lecture
    layout.add_text(
        "Astuce : Les valeurs opposées dans le cercle de Schwartz créent des tensions naturelles "
        "(ex: Autonomie ↔ Conformité, Pouvoir ↔ Universalisme). Identifier ces tensions "
        "est aussi important que de connaître ses valeurs dominantes.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3 * cm),
    )

    layout.render()


# =============================================================================
# PAGES 2-5 : Le Questionnaire PVQ-21
# =============================================================================

def create_pvq21_pages(c):
    """Le PVQ-21 : 21 descriptions avec échelle 1-6."""
    layout = PageLayout(
        c,
        "Le Questionnaire PVQ-21",
        config=LayoutConfig(part_title="1. VALEURS DE SCHWARTZ"),
    )

    # Consigne
    layout.add_text(
        "Consigne : Pour chaque courte description ci-dessous, demandez-vous : "
        "\"Dans quelle mesure cette personne me ressemble-t-elle ?\" "
        "et attribuez une note sur l'échelle suivante :",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    # Échelle de référence
    scale_labels = [
        "1 = Pas du tout comme moi",
        "2 = Pas comme moi",
        "3 = Un peu comme moi",
        "4 = Plutôt comme moi",
        "5 = Comme moi",
        "6 = Tout à fait comme moi",
    ]

    # Draw scale in 2 columns for compactness
    col_width = (layout.target_width - 0.5 * cm) / 2
    scale_y = layout.y_cursor
    for i, label in enumerate(scale_labels):
        col = i % 2
        row = i // 2
        x = layout.text_x if col == 0 else layout.text_x + col_width + 0.5 * cm
        y = scale_y - row * 0.45 * cm
        c.setFont(PDFStyle.FONT_ITALIC, 9)
        c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
        c.drawString(x, y, label)

    layout.y_cursor = scale_y - 3 * 0.45 * cm - 0.6 * cm

    # Prepare items as (field_id, text)
    items = [(item_id, text) for item_id, text, _value in PVQ21_ITEMS]

    _draw_likert_items(layout, items, show_number=True, start_number=1)

    layout.render()


# =============================================================================
# PAGES 6-7 : Questions de Validation
# =============================================================================

def create_validation_pages(c):
    """Questions de validation : Désirabilité Sociale, Faking Bad, Infréquence."""
    layout = PageLayout(
        c,
        "Questions de Validation",
        config=LayoutConfig(part_title="1. VALEURS DE SCHWARTZ"),
    )

    layout.add_text(
        "Ces questions permettent de vérifier la fiabilité de vos réponses. "
        "Répondez avec la même échelle de 1 (Pas du tout comme moi) à 6 (Tout à fait comme moi).",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    # --- Section A : Désirabilité Sociale ---
    layout.add_text(
        "A. Perception de soi",
        config=TextConfig(
            style_choice="subtitle",
            color=PDFStyle.COLOR_ACCENT_BLUE,
            font_size=11,
            spacing_after=0.3 * cm,
        ),
    )

    _draw_likert_items(layout, VALIDATION_ITEMS_FAKING_GOOD, show_number=True, start_number=1)

    # --- Section B : Dévalorisation ---
    layout.add_text(
        "B. Auto-évaluation",
        config=TextConfig(
            style_choice="subtitle",
            color=PDFStyle.COLOR_ACCENT_RED,
            font_size=11,
            spacing_after=0.3 * cm,
        ),
    )

    _draw_likert_items(layout, VALIDATION_ITEMS_FAKING_BAD, show_number=True, start_number=5)

    # --- Section C : Attention ---
    layout.add_text(
        "C. Vérification",
        config=TextConfig(
            style_choice="subtitle",
            color=PDFStyle.COLOR_ACCENT_BLUE,
            font_size=11,
            spacing_after=0.3 * cm,
        ),
    )

    _draw_likert_items(layout, VALIDATION_ITEMS_INFREQUENCY, show_number=True, start_number=9)

    # Note sur la tendance centrale
    layout.add_text(
        "Note pour le consultant : La Tendance Centrale se mesure en comptant le nombre "
        "de réponses \"3\" ou \"4\" sur l'ensemble du test. Si plus de 70% des réponses sont "
        "au centre, le profil indique un évitement ou une indécision systématique.",
        config=TextConfig(
            style_choice="italic",
            font_size=8,
            color=PDFStyle.COLOR_TEXT_SECONDARY,
            spacing_after=0.3 * cm,
        ),
    )

    layout.render()


# =============================================================================
# PAGES 8-9 : Traits de Personnalité Professionnels
# =============================================================================

def create_personality_pages(c):
    """Traits de personnalité professionnels : 6 dimensions × 2 items."""
    layout = PageLayout(
        c,
        "Traits de Personnalité Professionnels",
        config=LayoutConfig(part_title="1. VALEURS DE SCHWARTZ"),
    )

    layout.add_text(
        "Ces questions évaluent vos comportements naturels au travail. "
        "Elles permettent de nuancer vos valeurs (ce que vous voulez) par votre personnalité "
        "(ce que vous faites naturellement). Même échelle de 1 à 6.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    item_number = 11  # Continuing from validation items (1-10)

    for dim in PERSONALITY_DIMENSIONS:
        # Check if we need a page break (enough room for dimension header + 2 items)
        if layout.y_cursor < 6.0 * cm:
            layout.render()
            layout = PageLayout(
                c,
                "Traits de Personnalité (suite)",
                config=LayoutConfig(part_title="1. VALEURS DE SCHWARTZ"),
            )

        # Dimension header
        layout.add_text(
            dim["name"],
            config=TextConfig(
                style_choice="subtitle",
                color=PDFStyle.COLOR_ACCENT_BLUE,
                font_size=11,
                spacing_after=0.2 * cm,
            ),
        )

        items = [(field_id, text) for field_id, text, _reversed in dim["items"]]
        _draw_likert_items(layout, items, show_number=True, start_number=item_number)
        item_number += len(dim["items"])

    layout.render()
