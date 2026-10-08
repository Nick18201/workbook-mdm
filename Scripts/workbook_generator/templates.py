import logging
from xml.sax.saxutils import escape
from dataclasses import dataclass
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from .config import PDFStyle
from .components import (
    HINT_LEADING,
    HINT_SIZE,
    QUESTION_LEADING,
    QUESTION_SIZE,
    choice_scale_height,
    draw_answer_box,
    draw_choice_scale,
    draw_question,
    question_text_height,
)
from .drawn_blocks import draw_life_line, draw_tree_of_life
from .forms import create_checkbox, create_radio, reserve_field_name
from .utils import french_typography
from .primitives import (
    content_frame,
    draw_annotation,
    draw_card_title,
    draw_drawn_arrow,
    draw_eyebrow,
    draw_folio,
    draw_frise,
    draw_icon,
    draw_icon_badge,
    draw_label_pill,
    draw_page_head,
    draw_paragraph,
    draw_pastel_card,
    draw_rule,
    draw_star,
    draw_star_list,
    draw_text,
    draw_white_card,
    first_baseline,
    label_pill_size,
    paragraph_height,
    text_width,
    fit_text,
    pastel_cycle,
    star_list_height,
    wrap_text,
)

logger = logging.getLogger(__name__)

# Fixed texts of the common template of the carnets (never customized). The safety
# protocol of a heavy exercise follows James Pennebaker's expressive writing: a warning,
# a strict right to leave it blank, and an anchoring sentence to close it.
PROTOCOL_WARNING = "Les questions qui suivent sont franches et peuvent remuer. Prenez-les à votre rythme."
PROTOCOL_OPTIONAL = ("Si cet exercice vous semble trop lourd à faire hors séance, laissez-le vierge : "
                     "nous l'aborderons ensemble.")
ANCHOR_PROMPT = "Aujourd'hui, avec le recul, je sais que…"
ENERGY_PROMPT = "Votre niveau d'énergie aujourd'hui :"
ENERGY_REASON = "Ce chiffre s'explique surtout par…"


@dataclass
class LayoutConfig:
    part_title: str = ""  # eyebrow above the page title
    y_start: float = None


@dataclass
class QuestionConfig:
    box_height: float = 3.0 * cm
    subtitle: str = None
    example: str = None


@dataclass
class QuestionItem:
    question: str
    form_field_id: str
    subtitle: str = None
    example: str = None
    box_height: float = None  # None for auto-fit


@dataclass
class TextConfig:
    style_choice: str = "body"  # 'body', 'italic', 'subtitle' (DM Sans 700)
    font_size: float = None  # PDFStyle.SIZE_BODY
    color: object = None  # ink
    spacing_after: float = 0.5 * cm
    align: str = "left"


