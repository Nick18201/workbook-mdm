from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from workbook_generator.components import create_standard_two_columns_page, draw_answer_box
from workbook_generator.config import PDFStyle
from workbook_generator.document_builder import document_pastel
from workbook_generator.primitives import (
    draw_annotation,
    draw_disc,
    draw_eyebrow,
    draw_icon_badge,
    draw_paragraph,
    draw_pastel_card,
    draw_rule,
    pastel_cycle,
)
from workbook_generator.templates import PageLayout, LayoutConfig, QuestionConfig

WIDTH, HEIGHT = A4


def create_analysis_parcours_pages(c):
    """Exercises 2 and 3: four experience sheets (two per page), then the common thread and drivers."""
    layout = PageLayout(c, "Analyse *du parcours.*", config=LayoutConfig(part_title="Exercice 2 · Analyse du parcours"))
    layout.add_paragraphs([
        "Détaillez chaque expérience significative (emploi, stage, bénévolat). Cet inventaire sert de socle pour "
        "repérer vos réussites et ce que vous voulez retrouver, ou éviter, à l’avenir.",
    ], spacing_after=0.45 * cm)
    pastels = pastel_cycle(c)
    for i in range(1, 5):
        if i == 3:
            layout.page_break()
        layout.add_fields_card(
            [
                [("Titre du poste et entreprise (ou sujet d'étude)", f"exp_{i}_titre", None, 3),
                 ("Année(s)", f"exp_{i}_annee", None, 1)],
                [("Fiche de poste, missions principales", f"exp_{i}_missions", 1.9),
                 ("Compétences développées (techniques, relationnelles)", f"exp_{i}_competences", 1.9)],
                [("Ce que j'ai aimé", f"exp_{i}_aime", 1.9), ("Ce que je n'ai pas aimé", f"exp_{i}_paime", 1.9)],
            ],
            title=f"Expérience {i}",
            color=pastels[(i - 1) % 2],
        )
    layout.render()

    layout = PageLayout(c, "Votre fil *rouge.*", config=LayoutConfig(part_title="Exercice 3 · Fil rouge et moteurs"))
    layout.add_paragraphs([
        "Vous avez passé vos expériences en revue : prenez de la hauteur. L’objectif est de dépasser la "
        "chronologie pour comprendre votre logique, votre fil rouge.",
    ], spacing_after=0.45 * cm)
    layout.add_heading("1. Vos schémas")
    layout.add_question_block(
        "En regardant votre parcours, quelles répétitions ou quels schémas observez-vous ?",
        "bilan_schemas",
        config=QuestionConfig(box_height=4.0 * cm,
                              example="Choisir souvent sous la pression, rechercher l’expertise, partir au bout d’un an…"),
    )
    layout.add_heading("2. Vos moteurs fondamentaux")
    layout.add_numbered_lines(
        [("Ce qui vous fait avancer durablement", "moteur",
          "Ex : indépendance, sécurité financière, apprendre, aider, compétition, rôle d’expert…")],
        count=5,
    )
    layout.render()


# --- Life line ------------------------------------------------------------------

_NODES = [
    ("Sommet 1", "summit"), ("Vallée 1", "valley"), ("Sommet 2", "summit"),
    ("Vallée 2", "valley"), ("Sommet 3", "summit"),
]


