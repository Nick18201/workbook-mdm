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


def create_programme_page_7(c):
    """Page 7 : 5. Financement, Modalités d'Accès & Suivi des Résultats."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="FINANCEMENT & MODALITÉS"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE H1 : 5. FINANCEMENT, ACCESSIBILITÉ & SUIVI DES RÉSULTATS
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "5. Financement, Modalités d'Accès & Suivi",
        pos=(text_x, y_cursor),
        available_width=target_width,
        style=TitleStyle(size=18, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    y_cursor -= 0.30 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Dispositifs de prise en charge, accueil inclusif et suivi de votre parcours",
    )
    y_cursor -= 0.75 * cm

    pad_x = 0.8 * cm
    col_w = (target_width - 2 * pad_x - 0.8 * cm) / 2.0

    style_item = ParagraphStyle(
        "FinItemWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.7,
        leading=12.6,
        textColor=colors.HexColor("#222222"),
    )

    # -------------------------------------------------------------------------
    # 2. CARTE 1 : POSSIBILITÉS DE FINANCEMENT (Aérée)
    # -------------------------------------------------------------------------
    card1_h = 6.4 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(text_x, y_cursor - card1_h, target_width, card1_h, 8, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.70 * cm,
        "Possibilités de financement :",
    )

    txt_fin_col1 = (
        "· <b>CPF (Compte Personnel de Formation) :</b> Mobilisable pour les salariés du secteur privé, agents publics et chefs d'entreprise via l'application officielle "
        "<font color='#0066CC'><u>moncompteformation.gouv.fr</u></font> (organisme certifié Qualiopi).<br/><br/>"
        "· <b>Plan de Développement des Compétences :</b> Prise en charge directe par votre employeur (entreprises, associations, collectivités)."
    )
    p_fin1 = Paragraph(txt_fin_col1, style_item)
    p_fin1.wrap(col_w, 5.0 * cm)
    p_fin1.drawOn(c, text_x + pad_x, y_cursor - 1.05 * cm - p_fin1.height)

    # Ligne verticale de séparation
    sep1_x = text_x + pad_x + col_w + 0.4 * cm
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(
        sep1_x,
        y_cursor - 0.50 * cm,
        sep1_x,
        y_cursor - card1_h + 0.50 * cm,
    )

    txt_fin_col2 = (
        "· <b>France Travail (Pôle Emploi) :</b> Financement mobilisable via l'Aide Individuelle à la Formation (AIF).<br/><br/>"
        "· <b>Financement personnel :</b> Règlement direct sur fonds propres avec facilités de paiement échelonné.<br/><br/>"
        "· <b>Autres dispositifs :</b> AGEFIPH (situation de handicap), service social CARSAT, aides régionales ou départementales."
    )
    p_fin2 = Paragraph(txt_fin_col2, style_item)
    p_fin2.wrap(col_w, 5.0 * cm)
    p_fin2.drawOn(c, sep1_x + 0.4 * cm, y_cursor - 1.05 * cm - p_fin2.height)

    c.restoreState()
    y_cursor -= card1_h + 0.75 * cm

    # -------------------------------------------------------------------------
    # 3. CARTE 2 : DÉLAIS, MODALITÉS D'ACCÈS & ACCESSIBILITÉ HANDICAP (Aérée)
    # -------------------------------------------------------------------------
    card2_h = 7.6 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(text_x, y_cursor - card2_h, target_width, card2_h, 8, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.70 * cm,
        "Délais, modalités d'accès & accessibilité handicap :",
    )

    txt_acc_col1 = (
        "· <b>Public & Pré-requis :</b> Aucun pré-requis de diplôme, de qualification ou de niveau d'étude. Accessible à toute personne active (salariés du privé et public, demandeurs d'emploi, indépendants).<br/><br/>"
        "· <b>Formats flexibles :</b> Entretiens réalisables en présentiel au cabinet ou à distance en visioconférence.<br/><br/>"
        "· <b>Délais d'accès :</b> Démarrage moyen sous 14 jours ouvrés après contractualisation et validation du dossier."
    )
    p_acc1 = Paragraph(txt_acc_col1, style_item)
    p_acc1.wrap(col_w, 6.2 * cm)
    p_acc1.drawOn(c, text_x + pad_x, y_cursor - 1.05 * cm - p_acc1.height)

    # Ligne verticale de séparation
    sep2_x = text_x + pad_x + col_w + 0.4 * cm
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(
        sep2_x,
        y_cursor - 0.50 * cm,
        sep2_x,
        y_cursor - card2_h + 0.50 * cm,
    )

    txt_acc_col2 = (
        "· <b>Inclusion & Handicap :</b> L'accompagnement, les rythmes et les exercices s'adaptent aux situations individuelles.<br/><br/>"
        "· <b>Accessibilité PMR :</b> Le cabinet est entièrement accessible aux personnes à mobilité réduite (ascenseur, place PMR dédiée).<br/><br/>"
        "· <b>Livret d'accueil handicap :</b> Communiqué sur demande. En cas de besoin spécifique non couvert, orientation vers les partenaires experts de notre réseau."
    )
    p_acc2 = Paragraph(txt_acc_col2, style_item)
    p_acc2.wrap(col_w, 6.2 * cm)
    p_acc2.drawOn(c, sep2_x + 0.4 * cm, y_cursor - 1.05 * cm - p_acc2.height)

    c.restoreState()
    y_cursor -= card2_h + 0.75 * cm

    # -------------------------------------------------------------------------
    # 4. CARTE 3 : MOYENS DE SUIVI DE L'EXÉCUTION & RÉSULTATS (Aérée)
    # -------------------------------------------------------------------------
    card3_h = 5.4 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.0)
    c.roundRect(text_x, y_cursor - card3_h, target_width, card3_h, 8, fill=1, stroke=1)

    c.setFont(PDFStyle.FONT_TITLE, 11)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.70 * cm,
        "Moyens de suivi de l'exécution & évaluation des résultats :",
    )

    txt_sui_col1 = (
        "· <b>Attestations de présence :</b> Émargement régulier tout au long du bilan pour attester de l'assiduité du bénéficiaire.<br/><br/>"
        "· <b>Document de synthèse :</b> Remise d'un document ressource complet et confidentiel, co-construit lors de la phase de conclusion."
    )
    p_sui1 = Paragraph(txt_sui_col1, style_item)
    p_sui1.wrap(col_w, 4.2 * cm)
    p_sui1.drawOn(c, text_x + pad_x, y_cursor - 1.05 * cm - p_sui1.height)

    # Ligne verticale de séparation
    sep3_x = text_x + pad_x + col_w + 0.4 * cm
    c.setStrokeColor(colors.HexColor("#ECCEC6"))
    c.setLineWidth(0.6)
    c.line(
        sep3_x,
        y_cursor - 0.50 * cm,
        sep3_x,
        y_cursor - card3_h + 0.50 * cm,
    )

    txt_sui_col2 = (
        "· <b>Questionnaires de satisfaction :</b> Évaluation à chaud à l'issue du bilan, puis questionnaire d'impact à froid à 6 mois.<br/><br/>"
        "· <b>Entretien de suivi à 6 mois :</b> Rendez-vous individuel d'1h dédié pour faire le point sur l'avancement du projet, les réussites et les freins éventuels."
    )
    p_sui2 = Paragraph(txt_sui_col2, style_item)
    p_sui2.wrap(col_w, 4.2 * cm)
    p_sui2.drawOn(c, sep3_x + 0.4 * cm, y_cursor - 1.05 * cm - p_sui2.height)

    c.restoreState()

    c.showPage()
