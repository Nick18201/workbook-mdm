from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from .common import setup_programme_page


def create_programme_page_projets(c):
    """
    Page 6 : Les trois projets auxquels mène le bilan (Reconversion, Création/reprise, Évolution interne).
    Remplacement des anciennes cartes de développement personnel par l'orientation résolument 'passage à l'action'.
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Bénéfices & Trajectoires",
        subtitle="Les trois projets professionnels auxquels mène le bilan",
        page_num=6,
        total_pages=8,
        topic="Projets et trajectoires",
    )

    # 1. Chapeau de positionnement
    txt_chapeau = (
        "À l'opposé des approches théoriques de développement personnel, notre accompagnement "
        "est résolument orienté vers <b>le passage à l'action, l'arbitrage réaliste et la confrontation au terrain</b>. "
        "Chaque parcours converge vers l'un des trois projets d'aboutissement ci-dessous :"
    )
    style_chapeau = ParagraphStyle(
        "ProjetsChapeau",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.0,
        leading=13.2,
        textColor=colors.HexColor("#374151"),
    )
    p_chap = Paragraph(txt_chapeau, style_chapeau)
    p_chap.wrap(content_w, 2.5 * cm)
    p_chap.drawOn(c, content_x, y_cursor - p_chap.height)
    y_cursor -= p_chap.height + 0.60 * cm

    # 2. Les trois projets
    projets = [
        {
            "tag": "TRAJECTOIRE 1",
            "title": "Reconversion et bifurcation",
            "audience": "Pour changer de secteur, de fonction ou d'environnement de travail.",
            "points": [
                ("Sécurité financière", "vos droits (indemnités, Transitions Pro, maintien de salaire)."),
                ("Formation", "les seules formations courtes utiles, finançables CPF."),
                ("Terrain", "enquêtes et immersions auprès de personnes en poste."),
                ("Candidature", "CV de bifurcation, posture et récit d'entretien convaincant."),
            ],
            "deliverable": "Plan d'action sécurisé et enquêtes validées",
            "color_tag": PDFStyle.COLOR_ACCENT_RED,
        },
        {
            "tag": "TRAJECTOIRE 2",
            "title": "Création et reprise d'entreprise",
            "audience": "Pour lancer une activité indépendante ou reprendre une entreprise existante.",
            "points": [
                ("Modèle économique", "seuil de rentabilité calculé face à votre minimum vital."),
                ("Offre", "une première offre pilote testable sur le terrain sous 15 jours."),
                ("Posture", "fixer vos tarifs avec légitimité, poser vos limites."),
                ("Lancement", "choix du statut juridique, dispositifs ACRE/ARCE, premiers clients."),
            ],
            "deliverable": "Modèle passé au crash-test et plan de lancement opérationnel",
            "color_tag": PDFStyle.COLOR_ACCENT_BLUE,
        },
        {
            "tag": "TRAJECTOIRE 3",
            "title": "Évolution interne & Repositionnement",
            "audience": "Pour ne pas tout plaquer, mais refuser de continuer de la même manière.",
            "points": [
                ("Travail empêché", "repérer précisément ce qui bloque pour redéfinir votre poste."),
                ("Négociation", "un argumentaire solide pour l'entretien annuel ou la mobilité interne."),
                ("Limites", "protéger votre charge mentale et rééquilibrer vos horaires."),
                ("Pouvoir d'agir", "reprendre durablement la main de l'intérieur."),
            ],
            "deliverable": "Stratégie de repositionnement interne et plan de négociation",
            "color_tag": colors.HexColor("#0D9488"),  # Teal élégant
        },
    ]

    card_h = 6.2 * cm
    gap = 0.45 * cm

    style_pt = ParagraphStyle(
        "ProjPt",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.3,
        leading=11.6,
        textColor=colors.HexColor("#374151"),
    )

    for p in projets:
        cy = y_cursor - card_h

        c.saveState()
        # Fond de carte
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.setStrokeColor(colors.HexColor("#E5E7EB"))
        c.setLineWidth(0.8)
        c.roundRect(content_x, cy, content_w, card_h, 6, fill=1, stroke=1)

        # Liseré gauche coloré
        c.setFillColor(p["color_tag"])
        c.roundRect(content_x, cy, 0.45 * cm, card_h, 2, fill=1, stroke=0)

        inner_x = content_x + 0.85 * cm
        inner_w = content_w - 1.25 * cm

        # Tag + Titre
        c.setFont(PDFStyle.FONT_TITLE, 7.8)
        c.setFillColor(p["color_tag"])
        c.drawString(inner_x, cy + card_h - 0.60 * cm, p["tag"])

        c.setFont(PDFStyle.FONT_TITLE, 11.5)
        c.setFillColor(colors.HexColor("#111827"))
        c.drawString(inner_x + 3.2 * cm, cy + card_h - 0.60 * cm, p["title"])

        # Audience ("Pour qui")
        c.setFont(PDFStyle.FONT_ITALIC, 8.5)
        c.setFillColor(colors.HexColor("#4B5563"))
        c.drawString(inner_x, cy + card_h - 1.05 * cm, p["audience"])

        # Ligne discrète
        c.setStrokeColor(colors.HexColor("#F3F4F6"))
        c.setLineWidth(0.6)
        c.line(inner_x, cy + card_h - 1.25 * cm, content_x + content_w - 0.5 * cm, cy + card_h - 1.25 * cm)

        # Les 4 points en grille 2x2
        col_w = (inner_w - 0.5 * cm) / 2.0
        pt_y_top = cy + card_h - 1.55 * cm

        # Point 1 (Gauche haut)
        txt1 = f"• <b>{p['points'][0][0]} :</b> {p['points'][0][1]}"
        p1 = Paragraph(txt1, style_pt)
        p1.wrap(col_w, 1.3 * cm)
        p1.drawOn(c, inner_x, pt_y_top - p1.height)

        # Point 2 (Droite haut)
        txt2 = f"• <b>{p['points'][1][0]} :</b> {p['points'][1][1]}"
        p2 = Paragraph(txt2, style_pt)
        p2.wrap(col_w, 1.3 * cm)
        p2.drawOn(c, inner_x + col_w + 0.5 * cm, pt_y_top - p2.height)

        pt_y_bot = pt_y_top - 1.25 * cm

        # Point 3 (Gauche bas)
        txt3 = f"• <b>{p['points'][2][0]} :</b> {p['points'][2][1]}"
        p3 = Paragraph(txt3, style_pt)
        p3.wrap(col_w, 1.3 * cm)
        p3.drawOn(c, inner_x, pt_y_bot - p3.height)

        # Point 4 (Droite bas)
        txt4 = f"• <b>{p['points'][3][0]} :</b> {p['points'][3][1]}"
        p4 = Paragraph(txt4, style_pt)
        p4.wrap(col_w, 1.3 * cm)
        p4.drawOn(c, inner_x + col_w + 0.5 * cm, pt_y_bot - p4.height)

        # Livrable clé en bas de carte
        deliv_box_y = cy + 0.35 * cm
        deliv_box_h = 0.80 * cm
        c.setFillColor(colors.HexColor("#F9FAFB"))
        c.setStrokeColor(colors.HexColor("#E5E7EB"))
        c.roundRect(inner_x, deliv_box_y, inner_w, deliv_box_h, 4, fill=1, stroke=1)

        c.setFont(PDFStyle.FONT_TITLE, 8.2)
        c.setFillColor(p["color_tag"])
        c.drawString(inner_x + 0.3 * cm, deliv_box_y + 0.26 * cm, "🎯 LIVRABLE CLÉ :")

        c.setFont(PDFStyle.FONT_BODY, 8.2)
        c.setFillColor(colors.HexColor("#1F2937"))
        c.drawString(inner_x + 3.3 * cm, deliv_box_y + 0.26 * cm, p["deliverable"])

        c.restoreState()
        y_cursor -= card_h + gap

    c.showPage()
