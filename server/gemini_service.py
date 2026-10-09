"""
Gemini: turns a consultant's notes into a document (WorkbookSpec), customizes a reference
workbook for a person, and retouches a document on request. The rules every prompt carries
live in prompt_rules.py.
"""

import os
import json
import logging
import re
from functools import lru_cache
from typing import Any, Callable, List, NamedTuple, Optional
from google import genai
from google.genai import types

from .models import (
    WorkbookSpec,
    PageSpec,
    BlockSpec,
    QuestionItemSpec,
    ParseRequest,
    IterateRequest,
    IterateResponse,
    CustomizeRequest,
    CustomizeResponse,
)
from .predefined_workbooks import get_predefined_spec
from .prompt_rules import (
    ANSWER_RULES,
    BLOCKS_DOC,
    CHARGE_RULES,
    EXAMPLE_PAGE,
    EXERCISE_RULES,
    PERSONALIZATION_RULES,
    REFERENCE_BLOCKS_RULES,
    TEMPLATE_RULES,
    TONE_RULES,
)
from workbook_generator.config import PDFStyle
from workbook_generator.primitives import plain_title
from workbook_generator.spec import keep_fixed, part_of, put_part_back, tag_refs

logger = logging.getLogger(__name__)

# Modèles essayés dans l'ordre, configurables sans redéploiement de code (ex: GEMINI_MODELS="gemini-x-flash,gemini-y-flash")
GEMINI_MODELS = [
    m.strip()
    for m in os.environ.get("GEMINI_MODELS", "gemini-3.8-flash").split(",")
    if m.strip()
]
# Délai maximal d'un appel Gemini (une analyse prend ~30 s ; Cloud Run coupe la requête à 300 s)
GEMINI_TIMEOUT_S = float(os.environ.get("GEMINI_TIMEOUT_S", "120"))


@lru_cache(maxsize=4)
def _get_client(api_key: str) -> genai.Client:
    """Un client par clé API, réutilisé d'une requête à l'autre."""
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=int(GEMINI_TIMEOUT_S * 1000)),
    )


class GenerationResult(NamedTuple):
    """Résultat d'une génération : fallback_reason vaut None quand Gemini a répondu,
    sinon 'no_api_key' ou 'model_error' (le contenu vient alors du modèle de secours)."""

    value: Any
    fallback_reason: Optional[str] = None


def _generate_json(
    api_key: str, system_prompt: str, user_prompt: str, build: Callable[[dict], Any], label: str
) -> Optional[Any]:
    """
    Essaie chaque modèle de GEMINI_MODELS et retourne build(json) au premier succès,
    ou None si tous les modèles ont échoué.
    """
    client = _get_client(api_key)
    last_err = None

    for model_name in GEMINI_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    system_instruction=system_prompt,
                ),
            )
            raw_text = response.text.strip() if response.text else ""
            if not raw_text:
                continue
            # Strip markdown code blocks if wrapped by model
            if raw_text.startswith("```"):
                lines = raw_text.splitlines()
                if lines and lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw_text = "\n".join(lines).strip()

            return build(json.loads(raw_text))
        except Exception as e:
            logger.warning(f"Error calling {model_name} in {label}: {e}")
            last_err = e

    logger.error(f"{label}: all Gemini models failed ({last_err}). Falling back to heuristic.")
    return None


def _spec_json(spec: WorkbookSpec) -> str:
    """A spec as compact JSON for a prompt: only what it sets, without the empty fields."""
    return json.dumps(spec.model_dump(exclude_unset=True, exclude_none=True), ensure_ascii=False)


