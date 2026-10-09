"""
Conformity check of a workbook spec: the rules that guided the reference carnets (art
direction, common template of the carnets, conventions of the roadmap), checked on any
spec, those Gemini writes included. The reference workbooks pass it without a finding
(tests/test_conformity.py): a finding on a generated spec is a gap to our own standards.

Two levels: « à corriger » (a rule is broken: forbidden word, a table with no box, a label
the PDF cuts) and « à vérifier » (a likely gap a person should look at: an exercise without
its duration, a heavy question without the protocol, a gendered turn of phrase).
"""

import re
import unicodedata
from typing import Iterator, List, NamedTuple, Optional

from .spec import BlockSpec, PageSpec, WorkbookSpec

FIX = "à corriger"
CHECK = "à vérifier"


class Finding(NamedTuple):
    level: str  # FIX or CHECK
    page: Optional[int]  # page of the spec, from 1 (None: the whole document)
    rule: str  # short id of the rule
    message: str


# --- Vocabulary (DA-workbook.md, section 7) ------------------------------------------

FORBIDDEN = (
    ("coach", r"\bcoach(?:ing|s|é|ée)?\b",
     "« coach » : dire « consultant en transformation » ou « la personne qui vous accompagne »"),
    ("presentiel", r"\bprésentiel(?:le)?s?\b", "jamais « présentiel » : tout l'accompagnement se fait à distance"),
    ("mbti", r"\bMBTI\b|\b[EI][NS][TF][JP]\b", "jamais « MBTI » ni type en quatre lettres : « test des fonctionnements cognitifs »"),
    ("dev-perso", r"quête de sens|croyances? limitantes?|syndrome de l'imposteur|lâcher[- ]prise|épanouissement"
                  r"|ennéagramme|retrouver votre élan|espace d'écoute bienveillant",
     "registre du développement personnel, à proscrire"),
    ("tutoiement", r"\b(?:tu|toi|tes)\b", "vouvoiement : jamais de tutoiement"),
)
FORBIDDEN_RE = [(rule, re.compile(pattern, re.IGNORECASE if rule != "mbti" else 0), message)
                for rule, pattern, message in FORBIDDEN]

# A participle or adjective that agrees with the person who writes (feuille de route, section 6:
# « Ce qui m'étonne », not « Ce qui m'a surpris »). « m'a donné » (me = to me) does not agree.
GENDERED = re.compile(
    r"\b(?:m'a|m'ont|me suis|je suis|je me sens|je me sentais|je me suis senti|j'étais|je serais)\s+"
    r"(?:surpris|poussé|touché|marqué|blessé|déçu|motivé|freiné|bloqué|découragé|encouragé|rassuré|étonné|inspiré"
    r"|attiré|lassé|ennuyé|stressé|angoissé|épuisé|fatigué|perdu|seul|prêt|fier|heureux|content|inquiet|légitimé"
    r"|allé|né|devenu|resté|parti|venu|arrivé|tombé|entré|sorti|passé|retourné|coincé|senti)e?s?\b",
    re.IGNORECASE,
)

# Words of a heavy question (Pennebaker line: protocol before, anchoring sentence after)
HEAVY = re.compile(
    r"\b(?:peurs?|deuil|honte|humiliation|harcèlement|burn-?out|épuisement|licenciement|souffrance|culpabilit\w*"
    r"|colère|trahi\w*|jamais osé|jamais dit|blessures?|échecs?)\b",
    re.IGNORECASE,
)

# The trade of a contrast example has an epicene name (juriste, ergonome): a first word with
# a gendered ending (formatrice, ingénieur, acheteuse, consultant) is to be checked
GENDERED_TRADE = re.compile(r"^\s*[A-Za-zÀ-ÿ'-]*?(?:eur|euse|trice|ier|ière|ien|ienne|ant|ante|ais|aise|ine|é|ée)\b",
                            re.IGNORECASE)
