from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from workbook_generator.config import PDFStyle
from workbook_generator.components import (
    create_standard_cover,
    create_standard_summary_page,
)
from workbook_generator.templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig
from workbook_generator.forms import create_checkbox, create_input_field

# =============================================================================
# COUVERTURE & CONCEPT
# =============================================================================

def create_valeurs_cover(c):
    create_standard_cover(c, "CHAPITRE 5 : MES VALEURS ET MOTEURS PROFONDS")


def create_concept_page(c):
    points = [
        ("Sommaire :", ""),
        ("1.", "Mes Expériences d'Alignement"),
        ("2.", "Mes Expériences de Désalignement"),
        ("3.", "Mes Choix Difficiles"),
        ("4.", "Liste de Valeurs pour s'aider à nommer"),
        ("5.", "Hiérarchiser mes Valeurs"),
        ("6.", "Incarner ses Valeurs Non Négociables"),
        ("7.", "Traduire ses Valeurs en Conditions de Travail"),
        ("8.", "Mes Tensions de Valeurs"),
        ("9.", "Synthèse Finale"),
    ]
    create_standard_summary_page(c, "5", "VALEURS", "", points)


def create_intro_page(c):
    layout = PageLayout(
        c,
        "Comprendre ses valeurs",
        config=LayoutConfig(part_title="INTRODUCTION")
    )
    
    layout.add_text(
        "Ce workbook vous aide à identifier ce qui compte profondément pour vous dans votre vie professionnelle.",
        config=TextConfig(font_size=12, spacing_after=0.6 * cm, style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE)
    )
    
    layout.add_text(
        "Les valeurs ne sont pas seulement des idées abstraites. Elles se repèrent dans les situations où vous vous sentez :",
        config=TextConfig(font_size=11, spacing_after=0.4 * cm)
    )
    
    sentiments = [
        "• motivé(e) ;",
        "• fier(e) ;",
        "• utile ;",
        "• libre ;",
        "• reconnu(e) ;",
        "• en confiance ;"
    ]
    for s in sentiments:
        layout.add_text(
            s,
            config=TextConfig(font_size=11, spacing_after=0.2 * cm, color=PDFStyle.COLOR_ACCENT_RED, style_choice="subtitle")
        )
        
    layout.add_text(
        "mais aussi frustré(e), en colère, vidé(e), empêché(e) ou en conflit intérieur.",
        config=TextConfig(font_size=11, spacing_after=0.6 * cm)
    )
    
    layout.add_text(
        "L’objectif n’est pas de choisir les valeurs qui semblent les plus “belles” ou les plus attendues, mais d’identifier celles qui influencent réellement vos choix, votre énergie et votre rapport au travail.",
        config=TextConfig(font_size=11, spacing_after=0.5 * cm, style_choice="italic", color=PDFStyle.COLOR_TEXT_SECONDARY)
    )
    
    layout.render()


# =============================================================================
# 1. ALIGNEMENT
# =============================================================================

