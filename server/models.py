"""
Pydantic Schemas for Workbook Definition, Templates, and API Requests.
"""

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, model_validator

# Garde-fous contre les entrées démesurées (client ou LLM) : au-delà, l'API répond 422.
MAX_NOTES_LENGTH = 50_000
MAX_INSTRUCTION_LENGTH = 5_000
MAX_NAME_LENGTH = 200
MAX_PAGES = 30
MAX_BLOCKS_PER_PAGE = 10
MAX_LIST_ITEMS = 30
MAX_TEXT_LENGTH = 2_000
MAX_NESTING_DEPTH = 10
MAX_SCALE_STEPS = 10


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


class BlockSpec(BaseModel):
    type: Literal[
        "callout",
        "cards_grid",
        "scale",
        "checklist",
        "table",
        "stat_boxes",
        "question",
        "text",
    ] = Field(..., description="Type de composant atomique")
    text: Optional[str] = Field(None, description="Contenu texte principal (callout, text, ou intitulé question)")
    title: Optional[str] = Field(None, description="Titre optionnel du composant")
    variant: Optional[str] = Field("info", description="Variante visuelle : 'info', 'tip', 'quote'")
    cards: Optional[List[Dict[str, Any]]] = Field(None, description="Cartes pour grille [{'title': '...', 'subtitle': '...', 'field_id': '...'}]")
    columns: Optional[int] = Field(2, ge=1, le=4, description="Nombre de colonnes (cards_grid ou checklist)")
    card_height_cm: Optional[float] = Field(None, gt=0, le=20, description="Hauteur personnalisée des cartes en cm")
    label: Optional[str] = Field(None, description="Libellé de la jauge / échelle ou stat")
    min_val: Optional[int] = Field(0, description="Valeur minimale (scale)")
    max_val: Optional[int] = Field(10, description="Valeur maximale (scale)")
    min_label: Optional[str] = Field("", description="Libellé borne min (scale)")
    max_label: Optional[str] = Field("", description="Libellé borne max (scale)")
    items: Optional[List[Any]] = Field(None, description="Éléments de checklist")
    headers: Optional[List[str]] = Field(None, description="En-têtes de colonnes (table)")
    rows: Optional[List[List[Any]]] = Field(None, description="Lignes du tableau")
    stats: Optional[List[Dict[str, Any]]] = Field(None, description="Indicateurs clés [{'stat': '...', 'label': '...'}]")
    question: Optional[str] = Field(None, description="Intitulé de la question (question block)")
    field_id: Optional[str] = Field(None, description="Identifiant unique pour le champ AcroForm")
    subtitle: Optional[str] = Field(None, description="Sous-titre d'aide ou de précision")
    example: Optional[str] = Field(None, description="Exemple d'illustration")
    box_height_cm: Optional[float] = Field(None, gt=0, le=20, description="Hauteur de la zone de saisie en cm")
    field_prefix: Optional[str] = Field(None, description="Préfixe d'identifiants AcroForm")

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
        "questions",
        "meteo",
        "quadrants",
        "two_columns",
        "engagement",
        "enquete",
        "roadmap",
        "closing",
        "composite",
    ] = Field(..., description="Type de gabarit universel parmi les 10 disponibles ou 'composite' pour assemblage libre")
    title: str = Field("", description="Titre principal affiché en haut de la page")
    part_title: Optional[str] = Field(None, description="Mention d'en-tête de partie (ex: '1. RÉCAPITULATIF')")
    params: Dict[str, Any] = Field(
        default_factory=dict,
        description="Paramètres spécifiques selon le gabarit (questions, axes, etc.)",
    )
    blocks: Optional[List[BlockSpec]] = Field(
        None,
        max_length=MAX_BLOCKS_PER_PAGE,
        description="Liste des composants atomiques si template == 'composite'",
    )


class WorkbookSpec(BaseModel):
    chapter_num: int = Field(1, description="Numéro du chapitre")
    chapter_title: str = Field("Mes Réflexions", description="Titre principal du chapitre")
    title: Optional[str] = Field(None, description="Alias pour chapter_title")
    subtitle: str = Field("BILAN DE COMPÉTENCES & ALIGNEMENT", description="Sous-titre de couverture")
    beneficiary_name: Optional[str] = Field(None, description="Nom ou prénom du bénéficiaire pour personnalisation")
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