# An amount or a rate written in an example (carnet 4: never a personal figure; no figure
# without a source anywhere)
AMOUNT = re.compile(r"\d[\d\s .,]*\s?(?:€|euros?\b|k€)|\b\d+\s?%", re.IGNORECASE)
# Words of a job title too general to tie an example to the person's own trade
GENERIC_JOB_WORDS = {"responsable", "chef", "cheffe", "charge", "chargee", "assistant", "assistante", "directeur",
                     "directrice", "manager", "gestion", "projet", "service", "agent", "agente", "conseiller",
                     "conseillere", "technicien", "technicienne", "metier", "poste", "entreprise", "activite"}

# Keys that hold no text a reader sees
NON_TEXT_KEYS = {"field_id", "field_prefix", "data_id", "type", "template", "color", "variant", "answer", "_ref",
                 "style", "align", "pastel", "carnet", "url"}

DURATION = re.compile(r"\d+\s*(?:min|h)\b|facultatif|hors temps", re.IGNORECASE)
EXERCISE = re.compile(r"^\s*Exercice\s+(\d+)", re.IGNORECASE)
# The eyebrow of the former workbooks (« 1. CADRAGE INITIAL »), before the common template
OLD_EYEBROW = re.compile(r"^\s*\d+\.\s")

# Lengths the PDF cuts (feuille de route, section 5: carnets 3 and 4)
RATING_LABEL_MAX = 36
SCALE_BOUND_MAX = 20


def _texts(value, key=None) -> Iterator[str]:
    """Every text a reader sees in a page, a block or params."""
    if key in NON_TEXT_KEYS:
        return
    if isinstance(value, str):
        if not value.startswith(("http://", "https://")):
            yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from _texts(v, k)
    elif isinstance(value, (list, tuple)):
        if len(value) > 1 and isinstance(value[0], str) and isinstance(value[1], str) and re.match(
            r"^[a-z][a-z0-9_]*$", value[1]
        ):
            # a [label, field_id, …] or [label, data_id, …] list: only its label is text
            yield value[0]
            return
        for v in value:
            yield from _texts(v)


def _page_texts(page: PageSpec) -> Iterator[str]:
    yield page.title or ""
    yield page.part_title or ""
    yield from _texts(page.params)
    for block in page.blocks or []:
        yield from _texts(block.model_dump(exclude_none=True, exclude_defaults=True))


def _questions(page: PageSpec) -> Iterator[tuple]:
    """The questions a page asks the reader, as (text, block or None)."""
    for q in page.params.get("questions") or []:
        if isinstance(q, dict):
            yield str(q.get("question") or q.get("title") or ""), None
    for block in page.blocks or []:
        if block.question:
            yield block.question, block
        for q in block.questions or []:
            yield q.question, block
        if block.type == "fields_card":
            for row in block.rows or []:
                for field in row:
                    if isinstance(field, (list, tuple)) and field and isinstance(field[0], str):
                        yield field[0], block
        if block.type == "cards_grid":
            for card in block.cards or []:
                if isinstance(card, dict):
                    yield str(card.get("title") or ""), block


def _exercise_key(index: int, page: PageSpec) -> str:
    match = EXERCISE.match((page.part_title or "").replace("\xa0", " "))
    return f"exercice {match.group(1)}" if match else f"page {index}"


QUOTED = re.compile(r"«[^»]*»")


def _check_vocabulary(index, page, findings):
    seen = set()
    for text in _page_texts(page):
        for rule, pattern, message in FORBIDDEN_RE:
            # A quoted message (to a relative: « Si tu ne connaissais pas… ») may say « tu »
            match = pattern.search(QUOTED.sub("", text) if rule == "tutoiement" else text)
            if match and rule not in seen:
                seen.add(rule)
                findings.append(Finding(FIX, index, rule, f"{message} (« {match.group(0)} »)"))
        match = GENDERED.search(text)
        if match and "genre" not in seen:
            seen.add("genre")
            findings.append(Finding(CHECK, index, "genre", f"formule qui s'accorde avec la personne : « {match.group(0)} »"
                                                         " (écrire « ce qui m'étonne », tourner autrement)"))