def create_alignement_pages_part1(c):
    layout = PageLayout(
        c,
        "1. Mes expériences d'alignement (1/2)",
        config=LayoutConfig(part_title="1. ALIGNEMENT")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Identifier les situations professionnelles ou personnelles où vous vous êtes senti(e) à votre place.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text(
        "Repensez à trois situations (professionnelles, scolaires, associatives, personnelles) où vous étiez particulièrement aligné(e). En voici les deux premières :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Situation 1 - Décrivez brièvement le contexte (Quoi ? Qui ? Où ?) :",
        "align_sit1_desc",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Analyse 1 - Qu'est-ce qui vous donnait de l'énergie ? Qu'apportiez-vous ? Quelle valeur était respectée ?",
        "align_sit1_analyse",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Situation 2 - Décrivez brièvement le contexte (Quoi ? Qui ? Où ?) :",
        "align_sit2_desc",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Analyse 2 - Qu'est-ce qui vous donnait de l'énergie ? Qu'apportiez-vous ? Quelle valeur était respectée ?",
        "align_sit2_analyse",
        config=QuestionConfig(box_height=2.3 * cm),
    )

    layout.render()


def create_alignement_pages_part2(c):
    layout = PageLayout(
        c,
        "1. Mes expériences d'alignement (2/2)",
        config=LayoutConfig(part_title="1. ALIGNEMENT")
    )
    layout.add_text(
        "Voici la troisième situation d'alignement ainsi qu'un bilan global de cet exercice :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Situation 3 - Décrivez brièvement le contexte (Quoi ? Qui ? Où ?) :",
        "align_sit3_desc",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Analyse 3 - Qu'est-ce qui vous donnait de l'énergie ? Qu'apportiez-vous ? Quelle valeur était respectée ?",
        "align_sit3_analyse",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Synthèse - Valeurs possibles révélées par ces trois situations :",
        "align_valeurs_revelees",
        config=QuestionConfig(box_height=2.5 * cm),
    )

    layout.render()


# =============================================================================
# 2. DÉSALIGNEMENT
# =============================================================================

def create_desalignement_pages_part1(c):
    layout = PageLayout(
        c,
        "2. Mes expériences de désalignement (1/2)",
        config=LayoutConfig(part_title="2. DÉSALIGNEMENT")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Comprendre quelle valeur importante a été bafouée ou ignorée dans des moments difficiles.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text(
        "Repensez à trois situations où vous vous êtes senti(e) en difficulté, frustré(e), vidé(e) ou en conflit intérieur :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Situation 1 - Décrivez la situation de désalignement ou de perte de sens :",
        "desalign_sit1_desc",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Analyse 1 - Qu'est-ce qui vous a dérangé ? Quelle limite a été franchie ? Quelle valeur était absente ou bafouée ?",
        "desalign_sit1_analyse",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Situation 2 - Décrivez la situation de désalignement ou de perte de sens :",
        "desalign_sit2_desc",
        config=QuestionConfig(box_height=2.3 * cm),
    )
    layout.add_question_block(
        "Analyse 2 - Qu'est-ce qui vous a dérangé ? Quelle limite a été franchie ? Quelle valeur était absente ou bafouée ?",
        "desalign_sit2_analyse",
        config=QuestionConfig(box_height=2.3 * cm),
    )

    layout.render()


def create_desalignement_pages_part2(c):
    layout = PageLayout(
        c,
        "2. Mes expériences de désalignement (2/2)",
        config=LayoutConfig(part_title="2. DÉSALIGNEMENT")
    )
    layout.add_text(
        "Voici la troisième situation de désalignement ainsi qu'un bilan global :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Situation 3 - Décrivez la situation de désalignement ou de perte de sens :",
        "desalign_sit3_desc",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Analyse 3 - Qu'est-ce qui vous a dérangé ? Quelle limite a été franchie ? Quelle valeur était absente ou bafouée ?",
        "desalign_sit3_analyse",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Synthèse - Valeurs absentes, empêchées ou bafouées révélées :",
        "desalign_valeurs_revelees",
        config=QuestionConfig(box_height=2.5 * cm),
    )

    layout.render()


# =============================================================================
# 3. CHOIX DIFFICILES
# =============================================================================

def create_choix_difficiles_page1(c):
    layout = PageLayout(
        c,
        "3. Mes choix difficiles (1/2)",
        config=LayoutConfig(part_title="3. CHOIX DIFFICILES")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Révéler vos priorités profondes à travers des arbitrages complexes.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text(
        "Les valeurs apparaissent dans les choix difficiles car choisir implique de renoncer. Repensez à deux situations de choix complexes (ex: rester/partir, sécurité/risque, etc.) :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Choix difficile 1 - Quelle était la situation ?",
        "choix1_desc",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Options - Qu'est-ce que l'Option A et l'Option B permettaient chacune de préserver ?",
        "choix1_options",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Résolution - Qu'avez-vous choisi ? Qu'est-ce que cela a coûté et permis de respecter ?",
        "choix1_resolution",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Valeurs - Quelles valeurs étaient en conflit ?",
        "choix1_valeurs",
        config=QuestionConfig(box_height=1.5 * cm),
    )

    layout.render()


def create_choix_difficiles_page2(c):
    layout = PageLayout(
        c,
        "3. Mes choix difficiles (2/2)",
        config=LayoutConfig(part_title="3. CHOIX DIFFICILES")
    )
    layout.add_text(
        "Voici le second arbitrage complexe de votre parcours professionnel ou personnel :",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Choix difficile 2 - Quelle était la situation ?",
        "choix2_desc",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Options - Qu'est-ce que l'Option A et l'Option B permettaient chacune de préserver ?",
        "choix2_options",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Résolution - Qu'avez-vous choisi ? Qu'est-ce que cela a coûté et permis de respecter ?",
        "choix2_resolution",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Valeurs - Quelles valeurs étaient en conflit ?",
        "choix2_valeurs",
        config=QuestionConfig(box_height=1.5 * cm),
    )

    layout.render()


# =============================================================================
# 4. LISTE & HIÉRARCHISATION DES VALEURS
# =============================================================================

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
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.4*cm)
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
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.4*cm)
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
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
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
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.2*cm)
    )

    layout.render()