SYSTEM_PROMPT = """Tu es ingénieur pédagogique pour Marge de Manœuvre (bilans de compétences 100 % à distance, tournés vers la décision et l'action).
À partir des notes d'un consultant, tu conçois un document que la personne accompagnée remplit seule, entre deux séances (un PDF à remplir à l'écran ou sur papier) : un carnet de bord, ou un outil sur un thème précis (« Mes enquêtes métiers », « Préparer mon entretien »).
Les notes donnent le fond : garde leurs thèmes, leurs questions et leurs exercices, sans en perdre ; reformule-les seulement pour suivre nos règles. La forme suit nos carnets, décrits ci-dessous.

""" + "\n".join((TEMPLATE_RULES, EXERCISE_RULES, CHARGE_RULES, ANSWER_RULES, BLOCKS_DOC, EXAMPLE_PAGE, TONE_RULES)) + """
FORMAT DE RÉPONSE : uniquement un objet JSON, de cette forme :
{
  "chapter_title": "Mes enquêtes métiers",
  "subtitle": "Bilan de compétences",
  "folio": "Mes enquêtes métiers",
  "pastel": "lilac",
  "pages": [
    {"template": "cover", "params": {"cover_title": "Mes enquêtes *métiers.*", "number": "", "tagline": "Bilan de compétences", "promise": "Ce que le document apporte, en 3 à 8 mots."}},
    {"template": "summary", "title": "Préparer *l'échange.*", "params": {"num": "", "intro_text": "Le but du document, en deux ou trois phrases.", "points": ["Exercice 1 · … · 15 min", "Exercice 2 · … · 20 min", "Fin de carnet · 5 min"], "duration": "40 min", "split": "En une fois, ou en deux : … ."}},
    {"template": "composite", "title": "…", "part_title": "Exercice 1 · … · 15 min", "blocks": [{"type": "paragraphs", "items": ["…"]}]},
    {"template": "engagement", "title": "Votre livrable.", "part_title": "Fin de carnet · 5 min", "params": {"livrable_title": "…", "livrable_text": "…", "lines": ["…", "…"], "zones": ["Ce qui m'étonne en relisant mes réponses", "À aborder en séance : …", "Ce que j'ai laissé vierge, à reprendre ensemble"], "field_prefix": "enq_livrable"}},
    {"template": "closing", "params": {"messages": ["…", "…"]}}
  ]
}
'pastel' : sky, lilac, mint, almond, blush ou jasmine. 'beneficiary_name' : seulement si un prénom est donné.
"""


def _duration_text(minutes: int) -> str:
    """75 -> « 1 h 15 », 45 -> « 45 min », 120 -> « 2 h »."""
    hours, rest = divmod(int(minutes), 60)
    if not hours:
        return f"{rest} min"
    return f"{hours} h {rest:02d}" if rest else f"{hours} h"


def _parse_user_prompt(request: ParseRequest) -> str:
    """The notes, then what the consultant chose in the form."""
    minutes = request.writing_minutes()
    num = request.chapter_num
    energy = {
        True: "Météo de l'énergie : oui, sur la page qui suit l'ouverture.",
        False: "Météo de l'énergie : non, aucune page météo.",
        None: "Météo de l'énergie : seulement si les notes parlent de l'énergie, de la fatigue ou de l'état "
              "d'esprit de la personne ; sinon, aucune page météo.",
    }[request.wants_energy()]
    choices = [
        f"Titre souhaité : {request.chapter_title}" if request.chapter_title
        else "Titre : à tirer des notes, court, sans le prénom de la personne.",
        f"Numéro de carnet : {num}. En tête, \"chapter_num\": {num} ; couverture \"number\": {num}, ouverture "
        f"\"num\": \"{num}\"." if num
        else "Numéro de carnet : aucun. Le document est hors de la suite des carnets : couverture \"number\": \"\", "
             "ouverture \"num\": \"\", et \"folio\" et \"pastel\" en tête.",
        f"Bénéficiaire : {request.beneficiary_name} (\"beneficiary_name\")." if request.beneficiary_name
        else "Bénéficiaire : non précisé. N'écris aucun prénom.",
        f"Durée d'écriture visée : {_duration_text(minutes)}. Comptez 10 à 20 minutes par exercice, 2 min pour la "
        "météo, 5 min pour la fin : la somme des lignes de l'ouverture fait cette durée." if minutes
        else "Durée d'écriture : à tirer des notes, 10 à 20 minutes par exercice ; 'duration' en donne la somme.",
        energy,
        "Page de livrable : oui." if request.include_engagement
        else "Page de livrable : non ; le document finit par son dos.",
    ]
    return ("NOTES DU CONSULTANT :\n---\n" + request.raw_notes + "\n---\n\nSES CHOIX :\n- " + "\n- ".join(choices)
            + "\n\nConçois le document et réponds avec son JSON.")


