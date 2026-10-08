"""
The declarative format of a workbook (WorkbookSpec), shared by the CLI documents and the
web app: the reference workbooks are JSON files in workbooks/, the app produces the same
format (Gemini, customization, JSON import and export), and compiler.py renders both.
"""

import copy
import json
import os
import re
from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator

from .config import PDFStyle

# Bounds on any spec (client, LLM or file): beyond them the API answers 422. They leave room
# for the longest reference document (the business plan: 36 pages, up to 18 blocks a page).
MAX_NAME_LENGTH = 200
MAX_PAGES = 60
MAX_BLOCKS_PER_PAGE = 24
MAX_LIST_ITEMS = 60
MAX_TEXT_LENGTH = 2_000
MAX_NESTING_DEPTH = 10
MAX_SCALE_STEPS = 10

WORKBOOKS_DIR = os.path.join(PDFStyle.PROJECT_DIR, "workbooks")

# Stable id of a piece of data written in a carnet (« c4.seuils »), so that another carnet
# reports it with its origin: the carnet it comes from (c1 to c7, or route), then a name
DATA_ID_PATTERN = r"^(c[1-7]|route)\.[a-z0-9_]+$"
# Blocks customization never changes, wherever they are: the safety protocol, the weather
# of the day (the same in every carnet) and the reports between carnets
FIXED_BLOCK_TYPES = ("protocol", "anchor", "energy", "report")


def data_carnet(data_id):
    """The carnet a data id comes from: 'c4.seuils' -> 4, 'route.pistes' -> 'route'."""
    prefix = str(data_id).split(".", 1)[0]
    return PDFStyle.CARNET_ROUTE if prefix == "route" else int(prefix[1:])


def _check_bounded(value: Any, path: str = "", depth: int = 0) -> None:
    """
    Refuse les textes et listes démesurés n'importe où dans une spécification, y compris
    dans les 'params' libres : chaque élément devient des pages et des champs PDF.
    """
    if depth > MAX_NESTING_DEPTH:
        raise ValueError(f"{path or 'spécification'} : imbrication trop profonde")
    if isinstance(value, str):
        if len(value) > MAX_TEXT_LENGTH:
            raise ValueError(
                f"{path or 'texte'} : texte trop long ({len(value)} caractères, maximum {MAX_TEXT_LENGTH})"
            )
    elif isinstance(value, (list, tuple)):
        if len(value) > MAX_LIST_ITEMS:
            raise ValueError(f"{path or 'liste'} : {len(value)} éléments (maximum {MAX_LIST_ITEMS})")
        for i, item in enumerate(value):
            _check_bounded(item, f"{path}[{i}]", depth + 1)
    elif isinstance(value, dict):
        for key, item in value.items():
            _check_bounded(item, f"{path}.{key}" if path else str(key), depth + 1)


class QuestionItemSpec(BaseModel):
    question: str = Field(..., description="Intitulé de la question ou consigne de réflexion")
    field_id: str = Field(..., description="Identifiant unique pour le champ interactif AcroForm")
    subtitle: Optional[str] = Field(None, description="Sous-titre d'aide ou de précision (1 ligne)")
    example: Optional[str] = Field(None, description="Exemple concret pour guider la réponse (1 ligne)")
    box_height_cm: Optional[float] = Field(None, gt=0, le=20, description="Hauteur fixe de la zone de saisie en cm")


class QuadrantItemSpec(BaseModel):
    title: str = Field(..., description="Titre du quadrant (ex: Professionnel, Santé, Cadre)")
    subtitle: Optional[str] = Field(None, description="Mots-clés associés entre parenthèses")
    field_id: Optional[str] = Field(None, description="Identifiant du champ de saisie")


class TwoColumnsRowSpec(BaseModel):
    label: str = Field(..., description="Intitulé de la ligne / Situation de départ")
    left_tooltip: Optional[str] = Field(None, description="Exemple ou indication pour la colonne 1")
    right_tooltip: Optional[str] = Field(None, description="Exemple ou indication pour la colonne 2")


class SummaryPointSpec(BaseModel):
    label: str = Field(..., description="Numéro ou titre du point (ex: '1.')")
    desc: str = Field("", description="Description du point ou étape")


