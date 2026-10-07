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
    choice_scale_height,
    draw_answer_box,
    draw_choice_scale,
    draw_question,
    question_text_height,
)
from .forms import create_checkbox, reserve_field_name
from .primitives import (
    content_frame,
    draw_folio,
    draw_label_pill,
    draw_page_head,
    draw_paragraph,
    draw_pastel_card,
    draw_rule,
    draw_text,
    draw_white_card,
    label_pill_size,
    paragraph_height,
    text_width,
    fit_text,
    pastel_cycle,
    wrap_text,
)

logger = logging.getLogger(__name__)


@dataclass
class LayoutConfig:
    part_title: str = ""  # eyebrow above the page title
    use_side_panel: bool = True  # former art direction, ignored
    use_blobs: bool = False  # former art direction, ignored
    y_start: float = None


@dataclass
class QuestionConfig:
    box_height: float = 3.0 * cm
    subtitle: str = None
    example: str = None
    color_alternation: bool = True  # former art direction: questions are now always ink
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
            return True
        return False

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
                        color=q.get("color"),
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

    def add_table(self, headers, rows, col_widths=None, field_prefix="tbl"):
        """
        Table: a linen header row in PT Mono, then rows separated by rules. A dict cell is an
        answer field, an empty cell a check box; text cells wrap. The header repeats on
        continuation pages.
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
            p_th = Paragraph(escape(str(h_text)).upper(), style_th)
            _, ph = p_th.wrap(widths[i] - 2 * cell_pad, 200)
            th_paragraphs.append((p_th, ph))
            max_th_h = max(max_th_h, ph)
        header_h = max(0.75 * cm, max_th_h + 0.35 * cm)

        def draw_header():
            h_y = self.y_cursor - header_h
            self.c.saveState()
            self.c.setFillColor(PDFStyle.COLOR_SURFACE_ALT)
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
                        p_cell = Paragraph(escape(c_str), style_cell)
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
                                    tooltip=value.get("placeholder", ""), multiline=False)
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

    def render(self):
        """Finishes the page with its folio."""
        draw_folio(self.c)
        self.c.showPage()
