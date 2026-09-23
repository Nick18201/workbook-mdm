from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle
from workbook_generator.templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig
from workbook_generator.forms import create_checkbox, create_input_field


CATEGORIES_VALEURS = [
    {
        "title": "Liberté & autonomie",
        "values": ["Autonomie", "Liberté", "Indépendance", "Créativité", "Marge de manœuvre", "Responsabilité", "Choix", "Souplesse", "Authenticité", "Initiative"]
    },
    {
        "title": "Sécurité & stabilité",
        "values": ["Sécurité", "Stabilité", "Prévisibilité", "Cadre clair", "Protection", "Fiabilité", "Continuité", "Sérénité", "Équilibre", "Confort"]
    },
    {
        "title": "Réussite & reconnaissance",
        "values": ["Réussite", "Progression", "Ambition", "Excellence", "Compétence", "Reconnaissance", "Statut", "Légitimité", "Impact", "Fierté"]
    },
    {
        "title": "Relation & bienveillance",
        "values": ["Bienveillance", "Entraide", "Écoute", "Loyauté", "Respect", "Coopération", "Confiance", "Harmonie", "Soutien", "Qualité relationnelle"]
    },
    {
        "title": "Justice & utilité sociale",
        "values": ["Justice", "Équité", "Inclusion", "Égalité", "Utilité sociale", "Sens", "Contribution", "Engagement", "Éthique", "Responsabilité sociale"]
    },
    {
        "title": "Stimulation & apprentissage",
        "values": ["Nouveauté", "Défi", "Apprentissage", "Curiosité", "Exploration", "Variété", "Mouvement", "Intensité", "Expérimentation", "Évolution"]
    },
    {
        "title": "Plaisir & qualité de vie",
        "values": ["Plaisir", "Joie", "Légèreté", "Beauté", "Esthétique", "Confort de vie", "Temps pour soi", "Vitalité", "Spontanéité", "Simplicité"]
    },
    {
        "title": "Cadre, règles & transmission",
        "values": ["Rigueur", "Discipline", "Respect du cadre", "Tradition", "Transmission", "Fiabilité", "Méthode", "Structure", "Engagement", "Sens du devoir"]
    },
    {
        "title": "Influence & pouvoir d'agir",
        "values": ["Influence", "Leadership", "Décision", "Pouvoir d'agir", "Autorité", "Responsabilité", "Pilotage", "Capacité à transformer", "Capacité à orienter", "Maîtrise"]
    }
]


def _draw_valeurs_grid(c, layout, categories_subset, start_index):
    start_x = layout.text_x
    start_y = layout.y_cursor - 0.2 * cm
    form = c.acroForm

    for idx, cat in enumerate(categories_subset):
        col_idx = idx % 2
        row_idx = idx // 2

        x = start_x + col_idx * (8.0 * cm + 1.0 * cm)
        y = start_y - row_idx * (6.2 * cm + 0.8 * cm)

        # Draw a white card with thin border for premium aesthetic
        c.saveState()
        c.setStrokeColor(PDFStyle.COLOR_LINE)
        c.setLineWidth(0.5)
        c.setFillColor(PDFStyle.COLOR_WHITE)
        c.roundRect(x, y - 6.2 * cm, 8.0 * cm, 6.2 * cm, 4, fill=1, stroke=1)
        c.restoreState()

        # Category title
        c.saveState()
        c.setFont(PDFStyle.FONT_SUBTITLE, 9)
        c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
        c.drawString(x + 0.35 * cm, y - 0.5 * cm, cat["title"].upper())
        c.restoreState()

        # Draw 10 values with checkboxes
        for v_idx, val in enumerate(cat["values"]):
            item_y = y - 1.05 * cm - v_idx * 0.5 * cm
            field_name = f"val_chk_{start_index + idx}_{v_idx}"
            
            create_checkbox(
                form,
                field_name,
                pos=(x + 0.35 * cm, item_y),
                size=9,
                tooltip=f"Cocher {val}"
            )
            
            c.saveState()
            c.setFont(PDFStyle.FONT_BODY, 8.5)
            c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            c.drawString(x + 0.75 * cm, item_y + 0.04 * cm, val)
            c.restoreState()

    # Move cursor below cards
    layout.y_cursor = start_y - 3 * (6.2 * cm + 0.8 * cm) + 0.3 * cm


def create_liste_valeurs_page1(c):
    layout = PageLayout(
        c,
        "4. Liste de valeurs pour nommer ce qui compte (1/2)",
        config=LayoutConfig(part_title="4. SÉLECTION & HIÉRARCHISATION")
    )
    layout.add_text(
        "⏱ ~10 min | À partir des situations d'alignement, de désalignement et de vos choix difficiles, cochez les valeurs qui reviennent régulièrement dans votre parcours :",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.4 * cm)
    )
    _draw_valeurs_grid(c, layout, CATEGORIES_VALEURS[0:5], 0)
    layout.render()


def create_liste_valeurs_page2(c):
    layout = PageLayout(
        c,
        "4. Liste de valeurs pour nommer ce qui compte (2/2)",
        config=LayoutConfig(part_title="4. SÉLECTION & HIÉRARCHISATION")
    )
    layout.add_text(
        "Cochez d'autres valeurs régulières dans les catégories ci-dessous :",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.4 * cm)
    )
    _draw_valeurs_grid(c, layout, CATEGORIES_VALEURS[5:9], 5)
    layout.render()


