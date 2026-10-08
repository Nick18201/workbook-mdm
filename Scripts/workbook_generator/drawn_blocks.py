"""
Blocks drawn as illustrations, which fill the rest of their page: the life line and the
tree of life of carnet 2. PageLayout.add_life_line / add_tree_of_life place them.
"""

from reportlab.lib.units import cm

from .components import draw_answer_box
from .config import PDFStyle
from .document_builder import document_pastel
from .primitives import (
    draw_annotation,
    draw_disc,
    draw_eyebrow,
    draw_icon_badge,
    draw_paragraph,
    draw_pastel_card,
    draw_rule,
    pastel_cycle,
)


LIFE_LINE_PROMPTS = {"summit": "Ce que j'ai aimé", "valley": "Ce que j'en retiens"}


def draw_life_line(c, x, top, width, nodes, headers, field_prefix):
    """
    The life line, from top down to the bottom margin: a dotted axis, the summits on the
    left and the valleys on the right, each a pastel card with an event line (one written
    line, 0.85 cm) and a box (two handwritten lines, 1.6 cm).
    nodes: [(label, 'summit' | 'valley') or (label, kind, box label), ...]; without a box
    label, LIFE_LINE_PROMPTS. headers: the labels of the two sides.
    """
    center = x + width / 2
    left_header, right_header = (list(headers or []) + ["", ""])[:2]
    draw_eyebrow(c, x, top - 8, left_header, color=PDFStyle.COLOR_BLUE)
    draw_eyebrow(c, x + width, top - 8, right_header, color=PDFStyle.COLOR_CORAL_STRONG, align="right")

    card_w = width / 2 - 0.75 * cm
    pad = 0.35 * cm
    label_h, line_h, box_h = 10, 0.85 * cm, 1.6 * cm
    card_h = 2 * pad + 2 * (label_h + 3) + line_h + 0.25 * cm + box_h
    first_y = top - 0.65 * cm - card_h / 2
    last_y = PDFStyle.CONTENT_BOTTOM + card_h / 2
    step = (first_y - last_y) / max(len(nodes) - 1, 1)

    # The axis: a dotted line from a dot to a triangle, time running downwards
    c.saveState()
    c.setStrokeColor(PDFStyle.COLOR_INK, alpha=0.25)
    c.setLineWidth(1.5)
    c.setDash(3, 3)
    c.line(center, top - 0.55 * cm, center, PDFStyle.CONTENT_BOTTOM + 0.2 * cm)
    c.restoreState()
    draw_disc(c, center, top - 0.55 * cm, 4.5, PDFStyle.COLOR_INK)
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_INK)
    p = c.beginPath()
    p.moveTo(center - 5, PDFStyle.CONTENT_BOTTOM + 0.2 * cm)
    p.lineTo(center + 5, PDFStyle.CONTENT_BOTTOM + 0.2 * cm)
    p.lineTo(center, PDFStyle.CONTENT_BOTTOM - 0.15 * cm)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

    pastels = pastel_cycle(c)
    for i, node in enumerate(nodes, start=1):
        label, kind = node[0], node[1]
        summit = kind == "summit"
        prompt = str(node[2]) if len(node) > 2 and node[2] else LIFE_LINE_PROMPTS["summit" if summit else "valley"]
        cy = first_y - (i - 1) * step
        card_x = x if summit else center + 0.75 * cm
        color = pastels[1] if summit else pastels[2]
        # Connector, then the badge on the axis ringed with the page color
        draw_rule(c, card_x + card_w if summit else center, center if summit else card_x, cy,
                  color=PDFStyle.COLOR_INK, alpha=0.25, width=1, dash=(2, 2))
        draw_disc(c, center, cy, 14, PDFStyle.COLOR_PAGE)
        draw_icon_badge(c, center, cy, "trending_up" if summit else "trending_down", diameter=22, fill=color,
                        color=PDFStyle.COLOR_INK)

        draw_pastel_card(c, card_x, cy - card_h / 2, card_w, card_h, color=color, radius=12)
        t = cy + card_h / 2 - pad
        draw_eyebrow(c, card_x + pad, t - 7.5, f"{label} · date et événement", size=7.5,
                     tracking=PDFStyle.TRACKING_LABEL, max_width=card_w - 2 * pad)
        t -= label_h + 3
        draw_answer_box(c, card_x + pad, t - line_h, card_w - 2 * pad, line_h, f"{field_prefix}_{i}_titre",
                        tooltip=f"{label} : date et événement", multiline=False)
        t -= line_h + 0.25 * cm
        draw_eyebrow(c, card_x + pad, t - 7.5, prompt, size=7.5, tracking=PDFStyle.TRACKING_LABEL,
                     max_width=card_w - 2 * pad)
        t -= label_h + 3
        draw_answer_box(c, card_x + pad, t - box_h, card_w - 2 * pad, box_h, f"{field_prefix}_{i}_desc",
                        tooltip=f"{label} : {prompt}")