def _finalize_created_spec(spec: WorkbookSpec, request: ParseRequest) -> WorkbookSpec:
    """
    What the consultant chose, whatever the model wrote: a carnet of the bilan (1 to 7)
    takes its number, pastel and folio from the carnet; any other document shows no
    number and keeps a folio (its short title) and a pastel; no beneficiary unless given.
    """
    data = spec.model_dump(exclude_unset=True, exclude_none=True)
    num = request.chapter_num or None
    title = plain_title(data.get("chapter_title") or data.get("title") or "").rstrip(".!?… ")
    pastel, folio = data.pop("pastel", None), data.pop("folio", None)
    data.pop("carnet", None)
    data.pop("chapter_num", None)
    if num:
        data["chapter_num"] = num
        if num <= PDFStyle.CARNET_COUNT:
            data["carnet"] = num
    if not num or num > PDFStyle.CARNET_COUNT:
        if folio or title:
            data["folio"] = folio or title
        if pastel in PDFStyle.PASTELS:
            data["pastel"] = pastel
    if request.beneficiary_name:
        data["beneficiary_name"] = request.beneficiary_name
    else:
        data.pop("beneficiary_name", None)
    for page in data.get("pages") or []:
        params = page.setdefault("params", {}) if page.get("template") in ("cover", "summary") else None
        if page.get("template") == "cover":
            params["number"] = num or ""
        elif page.get("template") == "summary":
            params["num"] = str(num) if num else ""
        elif not num and page.get("template") != "closing" and page.get("part_title") is None:
            page["part_title"] = ""  # never « 1. TITRE » on a document without a number
    return WorkbookSpec(**data)


def parse_notes_with_gemini(request: ParseRequest) -> GenerationResult:
    """
    Turns a consultant's notes into a document (WorkbookSpec) that follows the common
    template of the carnets. Without a key, or when every model fails, the fallback builds
    one from the questions of the notes, and GenerationResult.fallback_reason says so.
    """
    api_key = os.environ.get("GEMINI_API_KEY")  # from Secret Manager in production

    if not api_key:
        logger.warning("GEMINI_API_KEY not found. Using the fallback document.")
        return GenerationResult(_build_fallback_spec(request), "no_api_key")

    spec = _generate_json(
        api_key, SYSTEM_PROMPT, _parse_user_prompt(request), lambda data: WorkbookSpec(**data), "parse"
    )
    if spec is None:
        return GenerationResult(_build_fallback_spec(request), "model_error")
    return GenerationResult(_finalize_created_spec(spec, request))


# --- Fallback document: the common template, built from the notes without a model -----

# Words of the notes that call for the safety protocol (forte charge)
HEAVY_NOTES = re.compile(
    r"\b(?:peurs?|deuil|honte|harcèlement|burn-?out|épuis\w*|licenci\w*|souffrance|culpabilit\w*|colère|échecs?"
    r"|conflits?)\b",
    re.IGNORECASE,
)
QUESTION_MAX = 120
GENERIC_QUESTIONS = [
    ("Ce que je retiens de la dernière séance", "sentence"),
    ("Ce que je veux approfondir avant la prochaine", "sentence"),
    ("Ce que je décide d'essayer d'ici là", "sentence"),
]


def _questions_of_notes(notes: str) -> List[str]:
    """The questions the notes ask: each line, or sentence, that ends with a « ? »."""
    found = []
    for line in notes.splitlines():
        line = re.sub(r"^[\s\-•*·]*(?:Q\d+\s*[:.)-]\s*)?", "", line).strip()
        if line.endswith("?") and 10 <= len(line) <= QUESTION_MAX:
            if line.isupper():
                line = line[0] + line[1:].lower()
            if line not in found:
                found.append(line)
    return found[:12]


