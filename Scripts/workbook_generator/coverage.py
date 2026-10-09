"""
A support laid out as it was written (the app's « Mettre en page un support »): reading
its text, then checking that a layout kept every element of it.

read_support() reads the text of a finished support, pasted from a PDF or a document:
its sections (a surtitle, a title), their instructions, its questions (a line ending with
« ? »), its labels to fill in (« : »), the options under them and the scales (1 to 10).
The fallback of the faithful layout builds its pages from it, and check_coverage() finds
each question and label of the support in a spec, by similarity of normalized strings:
typography, case and accents are not a loss, a missing or reworded element is.
"""

import re
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Iterator, List, NamedTuple, Optional, Tuple

from .conformity import FORBIDDEN_RE, NON_TEXT_KEYS
from .spec import WorkbookSpec

# --- Reading a support -------------------------------------------------------------

# A repeated header of our own documents (« marge », « de manoeuvre », « m a r g e  d e … »):
# not content, and the edge of a page of the PDF
BRAND_LINES = {"marge", "demanoeuvre", "demanœuvre", "margedemanoeuvre", "margedemanœuvre"}
# Check boxes drawn as characters, and list bullets
BOX_GLYPHS = "☐□▢◻◽❑❒○◯"
BULLET = re.compile(r"^(?:[•●▪►◆\-–—*·]|\[\s?\]|\(\s?\)|[" + BOX_GLYPHS + r"])\s*")
TERMINAL = tuple(".!?:;…»)")
# A short line without final punctuation: a title, a surtitle or an option
SHORT_MAX = 90
# A line cut by the width of the page is at least this long (shorter: an option, a title)
WRAPPED_MIN = 40
# A numbered heading (« 2. Le terrain », « Partie 2 », « Étape 3 ») is a title even after a question
NUMBERED_HEADING = re.compile(r"^(?:\d+[.)]\s|[IVX]+[.)]\s|(?:partie|étape|section|chapitre|phase|module)\s+\d)",
                              re.IGNORECASE)
# The fewest consecutive numbers that make a scale (1 2 3 … 10), not a page number
SCALE_MIN_STEPS = 3


@dataclass
class SupportItem:
    kind: str  # "text" (an instruction), "bullet", "question" (« ? ») or "label" (« : »)
    text: str
    options: List[str] = field(default_factory=list)
    scale: Optional[Tuple[int, int]] = None


@dataclass
class SupportSection:
    eyebrow: str = ""
    title: str = ""
    items: List[SupportItem] = field(default_factory=list)


def _despaced(line: str) -> str:
    return re.sub(r"\s+", "", line).lower()


def _tokens(text: str) -> List[Tuple[str, str]]:
    """The lines of a support as (kind, text): 'page' (an edge of page), 'blank', 'num', 'line'."""
    tokens = []
    for raw in (text or "").replace("\f", "\nmarge de manoeuvre\n").splitlines():
        line = re.sub(r"[ \t  ]+", " ", raw).strip()
        if not line:
            tokens.append(("blank", ""))
        elif _despaced(line) in BRAND_LINES:
            tokens.append(("page", ""))
        elif re.fullmatch(r"\d{1,3}", line):
            tokens.append(("num", line))
        else:
            tokens.append(("line", re.sub(r"^#+\s*", "", line)))
    return tokens


def _join_wrapped(tokens):
    """Lines cut by the copy of a PDF: a line without final punctuation, then a lowercase one."""
    joined = []
    for kind, text in tokens:
        previous = joined[-1][1] if joined and joined[-1][0] == "line" else ""
        if (kind == "line" and len(previous) >= WRAPPED_MIN and not previous.endswith(TERMINAL)
                and text[:1].islower()):
            joined[-1] = ("line", f"{joined[-1][1]} {text}")
        else:
            joined.append((kind, text))
    return joined


def _scales(tokens):
    """A run of consecutive numbers becomes a 'scale' token; a lone number (a page number) goes."""
    out, i = [], 0
    while i < len(tokens):
        if tokens[i][0] != "num":
            out.append(tokens[i])
            i += 1
            continue
        j = i
        while j + 1 < len(tokens) and tokens[j + 1][0] == "num" and int(tokens[j + 1][1]) == int(tokens[j][1]) + 1:
            j += 1
        if j - i + 1 >= SCALE_MIN_STEPS:
            out.append(("scale", f"{tokens[i][1]}-{tokens[j][1]}"))
        i = j + 1
    return out


def _kind(text: str) -> str:
    if text.endswith("?"):
        return "question"
    if text.endswith(":") and len(text) > 1:
        return "label"
    if BULLET.match(text) and len(text) > 2:
        return "bullet"
    if text.endswith(TERMINAL) or len(text) > SHORT_MAX:
        return "text"
    return "short"


