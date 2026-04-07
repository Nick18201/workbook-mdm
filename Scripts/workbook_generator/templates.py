from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
import logging
from dataclasses import dataclass
from .config import PDFStyle
from .components import (
    draw_page_background, draw_side_panel, draw_title,
    draw_page_decorations, draw_card
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
    color_alternation: bool = True

@dataclass
class TextConfig:
    style_choice: str = 'body'
    font_size: int = 11
    color: str = PDFStyle.COLOR_TEXT_MAIN
    spacing_after: float = 0.5 * cm
    align: str = 'left'

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
        draw_page_background(self.c, self.width, self.height, use_blobs=config.use_blobs)

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
            new_y = draw_title(self.c, self.title, pos=(self.text_x, self.title_y), available_width=self.target_width)
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

        if config.style_choice == 'body':
            font_name = PDFStyle.FONT_BODY
        elif config.style_choice == 'italic':
            font_name = PDFStyle.FONT_ITALIC
        elif config.style_choice == 'subtitle':
            font_name = PDFStyle.FONT_SUBTITLE
        else:
            font_name = PDFStyle.FONT_BODY

        self.c.setFont(font_name, config.font_size)
        self.c.setFillColor(config.color)

        lines = simpleSplit(text, font_name, config.font_size, self.target_width)
        for line in lines:
            if config.align == 'center':
                self.c.drawCentredString(self.text_x + self.target_width/2, self.y_cursor, line)
            elif config.align == 'right':
                self.c.drawRightString(self.text_x + self.target_width, self.y_cursor, line)
            else:
                self.c.drawString(self.text_x, self.y_cursor, line)
            self.y_cursor -= config.font_size + 0.1 * cm # Roughly line height

        self.y_cursor -= config.spacing_after
        return self.y_cursor

    def add_question_block(self, question, form_field_id, config: QuestionConfig = None):
        """Adds a standard question block and its AcroForm input."""
        if config is None:
            config = QuestionConfig()

        if config.color_alternation:
            color = PDFStyle.COLOR_ACCENT_BLUE if self.question_index % 2 == 0 else PDFStyle.COLOR_ACCENT_RED
        else:
            color = PDFStyle.COLOR_ACCENT_BLUE

        self.add_text(question, config=TextConfig(style_choice='subtitle', font_size=11, color=color, spacing_after=0.1*cm))

        if config.subtitle:
            self.add_text(config.subtitle, config=TextConfig(style_choice='body', font_size=10, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.1*cm))

        self.y_cursor -= 0.2 * cm # Gap before input

        # Check if we need to paginate (basic protection)
        if self.y_cursor - config.box_height < 3 * cm:
            logger.warning(f"Form field '{form_field_id}' might overflow bottom margin.")

        create_input_field(self.form, form_field_id, pos=(self.text_x, self.y_cursor - config.box_height), size=(self.target_width, config.box_height),
            multiline=True
        )

        self.y_cursor -= (config.box_height + 0.8 * cm)
        self.question_index += 1
        return self.y_cursor

    def add_space(self, height):
        self.y_cursor -= height
        return self.y_cursor

    def render(self):
        """Finalizes the page with decorations."""
        draw_page_decorations(self.c, self.width, self.height, part_title=self.part_title, x_offset=self.card_margin)
        self.c.showPage()
