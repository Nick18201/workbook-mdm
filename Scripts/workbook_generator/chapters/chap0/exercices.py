import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.forms import create_input_field
from workbook_generator.components import draw_pause_badge, draw_dot_grid, create_input_field
from workbook_generator.utils import cached_image_reader
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig


def create_premiere_etape_page(c):
    """
    New Cover Page: Première étape : Faire le point.
    """
    width, height = A4

    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Faint Grid
    draw_dot_grid(c, width, height, color=PDFStyle.COLOR_WHITE, opacity=0.1)

    c.saveState()
    c.setFont(PDFStyle.FONT_BRANDING, 160)
    c.setFillColor(PDFStyle.COLOR_WHITE, alpha=0.12)
    c.drawString(1.5 * cm, height - 9 * cm, "1.")
    c.restoreState()

    start_y = height - 10 * cm
    c.setFont(PDFStyle.FONT_BRANDING, 32)
    c.setFillColor(PDFStyle.COLOR_WHITE)
    c.drawString(2.5 * cm, start_y, "Première étape :")
    c.drawString(2.5 * cm, start_y - 1.2 * cm, "Faire le point")

    badge_y = start_y - 3 * cm
    c.saveState()

    c.setFont(PDFStyle.FONT_BRANDING, 13)
    c.drawString(2 * cm + 1.5 * cm, badge_y, "APPUYER SUR PAUSE")

    draw_pause_badge(c, 2.5 * cm, badge_y)

    c.restoreState()

    text_y = badge_y - 2 * cm

    style_white = ParagraphStyle(
        "NormalWhite",
        fontName=PDFStyle.FONT_BODY,
        fontSize=12,
        leading=16,
        textColor=PDFStyle.COLOR_WHITE,
    )

    text_content = [
        "Il est l'heure de faire le point sur votre situation actuelle ! Le début d'un bilan, c'est le bon moment pour enclencher le bouton PAUSE. Il est difficile de pouvoir réfléchir à ses besoins et à ses envies quand on est ancré•e dans une routine.",
        "Il est également difficile d'avoir accès à ces réflexions dans une vie où l'on est la tête sous l'eau, que ce soit par surcharge de travail, par ennui profond, ou par manque de sens.",
    ]

    for block in text_content:
        p = Paragraph(block, style_white)
        w, h = p.wrap(width - 5 * cm, height)
        p.drawOn(c, 2.5 * cm, text_y - h)
        text_y -= h + 0.8 * cm

    if os.path.exists(PDFStyle.PATH_PLUME_TEXTURE):
        c.saveState()
        c.translate(width - 1 * cm, height - 3 * cm)
        c.rotate(75)
        c.drawImage(
            cached_image_reader(PDFStyle.PATH_PLUME_TEXTURE),
            0,
            0,
            width=5 * cm,
            height=5 * cm,
            mask="auto",
            preserveAspectRatio=True,
            anchor="ne",
        )
        c.restoreState()

        c.saveState()
        c.translate(0, 0)
        c.rotate(10)
        c.drawImage(
            cached_image_reader(PDFStyle.PATH_PLUME_TEXTURE),
            -2 * cm,
            -1 * cm,
            width=7 * cm,
            height=7 * cm,
            mask="auto",
            preserveAspectRatio=True,
        )
        c.restoreState()

    c.showPage()


def create_faire_le_point_pages(c):
    """
    Faire le Point : Ma Situation Actuelle.
    """
    questions_part1 = [
        ("Comment je me sens actuellement ?", "feeling"),
        ("Quel a été le déclencheur de ce bilan ?", "trigger"),
        ("De quoi j’ai besoin en ce moment ?", "needs"),
        (
            "Qu’ai-je fait jusqu’à présent pour remédier à cette situation ?",
            "actions_taken",
        ),
    ]

    questions_part2 = [
        ("Qu’est ce que je n’ai pas encore changé ? Pourquoi ?", "not_changed"),
        (
            "Quels avantages ai-je à garder la situation telle quelle ?",
            "secondary_benefits",
        ),
        ("Quels besoins sont insatisfaits dans ma vie aujourd’hui ?", "unmet_needs"),
        ("Quelles actions concrètes puis-je mettre en place ?", "concrete_actions"),
    ]

    parts = [(questions_part1, "1/2"), (questions_part2, "2/2")]

    for idx_part, (questions, part_label) in enumerate(parts):
        layout = PageLayout(
            c,
            f"Faire le Point : Ma Situation ({part_label})",
            config=LayoutConfig(part_title="1. FAIRE LE POINT"),
        )

        if idx_part == 0:
            layout.add_text(
                "Le début d’un bilan, c’est le bon moment pour enclencher le bouton PAUSE.",
                config=TextConfig(style_choice="italic", spacing_after=0.3 * cm),
            )

        for question, key in questions:
            layout.add_question_block(
                question, f"s1_point_{key}", config=QuestionConfig(box_height=3.5 * cm)
            )

        layout.render()


