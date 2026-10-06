from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from .common import setup_programme_page, draw_session_card


def create_programme_page_deroule_1(c):
    """
    Page 2 : Le déroulé du Bilan - Temps 1 : Comprendre (Partie 1, Séances 1 à 3).
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Votre parcours d'accompagnement",
        subtitle="Un parcours structuré en séances individuelles",
        page_num=2,
        total_pages=8,
        topic="Programme du bilan",
    )

    # 1. Paragraphe d'introduction général du parcours
    txt_intro = (
        "<b>10 séances individuelles en visio et un entretien de suivi à 6 mois (45 min)</b>, "
        "soit <b>13 h d'accompagnement</b> avec la personne qui vous accompagne, choisie lors du premier échange. "
        "Entre les séances, <b>7 carnets de bord guidés</b>."
    )
    style_intro = ParagraphStyle(
        "DerouleIntroP2",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=13.0,
        textColor=colors.HexColor("#1F2937"),
    )

    intro_h = 1.40 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.setLineWidth(0.8)
    c.roundRect(content_x, y_cursor - intro_h, content_w, intro_h, 5, fill=1, stroke=1)

    p_intro = Paragraph(txt_intro, style_intro)
    p_intro.wrap(content_w - 0.7 * cm, intro_h)
    p_intro.drawOn(c, content_x + 0.35 * cm, y_cursor - intro_h + (intro_h - p_intro.height) / 2.0)
    c.restoreState()
    y_cursor -= intro_h + 0.50 * cm

    # 2. Bandeau Temps 1 : Comprendre
    band_h = 1.75 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.6)
    c.roundRect(content_x, y_cursor - band_h, content_w, band_h, 5, fill=1, stroke=1)

    # Pastille numéro 01
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.roundRect(content_x + 0.35 * cm, y_cursor - 1.30 * cm, 1.3 * cm, 0.9 * cm, 4, fill=1, stroke=0)
    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.drawCentredString(content_x + 1.0 * cm, y_cursor - 1.00 * cm, "01")

    # Titre et posture
    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(content_x + 1.9 * cm, y_cursor - 0.65 * cm, "TEMPS 1 : COMPRENDRE")

    c.setFont(PDFStyle.FONT_ITALIC, 8.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(content_x + 7.5 * cm, y_cursor - 0.65 * cm, "• Poser le sac à dos")

    # Phrase d'introduction du temps 1
    style_t1_intro = ParagraphStyle(
        "T1Intro",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor("#4B5563"),
    )
    txt_t1 = (
        "<i>Comprendre ce qui vous fait avancer : votre point de départ, votre parcours réel, "
        "votre fonctionnement, votre rapport à l'argent et vos valeurs.</i>"
    )
    p_t1 = Paragraph(txt_t1, style_t1_intro)
    p_t1.wrap(content_w - 2.2 * cm, 1.0 * cm)
    p_t1.drawOn(c, content_x + 1.9 * cm, y_cursor - band_h + 0.22 * cm)
    c.restoreState()
    y_cursor -= band_h + 0.50 * cm

    # 3. Les trois séances (S1, S2, S3)
    sessions = [
        {
            "badge": "S1",
            "title": "Faire le point sur votre situation actuelle",
            "description": (
                "On commence par revenir à l'essentiel. Votre état actuel, votre énergie, ce qui vous pèse, "
                "ce qui tient encore. On pose aussi le cadre de travail : vos attentes, la confidentialité, "
                "la façon dont nous avancerons ensemble."
            ),
            "objective": "clarifier votre point de départ et sortir du flou.",
            "height": 4.8 * cm,
        },
        {
            "badge": "S2",
            "title": "Comprendre ce qui vous a construit et l'impact de vos héritages",
            "description": (
                "Votre rapport au travail ne s'est pas fait au hasard. On explore votre environnement, les modèles "
                "que vous avez eus, les messages reçus. Ce qui a influencé vos choix, parfois sans que vous en ayez "
                "conscience. Cela permet de prendre du recul et de ne plus avancer en pilotage automatique."
            ),
            "objective": "identifier les influences qui orientent encore vos choix aujourd'hui.",
            "height": 5.3 * cm,
        },
        {
            "badge": "S3",
            "title": "Analyser et donner du sens à votre parcours",
            "description": (
                "Vous avez déjà des expériences, des compétences, des intuitions. On regarde votre travail réel, "
                "au-delà de la fiche de poste, pour identifier : ce que vous savez faire, ce que vous aimez réellement, "
                "et ce qui ne vous correspond plus."
            ),
            "objective": "faire émerger des lignes directrices et vos ressources réelles.",
            "height": 4.8 * cm,
        },
    ]

    gap = 0.40 * cm
    for s in sessions:
        h = s["height"]
        draw_session_card(
            c,
            content_x,
            y_cursor - h,
            content_w,
            h,
            badge=s["badge"],
            title=s["title"],
            description=s["description"],
            objective=s["objective"],
        )
        y_cursor -= h + gap

    c.showPage()
