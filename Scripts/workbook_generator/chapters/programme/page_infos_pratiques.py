from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from .common import setup_programme_page


def create_programme_page_infos_pratiques(c):
    """
    Page 8 : Informations pratiques & Cadre légal (Indicateur 1 Qualiopi).
    - Prérequis : aucun
    - Délais d'accès : échange gratuit 30 min, inscription MonCompteFormation, 14 jours légaux
    - Modalités d'évaluation : questionnaire de satisfaction, entretien de suivi à 6 mois
    - Accessibilité : référent handicap dédié (Nicolas Blum Ferracci)
    - Contact : email et margedemanoeuvre.fr/contact/
    - Confidentialité : synthèse personnelle (art. L. 6313-4 du Code du travail)
    """
    content_x, content_w, y_cursor = setup_programme_page(
        c,
        title="Informations pratiques",
        subtitle="Modalités, délais d'accès et cadre réglementaire (Indicateur 1 Qualiopi)",
        page_num=11,
        total_pages=12,
        topic="Informations pratiques",
    )

    # Grille 2 colonnes x 3 lignes
    col_gap = 0.50 * cm
    col_w = (content_w - col_gap) / 2.0
    row_gap = 0.45 * cm

    cards_data = [
        # Ligne 1
        {
            "row": 0,
            "col": 0,
            "height": 5.9 * cm,
            "title": "PRÉREQUIS",
            "text": (
                "<b>Aucun prérequis</b> de diplôme, de niveau d'études, d'expérience professionnelle "
                "ou de statut n'est exigé.<br/><br/>"
                "Le bilan de compétences est ouvert à toute personne active : salariés du secteur privé, "
                "indépendants, agents publics et demandeurs d'emploi souhaitant faire le point sur leur trajectoire."
            ),
        },
        {
            "row": 0,
            "col": 1,
            "height": 5.9 * cm,
            "title": "DÉLAIS D'ACCÈS",
            "text": (
                "• <b>Premier échange gratuit (30 min en visio) :</b> pour cerner vos attentes et valider l'adéquation.<br/>"
                "• <b>Inscription sur MonCompteFormation :</b> validation en ligne de votre dossier.<br/>"
                "• <b>Délai légal de rétractation :</b> un délai minimal de <b>14 jours ouvrés</b> est obligatoire "
                "entre votre inscription et la 1re séance pédagogique."
            ),
        },
        # Ligne 2
        {
            "row": 1,
            "col": 0,
            "height": 6.8 * cm,
            "title": "MODALITÉS D'ÉVALUATION",
            "text": (
                "• <b>Évaluation continue :</b> validation des livrables et des exercices pratiques à la fin de chaque séance.<br/>"
                "• <b>Questionnaire de satisfaction :</b> évaluation anonyme à chaud en fin de parcours pour mesurer la qualité "
                "de l'accompagnement et l'atteinte de vos objectifs.<br/>"
                "• <b>Entretien individuel de suivi à 6 mois (45 min) :</b> point d'étape sur la concrétisation de vos démarches."
            ),
        },
        {
            "row": 1,
            "col": 1,
            "height": 6.8 * cm,
            "title": "ACCESSIBILITÉ & HANDICAP",
            "text": (
                "Notre démarche s'adapte à chacun : nous adaptons les rythmes, les supports et les formats d'accompagnement.<br/><br/>"
                "Notre <b>référent handicap</b> étudie chaque situation pour organiser les aménagements nécessaires ou vous orienter :<br/><br/>"
                "<b>Nicolas Blum Ferracci</b><br/>"
                "<font name='ZapfDingbats'>✉</font> <b>nicolas.blumferracci@margedemanoeuvre.fr</b>"
            ),
        },
        # Ligne 3
        {
            "row": 2,
            "col": 0,
            "height": 6.4 * cm,
            "title": "CONTACT & INSCRIPTION",
            "text": (
                "Pour poser vos questions, étudier vos possibilités de prise en charge ou convenir d'un premier échange :<br/><br/>"
                "• <b>Email :</b> contact@margedemanoeuvre.fr<br/>"
                "• <b>Contact direct :</b> nicolas.blumferracci@margedemanoeuvre.fr<br/>"
                "• <b>Prise de rendez-vous en ligne :</b><br/>"
                "&nbsp;&nbsp;<b>margedemanoeuvre.fr/contact/</b>"
            ),
        },
        {
            "row": 2,
            "col": 1,
            "height": 6.4 * cm,
            "title": "CONFIDENTIALITÉ & PROPRIÉTÉ",
            "text": (
                "Le document de synthèse officiel co-rédigé <b>n'appartient qu'à vous</b> et ne peut être communiqué "
                "à aucun tiers sans votre accord explicite (art. L. 6313-4 du Code du travail).<br/><br/>"
                "L'ensemble de vos échanges et réflexions est couvert par une <b>obligation stricte de secret et de confidentialité</b>."
            ),
        },
    ]

    style_card = ParagraphStyle(
        "InfoCardText",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.3,
        leading=12.2,
        textColor=colors.HexColor("#374151"),
    )

    # Dessin des cartes
    row_heights = [5.9 * cm, 6.8 * cm, 6.4 * cm]
    current_y = y_cursor

    for r_idx, rh in enumerate(row_heights):
        row_cards = [c_data for c_data in cards_data if c_data["row"] == r_idx]

        for card in row_cards:
            cx = content_x if card["col"] == 0 else content_x + col_w + col_gap
            cy = current_y - rh

            c.saveState()
            # Fond blanc avec bordure discrète
            c.setFillColor(colors.HexColor("#FFFFFF"))
            c.setStrokeColor(colors.HexColor("#E5E7EB"))
            c.setLineWidth(0.8)
            c.roundRect(cx, cy, col_w, rh, 6, fill=1, stroke=1)

            # En-tête de carte avec fond doux
            header_h = 0.95 * cm
            c.setFillColor(colors.HexColor("#F9FAFB"))
            c.roundRect(cx, cy + rh - header_h, col_w, header_h, 6, fill=1, stroke=0)
            c.setStrokeColor(colors.HexColor("#E5E7EB"))
            c.setLineWidth(0.6)
            c.line(cx, cy + rh - header_h, cx + col_w, cy + rh - header_h)

            c.setFont(PDFStyle.FONT_TITLE, 8.8)
            c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
            c.drawString(cx + 0.45 * cm, cy + rh - 0.65 * cm, card["title"])

            # Contenu texte
            p = Paragraph(card["text"], style_card)
            p.wrap(col_w - 0.9 * cm, rh - header_h - 0.5 * cm)
            p.drawOn(c, cx + 0.45 * cm, cy + rh - header_h - p.height - 0.35 * cm)

            c.restoreState()

        current_y -= rh + row_gap

    c.showPage()