def _check_blocks(index, page, findings):
    if page.template == "roadmap":
        findings.append(Finding(CHECK, index, "roadmap", "le gabarit « roadmap » préremplit ses cases : les paliers "
                                                         "d'une feuille de route sont les lignes d'un tableau"))
    for block in page.blocks or []:
        _check_block(index, block, findings)


def _check_block(index, block: BlockSpec, findings):
    if block.type == "table" and block.rows:
        cells = [cell for row in block.rows for cell in row]
        if not any(isinstance(cell, dict) for cell in cells):
            findings.append(Finding(FIX, index, "tableau-sans-case", f"tableau sans aucune case à remplir "
                                                                     f"(« {block.title or ', '.join(block.headers or [])} »)"))
    if block.type == "rating_grid":
        for item in block.items or []:
            label = item[0] if isinstance(item, (list, tuple)) and item else item
            if isinstance(label, str) and len(label) > RATING_LABEL_MAX:
                findings.append(Finding(FIX, index, "libelle-tronque", f"libellé d'échelle tronqué au-delà de "
                                                                       f"{RATING_LABEL_MAX} caractères : « {label} »"))
    if block.type == "scale":
        for bound in (block.min_label, block.max_label):
            if bound and len(bound) > SCALE_BOUND_MAX:
                findings.append(Finding(FIX, index, "libelle-tronque", f"borne d'échelle tronquée au-delà de "
                                                                       f"{SCALE_BOUND_MAX} caractères : « {bound} »"))


def _check_structure(spec: WorkbookSpec, findings):
    pages = spec.pages
    if not pages:
        findings.append(Finding(FIX, None, "vide", "le document n'a aucune page"))
        return
    templates = [p.template for p in pages]
    if templates[0] != "cover":
        findings.append(Finding(CHECK, 1, "gabarit", "le document ne commence pas par sa couverture"))
    if templates[-1] != "closing":
        findings.append(Finding(CHECK, len(pages), "gabarit", "le document ne finit pas par son dos (« closing »)"))
    if "summary" not in templates:
        findings.append(Finding(CHECK, None, "gabarit", "pas d'ouverture (« summary ») : le but, les exercices et leur durée"))
    for i, page in enumerate(pages, start=1):
        if page.template == "summary" and not (page.params.get("duration") or page.params.get("duree")):
            findings.append(Finding(CHECK, i, "duree", "l'ouverture ne donne pas la durée d'écriture totale"))
    if "engagement" not in templates:
        findings.append(Finding(CHECK, None, "gabarit", "pas de page de livrable (« engagement ») avant le dos"))

    exercise_pages = 0
    for i, page in enumerate(pages, start=1):
        if page.template not in ("composite", "questions", "two_columns", "quadrants", "enquete", "roadmap"):
            continue
        exercise_pages += 1
        eyebrow = page.part_title
        if eyebrow is None or not eyebrow.strip() or OLD_EYEBROW.match(eyebrow):
            shown = eyebrow.strip() if eyebrow and eyebrow.strip() else ("vide" if eyebrow is not None else "N. TITRE")
            findings.append(Finding(CHECK, i, "sourcil", f"sourcil « {shown} » : écrire « Exercice N · nom · durée »"))
        elif EXERCISE.match(eyebrow.replace("\xa0", " ")) and not DURATION.search(eyebrow):
            findings.append(Finding(CHECK, i, "duree", f"sourcil sans durée : « {eyebrow} »"))
    has_example = any(b.type == "contrast_example" for p in pages for b in p.blocks or [])
    if exercise_pages and not has_example:
        findings.append(Finding(CHECK, None, "exemple", "aucun exemple contrasté (« En surface / Exploitable »), "
                                                        "tiré d'un métier voisin"))