def create_domaines_de_vie_page(c):
    """
    Les Domaines de Vie.
    """
    layout = PageLayout(
        c, "Les Domaines de Vie", config=LayoutConfig(part_title="1. FAIRE LE POINT")
    )

    style_intro = ParagraphStyle(
        "DomainIntro",
        fontName=PDFStyle.FONT_BODY,
        fontSize=11,
        leading=14,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
        alignment=TA_JUSTIFY,
    )

    intro_txt = (
        "Notre vie est composée de multiples facettes qui interagissent toutes entre elles. "
        "Prendre le temps d'observer son niveau de satisfaction dans chacun de ces domaines "
        "permet d'obtenir une « photographie » de son équilibre actuel.<br/><br/>"
        "<b>Consigne :</b> Pour chacun des domaines ci-dessous, attribuez une note de 1 "
        "(très peu satisfait•e) à 10 (pleinement épanoui•e)."
    )

    p_intro = Paragraph(intro_txt, style_intro)
    w_i, h_i = p_intro.wrap(layout.target_width, layout.height)
    p_intro.drawOn(c, layout.text_x, layout.y_cursor - h_i)

    layout.y_cursor -= h_i + 1.5 * cm

    domains = [
        "1. Argent / Finances",
        "2. Impact / Sens",
        "3. Dév. Personnel / Spiritualité",
        "4. Famille",
        "5. Santé / Énergie",
        "6. Lieu de vie / Environnement",
        "7. Loisirs / Passions",
        "8. Travail / Carrière",
    ]

    form = layout.form
    start_y = layout.y_cursor
    col_width = layout.target_width / 2

    for i, domain in enumerate(domains):
        col = i % 2
        row = i // 2

        x_pos = layout.text_x + (col * col_width)
        y_pos = start_y - (row * 1.5 * cm)

        c.setFont(PDFStyle.FONT_BODY, 11)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(x_pos, y_pos, domain)

        text_w = c.stringWidth(domain, PDFStyle.FONT_BODY, 11)
        dot_start = x_pos + text_w + 0.2 * cm
        dot_end = x_pos + 6.3 * cm

        if dot_end > dot_start:
            c.saveState()
            c.setDash(1, 2)
            c.setStrokeColor(PDFStyle.COLOR_LINE, alpha=0.3)
            c.line(dot_start, y_pos + 0.1 * cm, dot_end, y_pos + 0.1 * cm)
            c.restoreState()

        create_input_field(
            form,
            f"s1_domaine_note_{i+1}",
            pos=(x_pos + 6.5 * cm, y_pos - 0.1 * cm),
            size=(1.5 * cm, 0.6 * cm),
            tooltip="Note /10",
        )

    layout.y_cursor = start_y - (4 * 1.5 * cm) - 1.0 * cm

    style_refl = ParagraphStyle(
        "ReflBody",
        fontName=PDFStyle.FONT_BODY,
        fontSize=11,
        leading=15,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
        alignment=TA_JUSTIFY,
    )

    refl_intro = (
        "<b>Analyse de votre équilibre</b><br/>"
        "Prenez du recul sur vos notes : quels sont les domaines les plus satisfaisants ? "
        "Les moins satisfaisants ? Quel est l'impact de votre travail actuel "
        "(positif comme négatif) sur ces autres aspects de votre vie ?"
    )

    p_refl = Paragraph(refl_intro, style_refl)
    w_r, h_r = p_refl.wrap(layout.target_width, layout.height)
    p_refl.drawOn(c, layout.text_x, layout.y_cursor - h_r)

    area_top = layout.y_cursor - h_r - 0.5 * cm
    area_bottom = 2.5 * cm
    area_height = area_top - area_bottom

    if area_height < 3 * cm:
        area_height = 3 * cm

    create_input_field(
        form,
        "s1_domaine_reflexion",
        pos=(layout.text_x, area_bottom),
        size=(layout.target_width, area_height),
        tooltip="Votre réflexion",
        multiline=True,
    )

    layout.render()


def create_entourage_page(c):
    """
    Mon Entourage.
    """
    layout = PageLayout(
        c, "Mon Entourage", config=LayoutConfig(part_title="1. FAIRE LE POINT")
    )

    intro_txt = (
        "Le projet que vous menez ne se fait pas en vase clos. Votre entourage, "
        "qu'il soit proche ou plus lointain, joue un rôle crucial dans votre "
        "cheminement. Identifier vos alliés et les sources de tensions possibles "
        "est une étape importante pour sécuriser votre parcours."
    )
    layout.add_text(intro_txt, config=TextConfig(spacing_after=0.3 * cm))

    layout.add_question_block(
        "Soutien, conseil en positif",
        "s1_entourage_soutiens",
        config=QuestionConfig(
            box_height=7.5 * cm,
            subtitle="Qui peut vous soutenir ou vous conseiller utilement dans cette démarche ?",
        ),
    )

    layout.add_question_block(
        "Regard négatif ou anxiété des proches",
        "s1_entourage_freins",
        config=QuestionConfig(
            box_height=7.5 * cm,
            subtitle="Qui pourrait exprimer des doutes, des craintes ou un regard critique ?",
        ),
    )

    layout.render()
