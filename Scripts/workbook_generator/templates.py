from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from .utils import cached_simpleSplit as simpleSplit
import logging
from dataclasses import dataclass
from .config import PDFStyle
from .components import (
    draw_page_background,
    draw_side_panel,
    draw_title,
    draw_page_decorations,
    draw_card,
)
from .forms import create_input_field, create_checkbox

logger = logging.getLogger(__name__)


@dataclass
class LayoutConfig:
    part_title: str = ""
    use_side_panel: bool = True
    use_blobs: bool = False
    y_start: float = None


@dataclass
class QuestionConfig:
    box_height: float = 3.0 * cm
    subtitle: str = None
    example: str = None
    color_alternation: bool = True
    color: str = None


@dataclass
class QuestionItem:
    question: str
    form_field_id: str
    subtitle: str = None
    example: str = None
    color: str = None
    box_height: float = None  # None for auto-fit



@dataclass
class TextConfig:
    style_choice: str = "body"
    font_size: int = 11
    color: str = PDFStyle.COLOR_TEXT_MAIN
    spacing_after: float = 0.5 * cm
    align: str = "left"


class PageLayout:
    """
    Base Layout Engine for the Workbook.
    Automatically handles the boilerplate for:
    - Page dimensions, Backgrounds, Side Panels, Decorations.
    - Cursor tracking to prevent overlapping elements.
    - Simplified methods to add text and question blocks.
    """

    def __init__(self, c, title, config: LayoutConfig = None):
        self.c = c
        self.title = title

        if config is None:
            config = LayoutConfig()

        self.part_title = config.part_title

        self.width, self.height = A4
        self.card_margin = 2 * cm

        # Draw background elements
        draw_page_background(
            self.c, self.width, self.height, use_blobs=config.use_blobs
        )

        if config.use_side_panel:
            draw_side_panel(self.c, self.card_margin, self.width, self.height)
            self.text_x = self.card_margin + 1.0 * cm
            self.target_width = self.width - self.card_margin - 2.0 * cm
        else:
            self.text_x = 2.0 * cm
            self.target_width = self.width - 4.0 * cm

        # Draw Title
        if title:
            self.title_y = self.height - 4.0 * cm
            new_y = draw_title(
                self.c,
                self.title,
                pos=(self.text_x, self.title_y),
                available_width=self.target_width,
            )
            self.y_cursor = new_y - (24 * 0.5)
        else:
            self.title_y = self.height - 2.0 * cm
            self.y_cursor = self.title_y

        if config.y_start is not None:
            self.y_cursor = config.y_start

        self.question_index = 0
        self.form = self.c.acroForm

    def add_text(self, text, config: TextConfig = None):
        """Adds a paragraph of text, automatically wrapping and moving the cursor."""
        if config is None:
            config = TextConfig()

        if config.style_choice == "body":
            font_name = PDFStyle.FONT_BODY
        elif config.style_choice == "italic":
            font_name = PDFStyle.FONT_ITALIC
        elif config.style_choice == "subtitle":
            font_name = PDFStyle.FONT_SUBTITLE
        else:
            font_name = PDFStyle.FONT_BODY

        self.c.setFont(font_name, config.font_size)
        self.c.setFillColor(config.color)

        lines = simpleSplit(text, font_name, config.font_size, self.target_width)
        for line in lines:
            if config.align == "center":
                self.c.drawCentredString(
                    self.text_x + self.target_width / 2, self.y_cursor, line
                )
            elif config.align == "right":
                self.c.drawRightString(
                    self.text_x + self.target_width, self.y_cursor, line
                )
            else:
                self.c.drawString(self.text_x, self.y_cursor, line)
            self.y_cursor -= config.font_size + 0.1 * cm  # Roughly line height

        self.y_cursor -= config.spacing_after
        return self.y_cursor

    def add_question_block(
        self, question, form_field_id, config: QuestionConfig = None
    ):
        """Adds a standard question block and its AcroForm input."""
        if config is None:
            config = QuestionConfig()

        if config.color_alternation:
            color = (
                PDFStyle.COLOR_ACCENT_BLUE
                if self.question_index % 2 == 0
                else PDFStyle.COLOR_ACCENT_RED
            )
        else:
            color = config.color if config.color else PDFStyle.COLOR_ACCENT_BLUE

        self.add_text(
            question,
            config=TextConfig(
                style_choice="subtitle",
                font_size=11,
                color=color,
                spacing_after=0.1 * cm,
            ),
        )

        if config.subtitle:
            self.add_text(
                config.subtitle,
                config=TextConfig(
                    style_choice="body",
                    font_size=10,
                    color=PDFStyle.COLOR_TEXT_SECONDARY,
                    spacing_after=0.1 * cm,
                ),
            )

        if config.example:
            box_padding = 0.2 * cm
            font_size = 9
            font_name = PDFStyle.FONT_ITALIC

            lines = simpleSplit(
                f"Exemple : {config.example}",
                font_name,
                font_size,
                self.target_width - 2 * box_padding,
            )
            box_height = len(lines) * (font_size + 2) + 2 * box_padding

            self.y_cursor -= box_height
            self.c.setFillColorRGB(0.95, 0.95, 0.95)
            self.c.rect(
                self.text_x,
                self.y_cursor,
                self.target_width,
                box_height,
                fill=1,
                stroke=0,
            )

            self.c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
            self.c.setFont(font_name, font_size)
            text_y = self.y_cursor + box_height - box_padding - font_size
            for line in lines:
                self.c.drawString(self.text_x + box_padding, text_y, line)
                text_y -= font_size + 2

            self.y_cursor -= 0.2 * cm

        self.y_cursor -= 0.2 * cm  # Gap before input

        # Check if we need to paginate (basic protection)
        if self.y_cursor - config.box_height < 3 * cm:
            logger.warning(
                f"Form field '{form_field_id}' might overflow bottom margin."
            )

        create_input_field(
            self.form,
            form_field_id,
            pos=(self.text_x, self.y_cursor - config.box_height),
            size=(self.target_width, config.box_height),
            multiline=True,
        )

        self.y_cursor -= config.box_height + 0.8 * cm
        self.question_index += 1
        return self.y_cursor

    def add_questions_group(
        self,
        questions,
        min_box_height: float = 2.2 * cm,
        max_box_height: float = 7.5 * cm,
        safe_bottom_margin: float = 2.8 * cm,
    ):
        """
        Adds a group of questions dynamically auto-fitting available vertical space
        so that boxes scale proportionally and never overflow the bottom margin.

        Args:
            questions (list): List of QuestionItem instances, dicts, or tuples.
            min_box_height (float): Minimum height for each text area (default 2.2 cm).
            max_box_height (float): Maximum height for each text area (default 7.5 cm).
            safe_bottom_margin (float): Safe distance to bottom edge to protect footers (default 2.8 cm).
        """
        if not questions:
            return self.y_cursor

        norm_questions = []
        for q in questions:
            if isinstance(q, QuestionItem):
                norm_questions.append(q)
            elif isinstance(q, dict):
                norm_questions.append(
                    QuestionItem(
                        question=q.get("question", ""),
                        form_field_id=q.get("form_field_id")
                        or q.get("field_id", f"q_{self.question_index}_{len(norm_questions)}"),
                        subtitle=q.get("subtitle"),
                        example=q.get("example"),
                        color=q.get("color"),
                        box_height=q.get("box_height"),
                    )
                )
            elif isinstance(q, (tuple, list)):
                q_text = q[0]
                q_id = (
                    q[1]
                    if len(q) > 1
                    else f"q_{self.question_index}_{len(norm_questions)}"
                )
                q_sub = q[2] if len(q) > 2 else None
                norm_questions.append(
                    QuestionItem(
                        question=q_text, form_field_id=q_id, subtitle=q_sub
                    )
                )
            else:
                norm_questions.append(
                    QuestionItem(
                        question=str(q),
                        form_field_id=f"q_{self.question_index}_{len(norm_questions)}",
                    )
                )

        total_text_overhead = 0
        n_auto = 0
        fixed_height_sum = 0

        for q in norm_questions:
            lines = simpleSplit(
                q.question, PDFStyle.FONT_SUBTITLE, 11, self.target_width
            )
            t_h = len(lines) * (11 + 0.1 * cm) + 0.1 * cm

            s_h = 0
            if q.subtitle:
                sub_lines = simpleSplit(
                    q.subtitle, PDFStyle.FONT_BODY, 10, self.target_width
                )
                s_h = len(sub_lines) * (10 + 0.1 * cm) + 0.1 * cm

            ex_h = 0
            if q.example:
                box_padding = 0.2 * cm
                ex_lines = simpleSplit(
                    f"Exemple : {q.example}",
                    PDFStyle.FONT_ITALIC,
                    9,
                    self.target_width - 2 * box_padding,
                )
                ex_h = len(ex_lines) * (9 + 2) + 2 * box_padding + 0.4 * cm

            gap_overhead = 0.2 * cm + 0.8 * cm
            total_text_overhead += t_h + s_h + ex_h + gap_overhead

            if q.box_height is not None:
                fixed_height_sum += q.box_height
            else:
                n_auto += 1

        available_space = self.y_cursor - safe_bottom_margin
        remaining_for_boxes = available_space - total_text_overhead - fixed_height_sum

        if n_auto > 0:
            auto_box_h = remaining_for_boxes / n_auto
            auto_box_h = max(min_box_height, min(max_box_height, auto_box_h))
        else:
            auto_box_h = min_box_height

        for q in norm_questions:
            target_h = q.box_height if q.box_height is not None else auto_box_h
            cfg = QuestionConfig(
                box_height=target_h,
                subtitle=q.subtitle,
                example=q.example,
                color_alternation=(q.color is None),
                color=q.color,
            )
            self.add_question_block(q.question, q.form_field_id, config=cfg)

        return self.y_cursor

    def add_callout(self, text, title=None, variant="info", height=None):
        """
        Renders an elegant highlighted callout / quote card with generous breathing room.
        - variant: 'info' (Blue), 'tip' (Red), 'quote' (Success)
        """
        color_map = {
            "info": PDFStyle.COLOR_ACCENT_BLUE,
            "tip": PDFStyle.COLOR_ACCENT_RED,
            "quote": PDFStyle.COLOR_SUCCESS,
        }
        accent_color = color_map.get(variant, PDFStyle.COLOR_ACCENT_BLUE)

        font_name = PDFStyle.FONT_ITALIC if variant == "quote" else PDFStyle.FONT_BODY
        font_size = 9.5
        line_height = 14

        content_w = self.target_width - 1.2 * cm
        lines = simpleSplit(text, font_name, font_size, content_w)
        text_h = len(lines) * line_height

        header_h = 0.55 * cm if title else 0
        computed_h = header_h + text_h + 0.8 * cm
        h = max(height if height else computed_h, 1.6 * cm)

        card_y = self.y_cursor - h

        # Draw card container
        self.c.saveState()
        self.c.setFillColor(PDFStyle.COLOR_CARD_CREME)
        self.c.setStrokeColor(PDFStyle.COLOR_LINE)
        self.c.setLineWidth(0.5)
        self.c.roundRect(self.text_x, card_y, self.target_width, h, 4, fill=1, stroke=1)

        # Thick accent stripe on the left
        self.c.setFillColor(accent_color)
        self.c.rect(self.text_x, card_y, 0.22 * cm, h, fill=1, stroke=0)
        self.c.restoreState()

        # Text rendering
        curr_text_y = self.y_cursor - 0.5 * cm
        if title:
            self.c.saveState()
            self.c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
            self.c.setFillColor(accent_color)
            self.c.drawString(self.text_x + 0.5 * cm, curr_text_y, title.upper())
            self.c.restoreState()
            curr_text_y -= 0.5 * cm

        self.c.saveState()
        self.c.setFont(font_name, font_size)
        self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        for line in lines:
            self.c.drawString(self.text_x + 0.5 * cm, curr_text_y, line)
            curr_text_y -= line_height
        self.c.restoreState()

        self.y_cursor -= (h + 0.7 * cm)
        return self.y_cursor

    def add_cards_grid(self, cards, columns=2, card_height=None, field_prefix="grid"):
        """
        Renders an airy grid of cards (2 or 3 columns) with titles, subtitles and AcroForm text areas.
        """
        if not cards:
            return self.y_cursor

        cols = max(1, min(columns, 4))
        gap = 0.5 * cm
        col_w = (self.target_width - (cols - 1) * gap) / cols
        h = card_height if card_height else (4.8 * cm if cols == 2 else 4.0 * cm)

        # Group cards in rows
        n_cards = len(cards)
        rows_count = (n_cards + cols - 1) // cols

        for r_idx in range(rows_count):
            row_y = self.y_cursor - h
            for c_idx in range(cols):
                card_index = r_idx * cols + c_idx
                if card_index >= n_cards:
                    break

                card_data = cards[card_index]
                if isinstance(card_data, dict):
                    c_title = card_data.get("title", f"Carte {card_index+1}")
                    c_sub = card_data.get("subtitle", "")
                    c_fid = card_data.get("field_id", f"{field_prefix}_{card_index+1}")
                    c_placeholder = card_data.get("placeholder", "")
                elif isinstance(card_data, (tuple, list)):
                    c_title = card_data[0]
                    c_sub = card_data[1] if len(card_data) > 1 else ""
                    c_fid = card_data[2] if len(card_data) > 2 else f"{field_prefix}_{card_index+1}"
                    c_placeholder = ""
                else:
                    c_title = str(card_data)
                    c_sub = ""
                    c_fid = f"{field_prefix}_{card_index+1}"
                    c_placeholder = ""

                card_x = self.text_x + c_idx * (col_w + gap)

                # Card Box
                draw_card(self.c, card_x, row_y, col_w, h)

                # Card Title
                self.c.saveState()
                self.c.setFont(PDFStyle.FONT_SUBTITLE, 9)
                self.c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE if c_idx % 2 == 0 else PDFStyle.COLOR_ACCENT_RED)
                self.c.drawString(card_x + 0.35 * cm, row_y + h - 0.5 * cm, c_title.upper())

                sub_h = 0
                if c_sub:
                    self.c.setFont(PDFStyle.FONT_ITALIC, 8)
                    self.c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
                    self.c.drawString(card_x + 0.35 * cm, row_y + h - 0.9 * cm, c_sub)
                    sub_h = 0.4 * cm
                self.c.restoreState()

                # Text Input inside Card
                input_y = row_y + 0.3 * cm
                input_h = h - 0.85 * cm - sub_h
                create_input_field(
                    self.form,
                    c_fid,
                    pos=(card_x + 0.35 * cm, input_y),
                    size=(col_w - 0.7 * cm, input_h),
                    multiline=True,
                    tooltip=c_placeholder,
                    fill_color=PDFStyle.COLOR_CARD_CREME,
                )

            self.y_cursor -= (h + gap)

        self.y_cursor -= 0.3 * cm
        return self.y_cursor

    def add_scale_gauge(self, label, min_val=0, max_val=10, min_label="", max_label="", field_id=None):
        """
        Renders an interactive rating / evaluation scale with checkboxes and min/max labels with airy vertical rhythm.
        """
        fid_base = field_id or f"scale_{self.question_index}"
        self.question_index += 1

        # Label
        self.c.saveState()
        self.c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
        self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        self.c.drawString(self.text_x, self.y_cursor - 0.35 * cm, label)

        # Track line
        track_y = self.y_cursor - 1.0 * cm
        self.c.setStrokeColor(PDFStyle.COLOR_LINE)
        self.c.setLineWidth(1)
        self.c.line(self.text_x, track_y, self.text_x + self.target_width, track_y)
        self.c.restoreState()

        # Checkbox points
        steps = list(range(min_val, max_val + 1))
        n_steps = len(steps)
        step_w = self.target_width / max(1, n_steps - 1)

        for i, val in enumerate(steps):
            pt_x = self.text_x + i * step_w
            # Number label above
            self.c.saveState()
            self.c.setFont(PDFStyle.FONT_BODY, 8.5)
            self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            self.c.drawCentredString(pt_x, track_y + 0.22 * cm, str(val))
            self.c.restoreState()

            # Checkbox below track (10pt height = ~0.35 cm)
            create_checkbox(
                self.form,
                f"{fid_base}_{val}",
                pos=(pt_x - 5, track_y - 0.52 * cm),
                size=10,
                tooltip=f"{label} : {val}",
            )

        # Min / Max labels at ends (generously spaced below checkboxes)
        has_sublabels = bool(min_label or max_label)
        if has_sublabels:
            self.c.saveState()
            self.c.setFont(PDFStyle.FONT_ITALIC, 7.5)
            self.c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
            if min_label:
                self.c.drawString(self.text_x, track_y - 0.95 * cm, min_label)
            if max_label:
                self.c.drawRightString(self.text_x + self.target_width, track_y - 0.95 * cm, max_label)
            self.c.restoreState()

        h_total = 2.4 * cm if has_sublabels else 1.9 * cm
        self.y_cursor -= (h_total + 0.5 * cm)
        return self.y_cursor

    def add_checklist(self, items, title=None, columns=1, field_prefix="chk"):
        """
        Renders a checklist of tasks or criteria with checkboxes and labels with comfortable spacing.
        """
        if not items:
            return self.y_cursor

        cols = max(1, min(columns, 2))
        col_w = self.target_width if cols == 1 else (self.target_width - 0.6 * cm) / 2.0

        if title:
            self.c.saveState()
            self.c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
            self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            self.c.drawString(self.text_x, self.y_cursor - 0.35 * cm, title)
            self.c.restoreState()
            self.y_cursor -= 0.7 * cm

        row_h = 0.8 * cm
        n_items = len(items)
        rows_count = (n_items + cols - 1) // cols

        for r in range(rows_count):
            item_y = self.y_cursor - 0.45 * cm
            for c in range(cols):
                idx = r * cols + c
                if idx >= n_items:
                    break

                item_data = items[idx]
                if isinstance(item_data, dict):
                    label = item_data.get("label", str(item_data))
                    fid = item_data.get("field_id", f"{field_prefix}_{idx+1}")
                elif isinstance(item_data, (tuple, list)):
                    label = item_data[0]
                    fid = item_data[1] if len(item_data) > 1 else f"{field_prefix}_{idx+1}"
                else:
                    label = str(item_data)
                    fid = f"{field_prefix}_{idx+1}"

                item_x = self.text_x if c == 0 else self.text_x + col_w + 0.6 * cm

                create_checkbox(
                    self.form,
                    fid,
                    pos=(item_x, item_y),
                    size=10,
                    tooltip=label,
                )

                self.c.saveState()
                self.c.setFont(PDFStyle.FONT_BODY, 8.5)
                self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
                self.c.drawString(item_x + 0.55 * cm, item_y + 0.05 * cm, label)
                self.c.restoreState()

            self.y_cursor -= row_h

        self.y_cursor -= 0.6 * cm
        return self.y_cursor

    def add_table(self, headers, rows, col_widths=None, field_prefix="tbl"):
        """
        Renders a clean multi-column table with headers and data cells (labels or inputs).
        """
        n_cols = len(headers)
        if n_cols == 0:
            return self.y_cursor

        if col_widths is None:
            col_w = self.target_width / n_cols
            widths = [col_w] * n_cols
        else:
            widths = col_widths

        header_h = 0.7 * cm
        row_h = 0.95 * cm

        # Draw Header row
        h_y = self.y_cursor - header_h
        self.c.saveState()
        self.c.setFillColor(PDFStyle.COLOR_CARD_CREME)
        self.c.setStrokeColor(PDFStyle.COLOR_LINE)
        self.c.setLineWidth(0.5)
        self.c.roundRect(self.text_x, h_y, self.target_width, header_h, 3, fill=1, stroke=1)

        curr_x = self.text_x
        for i, h_text in enumerate(headers):
            self.c.setFont(PDFStyle.FONT_SUBTITLE, 8)
            self.c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
            self.c.drawString(curr_x + 0.25 * cm, h_y + 0.22 * cm, str(h_text).upper())
            curr_x += widths[i]
        self.c.restoreState()

        self.y_cursor -= (header_h + 0.15 * cm)

        # Draw Rows
        for r_idx, row in enumerate(rows):
            r_y = self.y_cursor - row_h
            curr_x = self.text_x
            for c_idx, cell in enumerate(row[:n_cols]):
                w = widths[c_idx]
                if isinstance(cell, dict):
                    fid = cell.get("field_id", f"{field_prefix}_r{r_idx+1}_c{c_idx+1}")
                    placeholder = cell.get("placeholder", "")
                    create_input_field(
                        self.form,
                        fid,
                        pos=(curr_x + 0.12 * cm, r_y + 0.1 * cm),
                        size=(w - 0.24 * cm, row_h - 0.2 * cm),
                        multiline=False,
                        tooltip=placeholder,
                        fill_color=PDFStyle.COLOR_WHITE,
                    )
                else:
                    self.c.saveState()
                    self.c.setFont(PDFStyle.FONT_BODY, 8.5)
                    self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
                    self.c.drawString(curr_x + 0.25 * cm, r_y + 0.3 * cm, str(cell))
                    self.c.restoreState()
                curr_x += w
            self.y_cursor -= row_h

        self.y_cursor -= 0.6 * cm
        return self.y_cursor

    def add_stat_boxes(self, stats):
        """
        Renders a row of 2, 3 or 4 highlight KPI / stat callout boxes.
        """
        if not stats:
            return self.y_cursor

        n = len(stats)
        gap = 0.5 * cm
        box_w = (self.target_width - (n - 1) * gap) / n
        h = 2.0 * cm
        box_y = self.y_cursor - h

        colors_list = [
            PDFStyle.COLOR_ACCENT_BLUE,
            PDFStyle.COLOR_ACCENT_RED,
            PDFStyle.COLOR_SUCCESS,
        ]

        for i, st in enumerate(stats):
            b_x = self.text_x + i * (box_w + gap)
            val = st.get("stat", "") if isinstance(st, dict) else str(st[0] if isinstance(st, (tuple, list)) else st)
            lbl = st.get("label", "") if isinstance(st, dict) else str(st[1] if isinstance(st, (tuple, list)) and len(st) > 1 else "")
            color = colors_list[i % len(colors_list)]

            self.c.saveState()
            self.c.setFillColor(PDFStyle.COLOR_CARD_CREME)
            self.c.setStrokeColor(PDFStyle.COLOR_LINE)
            self.c.setLineWidth(0.5)
            self.c.roundRect(b_x, box_y, box_w, h, 4, fill=1, stroke=1)

            # Stat number
            self.c.setFont(PDFStyle.FONT_BRANDING, 17)
            self.c.setFillColor(color)
            self.c.drawCentredString(b_x + box_w / 2.0, box_y + 1.0 * cm, str(val))

            # Stat label
            if lbl:
                self.c.setFont(PDFStyle.FONT_SUBTITLE, 7.5)
                self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
                self.c.drawCentredString(b_x + box_w / 2.0, box_y + 0.35 * cm, str(lbl).upper())

            self.c.restoreState()

        self.y_cursor -= (h + 0.7 * cm)
        return self.y_cursor

    def add_space(self, height):
        self.y_cursor -= height
        return self.y_cursor

    def render(self):
        """Finalizes the page with decorations."""
        draw_page_decorations(
            self.c,
            self.width,
            self.height,
            part_title=self.part_title,
            x_offset=self.card_margin,
        )
        self.c.showPage()