def _options_of(text: str) -> List[str]:
    """« ☐ CDI ☐ CDD ☐ Intérim » -> three options; « • Terrain » -> one."""
    parts = re.split("[" + BOX_GLYPHS + "]", text)
    if len(parts) > 2:
        return [p.strip(" -–") for p in parts if p.strip(" -–")]
    return [BULLET.sub("", text).strip()]


def is_shouting(text: str) -> bool:
    """A text written in capitals (« COMMENT SE DÉROULE UNE JOURNÉE ? »)."""
    letters = [ch for ch in text if ch.isalpha()]
    return len(letters) >= 3 and not any(ch.islower() for ch in letters)


# Acronyms a text in capitals keeps when it goes to sentence case
ACRONYMS = {"ACRE", "APEC", "ARCE", "ARE", "BTP", "BTS", "CCI", "CDD", "CDI", "CMA", "CPF", "CV", "DRH", "DUT", "EHPAD",
            "ESS", "ETP", "IA", "IUT", "MBA", "PDG", "PME", "PMSMP", "QVT", "RH", "RQTH", "RSE", "SIRET", "SMIC", "TPE",
            "TVA", "URSSAF", "VAE"}


def sentence_case(text: str) -> str:
    """« COMMENT SE DÉROULE UNE JOURNÉE ? » -> « Comment se déroule une journée ? » (typography only)."""
    if not is_shouting(text):
        return text
    text = re.sub(r"[^\W\d_]+", lambda m: m.group(0) if m.group(0) in ACRONYMS else m.group(0).lower(), text)
    first = next((k for k, ch in enumerate(text) if ch.isalpha()), None)
    return text if first is None else text[:first] + text[first].upper() + text[first + 1:]


def read_support(text: str) -> List[SupportSection]:
    """
    The sections of a support. A short line followed by an instruction is a title (and the
    capitals line before it, its surtitle); short lines right after a question or a label
    are its options, a run of numbers its scale. An edge of page ends a list of options.
    """
    tokens = _scales(_join_wrapped(_tokens(text)))
    sections = [SupportSection()]
    attached: Optional[SupportItem] = None  # the question or label that options would follow

    def section():
        return sections[-1]

    def start_section(eyebrow, title):
        if section().items or section().title or section().eyebrow:
            sections.append(SupportSection())
        section().eyebrow, section().title = eyebrow, title

    def next_kind(i):
        while i < len(tokens) and tokens[i][0] == "blank":
            i += 1
        if i >= len(tokens):
            return None
        return _kind(tokens[i][1]) if tokens[i][0] == "line" else tokens[i][0]

    i = 0
    while i < len(tokens):
        kind, value = tokens[i]
        if kind == "page":
            attached = None
            i += 1
            continue
        if kind == "blank":
            i += 1
            continue
        if kind == "scale":
            low, high = (int(n) for n in value.split("-"))
            if attached is not None and not attached.options and attached.scale is None:
                attached.scale = (low, high)
            i += 1
            continue
        line_kind = _kind(value)
        if line_kind in ("question", "label"):
            attached = SupportItem(line_kind, value)
            section().items.append(attached)
        elif line_kind == "bullet":
            if attached is not None and attached.scale is None:
                attached.options += _options_of(value)
            else:
                section().items.append(SupportItem("bullet", BULLET.sub("", value).strip()))
        elif line_kind == "text":
            attached = None
            section().items.append(SupportItem("text", value))
        else:
            # A run of short lines: options, or the title (and surtitle) of a new section
            run, j = [], i
            while j < len(tokens) and tokens[j][0] in ("line", "blank"):
                if tokens[j][0] == "line":
                    if _kind(tokens[j][1]) != "short":
                        break
                    run.append(tokens[j][1])
                j += 1
            numbered = next((k for k, line in enumerate(run) if NUMBERED_HEADING.match(line)), None)
            if numbered is not None:
                start, end = numbered, numbered + 2
            elif next_kind(j) == "text" or attached is None:
                start = len(run) - 1
                if len(run) >= 2 and is_shouting(run[-2]) and (attached is None or not is_shouting(run[-1])):
                    start -= 1
                end = len(run)
            else:
                start = end = len(run)
            options, heading, rest = run[:start], run[start:end], run[end:]
            if attached is not None and attached.scale is None:
                attached.options += options
            else:
                section().items += [SupportItem("text", line) for line in options]
            if heading:
                start_section(heading[0] if len(heading) == 2 else "", heading[-1])
                section().items += [SupportItem("text", line) for line in rest]
                attached = None
            i = j
            continue
        i += 1
    return [s for s in sections if s.items or s.title or s.eyebrow]


def support_title(sections: List[SupportSection]) -> str:
    """The name of a support: the surtitle of its first section, or its first title."""
    for s in sections:
        if s.eyebrow or s.title:
            return s.eyebrow or s.title
    return ""


