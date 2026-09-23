"""
Pydantic Schemas for Workbook Definition, Templates, and API Requests.
"""

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, model_validator


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
    columns: Optional[int] = Field(2, description="Nombre de colonnes (cards_grid ou checklist)")
    card_height_cm: Optional[float] = Field(None, description="Hauteur personnalisée des cartes en cm")
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
    box_height_cm: Optional[float] = Field(None, description="Hauteur de la zone de saisie en cm")
    field_prefix: Optional[str] = Field(None, description="Préfixe d'identifiants AcroForm")


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
        description="Liste des composants atomiques si template == 'composite'",
    )


class WorkbookSpec(BaseModel):
    chapter_num: int = Field(1, description="Numéro du chapitre")
    chapter_title: str = Field("Mes Réflexions", description="Titre principal du chapitre")
    title: Optional[str] = Field(None, description="Alias pour chapter_title")
    subtitle: str = Field("BILAN DE COMPÉTENCES & ALIGNEMENT", description="Sous-titre de couverture")
    theme: Literal["indigo", "earth"] = Field("indigo", description="Palette de couleur ('indigo' ou 'earth')")
    beneficiary_name: Optional[str] = Field(None, description="Nom ou prénom du bénéficiaire pour personnalisation")
    pages: List[PageSpec] = Field(default_factory=list, description="Liste ordonnée des pages du livret")

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
    raw_notes: str = Field(..., description="Notes de séance brutes ou texte au kilomètre")
    chapter_num: int = Field(1, description="Numéro du chapitre")
    chapter_title: Optional[str] = Field(None, description="Titre souhaité (optionnel, inféré si omis)")
    theme: Literal["indigo", "earth"] = Field("indigo", description="Thème de couleur")
    beneficiary_name: Optional[str] = Field(None, description="Prénom ou nom du coaché")
    api_key: Optional[str] = Field(None, description="Clé API Gemini facultative si non configurée sur le serveur")
