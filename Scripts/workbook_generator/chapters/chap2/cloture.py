from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from ...config import PDFStyle
from ...components import (
    draw_page_background,
    draw_side_panel,
    draw_title,
    draw_page_decorations,
)
from ...forms import create_input_field


def create_interview_page(c):
    """
    New Page: Interview avec une personne passionnée (Bonus).
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    new_y = draw_title(
        c, "Interview avec une personne passionnée", pos=(text_x, text_top)
    )

    c.setFont(PDFStyle.FONT_BODY, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(
        text_x,
        new_y - 0.2 * cm,
        "Rencontrez quelqu'un qui a un métier ou une vie qui vous inspire.",
    )

    form = c.acroForm
    y_cursor = new_y - 1.2 * cm

    col1_x = text_x
    col2_x = text_x + 8.0 * cm

    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(col1_x, y_cursor, "Personne interviewée :")
    create_input_field(
        form,
        "interview_nom",
        pos=(col1_x, y_cursor - 0.8 * cm),
        size=(7.0 * cm, 0.6 * cm),
    )

    c.drawString(col2_x, y_cursor, "Son métier / Activité :")
    create_input_field(
        form,
        "interview_metier",
        pos=(col2_x, y_cursor - 0.8 * cm),
        size=(width - col2_x - 1.5 * cm, 0.6 * cm),
    )

    y_cursor -= 2 * cm

    questions = [
        ("Qu'aimez-vous le plus dans ce que vous faites ?", "interview_q1", 2.5 * cm),
        (
            "Quelles sont les difficultés ou contraintes cachées ?",
            "interview_q2",
            2.5 * cm,
        ),
        (
            "Quel conseil donneriez-vous à quelqu'un qui veut se lancer ?",
            "interview_q3",
            2.5 * cm,
        ),
        ("Ce que j'en retiens pour moi (Mon ressenti) :", "interview_q4", 3.5 * cm),
    ]

    for q_text, q_id, q_height in questions:
        c.setFont(PDFStyle.FONT_SUBTITLE, 11)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(text_x, y_cursor, q_text)
        y_cursor -= q_height + 0.4 * cm
        create_input_field(
            form,
            q_id,
            pos=(text_x, y_cursor),
            size=(width - text_x - 1.5 * cm, q_height),
            multiline=True,
        )
        y_cursor -= 0.6 * cm

    draw_page_decorations(c, width, height, part_title="BONUS", x_offset=card_margin)
    c.showPage()
