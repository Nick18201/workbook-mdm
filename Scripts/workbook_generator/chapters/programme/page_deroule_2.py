from reportlab.lib.units import cm
from reportlab.lib import colors

from workbook_generator.config import PDFStyle
from .common import setup_programme_page, draw_session_card, draw_deliverables_card


def create_programme_page_deroule_2(c):
    """
    Page 3 : Le déroulé du Bilan - Temps 1 : Comprendre (Partie 2, Séances 4 à 6 + Livrables).
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Votre parcours d'accompagnement",
        subtitle="Un parcours structuré en séances individuelles",
        page_num=3,
        total_pages=8,
        topic="Programme du bilan",
    )

    # 1. Rappel bandeau Temps 1 (suite)
    band_h = 1.10 * cm
    c.saveState()
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(0.6)
    c.roundRect(content_x, y_cursor - band_h, content_w, band_h, 4, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 9.5)
    c.setFillColor(colors.HexColor("#111827"))
    c.drawString(content_x + 0.45 * cm, y_cursor - 0.70 * cm, "TEMPS 1 : COMPRENDRE (SUITE)")

    c.setFont(PDFStyle.FONT_ITALIC, 8.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(content_x + 6.8 * cm, y_cursor - 0.70 * cm, "• Approfondissement de l'introspection")
    c.restoreState()
    y_cursor -= band_h + 0.45 * cm

    # 2. Les trois séances (S4, S5, S6)
    sessions = [
        {
            "badge": "S4",
            "title": "Comprendre votre fonctionnement (MBTI®)",
            "description": (
                "On travaille votre fonctionnement en profondeur. Avec le questionnaire officiel MBTI®, vous comprenez : "
                "comment vous prenez des décisions, ce qui vous stimule, ce qui vous fatigue, votre manière d'interagir. "
                "On le met en regard de votre vécu : les environnements qui vous conviennent, ceux qui vous épuisent."
            ),
            "objective": "obtenir une grille de lecture claire de votre fonctionnement et de vos facteurs d'usure.",
            "height": 5.2 * cm,
        },
        {
            "badge": "S5",
            "title": "Poser sans tabou votre rapport à l'argent",
            "description": (
                "On pose les chiffres de votre sécurité financière : vos 4 seuils financiers, le revenu vital et le revenu "
                "sécurisant, le délai de trésorerie que vous pouvez tenir. Une transition viable se calcule, sans précariser "
                "l'équilibre de votre foyer."
            ),
            "objective": "fixer le seuil de sécurité financière qui servira à arbitrer vos pistes.",
            "height": 4.8 * cm,
        },
        {
            "badge": "S6",
            "title": "Clarifier vos valeurs et vos moteurs",
            "description": (
                "Vous définissez ce qui compte vraiment pour vous aujourd'hui : vos priorités, vos limites, vos critères de satisfaction. "
                "Ce qui est essentiel, et ce que vous n'êtes plus prêt(e) à accepter. Ils deviennent une grille anti-compromis, "
                "avec des critères observables sur le terrain."
            ),
            "objective": "définir vos critères de choix pour un projet cohérent.",
            "height": 5.0 * cm,
        },
    ]

    gap = 0.35 * cm
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

    # 3. Encadré Livrables Temps 1
    y_cursor -= 0.20 * cm
    deliv_h = 2.8 * cm
    draw_deliverables_card(
        c,
        content_x,
        y_cursor - deliv_h,
        content_w,
        deliv_h,
        title="LIVRABLES VALIDÉS À L'ISSUE DU TEMPS 1 (COMPRENDRE) :",
        items=[
            "Profil MBTI® complet et analyse d'impact environnemental",
            "Cartographie de vos énergies de travail et facteurs d'usure",
            "Seuil de sécurité financière (les 4 seuils clés pour arbitrer vos choix)",
        ],
    )

    c.showPage()
