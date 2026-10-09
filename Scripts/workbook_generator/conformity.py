"""
Conformity check of a workbook spec: the rules that guided the reference carnets (art
direction, common template of the carnets, conventions of the roadmap), checked on any
spec, those Gemini writes included. The reference workbooks pass it without a finding
(tests/test_conformity.py): a finding on a generated spec is a gap to our own standards.

Two levels: « à corriger » (a rule is broken: forbidden word, the paper workflow, a table
with no box, a label the PDF cuts) and « à vérifier » (a likely gap a person should look at:
an exercise without its duration, an intimate question without its announcement, a gendered
turn of phrase, a precaution that treats the person as fragile).
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
    ("papier", r"\bimprim(?:ez|er)\b|\bsur papier\b|\bapport(?:ez|er|e)(?:-le|-la)?\s+(?:ce|votre|vos|mon|mes|le|la)\s+"
               r"(?:carnet|module|livret|document)s?\b|\bapportez-le\b",
     "tout se fait à l'écran : le carnet se renvoie complété avant la séance (jamais « imprimez », « sur papier », "
     "« apportez ce carnet »)"),
)
# Rules a quoted word escapes: a message to a relative (« Si tu ne connaissais pas… »), a
# message received and cited (« épanouissement », « passion »…)
QUOTE_EXEMPT = {"tutoiement", "dev-perso"}
FORBIDDEN_RE = [(rule, re.compile(pattern, re.IGNORECASE if rule != "mbti" else 0), message)
                for rule, pattern, message in FORBIDDEN]

# A precaution that treats the person as fragile (feedback on carnet 1, 9 October 2026: a
# bilan, not psychology): say what the exercise is about and what it serves instead
PRECAUTION = re.compile(r"à votre rythme|peu(?:t|vent) (?:vous )?remuer|trop lourd|submerg\w*|douloureu\w*"
                        r"|laissez(?:-le|-la)? (?:la case )?vierge", re.IGNORECASE)

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
# A writing time: « 15 min », « 1 h 30 », « 2 h »
MINUTES = re.compile(r"(\d+)\s*h\b(?:\s*(\d{2})\b)?|(\d+)\s*min\b", re.IGNORECASE)
OPTIONAL = re.compile(r"facultatif", re.IGNORECASE)

# A figure that calls for a source (DA section 7: no unsourced figure): a rate, « 3 personnes
# sur 10 », « une personne sur deux », what studies show
STATISTIC = re.compile(
    r"\b\d+(?:[,.]\d+)?\s?%|\b\d+\s+(?:[a-zà-ÿ'-]+\s+){0,2}sur\s+\d+\b"
    r"|\b(?:un|une)\s+(?:personne|salarié|salariée|actif|active|cadre|français|française|créateur|créatrice"
    r"|entreprise|reconversion|projet)s?\s+sur\s+(?:deux|trois|quatre|cinq|dix)\b"
    r"|\b(?:les|des|une|plusieurs|de nombreuses)\s+études?\s+(?:montrent|prouvent|révèlent|indiquent|ont montré)\b"
    r"|\bselon\s+(?:une|des|les)\s+études?\b|\bstatistiquement\b",
    re.IGNORECASE,
)
# What names a source next to a figure: an address, the word, or a public body
SOURCE = re.compile(r"https?://|\bsource|\b(?:INSEE|DARES|APEC|France Travail|Pôle emploi|OCDE|Bpifrance|URSSAF"
                    r"|Céreq|CEREQ|France Stratégie|Eurostat|Banque de France)\b", re.IGNORECASE)

# A label that calls for a sentence, not a word (ANSWER_RULES of the prompts)
SENTENCE_LABEL = re.compile(r"^\s*(?:ce qu|pourquoi|comment|en quoi|qu'est-ce)|\?\s*$|\bet pourquoi\b", re.IGNORECASE)

# A web address, and what is left of it to compare with the notes
URL = re.compile(r"(?:https?://|www\.)[^\s«»\"'<>()\[\]]+", re.IGNORECASE)
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


def _strings(value) -> List[str]:
    """Every string of a page, a block or params, addresses and ids included."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, (list, tuple)):
        return [s for v in value for s in _strings(v)]
    return []


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
            match = pattern.search(QUOTED.sub("", text) if rule in QUOTE_EXEMPT else text)
            if match and rule not in seen:
                seen.add(rule)
                findings.append(Finding(FIX, index, rule, f"{message} (« {match.group(0)} »)"))
        match = PRECAUTION.search(text)
        if match and "precaution" not in seen:
            seen.add("precaution")
            findings.append(Finding(CHECK, index, "precaution", f"formule de précaution : « {match.group(0)} » (dire de "
                                                                 "quoi parle l'exercice et à quoi il sert ; le droit de "
                                                                 "passer une question est dit dans l'ouverture)"))
        match = GENDERED.search(text)
        if match and "genre" not in seen:
            seen.add("genre")
            findings.append(Finding(CHECK, index, "genre", f"formule qui s'accorde avec la personne : « {match.group(0)} »"
                                                         " (écrire « ce qui m'étonne », tourner autrement)"))


