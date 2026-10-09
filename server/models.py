"""
Pydantic Schemas of the API requests. The workbook format itself (WorkbookSpec, PageSpec,
BlockSpec) lives in Scripts/workbook_generator/spec.py, shared with the CLI documents.
"""

import os
import sys
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, model_validator

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from workbook_generator.spec import (  # noqa: E402  (re-exported for the server and the tests)
    BASE_BLOCK_TYPES,
    MAX_BLOCKS_PER_PAGE,
    MAX_LIST_ITEMS,
    MAX_NAME_LENGTH,
    MAX_NESTING_DEPTH,
    MAX_PAGES,
    MAX_PARTS,
    MAX_SCALE_STEPS,
    MAX_TEXT_LENGTH,
    BlockSpec,
    PageSpec,
    QuadrantItemSpec,
    QuestionItemSpec,
    SummaryPointSpec,
    TwoColumnsRowSpec,
    WorkbookSpec,
)

# Garde-fous contre les entrées démesurées (client ou LLM) : au-delà, l'API répond 422.
MAX_NOTES_LENGTH = 50_000
MAX_INSTRUCTION_LENGTH = 5_000


# Writing time of the former length formats, for clients that still send 'book_format'
BOOK_FORMAT_MINUTES = {"short": 45, "standard": 75, "deep": 120}


class ParseRequest(BaseModel):
    raw_notes: str = Field(..., max_length=MAX_NOTES_LENGTH, description="Notes de séance brutes ou texte au kilomètre")
    chapter_num: Optional[int] = Field(
        None, ge=0, le=20,
        description="Numéro du carnet (1 à 7 : un carnet du bilan) ; vide ou 0 : un document hors de la suite des carnets",
    )
    chapter_title: Optional[str] = Field(None, max_length=MAX_NAME_LENGTH, description="Titre souhaité (optionnel, inféré si omis)")
    beneficiary_name: Optional[str] = Field(None, max_length=MAX_NAME_LENGTH, description="Prénom ou nom du bénéficiaire")
    duration_min: Optional[int] = Field(
        None, ge=10, le=300, description="Durée d'écriture visée, en minutes (vide : selon les notes)"
    )
    meteo_option: Optional[
        Literal["auto", "none", "classic", "clarity", "mental_load"]
    ] = Field(
        "auto",
        description="Météo de l'énergie : 'classic' (oui), 'none' (non), 'auto' (si les notes parlent de l'énergie "
                    "ou de l'état d'esprit) ; 'clarity' et 'mental_load', anciennes valeurs, valent 'classic'",
    )
    session_focus: Optional[
        Literal["auto", "bilan", "decision", "action"]
    ] = Field("auto", description="Ancien champ de l'interface, sans effet")
    book_format: Optional[
        Literal["auto", "short", "standard", "deep"]
    ] = Field(
        None,
        description="Ancien format de longueur, pris en durée d'écriture quand duration_min est vide : "
                    "'short' 45 min, 'standard' 1 h 15, 'deep' 2 h, 'auto' selon les notes",
    )
    include_engagement: Optional[bool] = Field(
        True,
        description="Finir par la page du livrable (engagements et trois zones guidées)",
    )

    def writing_minutes(self) -> Optional[int]:
        """The writing time asked for, in minutes, or None to follow the notes."""
        return self.duration_min or BOOK_FORMAT_MINUTES.get(self.book_format or "")

    def wants_energy(self) -> Optional[bool]:
        """True, False, or None when the notes decide (they speak of energy or state of mind)."""
        option = self.meteo_option or "auto"
        return None if option == "auto" else option != "none"



class IterateRequest(BaseModel):
    current_spec: WorkbookSpec = Field(..., description="Spécification actuelle du livret à modifier")
    feedback: str = Field(..., max_length=MAX_INSTRUCTION_LENGTH, description="Consigne d'ajustement ou feedback utilisateur")
    raw_notes: Optional[str] = Field(None, max_length=MAX_NOTES_LENGTH, description="Notes de séance brutes d'origine pour contexte")


class IterateResponse(BaseModel):
    spec: WorkbookSpec = Field(..., description="Spécification mise à jour du livret")
    changes_summary: str = Field(..., description="Explication concise des modifications apportées")
    pedagogical_note: Optional[str] = Field(None, description="Note ou conseil pédagogique sur l'ajustement")


class TemplateInfo(BaseModel):
    id: str = Field(..., description="Identifiant unique du livret modèle")
    chapter_num: int = Field(..., description="Numéro du carnet")
    title: str = Field(..., description="Titre du livret")
    subtitle: str = Field(..., description="Sous-titre de couverture")
    description: str = Field(..., description="Brève description pédagogique")
    page_count: int = Field(..., description="Nombre de pages du PDF, pages « (suite) » comprises")
    icon: str = Field(..., description="Nom d'une icône Material Symbols Outlined pour l'affichage")
    category: str = Field("Bilan de Compétences", description="Catégorie du modèle")
    parts: List[str] = Field(default_factory=list, description="Parties d'un long livret, personnalisées une à une")


class PageCountResponse(BaseModel):
    page_count: int = Field(..., description="Nombre de pages du PDF, pages « (suite) » comprises")


class CheckRequest(BaseModel):
    spec: WorkbookSpec = Field(..., description="Spécification à contrôler")
    context: Optional[str] = Field(
        None, max_length=MAX_INSTRUCTION_LENGTH,
        description="Profil de la personne (personnalisation) : un exemple tiré de son métier est alors signalé",
    )
    structure: bool = Field(True, description="Contrôler aussi le gabarit commun des carnets")
    layout: bool = Field(True, description="Compiler la maquette pour repérer les pages « (suite) » presque vides")


class FindingInfo(BaseModel):
    level: str = Field(..., description="« à corriger » ou « à vérifier »")
    page: Optional[int] = Field(None, description="Page de la maquette, à partir de 1 (vide : tout le document)")
    rule: str = Field(..., description="Règle en cause")
    message: str = Field(..., description="Ce qui ne va pas, et comment faire")


class CustomizeRequest(BaseModel):
    template_id: Optional[str] = Field(None, max_length=50, description="Identifiant du modèle de base (ex: 'carnet-1')")
    base_spec: Optional[WorkbookSpec] = Field(None, description="Spécification de base si livret personnalisé ou importé")
    beneficiary_name: str = Field(..., max_length=MAX_NAME_LENGTH, description="Prénom ou nom complet du bénéficiaire")
    beneficiary_context: str = Field(..., max_length=MAX_INSTRUCTION_LENGTH, description="Profil, métier actuel, projet visé, défis majeurs")
    custom_instructions: Optional[str] = Field(None, max_length=MAX_INSTRUCTION_LENGTH, description="Consignes spécifiques d'adaptation souhaitées")
    part: Optional[int] = Field(
        None, ge=1, le=MAX_PARTS, description="Partie à personnaliser d'un livret découpé en parties (tout le livret si omis)"
    )

    @model_validator(mode="after")
    def check_base(self):
        if not self.template_id and self.base_spec is None:
            raise ValueError("indiquez un modèle de livret (template_id) ou une spécification de base (base_spec)")
        return self


class CustomizeResponse(BaseModel):
    spec: WorkbookSpec = Field(..., description="Spécification personnalisée du livret")
    customizations_summary: str = Field(..., description="Résumé des adaptations clés apportées pour ce profil")
    pedagogical_note: Optional[str] = Field(None, description="Conseil pédagogique pour l'accompagnement")