def _tree_zone(c, cx, top, width, number_title, hint, field_id, box_h, align="center"):
    """A zone of the tree: its label, a hint and an answer box, centred on cx below top."""
    x = cx - width / 2
    draw_eyebrow(c, cx if align == "center" else x, top - 8, number_title, size=7.5, tracking=PDFStyle.TRACKING_LABEL,
                 color=PDFStyle.COLOR_INK, align=align, max_width=width)
    hint_h = draw_paragraph(c, hint, x, top - 12, width, PDFStyle.FONT_BODY, 8.5, PDFStyle.COLOR_INK_MUTED, 11,
                            align=align)
    box_top = top - 12 - hint_h - 3
    draw_answer_box(c, x, box_top - box_h, width, box_h, field_id, tooltip=f"{number_title} : {hint}")
    return box_top - box_h


def draw_tree_of_life(c, x, top, width, zones, annotation=None):
    """
    The tree of life, from top down to the bottom margin, drawn with the art direction's
    shapes (discs for the foliage, a pill for the trunk, a dotted ground line), each part
    holding its answer box. zones: the six parts in this order, each (title, hint,
    field_id): roots, soil, trunk, branches, leaves, fruits.
    """
    roots, soil, trunk, branches, leaves, fruits = zones
    cx = x + width / 2
    bottom = PDFStyle.CONTENT_BOTTOM
    pastels = pastel_cycle(c)

    # The roots box (2 cm, two handwritten lines and more) sits between the ground and the margin
    ground_y = bottom + 4.1 * cm
    trunk_w, trunk_top = 5.4 * cm, ground_y + 5.6 * cm
    crown_r = min(5.2 * cm, (top - trunk_top) / 2 + 1.2 * cm)
    crown_cy = top - crown_r - 0.1 * cm
    side_r = 2.9 * cm

    # Shapes, back to front
    draw_disc(c, x + side_r * 0.95, crown_cy - crown_r * 0.62, side_r, pastels[2])
    draw_disc(c, x + width - side_r * 0.95, crown_cy - crown_r * 0.62, side_r, pastels[3])
    c.saveState()
    c.setFillColor(PDFStyle.COLOR_INK, alpha=0.07)
    # The trunk runs up under the crown so that they join
    c.roundRect(cx - trunk_w / 2, ground_y - 0.2 * cm, trunk_w, crown_cy - ground_y, trunk_w / 2.4, stroke=0, fill=1)
    c.restoreState()
    draw_disc(c, cx, crown_cy, crown_r, document_pastel(c))
    draw_rule(c, x, x + width, ground_y, color=PDFStyle.COLOR_INK, alpha=0.3, width=1.5, dash=(3, 3))
    # Roots: three curves from the trunk down to the roots box
    c.saveState()
    c.setStrokeColor(PDFStyle.COLOR_INK, alpha=0.25)
    c.setLineWidth(1.2)
    c.setLineCap(1)
    for dx in (-1.4 * cm, 0, 1.4 * cm):
        p = c.beginPath()
        p.moveTo(cx + dx * 0.5, ground_y - 0.2 * cm)
        p.curveTo(cx + dx * 0.7, ground_y - 0.6 * cm, cx + dx * 1.3, ground_y - 0.7 * cm, cx + dx * 1.6,
                  ground_y - 1.0 * cm)
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()

    # Zones
    _tree_zone(c, cx, crown_cy + 2.2 * cm, 6.6 * cm, *branches, 2.3 * cm)
    _tree_zone(c, x + side_r * 0.95, crown_cy - crown_r * 0.62 + 1.45 * cm, 4.5 * cm, *leaves, 1.9 * cm)
    _tree_zone(c, x + width - side_r * 0.95, crown_cy - crown_r * 0.62 + 1.45 * cm, 4.5 * cm, *fruits, 1.9 * cm)
    _tree_zone(c, cx, trunk_top - 0.3 * cm, trunk_w - 0.9 * cm, *trunk, trunk_top - ground_y - 1.6 * cm)
    _tree_zone(c, x + 2.3 * cm, ground_y + 2.6 * cm, 4.6 * cm, *soil, 1.6 * cm)
    _tree_zone(c, cx, ground_y - 1.15 * cm, 9.0 * cm, *roots, 2.0 * cm)

    if annotation:
        draw_annotation(c, x + width - 4.9 * cm, ground_y + 2.4 * cm, annotation, 4.6 * cm)
