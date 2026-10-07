import os
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from .common import setup_programme_page


def create_programme_page_objectifs(c):
    """
    Page 2 : Cadrage, Objectifs réglementaires & Compétences visées.
    - Les 3 phases légales du Code du travail (art. R. 6313-4 à R. 6313-8)
    - Compétences visées & Finalités du bilan
    - Cadrage évolutif & Premier échange gratuit (30 à 45 min en visio)
    - Document de synthèse officiel co-construit
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Objectifs & Cadre réglementaire",
        subtitle="Les 3 phases légales et le développement de votre pouvoir d'agir",
        page_num=2,
        total_pages=12,
        topic="Objectifs du bilan",
    )

    pad_x = 0.70 * cm
    inner_w = content_w - 2 * pad_x

    # -------------------------------------------------------------------------
    # 1. CHAPEAU D'INTRODUCTION : LA DÉMARCHE & L'ENJEU
    # -------------------------------------------------------------------------
    txt_intro = (
        "L'enjeu du bilan de compétences est de déterminer <b>quelle place accorder au travail dans votre existence</b> "
        "afin de réaligner ce que vous faites au quotidien avec qui vous êtes vraiment. "
        "En explorant votre fonctionnement, vos choix passés et vos valeurs, la démarche permet de déconstruire "
        "les schémas inconscients pour <b>remettre du sens dans vos décisions</b>, reprendre votre pouvoir d'agir "
        "et concrétiser un projet professionnel réaliste et épanouissant."
    )
    style_intro = ParagraphStyle(
        "ObjIntro",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=13.0,
        textColor=colors.HexColor("#1F2937"),
    )
    p_intro = Paragraph(txt_intro, style_intro)
    p_intro.wrap(content_w, 3.5 * cm)
    p_intro.drawOn(c, content_x, y_cursor - p_intro.height)
    y_cursor -= p_intro.height + 0.45 * cm

    # -------------------------------------------------------------------------
    # 2. ENCADRÉ : LES 3 PHASES RÉGLEMENTAIRES DU CODE DU TRAVAIL
    # -------------------------------------------------------------------------
    card_phases_h = 6.9 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setLineWidth(0.8)
    c.roundRect(content_x, y_cursor - card_phases_h, content_w, card_phases_h, 6, fill=1, stroke=1)

    # Titre encadré
    c.setFont(PDFStyle.FONT_TITLE, 9.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        content_x + pad_x,
        y_cursor - 0.65 * cm,
        "Les 3 phases légales obligatoires (articles R. 6313-4 à R. 6313-8 du Code du travail) :",
    )

    phases_items = [
        (
            "1. Phase préliminaire",
            "Confirmer l'engagement du bénéficiaire, analyser la nature de ses besoins, "
            "définir conjointement les conditions de déroulement du bilan et présenter les outils mobilisés.",
        ),
        (
            "2. Phase d'investigation",
            "Explorer en profondeur le parcours, les motivations et les compétences (savoirs, savoir-faire, savoir-être). "
            "Identifier les perspectives d'évolution et confronter les scénarios aux réalités du marché de l'emploi.",
        ),
        (
            "3. Phase de conclusion",
            "S'approprier les résultats de l'investigation, recenser les facteurs de réussite du projet, "
            "co-construire un plan d'action réaliste et finaliser le document de synthèse écrit.",
        ),
    ]

    style_phase = ParagraphStyle(
        "PhaseItem",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.4,
        leading=12.2,
        textColor=colors.HexColor("#374151"),
    )

    phase_y = y_cursor - 1.05 * cm
    for title_p, desc_p in phases_items:
        txt_p = f"• <b><font color='#2F2EFA'>{title_p} :</font></b> {desc_p}"
        p = Paragraph(txt_p, style_phase)
        p.wrap(inner_w, 2.0 * cm)
        p.drawOn(c, content_x + pad_x, phase_y - p.height)
        phase_y -= p.height + 0.32 * cm

    c.restoreState()
    y_cursor -= card_phases_h + 0.45 * cm

    # -------------------------------------------------------------------------
    # 3. ENCADRÉ : COMPÉTENCES VISÉES & FINALITÉS
    # -------------------------------------------------------------------------
    card_comp_h = 6.9 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.8)
    c.roundRect(content_x, y_cursor - card_comp_h, content_w, card_comp_h, 6, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 9.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        content_x + pad_x,
        y_cursor - 0.65 * cm,
        "Compétences visées & Finalités de l'accompagnement :",
    )

    comp_items = [
        (
            "Vision claire & Alignement",
            "Développer une connaissance lucide de son fonctionnement, de ses compétences et de ses motivations profondes. "
            "Clarifier ses valeurs et poser des critères de choix non négociables.",
        ),
        (
            "Analyse du marché & Employabilité",
            "Développer la capacité à analyser les dynamiques d'embauche et opportunités professionnelles, "
            "détecter les compétences recherchées et identifier les dispositifs de formation adaptés.",
        ),
        (
            "Satisfaction & Pouvoir d'agir",
            "Se rendre pleinement autonome dans la gestion de sa carrière, lever les freins psychologiques, "
            "sécuriser financièrement sa transition et engager des actions concrètes vérifiées sur le terrain.",
        ),
    ]

    style_comp = ParagraphStyle(
        "CompItem",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.4,
        leading=12.2,
        textColor=colors.HexColor("#374151"),
    )

    comp_y = y_cursor - 1.05 * cm
    for title_c, desc_c in comp_items:
        txt_c = f"• <b><font color='#DC2626'>{title_c} :</font></b> {desc_c}"
        p = Paragraph(txt_c, style_comp)
        p.wrap(inner_w, 2.0 * cm)
        p.drawOn(c, content_x + pad_x, comp_y - p.height)
        comp_y -= p.height + 0.32 * cm

    c.restoreState()
    y_cursor -= card_comp_h + 0.45 * cm

    # -------------------------------------------------------------------------
    # 4. ENCADRÉ : CADRAGE ÉVOLUTIF & PREMIER ÉCHANGE GRATUIT
    # -------------------------------------------------------------------------
    card_rdv_h = 3.2 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.0)
    c.roundRect(content_x, y_cursor - card_rdv_h, content_w, card_rdv_h, 6, fill=1, stroke=1)

    style_rdv = ParagraphStyle(
        "RdvText",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.3,
        leading=12.0,
        textColor=colors.HexColor("#1F2937"),
    )
    txt_rdv = (
        "<font name='ZapfDingbats' color='#DC2626'>☛</font> <b><font color='#DC2626'>Premier échange gratuit (30 à 45 min en visio) :</font></b> "
        "Présentation détaillée de l'accompagnement, analyse de votre situation, clarification de vos objectifs "
        "et vérification de l'adéquation mutuelle avant tout engagement.<br/><br/>"
        "<i>Le contenu du programme est ajustable après cet échange en fonction de vos besoins spécifiques "
        "et du travail déjà mené dans d'autres cadres.</i>"
    )
    p_rdv = Paragraph(txt_rdv, style_rdv)
    p_rdv.wrap(inner_w, 2.6 * cm)
    p_rdv.drawOn(c, content_x + pad_x, y_cursor - 0.45 * cm - p_rdv.height)

    c.restoreState()
    y_cursor -= card_rdv_h + 0.40 * cm

    # -------------------------------------------------------------------------
    # 5. ENCADRÉ BAS : DOCUMENT RESSOURCE PÉRENNE
    # -------------------------------------------------------------------------
    card_res_h = 1.65 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.7)
    c.roundRect(content_x, y_cursor - card_res_h, content_w, card_res_h, 5, fill=1, stroke=1)

    style_res = ParagraphStyle(
        "ResText",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.2,
        leading=11.6,
        textColor=colors.HexColor("#4B5563"),
    )
    txt_res = (
        "<b>Document ressource officiel :</b> La synthèse écrite co-construite remise à l'issue de la phase de conclusion "
        "représente un livrable officiel confidentiel, propriété exclusive du bénéficiaire (art. L. 6313-4 du Code du travail)."
    )
    p_res = Paragraph(txt_res, style_res)
    p_res.wrap(inner_w, 1.3 * cm)
    p_res.drawOn(c, content_x + pad_x, y_cursor - card_res_h + (card_res_h - p_res.height) / 2.0)

    c.restoreState()
    c.showPage()


# Alias pour rétro-compatibilité
create_programme_page_1 = create_programme_page_objectifs