class PageLayout:
    """
    Vertical flow layout of a content page: an eyebrow (part_title) and the page title
    with its accent, then blocks added one below the other, and the folio.
    - Cursor tracking prevents overlapping elements.
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
        self.text_x, self.target_width = content_frame()
        self.card_margin = self.text_x  # former name
        # Lowest point a block may reach; the folio sits below
        self.bottom_limit = PDFStyle.CONTENT_BOTTOM

        self.question_index = 0
        self.form = self.c.acroForm
        # Page where the current block starts: set to None before a block, it takes the page
        # of its first _ensure_space (compiler.py records it for the block's data id)
        self.block_page = None

        self._start_page(title)
        if config.y_start is not None:
            self.y_cursor = config.y_start
            self._page_top = self.y_cursor

    def _start_page(self, title, suffix=""):
        """Draws the page head (eyebrow and title) and puts the cursor below it."""
        bottom = draw_page_head(self.c, title, eyebrow=self.part_title, suffix=suffix)
        self.y_cursor = bottom - (0.6 * cm if title else 0)
        self._page_top = self.y_cursor

    def _new_page(self):
        """Finishes the current page and starts a continuation page."""
        self.render()
        self._start_page(self.title, suffix="(suite)" if self.title else "")

    def _ensure_space(self, height):
        """
        Starts a continuation page when a block of this height would run past the bottom
        margin (unless the page is still empty). Returns True when a new page was started,
        so callers can redraw what must repeat (e.g. a table header).
        """
        if self.y_cursor - height < self.bottom_limit and self.y_cursor < self._page_top:
            self._new_page()
            started = True
        else:
            started = False
        if self.block_page is None:
            self.block_page = self.c.getPageNumber()
        return started

    def _question_text_height(self, question, subtitle=None, example=None):
        """Vertical space taken by a question block, input box excluded (matches add_question_block)."""
        return question_text_height(self.target_width, question, subtitle, example) + 0.45 * cm

    def add_text(self, text, config: TextConfig = None):
        """Adds a paragraph of text, automatically wrapping and moving the cursor."""
        if config is None:
            config = TextConfig()

        font_name = {
            "italic": PDFStyle.FONT_HEADING_ITALIC,
            "subtitle": PDFStyle.FONT_HEADING_BOLD,
        }.get(config.style_choice, PDFStyle.FONT_BODY)
        size = config.font_size or PDFStyle.SIZE_BODY
        color = config.color or PDFStyle.COLOR_INK
        leading = size * PDFStyle.LEADING_BODY

        for line in wrap_text(str(text), font_name, size, self.target_width):
            self._ensure_space(leading)
            draw_paragraph(self.c, line, self.text_x, self.y_cursor, self.target_width, font_name, size, color,
                           leading, align=config.align)
            self.y_cursor -= leading

        self.y_cursor -= config.spacing_after
        return self.y_cursor

    def add_question_block(self, question, form_field_id, config: QuestionConfig = None):
        """Adds a question (DM Sans 700, hint and example in ink-muted) and its answer box."""
        if config is None:
            config = QuestionConfig()

        box_h = config.box_height if config.box_height is not None else 3.0 * cm
        # Keep the question, its hints and its answer box together on one page
        self._ensure_space(question_text_height(self.target_width, question, config.subtitle, config.example) + box_h)
        bottom = draw_question(
            self.c, self.text_x, self.y_cursor, self.target_width, question, form_field_id, box_h,
            subtitle=config.subtitle, example=config.example,
        )
        self.y_cursor = bottom - 0.45 * cm
        self.question_index += 1
        return self.y_cursor

    def add_questions_group(
        self,
        questions,
        min_box_height: float = 2.2 * cm,
        max_box_height: float = 7.5 * cm,
        safe_bottom_margin: float = None,
    ):
        """
        Adds a group of questions dynamically auto-fitting available vertical space
        so that boxes scale proportionally and never overflow the bottom margin.

        Args:
            questions (list): List of QuestionItem instances, dicts, or tuples.
            min_box_height (float): Minimum height for each text area (default 2.2 cm).
            max_box_height (float): Maximum height for each text area (default 7.5 cm).
            safe_bottom_margin (float): Lowest point of the boxes (default: the page's bottom limit).
        """
        if not questions:
            return self.y_cursor
        if safe_bottom_margin is None:
            safe_bottom_margin = self.bottom_limit

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
                        box_height=q.get("box_height"),
                    )
                )
            elif isinstance(q, (tuple, list)):
                q_text = q[0]
                q_id = q[1] if len(q) > 1 else f"q_{self.question_index}_{len(norm_questions)}"
                q_sub = q[2] if len(q) > 2 else None
                norm_questions.append(QuestionItem(question=q_text, form_field_id=q_id, subtitle=q_sub))
            else:
                norm_questions.append(
                    QuestionItem(question=str(q), form_field_id=f"q_{self.question_index}_{len(norm_questions)}")
                )

        overheads = [self._question_text_height(q.question, q.subtitle, q.example) for q in norm_questions]
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
        total_text_overhead = sum(overheads)
        fixed_height_sum = sum(q.box_height for q in questions if q.box_height is not None)
        n_auto = sum(1 for q in questions if q.box_height is None)

        available_space = self.y_cursor - safe_bottom_margin
        remaining_for_boxes = available_space - total_text_overhead - fixed_height_sum

        if n_auto > 0:
            auto_box_h = max(1.5 * cm, min(max_box_height, remaining_for_boxes / n_auto))
        else:
            auto_box_h = min_box_height

        for q in questions:
            target_h = q.box_height if q.box_height is not None else auto_box_h
            cfg = QuestionConfig(box_height=target_h, subtitle=q.subtitle, example=q.example)
            self.add_question_block(q.question, q.form_field_id, config=cfg)

    def add_callout(self, text, title=None, variant="info", height=None):
        """
        Inset (advice, reminder, quote): a card with a pill label. 'info' and 'tip' are
        pastel cards (the document pastel, almond for a tip); 'quote' is a white card whose
        text is set in Instrument Serif italic.
        """
        pad = PDFStyle.CARD_PADDING
        inner_w = self.target_width - 2 * pad
        label = title or {"tip": "Conseil", "quote": "Citation"}.get(variant, "À retenir")
        if variant == "quote":
            font, size, leading = PDFStyle.FONT_SERIF, 13, 13 * 1.35
        else:
            font, size, leading = PDFStyle.FONT_BODY, PDFStyle.SIZE_BODY, PDFStyle.SIZE_BODY * PDFStyle.LEADING_BODY

        _, pill_h = label_pill_size(label)
        text_h = paragraph_height(text, inner_w, font, size, leading)
        computed_h = 2 * pad + pill_h + 0.3 * cm + text_h
        h = max(height or computed_h, computed_h, 1.6 * cm)

        self._ensure_space(h)
        card_y = self.y_cursor - h
        if variant == "quote":
            draw_white_card(self.c, self.text_x, card_y, self.target_width, h)
            pill_variant = "pastel"
        else:
            color = PDFStyle.COLOR_ALMOND if variant == "tip" else None
            draw_pastel_card(self.c, self.text_x, card_y, self.target_width, h, color=color)
            pill_variant = "on_pastel"

        draw_label_pill(self.c, self.text_x + pad, self.y_cursor - pad - pill_h, label, variant=pill_variant,
                        max_width=inner_w)
        draw_paragraph(self.c, text, self.text_x + pad, self.y_cursor - pad - pill_h - 0.3 * cm, inner_w,
                       font, size, PDFStyle.COLOR_INK, leading)

        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_cards_grid(self, cards, columns=2, card_height=None, field_prefix="grid"):
        """
        Grid of pastel cards (1 to 4 columns), each with a title, a hint and an answer box.
        Titles and hints wrap; a card is at least tall enough for its texts.
        """
        if not cards:
            return self.y_cursor

        cols = max(1, min(columns, 4))
        gap = 0.4 * cm
        col_w = (self.target_width - (cols - 1) * gap) / cols
        pad = 0.45 * cm
        inner_w = col_w - 2 * pad
        title_size = 12 if cols <= 2 else 10.5
        title_lead = title_size * 1.25
        sub_size = HINT_SIZE if cols <= 2 else 8.5
        sub_lead = sub_size * 1.4
        min_box = 1.4 * cm

        parsed = []
        for idx, card in enumerate(cards):
            if isinstance(card, dict):
                parsed.append((str(card.get("title", f"Carte {idx+1}")), str(card.get("subtitle", "") or ""),
                               card.get("field_id", f"{field_prefix}_{idx+1}"), str(card.get("placeholder", "") or "")))
            elif isinstance(card, (tuple, list)):
                parsed.append((str(card[0]), str(card[1]) if len(card) > 1 else "",
                               card[2] if len(card) > 2 else f"{field_prefix}_{idx+1}", ""))
            else:
                parsed.append((str(card), "", f"{field_prefix}_{idx+1}", ""))

        def texts_height(c_title, c_sub):
            h = paragraph_height(c_title, inner_w, PDFStyle.FONT_HEADING_BOLD, title_size, title_lead)
            if c_sub:
                h += 2 + paragraph_height(c_sub, inner_w, PDFStyle.FONT_BODY, sub_size, sub_lead)
            return h

        pastels = pastel_cycle(self.c)
        for r_idx in range(0, len(parsed), cols):
            row = parsed[r_idx:r_idx + cols]
            texts_h = max(texts_height(t, s) for t, s, _, _ in row)
            default_h = 5.0 * cm if cols <= 2 else 4.4 * cm
            h = max(card_height or default_h, 2 * pad + texts_h + 0.3 * cm + min_box)
            self._ensure_space(h)
            row_y = self.y_cursor - h
            for c_idx, (c_title, c_sub, c_fid, c_placeholder) in enumerate(row):
                card_x = self.text_x + c_idx * (col_w + gap)
                draw_pastel_card(self.c, card_x, row_y, col_w, h, color=pastels[(r_idx + c_idx) % 2])
                t = self.y_cursor - pad
                t -= draw_paragraph(self.c, c_title, card_x + pad, t, inner_w, PDFStyle.FONT_HEADING_BOLD,
                                    title_size, PDFStyle.COLOR_INK, title_lead)
                if c_sub:
                    t -= 2 + draw_paragraph(self.c, c_sub, card_x + pad, t - 2, inner_w, PDFStyle.FONT_BODY,
                                            sub_size, PDFStyle.COLOR_INK_MUTED, sub_lead)
                t -= 0.3 * cm
                draw_answer_box(self.c, card_x + pad, row_y + pad, inner_w, t - (row_y + pad), c_fid,
                                tooltip=c_placeholder or c_title)
            self.y_cursor -= h + gap

        self.y_cursor -= PDFStyle.GAP_BLOCK - gap
        return self.y_cursor

    def add_scale_gauge(self, label, min_val=0, max_val=10, min_label="", max_label="", field_id=None):
        """
        Single-choice rating scale: the label, then one pastille per value (radio buttons
        of one group). A long label wraps.
        """
        fid_base = field_id or f"scale_{self.question_index}"
        self.question_index += 1

        label = str(label)
        pad = 0.45 * cm
        inner_w = self.target_width - 2 * pad
        label_h = paragraph_height(label, inner_w, PDFStyle.FONT_HEADING_BOLD,
                                   PDFStyle.SIZE_TITLE_ELEMENT, PDFStyle.SIZE_TITLE_ELEMENT * 1.3)
        scale_h = choice_scale_height(bool(min_label or max_label))
        card_h = 2 * pad + label_h + 6 + scale_h
        self._ensure_space(card_h)

        draw_pastel_card(self.c, self.text_x, self.y_cursor - card_h, self.target_width, card_h,
                         color=pastel_cycle(self.c)[1], radius=12)
        top = self.y_cursor - pad
        top -= draw_paragraph(self.c, label, self.text_x + pad, top, inner_w, PDFStyle.FONT_HEADING_BOLD,
                              PDFStyle.SIZE_TITLE_ELEMENT, PDFStyle.COLOR_INK, PDFStyle.SIZE_TITLE_ELEMENT * 1.3) + 6
        group = reserve_field_name(self.form, fid_base)
        scale_w = min(inner_w, (max_val - min_val + 1) * 1.45 * cm)
        draw_choice_scale(self.c, group, self.text_x + pad, top, scale_w,
                          list(range(min_val, max_val + 1)), min_label, max_label, tooltip=label)
        self.y_cursor -= card_h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_checklist(self, items, title=None, columns=1, field_prefix="chk"):
        """Checklist: check boxes with wrapped labels, on one or two columns, under an optional title."""
        if not items:
            return self.y_cursor

        cols = max(1, min(columns, 2))
        gap_x = 0.6 * cm
        col_w = self.target_width if cols == 1 else (self.target_width - gap_x) / 2.0
        size = PDFStyle.SIZE_BODY
        leading = size * 1.4
        label_w = col_w - 20

        if title:
            title_h = paragraph_height(str(title), self.target_width, PDFStyle.FONT_HEADING_BOLD,
                                       PDFStyle.SIZE_TITLE_ELEMENT, PDFStyle.SIZE_TITLE_ELEMENT * 1.3)
            # Keep the title with at least the first row
            self._ensure_space(title_h + 6 + leading + 6)
            self.y_cursor -= draw_paragraph(self.c, str(title), self.text_x, self.y_cursor, self.target_width,
                                            PDFStyle.FONT_HEADING_BOLD, PDFStyle.SIZE_TITLE_ELEMENT,
                                            PDFStyle.COLOR_INK, PDFStyle.SIZE_TITLE_ELEMENT * 1.3) + 6

        entries = []
        for idx, item in enumerate(items):
            if isinstance(item, dict):
                label, fid = item.get("label", str(item)), item.get("field_id", f"{field_prefix}_{idx+1}")
            elif isinstance(item, (tuple, list)):
                label, fid = item[0], item[1] if len(item) > 1 else f"{field_prefix}_{idx+1}"
            else:
                label, fid = str(item), f"{field_prefix}_{idx+1}"
            entries.append((str(label), fid))

        for r in range(0, len(entries), cols):
            row = entries[r:r + cols]
            row_h = max(paragraph_height(label, label_w, PDFStyle.FONT_BODY, size, leading) for label, _ in row) + 6
            self._ensure_space(row_h)
            for c_idx, (label, fid) in enumerate(row):
                item_x = self.text_x + c_idx * (col_w + gap_x)
                box_y = self.y_cursor - (leading - size) / 2 - 0.8 * size - 1
                create_checkbox(self.form, fid, pos=(item_x, box_y), size=11, tooltip=label)
                draw_paragraph(self.c, label, item_x + 20, self.y_cursor, label_w, PDFStyle.FONT_BODY, size,
                               PDFStyle.COLOR_INK, leading)
            self.y_cursor -= row_h

        self.y_cursor -= PDFStyle.GAP_BLOCK - 6
        return self.y_cursor

    def add_table(self, headers, rows, col_widths=None, field_prefix="tbl", field_height=None):
        """
        Table: a white header row in PT Mono, then rows separated by rules. A dict cell is an
        answer field, an empty cell a check box; text cells wrap. The header repeats on
        continuation pages. field_height sets the height of the answer fields (one line by
        default); fields taller than 1.2 cm take several lines.
        """
        n_cols = len(headers)
        if n_cols == 0:
            return self.y_cursor

        if col_widths is None:
            if n_cols == 3:
                widths = [0.30 * self.target_width, 0.22 * self.target_width, 0.48 * self.target_width]
            elif n_cols == 2:
                widths = [0.40 * self.target_width, 0.60 * self.target_width]
            else:
                widths = [self.target_width / n_cols] * n_cols
        else:
            widths = col_widths

        cell_pad = 0.2 * cm
        style_th = ParagraphStyle(
            "TableTH", fontName=PDFStyle.FONT_LABEL, fontSize=7.5, leading=10,
            textColor=PDFStyle.COLOR_INK_MUTED,
        )
        style_cell = ParagraphStyle(
            "TableCell", fontName=PDFStyle.FONT_BODY, fontSize=9, leading=12.5,
            textColor=PDFStyle.COLOR_INK,
        )

        th_paragraphs = []
        max_th_h = 0
        for i, h_text in enumerate(headers):
            p_th = Paragraph(escape(french_typography(str(h_text)).upper()), style_th)
            _, ph = p_th.wrap(widths[i] - 2 * cell_pad, 200)
            th_paragraphs.append((p_th, ph))
            max_th_h = max(max_th_h, ph)
        header_h = max(0.75 * cm, max_th_h + 0.35 * cm)

        def draw_header():
            h_y = self.y_cursor - header_h
            self.c.saveState()
            self.c.setFillColor(PDFStyle.COLOR_SURFACE_CARD)
            self.c.roundRect(self.text_x, h_y, self.target_width, header_h, 6, fill=1, stroke=0)
            self.c.restoreState()
            curr_x = self.text_x
            for i, (p_th, ph) in enumerate(th_paragraphs):
                p_th.drawOn(self.c, curr_x + cell_pad, h_y + (header_h - ph) / 2)
                curr_x += widths[i]
            self.y_cursor -= header_h

        # Keep the header with at least one row
        self._ensure_space(header_h + 0.95 * cm)
        draw_header()

        for r_idx, row in enumerate(rows):
            if not isinstance(row, (list, tuple)):
                row = [row]
            cell_items = []
            row_h = 0.95 * cm
            if field_height and any(isinstance(cell, dict) for cell in row):
                row_h = max(row_h, field_height + 8)
            for c_idx in range(n_cols):
                w = widths[c_idx]
                cell = row[c_idx] if c_idx < len(row) else ""
                if isinstance(cell, dict):
                    cell_items.append(("input", cell, 0))
                else:
                    c_str = str(cell).strip()
                    if not c_str:
                        cell_items.append(("empty", "", 0))
                    else:
                        p_cell = Paragraph(escape(french_typography(c_str)), style_cell)
                        _, ch = p_cell.wrap(w - 2 * cell_pad, 300)
                        cell_items.append(("text", p_cell, ch))
                        row_h = max(row_h, ch + 0.4 * cm)

            if self._ensure_space(row_h):
                draw_header()
            r_y = self.y_cursor - row_h

            curr_x = self.text_x
            for c_idx, (kind, value, ch) in enumerate(cell_items):
                w = widths[c_idx]
                if kind == "input":
                    fid = value.get("field_id", f"{field_prefix}_r{r_idx+1}_c{c_idx+1}")
                    draw_answer_box(self.c, curr_x + 3, r_y + 4, w - 6, row_h - 8, fid,
                                    tooltip=value.get("placeholder", ""),
                                    multiline=field_height is not None and row_h - 8 > 1.2 * cm)
                elif kind == "empty":
                    fid = f"{field_prefix}_r{r_idx+1}_c{c_idx+1}"
                    create_checkbox(self.form, f"{fid}_chk", pos=(curr_x + w / 2 - 5.5, r_y + (row_h - 11) / 2),
                                    size=11, tooltip="Cocher le niveau")
                else:
                    value.drawOn(self.c, curr_x + cell_pad, r_y + (row_h - ch) / 2)
                curr_x += w

            draw_rule(self.c, self.text_x, self.text_x + self.target_width, r_y)
            self.y_cursor -= row_h

        self.y_cursor -= PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_stat_boxes(self, stats):
        """A row of 2 to 4 key figures: white cards with the value in PT Mono blue and a label."""
        if not stats:
            return self.y_cursor

        n = len(stats)
        gap = 0.4 * cm
        box_w = (self.target_width - (n - 1) * gap) / n
        h = 2.3 * cm
        self._ensure_space(h)
        box_y = self.y_cursor - h

        for i, st in enumerate(stats):
            b_x = self.text_x + i * (box_w + gap)
            val = (st.get("value") or st.get("stat", "")) if isinstance(st, dict) else str(st[0] if isinstance(st, (tuple, list)) else st)
            lbl = st.get("label", "") if isinstance(st, dict) else str(st[1] if isinstance(st, (tuple, list)) and len(st) > 1 else "")

            draw_white_card(self.c, b_x, box_y, box_w, h, radius=12)
            val_str = str(val).strip()
            inner = box_w - 0.5 * cm
            size = 20
            while size > 10 and text_width(val_str, PDFStyle.FONT_LABEL, size) > inner:
                size -= 0.5
            val_str = fit_text(val_str, PDFStyle.FONT_LABEL, size, inner)
            draw_text(self.c, b_x + box_w / 2, box_y + h - 0.45 * cm - size * 0.8, val_str, PDFStyle.FONT_LABEL,
                      size, PDFStyle.COLOR_BLUE, align="center")
            if lbl:
                draw_paragraph(self.c, str(lbl).upper(), b_x + 0.25 * cm, box_y + 0.95 * cm, inner, PDFStyle.FONT_LABEL,
                               7, PDFStyle.COLOR_INK_MUTED, 9.5, tracking=PDFStyle.TRACKING_LABEL, align="center",
                               max_lines=2)

        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_space(self, height):
        self.y_cursor -= height
        return self.y_cursor

    def page_break(self):
        """Continues on a new page titled "<title> (suite)" (to share a long exercise evenly)."""
        self._new_page()
        return self.y_cursor

    # --- Reading pages ------------------------------------------------------------

    def add_frise(self, steps, start_label="", end_label=""):
        """The art direction's timeline: steps are (icon, title, marker) on a dotted line."""
        above = 40 if (start_label or end_label) else 22
        below = 15 + 10 + 3 * 12.5 + 14
        self._ensure_space(above + below)
        line_y = self.y_cursor - above
        h = draw_frise(self.c, self.text_x, line_y, self.target_width, steps, start_label, end_label)
        self.y_cursor = line_y - h - PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_heading(self, text, color=None, size=None):
        """A heading inside the page (DM Sans 700), kept with the first lines that follow it."""
        size = size or PDFStyle.SIZE_TITLE_CARD
        leading = size * 1.25
        h = paragraph_height(text, self.target_width, PDFStyle.FONT_HEADING_BOLD, size, leading)
        self._ensure_space(h + 4 + 2 * PDFStyle.SIZE_BODY * PDFStyle.LEADING_BODY)
        self.y_cursor -= draw_paragraph(self.c, text, self.text_x, self.y_cursor, self.target_width,
                                        PDFStyle.FONT_HEADING_BOLD, size, color or PDFStyle.COLOR_INK, leading) + 4
        return self.y_cursor

    def add_paragraphs(self, paragraphs, gap=0.3 * cm, spacing_after=None, color=None, size=None):
        """
        Running text: one paragraph per item, and runs of items starting with '• ' as a
        star list. Long text continues on the next page line by line.
        """
        bullets = []
        for i, paragraph in enumerate(paragraphs):
            paragraph = str(paragraph).strip()
            if paragraph.startswith("•"):
                bullets.append(paragraph.lstrip("• ").strip())
            elif paragraph:
                if bullets:
                    self.add_star_list(bullets, spacing_after=gap)
                    bullets = []
                self.add_text(paragraph, TextConfig(spacing_after=gap, color=color, font_size=size))
        if bullets:
            self.add_star_list(bullets, spacing_after=gap)
        self.y_cursor -= (PDFStyle.GAP_BLOCK if spacing_after is None else spacing_after) - gap
        return self.y_cursor

    def add_star_list(self, items, spacing_after=None, size=None):
        """A list with coral-strong star bullets; an item never splits across pages."""
        size = size or PDFStyle.SIZE_BODY
        for i, item in enumerate(items):
            h = star_list_height([item], self.target_width, size)
            self._ensure_space(h)
            draw_star_list(self.c, [item], self.text_x, self.y_cursor, self.target_width, size)
            self.y_cursor -= h + (size * 0.75 if i < len(items) - 1 else 0)
        self.y_cursor -= PDFStyle.GAP_BLOCK if spacing_after is None else spacing_after
        return self.y_cursor

    def add_annotation(self, text, arrow=True, width_ratio=0.55):
        """
        The page's handwritten touch: a short note in Instrument Serif italic, slightly
        turned, on the right, with the drawn arrow pointing back up to the content.
        """
        width = self.target_width * width_ratio
        x = self.text_x + self.target_width - width
        size = PDFStyle.SIZE_ANNOTATION
        h = paragraph_height(text, width, PDFStyle.FONT_SERIF, size, size * 1.3)
        self._ensure_space(h + 0.5 * cm)
        top = self.y_cursor - 0.2 * cm
        draw_annotation(self.c, x, top, text, width)
        if arrow:
            draw_drawn_arrow(self.c, x - 1.9 * cm, top - h / 2 - 0.1 * cm, width=1.5 * cm, flip=True)
        self.y_cursor = top - h - PDFStyle.GAP_BLOCK
        return self.y_cursor

    # --- Form blocks --------------------------------------------------------------

    FIELD_LABEL_SIZE = 7.5
    FIELD_LABEL_LEADING = 10

    QUESTION_LABEL_SIZE = 10
    QUESTION_LABEL_LEADING = 13

    def _field_label_height(self, label, width, questions=False):
        if questions:
            return paragraph_height(label, width, PDFStyle.FONT_HEADING_BOLD, self.QUESTION_LABEL_SIZE,
                                    self.QUESTION_LABEL_LEADING)
        lines = wrap_text(str(label).upper(), PDFStyle.FONT_LABEL, self.FIELD_LABEL_SIZE, width,
                          PDFStyle.TRACKING_LABEL)
        return min(len(lines), 2) * self.FIELD_LABEL_LEADING

    def _draw_field_label(self, label, x, top, width, questions=False):
        if questions:
            return draw_paragraph(self.c, label, x, top, width, PDFStyle.FONT_HEADING_BOLD, self.QUESTION_LABEL_SIZE,
                                  PDFStyle.COLOR_INK, self.QUESTION_LABEL_LEADING)
        return draw_paragraph(self.c, str(label).upper(), x, top, width, PDFStyle.FONT_LABEL, self.FIELD_LABEL_SIZE,
                              PDFStyle.COLOR_INK_MUTED, self.FIELD_LABEL_LEADING, tracking=PDFStyle.TRACKING_LABEL,
                              max_lines=2)

    def add_fields_card(self, rows, title=None, hint=None, color=None, field_height=0.85 * cm, question_labels=False):
        """
        A pastel card of labelled answer boxes laid out in rows (an experience sheet, a job
        sheet, a contact card...). rows: lists of fields, each (label, field_id) or
        (label, field_id, height_cm) or (label, field_id, height_cm, weight); boxes taller
        than 1.2 cm are multiline. title is a pill label, hint a line of ink-muted text.
        Labels are PT Mono markers, or short questions in DM Sans with question_labels.
        """
        pad = PDFStyle.CARD_PADDING
        inner = self.target_width - 2 * pad
        col_gap, row_gap, label_gap = 0.4 * cm, 0.35 * cm, 3

        def parse(field):
            label, fid = field[0], field[1]
            height = field[2] * cm if len(field) > 2 and field[2] else field_height
            weight = field[3] if len(field) > 3 else 1
            return label, fid, height, weight

        layout_rows = []
        for row in rows:
            fields = [parse(f) for f in row]
            total = sum(f[3] for f in fields)
            widths = [(inner - col_gap * (len(fields) - 1)) * f[3] / total for f in fields]
            label_h = max((self._field_label_height(f[0], w, question_labels) for f, w in zip(fields, widths) if f[0]),
                          default=0)
            box_h = max(f[2] for f in fields)
            layout_rows.append((fields, widths, label_h, box_h))

        head_h = 0
        if title:
            head_h += label_pill_size(title)[1] + 0.3 * cm
        if hint:
            head_h += paragraph_height(hint, inner, PDFStyle.FONT_BODY, HINT_SIZE, HINT_LEADING) + 0.25 * cm
        body_h = sum((lh + label_gap if lh else 0) + bh for _, _, lh, bh in layout_rows) + row_gap * (len(layout_rows) - 1)
        h = 2 * pad + head_h + body_h
        self._ensure_space(h)

        draw_pastel_card(self.c, self.text_x, self.y_cursor - h, self.target_width, h, color=color)
        x0, t = self.text_x + pad, self.y_cursor - pad
        if title:
            _, pill_h = draw_label_pill(self.c, x0, t - label_pill_size(title)[1], title, variant="on_pastel",
                                        max_width=inner)
            t -= pill_h + 0.3 * cm
        if hint:
            t -= draw_paragraph(self.c, hint, x0, t, inner, PDFStyle.FONT_BODY, HINT_SIZE, PDFStyle.COLOR_INK_MUTED,
                                HINT_LEADING) + 0.25 * cm
        for fields, widths, label_h, box_h in layout_rows:
            fx = x0
            for (label, fid, height, _), w in zip(fields, widths):
                if label:
                    self._draw_field_label(label, fx, t, w, question_labels)
                box_top = t - (label_h + label_gap if label_h else 0)
                draw_answer_box(self.c, fx, box_top - height, w, height, fid, tooltip=str(label or fid),
                                multiline=height > 1.2 * cm)
                fx += w + col_gap
            t -= (label_h + label_gap if label_h else 0) + box_h + row_gap
        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_numbered_lines(self, columns, count=5, line_height=0.8 * cm, start=1):
        """
        Side by side pastel cards, each with a title, an optional hint and `count` numbered
        one-line answer boxes. columns: [(title, field_prefix) or (title, field_prefix, hint)
        or (title, field_prefix, hint, first)]: `first` numbers that card from another value
        than `start`, so that one ranked list runs over two cards (01 to 05, then 06 to 10).
        """
        n = max(1, min(len(columns), 2))
        gap = 0.45 * cm
        col_w = (self.target_width - gap * (n - 1)) / n
        pad = 0.45 * cm
        inner = col_w - 2 * pad
        number_w = 0.6 * cm
        line_gap = 0.2 * cm

        def head_height(col):
            h = paragraph_height(col[0], inner, PDFStyle.FONT_HEADING_BOLD, PDFStyle.SIZE_TITLE_ELEMENT,
                                 PDFStyle.SIZE_TITLE_ELEMENT * 1.3)
            if len(col) > 2 and col[2]:
                h += 2 + paragraph_height(col[2], inner, PDFStyle.FONT_BODY, HINT_SIZE, HINT_LEADING)
            return h + 0.3 * cm

        head_h = max(head_height(col) for col in columns[:n])
        h = 2 * pad + head_h + count * line_height + (count - 1) * line_gap
        self._ensure_space(h)
        pastels = pastel_cycle(self.c)
        for k, col in enumerate(columns[:n]):
            x = self.text_x + k * (col_w + gap)
            draw_pastel_card(self.c, x, self.y_cursor - h, col_w, h, color=pastels[k % len(pastels)], radius=12)
            t = self.y_cursor - pad
            t2 = t - draw_paragraph(self.c, col[0], x + pad, t, inner, PDFStyle.FONT_HEADING_BOLD,
                                    PDFStyle.SIZE_TITLE_ELEMENT, PDFStyle.COLOR_INK, PDFStyle.SIZE_TITLE_ELEMENT * 1.3)
            if len(col) > 2 and col[2]:
                draw_paragraph(self.c, col[2], x + pad, t2 - 2, inner, PDFStyle.FONT_BODY, HINT_SIZE,
                               PDFStyle.COLOR_INK_MUTED, HINT_LEADING)
            t -= head_h
            first = col[3] if len(col) > 3 and col[3] is not None else start
            for i in range(count):
                box_y = t - line_height
                draw_text(self.c, x + pad, box_y + line_height / 2 - 3, f"{first + i:02d}", PDFStyle.FONT_LABEL, 9,
                          PDFStyle.COLOR_BLUE)
                draw_answer_box(self.c, x + pad + number_w, box_y, inner - number_w, line_height,
                                f"{col[1]}_{first + i}", tooltip=f"{col[0]} {first + i}", multiline=False)
                t -= line_height + line_gap
        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_rating_grid(self, labels, field_prefix, values=None, min_label="", max_label="", title=None):
        """
        One single-choice scale per label, as rows of pastilles in a pastel card (the values
        are written once, above the first row). labels: texts or (text, field_id).
        """
        values = list(values or range(1, 11))
        pad = PDFStyle.CARD_PADDING
        inner = self.target_width - 2 * pad
        label_w = inner * 0.38
        scale_x = self.text_x + pad + label_w + 0.3 * cm
        scale_w = self.text_x + self.target_width - pad - scale_x
        d = 13
        step = (scale_w - d) / max(len(values) - 1, 1)
        row_h = 0.82 * cm
        numbers_h = 12
        footer_h = 14 if (min_label or max_label) else 0
        title_h = label_pill_size(title)[1] + 0.3 * cm if title else 0
        h = 2 * pad + title_h + numbers_h + len(labels) * row_h + footer_h
        self._ensure_space(h)

        draw_pastel_card(self.c, self.text_x, self.y_cursor - h, self.target_width, h)
        t = self.y_cursor - pad
        if title:
            draw_label_pill(self.c, self.text_x + pad, t - label_pill_size(title)[1], title, variant="on_pastel",
                            max_width=inner)
            t -= title_h
        # A value written in words (« En vigilance ») stays inside the card, even above the last pastille
        right = self.text_x + self.target_width - pad / 2
        for k, val in enumerate(values):
            half = text_width(str(val), PDFStyle.FONT_LABEL, 8) / 2
            draw_text(self.c, min(scale_x + d / 2 + k * step, right - half), t - 8, str(val), PDFStyle.FONT_LABEL, 8,
                      PDFStyle.COLOR_INK_MUTED, align="center")
        t -= numbers_h
        for i, item in enumerate(labels):
            text, fid = (item[0], item[1]) if isinstance(item, (tuple, list)) else (item, f"{field_prefix}_{i + 1}")
            cy = t - row_h / 2
            if i:
                draw_rule(self.c, self.text_x + pad, self.text_x + self.target_width - pad, t, color=PDFStyle.COLOR_INK,
                          alpha=0.1)
            draw_text(self.c, self.text_x + pad, cy - 3.5, fit_text(str(text), PDFStyle.FONT_BODY, PDFStyle.SIZE_BODY,
                                                                  label_w), PDFStyle.FONT_BODY, PDFStyle.SIZE_BODY,
                      PDFStyle.COLOR_INK)
            group = reserve_field_name(self.form, fid)
            for k, val in enumerate(values):
                cx = scale_x + d / 2 + k * step
                self.c.saveState()
                self.c.setFillColor(PDFStyle.COLOR_SURFACE_CARD)
                self.c.setStrokeColor(PDFStyle.COLOR_LINE_STRONG)
                self.c.setLineWidth(PDFStyle.LINE_WIDTH_FIELD)
                self.c.circle(cx, cy, d / 2, stroke=1, fill=1)
                self.c.restoreState()
                create_radio(self.form, group, val, pos=(cx - d / 2 + 1, cy - d / 2 + 1), size=d - 2,
                             tooltip=f"{text} : {val}", framed=False)
            t -= row_h
        if footer_h:
            if min_label:
                draw_text(self.c, scale_x, t - 10, str(min_label), PDFStyle.FONT_BODY, HINT_SIZE, PDFStyle.COLOR_INK_MUTED)
            if max_label:
                draw_text(self.c, scale_x + scale_w, t - 10, str(max_label), PDFStyle.FONT_BODY, HINT_SIZE,
                          PDFStyle.COLOR_INK_MUTED, align="right")
        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_info_cards(self, cards, columns=2, check_label=None):
        """
        Pastel cards to read: a two-part title (ink, then blue italic), a text and an
        optional note in ink-muted italic. cards: dicts {title, subtitle, text, note,
        field_id}; with check_label and a field_id, a check box sits under the note
        (« Me correspond »). Each row is as tall as its tallest card.
        """
        cols = max(1, min(columns, 3))
        gap = 0.4 * cm
        col_w = (self.target_width - gap * (cols - 1)) / cols
        pad = 0.45 * cm
        inner = col_w - 2 * pad
        size, leading = PDFStyle.SIZE_BODY_SMALL, PDFStyle.SIZE_BODY_SMALL * 1.4
        title_size = 11.5

        def heights(card):
            h = paragraph_height(card.get("title", ""), inner, PDFStyle.FONT_HEADING_BOLD, title_size, title_size * 1.15)
            if card.get("subtitle"):
                h += paragraph_height(card["subtitle"], inner, PDFStyle.FONT_HEADING_ITALIC, title_size, title_size * 1.15)
            h += 0.2 * cm
            if card.get("text"):
                h += paragraph_height(card["text"], inner, PDFStyle.FONT_BODY, size, leading) + 0.15 * cm
            if card.get("note"):
                h += paragraph_height(card["note"], inner, PDFStyle.FONT_HEADING_ITALIC, size, leading) + 0.15 * cm
            if check_label and card.get("field_id"):
                h += 14
            return h + 2 * pad

        pastels = pastel_cycle(self.c)
        for r in range(0, len(cards), cols):
            row = cards[r:r + cols]
            h = max(heights(card) for card in row)
            self._ensure_space(h)
            for k, card in enumerate(row):
                x = self.text_x + k * (col_w + gap)
                draw_pastel_card(self.c, x, self.y_cursor - h, col_w, h, color=pastels[(r + k) % len(pastels)], radius=12)
                t = self.y_cursor - pad
                t -= draw_card_title(self.c, card.get("title", ""), card.get("subtitle"), x + pad, t, inner,
                                     size=title_size) + 0.2 * cm
                if card.get("text"):
                    t -= draw_paragraph(self.c, card["text"], x + pad, t, inner, PDFStyle.FONT_BODY, size,
                                        PDFStyle.COLOR_INK, leading) + 0.15 * cm
                if card.get("note"):
                    t -= draw_paragraph(self.c, card["note"], x + pad, t, inner, PDFStyle.FONT_HEADING_ITALIC, size,
                                        PDFStyle.COLOR_INK_MUTED, leading) + 0.15 * cm
                if check_label and card.get("field_id"):
                    box_y = self.y_cursor - h + pad
                    create_checkbox(self.form, card["field_id"], pos=(x + pad, box_y), size=10,
                                    tooltip=f"{card.get('title', '')} : {check_label}")
                    draw_text(self.c, x + pad + 15, box_y + 2, check_label.upper(), PDFStyle.FONT_LABEL, 7,
                              PDFStyle.COLOR_INK_MUTED, PDFStyle.TRACKING_LABEL)
            self.y_cursor -= h + gap
        self.y_cursor -= PDFStyle.GAP_BLOCK - gap
        return self.y_cursor

    def add_link_card(self, title, links, color=None):
        """
        A pastel card listing resources: a pill title, then per link a star, the name in
        blue (clickable) and a short description. links: [(name, url, description), ...].
        """
        pad = PDFStyle.CARD_PADDING
        inner = self.target_width - 2 * pad
        size, leading = PDFStyle.SIZE_BODY, PDFStyle.SIZE_BODY * 1.4
        _, pill_h = label_pill_size(title)
        text_x_offset = size * 1.6

        def item_text(name, description):
            return f"{name} : {description}" if description else name

        # 8 pt of slack: the name is set in semibold, wider than the regular text it is measured in
        items_h = [paragraph_height(item_text(n, d), inner - text_x_offset - 8, PDFStyle.FONT_BODY, size, leading)
                   for n, _, d in links]
        h = 2 * pad + pill_h + 0.3 * cm + sum(items_h) + 0.2 * cm * (len(links) - 1)
        self._ensure_space(h)
        draw_pastel_card(self.c, self.text_x, self.y_cursor - h, self.target_width, h, color=color)
        draw_label_pill(self.c, self.text_x + pad, self.y_cursor - pad - pill_h, title, variant="on_pastel",
                        max_width=inner)
        t = self.y_cursor - pad - pill_h - 0.3 * cm
        for (name, url, description), item_h in zip(links, items_h):
            x = self.text_x + pad
            baseline = t - (leading - size) / 2 - 0.8 * size
            draw_star(self.c, x, baseline + 0.36 * size - size * 0.425, size * 0.85)
            # The name in blue semibold, then the description in ink on the same paragraph
            name_w = text_width(name, PDFStyle.FONT_BODY_BOLD, size)
            draw_text(self.c, x + text_x_offset, baseline, name, PDFStyle.FONT_BODY_BOLD, size, PDFStyle.COLOR_BLUE)
            self.c.linkURL(url, (x + text_x_offset, baseline - 2, x + text_x_offset + name_w, baseline + size), relative=0)
            if description:
                rest = wrap_text(f"{name} : {description}", PDFStyle.FONT_BODY, size, inner - text_x_offset - 8)
                first = rest[0][len(name):] if rest[0].startswith(name) else rest[0]
                draw_text(self.c, x + text_x_offset + name_w, baseline, first, PDFStyle.FONT_BODY, size, PDFStyle.COLOR_INK)
                for k, line in enumerate(rest[1:], start=1):
                    draw_text(self.c, x + text_x_offset, baseline - k * leading, line, PDFStyle.FONT_BODY, size,
                              PDFStyle.COLOR_INK)
            t -= item_h + 0.2 * cm
        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_checklist_cards(self, groups, columns=2, field_prefix="chk", item_columns=1):
        """
        Check boxes sorted by category: one pastel card per group (title, items), `columns`
        cards per row, each row as tall as its tallest card. A row never splits across pages.
        """
        cols = max(1, min(columns, 3))
        gap = 0.4 * cm
        col_w = (self.target_width - gap * (cols - 1)) / cols
        pad = 0.4 * cm
        inner = col_w - 2 * pad
        sub_gap = 0.3 * cm
        sub_w = (inner - sub_gap * (item_columns - 1)) / item_columns
        size, leading = PDFStyle.SIZE_BODY_SMALL, PDFStyle.SIZE_BODY_SMALL * 1.35
        box = 9
        label_w = sub_w - box - 5

        def item_rows(items):
            per_col = -(-len(items) // item_columns)
            return [items[k * per_col:(k + 1) * per_col] for k in range(item_columns)]

        def card_height(title, items):
            h = paragraph_height(title, inner, PDFStyle.FONT_HEADING_BOLD, 10.5, 13) + 0.25 * cm
            h += max(sum(paragraph_height(it, label_w, PDFStyle.FONT_BODY, size, leading) + 1 for it in col)
                     for col in item_rows(items))
            return h + 2 * pad

        pastels = pastel_cycle(self.c)
        n = 0
        for r in range(0, len(groups), cols):
            row = groups[r:r + cols]
            h = max(card_height(t, items) for t, items in row)
            self._ensure_space(h)
            for k, (title, items) in enumerate(row):
                x = self.text_x + k * (col_w + gap)
                draw_pastel_card(self.c, x, self.y_cursor - h, col_w, h, color=pastels[(r + k) % len(pastels)], radius=12)
                t = self.y_cursor - pad
                t -= draw_paragraph(self.c, title, x + pad, t, inner, PDFStyle.FONT_HEADING_BOLD, 10.5,
                                    PDFStyle.COLOR_INK, 13) + 0.25 * cm
                for s, col_items in enumerate(item_rows(items)):
                    it_x = x + pad + s * (sub_w + sub_gap)
                    yy = t
                    for item in col_items:
                        n += 1
                        baseline = yy - (leading - size) / 2 - 0.8 * size
                        create_checkbox(self.form, f"{field_prefix}_{n}", pos=(it_x, baseline - 1.5), size=box,
                                        tooltip=str(item))
                        yy -= draw_paragraph(self.c, str(item), it_x + box + 5, yy, label_w, PDFStyle.FONT_BODY, size,
                                             PDFStyle.COLOR_INK, leading) + 1
            self.y_cursor -= h + gap
        self.y_cursor -= PDFStyle.GAP_BLOCK - gap
        return self.y_cursor

    def add_fill_in_card(self, lines, size=None, field_height=0.85 * cm):
        """
        A pastel card of sentences to complete (« Moi, [nom], je décide d'investir [n] heures… »):
        each line mixes texts and one-line answer boxes, (field_id, width, tooltip) with the
        width in cm; a box without width takes the rest of its line.
        """
        size = size or PDFStyle.SIZE_LEAD
        pad, row_gap, gap = PDFStyle.CARD_PADDING, 0.45 * cm, 0.25 * cm
        h = 2 * pad + len(lines) * field_height + (len(lines) - 1) * row_gap
        self._ensure_space(h)
        x, width, top = self.text_x, self.target_width, self.y_cursor
        draw_pastel_card(self.c, x, top - h, width, h)
        row_y = top - pad - field_height
        for line in lines:
            baseline = row_y + field_height / 2 - 0.35 * size
            cursor = x + pad
            for part in line:
                if isinstance(part, str):
                    cursor += draw_text(self.c, cursor, baseline, part, PDFStyle.FONT_BODY, size,
                                        PDFStyle.COLOR_INK) + gap
                    continue
                field_id = part[0]
                box_w = part[1] * cm if len(part) > 1 and part[1] else x + width - pad - cursor
                tooltip = part[2] if len(part) > 2 else field_id
                draw_answer_box(self.c, cursor, row_y, box_w, field_height, field_id, tooltip=tooltip, multiline=False)
                cursor += box_w + gap
            row_y -= field_height + row_gap
        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    # --- Common template of the carnets ---------------------------------------------

    def add_protocol(self, text=None):
        """
        Before a heavy exercise: a white card with a shield badge, « Avant de commencer »,
        the warning (`text`, or PROTOCOL_WARNING) and the right to leave it blank.
        """
        pad = PDFStyle.CARD_PADDING
        badge = 1.0 * cm
        text_x = self.text_x + pad + badge + 0.4 * cm
        inner = self.text_x + self.target_width - pad - text_x
        label = "Avant de commencer"
        warning = str(text or PROTOCOL_WARNING)
        size, leading = PDFStyle.SIZE_BODY, PDFStyle.SIZE_BODY * PDFStyle.LEADING_BODY
        _, pill_h = label_pill_size(label)
        warning_h = paragraph_height(warning, inner, PDFStyle.FONT_BODY, size, leading)
        optional_h = paragraph_height(PROTOCOL_OPTIONAL, inner, PDFStyle.FONT_BODY_BOLD, size, leading)
        h = 2 * pad + max(badge, pill_h + 0.25 * cm + warning_h + 0.1 * cm + optional_h)
        self._ensure_space(h)

        top = self.y_cursor
        draw_white_card(self.c, self.text_x, top - h, self.target_width, h)
        draw_icon_badge(self.c, self.text_x + pad + badge / 2, top - pad - badge / 2, "shield", diameter=badge)
        draw_label_pill(self.c, text_x, top - pad - pill_h, label, max_width=inner)
        t = top - pad - pill_h - 0.25 * cm
        t -= draw_paragraph(self.c, warning, text_x, t, inner, PDFStyle.FONT_BODY, size, PDFStyle.COLOR_INK,
                            leading) + 0.1 * cm
        draw_paragraph(self.c, PROTOCOL_OPTIONAL, text_x, t, inner, PDFStyle.FONT_BODY_BOLD, size, PDFStyle.COLOR_INK,
                       leading)
        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_anchor(self, field_id, box_height=1.6 * cm):
        """After a heavy exercise: « Pour clore », the anchoring sentence (ANCHOR_PROMPT) and its box."""
        pad = PDFStyle.CARD_PADDING
        inner = self.target_width - 2 * pad
        label = "Pour clore"
        _, pill_h = label_pill_size(label)
        prompt_h = paragraph_height(ANCHOR_PROMPT, inner, PDFStyle.FONT_HEADING_BOLD, QUESTION_SIZE, QUESTION_LEADING)
        h = 2 * pad + pill_h + 0.25 * cm + prompt_h + 0.2 * cm + box_height
        self._ensure_space(h)

        top = self.y_cursor
        draw_pastel_card(self.c, self.text_x, top - h, self.target_width, h)
        draw_label_pill(self.c, self.text_x + pad, top - pad - pill_h, label, variant="on_pastel", max_width=inner)
        t = top - pad - pill_h - 0.25 * cm
        t -= draw_paragraph(self.c, ANCHOR_PROMPT, self.text_x + pad, t, inner, PDFStyle.FONT_HEADING_BOLD,
                            QUESTION_SIZE, PDFStyle.COLOR_INK, QUESTION_LEADING) + 0.2 * cm
        draw_answer_box(self.c, self.text_x + pad, t - box_height, inner, box_height, field_id, tooltip=ANCHOR_PROMPT)
        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_contrast_example(self, surface, exploitable, title=None):
        """
        A contrasted example, taken from a neighbouring trade (`title`): the same answer
        « En surface » (white card) and « Exploitable » (pastel card), side by side.
        """
        pad = 0.45 * cm
        arrow_gap = 0.8 * cm
        col_w = (self.target_width - arrow_gap) / 2
        inner = col_w - 2 * pad
        size, leading = PDFStyle.SIZE_BODY, PDFStyle.SIZE_BODY * 1.45
        _, pill_h = label_pill_size("En surface")
        head_h = 8 + 0.3 * cm
        texts_h = max(paragraph_height(str(t or ""), inner, PDFStyle.FONT_HEADING_ITALIC, size, leading)
                      for t in (surface, exploitable))
        card_h = 2 * pad + pill_h + 0.25 * cm + texts_h
        self._ensure_space(head_h + card_h)

        top = self.y_cursor
        draw_eyebrow(self.c, self.text_x, top - 8, f"Exemple · {title}" if title else "Exemple",
                     max_width=self.target_width)
        top -= head_h
        cards = (
            ("En surface", surface, self.text_x, PDFStyle.COLOR_INK_MUTED, "pastel"),
            ("Exploitable", exploitable, self.text_x + col_w + arrow_gap, PDFStyle.COLOR_INK, "on_pastel"),
        )
        for label, text, x, color, pill in cards:
            if pill == "pastel":
                draw_white_card(self.c, x, top - card_h, col_w, card_h, radius=12)
            else:
                draw_pastel_card(self.c, x, top - card_h, col_w, card_h, radius=12)
            draw_label_pill(self.c, x + pad, top - pad - pill_h, label, variant=pill, max_width=inner)
            draw_paragraph(self.c, str(text or ""), x + pad, top - pad - pill_h - 0.25 * cm, inner,
                           PDFStyle.FONT_HEADING_ITALIC, size, color, leading)
        draw_icon(self.c, "arrow_forward", self.text_x + col_w + arrow_gap / 2, top - card_h / 2, 16)
        self.y_cursor = top - card_h - PDFStyle.GAP_BLOCK
        return self.y_cursor

    def add_energy_check(self, field_prefix):
        """
        The weather of the day, the same at the start of every carnet (two minutes): the
        energy level from 0 to 10 (a single choice), then « Ce chiffre s'explique surtout par… ».
        """
        pad = PDFStyle.CARD_PADDING
        inner = self.target_width - 2 * pad
        label = "Météo du jour"
        _, pill_h = label_pill_size(label)
        prompt_h = paragraph_height(ENERGY_PROMPT, inner, PDFStyle.FONT_HEADING_BOLD, QUESTION_SIZE, QUESTION_LEADING)
        reason_h = paragraph_height(ENERGY_REASON, inner, PDFStyle.FONT_HEADING_BOLD, QUESTION_SIZE, QUESTION_LEADING)
        box_h = 1.6 * cm  # two handwritten lines
        h = (2 * pad + pill_h + 0.25 * cm + prompt_h + 0.15 * cm + choice_scale_height(True) + 0.3 * cm
             + reason_h + 0.15 * cm + box_h)
        self._ensure_space(h)

        top = self.y_cursor
        draw_pastel_card(self.c, self.text_x, top - h, self.target_width, h)
        x = self.text_x + pad
        draw_label_pill(self.c, x, top - pad - pill_h, label, variant="on_pastel", max_width=inner)
        t = top - pad - pill_h - 0.25 * cm
        t -= draw_paragraph(self.c, ENERGY_PROMPT, x, t, inner, PDFStyle.FONT_HEADING_BOLD, QUESTION_SIZE,
                            PDFStyle.COLOR_INK, QUESTION_LEADING) + 0.15 * cm
        group = reserve_field_name(self.form, f"{field_prefix}_energie")
        t -= draw_choice_scale(self.c, group, x, t, inner, list(range(11)), "À plat", "En pleine forme",
                               tooltip="Niveau d'énergie") + 0.3 * cm
        t -= draw_paragraph(self.c, ENERGY_REASON, x, t, inner, PDFStyle.FONT_HEADING_BOLD, QUESTION_SIZE,
                            PDFStyle.COLOR_INK, QUESTION_LEADING) + 0.15 * cm
        draw_answer_box(self.c, x, t - box_h, inner, box_h, f"{field_prefix}_raison", tooltip=ENERGY_REASON)
        self.y_cursor -= h + PDFStyle.GAP_BLOCK
        return self.y_cursor

    REPORT_LABEL_SIZE = 10
    REPORT_LABEL_LEADING = 13

    def add_report(self, lines, title=None, columns=1):
        """
        Data written in another carnet, copied here with its origin (« one piece of data,
        one entry »): a pastel card titled « À reporter », then per line its label, the
        origin on the right (« carnet 4 · p. 12 ») and a box; boxes taller than 1.2 cm are
        multiline. lines: (label, origin, field_id, height_cm or None), laid out on 1 or 2
        columns (short lines, e.g. the four zones). A card that does not fit continues on
        the next page.
        """
        pad = PDFStyle.CARD_PADDING
        inner = self.target_width - 2 * pad
        title = title or "À reporter"
        _, pill_h = label_pill_size(title)
        row_gap, col_gap = 0.35 * cm, 0.4 * cm
        cols = max(1, min(int(columns or 1), 2))
        col_w = (inner - col_gap * (cols - 1)) / cols

        def origin_width(origin):
            # Room for the page, resolved or not (« CARNET 4 · P. 00 »), so that a page number
            # never changes how the labels wrap (nor the pages of the document)
            if not origin:
                return 0
            return text_width(f"{origin.split(' · ')[0]} · P. 00", PDFStyle.FONT_LABEL, PDFStyle.SIZE_FOLIO,
                              PDFStyle.TRACKING_LABEL)

        items = []
        for label, origin, field_id, height in lines:
            origin = str(origin or "").upper()
            label_w = col_w - origin_width(origin) - (0.4 * cm if origin else 0)
            label_h = paragraph_height(str(label), label_w, PDFStyle.FONT_HEADING_BOLD, self.REPORT_LABEL_SIZE,
                                       self.REPORT_LABEL_LEADING)
            items.append((str(label), origin, field_id, label_w, label_h, height * cm if height else 0.85 * cm))
        # A row of the grid: its items, then the height of their labels and of their boxes
        rows = []
        for k in range(0, len(items), cols):
            row = items[k:k + cols]
            rows.append((row, max(i[4] for i in row), max(i[5] for i in row)))

        first = True
        while rows:
            head = pill_h + 0.3 * cm if first else 0
            self._ensure_space(2 * pad + head + rows[0][1] + 3 + rows[0][2])
            available = self.y_cursor - self.bottom_limit - 2 * pad - head
            count, used = 0, 0
            for _, label_h, box_h in rows:
                need = label_h + 3 + box_h + (row_gap if count else 0)
                if count and used + need > available:
                    break
                used += need
                count += 1
            chunk, rows = rows[:count], rows[count:]
            h = 2 * pad + head + used
            top = self.y_cursor
            draw_pastel_card(self.c, self.text_x, top - h, self.target_width, h)
            t = top - pad
            if first:
                draw_label_pill(self.c, self.text_x + pad, t - pill_h, title, variant="on_pastel", max_width=inner)
                t -= head
            for row, label_h, box_h in chunk:
                for k, (label, origin, field_id, label_w, _, item_box_h) in enumerate(row):
                    x = self.text_x + pad + k * (col_w + col_gap)
                    draw_paragraph(self.c, label, x, t, label_w, PDFStyle.FONT_HEADING_BOLD, self.REPORT_LABEL_SIZE,
                                   PDFStyle.COLOR_INK, self.REPORT_LABEL_LEADING)
                    if origin:
                        draw_text(self.c, x + col_w, first_baseline(t, PDFStyle.SIZE_FOLIO, self.REPORT_LABEL_LEADING),
                                  origin, PDFStyle.FONT_LABEL, PDFStyle.SIZE_FOLIO, PDFStyle.COLOR_INK_MUTED,
                                  PDFStyle.TRACKING_LABEL, align="right")
                    box_top = t - label_h - 3
                    draw_answer_box(self.c, x, box_top - item_box_h, col_w, item_box_h, field_id, tooltip=label,
                                    multiline=item_box_h > 1.2 * cm)
                t -= label_h + 3 + box_h + row_gap
            self.y_cursor = top - h - PDFStyle.GAP_BLOCK
            first = False
            if rows:
                self._new_page()
        return self.y_cursor

    def add_life_line(self, nodes, headers=None, field_prefix="timeline_node"):
        """The life line of drawn_blocks.draw_life_line, down to the bottom of the page."""
        self._ensure_space(14 * cm)
        draw_life_line(self.c, self.text_x, self.y_cursor, self.target_width, nodes, headers, field_prefix)
        self.y_cursor = PDFStyle.CONTENT_BOTTOM
        return self.y_cursor

    def add_tree_of_life(self, zones, annotation=None):
        """The tree of life of drawn_blocks.draw_tree_of_life, down to the bottom of the page."""
        self._ensure_space(14 * cm)
        draw_tree_of_life(self.c, self.text_x, self.y_cursor, self.target_width, zones, annotation)
        self.y_cursor = PDFStyle.CONTENT_BOTTOM
        return self.y_cursor

    def render(self):
        """Finishes the page with its folio."""
        draw_folio(self.c)
        self.c.showPage()