def create_timeline_page(c):
    """Exercise 4: the life line, high points on the left and low points on the right."""
    layout = PageLayout(c, "Votre ligne *de vie.*", config=LayoutConfig(part_title="Exercice 4 · Ligne de vie"))
    layout.add_paragraphs([
        "Retracez votre parcours, professionnel et personnel. Notez les moments forts (les sommets) et les "
        "moments difficiles (les vallées) : ce qui vous donne de l’énergie, et ce que vous avez appris des épreuves.",
    ], spacing_after=0.35 * cm)

    x, width = layout.text_x, layout.target_width
    center = x + width / 2
    top = layout.y_cursor
    draw_eyebrow(c, x, top - 8, "Les sommets · moments forts", color=PDFStyle.COLOR_BLUE)
    draw_eyebrow(c, x + width, top - 8, "Les vallées · apprentissages", color=PDFStyle.COLOR_CORAL_STRONG,
                 align="right")

    card_w = width / 2 - 0.75 * cm
    pad = 0.35 * cm
    label_h, line_h, box_h = 10, 0.75 * cm, 1.55 * cm
    card_h = 2 * pad + 2 * (label_h + 3) + line_h + 0.25 * cm + box_h
    first_y = top - 0.65 * cm - card_h / 2
    last_y = PDFStyle.CONTENT_BOTTOM + card_h / 2
    step = (first_y - last_y) / (len(_NODES) - 1)

    # The axis: a dotted line from a dot to a triangle, time running downwards
    c.saveState()
    c.setStrokeColor(PDFStyle.COLOR_INK, alpha=0.25)
    c.setLineWidth(1.5)
    c.setDash(3, 3)
    c.line(center, top - 0.55 * cm, center, PDFStyle.CONTENT_BOTTOM + 0.2 * cm)
    c.restoreState()
    draw_disc(c, center, top - 0.55 * cm, 4.5, PDFStyle.COLOR_INK)
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_INK)
    p = c.beginPath()
    p.moveTo(center - 5, PDFStyle.CONTENT_BOTTOM + 0.2 * cm)
    p.lineTo(center + 5, PDFStyle.CONTENT_BOTTOM + 0.2 * cm)
    p.lineTo(center, PDFStyle.CONTENT_BOTTOM - 0.15 * cm)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

    pastels = pastel_cycle(c)
    for i, (label, kind) in enumerate(_NODES, start=1):
        cy = first_y - (i - 1) * step
        summit = kind == "summit"
        card_x = x if summit else center + 0.75 * cm
        color = pastels[1] if summit else pastels[2]
        # Connector, then the badge on the axis ringed with the page color
        draw_rule(c, card_x + card_w if summit else center, center if summit else card_x, cy,
                  color=PDFStyle.COLOR_INK, alpha=0.25, width=1, dash=(2, 2))
        draw_disc(c, center, cy, 14, PDFStyle.COLOR_PAGE)
        draw_icon_badge(c, center, cy, "trending_up" if summit else "trending_down", diameter=22, fill=color,
                        color=PDFStyle.COLOR_INK)

        draw_pastel_card(c, card_x, cy - card_h / 2, card_w, card_h, color=color, radius=12)
        t = cy + card_h / 2 - pad
        draw_eyebrow(c, card_x + pad, t - 7.5, f"{label} · date et événement", size=7.5,
                     tracking=PDFStyle.TRACKING_LABEL, max_width=card_w - 2 * pad)
        t -= label_h + 3
        draw_answer_box(c, card_x + pad, t - line_h, card_w - 2 * pad, line_h, f"timeline_node_{i}_titre",
                        tooltip=f"{label} : date et événement", multiline=False)
        t -= line_h + 0.25 * cm
        draw_eyebrow(c, card_x + pad, t - 7.5, "Ce que j'ai aimé" if summit else "Ce que j'en retiens", size=7.5,
                     tracking=PDFStyle.TRACKING_LABEL, max_width=card_w - 2 * pad)
        t -= label_h + 3
        draw_answer_box(c, card_x + pad, t - box_h, card_w - 2 * pad, box_h, f"timeline_node_{i}_desc",
                        tooltip="Ce que j'ai aimé" if summit else "Ce que j'en retiens")
    layout.render()


def create_skills_transfer_page(c):
    """Exercise 5: from lived experiences to hidden skills."""
    create_standard_two_columns_page(
        c,
        title="Vos compétences *de vie.*",
        part_title="Exercice 5 · Compétences de vie",
        intro_text=(
            "Votre vécu est un capital : vous ne partez pas de zéro. Une expérience vécue (organiser un événement "
            "familial) cache souvent des compétences (planifier, gérer le stress). Ne négligez aucune expérience : "
            "même la gestion du quotidien en développe."
        ),
        col1_header="L'expérience vécue (ex : divorce, voyage, association…)",
        col2_header="La compétence cachée (ex : négociation, logistique…)",
        rows_data=[
            {"label": "1. Vie familiale et personnelle (ex : organisation, aidant, parent…)"},
            {"label": "2. Défis et épreuves (ex : santé, reconversion, chômage…)"},
            {"label": "3. Engagements et loisirs (ex : sport, association, art, bénévolat…)"},
            {"label": "4. Voyages et découvertes (ex : expatriation, année sabbatique…)"},
            {"label": "5. Autre expérience marquante (au choix)"},
        ],
        field_prefix="skill",
    )


# --- Tree of life ------------------------------------------------------------------

def _tree_zone(c, cx, top, width, number_title, hint, field_id, box_h, align="center"):
    """A zone of the tree: its label, a hint and an answer box, centred on cx below top."""
    x = cx - width / 2
    draw_eyebrow(c, cx if align == "center" else x, top - 8, number_title, size=7.5, tracking=PDFStyle.TRACKING_LABEL,
                 color=PDFStyle.COLOR_INK, align=align, max_width=width)
    hint_h = draw_paragraph(c, hint, x, top - 12, width, PDFStyle.FONT_BODY, 8.5, PDFStyle.COLOR_INK_MUTED, 11,
                            align=align)
    box_top = top - 12 - hint_h - 3
    draw_answer_box(c, x, box_top - box_h, width, box_h, field_id, tooltip=f"{number_title} : {hint}")
    return box_top - box_h