class ParseRequest(BaseModel):
    raw_notes: str = Field(..., max_length=MAX_NOTES_LENGTH, description="Notes de séance brutes ou texte au kilomètre")
    chapter_num: int = Field(1, description="Numéro du chapitre")
    chapter_title: Optional[str] = Field(None, max_length=MAX_NAME_LENGTH, description="Titre souhaité (optionnel, inféré si omis)")
    beneficiary_name: Optional[str] = Field(None, max_length=MAX_NAME_LENGTH, description="Prénom ou nom du bénéficiaire")
    meteo_option: Optional[
        Literal["auto", "none", "classic", "clarity", "mental_load"]
    ] = Field(
        "auto",
        description="Option de check-in / météo : 'auto' (décision IA), 'none' (pas de météo), 'classic' (météo classique), 'clarity' (boussole/intention), 'mental_load' (charge mentale)",
    )
    session_focus: Optional[
        Literal["auto", "bilan", "decision", "action"]
    ] = Field(
        "auto",
        description="Focus pédagogique dominant : 'auto' (libre), 'bilan' (diagnostic/recul), 'decision' (arbitrage/comparatif), 'action' (plan d'action/roadmap)",
    )
    book_format: Optional[
        Literal["auto", "short", "standard", "deep"]
    ] = Field(
        "standard",
        description="Format de longueur : 'short' (court, 6-7p), 'standard' (7-10p), 'deep' (complet, + de 10p)",
    )
    include_engagement: Optional[bool] = Field(
        True,
        description="Inclure la page de pacte d'engagement et signature en fin de livret",
    )
    api_key: Optional[str] = Field(None, description="Clé API Gemini facultative si non configurée sur le serveur")



class IterateRequest(BaseModel):
    current_spec: WorkbookSpec = Field(..., description="Spécification actuelle du livret à modifier")
    feedback: str = Field(..., max_length=MAX_INSTRUCTION_LENGTH, description="Consigne d'ajustement ou feedback utilisateur")
    raw_notes: Optional[str] = Field(None, max_length=MAX_NOTES_LENGTH, description="Notes de séance brutes d'origine pour contexte")
    api_key: Optional[str] = Field(None, description="Clé API Gemini facultative si non configurée sur le serveur")


class IterateResponse(BaseModel):
    spec: WorkbookSpec = Field(..., description="Spécification mise à jour du livret")
    changes_summary: str = Field(..., description="Explication concise des modifications apportées")
    pedagogical_note: Optional[str] = Field(None, description="Note ou conseil pédagogique sur l'ajustement")


class TemplateInfo(BaseModel):
    id: str = Field(..., description="Identifiant unique du livret modèle")
    chapter_num: int = Field(..., description="Numéro du chapitre")
    title: str = Field(..., description="Titre du livret")
    subtitle: str = Field(..., description="Sous-titre de couverture")
    description: str = Field(..., description="Brève description pédagogique")
    page_count: int = Field(..., description="Nombre de pages du livret")
    icon: str = Field(..., description="Emoji distinctif pour l'affichage")
    category: str = Field("Bilan de Compétences", description="Catégorie du modèle")


class CustomizeRequest(BaseModel):
    template_id: Optional[str] = Field(None, max_length=50, description="Identifiant du modèle de base (ex: 'chap1')")
    base_spec: Optional[WorkbookSpec] = Field(None, description="Spécification de base si livret personnalisé ou importé")
    beneficiary_name: str = Field(..., max_length=MAX_NAME_LENGTH, description="Prénom ou nom complet du bénéficiaire")
    beneficiary_context: str = Field(..., max_length=MAX_INSTRUCTION_LENGTH, description="Profil, métier actuel, projet visé, défis majeurs")
    custom_instructions: Optional[str] = Field(None, max_length=MAX_INSTRUCTION_LENGTH, description="Consignes spécifiques d'adaptation souhaitées")
    api_key: Optional[str] = Field(None, description="Clé API Gemini facultative si non configurée sur le serveur")

    @model_validator(mode="after")
    def check_base(self):
        if not self.template_id and self.base_spec is None:
            raise ValueError("indiquez un modèle de livret (template_id) ou une spécification de base (base_spec)")
        return self


class CustomizeResponse(BaseModel):
    spec: WorkbookSpec = Field(..., description="Spécification personnalisée du livret")
    customizations_summary: str = Field(..., description="Résumé des adaptations clés apportées pour ce profil")
    pedagogical_note: Optional[str] = Field(None, description="Conseil pédagogique pour l'accompagnement")


