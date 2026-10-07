from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from .common import setup_programme_page, draw_session_card, draw_deliverables_card


def create_programme_page_deroule_3(c):
    """
    Page 4 : Le déroulé du Bilan - Temps 2 : Confronter (Séances 7 et 8 + Livrables).
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Votre parcours d'accompagnement",
        subtitle="Un parcours structuré en séances individuelles",
        page_num=5,
        total_pages=12,
        topic="Programme du bilan",
    )

    # 1. Bandeau Temps 2 : Confronter
    band_h = 1.80 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.6)
    c.roundRect(content_x, y_cursor - band_h, content_w, band_h, 5, fill=1, stroke=1)

    # Pastille numéro 02
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.roundRect(content_x + 0.35 * cm, y_cursor - 1.35 * cm, 1.3 * cm, 0.9 * cm, 4, fill=1, stroke=0)
    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.drawCentredString(content_x + 1.0 * cm, y_cursor - 1.05 * cm, "02")

    # Titre et posture
    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(content_x + 1.9 * cm, y_cursor - 0.70 * cm, "TEMPS 2 : CONFRONTER")

    c.setFont(PDFStyle.FONT_ITALIC, 8.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(content_x + 7.5 * cm, y_cursor - 0.70 * cm, "• Confronter l'idée au terrain")

    # Phrase d'introduction
    style_t2_intro = ParagraphStyle(
        "T2Intro",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor("#4B5563"),
    )
    txt_t2 = (
        "<i>Confronter vos pistes au marché : ouvrir les possibles, puis vérifier métiers, salaires "
        "et débouchés auprès de celles et ceux qui les exercent.</i>"
    )
    p_t2 = Paragraph(txt_t2, style_t2_intro)
    p_t2.wrap(content_w - 2.2 * cm, 1.0 * cm)
    p_t2.drawOn(c, content_x + 1.9 * cm, y_cursor - band_h + 0.25 * cm)
    c.restoreState()
    y_cursor -= band_h + 0.60 * cm

    # 2. Les deux séances (S7, S8)
    sessions = [
        {
            "badge": "S7",
            "title": "Explorer des métiers et des secteurs",
            "description": (
                "On ouvre le champ des possibles de manière structurée : 10 pistes qualifiées, 5 réalistes "
                "et 5 audacieuses, cohérentes avec votre profil, vos compétences et vos aspirations. "
                "Vous préparez les enquêtes terrain qui vont les mettre à l'épreuve."
            ),
            "objective": "faire émerger des pistes alignées avec votre profil.",
            "height": 5.8 * cm,
        },
        {
            "badge": "S8",
            "title": "Approfondir et confronter vos pistes",
            "description": (
                "On passe à une phase concrète. Vos pistes sont classées en trois familles de scénarios : "
                "pistes directes, passerelles courtes, angles morts. Vous lancez des enquêtes auprès de professionnels "
                "en poste et vérifiez salaires et débouchés dans votre bassin d'emploi."
            ),
            "objective": "confronter vos idées à la réalité et affiner vos projections.",
            "height": 5.8 * cm,
        },
    ]

    gap = 0.50 * cm
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

    # 3. Encadré Livrables Temps 2
    y_cursor -= 0.20 * cm
    deliv_h = 2.9 * cm
    draw_deliverables_card(
        c,
        content_x,
        y_cursor - deliv_h,
        content_w,
        deliv_h,
        title="LIVRABLES VALIDÉS À L'ISSUE DU TEMPS 2 (CONFRONTER) :",
        items=[
            "Matrice de faisabilité marché (adéquation compétences, marché, débouchés)",
            "3 scénarios professionnels documentés et comparés",
            "Retours d'enquêtes terrain auprès de professionnels en poste",
        ],
    )

    c.showPage()