def _build_fallback_spec(request: ParseRequest) -> WorkbookSpec:
    """
    A document without a model, in the common template of the carnets: cover, opener with
    the writing time, the weather of the day if asked, the questions of the notes (or three
    generic ones) with a contrast example, the protocol when the notes are heavy, the next
    step, the deliverable and the back cover.
    """
    notes = request.raw_notes or ""
    title = (request.chapter_title or "Votre carnet de travail").strip().rstrip(".!?… ")
    minutes = request.writing_minutes() or 45
    energy = request.wants_energy()
    energy = bool(energy) if energy is not None else bool(re.search(r"énergie|fatigu|météo|humeur", notes, re.I))
    heavy = bool(HEAVY_NOTES.search(notes))
    questions = [(q, "sentence") for q in _questions_of_notes(notes)] or GENERIC_QUESTIONS

    end = 5 if request.include_engagement else 0
    first = max(10, minutes - (2 if energy else 0) - end - 10)

    pages = [PageSpec(template="cover", params={
        "cover_title": f"{title}.", "tagline": "Bilan de compétences",
        "promise": "Vos réponses, pour la prochaine séance.",
    })]
    points = (["Météo · 2 min"] if energy else []) + [
        f"Exercice 1 · Vos réponses · {_duration_text(first)}",
        "Exercice 2 · Votre prochain pas · 10 min",
    ] + (["Fin de carnet · 5 min"] if request.include_engagement else [])
    pages.append(PageSpec(template="summary", title="Avant la prochaine *séance.*", params={
        "intro_text": "Ce carnet reprend les questions de votre dernière séance. Répondez à votre rythme : "
                      "nous relirons vos réponses ensemble.",
        "points": points,
        "duration": _duration_text(first + 10 + (2 if energy else 0) + end),
        "split": "En une fois, ou en deux : l'exercice 1, puis la suite.",
    }))
    if energy:
        pages.append(PageSpec(template="composite", title="Avant de *commencer.*", part_title="Météo · 2 min",
                              blocks=[BlockSpec(type="energy", field_prefix="doc_meteo")]))

    blocks = [BlockSpec(type="protocol", text="Certaines questions de cette page touchent à ce qui pèse.")] if heavy else []
    blocks += [
        BlockSpec(type="paragraphs", items=["Les questions de la séance, à reprendre avec vos mots : "
                                            "des faits, des exemples, ce que vous en tirez."]),
        BlockSpec(type="contrast_example", title="Géomètre", surface="Je vais essayer d'y penser.",
                  exploitable="Mardi, je décline la réunion de 18 h et je propose un point de quinze minutes "
                              "le lendemain matin."),
        BlockSpec(type="questions_group", questions=[
            QuestionItemSpec(question=q, field_id=f"doc_q{k}", answer=answer)
            for k, (q, answer) in enumerate(questions, start=1)
        ]),
    ]
    pages.append(PageSpec(template="composite", title="Vos *réponses.*",
                          part_title=f"Exercice 1 · Vos réponses · {_duration_text(first)}", blocks=blocks))

    next_step = [
        BlockSpec(type="paragraphs", items=["Un pas concret d'ici la prochaine séance, même petit."]),
        BlockSpec(type="fields_card", question_labels=True, rows=[
            [["Ce que je fais", "doc_pas", "sentence"]],
            [["Quand", "doc_pas_quand", "word"], ["Ce qui pourrait m'en empêcher", "doc_pas_obstacle", "sentence"]],
        ]),
    ]
    if heavy:
        next_step.append(BlockSpec(type="anchor", field_id="doc_ancrage"))
    pages.append(PageSpec(template="composite", title="Votre prochain *pas.*",
                          part_title="Exercice 2 · Votre prochain pas · 10 min", blocks=next_step))
    if request.include_engagement:
        pages.append(PageSpec(template="engagement", title="Votre livrable.", part_title="Fin de carnet · 5 min", params={
            "livrable_title": "Vos réponses et votre prochain pas",
            "livrable_text": "Ce que vous retenez de la séance et ce que vous décidez d'essayer. Nous les relisons "
                             "ensemble à la prochaine séance.",
            "lines": ["Je fais mon prochain pas avant la séance.", "J'apporte ce carnet à la prochaine séance."],
            "zones": ["Ce qui m'étonne en relisant mes réponses",
                      "À aborder en séance : une question restée sans réponse",
                      "Ce que j'ai laissé vierge, à reprendre ensemble"],
            "field_prefix": "doc_livrable",
        }))
    pages.append(PageSpec(template="closing", params={"messages": [
        "Ce carnet reste le vôtre.", "Prochaine étape : la séance. Apportez ce carnet.",
    ]}))
    spec = WorkbookSpec(chapter_title=title, subtitle="Bilan de compétences", pages=pages)
    return _finalize_created_spec(spec, request)


