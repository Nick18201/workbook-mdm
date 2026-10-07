from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from .common import setup_programme_page


def create_programme_page_organisation_pedagogie(c):
    """
    Page 8 : Organisation Pratique & Moyens Pédagogiques.
    - 100 % en visio partout en France
    - 7 carnets de bord guidés, Copilote IA Marge de Manœuvre, Espace Notion ressource
    - Questionnaire MBTI® officiel et inventaire Hexa3D
    - Organisation du travail inter-séances
    - Assistance pédagogique réactive sous 48h ouvrées et cadre déontologique strict
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Organisation & Moyens pédagogiques",
        subtitle="Modalités d'accompagnement, outils exclusifs et travail inter-séances",
        page_num=8,
        total_pages=12,
        topic="Organisation & Moyens",
    )

    pad_x = 0.70 * cm
    inner_w = content_w - 2 * pad_x

    # -------------------------------------------------------------------------
    # 1. ENCADRÉ 1 : MOYENS TECHNIQUES, PÉDAGOGIQUES & OUTILS EXCLUSIFS (2 COL)
    # -------------------------------------------------------------------------
    moyens_h = 9.3 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setLineWidth(0.8)
    c.roundRect(content_x, y_cursor - moyens_h, content_w, moyens_h, 6, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 9.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        content_x + pad_x,
        y_cursor - 0.65 * cm,
        "Moyens techniques, pédagogiques & outils exclusifs :",
    )

    style_col_item = ParagraphStyle(
        "MoyenColItem",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.3,
        leading=12.2,
        textColor=colors.HexColor("#222222"),
    )

    col_gap = 0.6 * cm
    col_w = (inner_w - col_gap) / 2.0

    # Colonne Gauche : Entretiens visio, Carnets, Copilote IA, Enquêtes
    txt_col1 = (
        "• <b>Entretiens 100 % en visio :</b> séances individuelles de 1h à 1h30, "
        "espacées de 1 à 2 semaines, avec le même accompagnateur tout au long du bilan.<br/><br/>"
        "• <b>7 carnets de bord guidés :</b> supports structurés pas à pas pour mener votre travail "
        "personnel en toute autonomie (conservés à vie).<br/><br/>"
        "• <b>Copilote IA exclusif :</b> un assistant interactif conçu pour challenger vos réflexions, "
        "stimuler votre créativité et vous guider dans vos exercices.<br/><br/>"
        "• <b>Enquêtes-métiers terrain :</b> confrontation au réel et rencontres de professionnels en activité "
        "grâce à des guides d'entretien ciblés."
    )
    p_col1 = Paragraph(txt_col1, style_col_item)
    p_col1.wrap(col_w, 8.0 * cm)
    p_col1.drawOn(c, content_x + pad_x, y_cursor - 1.05 * cm - p_col1.height)

    # Séparation verticale
    sep_x = content_x + pad_x + col_w + (col_gap / 2.0)
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(sep_x, y_cursor - 0.85 * cm, sep_x, y_cursor - moyens_h + 0.60 * cm)

    # Colonne Droite : Espace Notion, Tests certifiés, Outils créatifs, Assistance
    txt_col2 = (
        "• <b>Espace Notion ressource :</b> bibliothèque exclusive d'articles, podcasts, "
        "vidéos et fiches repères accessible jusqu'au suivi à 6 mois.<br/><br/>"
        "• <b>Tests certifiés :</b> questionnaire officiel <b>MBTI®</b> (Myers-Briggs) "
        "et inventaire d'intérêts professionnels (Hexa3D).<br/><br/>"
        "• <b>Exercices de créativité :</b> cartes projectives, matrices décisionnelles "
        "et grilles d'arbitrage anti-compromis.<br/><br/>"
        "• <b>Assistance pédagogique réactive :</b> suivi continu par email et téléphone, "
        "réponse garantie sous 48h ouvrées maximum."
    )
    p_col2 = Paragraph(txt_col2, style_col_item)
    p_col2.wrap(col_w, 8.0 * cm)
    p_col2.drawOn(c, sep_x + (col_gap / 2.0), y_cursor - 1.05 * cm - p_col2.height)

    c.restoreState()
    y_cursor -= moyens_h + 0.50 * cm

    # -------------------------------------------------------------------------
    # 2. ENCADRÉ 2 : ORGANISATION DU TRAVAIL INTER-SÉANCES
    # -------------------------------------------------------------------------
    inter_h = 5.9 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.0)
    c.roundRect(content_x, y_cursor - inter_h, content_w, inter_h, 6, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 9.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        content_x + pad_x,
        y_cursor - 0.65 * cm,
        "Organisation & réalisation du travail inter-séances :",
    )

    style_inter = ParagraphStyle(
        "InterTxt",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.4,
        leading=12.4,
        textColor=colors.HexColor("#1F2937"),
    )
    txt_inter = (
        "• <b>Rythme et alternance :</b> Le bilan alterne des entretiens réguliers en visio et des temps "
        "dédiés de travail personnel (environ 1h à 2h par carnet, selon vos disponibilités).<br/><br/>"
        "• <b>Supports accessibles en continu :</b> Vos exercices s'appuient sur vos carnets guidés et l'espace Notion ressource, "
        "disponibles dès la formalisation de votre parcours.<br/><br/>"
        "• <b>Consignes personnalisées :</b> À l'issue de chaque séance, votre accompagnateur formule des consignes claires "
        "et adapte les exercices à votre charge mentale et à vos priorités du moment."
    )
    p_inter = Paragraph(txt_inter, style_inter)
    p_inter.wrap(inner_w, 4.8 * cm)
    p_inter.drawOn(c, content_x + pad_x, y_cursor - 1.05 * cm - p_inter.height)

    c.restoreState()
    y_cursor -= inter_h + 0.50 * cm

    # -------------------------------------------------------------------------
    # 3. ENCADRÉ 3 : CADRE DE CONFIANCE & DÉONTOLOGIE
    # -------------------------------------------------------------------------
    cadre_h = 4.6 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.8)
    c.roundRect(content_x, y_cursor - cadre_h, content_w, cadre_h, 6, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 9.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        content_x + pad_x,
        y_cursor - 0.65 * cm,
        "Assistance continue & Engagement déontologique :",
    )

    style_cadre = ParagraphStyle(
        "CadreTxt",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.3,
        leading=12.2,
        textColor=colors.HexColor("#374151"),
    )
    txt_cadre = (
        "• <b>Assistance pédagogique & technique réactive :</b> Tout au long du parcours, vous n'êtes jamais seul(e). "
        "Votre accompagnateur référent répond à vos questions par email ou par téléphone dans un délai garanti de <b>48h ouvrées</b>.<br/><br/>"
        "• <b>Cadre de confiance absolu :</b> Respect strict du secret professionnel, posture de neutralité, "
        "adhésion au code de déontologie des psychologues et protection intégrale de vos données personnelles."
    )
    p_cadre = Paragraph(txt_cadre, style_cadre)
    p_cadre.wrap(inner_w, 3.6 * cm)
    p_cadre.drawOn(c, content_x + pad_x, y_cursor - 1.05 * cm - p_cadre.height)

    c.restoreState()
    c.showPage()


# Alias
create_programme_page_4 = create_programme_page_organisation_pedagogie
