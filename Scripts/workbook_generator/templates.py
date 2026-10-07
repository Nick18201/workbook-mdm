import logging
from xml.sax.saxutils import escape
from dataclasses import dataclass
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from .utils import cached_simpleSplit as simpleSplit, fit_font_size, ellipsize
from .config import PDFStyle
from .components import (
    draw_page_background,
    draw_side_panel,
    draw_title,
    draw_page_decorations,
    draw_card,
)
from .forms import create_input_field, create_checkbox, create_radio, reserve_field_name

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


def _example_display(example):
    """Normalizes an example to the 'Exemple : …' form shown under a question."""
    ex_clean = example.strip()
    if ex_clean.lower().startswith("exemple :"):
        return ex_clean
    if ex_clean.lower().startswith("ex :"):
        return "Exemple :" + ex_clean[4:]
    if ex_clean.lower().startswith("ex:"):
        return "Exemple :" + ex_clean[3:]
    return f"Exemple : {ex_clean}"


class PageLayout:
    """
    Base Layout Engine for the Workbook.
    Automatically handles the boilerplate for:
    - Page dimensions, Backgrounds, Side Panels, Decorations.
    - Cursor tracking to prevent overlapping elements.
    - Simplified methods to add text and question blocks.
    - Overflow: a block that would run past the bottom margin continues on a new page
      titled "<title> (suite)", so content is never drawn off the page.
    """

    def __init__(self, c, title, config: LayoutConfig = None):
        self.c = c
        self.title = title

        if config is None:
            config = LayoutConfig()

        self.config = config
        self.part_title = config.part_title

        self.width, self.height = A4
        self.card_margin = 2 * cm
        # Lowest point a block may reach; the page number sits at 1.5 cm
        self.bottom_limit = 2.0 * cm

        self.question_index = 0
        self.form = self.c.acroForm

        self._start_page(title)
        if config.y_start is not None:
            self.y_cursor = config.y_start
            self._page_top = self.y_cursor

    def _start_page(self, title):
        """Draws the page frame (background, side panel, title) and puts the cursor below the title."""
        draw_page_background(
            self.c, self.width, self.height, use_blobs=self.config.use_blobs
        )

        if self.config.use_side_panel:
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
                title,
                pos=(self.text_x, self.title_y),
                available_width=self.target_width,
            )
            self.y_cursor = new_y - (24 * 0.5)
        else:
            self.title_y = self.height - 2.0 * cm
            self.y_cursor = self.title_y

        self._page_top = self.y_cursor

    def _new_page(self):
        """Finishes the current page and starts a continuation page."""
        self.render()
        self._start_page(f"{self.title} (suite)" if self.title else "")

    def _ensure_space(self, height):
        """
        Starts a continuation page when a block of this height would run past the bottom
        margin (unless the page is still empty). Returns True when a new page was started,
        so callers can redraw what must repeat (e.g. a table header) and reset fonts.
        """
        if self.y_cursor - height < self.bottom_limit and self.y_cursor < self._page_top:
            self._new_page()
            return True
        return False

    def _question_text_height(self, question, subtitle=None, example=None):
        """Vertical space taken by a question block, input box excluded (matches add_question_block)."""
        lines = simpleSplit(question, PDFStyle.FONT_SUBTITLE, 11, self.target_width)
        t_h = len(lines) * (11 + 0.1 * cm) + 0.1 * cm

        s_h = 0
        if subtitle:
            sub_lines = simpleSplit(subtitle, PDFStyle.FONT_BODY, 10, self.target_width)
            s_h = len(sub_lines) * (10 + 0.1 * cm) + 0.1 * cm

        ex_h = 0
        if example:
            box_padding = 0.25 * cm
            ex_lines = simpleSplit(
                _example_display(example),
                PDFStyle.FONT_ITALIC,
                9,
                self.target_width - 2 * box_padding,
            )
            ex_h = len(ex_lines) * (9 + 2) + 2 * box_padding + 0.35 * cm

        gap_overhead = 0.15 * cm + 0.65 * cm
        return t_h + s_h + ex_h + gap_overhead

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

        line_h = config.font_size + 0.1 * cm  # Roughly line height
        lines = simpleSplit(text, font_name, config.font_size, self.target_width)
        for line in lines:
            if self._ensure_space(line_h):
                self.c.setFont(font_name, config.font_size)
                self.c.setFillColor(config.color)
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
            self.y_cursor -= line_h

        self.y_cursor -= config.spacing_after
        return self.y_cursor

    def add_question_block(
        self, question, form_field_id, config: QuestionConfig = None
    ):
        """Adds a standard question block and its AcroForm input."""
        if config is None:
            config = QuestionConfig()

        box_h = config.box_height if config.box_height is not None else 3.0 * cm
        # Keep the question, its hints and its answer box together on one page
        self._ensure_space(
            self._question_text_height(question, config.subtitle, config.example) + box_h
        )

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
            box_padding = 0.25 * cm
            font_size = 9
            font_name = PDFStyle.FONT_ITALIC

            lines = simpleSplit(
                _example_display(config.example),
                font_name,
                font_size,
                self.target_width - 2 * box_padding,
            )
            box_height = len(lines) * (font_size + 2) + 2 * box_padding

            self.y_cursor -= box_height
            self.c.setFillColorRGB(0.96, 0.96, 0.98)
            self.c.roundRect(
                self.text_x,
                self.y_cursor,
                self.target_width,
                box_height,
                3,
                fill=1,
                stroke=0,
            )

            self.c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
            self.c.setFont(font_name, font_size)
            text_y = self.y_cursor + box_height - box_padding - font_size
            for line in lines:
                self.c.drawString(self.text_x + box_padding, text_y, line)
                text_y -= font_size + 2

            self.y_cursor -= 0.25 * cm

        self.y_cursor -= 0.15 * cm  # Gap before input

        # Always draw visible background on canvas so the writing zone is NEVER blank
        self.c.saveState()
        self.c.setFillColor(PDFStyle.COLOR_FIELD_BG)
        self.c.setStrokeColor(PDFStyle.COLOR_LINE)
        self.c.setLineWidth(0.5)
        self.c.roundRect(
            self.text_x,
            self.y_cursor - box_h,
            self.target_width,
            box_h,
            4,
            fill=1,
            stroke=1,
        )
        self.c.restoreState()

        create_input_field(
            self.form,
            form_field_id,
            pos=(self.text_x, self.y_cursor - box_h),
            size=(self.target_width, box_h),
            multiline=True,
            fill_color=PDFStyle.COLOR_FIELD_BG,
        )

        self.y_cursor -= box_h + 0.65 * cm
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

        overheads = [
            self._question_text_height(q.question, q.subtitle, q.example)
            for q in norm_questions
        ]
        min_auto_h = 1.5 * cm

        # Questions are placed in chunks that fit the current page (boxes of at least
        # min_auto_h); the rest continues on new pages, each chunk auto-fitting its page.
        start = 0
        while start < len(norm_questions):
            available = self.y_cursor - safe_bottom_margin
            used, count = 0, 0
            for q, overhead in zip(norm_questions[start:], overheads[start:]):
                need = overhead + (q.box_height if q.box_height is not None else min_auto_h)
                if used + need > available:
                    break
                used += need
                count += 1

            if count == 0:
                if self.y_cursor < self._page_top:
                    self._new_page()
                    continue
                count = 1  # Too tall even for an empty page: place it anyway

            self._add_questions_chunk(
                norm_questions[start:start + count],
                overheads[start:start + count],
                min_box_height,
                max_box_height,
                safe_bottom_margin,
            )
            start += count
            if start < len(norm_questions):
                self._new_page()

        return self.y_cursor

    def _add_questions_chunk(self, questions, overheads, min_box_height, max_box_height, safe_bottom_margin):
        """Renders questions that fit on the current page, sharing the free height between their boxes."""
        total_text_overhead = 0
        n_auto = 0
        fixed_height_sum = 0

        for q, overhead in zip(questions, overheads):
            total_text_overhead += overhead
            if q.box_height is not None:
                fixed_height_sum += q.box_height
            else:
                n_auto += 1

        available_space = self.y_cursor - safe_bottom_margin
        remaining_for_boxes = available_space - total_text_overhead - fixed_height_sum

        if n_auto > 0:
            auto_box_h = remaining_for_boxes / n_auto
            auto_box_h = max(1.5 * cm, min(max_box_height, auto_box_h))
        else:
            auto_box_h = min_box_height

        for q in questions:
            target_h = q.box_height if q.box_height is not None else auto_box_h
            cfg = QuestionConfig(
                box_height=target_h,
                subtitle=q.subtitle,
                example=q.example,
                color_alternation=(q.color is None),
                color=q.color,
            )
            self.add_question_block(q.question, q.form_field_id, config=cfg)

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

        title_lines = simpleSplit(title.upper(), PDFStyle.FONT_SUBTITLE, 9.5, content_w) if title else []
        title_lead = 12
        header_h = 0.55 * cm + (len(title_lines) - 1) * title_lead if title_lines else 0
        computed_h = header_h + text_h + 0.8 * cm
        h = max(height if height else computed_h, 1.6 * cm)

        self._ensure_space(h)
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
        if title_lines:
            self.c.saveState()
            self.c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
            self.c.setFillColor(accent_color)
            for i, t_line in enumerate(title_lines):
                if i:
                    curr_text_y -= title_lead
                self.c.drawString(self.text_x + 0.5 * cm, curr_text_y, t_line)
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
        Multi-line title and subtitle support with dynamic sizing to prevent any overflow.
        """
        if not cards:
            return self.y_cursor

        cols = max(1, min(columns, 4))
        gap = 0.5 * cm
        col_w = (self.target_width - (cols - 1) * gap) / cols
        h = card_height if card_height else (4.8 * cm if cols == 2 else 4.0 * cm)
        pad_x = 0.35 * cm
        inner_w = col_w - 2 * pad_x

        # Adapt font sizes based on columns to guarantee breathing room
        if cols >= 3:
            title_font_size = 8
            title_lh = 10
            sub_font_size = 7.5
            sub_lh = 9.5
        elif cols == 2:
            title_font_size = 9
            title_lh = 11.5
            sub_font_size = 8
            sub_lh = 10
        else:
            title_font_size = 10
            title_lh = 13
            sub_font_size = 8.5
            sub_lh = 11

        # Group cards in rows
        n_cards = len(cards)
        rows_count = (n_cards + cols - 1) // cols

        for r_idx in range(rows_count):
            self._ensure_space(h)
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

                # Card Title (wrapped to inner_w)
                self.c.saveState()
                self.c.setFont(PDFStyle.FONT_SUBTITLE, title_font_size)
                self.c.setFillColor(
                    PDFStyle.COLOR_ACCENT_BLUE
                    if c_idx % 2 == 0
                    else PDFStyle.COLOR_ACCENT_RED
                )

                title_lines = simpleSplit(
                    c_title.upper(), PDFStyle.FONT_SUBTITLE, title_font_size, inner_w
                )
                curr_text_y = row_y + h - 0.45 * cm
                for t_line in title_lines:
                    self.c.drawString(card_x + pad_x, curr_text_y, t_line)
                    curr_text_y -= title_lh

                # Card Subtitle (wrapped to inner_w)
                if c_sub:
                    self.c.setFont(PDFStyle.FONT_ITALIC, sub_font_size)
                    self.c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
                    curr_text_y -= 0.05 * cm
                    sub_lines = simpleSplit(
                        c_sub, PDFStyle.FONT_ITALIC, sub_font_size, inner_w
                    )
                    for s_line in sub_lines:
                        self.c.drawString(card_x + pad_x, curr_text_y, s_line)
                        curr_text_y -= sub_lh

                self.c.restoreState()

                # Text Input & Writing Guides inside Card
                input_y = row_y + 0.3 * cm
                input_h = max(1.2 * cm, curr_text_y - 0.15 * cm - input_y)

                # Subtle dotted writing guide lines
                self.c.saveState()
                self.c.setStrokeColor(PDFStyle.COLOR_LINE)
                self.c.setLineWidth(0.5)
                self.c.setDash([2, 3], 0)
                guide_gap = 0.65 * cm
                curr_gy = input_y + input_h - guide_gap
                while curr_gy > input_y + 0.2 * cm:
                    self.c.line(
                        card_x + pad_x, curr_gy, card_x + col_w - pad_x, curr_gy
                    )
                    curr_gy -= guide_gap
                self.c.restoreState()

                create_input_field(
                    self.form,
                    c_fid,
                    pos=(card_x + pad_x, input_y),
                    size=(inner_w, input_h),
                    multiline=True,
                    tooltip=c_placeholder,
                    fill_color=None,
                )

            self.y_cursor -= (h + gap)

        self.y_cursor -= 0.3 * cm
        return self.y_cursor

    def add_scale_gauge(self, label, min_val=0, max_val=10, min_label="", max_label="", field_id=None):
        """
        Renders a high-end interactive rating / evaluation scale inside an elegant card.
        The values are radio buttons of one group, so a single value can be chosen.
        A long label wraps and the card grows accordingly.
        """
        fid_base = field_id or f"scale_{self.question_index}"
        self.question_index += 1

        label = str(label)
        label_lines = simpleSplit(label, PDFStyle.FONT_SUBTITLE, 9.5, self.target_width - 0.8 * cm) or [label]
        label_lead = 11.5
        card_h = (2.8 * cm if (min_label or max_label) else 2.3 * cm) + (len(label_lines) - 1) * label_lead
        self._ensure_space(card_h)
        card_y = self.y_cursor - card_h

        # Card container
        draw_card(self.c, self.text_x, card_y, self.target_width, card_h)

        # 1. Label at top of card
        self.c.saveState()
        self.c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
        self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        for i, l_line in enumerate(label_lines):
            self.c.drawString(self.text_x + 0.4 * cm, card_y + card_h - 0.55 * cm - i * label_lead, l_line)
        self.c.restoreState()

        # 2. Track & Steps
        track_margin_x = 0.8 * cm
        track_w = self.target_width - 2 * track_margin_x
        track_y = card_y + (1.2 * cm if (min_label or max_label) else 0.8 * cm)

        # Background track line
        self.c.saveState()
        self.c.setStrokeColor(PDFStyle.COLOR_LINE)
        self.c.setLineWidth(1.5)
        self.c.line(self.text_x + track_margin_x, track_y, self.text_x + track_margin_x + track_w, track_y)
        self.c.restoreState()

        steps = list(range(min_val, max_val + 1))
        n_steps = len(steps)
        step_w = track_w / max(1, n_steps - 1)
        group = reserve_field_name(self.form, fid_base)

        for i, val in enumerate(steps):
            pt_x = self.text_x + track_margin_x + i * step_w

            # Step node dot
            self.c.saveState()
            self.c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE if val in (min_val, max_val, (min_val + max_val) // 2) else PDFStyle.COLOR_LINE)
            self.c.circle(pt_x, track_y, 2, fill=1, stroke=0)

            # Number label above
            self.c.setFont(PDFStyle.FONT_SUBTITLE, 8.5)
            self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            self.c.drawCentredString(pt_x, track_y + 0.22 * cm, str(val))
            self.c.restoreState()

            # Radio button below track
            create_radio(
                self.form,
                group,
                val,
                pos=(pt_x - 5, track_y - 0.45 * cm),
                size=10,
                tooltip=f"{label} : {val}",
            )

        # 3. Min / Max labels at bottom
        if min_label or max_label:
            self.c.saveState()
            self.c.setFont(PDFStyle.FONT_ITALIC, 7.5)
            self.c.setFillColor(PDFStyle.COLOR_TEXT_SECONDARY)
            if min_label:
                self.c.drawString(self.text_x + 0.4 * cm, card_y + 0.28 * cm, f"◀ {min_label}")
            if max_label:
                self.c.drawRightString(self.text_x + self.target_width - 0.4 * cm, card_y + 0.28 * cm, f"{max_label} ▶")
            self.c.restoreState()

        self.y_cursor -= (card_h + 0.5 * cm)
        return self.y_cursor

    def add_checklist(self, items, title=None, columns=1, field_prefix="chk"):
        """
        Renders a checklist of tasks or criteria with checkboxes and labels with comfortable spacing and text wrapping.
        """
        if not items:
            return self.y_cursor

        cols = max(1, min(columns, 2))
        gap_x = 0.6 * cm
        col_w = self.target_width if cols == 1 else (self.target_width - gap_x) / 2.0

        if title:
            title_lines = simpleSplit(str(title), PDFStyle.FONT_SUBTITLE, 9.5, self.target_width) or [str(title)]
            title_lead = 12
            title_h = 0.65 * cm + (len(title_lines) - 1) * title_lead
            # Keep the title with at least the first row
            self._ensure_space(title_h + 0.72 * cm)
            self.c.saveState()
            self.c.setFont(PDFStyle.FONT_SUBTITLE, 9.5)
            self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
            for i, t_line in enumerate(title_lines):
                self.c.drawString(self.text_x, self.y_cursor - 0.35 * cm - i * title_lead, t_line)
            self.c.restoreState()
            self.y_cursor -= title_h

        n_items = len(items)
        rows_count = (n_items + cols - 1) // cols
        max_label_w = col_w - 0.7 * cm
        font_size = 8.5
        line_height = 11.0

        for r in range(rows_count):
            # Pre-compute wrapping for this row
            row_items = []
            max_lines = 1
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

                label = str(label)
                lines = simpleSplit(label, PDFStyle.FONT_BODY, font_size, max_label_w)
                if not lines:
                    lines = [label]
                max_lines = max(max_lines, len(lines))
                row_items.append((c, fid, label, lines))

            row_h = max(0.72 * cm, max_lines * line_height + 0.28 * cm)
            self._ensure_space(row_h)
            top_y = self.y_cursor

            for (c, fid, label, lines) in row_items:
                item_x = self.text_x if c == 0 else self.text_x + col_w + gap_x
                # Checkbox aligned with first line of text
                chk_y = top_y - 0.38 * cm
                create_checkbox(
                    self.form,
                    fid,
                    pos=(item_x, chk_y),
                    size=10,
                    tooltip=label,
                )

                self.c.saveState()
                self.c.setFont(PDFStyle.FONT_BODY, font_size)
                self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
                text_x = item_x + 0.6 * cm
                base_y = top_y - 0.35 * cm
                for li, l_text in enumerate(lines):
                    self.c.drawString(text_x, base_y - li * line_height, l_text)
                self.c.restoreState()

            self.y_cursor -= row_h

        self.y_cursor -= 0.4 * cm
        return self.y_cursor

    def add_table(self, headers, rows, col_widths=None, field_prefix="tbl"):
        """
        Renders a clean multi-column table with headers and data cells (auto-wrapped labels or inputs).
        """
        n_cols = len(headers)
        if n_cols == 0:
            return self.y_cursor

        # Smart column width distribution if not explicitly specified
        if col_widths is None:
            if n_cols == 3:
                # Optimized for: [Critère/Pilier (30%), Évaluation/Risque (22%), Plan/Action (48%)]
                widths = [
                    0.30 * self.target_width,
                    0.22 * self.target_width,
                    0.48 * self.target_width,
                ]
            elif n_cols == 2:
                widths = [0.40 * self.target_width, 0.60 * self.target_width]
            elif n_cols == 4:
                widths = [0.25 * self.target_width] * 4
            else:
                col_w = self.target_width / n_cols
                widths = [col_w] * n_cols
        else:
            widths = col_widths

        style_th = ParagraphStyle(
            "TableTH",
            fontName=PDFStyle.FONT_SUBTITLE,
            fontSize=7.5,
            leading=9.5,
            textColor=PDFStyle.COLOR_ACCENT_BLUE,
        )

        style_cell = ParagraphStyle(
            "TableCell",
            fontName=PDFStyle.FONT_BODY,
            fontSize=8,
            leading=10.5,
            textColor=PDFStyle.COLOR_TEXT_MAIN,
        )

        # 1. Compute Header Height & wrap header paragraphs
        th_paragraphs = []
        max_th_h = 0
        for i, h_text in enumerate(headers):
            cell_w = widths[i] - 0.3 * cm
            p_th = Paragraph(f"<b>{escape(str(h_text)).upper()}</b>", style_th)
            _, ph = p_th.wrap(cell_w, 200)
            th_paragraphs.append((p_th, ph))
            max_th_h = max(max_th_h, ph)

        header_h = max(0.65 * cm, max_th_h + 0.3 * cm)

        def draw_header():
            h_y = self.y_cursor - header_h

            # Draw Header row background
            self.c.saveState()
            self.c.setFillColor(PDFStyle.COLOR_CARD_CREME)
            self.c.setStrokeColor(PDFStyle.COLOR_LINE)
            self.c.setLineWidth(0.5)
            self.c.roundRect(self.text_x, h_y, self.target_width, header_h, 3, fill=1, stroke=1)

            curr_x = self.text_x
            for i, (p_th, ph) in enumerate(th_paragraphs):
                p_th.drawOn(self.c, curr_x + 0.15 * cm, h_y + (header_h - ph) / 2)
                curr_x += widths[i]
            self.c.restoreState()

            self.y_cursor -= (header_h + 0.1 * cm)

        # Keep the header with at least one row
        self._ensure_space(header_h + 0.1 * cm + 0.85 * cm)
        draw_header()

        # 2. Draw Rows with dynamic auto-wrap (the header repeats on continuation pages)
        for r_idx, row in enumerate(rows):
            if not isinstance(row, (list, tuple)):
                row = [row]
            # Pre-wrap all cells in this row to determine required row height
            cell_items = []
            max_row_h = 0.85 * cm

            for c_idx in range(n_cols):
                w = widths[c_idx]
                cell = row[c_idx] if c_idx < len(row) else ""

                if isinstance(cell, dict):
                    cell_items.append(("input", cell, 0.7 * cm))
                else:
                    c_str = str(cell).strip()
                    if not c_str:
                        # Empty cell: treat as interactive rating / tick box or input zone
                        cell_items.append(("empty", "", 0.65 * cm))
                    else:
                        p_cell = Paragraph(escape(c_str), style_cell)
                        _, ch = p_cell.wrap(w - 0.3 * cm, 300)
                        cell_items.append(("text", p_cell, ch))
                        max_row_h = max(max_row_h, ch + 0.3 * cm)

            row_h = max_row_h
            if self._ensure_space(row_h):
                draw_header()
            r_y = self.y_cursor - row_h

            # Draw row background
            self.c.saveState()
            row_bg = PDFStyle.COLOR_WHITE if r_idx % 2 == 0 else PDFStyle.COLOR_CARD_CREME
            self.c.setFillColor(row_bg)
            self.c.setStrokeColor(PDFStyle.COLOR_LINE)
            self.c.setLineWidth(0.5)
            self.c.roundRect(self.text_x, r_y, self.target_width, row_h, 2, fill=1, stroke=1)

            curr_x = self.text_x
            for c_idx, item in enumerate(cell_items):
                w = widths[c_idx]
                kind = item[0]

                if kind == "input":
                    cell_dict = item[1]
                    fid = cell_dict.get("field_id", f"{field_prefix}_r{r_idx+1}_c{c_idx+1}")
                    placeholder = cell_dict.get("placeholder", "")
                    create_input_field(
                        self.form,
                        fid,
                        pos=(curr_x + 0.12 * cm, r_y + 0.1 * cm),
                        size=(w - 0.24 * cm, row_h - 0.2 * cm),
                        multiline=False,
                        tooltip=placeholder,
                        fill_color=PDFStyle.COLOR_WHITE,
                    )
                elif kind == "empty":
                    # For empty middle/rating columns, provide 3 evaluation score checkboxes
                    fid = f"{field_prefix}_r{r_idx+1}_c{c_idx+1}"
                    # Draw 3 miniature status indicators
                    dot_y = r_y + (row_h - 10) / 2
                    col_center_x = curr_x + w / 2
                    create_checkbox(
                        self.form,
                        f"{fid}_chk",
                        pos=(col_center_x - 5, dot_y),
                        size=10,
                        tooltip="Cocher le niveau",
                    )
                else:
                    p_cell, ch = item[1], item[2]
                    p_cell.drawOn(self.c, curr_x + 0.15 * cm, r_y + (row_h - ch) / 2)

                curr_x += w

            self.c.restoreState()
            self.y_cursor -= (row_h + 0.08 * cm)

        self.y_cursor -= 0.4 * cm
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
        h = 2.2 * cm
        self._ensure_space(h)
        box_y = self.y_cursor - h

        colors_list = [
            PDFStyle.COLOR_ACCENT_BLUE,
            PDFStyle.COLOR_ACCENT_RED,
            PDFStyle.COLOR_SUCCESS,
        ]

        for i, st in enumerate(stats):
            b_x = self.text_x + i * (box_w + gap)
            val = (st.get("value") or st.get("stat", "")) if isinstance(st, dict) else str(st[0] if isinstance(st, (tuple, list)) else st)
            lbl = st.get("label", "") if isinstance(st, dict) else str(st[1] if isinstance(st, (tuple, list)) and len(st) > 1 else "")
            color = colors_list[i % len(colors_list)]

            self.c.saveState()
            self.c.setFillColor(PDFStyle.COLOR_CARD_CREME)
            self.c.setStrokeColor(PDFStyle.COLOR_LINE)
            self.c.setLineWidth(0.5)
            self.c.roundRect(b_x, box_y, box_w, h, 4, fill=1, stroke=1)

            val_str = str(val).strip()
            # Dynamic font sizing for stat number
            if len(val_str) > 14:
                val_font_size = 11
            elif len(val_str) > 9:
                val_font_size = 13.5
            else:
                val_font_size = 16.5
            # Narrow boxes (3-4 stats): shrink further, then show '…' rather than overflow
            val_font_size = fit_font_size(val_str, PDFStyle.FONT_BRANDING, val_font_size, box_w - 0.3 * cm, min_size=8)
            val_str = ellipsize(val_str, PDFStyle.FONT_BRANDING, val_font_size, box_w - 0.3 * cm)

            # Wrap label if needed (2 lines fit; the second ends with '…' if more is needed)
            lbl_str = str(lbl).upper().strip()
            lbl_w = box_w - 0.4 * cm
            lbl_lines = simpleSplit(lbl_str, PDFStyle.FONT_SUBTITLE, 7.0, lbl_w) if lbl_str else []
            if len(lbl_lines) > 2:
                lbl_lines = [lbl_lines[0], ellipsize(" ".join(lbl_lines[1:]), PDFStyle.FONT_SUBTITLE, 7.0, lbl_w)]

            if len(lbl_lines) > 1:
                val_y = box_y + 1.25 * cm
            else:
                val_y = box_y + 1.1 * cm

            # Stat number
            self.c.setFont(PDFStyle.FONT_BRANDING, val_font_size)
            self.c.setFillColor(color)
            self.c.drawCentredString(b_x + box_w / 2.0, val_y, val_str)

            # Stat label
            if lbl_lines:
                self.c.setFont(PDFStyle.FONT_SUBTITLE, 7.0)
                self.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
                if len(lbl_lines) == 1:
                    self.c.drawCentredString(b_x + box_w / 2.0, box_y + 0.35 * cm, lbl_lines[0])
                else:
                    self.c.drawCentredString(b_x + box_w / 2.0, box_y + 0.48 * cm, lbl_lines[0])
                    self.c.drawCentredString(b_x + box_w / 2.0, box_y + 0.22 * cm, lbl_lines[1])

            self.c.restoreState()

        self.y_cursor -= (h + 0.5 * cm)
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