# The 8 blocks Gemini may create; the others come from the reference workbooks
BASE_BLOCK_TYPES = ("callout", "cards_grid", "scale", "checklist", "table", "stat_boxes", "question", "text")


class BlockSpec(BaseModel):
    """
    One block of a composite page, i.e. one PageLayout.add_* call (see templates.py).
    Lengths are in centimetres (*_cm), colors are PDFStyle color or pastel names ('sky').
    Tuples of the Python API are lists: a fields_card field is [label, field_id, height_cm,
    weight], a frise step [icon, title, marker], a link [name, url, description], a
    checklist_cards group [title, items], a numbered_lines card [title, field_prefix, hint],
    a fill_in_card line a list of texts and boxes [field_id, width_cm, tooltip], a life_line
    node [label, 'summit' | 'valley'], a tree_of_life zone [title, hint, field_id] (roots,
    soil, trunk, branches, leaves, fruits).
    The common template of the carnets adds 'protocol' (before a heavy exercise: the warning
    in 'text', or a default one), 'anchor' (after it: the anchoring sentence, 'field_id'),
    'contrast_example' ('title' names the neighbouring trade, 'surface' and 'exploitable'
    the two versions of an answer) and 'energy' (the weather of the day, 'field_prefix').
    Their fixed texts live in templates.py, so a customization cannot change them.
    A 'report' line copies a piece of data written in another carnet: its items are
    [label, data_id, field_id, height_cm], and the origin (« carnet 4 · p. 12 ») is
    resolved when the PDF is built. 'data_id' names the data a block produces, 'fixed'
    keeps a block out of customization (see keep_fixed).
    """
    type: Literal[
        "callout",
        "cards_grid",
        "scale",
        "checklist",
        "table",
        "stat_boxes",
        "question",
        "text",
        "questions_group",
        "heading",
        "paragraphs",
        "star_list",
        "annotation",
        "frise",
        "fields_card",
        "numbered_lines",
        "rating_grid",
        "info_cards",
        "link_card",
        "checklist_cards",
        "fill_in_card",
        "life_line",
        "tree_of_life",
        "protocol",
        "anchor",
        "contrast_example",
        "energy",
        "report",
        "space",
        "page_break",
    ] = Field(..., description="Type de composant atomique")
    text: Optional[str] = Field(None, description="Contenu texte principal (callout, text, heading, annotation)")
    title: Optional[str] = Field(None, description="Titre optionnel du composant")
    variant: Optional[str] = Field("info", description="Variante visuelle du callout : 'info', 'tip', 'quote'")
    cards: Optional[List[Any]] = Field(None, description="Cartes (cards_grid, info_cards, numbered_lines)")
    columns: Optional[int] = Field(None, ge=1, le=4, description="Nombre de colonnes (défaut selon le bloc)")
    card_height_cm: Optional[float] = Field(None, gt=0, le=20, description="Hauteur personnalisée des cartes en cm")
    label: Optional[str] = Field(None, description="Libellé de la jauge / échelle ou stat")
    min_val: Optional[int] = Field(0, description="Valeur minimale (scale)")
    max_val: Optional[int] = Field(10, description="Valeur maximale (scale)")
    min_label: Optional[str] = Field("", description="Libellé borne min (scale, rating_grid)")
    max_label: Optional[str] = Field("", description="Libellé borne max (scale, rating_grid)")
    items: Optional[List[Any]] = Field(None, description="Éléments (checklist, paragraphs, star_list, rating_grid)")
    headers: Optional[List[str]] = Field(None, description="En-têtes de colonnes (table)")
    rows: Optional[List[List[Any]]] = Field(None, description="Lignes du tableau, ou rangées de champs (fields_card)")
    stats: Optional[List[Dict[str, Any]]] = Field(None, description="Indicateurs clés [{'stat': '...', 'label': '...'}]")
    question: Optional[str] = Field(None, description="Intitulé de la question (question block)")
    field_id: Optional[str] = Field(None, description="Identifiant unique pour le champ AcroForm")
    subtitle: Optional[str] = Field(None, description="Sous-titre d'aide ou de précision")
    example: Optional[str] = Field(None, description="Exemple d'illustration")
    box_height_cm: Optional[float] = Field(None, gt=0, le=20, description="Hauteur de la zone de saisie en cm")
    field_prefix: Optional[str] = Field(None, description="Préfixe d'identifiants AcroForm")
    # Blocks of the reference workbooks
    questions: Optional[List[QuestionItemSpec]] = Field(None, description="Questions (questions_group)")
    min_box_height_cm: Optional[float] = Field(None, gt=0, le=20, description="Hauteur minimale des zones (questions_group)")
    max_box_height_cm: Optional[float] = Field(None, gt=0, le=20, description="Hauteur maximale des zones (questions_group)")
    safe_bottom_margin_cm: Optional[float] = Field(None, ge=0, le=20, description="Marge basse réservée (questions_group)")
    height_cm: Optional[float] = Field(None, gt=0, le=20, description="Hauteur (callout, space) en cm")
    col_widths_cm: Optional[List[float]] = Field(None, description="Largeurs des colonnes (table) en cm")
    color: Optional[str] = Field(None, description="Couleur : nom d'un pastel ('sky', 'mint'…) ou d'une couleur de la DA")
    size: Optional[float] = Field(None, ge=6, le=40, description="Corps du texte en points (heading, paragraphs, star_list)")
    gap_cm: Optional[float] = Field(None, ge=0, le=10, description="Espace entre paragraphes en cm")
    spacing_after_cm: Optional[float] = Field(None, ge=0, le=10, description="Espace après le bloc en cm")
    style: Optional[Literal["body", "italic", "subtitle"]] = Field(None, description="Style du texte (text)")
    font_size: Optional[float] = Field(None, ge=6, le=40, description="Corps du texte (text)")
    align: Optional[str] = Field(None, description="Alignement du texte (text)")
    arrow: Optional[bool] = Field(None, description="Flèche dessinée de l'annotation")
    width_ratio: Optional[float] = Field(None, gt=0, le=1, description="Largeur de l'annotation (part de la page)")
    steps: Optional[List[Any]] = Field(None, description="Étapes de la frise [[icône, titre, repère], …]")
    start_label: Optional[str] = Field(None, description="Libellé de départ de la frise")
    end_label: Optional[str] = Field(None, description="Libellé d'arrivée de la frise")
    hint: Optional[str] = Field(None, description="Ligne d'aide sous le titre (fields_card)")
    field_height_cm: Optional[float] = Field(None, gt=0, le=20, description="Hauteur par défaut des champs (fields_card)")
    question_labels: Optional[bool] = Field(None, description="Libellés en questions plutôt qu'en repères (fields_card)")
    count: Optional[int] = Field(None, ge=1, le=MAX_LIST_ITEMS, description="Nombre de lignes (numbered_lines)")
    line_height_cm: Optional[float] = Field(None, gt=0, le=5, description="Hauteur d'une ligne (numbered_lines)")
    start: Optional[int] = Field(None, ge=0, description="Premier numéro (numbered_lines)")
    values: Optional[List[Any]] = Field(None, description="Valeurs de l'échelle (rating_grid, 1 à 10 par défaut)")
    check_label: Optional[str] = Field(None, description="Case à cocher sous chaque carte (info_cards)")
    links: Optional[List[List[Any]]] = Field(None, description="Ressources [[nom, url, description], …] (link_card)")
    groups: Optional[List[Any]] = Field(None, description="Groupes de cases [[titre, [éléments]], …] (checklist_cards)")
    item_columns: Optional[int] = Field(None, ge=1, le=4, description="Colonnes de cases dans chaque carte")
    surface: Optional[str] = Field(None, description="Réponse « En surface » de l'exemple contrasté")
    exploitable: Optional[str] = Field(None, description="Réponse « Exploitable » de l'exemple contrasté")
    fixed: Optional[bool] = Field(None, description="Bloc fixe : la personnalisation ne le modifie jamais")
    data_id: Optional[str] = Field(
        None, pattern=DATA_ID_PATTERN, description="Identifiant de la donnée écrite dans ce bloc (ex : 'c4.seuils')"
    )

    @model_validator(mode="after")
    def check_reports(self):
        """Chaque ligne d'un report renvoie à une donnée d'un carnet : [libellé, 'c4.seuils', field_id]."""
        if self.type == "report":
            for item in self.items or []:
                data_id = item[1] if isinstance(item, (list, tuple)) and len(item) > 1 else None
                if not isinstance(data_id, str) or not re.match(DATA_ID_PATTERN, data_id):
                    raise ValueError(f"report : {item!r} doit être [libellé, identifiant de donnée, field_id]")
        return self

    @model_validator(mode="after")
    def check_scale_range(self):
        """Une échelle compte au plus MAX_SCALE_STEPS + 1 boutons radio."""
        if self.type == "scale":
            low = 0 if self.min_val is None else self.min_val
            high = 10 if self.max_val is None else self.max_val
            if not 0 < high - low <= MAX_SCALE_STEPS:
                raise ValueError(
                    f"échelle de {low} à {high} : max_val doit dépasser min_val de 1 à {MAX_SCALE_STEPS}"
                )
            self.min_val, self.max_val = low, high
        return self