ITERATE_SYSTEM_PROMPT = """Tu es ingénieur pédagogique pour Marge de Manœuvre (bilans de compétences 100 % à distance, tournés vers la décision et l'action).
On te donne un document à remplir (WorkbookSpec) et une consigne du consultant qui le prépare.

TON RÔLE :
1. Appliquer la consigne, précisément, et rien d'autre : les pages et les blocs qu'elle ne vise pas restent tels quels, mot pour mot.
2. Une page ou un bloc qui porte "fixed": true ne change que si la consigne le demande expressément.
3. Un exercice ajouté ou réécrit suit nos règles ci-dessous (sourcil « Exercice N · nom · durée », phrase d'ouverture, exemple contrasté, tailles de case, charge émotionnelle) ; mets à jour la liste et la durée totale de l'ouverture ('points', 'duration').
4. Garde l'ordre du gabarit : couverture, ouverture, météo s'il y en a une, exercices, livrable, dos.
5. Résumer ce que tu as changé, en une à trois phrases.

""" + "\n".join((REFERENCE_BLOCKS_RULES, EXERCISE_RULES, CHARGE_RULES, ANSWER_RULES, BLOCKS_DOC, TONE_RULES)) + """
FORMAT DE RÉPONSE : uniquement un objet JSON :
{
  "spec": { …le document complet, modifié… },
  "changes_summary": "Ce que tu as modifié, ajouté ou supprimé.",
  "pedagogical_note": "Une courte justification pédagogique."
}
"""


def refine_spec_with_gemini(request: IterateRequest) -> GenerationResult:
    """
    Refines an existing WorkbookSpec based on conversational user feedback using Gemini Flash.
    Tries the models of GEMINI_MODELS in order.
    """
    api_key = os.environ.get("GEMINI_API_KEY")  # from Secret Manager in production

    if not api_key:
        logger.warning(
            "GEMINI_API_KEY not found. Using structured heuristic iteration fallback."
        )
        return GenerationResult(_build_fallback_iteration(request), "no_api_key")

    current_json = _spec_json(request.current_spec)

    notes_context = (
        f"\nNOTES DE SÉANCE D'ORIGINE :\n{request.raw_notes}\n"
        if request.raw_notes
        else ""
    )

    user_prompt = f"""Voici la spécification actuelle du livret pédagogique :
---
{current_json}
---{notes_context}
CONSIGNE D'AJUSTEMENT OU RETOUCHE :
"{request.feedback}"

Applique précisément ces modifications à la structure du livret tout en conservant l'harmonie et l'aération de l'ensemble.
Génère la réponse JSON complète avec 'spec', 'changes_summary' et 'pedagogical_note'."""

    def build(data: dict) -> IterateResponse:
        return IterateResponse(
            spec=WorkbookSpec(**data.get("spec", data)),
            changes_summary=data.get(
                "changes_summary",
                "Ajustements appliqués avec succès selon vos consignes.",
            ),
            pedagogical_note=data.get("pedagogical_note", ""),
        )

    result = _generate_json(api_key, ITERATE_SYSTEM_PROMPT, user_prompt, build, "iterate")
    if result is None:
        return GenerationResult(_build_fallback_iteration(request), "model_error")
    return GenerationResult(result)


def _build_fallback_iteration(request: IterateRequest) -> IterateResponse:
    """
    Fallback heuristic when offline or when Gemini is unreachable.
    """
    new_spec = WorkbookSpec(**request.current_spec.model_dump(exclude_unset=True))
    return IterateResponse(
        spec=new_spec,
        changes_summary="Ajustements enregistrés sur votre maquette.",
        pedagogical_note="Maquette révisée.",
    )