def _check_statistics(index, page, findings):
    """A figure names its source in the same block (DA section 7): flagged once per page."""
    groups = [([page.title or "", page.part_title or ""] + list(_texts(page.params)), _strings(page.params))]
    for block in page.blocks or []:
        if block.type != "contrast_example":  # an example's figure is a « montant »
            dumped = block.model_dump(exclude_none=True, exclude_defaults=True)
            groups.append((list(_texts(dumped)), _strings(dumped)))
    for texts, raw in groups:
        for text in texts:
            match = STATISTIC.search(text)
            if match and not any(SOURCE.search(s) for s in raw):
                findings.append(Finding(CHECK, index, "statistique", f"chiffre sans source : « {match.group(0)} » "
                                                                     "(nommer sa source dans le bloc, ou le retirer)"))
                return


def _unsized_box(block: BlockSpec) -> Optional[str]:
    """
    The label of a box of this block that says neither the answer it expects nor a height
    (field policy), else None. A questions_group may leave it out: its boxes share the room
    left on the page, from 1.6 cm up. A fields_card box takes one line by default, right for
    a word (a name, a date): only a label that calls for a sentence needs its answer.
    """
    if block.type == "question" and not (block.answer or block.box_height_cm):
        return block.question or ""
    if block.type == "fields_card" and not (block.answer or block.field_height_cm):
        for row in block.rows or []:
            for field in row:
                if (isinstance(field, (list, tuple)) and field and (len(field) < 3 or field[2] in (None, ""))
                        and SENTENCE_LABEL.search(str(field[0]))):
                    return str(field[0])
    if block.type == "table" and not (block.answer or block.field_height_cm):
        for row in block.rows or []:
            for cell in row:
                if isinstance(cell, dict) and not cell.get("answer"):
                    return str(cell.get("placeholder") or block.title or ", ".join(block.headers or []))
    if block.type == "cards_grid" and not (block.answer or block.card_height_cm):
        card = (block.cards or [{}])[0]
        return str(card.get("title") if isinstance(card, dict) else card or block.title or "")
    return None


def _check_blocks(index, page, findings):
    if page.template == "roadmap":
        findings.append(Finding(CHECK, index, "roadmap", "le gabarit « roadmap » préremplit ses cases : les paliers "
                                                         "d'une feuille de route sont les lignes d'un tableau"))
    for block in page.blocks or []:
        _check_block(index, block, findings)
    for block in page.blocks or []:
        label = _unsized_box(block)
        if label is not None:
            findings.append(Finding(CHECK, index, "case-sans-taille", f"case sans réponse attendue : « {label} » "
                                                                      "('answer' : word, sentence, paragraph ou long)"))
            break


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


def _minutes(text) -> int:
    """The writing time a text gives, in minutes: « 1 h 30 » is 90, « 1 h 45, puis 2 h » 225."""
    total = 0
    for hours, rest, minutes in MINUTES.findall(str(text or "").replace("\xa0", " ")):
        total += int(hours) * 60 + int(rest or 0) if hours else int(minutes)
    return total


def _shown(minutes: int) -> str:
    hours, rest = divmod(minutes, 60)
    return f"{rest} min" if not hours else f"{hours} h {rest:02d}" if rest else f"{hours} h"


def _tolerance(minutes: int) -> int:
    """A total may round its lines (« 15 h » for 15 h 10): 5 min, or a tenth of a long time."""
    return max(5, round(minutes / 10))


def _point_text(point) -> str:
    if isinstance(point, dict):
        return " · ".join(str(point.get(k)) for k in ("label", "title", "text", "duration") if point.get(k))
    return str(point or "")