def _plain_words(text):
    text = unicodedata.normalize("NFD", (text or "").lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return set(re.findall(r"[a-z]{5,}", text))


def _check_examples(spec: WorkbookSpec, context: Optional[str], findings):
    """Contrast examples: an epicene neighbouring trade, never the person's own, no amount."""
    own = _plain_words(context) - GENERIC_JOB_WORDS
    for i, page in enumerate(spec.pages, start=1):
        for block in page.blocks or []:
            examples = [block.example] if block.example else []
            examples += [q.example for q in block.questions or [] if q.example]
            if block.type == "contrast_example":
                examples += [block.surface or "", block.exploitable or ""]
                title = block.title or ""
                if GENDERED_TRADE.match(title):
                    findings.append(Finding(CHECK, i, "metier-genre", f"exemple tiré d'un métier au nom genré : « {title} »"
                                                                      " (prendre un nom épicène : juriste, ergonome…)"))
                shared = _plain_words(title) & own
                if shared:
                    findings.append(Finding(CHECK, i, "metier-personne", f"exemple tiré du métier de la personne : « {title} »"
                                                                         " (prendre un métier voisin, elle le recopierait)"))
            for text in examples:
                match = AMOUNT.search(text or "")
                if match:
                    findings.append(Finding(CHECK, i, "montant", f"montant écrit dans un exemple : « {match.group(0).strip()} »"
                                                                 " (jamais de chiffre personnel ; une source, ou une fourchette à voir en séance)"))
                    break


def _check_heavy_questions(spec: WorkbookSpec, findings):
    """A heavy question needs the protocol in its exercise, or to be optional and fixed (medium charge)."""
    protected = set()
    for i, page in enumerate(spec.pages, start=1):
        if any(b.type in ("protocol", "anchor") for b in page.blocks or []):
            protected.add(_exercise_key(i, page))
    for i, page in enumerate(spec.pages, start=1):
        if _exercise_key(i, page) in protected or page.fixed:
            continue
        for text, block in _questions(page):
            match = HEAVY.search(text or "")
            if match and not (block is not None and block.fixed):
                findings.append(Finding(CHECK, i, "charge", f"question à forte charge sans protocole (« {match.group(0)} ») :"
                                                            " avertissement avant, phrase d'ancrage après"))
                break


# A « (suite) » page whose content stops above this share of the page height holds one
# small block: our carnets cut a long exercise into two balanced pages (the least filled
# continuation of the reference workbooks reaches 45 %, tests/test_workbooks.py asks 40 %)
CONTINUATION_MIN_SHARE = 0.42


def _check_layout(spec: WorkbookSpec, findings):
    from .compiler import workbook_continuations  # compiles the spec: imported on use only

    for continuation in workbook_continuations(spec):
        if continuation["used"] < CONTINUATION_MIN_SHARE:
            findings.append(Finding(CHECK, continuation["page"], "suite-presque-vide",
                                    f"sa page « (suite) » (p. {continuation['pdf_page']} du PDF) ne porte presque rien : "
                                    "couper l'exercice en deux pages équilibrées ('page_break'), ou le resserrer"))


def check_spec(spec: WorkbookSpec, structure: bool = True, context: Optional[str] = None,
               layout: bool = False) -> List[Finding]:
    """
    The findings of a spec, page by page. `structure=False` skips the common template of a
    carnet (cover, opener, deliverable, eyebrows, contrast example), for a document laid out
    as it was written. `context` describes the person (customization): an example taken
    from their own trade is then flagged. `layout=True` compiles the spec to find the
    « (suite) » pages that hold almost nothing.
    """
    findings: List[Finding] = []
    for i, page in enumerate(spec.pages, start=1):
        _check_vocabulary(i, page, findings)
        _check_blocks(i, page, findings)
    if structure:
        _check_structure(spec, findings)
    _check_examples(spec, context, findings)
    _check_heavy_questions(spec, findings)
    if layout:
        _check_layout(spec, findings)
    return sorted(findings, key=lambda f: (f.page or 0, f.level != FIX))
