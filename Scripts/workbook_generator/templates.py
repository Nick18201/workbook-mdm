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
)
from .forms import create_input_field

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