class PageSpec(BaseModel):
    template: Literal[
        "cover",
        "summary",
        "recap",
        "questions",
        "meteo",
        "quadrants",
        "two_columns",
        "engagement",
        "enquete",
        "roadmap",
        "closing",
        "composite",
    ] = Field(..., description="Type de gabarit universel, ou 'composite' pour assemblage libre")
    title: str = Field("", description="Titre principal affiché en haut de la page")
    part_title: Optional[str] = Field(None, description="Sourcil au-dessus du titre (vide : aucun ; absent : automatique)")
    params: Dict[str, Any] = Field(
        default_factory=dict,
        description="Paramètres spécifiques selon le gabarit (questions, axes, etc.)",
    )
    blocks: Optional[List[BlockSpec]] = Field(
        None,
        max_length=MAX_BLOCKS_PER_PAGE,
        description="Liste des composants atomiques si template == 'composite'",
    )
    fixed: Optional[bool] = Field(None, description="Page fixe : la personnalisation ne la modifie jamais")
    data_id: Optional[str] = Field(
        None, pattern=DATA_ID_PATTERN, description="Identifiant de la donnée écrite sur cette page (ex : 'c4.livrable')"
    )


# A carnet of the bilan: 1 to 7, or the carnet de route
Carnet = Union[Annotated[int, Field(ge=1, le=PDFStyle.CARNET_COUNT)], Literal["route"]]


