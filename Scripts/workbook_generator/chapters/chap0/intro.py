import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

from workbook_generator.config import PDFStyle
from workbook_generator.forms import create_input_field
from workbook_generator.components import (
    TitleStyle,
    create_standard_cover,
    draw_title,
    draw_page_footer,
    draw_branding_logo,
    draw_side_panel,
    draw_page_decorations,
    draw_card,
    draw_page_background,
    create_standard_summary_page,
)
from workbook_generator.utils import cached_ImageReader
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig

def create_cover_page(c):
    create_standard_cover(c, "CHAPITRE 0 : LE PRÉLUDE")




def create_summary_page(c):
    """Page: Au Programme."""
    intro_txt = (
        "On se réoriente, on se forme, on change sa façon d’exercer son métier : "
        "le rapport au travail évolue, et trouver sa place demande du temps.<br/><br/>"
        "La question centrale de votre bilan : "
        "<b>quelle place voulez-vous donner au travail dans votre vie, et sous quelle forme ?</b> "
        "Nous la traiterons ensemble, avec beaucoup d’autres.<br/><br/>"
        "<i>Un espace Notion rassemble aussi des ressources (sites, podcasts, articles), "
        "accessibles à tout moment.</i>"
    )

    steps = [
        ("05. Prendre du recul :", "sur vos choix passés et vos expériences."),
        (
            "13. Explorer votre personnalité :",
            "Vos forces, ce que vous aimez, vos besoins.",
        ),
        (
            "32. Actions concrètes :",
            "découvrir des secteurs et métiers qui me correspondent.",
        ),
        ("43. Plan d'action :", "Réussir votre projet."),
    ]

    create_standard_summary_page(c, "0", "AU PROGRAMME", intro_txt, steps)




