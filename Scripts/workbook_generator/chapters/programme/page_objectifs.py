from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.components import draw_title, TitleStyle
from .common import (
    setup_workbook_programme_page,
    draw_workbook_highlight_box,
    get_workbook_styles,
)


def create_programme_page_1(c):
    """Page 1 : Cadrage, Objectifs du Bilan & Compétences Visées."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="PROGRAMME DE FORMATION : BILAN DE COMPÉTENCES"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. GRAND TITRE PRINCIPAL DU DOCUMENT & SOUS-TITRE (Charte Workbook)
    # -------------------------------------------------------------------------
    # Tag de sur-titre en rouge bien dégagé
    c.setFont(PDFStyle.FONT_TITLE, 9.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(text_x, y_cursor, "BILAN DE COMPÉTENCES & ALIGNEMENT")
    y_cursor -= 1.45 * cm  # Dégagement aéré pour une parfaite séparation visuelle avec le titre H1

    y_cursor = draw_title(
        c,
        "Programme du Bilan de Compétences",
        pos=(text_x, y_cursor),
        available_width=target_width,
        style=TitleStyle(size=21, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    y_cursor -= 0.35 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Déterminer la place du travail dans votre existence & réaligner vos choix",
    )
    y_cursor -= 0.75 * cm

    # -------------------------------------------------------------------------
    # 2. PARAGRAPHE D'INTRODUCTION (Démarche & Enjeu)
    # -------------------------------------------------------------------------
    txt_intro = (
        "L'enjeu est de déterminer <b>quelle place accorder au travail dans votre existence</b> "
        "afin de réaligner ce que vous faites au quotidien avec qui vous êtes vraiment. "
        "En explorant votre fonctionnement, vos choix passés et vos valeurs, la démarche permet "
        "de déconstruire les schémas inconscients pour <b>remettre du sens dans vos décisions</b>, "
        "reprendre votre pouvoir d'agir et concrétiser un projet réaliste."
    )
    style_intro = ParagraphStyle(
        "IntroP1",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#222222"),
    )
    p_intro = Paragraph(txt_intro, style_intro)
    p_intro.wrap(target_width, 4 * cm)
    p_intro.drawOn(c, text_x, y_cursor - p_intro.height)
    y_cursor -= p_intro.height + 0.85 * cm

    # -------------------------------------------------------------------------
    # 3. ENCADRÉ CADRAGE ÉVOLUTIF & PREMIER ÉCHANGE GRATUIT (Aéré)
    # -------------------------------------------------------------------------
    cadre_pad_x = 0.8 * cm
    cadre_w = target_width
    cadre_inner_w = cadre_w - 2 * cadre_pad_x

    style_cadre_evol = ParagraphStyle(
        "CadreEvol",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=12.8,
        textColor=colors.HexColor("#555555"),
    )
    txt_evol = (
        "<i>Le contenu de ce programme pourra évoluer après échange avec le bénéficiaire "
        "en fonction de ses besoins et du développement personnel déjà effectué dans d'autres cadres.</i>"
    )
    p_evol = Paragraph(txt_evol, style_cadre_evol)
    p_evol.wrap(cadre_inner_w, 4 * cm)

    style_rdv0 = ParagraphStyle(
        "CadreRdv0",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.0,
        leading=13.2,
        textColor=PDFStyle.COLOR_ACCENT_BLUE,
    )
    txt_rdv0 = (
        "<b><font color='#FF4D4D'>Premier échange gratuit (30 à 45 min) :</font></b> "
        "Présentation de l’accompagnement · Analyse de votre situation · "
        "Clarification de vos objectifs et identification de vos besoins."
    )
    p_rdv0 = Paragraph(txt_rdv0, style_rdv0)
    p_rdv0.wrap(cadre_inner_w, 4 * cm)

    # Calcul exact de la hauteur pour garantir un padding intérieur généreux
    top_pad = 0.55 * cm
    gap_inter = 0.28 * cm
    bottom_pad = 0.55 * cm
    cadre_h = top_pad + p_evol.height + gap_inter + 1.0 + gap_inter + p_rdv0.height + bottom_pad

    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(text_x, y_cursor - cadre_h, cadre_w, cadre_h, 8, fill=1, stroke=1)

    # Dessin paragraphe 1
    evol_y = y_cursor - top_pad - p_evol.height
    p_evol.drawOn(c, text_x + cadre_pad_x, evol_y)

    # Ligne fine séparatrice bien centrée
    line_y = evol_y - gap_inter
    c.setStrokeColor(colors.HexColor("#DDE2FA"))
    c.setLineWidth(0.6)
    c.line(
        text_x + cadre_pad_x,
        line_y,
        text_x + cadre_w - cadre_pad_x,
        line_y,
    )

    # Dessin paragraphe 2
    rdv0_y = line_y - gap_inter - p_rdv0.height
    p_rdv0.drawOn(c, text_x + cadre_pad_x, rdv0_y)

    c.restoreState()
    y_cursor -= cadre_h + 1.05 * cm

    # -------------------------------------------------------------------------
    # 4. SECTION : OBJECTIFS DU BILAN & COMPÉTENCES VISÉES
    # -------------------------------------------------------------------------
    c.setFont(PDFStyle.FONT_TITLE, 13)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x, y_cursor, "Objectifs du Bilan & Compétences Visées"
    )
    y_cursor -= 0.65 * cm

    txt_obj_intro = (
        "Le bilan de compétences vise à développer la <b>capacité à faire des choix professionnels</b> "
        "grâce à une meilleure connaissance de soi (valeurs, besoins, personnalité), de ses motivations "
        "(envies, moteurs personnels) et de ses compétences (ressources, savoirs, savoir-faire, compétences relationnelles)."
    )
    p_obj_intro = Paragraph(txt_obj_intro, style_intro)
    p_obj_intro.wrap(target_width, 3 * cm)
    p_obj_intro.drawOn(c, text_x, y_cursor - p_obj_intro.height)
    y_cursor -= p_obj_intro.height + 0.60 * cm

    competences_items = [
        (
            "Vision claire & Alignement",
            "Permettre au bénéficiaire de développer une vision claire de ses compétences et de faire "
            "le point sur ses besoins, valeurs et envies professionnelles.",
        ),
        (
            "Analyse du marché & Employabilité",
            "Développer la capacité à analyser les offres et le marché de l’emploi, à détecter les compétences "
            "recherchées par les employeurs et à identifier des dispositifs de formation adaptés.",
        ),
        (
            "Satisfaction & Autonomie",
            "Améliorer durablement son niveau de satisfaction au travail, se rendre autonome dans la gestion "
            "de sa carrière et confronter ses idées aux réalités du marché grâce à un plan d'action réaliste.",
        ),
    ]

    style_comp = ParagraphStyle(
        "CompItemWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.2,
        leading=13.8,
        textColor=colors.HexColor("#222222"),
    )

    for titre_c, desc_c in competences_items:
        txt_bullet = (
            f"<b><font color='#2F2EFA'>· {titre_c} :</font></b> {desc_c}"
        )
        p_c = Paragraph(txt_bullet, style_comp)
        p_c.wrap(target_width, 3 * cm)
        p_c.drawOn(c, text_x, y_cursor - p_c.height)
        y_cursor -= p_c.height + 0.50 * cm

    # -------------------------------------------------------------------------
    # 5. ENCADRÉ SYNTHÈSE & RESSOURCE PÉRENNE
    # -------------------------------------------------------------------------
    y_cursor -= 0.45 * cm
    callout_h = 1.90 * cm
    synthese_txt = (
        "La <b>synthèse du bilan de compétences</b> remise au bénéficiaire en fin d'accompagnement "
        "représentera un document ressource officiel co-construit pour la suite de sa carrière."
    )
    draw_workbook_highlight_box(
        c,
        text_x,
        y_cursor - callout_h,
        target_width,
        callout_h,
        prefix="👉 DOCUMENT RESSOURCE :",
        text=synthese_txt,
        accent_color=PDFStyle.COLOR_ACCENT_RED,
        bg_color=PDFStyle.COLOR_BG_NUDE,
        font_size=9.2,
        leading=13.2,
    )

    c.showPage()
