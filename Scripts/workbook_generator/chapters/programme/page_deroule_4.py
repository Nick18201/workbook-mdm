from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from .common import setup_programme_page, draw_session_card, draw_deliverables_card


def create_programme_page_deroule_4(c):
    """
    Page 5 : Le déroulé du Bilan - Temps 3 : Décider et agir (Séances 9, 10, Suivi + Livrables).
    Note sur les 13 séances supprimée conformément aux spécifications.
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Votre parcours d'accompagnement",
        subtitle="Un parcours structuré en séances individuelles",
        page_num=5,
        total_pages=8,
        topic="Programme du bilan",
    )

    # 1. Bandeau Temps 3 : Décider et agir
    band_h = 1.70 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.6)
    c.roundRect(content_x, y_cursor - band_h, content_w, band_h, 5, fill=1, stroke=1)

    # Pastille numéro 03
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.roundRect(content_x + 0.35 * cm, y_cursor - 1.25 * cm, 1.3 * cm, 0.9 * cm, 4, fill=1, stroke=0)
    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.drawCentredString(content_x + 1.0 * cm, y_cursor - 0.95 * cm, "03")

    # Titre et posture
    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(content_x + 1.9 * cm, y_cursor - 0.65 * cm, "TEMPS 3 : DÉCIDER ET AGIR")

    c.setFont(PDFStyle.FONT_ITALIC, 8.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(content_x + 8.1 * cm, y_cursor - 0.65 * cm, "• Sécuriser le passage à l'action")

    # Phrase d'introduction
    style_t3_intro = ParagraphStyle(
        "T3Intro",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor("#4B5563"),
    )
    txt_t3 = (
        "<i>Repartir avec un plan daté : arbitrer, adapter votre carnet de route à votre projet, "
        "engager les premières actions.</i>"
    )
    p_t3 = Paragraph(txt_t3, style_t3_intro)
    p_t3.wrap(content_w - 2.2 * cm, 1.0 * cm)
    p_t3.drawOn(c, content_x + 1.9 * cm, y_cursor - band_h + 0.22 * cm)
    c.restoreState()
    y_cursor -= band_h + 0.35 * cm

    # 2. Les séances : S9, S10, Suivi à 6 mois
    sessions = [
        {
            "badge": "S9",
            "title": "Faire un choix cohérent avec votre introspection et le marché",
            "description": (
                "On fait des choix. On identifie les pistes prioritaires et les moyens d'y accéder. Votre carnet de route "
                "s'adapte ensuite à votre projet : formations et financements pour une reconversion, modèle économique "
                "et première offre pour une création, argumentaire de repositionnement pour une évolution interne."
            ),
            "objective": "passer d'une réflexion à un projet clair et réaliste.",
            "height": 4.8 * cm,
            "is_followup": False,
        },
        {
            "badge": "S10",
            "title": "Structurer la suite",
            "description": (
                "On fait la synthèse du travail réalisé. Vous repartez avec deux trajectoires complémentaires, "
                "une piste A (projet d'élan) et une piste B (refuge et tremplin), des premières actions à mener dans les 7 jours, "
                "et le document de synthèse co-rédigé, qui n'appartient qu'à vous."
            ),
            "objective": "repartir avec une trajectoire claire sur les prochains mois.",
            "height": 4.6 * cm,
            "is_followup": False,
        },
        {
            "badge": "Suivi",
            "title": "On se revoit 6 mois après pour faire le point sur votre projet (45 min)",
            "description": (
                "Un entretien individuel de 45 min pour analyser vos avancées réelles, ajuster les démarches si besoin, "
                "lever les nouveaux blocages et consolider durablement la dynamique engagée."
            ),
            "objective": "consolider la dynamique et ajuster la trajectoire si nécessaire.",
            "height": 4.0 * cm,
            "is_followup": True,
        },
    ]

    gap = 0.30 * cm
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
            is_followup=s["is_followup"],
        )
        y_cursor -= h + gap

    # 3. Encadré Livrables Temps 3 (avec hauteur suffisante pour que le 4e item respire parfaitement)
    y_cursor -= 0.15 * cm
    deliv_h = 3.3 * cm
    draw_deliverables_card(
        c,
        content_x,
        y_cursor - deliv_h,
        content_w,
        deliv_h,
        title="LIVRABLES VALIDÉS À L'ISSUE DU TEMPS 3 (DÉCIDER ET AGIR) :",
        items=[
            "Feuilles de route piste A (projet d'élan) et piste B (refuge et tremplin)",
            "Premières actions concrètes à mener sous 7 jours",
            "Document de synthèse officiel co-rédigé (confidentiel et strictement personnel)",
            "Entretien individuel de suivi à 6 mois inclus",
        ],
    )

    c.showPage()