def create_editorial_page_card(c):
    """Page: Édito avec carte."""
    width, height = A4

    draw_page_background(c, width, height, use_blobs=True)

    card_x = 3 * cm
    card_y = 3.2 * cm
    card_w = width - 2 * card_x
    card_h = height - 4.8 * cm - card_y

    draw_card(c, card_x, card_y, card_w, card_h)

    draw_branding_logo(c, 1.5 * cm, height - 1.5 * cm, size=13)

    inner_x = card_x + 1.0 * cm
    inner_w = card_w - 2.0 * cm
    title_y = card_y + card_h - 1.5 * cm

    new_y = draw_title(
        c,
        "Le mot d'accueil.",
        pos=(inner_x, title_y),
        available_width=inner_w,
        style=TitleStyle(size=22),
    )

    if os.path.exists(PDFStyle.PATH_GUILLEMETS):
        c.drawImage(
            cached_ImageReader(PDFStyle.PATH_GUILLEMETS),
            card_x + card_w - 4.5 * cm,
            title_y - 0.5 * cm,
            width=2.8 * cm,
            height=2.8 * cm,
            mask="auto",
            preserveAspectRatio=True,
        )
    else:
        c.saveState()
        c.setFont(PDFStyle.FONT_HAND, 65)
        c.setFillColor(PDFStyle.COLOR_ACCENT_YELLOW)
        c.drawRightString(
            card_x + card_w - 1.0 * cm, title_y + 0.2 * cm, "\u201c\u201c"
        )
        c.restoreState()

    text_y = new_y - 0.5 * cm

    style = ParagraphStyle(
        "EditoBody",
        fontName=PDFStyle.FONT_BODY,
        fontSize=11,
        leading=17,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
        alignment=TA_JUSTIFY,
    )

    paragraphs = [
        "Vous commencez un bilan de compétences : vous avez décidé de faire le point sur votre parcours professionnel et de passer à l’action.",
        "Ces carnets vous accompagnent tout au long du bilan. Ils rassemblent vos idées, vos constats et vos décisions. Vous les remplissez entre les séances, et nous les relisons ensemble.",
        "Le bilan alterne questionnaires, exercices pratiques et échanges en séance. Chaque exercice sert de support à nos entretiens. Ajoutez librement les questions ou les pistes qui vous semblent utiles.",
        "Pour travailler, réservez des moments calmes, sans interruption. Notez ce qui vous vient sans vous censurer : le tri se fait en séance.",
    ]

    for para in paragraphs:
        p = Paragraph(para, style)
        pw, ph = p.wrap(inner_w, height)
        if text_y - ph >= card_y + 0.5 * cm:
            p.drawOn(c, inner_x, text_y - ph)
        text_y -= ph + 0.5 * cm

    if os.path.exists(PDFStyle.PATH_PLANTE_BLEUE):
        plant_w = 10 * cm
        plant_h = 12 * cm

        if os.path.exists(PDFStyle.PATH_PLANTE_ROSE_OMBRE):
            c.drawImage(
                cached_ImageReader(PDFStyle.PATH_PLANTE_ROSE_OMBRE),
                width - plant_w + 6.5 * cm + 0.3 * cm,
                height - plant_h + 3 * cm - 0.2 * cm,
                width=plant_w,
                height=plant_h,
                mask="auto",
                preserveAspectRatio=True,
            )

        c.drawImage(
            cached_ImageReader(PDFStyle.PATH_PLANTE_BLEUE),
            width - plant_w + 6.5 * cm,
            height - plant_h + 3 * cm,
            width=plant_w,
            height=plant_h,
            mask="auto",
            preserveAspectRatio=True,
        )

        c.saveState()

        corner_x = -5.5 * cm
        corner_y = -plant_h * 0.3

        if os.path.exists(PDFStyle.PATH_PLANTE_ROSE_OMBRE):
            c.drawImage(
                cached_ImageReader(PDFStyle.PATH_PLANTE_ROSE_OMBRE),
                corner_x + 0.3 * cm,
                corner_y - 0.2 * cm,
                width=plant_w,
                height=plant_h,
                mask="auto",
                preserveAspectRatio=True,
            )

        c.drawImage(
            cached_ImageReader(PDFStyle.PATH_PLANTE_BLEUE),
            corner_x,
            corner_y,
            width=plant_w,
            height=plant_h,
            mask="auto",
            preserveAspectRatio=True,
        )
        c.restoreState()

    draw_page_decorations(c, width, height)
    c.showPage()