# --- Coverage ------------------------------------------------------------------------

# Two strings are the same element above this similarity (difflib ratio, 0 to 1): the
# typography and a forbidden word replaced stay above, a reworded question falls below
MATCH_THRESHOLD = 0.8
# Below this many words, an element (« Date », « CDI ») only counts as whole words
SHORT_ELEMENT_WORDS = 3

FIELD_ID = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")


class Missing(NamedTuple):
    kind: str  # "question", "libellé" or "option"
    text: str
    of: Optional[str] = None  # the question an option belongs to
    note: Optional[str] = None


class Coverage(NamedTuple):
    total: int  # questions and labels of the support
    found: int
    options_total: int
    options_found: int
    missing: List[Missing]
    out_of_order: List[str]


def normalize(text: str) -> str:
    """« Qu’est-ce qui ?» and « QU'EST-CE QUI » compare equal: no case, accent, ligature, punctuation."""
    text = (text or "").replace("œ", "oe").replace("Œ", "OE").replace("æ", "ae").replace("Æ", "AE")
    text = "".join(ch for ch in unicodedata.normalize("NFKD", text) if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _strings(value, key=None) -> Iterator[str]:
    if key in NON_TEXT_KEYS:
        return
    if isinstance(value, str):
        if not value.startswith(("http://", "https://")):
            yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from _strings(v, k)
    elif isinstance(value, (list, tuple)):
        for k, v in enumerate(value):
            # [label, field_id, …] lists: the id is no text
            if not (k and isinstance(v, str) and FIELD_ID.match(v)):
                yield from _strings(v)


def spec_texts(spec: WorkbookSpec) -> List[str]:
    """Every text a reader sees, in reading order."""
    texts = []
    for page in spec.pages:
        texts += [t for t in (page.title, page.part_title) if t]
        texts += list(_strings(page.params))
        for block in page.blocks or []:
            texts += list(_strings(block.model_dump(exclude_none=True, exclude_defaults=True)))
    return [t for t in texts if t.strip()]


def _partial_ratio(element: str, text: str) -> float:
    """The similarity of an element with the part of a longer text that matches it best."""
    if len(text) <= len(element):
        return SequenceMatcher(None, element, text).ratio()
    best = 0.0
    matcher = SequenceMatcher(None, element, text, autojunk=False)
    for block in matcher.get_matching_blocks():
        if not block.size:
            continue
        start = max(0, block.b - block.a)
        window = text[start:start + len(element)]
        best = max(best, SequenceMatcher(None, element, window).ratio())
        if best == 1.0:
            break
    return best


def _matches(element: str, text: str) -> bool:
    if f" {element} " in f" {text} ":
        return True
    words = element.split()
    if len(words) < SHORT_ELEMENT_WORDS:
        return False
    # Cheap filter first: a text sharing no long word with the element is not it
    long_words = [w for w in words if len(w) >= 4]
    if long_words and not any(w in text for w in long_words):
        return False
    return _partial_ratio(element, text) >= MATCH_THRESHOLD


def _shown(text: str) -> str:
    """An element as the app lists it: sentence case for a text in capitals."""
    return sentence_case(text.rstrip(" :"))


def _note(text: str) -> Optional[str]:
    if any(pattern.search(text) for rule, pattern, _ in FORBIDDEN_RE if rule != "tutoiement"):
        return "mot proscrit : sans doute remplacé, à vérifier"
    return None


def check_coverage(spec: WorkbookSpec, source_text: str) -> Coverage:
    """
    Finds each question and label of the support in the spec, in order, then each of
    their options. An element found before the previous one is out of order.
    """
    elements = [item for s in read_support(source_text) for item in s.items if item.kind in ("question", "label")]
    texts = [normalize(t) for t in spec_texts(spec)]
    missing, out_of_order = [], []
    found = options_total = options_found = 0
    position = 0
    for item in elements:
        element = normalize(item.text)
        index = next((k for k in range(position, len(texts)) if _matches(element, texts[k])), None)
        if index is None:
            index = next((k for k in range(position) if _matches(element, texts[k])), None)
            if index is not None:
                out_of_order.append(_shown(item.text))
        else:
            position = index
        kind = "question" if item.kind == "question" else "libellé"
        if index is None:
            missing.append(Missing(kind, _shown(item.text), note=_note(item.text)))
        else:
            found += 1
        for option in item.options:
            options_total += 1
            target = normalize(option)
            if target and any(f" {target} " in f" {t} " for t in texts):
                options_found += 1
            else:
                missing.append(Missing("option", option, of=_shown(item.text), note=_note(option)))
    return Coverage(len(elements), found, options_total, options_found, missing, out_of_order)
