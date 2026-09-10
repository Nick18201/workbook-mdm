from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.components import draw_title, TitleStyle, cached_image_reader
from .common import (
    setup_workbook_programme_page,
    get_workbook_styles,
)


def create_programme_page_8(c):
    """Page 8 : 6. Accès au Cabinet & Modalités d'Accueil."""
    text_x, target_width, y_cursor = setup_workbook_programme_page(
        c, part_title="ACCÈS AU CABINET"
    )
    styles = get_workbook_styles()

    # -------------------------------------------------------------------------
    # 1. TITRE H1 : 6. ACCÈS AU CABINET & MODALITÉS D'ACCUEIL
    # -------------------------------------------------------------------------
    y_cursor = draw_title(
        c,
        "6. Accès au Cabinet & Modalités d'Accueil",
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
        "Situation géographique, accès multimodal et commodités à La Chapelle-sur-Erdre",
    )
    y_cursor -= 0.75 * cm

    # -------------------------------------------------------------------------
    # 2. CARTE COORDONNÉES & TRANSPORTS (Aérée)
    # -------------------------------------------------------------------------
    card_info_h = 5.2 * cm
    pad_x = 0.8 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_FIELD_BG)
    c.setStrokeColor(colors.HexColor("#D2D8FA"))
    c.setLineWidth(0.8)
    c.roundRect(
        text_x, y_cursor - card_info_h, target_width, card_info_h, 8, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_TITLE, 10.5)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.65 * cm,
        "Adresse du cabinet : Centre Attitude (1er étage à droite, au sein de l’Espace Missana)",
    )

    c.setFont(PDFStyle.FONT_BODY, 9.2)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(
        text_x + pad_x,
        y_cursor - 1.05 * cm,
        "📍 60 rue du Leinster, 44240 La Chapelle-sur-Erdre",
    )

    # Séparation horizontale discrète
    c.setStrokeColor(colors.HexColor("#D8DCFA"))
    c.setLineWidth(0.6)
    c.line(
        text_x + pad_x,
        y_cursor - 1.35 * cm,
        text_x + target_width - pad_x,
        y_cursor - 1.35 * cm,
    )

    style_transp = ParagraphStyle(
        "TranspWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=8.8,
        leading=13.0,
        textColor=colors.HexColor("#222222"),
    )

    col_w = (target_width - 2 * pad_x - 0.8 * cm) / 2.0

    txt_transp1 = (
        "· <b>À vélo :</b> à 30 min du centre-ville de Nantes le long de l'Erdre. Parking vélo sécurisé disponible sur place.<br/><br/>"
        "· <b>En transports en commun :</b><br/>"
        "  - <b>Bus 86 :</b> arrêt <i>Capellia</i> à 5 min à pied.<br/>"
        "  - <b>Tram-train (Nantes - Châteaubriant) :</b> arrêt <i>Erdre Active</i> à 10 min à pied."
    )
    p_transp1 = Paragraph(txt_transp1, style_transp)
    p_transp1.wrap(col_w, 3.5 * cm)
    p_transp1.drawOn(c, text_x + pad_x, y_cursor - 1.55 * cm - p_transp1.height)

    # Ligne verticale de séparation
    sep_x = text_x + pad_x + col_w + 0.4 * cm
    c.line(
        sep_x,
        y_cursor - 1.45 * cm,
        sep_x,
        y_cursor - card_info_h + 0.40 * cm,
    )

    txt_transp2 = (
        "· <b>En voiture :</b> accès direct depuis le périphérique nord de Nantes.<br/><br/>"
        "· <b>Stationnement & commodités :</b><br/>"
        "  - Parking gratuit réservé aux visiteurs.<br/>"
        "  - <b>Place PMR dédiée</b> au pied du bâtiment.<br/>"
        "  - Borne de recharge pour véhicules électriques."
    )
    p_transp2 = Paragraph(txt_transp2, style_transp)
    p_transp2.wrap(col_w, 3.5 * cm)
    p_transp2.drawOn(c, sep_x + 0.4 * cm, y_cursor - 1.55 * cm - p_transp2.height)

    c.restoreState()
    y_cursor -= card_info_h + 0.80 * cm

    # -------------------------------------------------------------------------
    # 3. DEUX IMAGES CÔTE À CÔTE (PLAN D'ACCÈS & VUE AÉRIENNE PARKING PMR)
    # -------------------------------------------------------------------------
    img_gap = 0.6 * cm
    img_w = (target_width - img_gap) / 2.0
    img_h = 5.3 * cm
    box_img_h = 6.4 * cm

    images_data = [
        {
            "path": PDFStyle.PATH_PLAN_ACCES,
            "legende": "Plan de situation — Espace Missana",
        },
        {
            "path": PDFStyle.PATH_PARKING_PMR,
            "legende": "Vue aérienne — Accès parking & place PMR",
        },
    ]

    for i, item in enumerate(images_data):
        ix = text_x + i * (img_w + img_gap)
        iy = y_cursor - box_img_h

        c.saveState()
        # Cadre blanc avec bordure soignée
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.setStrokeColor(colors.HexColor("#CBD0FA"))
        c.setLineWidth(0.8)
        c.roundRect(ix, iy, img_w, box_img_h, 6, fill=1, stroke=1)

        # Dessin de l'image
        try:
            reader = cached_image_reader(item["path"])
            if reader:
                pad = 0.25 * cm
                draw_w = img_w - 2 * pad
                draw_h = img_h - pad
                draw_x = ix + pad
                draw_y = iy + box_img_h - pad - draw_h
                c.drawImage(
                    reader,
                    draw_x,
                    draw_y,
                    width=draw_w,
                    height=draw_h,
                    preserveAspectRatio=True,
                    anchor="c",
                )
        except Exception:
            c.setFont(PDFStyle.FONT_ITALIC, 8.0)
            c.setFillColor(colors.HexColor("#888888"))
            c.drawCentredString(ix + img_w / 2.0, iy + box_img_h / 2.0, f"Image: {item['path']}")

        # Légende sous l'image
        c.setFont(PDFStyle.FONT_TITLE, 8.0)
        c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
        c.drawCentredString(ix + img_w / 2.0, iy + 0.32 * cm, item["legende"])

        c.restoreState()

    y_cursor -= box_img_h + 1.0 * cm

    # -------------------------------------------------------------------------
    # 4. ENCADRÉ CONTACT & ACCUEIL (Aéré)
    # -------------------------------------------------------------------------
    contact_h = 4.2 * cm
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_BG_NUDE)
    c.setStrokeColor(PDFStyle.COLOR_ACCENT_RED)
    c.setLineWidth(1.2)
    c.roundRect(
        text_x, y_cursor - contact_h, target_width, contact_h, 8, fill=1, stroke=1
    )

    c.setFont(PDFStyle.FONT_BRANDING, 13.0)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(
        text_x + pad_x,
        y_cursor - 0.75 * cm,
        "Prendre rendez-vous & poser vos questions",
    )

    c.setFont(PDFStyle.FONT_TITLE, 9.8)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(
        text_x + pad_x,
        y_cursor - 1.30 * cm,
        "Premier échange d'orientation offert (30 à 45 min) en présentiel ou en visio.",
    )

    style_contact_txt = ParagraphStyle(
        "ContactTxtWk",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9.2,
        leading=14.0,
        textColor=colors.HexColor("#222222"),
    )
    txt_ct = (
        "<b>Lysiane BRAND</b> — Psychologue du travail & Consultante en bilan de compétences<br/>"
        "📞 <b>Téléphone :</b> 06 74 55 20 22 &nbsp;&nbsp;|&nbsp;&nbsp; "
        "✉️ <b>Email :</b> lysiane.brand@gmail.com &nbsp;&nbsp;|&nbsp;&nbsp; "
        "🌐 <b>Site web :</b> margedemanoeuvre.fr"
    )
    p_ct = Paragraph(txt_ct, style_contact_txt)
    p_ct.wrap(target_width - 2 * pad_x, 2.2 * cm)
    p_ct.drawOn(c, text_x + pad_x, y_cursor - contact_h + 0.40 * cm)

    c.restoreState()

    c.showPage()
