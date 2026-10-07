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
    )


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
    )


def build_test_suite_pdf(output_filename="Test_All_Templates.pdf"):
    builder = DocumentBuilder(output_path=output_filename, carnet=4)
    builder.set_title("Planche de démonstration - DA Éditorial & Affirmé")

    for page in (page_elements_1, page_elements_2, page_cover, page_opener, page_questions,
                 page_composite_1, page_composite_2, page_meteo, page_quadrants, page_two_columns,
                 page_enquete, page_roadmap, page_livrable, create_closing_page):
        builder.add_page(page)

    builder.save()


if __name__ == "__main__":
    output_pdf = os.path.join(os.path.dirname(CURRENT_DIR), "Test_All_Templates.pdf")
    build_test_suite_pdf(output_filename=output_pdf)
