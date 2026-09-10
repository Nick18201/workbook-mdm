from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.components import draw_title, TitleStyle
from .common import (
    setup_workbook_programme_page,
    get_workbook_styles,
)


def create_programme_page_5(c):
    """Page 5 : 3. Vos Accompagnateurs (Lysiane Brand & Nicolas Blum Ferracci)."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="VOS ACCOMPAGNATEURS"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE H1 : 3. VOS ACCOMPAGNATEURS
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "3. Vos Accompagnateurs",
        pos=(text_x, y_cursor),
        available_width=target_width,
        style=TitleStyle(size=18, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    y_cursor -= 0.30 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 9.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Des profils complémentaires alliant psychologie, réalité du marché et conduite du changement",
    )
    y_cursor -= 0.75 * cm

    pad_x = 0.90 * cm
    card_inner_w = target_width - 2 * pad_x

    style_desc_lysiane = ParagraphStyle(
        "CoachDescLysiane",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.4,
        leading=15.0,
        textColor=colors.HexColor("#222222"),
    )

    style_desc_nicolas = ParagraphStyle(
        "CoachDescNicolas",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.0,
        leading=14.0,
        textColor=colors.HexColor("#222222"),
    )

    # -------------------------------------------------------------------------
    # 2. CARTE 1 : LYSIANE BRAND (Agrandie & Répartie)
    # -------------------------------------------------------------------------
    card1_h = 9.4 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.2)
    c.roundRect(
        text_x, y_cursor - card1_h, target_width, card1_h, 8, fill=1, stroke=1
    )

    # Badge rôle
    tag1 = "PSYCHOLOGUE DU TRAVAIL"
    tag1_w = c.stringWidth(tag1, PDFStyle.FONT_TITLE, 7.6) + 0.55 * cm
    tag1_h = 0.48 * cm
    tag1_x = text_x + target_width - pad_x - tag1_w
    tag1_y = y_cursor - 0.85 * cm

    c.setFillColor(colors.HexColor("#FFEAE8"))
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(0.8)
    c.roundRect(tag1_x, tag1_y, tag1_w, tag1_h, tag1_h / 2.0, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 7.6)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawCentredString(tag1_x + tag1_w / 2.0, tag1_y + 0.12 * cm, tag1)

    # Nom & Titre
    c.setFont(PDFStyle.FONT_BRANDING, 14.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.85 * cm,
        "Lysiane BRAND",
    )

    c.setFont(PDFStyle.FONT_TITLE, 10.0)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x + pad_x,
        y_cursor - 1.50 * cm,
        "Psychologue du travail · Consultante en bilan de compétences",
    )

    # Ligne de séparation fine entre en-tête et corps
    c.setStrokeColor(colors.HexColor("#ECCEC6"))
    c.setLineWidth(0.6)
    c.line(
        text_x + pad_x,
        y_cursor - 1.80 * cm,
        text_x + target_width - pad_x,
        y_cursor - 1.80 * cm,
    )

    # Contenu détaillé Lysiane Brand
    txt_lysiane = (
        "· <b>Déontologie & Confidentialité :</b> Soumise au code de déontologie des psychologues, "
        "Lysiane garantit une stricte confidentialité des échanges et documents produits, "
        "dans une posture de neutralité bienveillante tout au long de l'accompagnement.<br/><br/>"
        "· <b>Expertise recrutement :</b> 4 années d'expérience dans le secteur du recrutement (en entreprise "
        "et en cabinet) lui confèrent une solide connaissance du marché de l'emploi, de ses exigences et de ses tensions.<br/><br/>"
        "· <b>Outils & Certifications :</b> Rompue aux techniques d'entretien, elle maîtrise les outils de psychologie "
        "propres à sa formation. Elle est certifiée au questionnaire <b>MBTI</b> par The Myers Briggs Company et formée à l’<b>Ennéagramme</b> au CEE."
    )
    p_lysiane = Paragraph(txt_lysiane, style_desc_lysiane)
    p_lysiane.wrap(card_inner_w, 7.5 * cm)
    p_lysiane.drawOn(c, text_x + pad_x, y_cursor - 2.25 * cm - p_lysiane.height)

    c.restoreState()
    y_cursor -= card1_h + 0.90 * cm

    # -------------------------------------------------------------------------
    # 3. CARTE 2 : NICOLAS BLUM FERRACCI (Agrandie & Répartie)
    # -------------------------------------------------------------------------
    card2_h = 10.8 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(1.0)
    c.roundRect(
        text_x, y_cursor - card2_h, target_width, card2_h, 8, fill=1, stroke=1
    )

    # Badge rôle
    tag2 = "TRANSFORMATION & OPÉRATIONS"
    tag2_w = c.stringWidth(tag2, PDFStyle.FONT_TITLE, 7.6) + 0.55 * cm
    tag2_h = 0.48 * cm
    tag2_x = text_x + target_width - pad_x - tag2_w
    tag2_y = y_cursor - 0.85 * cm

    c.setFillColor(colors.HexColor("#EAEBFE"))
    c.setStrokeColor(colors.HexColor("#2F2EFA"))
    c.setLineWidth(0.8)
    c.roundRect(tag2_x, tag2_y, tag2_w, tag2_h, tag2_h / 2.0, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 7.6)
    c.setFillColor(colors.HexColor("#2F2EFA"))
    c.drawCentredString(tag2_x + tag2_w / 2.0, tag2_y + 0.12 * cm, tag2)

    # Nom & Titre
    c.setFont(PDFStyle.FONT_BRANDING, 14.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.85 * cm,
        "Nicolas BLUM FERRACCI",
    )

    c.setFont(PDFStyle.FONT_TITLE, 10.0)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x + pad_x,
        y_cursor - 1.50 * cm,
        "Consultant en transformation · Associé & Responsable des opérations",
    )

    # Ligne de séparation fine entre en-tête et corps
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(
        text_x + pad_x,
        y_cursor - 1.80 * cm,
        text_x + target_width - pad_x,
        y_cursor - 1.80 * cm,
    )

    # Contenu détaillé Nicolas Blum Ferracci (texte exact fourni par l'utilisateur)
    txt_nicolas = (
        "· <b>Dynamiques de transformation & conduite du changement :</b> Formé à la psychologie et rompu aux dynamiques "
        "de transformation, Nicolas accompagne les professionnels à des moments charnières de leur trajectoire. Consultant indépendant en "
        "transformation digitale et conduite du changement en entreprise, fort de 5 ans d’expérience en ESN, il dispose d’une "
        "compréhension fine des mutations organisationnelles et des réalités concrètes du monde professionnel.<br/><br/>"
        "· <b>Parcours hybride & culture de l'innovation :</b> Associé et responsable des opérations chez Marge de Manœuvre, "
        "il articule ses accompagnements autour d'un parcours hybride : l'expérience du recrutement et du terrain d'entreprise pour ancrer chaque démarche "
        "dans le réel, la rigueur du design d’expérience pour modéliser des parcours sur-mesure, et une culture continue de l’innovation pour ouvrir le champ des possibles.<br/><br/>"
        "· <b>Postures & leviers d'action :</b> En bilan de compétences, il aide chacun à faire le tri, à lever les blocages et à formaliser une "
        "trajectoire claire : valorisant la singularité de la personne, alignée avec les exigences du marché et lui redonnant toute sa capacité d’action."
    )
    p_nicolas = Paragraph(txt_nicolas, style_desc_nicolas)
    p_nicolas.wrap(card_inner_w, 8.5 * cm)
    p_nicolas.drawOn(c, text_x + pad_x, y_cursor - 2.25 * cm - p_nicolas.height)

    c.restoreState()

    c.showPage()


create_programme_page_accompagnateurs = create_programme_page_5