# =============================================================================
# 5. INCARNER SES VALEURS & CONDITIONS DE TRAVAIL
# =============================================================================

def _create_incarner_valeur_page(c, num):
    layout = PageLayout(
        c,
        "6. Incarner mes valeurs non négociables ({num}/3)".format(num=num),
        config=LayoutConfig(part_title="6. INCARNATION DES VALEURS")
    )
    layout.add_text(
        "⏱ ~5 min | Traduire chaque valeur clé en ressentis, actions et besoins concrets.",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    
    # Value title box
    layout.add_text(
        f"VALEUR NON NÉGOCIABLE N°{num} :",
        config=TextConfig(style_choice="subtitle", font_size=11, color=PDFStyle.COLOR_ACCENT_RED, spacing_after=0.1*cm)
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
        config=QuestionConfig(box_height=2.2 * cm, color_alternation=False, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    layout.add_question_block(
        "2. Dans quelles situations passées ai-je déjà vécu cette valeur ?",
        f"incarner_val_{num}_q2",
        config=QuestionConfig(box_height=2.2 * cm, color_alternation=False, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    layout.add_question_block(
        "3. Qu'est-ce que je ressens quand cette valeur est respectée / absente ?",
        f"incarner_val_{num}_q3",
        config=QuestionConfig(box_height=2.2 * cm, color_alternation=False, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    layout.add_question_block(
        "4. De quoi ai-je besoin concrètement pour que cette valeur existe dans mon futur travail ?",
        f"incarner_val_{num}_q4",
        config=QuestionConfig(box_height=2.2 * cm, color_alternation=False, color=PDFStyle.COLOR_ACCENT_BLUE),
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
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )

    layout.add_question_block(
        "1. Pour respecter mes valeurs, j'ai besoin d'un environnement où...",
        "conditions_positives",
        config=QuestionConfig(
            box_height=4.0 * cm,
            example="je peux organiser mon travail avec autonomie ; les relations sont respectueuses ; les objectifs sont clairs ; je peux apprendre régulièrement ; je me sens utile ; le rythme est soutenable."
        ),
    )
    layout.add_question_block(
        "2. Pour respecter mes valeurs, j'ai besoin d'éviter les environnements où...",
        "conditions_negatives",
        config=QuestionConfig(
            box_height=4.0 * cm,
            example="tout est contrôlé ; les priorités changent sans cesse ; il y a peu de reconnaissance ; les relations sont froides ou compétitives ; la pression est permanente ; il n'y a pas d'évolution."
        ),
    )

    layout.render()


# =============================================================================
# 6. TENSIONS DE VALEURS & SYNTHÈSE
# =============================================================================

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
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
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
        config=TextConfig(style_choice="subtitle", font_size=10, color=PDFStyle.COLOR_ACCENT_RED, spacing_after=0.3*cm)
    )

    layout.add_question_block(
        "Tension 1 - Quelles sont les deux valeurs en tension ? Dans quelles situations cela apparaît-il ?",
        "tension1_situations",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Arbitrage - Quelle valeur avez-vous tendance à privilégier ? Laquelle sacrifiez-vous ?",
        "tension1_arbitrage",
        config=QuestionConfig(box_height=2.2 * cm),
    )
    layout.add_question_block(
        "Équilibre - Quel meilleur équilibre ou compromis constructif pourriez-vous rechercher ?",
        "tension1_equilibre",
        config=QuestionConfig(box_height=2.2 * cm),
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
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
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