CUSTOMIZE_SYSTEM_PROMPT = """Tu es ingénieur pédagogique pour Marge de Manœuvre (bilans de compétences 100 % à distance, pour salariés, cadres et futurs entrepreneurs).
On te donne un document de référence (WorkbookSpec), l'un de nos carnets, et le profil d'une personne accompagnée. Tu le PERSONNALISES pour elle, selon les consignes du consultant.

RÈGLES D'OR :
1. PRÉSERVER L'OSSATURE :
   - Garde l'ordre des pages, leurs gabarits, le nombre de pages, de blocs et de questions, et la structure des clés ('params', 'blocks', 'rows', 'questions', 'items', 'lines', 'messages').
   - Une page ou un bloc qui porte "fixed": true est fixe : ne le modifie pas (il sera rétabli tel quel de toute façon).
   - Chaque page et chaque bloc porte une clé '_ref' (ex : "p3", "p3.b2") : recopie-la telle quelle sur la page ou le bloc correspondant.
2. ADAPTER À LA PERSONNE, dans les limites de la section suivante :
   - Renseigne 'beneficiary_name' avec son prénom, s'il est donné.
   - Exemples contrastés et 'example' : un métier voisin du sien, jamais le sien ni celui qu'elle vise (elle le recopierait), au nom épicène (juriste, ergonome, géomètre…), différent à chaque fois ; aucun montant, salaire ni pourcentage.
   - Les consignes, sous-titres et questions font écho à sa situation, sans s'allonger.
   - Applique les consignes du consultant, s'il en donne.
3. LONGUEURS (le PDF coupe ce qui dépasse) : titre de page 25 à 45 caractères, question 120, exemple 90 (sans préfixe « Ex : »), libellé d'une ligne de 'rating_grid' 30, borne d'échelle 20.

""" + "\n".join((PERSONALIZATION_RULES, REFERENCE_BLOCKS_RULES, TONE_RULES)) + """
FORMAT DE RÉPONSE : uniquement un objet JSON :
{
  "spec": { …le document complet, personnalisé… },
  "customizations_summary": "Les adaptations clés, en 3 à 5 points.",
  "pedagogical_note": "Un conseil pour le consultant qui animera ce document avec la personne."
}
"""


def _part_scope(spec: WorkbookSpec, part: Optional[int]) -> str:
    """Tells Gemini it only gets one part of a long workbook (nothing for a whole workbook)."""
    if not part:
        return ""
    titles = spec.parts or []
    name = f", « {titles[part - 1]} »" if part <= len(titles) else ""
    return (
        f"Ce livret est long : tu n'en reçois que la partie {part} sur {max(len(titles), part)}{name}. "
        "Personnalise ces pages seulement et renvoie-les toutes, dans le même ordre : "
        "les autres parties sont personnalisées à part."
    )