def create_hierarchiser_valeurs_page(c):
    layout = PageLayout(
        c,
        "5. Hiérarchiser mes valeurs",
        config=LayoutConfig(part_title="5. SÉLECTION & HIÉRARCHISATION")
    )
    layout.add_text(
        "⏱ ~10 min | Trier et prioriser vos moteurs pour dégager vos valeurs fondamentales.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3 * cm)
    )
    layout.add_text(
        "Parmi toutes les valeurs cochées à la page précédente, réduisez progressivement votre choix pour extraire les valeurs clés qui guident votre vie professionnelle :",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    layout.add_question_block(
        "1. Mes 10 valeurs importantes :",
        "hierarchie_10_valeurs",
        config=QuestionConfig(box_height=2.2 * cm, subtitle="Notez les 10 valeurs qui résonnent le plus dans votre parcours."),
    )
    layout.add_question_block(
        "2. Mes 5 valeurs prioritaires :",
        "hierarchie_5_valeurs",
        config=QuestionConfig(box_height=2.2 * cm, subtitle="Sélectionnez les 5 valeurs les plus fortes parmi les 10 ci-dessus."),
    )
    layout.add_question_block(
        "3. Mes 3 valeurs non négociables :",
        "hierarchie_3_valeurs",
        config=QuestionConfig(box_height=2.2 * cm, subtitle="Choisissez les 3 valeurs les plus vitales parmi les 5."),
    )
    
    layout.add_text(
        "Une valeur non négociable est une valeur qui, si elle est durablement absente de votre travail, risque d'entraîner une perte de motivation, d'énergie ou de sens.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.2 * cm)
    )

    layout.render()


def _create_incarner_valeur_page(c, num):
    layout = PageLayout(
        c,
        "6. Incarner mes valeurs non négociables ({num}/3)".format(num=num),
        config=LayoutConfig(part_title="6. INCARNATION DES VALEURS")
    )
    layout.add_text(
        "⏱ ~5 min | Traduire chaque valeur clé en ressentis, actions et besoins concrets.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3 * cm)
    )
    
    # Value title box
    layout.add_text(
        f"VALEUR NON NÉGOCIABLE N°{num} :",
        config=TextConfig(style_choice="subtitle", font_size=11, color=PDFStyle.COLOR_ACCENT_RED, spacing_after=0.1 * cm)
    )
    
    # Text input for the name of the value
    create_input_field(
        layout.form,
        f"incarner_val_{num}_name",
        pos=(layout.text_x, layout.y_cursor - 0.9 * cm),
        size=(layout.target_width, 0.9 * cm),
        tooltip=f"Saisissez le nom de la valeur non négociable {num}"
    )
    layout.y_cursor -= 1.4 * cm

    layout.add_question_block(
        "1. Comment cette valeur se manifeste-t-elle concrètement dans mon travail ?",
        f"incarner_val_{num}_q1",
        config=QuestionConfig(box_height=2.5 * cm, color_alternation=False, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    layout.add_question_block(
        "2. Dans quelles situations passées ai-je déjà vécu cette valeur ?",
        f"incarner_val_{num}_q2",
        config=QuestionConfig(box_height=2.5 * cm, color_alternation=False, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    layout.add_question_block(
        "3. Qu'est-ce que je ressens quand cette valeur est respectée / absente ?",
        f"incarner_val_{num}_q3",
        config=QuestionConfig(box_height=2.5 * cm, color_alternation=False, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    layout.add_question_block(
        "4. De quoi ai-je besoin concrètement pour que cette valeur existe dans mon futur travail ?",
        f"incarner_val_{num}_q4",
        config=QuestionConfig(box_height=2.5 * cm, color_alternation=False, color=PDFStyle.COLOR_ACCENT_BLUE),
    )

    layout.render()


def create_incarner_valeur_1_page(c):
    _create_incarner_valeur_page(c, 1)


def create_incarner_valeur_2_page(c):
    _create_incarner_valeur_page(c, 2)


def create_incarner_valeur_3_page(c):
    _create_incarner_valeur_page(c, 3)


def create_conditions_travail_page(c):
    layout = PageLayout(
        c,
        "7. Traduire mes valeurs en conditions de travail",
        config=LayoutConfig(part_title="7. CONDITIONS DE TRAVAIL")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Formuler des critères concrets et observables pour évaluer vos futurs postes.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3 * cm)
    )

    layout.add_question_block(
        "1. Pour respecter mes valeurs, j'ai besoin d'un environnement où...",
        "conditions_positives",
        config=QuestionConfig(
            box_height=5.2 * cm,
            example="je peux organiser mon travail avec autonomie ; les relations sont respectueuses ; les objectifs sont clairs ; je peux apprendre régulièrement ; je me sens utile ; le rythme est soutenable."
        ),
    )
    layout.add_question_block(
        "2. Pour respecter mes valeurs, j'ai besoin d'éviter les environnements où...",
        "conditions_negatives",
        config=QuestionConfig(
            box_height=5.2 * cm,
            example="tout est contrôlé ; les priorités changent sans cesse ; il y a peu de reconnaissance ; les relations sont froides ou compétitives ; la pression est permanente ; il n'y a pas d'évolution."
        ),
    )

    layout.render()
