"""
Planche de démonstration de la DA « Éditorial & Affirmé » : les éléments de base, puis
chaque gabarit dans des conditions réelles (carnet 4, « Mon rapport à l'argent »).
Génère 'Test_All_Templates.pdf' à la racine du dépôt.
"""

import os
import sys

# Ensure Scripts directory is in python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from workbook_generator import (
    DocumentBuilder,
    PDFStyle,
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    QuestionItem,
    TextConfig,
    create_cover_page,
    create_standard_summary_page,
    create_standard_engagement_page,
    create_standard_meteo_page,
    create_standard_quadrants_page,
    create_standard_two_columns_page,
    create_standard_enquete_page,
    create_standard_roadmap_page,
    create_closing_page,
    draw_annotation,
    draw_card_title,
    draw_drawn_arrow,
    draw_eyebrow,
    draw_field_box,
    draw_folio,
    draw_frise,
    draw_heading,
    draw_icon_badge,
    draw_label_pill,
    draw_logotype,
    draw_number,
    draw_page_head,
    draw_paragraph,
    draw_pastel_card,
    draw_signature,
    draw_stamp,
    draw_star_list,
    postit,
)
from workbook_generator.primitives import content_frame, draw_filled_arrow

WIDTH, HEIGHT = A4


# --- Éléments de la DA ----------------------------------------------------------

