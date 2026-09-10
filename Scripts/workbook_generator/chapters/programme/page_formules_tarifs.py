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


def create_programme_page_6(c):
    """Page 6 : 4. Les 3 Formules de Bilans & Tarifs."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="FORMULES & TARIFS"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE H1 : 4. LES 3 FORMULES DE BILANS & TARIFS
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "4. Les 3 Formules de Bilans & Tarifs",
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
        "Des formules adaptées à votre niveau de maturité, avec tests et livret inclus",
    )
    y_cursor -= 0.75 * cm

    # -------------------------------------------------------------------------
    # 2. BANNIÈRE INFORMATIVE INCLUSIONS (Aérée & Centrée)
    # -------------------------------------------------------------------------
    inclus_pad_x = 0.85 * cm
    inclus_inner_w = target_width - 2 * inclus_pad_x

    style_inclus = ParagraphStyle(
        "InclusWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.2,
        leading=13.8,
        textColor=PDFStyle.COLOR_ACCENT_BLUE,
    )
    txt_inclus = (
        "<b>🎁 TOUS LES TARIFS INCLUENT :</b> la passation en ligne du questionnaire <b>MBTI</b>, "
        "l'inventaire d'intérêts professionnels <b>Hexa3D</b>, l'accès illimité au <b>site Notion ressource</b> "
        "et le <b>livret d'accompagnement</b> de réflexion."
    )
    p_inclus = Paragraph(txt_inclus, style_inclus)
    p_inclus.wrap(inclus_inner_w, 4.0 * cm)

    # Hauteur avec padding vertical de 0.55 cm minimum
    inclus_h = max(2.3 * cm, p_inclus.height + 1.10 * cm)
    pad_y = (inclus_h - p_inclus.height) / 2.0

    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(
        text_x, y_cursor - inclus_h, target_width, inclus_h, 8, fill=1, stroke=1
    )

    p_inclus.drawOn(c, text_x + inclus_pad_x, y_cursor - pad_y - p_inclus.height)
    c.restoreState()

    y_cursor -= inclus_h + 0.90 * cm

    # -------------------------------------------------------------------------
    # 3. LES 3 GRANDES CARTES TARIFAIRES (Aérées)
    # -------------------------------------------------------------------------
    card_gap = 0.40 * cm
    card_tarifs_w = (target_width - 2 * card_gap) / 3.0
    card_tarifs_h = 8.6 * cm

    formats = [
        {
            "titre": "L’impulsion",
            "format": "8 séances (12h)",
            "heures": "+ travail personnel",
            "prix": "1 600 € TTC",
            "tag": "PROJET CIBLÉ",
            "tag_bg": "#EAEBFE",
            "tag_col": "#2F2EFA",
            "desc": "Idéal si vous avez <b>déjà une idée de projet ou une direction</b>, et souhaitez la valider et structurer rapidement votre plan d'action.",
        },
        {
            "titre": "La trajectoire",
            "format": "10 séances (15h)",
            "heures": "+ travail personnel",
            "prix": "1 850 € TTC",
            "tag": "LE PLUS CHOISI",
            "tag_bg": "#FFEAE8",
            "tag_col": "#FF4D4D",
            "desc": "<b>Le format le plus choisi :</b> il permet de mener un travail complet d'introspection et d'explorer sereinement plusieurs pistes professionnelles.",
        },
        {
            "titre": "L’amplitude",
            "format": "12 séances (18h)",
            "heures": "+ travail personnel",
            "prix": "2 220 € TTC",
            "tag": "ACCOMPAGNEMENT RENFORCÉ",
            "tag_bg": "#EAEBFE",
            "tag_col": "#2F2EFA",
            "desc": "Recommandé si vous êtes en <b>perte totale de repères</b>, en situation d'épuisement professionnel (burn-out) ou face à une reconversion radicale.",
        },
    ]

    style_format_desc = ParagraphStyle(
        "FormatDescWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=13.0,
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

        # 1. Badge / Tag centré
        tag_w = c.stringWidth(fmt["tag"], PDFStyle.FONT_TITLE, 7.4) + 0.50 * cm
        tag_h = 0.46 * cm
        tag_x = cx + (card_tarifs_w - tag_w) / 2.0
        tag_y = cy + card_tarifs_h - 0.75 * cm

        c.setFillColor(colors.HexColor(fmt["tag_bg"]))
        c.setStrokeColor(colors.HexColor(fmt["tag_col"]))
        c.setLineWidth(0.8)
        c.roundRect(tag_x, tag_y, tag_w, tag_h, tag_h / 2.0, fill=1, stroke=1)

        c.setFont(PDFStyle.FONT_TITLE, 7.4)
        c.setFillColor(colors.HexColor(fmt["tag_col"]))
        c.drawCentredString(tag_x + tag_w / 2.0, tag_y + 0.12 * cm, fmt["tag"])

        # 2. Nom de formule centré
        c.setFont(PDFStyle.FONT_BRANDING, 13.0)
        c.setFillColor(
            PDFStyle.COLOR_ACCENT_RED if is_populaire else PDFStyle.COLOR_ACCENT_BLUE
        )
        c.drawCentredString(
            cx + card_tarifs_w / 2.0, cy + card_tarifs_h - 1.55 * cm, f"Bilan - {fmt['titre']}"
        )

        # 3. Format & volume
        c.setFont(PDFStyle.FONT_TITLE, 9.5)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawCentredString(
            cx + card_tarifs_w / 2.0, cy + card_tarifs_h - 2.05 * cm, fmt["format"]
        )

        c.setFont(PDFStyle.FONT_BODY, 8.2)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawCentredString(
            cx + card_tarifs_w / 2.0, cy + card_tarifs_h - 2.45 * cm, fmt["heures"]
        )

        # 4. Prix centré en grand
        c.setFont(PDFStyle.FONT_BRANDING, 15.0)
        c.setFillColor(
            PDFStyle.COLOR_ACCENT_RED if is_populaire else PDFStyle.COLOR_ACCENT_BLUE
        )
        c.drawCentredString(
            cx + card_tarifs_w / 2.0, cy + card_tarifs_h - 3.25 * cm, fmt["prix"]
        )

        # 5. Ligne de séparation
        c.setStrokeColor(colors.HexColor("#D4D8F5"))
        c.setLineWidth(0.6)
        c.line(
            cx + 0.40 * cm,
            cy + card_tarifs_h - 3.65 * cm,
            cx + card_tarifs_w - 0.40 * cm,
            cy + card_tarifs_h - 3.65 * cm,
        )

        # 6. Description du profil avec padding intérieur
        p_desc = Paragraph(fmt["desc"], style_format_desc)
        p_desc.wrap(card_tarifs_w - 0.8 * cm, card_tarifs_h - 4.2 * cm)
        p_desc.drawOn(c, cx + 0.40 * cm, cy + card_tarifs_h - 4.05 * cm - p_desc.height)

        c.restoreState()

    y_cursor -= card_tarifs_h + 0.85 * cm

    # -------------------------------------------------------------------------
    # 4. RAPPEL DU PREMIER RDV GRATUIT
    # -------------------------------------------------------------------------
    c.setFont(PDFStyle.FONT_ITALIC, 9.2)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawCentredString(
        text_x + target_width / 2.0,
        y_cursor,
        "Premier échange d'information gratuit et sans engagement (30 à 45 min) pour définir votre formule.",
    )

    c.showPage()