def create_intro_sense_page(c):
    """Page: Introduction 'Mettre du sens'."""
    width, height = A4

    draw_page_background(c, width, height, use_blobs=True)

    card_x = 2 * cm
    card_y = 2.1 * cm
    card_w = width - 2 * card_x
    card_h = height - 3 * cm

    draw_card(c, card_x, card_y, card_w, card_h)

    logo_x = card_x + 1 * cm
    logo_y = card_y + card_h - 1 * cm
    draw_branding_logo(c, logo_x, logo_y, size=13)

    text_x = card_x + 1.5 * cm
    text_top = card_y + card_h - 4.5 * cm
    content_width = card_w - 3 * cm

    c.setFont(PDFStyle.FONT_TITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, text_top + 1.2 * cm, "INTRODUCTION")

    PURPLE_TITLE = colors.HexColor("#6C5CE7")
    new_y = draw_title(
        c,
        "Comprendre pour décider.",
        pos=(text_x, text_top),
        available_width=content_width,
        style=TitleStyle(size=28, color=PURPLE_TITLE),
    )

    if os.path.exists(PDFStyle.PATH_STAMP):
        stamp_size = 4 * cm
        c.saveState()
        c.translate(width - stamp_size / 2 - 3 * cm, height - stamp_size / 2 - 1.5 * cm)
        c.rotate(-10)
        c.drawImage(
            cached_ImageReader(PDFStyle.PATH_STAMP),
            -stamp_size / 2,
            -stamp_size / 2,
            width=stamp_size,
            height=stamp_size,
            mask="auto",
            preserveAspectRatio=True,
        )
        c.restoreState()

    text_y = new_y - 0.2 * cm

    paragraphs = [
        "Savoir pourquoi vous faites ce que vous faites, c’est reprendre la main sur vos décisions professionnelles.",
        "La psychologie et la sociologie le montrent : une part de nos choix vient de notre histoire, de notre milieu et des modèles reçus, plus que d’une décision libre. Le bilan vous aide à faire la différence, pour décider en connaissance de cause.",
        "Nous partons d’un principe simple : chacun peut apprendre, s’adapter et changer. Chacun a aussi des facilités naturelles pour certaines tâches.",
        "Votre personnalité se construit tout au long de la vie, et elle vous distingue : aptitudes, points forts, goûts. C’est ce qui rend les rôles complémentaires dans une équipe.",
        "Le lien entre ce que vous êtes et ce que vous faites au quotidien peut pourtant se distendre. Fatigue, perte d’intérêt, tâches qui semblent inutiles, attentes qui changent : les raisons de faire le point sont nombreuses.",
        "Notre objectif : vous aider à construire un projet professionnel réaliste, qui tienne compte de ce que vous êtes, du marché du travail, de votre salaire et de votre rythme de vie.",
        "C’est un objectif ambitieux. Ce carnet en est la première étape.",
    ]

    style = ParagraphStyle(
        "IntroSenseBody",
        fontName=PDFStyle.FONT_BODY,
        fontSize=11.5,
        leading=16,
        textColor=PDFStyle.COLOR_ACCENT_BLUE,
        alignment=TA_JUSTIFY,
    )

    for paragraph in paragraphs:
        p = Paragraph(paragraph, style)
        pw, ph = p.wrap(content_width, height)
        if text_y - ph < card_y + 0.5 * cm:
            break
        p.drawOn(c, text_x, text_y - ph)
        text_y -= ph + 0.5 * cm

    draw_page_footer(c, width, height)
    c.showPage()




def create_form_page_card(c):
    """Page: Mon Engagement (Formulaire)."""
    width, height = A4

    draw_page_background(c, width, height)

    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm

    new_y = draw_title(c, "Mon engagement.", pos=(text_x, text_top))

    form = c.acroForm
    start_y = new_y - 0.5 * cm

    c.setFont(PDFStyle.FONT_BODY, 12)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, start_y, "Moi, ")

    create_input_field(
        form,
        "nom_complet",
        pos=(text_x + 1.5 * cm, start_y - 5),
        size=(8 * cm, 20),
        tooltip="Prénom Nom",
    )

    start_y -= 2 * cm
    c.drawString(text_x, start_y, "décide d'investir")

    create_input_field(
        form,
        "engagement_hebdo",
        pos=(text_x + 3.5 * cm, start_y - 5),
        size=(1.5 * cm, 20),
        tooltip="Nb",
    )

    c.drawString(text_x + 5.5 * cm, start_y, "heures par semaine.")

    start_y -= 1.8 * cm
    c.drawString(text_x, start_y, "Mon objectif principal :")
    start_y -= 0.6 * cm

    box_h = 3.5 * cm
    create_input_field(
        form,
        "objectif_3_mois",
        pos=(text_x, start_y - box_h),
        size=(width - text_x - 1 * cm, box_h),
        tooltip="Objectif",
        multiline=True,
    )

    start_y -= box_h + 1.0 * cm
    c.drawString(text_x, start_y, "Je m'autorise à :")
    start_y -= 0.6 * cm

    create_input_field(
        form,
        "permission_personnelle",
        pos=(text_x, start_y - box_h),
        size=(width - text_x - 1 * cm, box_h),
        tooltip="Permission",
        multiline=True,
    )

    # Hidden Fields
    form.textfield(
        name="meta_doc_type", value="workbook_chap0", x=0, y=-10, width=0, height=0
    )
    form.textfield(
        name="meta_doc_version", value="1.3_da_v4", x=0, y=-10, width=0, height=0
    )

    draw_page_decorations(
        c, width, height, part_title="INTRODUCTION", x_offset=card_margin
    )
    c.showPage()