def _check_durations(spec: WorkbookSpec, duration_min: Optional[int], findings):
    """
    The writing time adds up (carte du parcours, section 4): the eyebrows of an exercise make
    its line in the opener, the lines (an optional one aside) make the total, and the total
    is the time the consultant asked for.
    """
    opener = next(((i, p) for i, p in enumerate(spec.pages, start=1) if p.template == "summary"), None)
    if opener is None:
        return
    index, page = opener
    points = page.params.get("points") or page.params.get("steps") or page.params.get("items") or []
    listed, lines = {}, 0
    for point in points:
        text = _point_text(point).replace("\xa0", " ")
        minutes = _minutes(text)
        match = EXERCISE.match(text)
        if match:
            listed[match.group(1)] = listed.get(match.group(1), 0) + minutes
        if not OPTIONAL.search(text):
            lines += minutes

    eyebrows = {}  # exercise number -> {eyebrow: minutes}, a page repeated under one eyebrow counted once
    for p in spec.pages:
        eyebrow = (p.part_title or "").replace("\xa0", " ").strip()
        match = EXERCISE.match(eyebrow)
        if match:
            eyebrows.setdefault(match.group(1), {})[eyebrow] = _minutes(eyebrow)
    for number, seen in eyebrows.items():
        written = sum(seen.values())
        if number not in listed:
            if listed:
                findings.append(Finding(CHECK, index, "duree", f"l'exercice {number} n'est pas dans la liste de l'ouverture"))
        elif written and listed[number] and written != listed[number]:
            findings.append(Finding(CHECK, index, "duree", f"l'exercice {number} compte {_shown(listed[number])} dans "
                                                           f"l'ouverture et {_shown(written)} dans ses sourcils"))

    total = _minutes(page.params.get("duration") or page.params.get("duree"))
    if total and lines and abs(total - lines) > _tolerance(lines):
        findings.append(Finding(CHECK, index, "duree", f"l'ouverture annonce {_shown(total)} au total, et ses lignes "
                                                       f"font {_shown(lines)}"))
    announced = total or lines
    if duration_min and announced and abs(announced - duration_min) > _tolerance(duration_min):
        findings.append(Finding(CHECK, index, "duree", f"l'ouverture annonce {_shown(announced)}, et la durée "
                                                       f"d'écriture demandée était de {_shown(duration_min)}"))


def _bare_address(text: str) -> str:
    """An address as the notes may write it: no scheme, no « www. », no final slash or point."""
    return re.sub(r"https?://|\bwww\.", "", text.lower()).rstrip("/.,;:!?")


def _check_addresses(spec: WorkbookSpec, sources: str, findings):
    """
    A web address the notes (or the support) do not give was made up by the model (TONE_RULES):
    it may not exist. Flagged, never removed: the consultant checks it.
    """
    known = _bare_address(sources)
    seen = set()
    for i, page in enumerate(spec.pages, start=1):
        for text in _strings(page.model_dump(exclude_none=True)):
            for address in URL.findall(text):
                bare = _bare_address(address)
                if bare and bare not in known and bare not in seen:
                    seen.add(bare)
                    findings.append(Finding(FIX, i, "adresse", f"adresse web absente du texte d'origine : « {address.rstrip('.,;:!?')} » "
                                                               "(vérifier qu'elle existe, ou la retirer)"))


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
    """A question that touches on the intimate needs the announcement of its exercise, or to be fixed."""
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
                findings.append(Finding(CHECK, i, "charge", f"question qui touche à l'intime sans annonce (« {match.group(0)} ») :"
                                                            " une phrase factuelle avant l'exercice (bloc 'protocol')"))
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
               layout: bool = False, sources: Optional[str] = None,
               duration_min: Optional[int] = None) -> List[Finding]:
    """
    The findings of a spec, page by page. `structure=False` skips the common template of a
    carnet (cover, opener, deliverable, eyebrows, contrast example, writing times), for a
    document laid out as it was written. `context` describes the person (customization): an
    example taken from their own trade is then flagged. `layout=True` compiles the spec to
    find the « (suite) » pages that hold almost nothing. `sources` is the text the document
    comes from (notes, support): a web address it does not give is flagged. `duration_min`
    is the writing time asked for a document created from notes.
    """
    findings: List[Finding] = []
    for i, page in enumerate(spec.pages, start=1):
        _check_vocabulary(i, page, findings)
        _check_statistics(i, page, findings)
        _check_blocks(i, page, findings)
    if structure:
        _check_structure(spec, findings)
        _check_durations(spec, duration_min, findings)
    if sources:
        _check_addresses(spec, sources, findings)
    _check_examples(spec, context, findings)
    _check_heavy_questions(spec, findings)
    if layout:
        _check_layout(spec, findings)
    return sorted(findings, key=lambda f: (f.page or 0, f.level != FIX))