class WorkbookSpec(BaseModel):
    chapter_num: int = Field(1, description="Numéro du carnet (grand numéro de la couverture et de l'ouverture)")
    chapter_title: str = Field("Mes Réflexions", description="Titre principal du carnet")
    title: Optional[str] = Field(None, description="Alias pour chapter_title")
    subtitle: str = Field("BILAN DE COMPÉTENCES", description="Sous-titre de couverture")
    beneficiary_name: Optional[str] = Field(None, description="Nom ou prénom du bénéficiaire pour personnalisation")
    carnet: Optional[Carnet] = Field(
        None, description="Carnet du bilan, 1 à 7 ou 'route' : pastel, folio « carnet N/7 » ou « carnet de route »"
    )
    folio: Optional[str] = Field(None, max_length=MAX_NAME_LENGTH, description="Texte du folio (défaut : le titre)")
    pastel: Optional[str] = Field(None, description="Pastel dominant ('lilac', 'sky'…)")
    pdf_title: Optional[str] = Field(None, max_length=MAX_NAME_LENGTH, description="Titre des métadonnées du PDF")
    pages: List[PageSpec] = Field(
        default_factory=list, max_length=MAX_PAGES, description="Liste ordonnée des pages du livret"
    )

    @model_validator(mode="before")
    @classmethod
    def check_sizes(cls, data: Any) -> Any:
        _check_bounded(data)
        return data

    @model_validator(mode="before")
    @classmethod
    def sync_titles(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "title" in data and ("chapter_title" not in data or not data["chapter_title"]):
                data["chapter_title"] = data["title"]
            elif "chapter_title" in data and ("title" not in data or not data["title"]):
                data["title"] = data["chapter_title"]
        return data


# --- Customization: what is fixed stays fixed -------------------------------------

REF_KEY = "_ref"  # position of a page (« p3 ») or a block (« p3.b2 ») in the spec sent to Gemini
IDENTITY_KEYS = ("carnet", "folio", "pastel", "chapter_num")


def _page_is_fixed(page):
    return bool(page.get("fixed"))


def _block_is_fixed(block):
    return bool(block.get("fixed")) or block.get("type") in FIXED_BLOCK_TYPES


def _page_holds_fixed(page):
    return _page_is_fixed(page) or any(_block_is_fixed(b) for b in page.get("blocks") or [])


def tag_refs(spec: WorkbookSpec) -> dict:
    """The spec as a dict (set fields only) whose pages and blocks carry a '_ref', for keep_fixed."""
    data = spec.model_dump(exclude_unset=True, exclude_none=True)
    for i, page in enumerate(data.get("pages") or [], start=1):
        page[REF_KEY] = f"p{i}"
        for k, block in enumerate(page.get("blocks") or [], start=1):
            block[REF_KEY] = f"p{i}.b{k}"
    return data


def _strip_refs(value):
    if isinstance(value, dict):
        return {k: _strip_refs(v) for k, v in value.items() if k != REF_KEY}
    if isinstance(value, list):
        return [_strip_refs(v) for v in value]
    return value


def _merge(base_items, out_items, kind, is_fixed, merge_item, holds_fixed):
    """
    The output items, with each fixed base item back as it was: matched by '_ref', or by
    position when nothing was added nor removed; a fixed item that went missing comes back
    after the nearest item that precedes it in base.
    """
    by_ref = {b[REF_KEY]: b for b in base_items}
    out_items = [dict(o) for o in out_items if isinstance(o, dict)]
    if len(out_items) == len(base_items):
        for b, o in zip(base_items, out_items):
            if o.get(REF_KEY) not in by_ref and o.get(kind) == b.get(kind):
                o[REF_KEY] = b[REF_KEY]
    if out_items and any(holds_fixed(b) for b in base_items) and not any(o.get(REF_KEY) in by_ref for o in out_items):
        raise ValueError("la personnalisation a perdu la structure du livret")

    result, placed = [], {}
    for o in out_items:
        b = by_ref.get(o.get(REF_KEY))
        if b is None or b[REF_KEY] in placed:
            o.pop(REF_KEY, None)  # an item the customization added
            result.append(o)
            continue
        placed[b[REF_KEY]] = len(result)
        result.append(copy.deepcopy(b) if is_fixed(b) else merge_item(b, o))
    for i, b in enumerate(base_items):
        if b[REF_KEY] in placed or not is_fixed(b):
            continue
        pos = next((placed[p[REF_KEY]] + 1 for p in reversed(base_items[:i]) if p[REF_KEY] in placed), 0)
        placed = {ref: j + 1 if j >= pos else j for ref, j in placed.items()}
        placed[b[REF_KEY]] = pos
        result.insert(pos, copy.deepcopy(b))
    return result


def _merge_block(base, out):
    if base.get("data_id"):
        out["data_id"] = base["data_id"]
    return out


def _merge_page(base, out):
    if base.get("data_id"):
        out["data_id"] = base["data_id"]
    if base.get("blocks") is not None or out.get("blocks") is not None:
        out["blocks"] = _merge(base.get("blocks") or [], out.get("blocks") or [], "type", _block_is_fixed,
                               _merge_block, _block_is_fixed)
    return out


def keep_fixed(base: dict, out: dict) -> dict:
    """
    The customization rule, enforced: Gemini only changes what is adaptable. In `out` (the
    customized spec, as a dict), every page marked 'fixed', every block marked 'fixed' or of
    FIXED_BLOCK_TYPES comes back as in `base` (from tag_refs), even if it was changed or
    dropped. The identity of the document (carnet, folio, pastel, number) and the data ids
    stay as in base. Raises ValueError when the output lost both its references and its
    structure. Returns the merged spec without the '_ref' keys.
    """
    out = dict(out)
    for key in IDENTITY_KEYS:
        if key in base:
            out[key] = base[key]
        elif key != "chapter_num":
            out.pop(key, None)
    out["pages"] = _merge(base.get("pages") or [], out.get("pages") or [], "template", _page_is_fixed, _merge_page,
                          _page_holds_fixed)
    return _strip_refs(out)


def workbook_path(workbook_id: str) -> str:
    """Path of a reference workbook's JSON file (workbooks/<id>.json)."""
    return os.path.join(WORKBOOKS_DIR, f"{workbook_id}.json")


def load_workbook(workbook_id: str) -> WorkbookSpec:
    """A reference workbook, read and validated from workbooks/<id>.json."""
    with open(workbook_path(workbook_id), encoding="utf-8") as f:
        return WorkbookSpec.model_validate(json.load(f))
