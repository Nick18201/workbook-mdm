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


def create_programme_page_3(c):
    """Page 3 : 2. Organisation Pratique & 3. Les 3 Formats de Bilans & Tarifs."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="ORGANISATION & TARIFS"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE H1 : 2. ORGANISATION PRATIQUE & OUTILS
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "2. Organisation Pratique & Outils",
        pos=(text_x, y_cursor),
        available_width=target_width,
        style=TitleStyle(size=18, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    y_cursor -= 0.20 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Un accompagnement individuel, agile et personnalisé entre chaque séance",
    )
    y_cursor -= 0.65 * cm

    # -------------------------------------------------------------------------
    # 2. DEUX BLOCS ORGANISATION (LES SÉANCES & ENTRE LES SÉANCES)
    # -------------------------------------------------------------------------
    orga_card_h = 4.5 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(
        text_x, y_cursor - orga_card_h, target_width, orga_card_h, 8, fill=1, stroke=1
    )

    style_orga_bullet = ParagraphStyle(
        "OrgaBullet",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=12.6,
        textColor=colors.HexColor("#222222"),
    )

    # Colonne Gauche : Les séances
    col_w = (target_width - 1.2 * cm) / 2.0
    c.setFont(PDFStyle.FONT_TITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(text_x + 0.5 * cm, y_cursor - 0.60 * cm, "Les séances :")

    txt_seances = (
        "· <b>100% individuelles</b>, avec un consultant dédié tout au long du parcours.<br/>"
        "· <b>Format mixte :</b> présentiel et/ou distanciel selon vos besoins.<br/>"
        "· <b>Durée des séances :</b> 1h30 à 2h, espacées de 1 à 2 semaines pour laisser décanter et avancer entre les rendez-vous."
    )
    p_seances = Paragraph(txt_seances, style_orga_bullet)
    p_seances.wrap(col_w, 3.2 * cm)
    p_seances.drawOn(c, text_x + 0.5 * cm, y_cursor - 0.78 * cm - p_seances.height)

    # Ligne verticale de séparation interne
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(
        text_x + col_w + 0.6 * cm,
        y_cursor - 0.40 * cm,
        text_x + col_w + 0.6 * cm,
        y_cursor - orga_card_h + 0.40 * cm,
    )

    # Colonne Droite : Entre les séances
    c.setFont(PDFStyle.FONT_TITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x + col_w + 0.9 * cm, y_cursor - 0.60 * cm, "Entre les séances :"
    )

    txt_entre = (
        "· <b>Accès à une plateforme collaborative dédiée.</b><br/>"
        "· <b>Exercices guidés</b>, tests de personnalité et grilles d'analyse.<br/>"
        "· <b>Outils d'aide à la décision</b> et supports méthodologiques exclusifs.<br/>"
        "· <b>Échanges continus</b> avec votre consultant par messagerie."
    )
    p_entre = Paragraph(txt_entre, style_orga_bullet)
    p_entre.wrap(col_w, 3.2 * cm)
    p_entre.drawOn(
        c, text_x + col_w + 0.9 * cm, y_cursor - 0.78 * cm - p_entre.height
    )

    c.restoreState()
    # Espace généreux entre la carte d'organisation et la section suivante
    y_cursor -= orga_card_h + 0.90 * cm

    # -------------------------------------------------------------------------
    # 3. TITRE H1 : 3. LES 3 FORMATS DE BILANS & TARIFS
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "3. Les 3 Formats de Bilans & Tarifs",
        pos=(text_x, y_cursor),
        available_width=target_width,
        style=TitleStyle(size=18, color=PDFStyle.COLOR_ACCENT_BLUE),
    )
    y_cursor -= 0.20 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x,
        y_cursor,
        "Des parcours adaptés à votre situation, vos enjeux et votre niveau d'exploration",
    )
    y_cursor -= 0.70 * cm

    # -------------------------------------------------------------------------
    # 4. LES 3 GRANDES CARTES TARIFAIRES (Sans chevauchement)
    # -------------------------------------------------------------------------
    card_gap = 0.35 * cm
    card_tarifs_w = (target_width - 2 * card_gap) / 3.0
    card_tarifs_h = 6.6 * cm

    formats = [
        {
            "titre": "Format 8 séances",
            "heures": "12h d'entretiens individuels",
            "prix": "1 680 € TTC",
            "tag": "PROJET CIBLÉ",
            "tag_bg": "#EAEBFE",
            "tag_col": "#2F2EFA",
            "desc": "Idéal si vous avez <b>déjà une idée de projet ou une direction</b>, et souhaitez la valider et structurer rapidement votre plan d'action.",
        },
        {
            "titre": "Format 10 séances",
            "heures": "15h d'entretiens individuels",
            "prix": "2 100 € TTC",
            "tag": "LE PLUS CHOISI",
            "tag_bg": "#FFEAE8",
            "tag_col": "#FF4D4D",
            "desc": "<b>Le format le plus choisi :</b> il permet de mener un travail complet d'introspection et d'explorer sereinement plusieurs pistes professionnelles.",
        },
        {
            "titre": "Format 12 séances",
            "heures": "18h d'entretiens individuels",
            "prix": "2 520 € TTC",
            "tag": "SUIVI APPROFONDI",
            "tag_bg": "#EAEBFE",
            "tag_col": "#2F2EFA",
            "desc": "Recommandé si vous êtes en <b>perte totale de repères</b>, en situation d'épuisement professionnel (burn-out) ou face à une reconversion radicale.",
        },
    ]

    style_format_desc = ParagraphStyle(
        "FormatDescWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.6,
        leading=12.2,
        textColor=colors.HexColor("#222222"),
    )

    for i, fmt in enumerate(formats):
        cx = text_x + i * (card_tarifs_w + card_gap)
        cy = y_cursor - card_tarifs_h

        is_populaire = i == 1
        border_col = (
            PDFStyle.COLOR_ACCENT_RED
            if is_populaire
            else colors.HexColor("#CBD0FA")
        )
        bg_col = (
            colors.HexColor("#FFF8F6")
            if is_populaire
            else PDFStyle.COLOR_FIELD_BG
        )

        c.saveState()
        # Fond de la carte
        c.setFillColor(bg_col)
        c.setStrokeColor(border_col)
        c.setLineWidth(1.4 if is_populaire else 0.8)
        c.roundRect(cx, cy, card_tarifs_w, card_tarifs_h, 8, fill=1, stroke=1)

        # 1. Badge / Tag centré tout en haut de la carte
        tag_w = c.stringWidth(fmt["tag"], PDFStyle.FONT_TITLE, 7.5) + 0.5 * cm
        tag_h = 0.44 * cm
        tag_x = cx + (card_tarifs_w - tag_w) / 2.0
        tag_y = cy + card_tarifs_h - 0.65 * cm

        c.setFillColor(colors.HexColor(fmt["tag_bg"]))
        c.setStrokeColor(colors.HexColor(fmt["tag_col"]))
        c.setLineWidth(0.8)
        c.roundRect(tag_x, tag_y, tag_w, tag_h, tag_h / 2.0, fill=1, stroke=1)

        c.setFont(PDFStyle.FONT_TITLE, 7.5)
        c.setFillColor(colors.HexColor(fmt["tag_col"]))
        c.drawCentredString(tag_x + tag_w / 2.0, tag_y + 0.10 * cm, fmt["tag"])

        # 2. Titre du format centré sous le badge
        c.setFont(PDFStyle.FONT_TITLE, 11)
        c.setFillColor(
            PDFStyle.COLOR_ACCENT_RED if is_populaire else PDFStyle.COLOR_ACCENT_BLUE
        )
        c.drawCentredString(
            cx + card_tarifs_w / 2.0, cy + card_tarifs_h - 1.30 * cm, fmt["titre"]
        )

        # 3. Volume d'heures centré
        c.setFont(PDFStyle.FONT_BODY, 8.2)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawCentredString(
            cx + card_tarifs_w / 2.0, cy + card_tarifs_h - 1.72 * cm, fmt["heures"]
        )

        # 4. Prix centré en grand
        c.setFont(PDFStyle.FONT_BRANDING, 14.5)
        c.setFillColor(
            PDFStyle.COLOR_ACCENT_RED if is_populaire else PDFStyle.COLOR_ACCENT_BLUE
        )
        c.drawCentredString(
            cx + card_tarifs_w / 2.0, cy + card_tarifs_h - 2.35 * cm, fmt["prix"]
        )

        # 5. Ligne de séparation
        c.setStrokeColor(colors.HexColor("#D4D8F5"))
        c.setLineWidth(0.6)
        c.line(
            cx + 0.35 * cm,
            cy + card_tarifs_h - 2.68 * cm,
            cx + card_tarifs_w - 0.35 * cm,
            cy + card_tarifs_h - 2.68 * cm,
        )

        # 6. Description du profil
        p_desc = Paragraph(fmt["desc"], style_format_desc)
        p_desc.wrap(card_tarifs_w - 0.7 * cm, card_tarifs_h - 2.8 * cm)
        p_desc.drawOn(c, cx + 0.35 * cm, cy + card_tarifs_h - 2.90 * cm - p_desc.height)

        c.restoreState()

    c.showPage()