def page_elements_1(c):
    x, width = content_frame()
    y = draw_page_head(c, "Les éléments de la *direction artistique.*", eyebrow="Planche de démonstration") - 0.8 * cm

    # Couleurs
    draw_eyebrow(c, x, y, "Couleurs")
    y -= 0.5 * cm
    swatches = [
        ("ink", PDFStyle.COLOR_INK), ("ink-muted", PDFStyle.COLOR_INK_MUTED), ("line-strong", PDFStyle.COLOR_LINE_STRONG),
        ("coral", PDFStyle.COLOR_CORAL), ("coral-strong", PDFStyle.COLOR_CORAL_STRONG), ("blue", PDFStyle.COLOR_BLUE),
    ] + [(name, color) for name, color in PDFStyle.PASTELS.items()]
    size, gap = 1.1 * cm, (width - 6 * 1.1 * cm) / 5
    for i, (name, color) in enumerate(swatches):
        sx = x + (i % 6) * (size + gap)
        sy = y - (i // 6) * (size + 0.75 * cm) - size
        draw_pastel_card(c, sx, sy, size, size, color=color, radius=6)
        if name in PDFStyle.PASTELS:
            c.saveState()
            c.setStrokeColor(PDFStyle.COLOR_LINE)
            c.roundRect(sx, sy, size, size, 6, stroke=1, fill=0)
            c.restoreState()
        draw_eyebrow(c, sx, sy - 0.35 * cm, name, size=6.5, tracking=0.1)
    y -= 2 * (size + 0.75 * cm) + 0.3 * cm

    # Titres
    draw_eyebrow(c, x, y, "Titres : fin en corail, titre de carte en deux temps")
    y -= 0.4 * cm
    y = draw_heading(c, "Prenez de la *marge.*", x, y, width, size=PDFStyle.SIZE_TITLE_PAGE) - 0.3 * cm
    y -= draw_card_title(c, "Moteurs profonds et réalité économique", "pour valider chaque décision", x, y, width * 0.7) + 0.6 * cm

    # Repères
    draw_eyebrow(c, x, y, "Repères en PT Mono : sourcil, étiquettes, gros numéro")
    y -= 0.35 * cm
    w1, h1 = draw_label_pill(c, x, y - 20, "Exercice 2 · 20 min")
    w2, _ = draw_label_pill(c, x + w1 + 10, y - 20, "En séance", variant="solid")
    draw_pastel_card(c, x + w1 + w2 + 20, y - 26, 4.6 * cm, 32, radius=10)
    draw_label_pill(c, x + w1 + w2 + 28, y - 20, "Sur une carte", variant="on_pastel")
    draw_number(c, x + width - 3.2 * cm, y - 40, "04", size=54)
    y -= 2.0 * cm

    # Texte
    draw_eyebrow(c, x, y, "Texte courant en Manrope, annotation en Instrument Serif")
    y -= 0.35 * cm
    h = draw_paragraph(
        c, "Chaque carnet contient un objectif, quatre exercices et un livrable validé en séance avec "
           "la personne qui vous accompagne. Vous le travaillez entre deux séances, à votre rythme.",
        x, y, width * 0.58,
    )
    draw_annotation(c, x + width * 0.66, y - 4, "Entre deux séances, le bilan continue.", width * 0.32)
    draw_drawn_arrow(c, x + width * 0.6, y - h + 4, width=34, flip=True)
    y -= h + 0.8 * cm

    # Zone à remplir
    draw_eyebrow(c, x, y, "Zone à remplir : blanc, bordure line-strong")
    y -= 0.35 * cm
    draw_field_box(c, x, y - 1.6 * cm, width, 1.6 * cm)
    draw_folio(c)
    c.showPage()


def page_elements_2(c):
    x, width = content_frame()
    y = draw_page_head(c, "Les touches *faites main.*", eyebrow="Planche de démonstration") - 0.8 * cm

    # Post-it et tampon
    draw_eyebrow(c, x, y, "Post-it, ruban washi et tampon")
    y -= 0.6 * cm
    with postit(c, x + 0.3 * cm, y - 3.6 * cm, 7.2 * cm, 3.4 * cm, angle=-2):
        draw_paragraph(c, "De la réflexion à une décision concrète.", 0.6 * cm, 3.4 * cm - 0.7 * cm, 6.0 * cm,
                       PDFStyle.FONT_SERIF, PDFStyle.SIZE_POSTIT, PDFStyle.COLOR_INK, PDFStyle.SIZE_POSTIT * 1.3)
        draw_stamp(c, 2.4 * cm, 0.75 * cm)

    # Liste à étoiles
    list_x = x + 8.6 * cm
    draw_eyebrow(c, list_x, y + 0.2 * cm, "Exercices & protocoles")
    draw_star_list(c, ["Les 8 archétypes financiers", "Cadrage des 4 seuils financiers",
                       "Délai de trésorerie tolérable"], list_x, y - 0.1 * cm, width - 8.6 * cm)
    y -= 4.6 * cm

    # Icônes
    draw_eyebrow(c, x, y, "Icônes Material Symbols dans leurs pastilles")
    y -= 1.0 * cm
    icons = ["menu_book", "auto_awesome", "fact_check", "route", "shield", "query_stats", "forum", "lock"]
    for i, icon in enumerate(icons):
        draw_icon_badge(c, x + 0.55 * cm + i * 1.6 * cm, y, icon, diameter=1.1 * cm)
    draw_filled_arrow(c, x + width - 0.8 * cm, y - 4, width=16)
    y -= 1.5 * cm

    # Frise
    draw_eyebrow(c, x, y, "Frise")
    y -= 1.4 * cm
    y -= draw_frise(
        c, x, y, width,
        [("menu_book", "Sept carnets de bord", "Vous les gardez"),
         ("fact_check", "Un livrable par carnet", "Validé en séance"),
         ("route", "Un plan d'action", "À 30, 60 et 90 jours")],
        start_label="Après la séance", end_label="Avant la suivante",
    ) + 1.0 * cm

    # Marque
    draw_eyebrow(c, x, y, "Logotype et signature")
    y -= 1.0 * cm
    draw_logotype(c, x, y, size=18)
    draw_signature(c, x + width, y - 0.6 * cm, size=30, align="right")
    draw_folio(c)
    c.showPage()


# --- Gabarits --------------------------------------------------------------------

def page_cover(c):
    create_cover_page(
        c, "Mon rapport *à l'argent.*", number=4, tagline="Bilan de compétences",
        promise="Le budget ne doit pas décider à votre place.",
    )


def page_opener(c):
    create_standard_summary_page(
        c, "4", "Mon rapport *à l'argent.*",
        "Poser sans détour les chiffres de votre sécurité financière pour bâtir une trajectoire viable.",
        [("1.", "Les 8 archétypes financiers"), ("2.", "Déconstruction de l'illégitimité tarifaire"),
         ("3.", "Cadrage des 4 seuils financiers"), ("4.", "Délai de trésorerie tolérable")],
        duration="2 h", split="En deux fois : exercices 1 et 2, puis 3 et 4.",
    )


def page_weather_recap(c):
    layout = PageLayout(c, "Avant de *commencer.*", config=LayoutConfig(part_title="Récapitulatif · 10 min"))
    layout.add_energy_check("demo_meteo")
    layout.add_questions_group([
        QuestionItem(question="Le profil de fonctionnement que vous avez validé en séance :",
                     form_field_id="demo_recap_profil"),
        QuestionItem(question="Ce que la séance a confirmé, ce qu'elle a déplacé :", form_field_id="demo_recap_seance"),
    ], max_box_height=3.0 * cm)
    layout.render()


def page_reports(c):
    layout = PageLayout(c, "Ce que vous *savez déjà.*", config=LayoutConfig(part_title="Exercice 2 · Cartographie · 20 min"))
    layout.add_text("Une donnée, une saisie : reportez ce que vous avez écrit dans les carnets précédents, "
                    "sans le réécrire.", config=TextConfig(spacing_after=0.5 * cm))
    layout.add_report([
        ("Le profil de fonctionnement que vous avez validé", "carnet 4 · p. 3", "demo_report_profil", None),
        ("Vos quatre seuils", "carnet 4 · p. 12", "demo_report_seuils", 1.6),
        ("Vos trois valeurs et leur condition observable", "carnet 5 · p. 14", "demo_report_valeurs", 2.2),
        ("Vos quatre zones", "carnet 2", "demo_report_zones", 1.6),
    ])
    layout.render()


def page_heavy_exercise(c):
    layout = PageLayout(c, "Votre histoire *avec l'argent.*",
                        config=LayoutConfig(part_title="Exercice 3 · Histoire · 25 min"))
    layout.add_protocol("Cet exercice revient sur l'argent dans votre famille, et sur ce qu'il en reste aujourd'hui.")
    layout.add_contrast_example(
        "Chez nous, on ne parlait pas d'argent.",
        "Chez nous, on ne parlait pas d'argent : je n'ai jamais négocié un salaire, et je découvre "
        "les grilles de mon secteur à 40 ans.",
        title="Libraire",
    )
    layout.add_question_block("Ce que l'on disait de l'argent chez vous, et ce que vous en avez gardé :",
                              "demo_histoire", config=QuestionConfig(box_height=4.0 * cm))
    layout.add_anchor("demo_ancrage")
    layout.render()


def page_questions(c):
    layout = PageLayout(c, "Vos seuils de *sécurité.*", config=LayoutConfig(part_title="Exercice 3 · 25 min"))
    layout.add_text(
        "Notez vos chiffres sans les arrondir. Ils serviront à trier les pistes pendant la phase d'exploration.",
        config=TextConfig(spacing_after=0.5 * cm),
    )
    layout.add_callout("Comptez vos dépenses fixes sur les douze derniers mois, pas sur un mois type.", variant="tip")
    layout.add_questions_group([
        QuestionItem(
            question="1. Quel est votre salaire vital, en dessous duquel vous ne pouvez pas descendre ?",
            form_field_id="demo_q_vital",
            subtitle="Loyer ou crédit, charges fixes, alimentation, transports.",
            example="2 100 € nets par mois",
        ),
        QuestionItem(
            question="2. Et votre salaire de confort, celui qui vous laisse respirer ?",
            form_field_id="demo_q_confort",
        ),
    ])
    layout.render()


def page_composite_1(c):
    layout = PageLayout(c, "Où en est *votre projet ?*", config=LayoutConfig(part_title="Exercice 4 · 15 min"))
    layout.add_cards_grid([
        {"title": "La zone de friction", "subtitle": "Quelle dépense vous inquiète le plus ?", "field_id": "demo_friction"},
        {"title": "Le levier décisif", "subtitle": "Quelle décision changerait la donne ?", "field_id": "demo_levier"},
    ])
    layout.add_scale_gauge("Votre confiance dans votre budget de transition", 0, 10, "Aucune", "Totale",
                           field_id="demo_confiance")
    layout.add_callout("Un budget clair rend les arbitrages moins lourds, pas plus.", variant="quote")
    layout.render()


def page_composite_2(c):
    layout = PageLayout(c, "Vos repères *chiffrés.*", config=LayoutConfig(part_title="Exercice 4 · suite"))
    layout.add_stat_boxes([
        {"value": "2 100 €", "label": "Salaire vital"},
        {"value": "6 mois", "label": "Trésorerie tolérable"},
        {"value": "3", "label": "Pistes à comparer"},
    ])
    layout.add_table(
        ["Critère", "À vérifier", "Ce que je décide"],
        [["Revenus de la transition", "", {"field_id": "demo_t1"}],
         ["Charges incompressibles", "", {"field_id": "demo_t2"}],
         ["Rythme de vie visé", "", {"field_id": "demo_t3"}]],
        field_prefix="demo_tbl",
    )
    layout.add_checklist(
        ["Budget de transition chiffré", "Seuil de sécurité validé", "Arbitrages posés par écrit", "Délai de trésorerie fixé"],
        title="Avant la prochaine séance", columns=2, field_prefix="demo_chk",
    )
    layout.render()


def page_reading(c):
    layout = PageLayout(c, "Une page *de lecture.*", config=LayoutConfig(part_title="À lire"))
    layout.add_paragraphs([
        "Les pages de lecture enchaînent intertitres, paragraphes et listes à puces étoile.",
        "• Une puce étoile par idée.",
        "• Un item ne se coupe jamais entre deux pages.",
    ])
    layout.add_heading("Un intertitre")
    layout.add_frise(
        [("history", "Prendre du recul", "Choix passés"), ("psychology", "Explorer", "Forces, envies"),
         ("travel_explore", "Le terrain", "Métiers"), ("flag", "Décider", "Plan d'action")],
        start_label="Aujourd'hui", end_label="Fin du bilan",
    )
    layout.add_info_cards([
        {"title": "Le sécuritaire", "subtitle": "l'argent comme protection",
         "text": "L'argent sert d'abord à se sentir à l'abri.", "note": "Question clé : de quelle sécurité ai-je besoin ?",
         "field_id": "demo_info_1"},
        {"title": "L'indépendant", "subtitle": "l'argent comme liberté",
         "text": "L'argent permet de choisir et de ne pas dépendre.", "note": "Question clé : comment rester libre ?",
         "field_id": "demo_info_2"},
    ], check_label="Me correspond")
    layout.add_annotation("Une seule touche faite main par page.")
    layout.render()


def page_form_blocks(c):
    layout = PageLayout(c, "Des blocs *de formulaire.*", config=LayoutConfig(part_title="Formulaires"))
    layout.add_fields_card([
        [("Titre du poste et entreprise", "demo_fc_titre", None, 3), ("Année(s)", "demo_fc_annee", None, 1)],
        [("Ce que j'ai aimé", "demo_fc_aime", 1.6), ("Ce que je n'ai pas aimé", "demo_fc_paime", 1.6)],
    ], title="Expérience 1")
    layout.add_rating_grid(["Argent, finances", "Santé, énergie", "Travail, carrière"], "demo_rating",
                           min_label="1 · Très peu satisfait·e", max_label="10 · Pleinement satisfait·e")
    layout.add_numbered_lines([("3 métiers « no limit »", "demo_nl"), ("3 métiers réalistes", "demo_r")], count=3)
    layout.add_checklist_cards([("Liberté", ["Autonomie", "Choix", "Initiative"]),
                                ("Sécurité", ["Stabilité", "Cadre clair", "Sérénité"]),
                                ("Réussite", ["Progression", "Impact", "Fierté"])], columns=3, field_prefix="demo_cc")
    layout.add_link_card("Des ressources", [("ONISEP", "https://www.onisep.fr/decouvrir-les-metiers",
                                             "les formations, les secteurs et les débouchés.")])
    layout.render()


def page_drawn_blocks(c):
    layout = PageLayout(c, "Des blocs *dessinés.*", config=LayoutConfig(part_title="Illustrations"))
    layout.add_fill_in_card([["Moi,", ("demo_fill_nom", None, "Prénom Nom")],
                             ["je décide d'investir", ("demo_fill_heures", 1.6, "Nombre d'heures"),
                              "heures par semaine dans mon bilan."]])
    layout.add_life_line([("Sommet 1", "summit"), ("Vallée 1", "valley"), ("Sommet 2", "summit")],
                         headers=["Les sommets · moments forts", "Les vallées · apprentissages"],
                         field_prefix="demo_vie")
    layout.render()


def page_tree_of_life(c):
    layout = PageLayout(c, "Un arbre *de vie.*", config=LayoutConfig(part_title="Illustrations"))
    layout.add_tree_of_life([
        ("1. Racines", "Votre histoire, vos origines", "demo_arbre_racines"),
        ("2. Sol", "Vos besoins actuels", "demo_arbre_sol"),
        ("3. Tronc", "Vos compétences et vos valeurs", "demo_arbre_tronc"),
        ("4. Branches", "Vos projets et vos envies", "demo_arbre_branches"),
        ("5. Feuilles", "Vos soutiens, votre entourage", "demo_arbre_feuilles"),
        ("6. Fruits", "Vos réussites, ce que vous avez reçu", "demo_arbre_fruits"),
    ], annotation="Les épreuves font partie de l'arbre, sans le résumer.")
    layout.render()


def page_meteo(c):
    create_standard_meteo_page(c, title="Votre météo *du jour.*", part_title="Ouverture de séance",
                               field_prefix="demo_meteo")


def page_quadrants(c):
    create_standard_quadrants_page(
        c, title="Votre équilibre *à 360°.*", part_title="Exercice 5",
        instruction="Pour chaque domaine, écrivez en une phrase ce que votre projet doit préserver.",
        quadrants_data=[
            ("Revenus", "Salaire, épargne, sécurité", "demo_quad_revenus"),
            ("Rythme de vie", "Horaires, trajets, télétravail", "demo_quad_rythme"),
            ("Entourage", "Famille, alliés, réseau", "demo_quad_entourage"),
            ("Cadre de travail", "Autonomie, management", "demo_quad_cadre"),
        ],
        field_prefix="demo_quad",
    )


def page_two_columns(c):
    create_standard_two_columns_page(
        c, title="Du frein *au levier.*", part_title="Exercice 6",
        intro_text="Pour chaque situation, notez ce que vous en tirez pour la suite de votre projet.",
        col1_header="Ce qui vous freine aujourd'hui", col2_header="Ce que vous pouvez en faire",
        rows_data=[
            ("1. Parler d'argent en entretien", "Ce qui vous retient", "Ce que vous allez dire"),
            ("2. Fixer un tarif", "Ce qui vous fait hésiter", "Le prix que vous retenez"),
            ("3. Poser vos limites", "La situation", "La règle que vous vous donnez"),
        ],
        field_prefix="demo_twocol",
    )


def page_enquete(c):
    create_standard_enquete_page(c, part_title="Exploration du terrain", field_prefix="demo_enquete")


def page_roadmap(c):
    create_standard_roadmap_page(c, field_prefix="demo_roadmap")


def page_livrable(c):
    create_standard_engagement_page(
        c, part_title="Fin de carnet", title="Votre *livrable.*",
        livrable_title="Matrice budgétaire non négociable",
        livrable_text="Le chiffrage précis de votre salaire vital et sécurisant, pour arbitrer les opportunités.",
        custom_lines=[
            "Tenir mon budget de transition chaque semaine.",
            "Relire mes seuils avant chaque entretien.",
            "Préparer deux questions sur la rémunération pour la prochaine séance.",
        ],
        field_prefix="demo_livrable",
        pistes=True,
    )


def build_test_suite_pdf(output_filename="Test_All_Templates.pdf"):
    builder = DocumentBuilder(output_path=output_filename, carnet=4)
    builder.set_title("Planche de démonstration - DA Éditorial & Affirmé")

    for page in (page_elements_1, page_elements_2, page_cover, page_opener, page_weather_recap, page_questions,
                 page_heavy_exercise, page_reports,
                 page_composite_1, page_composite_2, page_reading, page_form_blocks, page_drawn_blocks,
                 page_tree_of_life, page_meteo, page_quadrants,
                 page_two_columns,
                 page_enquete, page_roadmap, page_livrable, create_closing_page):
        builder.add_page(page)

    builder.save()


if __name__ == "__main__":
    output_pdf = os.path.join(os.path.dirname(CURRENT_DIR), "Test_All_Templates.pdf")
    build_test_suite_pdf(output_filename=output_pdf)