def customize_spec_with_gemini(request: CustomizeRequest) -> GenerationResult:
    """
    Personnalise un livret existant (spécification de référence) en fonction du profil
    du bénéficiaire et des consignes du consultant via Gemini Flash.
    """
    # 1. Résolution de la spécification de base
    base_spec = request.base_spec
    if not base_spec and request.template_id:
        base_spec = get_predefined_spec(request.template_id)

    if not base_spec:
        raise ValueError("Spécification de base introuvable. Veuillez sélectionner un modèle valide ou fournir une spécification.")

    api_key = os.environ.get("GEMINI_API_KEY")  # from Secret Manager in production
    if not api_key:
        logger.warning("GEMINI_API_KEY non configurée. Utilisation du fallback.")
        return GenerationResult(_build_fallback_customization(request, base_spec), "no_api_key")

    # Pages and blocks carry a '_ref', so that what is fixed comes back as it was (keep_fixed).
    # A long workbook goes part by part: Gemini then only gets the pages of one part.
    base_tagged = tag_refs(base_spec)
    sent = part_of(base_tagged, request.part) if request.part else base_tagged
    base_spec_json = json.dumps(sent, ensure_ascii=False)
    user_prompt = f"""Voici le livret pédagogique de référence (modèle existant) à personnaliser :
---
{base_spec_json}
---
{_part_scope(base_spec, request.part)}
PROFIL DU BÉNÉFICIAIRE :
- Nom / Prénom : {request.beneficiary_name}
- Contexte & Métier / Projet : {request.beneficiary_context}
- Consignes spécifiques d'adaptation du consultant : {request.custom_instructions or "Adapter harmonieusement l'ensemble des exemples et questions au profil du bénéficiaire."}

MISSION :
Personnalise ce livret de référence pour {request.beneficiary_name}.
Adapte les exemples concrets, contextualise les questions et affine les exercices pour que le livret lui parle immédiatement.
Respecte scrupuleusement la structure des gabarits et les longueurs maximales de texte.
Génère le JSON complet avec 'spec', 'customizations_summary' et 'pedagogical_note'."""

    def build(data: dict) -> CustomizeResponse:
        spec = keep_fixed(sent, data.get("spec", data))
        if request.part:
            spec = put_part_back(base_spec.model_dump(exclude_unset=True, exclude_none=True), request.part, spec)
        return CustomizeResponse(
            spec=WorkbookSpec(**spec),
            customizations_summary=data.get(
                "customizations_summary",
                f"Livret adapté avec succès pour {request.beneficiary_name} ({request.beneficiary_context}).",
            ),
            pedagogical_note=data.get("pedagogical_note", ""),
        )

    result = _generate_json(api_key, CUSTOMIZE_SYSTEM_PROMPT, user_prompt, build, "customize")
    if result is None:
        return GenerationResult(_build_fallback_customization(request, base_spec), "model_error")
    return GenerationResult(result)


def _build_fallback_customization(
    request: CustomizeRequest, base_spec: WorkbookSpec
) -> CustomizeResponse:
    """
    Personnalisation déterministe hors-ligne lorsque l'API Gemini est indisponible.
    Comme celle de Gemini, elle ne touche pas à ce qui est fixe.
    """
    spec_dict = tag_refs(base_spec)
    spec_dict["beneficiary_name"] = request.beneficiary_name

    # Contextualiser la couverture
    pages = spec_dict.get("pages", [])
    if pages and pages[0].get("template") == "cover":
        cov_params = pages[0].get("params", {})
        sub = cov_params.get("subtitle", "")
        if "pour" not in sub.lower():
            cov_params["subtitle"] = f"{sub} · Pour {request.beneficiary_name}"
        pages[0]["params"] = cov_params

    # Contextualiser l'introduction du sommaire si présente
    if len(pages) > 1 and pages[1].get("template") == "summary":
        sum_params = pages[1].get("params", {})
        old_intro = sum_params.get("intro_text", "")
        if request.beneficiary_context and "adapté" not in old_intro.lower():
            sum_params["intro_text"] = f"{old_intro} (Livret personnalisé pour {request.beneficiary_name} - {request.beneficiary_context[:60]})."
        pages[1]["params"] = sum_params

    # Injection du contexte dans un exemple de question si disponible
    for p in pages:
        if p.get("template") == "questions":
            qs = p.get("params", {}).get("questions", [])
            if qs and isinstance(qs[0], dict):
                qs[0]["example"] = f"Projet {request.beneficiary_context[:45]}..." if request.beneficiary_context else qs[0].get("example")

    new_spec = WorkbookSpec(**keep_fixed(tag_refs(base_spec), spec_dict))
    if request.part:  # as with Gemini, only the pages of the requested part change
        new_spec = WorkbookSpec(**put_part_back(
            base_spec.model_dump(exclude_unset=True, exclude_none=True), request.part,
            part_of(new_spec.model_dump(exclude_unset=True, exclude_none=True), request.part),
        ))
    summary = (
        f"Version personnalisée pour {request.beneficiary_name} générée avec succès. "
        f"Profil intégré ({request.beneficiary_context})."
    )
    pedagogical_note = f"Ce livret servira de support personnalisé pour votre travail avec {request.beneficiary_name}."

    return CustomizeResponse(
        spec=new_spec,
        customizations_summary=summary,
        pedagogical_note=pedagogical_note,
    )


