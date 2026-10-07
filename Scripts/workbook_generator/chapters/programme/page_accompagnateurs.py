from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from .common import setup_programme_page


def create_programme_page_accompagnateurs(c):
    """
    Page 9 : Vos Accompagnateurs (Lysiane Brand & Nicolas Blum Ferracci).
    Profils complémentaires alliant psychologie du travail, réalité du marché et conduite du changement.
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Vos accompagnateurs",
        subtitle="Des profils complémentaires alliant psychologie du travail et réalité du marché",
        page_num=9,
        total_pages=12,
        topic="Vos accompagnateurs",
    )

    pad_x = 0.75 * cm
    card_inner_w = content_w - 2 * pad_x

    style_desc_lysiane = ParagraphStyle(
        "ConsultantDescLysiane",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#222222"),
    )

    style_desc_nicolas = ParagraphStyle(
        "ConsultantDescNicolas",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor("#222222"),
    )

    # -------------------------------------------------------------------------
    # 1. CARTE 1 : LYSIANE BRAND (Psychologue du travail)
    # -------------------------------------------------------------------------
    card1_h = 9.8 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.0)
    c.roundRect(content_x, y_cursor - card1_h, content_w, card1_h, 6, fill=1, stroke=1)

    # Badge rôle en haut à droite
    tag1 = "PSYCHOLOGUE DU TRAVAIL"
    tag1_w = c.stringWidth(tag1, PDFStyle.FONT_TITLE, 7.5) + 0.50 * cm
    tag1_h = 0.50 * cm
    tag1_x = content_x + content_w - pad_x - tag1_w
    tag1_y = y_cursor - 0.75 * cm

    c.setFillColor(colors.HexColor("#FFEAE8"))
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(0.8)
    c.roundRect(tag1_x, tag1_y, tag1_w, tag1_h, tag1_h / 2.0, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 7.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawCentredString(tag1_x + tag1_w / 2.0, tag1_y + 0.13 * cm, tag1)

    # Nom & Titre
    c.setFont(PDFStyle.FONT_BRANDING, 14.0)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(content_x + pad_x, y_cursor - 0.75 * cm, "Lysiane BRAND")

    c.setFont(PDFStyle.FONT_TITLE, 9.2)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        content_x + pad_x,
        y_cursor - 1.30 * cm,
        "Psychologue du travail · Consultante en bilan de compétences",
    )

    # Séparation fine
    c.setStrokeColor(colors.HexColor("#ECCEC6"))
    c.setLineWidth(0.6)
    c.line(
        content_x + pad_x,
        y_cursor - 1.55 * cm,
        content_x + content_w - pad_x,
        y_cursor - 1.55 * cm,
    )

    # Contenu détaillé Lysiane Brand
    txt_lysiane = (
        "• <b>Déontologie & Confidentialité :</b> Soumise au code de déontologie des psychologues, "
        "Lysiane garantit une stricte confidentialité des échanges et documents produits, "
        "dans une posture de neutralité tout au long de votre accompagnement.<br/><br/>"
        "• <b>Expertise recrutement & marché :</b> 4 années d'expérience dans le secteur du recrutement "
        "(en entreprise et en cabinet) lui confèrent une solide connaissance du marché de l'emploi, de ses exigences et de ses opportunités réelles.<br/><br/>"
        "• <b>Outils & Certifications :</b> Rompue aux techniques d'entretien approfondi, elle maîtrise les approches cliniques "
        "propres à sa formation. Elle est certifiée au questionnaire <b>MBTI®</b> officiel par The Myers-Briggs Company."
    )
    p_lysiane = Paragraph(txt_lysiane, style_desc_lysiane)
    p_lysiane.wrap(card_inner_w, 7.5 * cm)
    p_lysiane.drawOn(c, content_x + pad_x, y_cursor - 1.85 * cm - p_lysiane.height)

    c.restoreState()
    y_cursor -= card1_h + 0.60 * cm

    # -------------------------------------------------------------------------
    # 2. CARTE 2 : NICOLAS BLUM FERRACCI (Transformation & Opérations)
    # -------------------------------------------------------------------------
    card2_h = 11.2 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setLineWidth(1.0)
    c.roundRect(content_x, y_cursor - card2_h, content_w, card2_h, 6, fill=1, stroke=1)

    # Badge rôle en haut à droite
    tag2 = "TRANSFORMATION & OPÉRATIONS"
    tag2_w = c.stringWidth(tag2, PDFStyle.FONT_TITLE, 7.5) + 0.50 * cm
    tag2_h = 0.50 * cm
    tag2_x = content_x + content_w - pad_x - tag2_w
    tag2_y = y_cursor - 0.75 * cm

    c.setFillColor(colors.HexColor("#EAEBFE"))
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setLineWidth(0.8)
    c.roundRect(tag2_x, tag2_y, tag2_w, tag2_h, tag2_h / 2.0, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 7.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawCentredString(tag2_x + tag2_w / 2.0, tag2_y + 0.13 * cm, tag2)

    # Nom & Titre
    c.setFont(PDFStyle.FONT_BRANDING, 14.0)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(content_x + pad_x, y_cursor - 0.75 * cm, "Nicolas BLUM FERRACCI")

    c.setFont(PDFStyle.FONT_TITLE, 9.2)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        content_x + pad_x,
        y_cursor - 1.30 * cm,
        "Consultant en transformation · Associé & Responsable des opérations",
    )

    # Séparation fine
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(
        content_x + pad_x,
        y_cursor - 1.55 * cm,
        content_x + content_w - pad_x,
        y_cursor - 1.55 * cm,
    )

    # Contenu détaillé Nicolas Blum Ferracci
    txt_nicolas = (
        "• <b>Dynamiques de transformation & conduite du changement :</b> Formé à la psychologie et rompu aux dynamiques "
        "de transformation, Nicolas accompagne les professionnels à des moments charnières de leur trajectoire. Consultant indépendant "
        "en transformation digitale et conduite du changement en entreprise, fort de 5 ans d’expérience en ESN, il dispose d’une "
        "compréhension fine des mutations organisationnelles et des réalités concrètes du monde professionnel.<br/><br/>"
        "• <b>Parcours hybride & culture de l'innovation :</b> Associé et responsable des opérations chez Marge de Manœuvre, "
        "il articule ses accompagnements autour d'un parcours hybride : l'expérience du recrutement et du terrain d'entreprise pour ancrer chaque démarche "
        "dans le réel, la rigueur du design d’expérience pour modéliser des parcours sur-mesure, et une culture continue de l’innovation pour ouvrir le champ des possibles.<br/><br/>"
        "• <b>Postures & leviers d'action :</b> En bilan de compétences, il aide chacun à faire le tri, à lever les blocages et à formaliser une "
        "trajectoire claire : valorisant la singularité de la personne, alignée avec les exigences du marché et lui redonnant toute sa capacité d’action."
    )
    p_nicolas = Paragraph(txt_nicolas, style_desc_nicolas)
    p_nicolas.wrap(card_inner_w, 8.8 * cm)
    p_nicolas.drawOn(c, content_x + pad_x, y_cursor - 1.85 * cm - p_nicolas.height)

    c.restoreState()
    c.showPage()


# Alias
create_programme_page_5 = create_programme_page_accompagnateurs