def create_tree_of_life_page(c):
    """
    Exercise 6: the tree of life, drawn with the art direction's shapes (discs for the
    foliage, a pill for the trunk, a dotted ground line), each part holding its answer box.
    """
    layout = PageLayout(c, "Votre arbre *de vie.*", config=LayoutConfig(part_title="Exercice 6 · Arbre de vie"))
    layout.add_paragraphs([
        "Relisez votre parcours comme un tout. Renseignez les racines (votre histoire), le sol (vos besoins), le "
        "tronc (vos forces), les branches (vos projets), les feuilles (vos soutiens) et les fruits (vos réussites).",
    ], spacing_after=0.2 * cm)

    x, width = layout.text_x, layout.target_width
    cx = x + width / 2
    top = layout.y_cursor
    bottom = PDFStyle.CONTENT_BOTTOM
    pastels = pastel_cycle(c)

    ground_y = bottom + 3.4 * cm
    trunk_w, trunk_top = 5.4 * cm, ground_y + 5.6 * cm
    crown_r = min(5.2 * cm, (top - trunk_top) / 2 + 1.2 * cm)
    crown_cy = top - crown_r - 0.1 * cm
    side_r = 2.9 * cm

    # Shapes, back to front
    draw_disc(c, x + side_r * 0.95, crown_cy - crown_r * 0.62, side_r, pastels[2])
    draw_disc(c, x + width - side_r * 0.95, crown_cy - crown_r * 0.62, side_r, pastels[3])
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_INK, alpha=0.07)
    # The trunk runs up under the crown so that they join
    c.roundRect(cx - trunk_w / 2, ground_y - 0.2 * cm, trunk_w, crown_cy - ground_y, trunk_w / 2.4, stroke=0, fill=1)
    c.restoreState()
    draw_disc(c, cx, crown_cy, crown_r, document_pastel(c))
    draw_rule(c, x, x + width, ground_y, color=PDFStyle.COLOR_INK, alpha=0.3, width=1.5, dash=(3, 3))
    # Roots: three curves from the trunk down to the roots box
    c.saveState()
    c.setStrokeColor(PDFStyle.COLOR_INK, alpha=0.25)
    c.setLineWidth(1.2)
    c.setLineCap(1)
    for dx in (-1.4 * cm, 0, 1.4 * cm):
        p = c.beginPath()
        p.moveTo(cx + dx * 0.5, ground_y - 0.2 * cm)
        p.curveTo(cx + dx * 0.7, ground_y - 0.6 * cm, cx + dx * 1.3, ground_y - 0.7 * cm, cx + dx * 1.6,
                  ground_y - 1.0 * cm)
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()

    # Zones
    _tree_zone(c, cx, crown_cy + 2.2 * cm, 6.6 * cm, "4. Branches", "Vos projets et vos envies", "arbre_branches",
               2.3 * cm)
    _tree_zone(c, x + side_r * 0.95, crown_cy - crown_r * 0.62 + 1.45 * cm, 4.5 * cm, "5. Feuilles",
               "Vos soutiens, votre entourage", "arbre_feuilles", 1.9 * cm)
    _tree_zone(c, x + width - side_r * 0.95, crown_cy - crown_r * 0.62 + 1.45 * cm, 4.5 * cm, "6. Fruits",
               "Vos réussites, ce que vous avez reçu", "arbre_fruits", 1.9 * cm)
    _tree_zone(c, cx, trunk_top - 0.3 * cm, trunk_w - 0.9 * cm, "3. Tronc", "Vos compétences et vos valeurs",
               "arbre_tronc", trunk_top - ground_y - 1.6 * cm)
    _tree_zone(c, x + 2.3 * cm, ground_y + 2.5 * cm, 4.6 * cm, "2. Sol", "Vos besoins actuels", "arbre_sol",
               1.5 * cm)
    _tree_zone(c, cx, ground_y - 1.15 * cm, 9.0 * cm, "1. Racines", "Votre histoire, vos origines", "arbre_racines",
               1.3 * cm)

    draw_annotation(c, x + width - 4.9 * cm, ground_y + 2.4 * cm,
                    "Les épreuves font partie de l’arbre, sans le résumer.", 4.6 * cm)
    layout.render()
