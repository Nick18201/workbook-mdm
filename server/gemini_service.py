"""
Gemini Flash Integration: Transforms raw session notes into a structured WorkbookSpec.
Uses google-genai SDK with strict Pydantic Structured Outputs.
"""

import os
import json
import logging
from functools import lru_cache
from typing import Any, Callable, NamedTuple, Optional
from google import genai
from google.genai import types

from .models import (
    WorkbookSpec,
    PageSpec,
    BlockSpec,
    ParseRequest,
    IterateRequest,
    IterateResponse,
    CustomizeRequest,
    CustomizeResponse,
)
from .predefined_workbooks import get_predefined_spec

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
                    temperature=0.2,
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


# Ton et vocabulaire de la DA (DA-workbook.md, section 7), communs aux trois prompts
TONE_RULES = """TON ET VOCABULAIRE (charte de Marge de Manœuvre, pour TOUS les textes du livret) :
- Vouvoiement. Phrases courtes, affirmatives et concrètes, tournées vers la décision et l'action.
- Lexique à privilégier : action, décision, projet, livrable, marché, faisabilité, salaire, rythme de vie, arbitrage, « validé en séance ».
- À proscrire : le registre du développement personnel (« quête de sens », « retrouver votre élan », « espace d'écoute bienveillant », « croyances limitantes », « syndrome de l'imposteur », ennéagramme, « lâcher prise », « épanouissement »).
- Le métier : jamais « coach » ni « coaching ». Dire « consultant en transformation », « la personne qui vous accompagne » ou « votre référent·e ». Jamais « cabinet » pour parler de Marge de Manœuvre.
- Tout l'accompagnement se fait à distance : jamais « présentiel ».
- N'invente aucun chiffre, témoignage ou partenariat ; aucune statistique sans source.
- Titres de page : une affirmation ponctuée, en minuscules sauf la première lettre et les noms propres (jamais de Majuscule À Chaque Mot), terminée par un point, un « ? » ou un « ! » (ex : « Votre situation actuelle. », « Mon rapport *à l'argent.* »).
- Typographie française : guillemets « », espace avant : ; ! ?, « œ » (cœur, manœuvre), « MBTI® » toujours avec ®.
"""


SYSTEM_PROMPT = """Tu es un ingénieur pédagogique et directeur artistique d'élite pour 'Marge de Manœuvre' (bilans de compétences 100 % à distance, tournés vers le passage à l'action).
Ton rôle est de transformer des notes de séance brutes ou des comptes-rendus informels en une structure de livret pédagogique PDF élégant, synthétique et percutant.

RÈGLES D'OR DE STRUCTURATION :
1. Penser en pages : Chaque page a une intention pédagogique unique (max 1 concept ou 1 exercice par page).
2. Nombre de pages selon le format souhaité :
   - 'short' (Court) : STRICTEMENT 6 à 7 pages au total.
     Couverture, Sommaire, (Météo si demandée), 2-3 exercices clés, (Engagement si demandé), Clôture.
   - 'standard' (Standard) : STRICTEMENT 7 à 10 pages au total (idéalement 8 ou 9 pages).
     Couverture, Sommaire, (Météo si demandée), 3 à 5 exercices variés (matrices, passerelles, questions, roadmap), (Engagement si demandé), Clôture.
   - 'deep' (Complet) : STRICTEMENT PLUS DE 10 PAGES (11 à 14 pages).
     Parcours d'introspection approfondi et complet : Couverture, Sommaire, (Météo si demandée), Matrice 4 piliers, Passerelle freins/leviers, Enquête exploratoire terrain, Tableau d'évaluation / Crash test, Matrice d'arbitrage de cap, Feuille de route 30-60-90j, Questions d'ancrage, (Engagement si demandé), Clôture.
3. Structure & Enchaînement des pages :
   - Page 1 : 'cover' (Couverture : numéro et titre du chapitre, et la promesse du carnet sur un post-it)
   - Page 2 : 'summary' (Sommaire fidèle des étapes du livret avec numéros et courtes descriptions)
   - Page 3 (Conditionnelle selon l'option Page Météo demandée) :
     * Si Check-in = 'none' : NE METS AUCUNE PAGE MÉTÉO NI ICE-BREAKER ! Passe immédiatement aux exercices de fond après le sommaire.
     * Si Check-in = 'classic' : Page 'meteo' standard (émotions soleil/nuageux/pluvieux/orageux, jauge d'énergie 0-10, question de recentrage).
     * Si Check-in = 'auto' : N'insère une page 'meteo' QUE si les notes de séance décrivent explicitement un état d'esprit, une fatigue ou une météo d'ouverture. Si les notes abordent directement le sujet de fond, NE METS PAS de page météo.
   - Pages intermédiaires : Exercices variés choisissant le gabarit le plus percutant selon les besoins :
     * 'questions' : Pour du questionnement guidé (1 à 3 questions maximum par page). Intitulés courts (max 120 caractères), sous-titre explicatif et exemple concret (précédé de 'Ex :').
     * 'quadrants' : Pour 4 axes, piliers de vie, SWOT ou matrice 360°.
     * 'two_columns' : Pour les passages de cap (Avant / Après, Frein / Levier, Épreuve / Compétence).
     * 'enquete' : Pour les interviews terrain, démarche réseau, exploration métier.
     * 'roadmap' : Pour les plans d'action 30·60·90 jours avec objectifs, actions et KPI.
     * 'composite' : Pour une page sur-mesure assemblant librement des blocs atomiques ('blocks') :
       - 'callout' : encadré de citation ou conseil clé (variant: 'info', 'tip', 'quote')
       - 'scale' : jauge / échelle d'évaluation de 0 à 10 avec bornes min/max
       - 'cards_grid' : grille de 2 ou 3 cartes d'analyse avec titre, sous-titre et champ de saisie
       - 'checklist' : liste de critères ou tâches à cocher (1 ou 2 colonnes)
       - 'table' : tableau structuré avec headers et cellules de saisie
       - 'stat_boxes' : rangée de 2 à 4 chiffres clés ou indicateurs phares
       - 'question' : question ouverte avec champ de saisie
   - Page avant-dernière (Conditionnelle) : 'engagement' (Fin de carnet : le livrable du carnet sur un post-it avec le tampon « Validé en séance », la date de la séance, puis 3 à 5 engagements à cocher).
     * Si include_engagement est False : Ne PAS inclure de page 'engagement'.
   - Dernière page : 'closing' (4e de couverture : la signature de Marge de Manœuvre et 2 ou 3 phrases courtes).
4. Calibrage des textes & Aération visuelle :
   - AUCUN émoji ni pictogramme (☀️, 🎯, ✅, 🟢…) dans les textes : la police du PDF ne les affiche pas.
   - Titre de page : 25 à 45 caractères maximum. Son dernier mot s'affiche en corail ; pour mettre en corail un autre groupe de mots, entoure-le d'astérisques (ex : "Mon rapport *à l'argent.*").
   - Question : max 120 caractères.
   - Exemple : max 90 caractères. Écris directement l'exemple SANS préfixe "Ex :" ou "Exemple :" (ex: "Responsable RSE en PME...").
   - Points de sommaire ('desc') : max 85 caractères par point.
   - Messages de clôture ('closing') : max 90 caractères par message.
   - RÈGLE D'OR D'ESPACEMENT & RESPIRATION (ZÉRO SURCHARGE) :
     * Sur une page 'composite', limite-toi strictement à 2 ou 3 blocs max.
     * Ne JAMAIS empiler un tableau ('table') de 3 ou 4 lignes ET une grille de cartes ('cards_grid') sur la même page ! Cela surcharge la page.
     * S'il y a un tableau d'analyse (ex: Faisabilité / Crash Test) ET des choix (ex: Plan A / Plan B), CRÉER DEUX PAGES DISTINCTES :
       - Page 1 : Tableau d'analyse (ex: Crash Test 4 Piliers) + 1 échelle d'évaluation ou 1 question.
       - Page 2 : Grille de cartes (ex: Plan A L'Étoile / Plan B Le Filet) + 1 question de passage à l'action.
   - Sois synthétique, concret et orienté passage à l'action.

5. STRUCTURE DES PARAMÈTRES PAR GABARIT (dans "params") :
   - 'cover' : {"subtitle": "Chapitre 4 : Mon rapport à l'argent", "title": "BILAN DE COMPÉTENCES", "promise": "Phrase de 3 à 8 mots sur ce que le carnet apporte (post-it)"}
   - 'summary' : {"intro_text": "Court texte d'introduction...", "points": [{"label": "01", "desc": "Titre et résumé de l'étape"}]}
   - 'meteo' : {"emotion_prompt": "Aujourd'hui, je me sens :", "energy_prompt": "Mon niveau d'énergie :", "thought_prompt": "Ce qui prend le plus de place dans ma tête :"}
   - 'quadrants' : {"instruction": "Consigne...", "quadrants": [{"title": "Professionnel", "subtitle": "Sens, Mission"}, {"title": "Personnel", "subtitle": "Santé, Équilibre"}, {"title": "Social", "subtitle": "Relations"}, {"title": "Cadre", "subtitle": "Limites, Règles"}]}
   - 'two_columns' : {"intro_text": "...", "col1_header": "Situation / Défi", "col2_header": "Enseignement / Levier", "rows": [{"label": "1. Titre ou thème", "left_tooltip": "Situation", "right_tooltip": "Enseignement"}]}
   - 'questions' : {"intro_text": "...", "questions": [{"question": "Intitulé...", "subtitle": "Précision...", "example": "Responsable RSE en PME..."}]}
   - 'enquete' : {"intro_text": "...", "questions": [{"title": "1. Besoins & Douleurs", "subtitle": "..."}, {"title": "2. Solutions & Limites", "subtitle": "..."}, {"title": "3. Recommandations", "subtitle": "..."}]}
   - 'roadmap' : {"intro_text": "...", "stages": [{"period": "PALIER 1 · 0 À 30 JOURS", "theme": "CONSOLIDER", "default_obj": "Objectif...", "actions": ["Action 1", "Action 2", "Action 3"], "default_kpi": "KPI..."}]}
   - 'engagement' : {"livrable_title": "Nom du livrable validé en séance", "livrable_text": "Une phrase qui décrit ce livrable", "lines": ["Engagement concret 1", "Engagement concret 2", "Engagement concret 3"]}
   - 'closing' : {"messages": ["Ce carnet reste le vôtre.", "Relisez vos réponses avant la prochaine séance.", "La suite se décide ensemble, en séance."]}
   - 'composite' : la liste des composants va dans "blocks" (2 blocs idéalement, max 3 petits). RÈGLE CRITIQUE : Ne JAMAIS produire un bloc vide ! Chaque bloc DOIT contenir son contenu textuel complet :
     * 'callout' : {"type": "callout", "title": "Titre du repère", "text": "Citation percutante ou conseil clé...", "variant": "info|tip|quote"}
     * 'cards_grid' : {"type": "cards_grid", "title": "Titre de la grille", "columns": 2, "cards": [{"title": "1. Atout / Constat", "subtitle": "Ce qui a suscité de l'intérêt", "placeholder": "Notes du bénéficiaire..."}, {"title": "2. Friction / Risque", "subtitle": "Ce qui a freiné ou bloqué", "placeholder": "Notes du bénéficiaire..."}]}
     * 'scale' : {"type": "scale", "label": "Niveau d'alignement ou de confiance :", "min_val": 0, "max_val": 10, "min_label": "0 · Décalage", "max_label": "10 · Confiance totale"}
     * 'table' : {"type": "table", "title": "Tableau d'évaluation", "headers": ["Pilier / Critère", "Niveau de risque", "Plan de parade ou levier"], "rows": [["Finances & Rémunération", "Modéré", "Maintien ARE, négociation"], ["Temps & Équilibre", "Faible", "Télétravail partiel"]]}
     * 'checklist' : {"type": "checklist", "title": "Critères de validation", "items": ["Premier prospect contacté", "Proposition relue à voix haute", "Date butoir fixée"]}
     * 'question' : {"type": "question", "question": "Intitulé...", "subtitle": "Précision...", "example": "Pilote de projets à impact..."}

6. FORMAT GLOBAL JSON ATTENDU :
Produis UNIQUEMENT un objet JSON valide conforme à la structure suivante :
{
  "chapter_num": 1,
  "chapter_title": "Titre du livret",
  "subtitle": "BILAN DE COMPÉTENCES & ALIGNEMENT",
  "beneficiary_name": "Nom ou prénom",
  "pages": [
    {
      "template": "cover|summary|meteo|quadrants|two_columns|questions|enquete|roadmap|engagement|closing|composite",
      "title": "Titre de la page.",
      "part_title": "1. TITRE DE LA PARTIE",
      "params": {},
      "blocks": []
    }
  ]
}

""" + TONE_RULES


def parse_notes_with_gemini(request: ParseRequest) -> GenerationResult:
    """
    Calls Gemini Flash to parse raw notes into a WorkbookSpec.
    Uses response_mime_type='application/json' for 100% compatibility with Gemini Developer API
    (avoiding additionalProperties schema rejection).
    Falls back to a smart heuristic mock if no API key is available or on failure,
    and reports it through GenerationResult.fallback_reason.
    """
    api_key = os.environ.get("GEMINI_API_KEY")  # from Secret Manager in production

    if not api_key:
        logger.warning(
            "GEMINI_API_KEY not found. Using structured heuristic mock for demonstration."
        )
        return GenerationResult(_build_fallback_spec(request), "no_api_key")

    user_prompt = f"""Voici les notes de séance à transformer en livret pédagogique :
---
Numéro de chapitre souhaité : {request.chapter_num}
Titre suggéré : {request.chapter_title or 'À déterminer selon les notes'}
Bénéficiaire : {request.beneficiary_name or 'Non spécifié'}

OPTIONS STRUCTURELLES SOUHAITÉES EN AMONT :
- Format souhaité : {request.book_format or 'standard'}
  * 'short' => Format Court : STRICTEMENT 6 à 7 pages au total.
  * 'standard' => Format Standard : STRICTEMENT 7 à 10 pages au total.
  * 'deep' => Format Complet : STRICTEMENT PLUS DE 10 PAGES (11 à 14 pages).
- Option Page Météo : {request.meteo_option or 'classic'}
  * 'none' => NE METTRE AUCUNE PAGE MÉTÉO NI ICE-BREAKER ! Démarrage direct après le sommaire.
  * 'classic' => Page météo émotionnelle et jauge d'énergie (0-10) standard.
  * 'auto' => Décider selon les notes : si les notes contiennent une météo, en mettre une, sinon ne pas en mettre.
- Inclure page de pacte d'engagement : {'Oui' if request.include_engagement else 'Non'}

NOTES BRUTES :
{request.raw_notes}
---
Génère la structure JSON complète du livret au format WorkbookSpec."""

    spec = _generate_json(
        api_key, SYSTEM_PROMPT, user_prompt, lambda data: WorkbookSpec(**data), "parse"
    )
    if spec is None:
        return GenerationResult(_build_fallback_spec(request), "model_error")
    return GenerationResult(spec)


def _build_fallback_spec(request: ParseRequest) -> WorkbookSpec:
    """
    Constructs a high-quality pedagogical fallback WorkbookSpec when offline,
    strictly respecting upfront options (meteo_option, session_focus, book_format, include_engagement).
    """
    title = (
        request.chapter_title
        or "Exploration et décisions."
    )
    ben = f" pour {request.beneficiary_name}" if request.beneficiary_name else ""

    notes_lower = request.raw_notes.lower()
    has_values = "valeur" in notes_lower or "principe" in notes_lower
    has_obstacle = (
        "frein" in notes_lower or "bloqu" in notes_lower or "peur" in notes_lower
    )

    pages: List[PageSpec] = []

    # 1. Cover
    pages.append(
        PageSpec(
            template="cover",
            title="BILAN DE COMPÉTENCES & ALIGNEMENT",
            params={
                "subtitle": f"Chapitre {request.chapter_num} : {title}",
                "title": "BILAN DE COMPÉTENCES & ALIGNEMENT",
                "promise": "De la réflexion à une décision concrète.",
            },
        )
    )

    content_pages: List[PageSpec] = []
    summary_items: List[str] = []

    # 2. Check-in / Meteo
    meteo_opt = request.meteo_option or "auto"
    should_include_meteo = False
    if meteo_opt in ("classic", "clarity", "mental_load"):
        should_include_meteo = True
    elif meteo_opt == "auto":
        should_include_meteo = any(
            k in notes_lower
            for k in ["météo", "meteo", "énergie", "energie", "fatigue", "humeur", "pression"]
        )

    if should_include_meteo:
        if meteo_opt == "clarity":
            content_pages.append(
                PageSpec(
                    template="composite",
                    title="Votre intention pour ce carnet.",
                    part_title="1. CLARIFICATION",
                    blocks=[
                        BlockSpec(
                            type="callout",
                            title="INTENTION DE SÉANCE",
                            text="Une intention claire transforme le temps de réflexion en décision concrète.",
                            variant="info",
                        ),
                        BlockSpec(
                            type="scale",
                            label="Clarté de mon cap pour cette session :",
                            min_val=0,
                            max_val=10,
                            min_label="0 · Flou",
                            max_label="10 · Vision nette",
                            field_id="sc_clarity",
                        ),
                        BlockSpec(
                            type="question",
                            question="Quelle retombée concrète attendez-vous en priorité de ce livret ?",
                            field_id="q_clarity_intent",
                            subtitle="Votre boussole directrice pour cette étape.",
                            example="Ex : Valider un scénario professionnel sans douter.",
                            box_height_cm=3.0,
                        ),
                    ],
                )
            )
            summary_items.append("Votre intention pour ce carnet")
        elif meteo_opt == "mental_load":
            content_pages.append(
                PageSpec(
                    template="composite",
                    title="Ce qui peut attendre.",
                    part_title="1. RECENTRAGE",
                    blocks=[
                        BlockSpec(
                            type="callout",
                            title="ESPACE MENTAL",
                            text="Mettre de côté ce qui encombre l'esprit libère du temps pour les décisions clés.",
                            variant="quote",
                        ),
                        BlockSpec(
                            type="scale",
                            label="Niveau de disponibilité mentale actuel :",
                            min_val=0,
                            max_val=10,
                            min_label="0 · Surchargé",
                            max_label="10 · Pleine disponibilité",
                            field_id="sc_dispo",
                        ),
                        BlockSpec(
                            type="question",
                            question="Ce que vous choisissez de mettre entre parenthèses le temps de ce livret :",
                            field_id="q_depot_charge",
                            subtitle="Ce qui peut attendre sans compromettre l'essentiel.",
                            example="Ex : Les urgences de messagerie de l'après-midi.",
                            box_height_cm=3.0,
                        ),
                    ],
                )
            )
            summary_items.append("Ce qui peut attendre")
        else:  # classic or auto
            content_pages.append(
                PageSpec(
                    template="meteo",
                    title="Votre état d'esprit du moment.",
                    part_title="1. MÉTÉO DU MOMENT",
                    params={
                        "emotion_prompt": "Aujourd'hui, je me sens :",
                        "energy_prompt": "Mon niveau d'énergie actuel :",
                        "thought_prompt": "Ce qui prend le plus de place dans mon esprit en ouvrant ce livret :",
                        "field_prefix": "meteo",
                    },
                )
            )
            summary_items.append("État d'esprit et énergie du moment")

    # 3. Core Exercises dynamically structured according to book_format:
    # - short: Court (6-7 pages total)
    # - standard / auto: Standard (7-10 pages total, e.g. 8-9 pages)
    # - deep: Complet (+ de 10 pages total, e.g. 11-12 pages)
    fmt = request.book_format or "standard"

    # Always: Quadrants & Two Columns
    content_pages.append(
        PageSpec(
            template="quadrants",
            title="Vos quatre *piliers d'équilibre.*",
            part_title=f"{len(summary_items)+1}. MATRICE D'ALIGNEMENT",
            params={
                "instruction": "Pour chacun des quatre domaines, formulez en une phrase courte votre priorité.",
                "quadrants": [
                    ("Professionnel", "Missions, impact, salaire", "p_pro"),
                    ("Personnel", "Temps pour soi, santé", "p_perso"),
                    ("Social et familial", "Relations, rythme de vie", "p_social"),
                    (
                        "Mes valeurs clés" if has_values else "Cadre et autonomie",
                        "Besoin d'autonomie",
                        "p_cadre",
                    ),
                ],
                "field_prefix": "quad",
            },
        )
    )
    summary_items.append("Vision à 360° et priorités")

    content_pages.append(
        PageSpec(
            template="two_columns",
            title="Du constat *au levier.*",
            part_title=f"{len(summary_items)+1}. ÉVOLUTION & DÉCISIONS",
            params={
                "intro_text": "Pour chaque difficulté ou situation subie, notez la décision ou le levier qui vous permet d'avancer.",
                "col1_header": "Situation subie / frein",
                "col2_header": "Décision / levier",
                "rows": [
                    (
                        "1. Ma relation au temps et aux urgences",
                        "Ce qui me débordait",
                        "La règle que je pose",
                    ),
                    (
                        "2. Poser mes limites",
                        "Où j'avais du mal à dire non",
                        "Ce que je décide de tenir",
                    ),
                    (
                        "3. Reconnaissance et légitimité",
                        "Ce que j'attendais des autres",
                        "La valeur que je m'accorde",
                    ),
                ],
                "field_prefix": "twocol",
            },
        )
    )
    summary_items.append(
        "Du constat au levier : vos freins, vos décisions"
        if has_obstacle
        else "Vos compétences et vos moteurs d'action"
    )

    # For Standard & Deep formats: add Questions and Roadmap
    if fmt in ("standard", "deep", "auto"):
        content_pages.append(
            PageSpec(
                template="questions",
                title="Pour aller *plus loin.*",
                part_title=f"{len(summary_items)+1}. EXPLORATION",
                params={
                    "intro_text": "Prenez quelques minutes pour répondre à ces questions de synthèse.",
                    "questions": [
                        {
                            "question": "1. Qu'est-ce que la dernière séance a changé dans votre façon de voir votre projet ?",
                            "field_id": "q_conscience",
                            "subtitle": "Un constat, une information ou une décision qui a fait avancer votre réflexion.",
                        },
                        {
                            "question": "2. Quel est le premier pas, même minuscule, que vous pouvez accomplir d'ici 48h ?",
                            "field_id": "q_action",
                            "example": "Ex : Envoyer un mail de clarification, bloquer une plage blanche dans mon agenda.",
                        },
                    ],
                },
            )
        )
        summary_items.append("Questions pour aller plus loin")

    # For Deep format (+ de 10 pages): add Enquete, Crash-test table, and Options Cards Grid
    if fmt == "deep":
        content_pages.append(
            PageSpec(
                template="enquete",
                title="Enquête métier *et réseau.*",
                part_title=f"{len(summary_items)+1}. EXPLORATION TERRAIN",
                params={
                    "intro_text": "Faites valider vos hypothèses par 2 ou 3 professionnels en poste pour confronter votre projet à la réalité.",
                    "questions": [
                        {"title": "1. Réalité du quotidien", "subtitle": "Les missions effectives, le rythme et les contraintes non dites"},
                        {"title": "2. Compétences clés et attentes", "subtitle": "Les compétences indispensables et les profils recherchés"},
                        {"title": "3. Recommandations et conseils", "subtitle": "Ce que mon interlocuteur ferait à ma place aujourd'hui"},
                    ],
                },
            )
        )
        summary_items.append("Enquête métier et réalité du terrain")

        content_pages.append(
            PageSpec(
                template="composite",
                title="Le test de *faisabilité.*",
                part_title=f"{len(summary_items)+1}. ÉVALUATION DES RISQUES",
                blocks=[
                    BlockSpec(
                        type="callout",
                        title="CONSEIL MÉTHODOLOGIQUE",
                        text="Un projet solide n'est pas un projet sans risque, mais un projet où chaque risque a une parade identifiée.",
                        variant="tip",
                    ),
                    BlockSpec(
                        type="table",
                        title="Les trois piliers à sécuriser",
                        headers=["Critère", "Niveau de risque", "Parade prévue"],
                        rows=[
                            ["Finances et rémunération", "Modéré", "Maintien de l'ARE, négociation salariale"],
                            ["Temps et rythme de vie", "Faible", "Télétravail partiel, horaires cadrés"],
                            ["Compétences et passerelles", "Porteur", "Valorisation de l'expérience transférable"],
                        ],
                    ),
                    BlockSpec(
                        type="scale",
                        label="Confiance globale dans la faisabilité de ce cap :",
                        min_val=0,
                        max_val=10,
                        min_label="0 · Très incertain",
                        max_label="10 · Confiance totale",
                        field_id="sc_viability",
                    ),
                ],
            )
        )
        summary_items.append("Test de faisabilité et parades")

        content_pages.append(
            PageSpec(
                template="composite",
                title="Arbitrer *entre deux scénarios.*",
                part_title=f"{len(summary_items)+1}. DÉCISION",
                blocks=[
                    BlockSpec(
                        type="cards_grid",
                        title="Comparatif des scénarios professionnels",
                        columns=2,
                        cards=[
                            {"title": "Scénario A (le projet cible)", "subtitle": "Le projet qui mobilise le plus votre motivation", "field_id": "c_opt_a"},
                            {"title": "Scénario B (le filet)", "subtitle": "L'alternative sûre et réaliste à court terme", "field_id": "c_opt_b"},
                        ],
                    ),
                    BlockSpec(
                        type="question",
                        question="Quel arbitrage décidez-vous de poser entre le scénario A et le scénario B ?",
                        field_id="q_arbitrage",
                        subtitle="La décision qui vous permet d'avancer dès aujourd'hui.",
                        example="Ex : Avancer sur le scénario A pendant 3 mois, avec le B en repli validé.",
                        box_height_cm=3.0,
                    ),
                ],
            )
        )
        summary_items.append("Arbitrage entre les scénarios A et B")

    # For Standard & Deep formats: add Roadmap
    if fmt in ("standard", "deep", "auto"):
        content_pages.append(
            PageSpec(
                template="roadmap",
                title="Votre feuille *de route.*",
                part_title=f"{len(summary_items)+1}. PLAN D'ACTION",
                params={
                    "intro_text": "Trois paliers pour passer de la décision à l'action.",
                    "stages": [
                        {
                            "period": "PALIER 1 · 0 À 30 JOURS",
                            "theme": "SÉCURISER",
                            "default_obj": "Valider le cadre d'action",
                            "actions": ["Poser le point d'étape", "Identifier 2 alliés", "Clarifier mes critères"],
                            "default_kpi": "Point calé",
                        },
                        {
                            "period": "PALIER 2 · 30 À 60 JOURS",
                            "theme": "DÉPLOYER",
                            "default_obj": "Tester sur le terrain",
                            "actions": ["Entretien réseau 1", "Entretien réseau 2", "Synthèse d'opportunités"],
                            "default_kpi": "2 retours obtenus",
                        },
                        {
                            "period": "PALIER 3 · 60 À 90 JOURS",
                            "theme": "ANCRER",
                            "default_obj": "Consolider la trajectoire",
                            "actions": ["Bilan d'étape", "Ajustement du cap", "Point avec la personne qui vous accompagne"],
                            "default_kpi": "Trajectoire sécurisée",
                        },
                    ],
                },
            )
        )
        summary_items.append("Feuille de route à 30, 60 et 90 jours")

    # 4. Engagement (Conditionnel)
    if request.include_engagement is not False:
        content_pages.append(
            PageSpec(
                template="engagement",
                title="Votre livrable.",
                part_title=f"{len(summary_items)+1}. MON ENGAGEMENT",
                params={
                    "lines": [
                        "Je réserve chaque semaine un créneau fixe à ce carnet.",
                        "Je regarde ma trajectoire avec lucidité, sans complaisance.",
                        "Je teste une piste sur le terrain avant de l'écarter.",
                        (
                            f"Ce parcours est le mien ({request.beneficiary_name}), et je décide d'en être pleinement l'acteur."
                            if request.beneficiary_name
                            else "Ce parcours est le mien, et je décide d'en être pleinement l'acteur."
                        ),
                    ]
                },
            )
        )
        summary_items.append("Votre livrable et vos engagements")

    # 5. Summary Page (Page 2) with exact numbering
    points = [(f"{i+1}.", item) for i, item in enumerate(summary_items)]
    summary_page = PageSpec(
        template="summary",
        title=title,
        params={
            "num": str(request.chapter_num),
            "intro_text": f"Ce livret personnel{ben} a été conçu pour structurer les enseignements de votre dernière séance et fixer vos prochains repères d'action.",
            "points": points,
        },
    )

    # 6. Closing Page (Dernière page)
    closing_page = PageSpec(
        template="closing",
        title="Clôture",
        params={
            "messages": [
                "Ce carnet reste le vôtre.",
                "Relisez vos réponses avant la prochaine séance.",
                "La suite se décide ensemble, en séance.",
            ]
        },
    )

    all_pages = [pages[0], summary_page] + content_pages + [closing_page]

    return WorkbookSpec(
        chapter_num=request.chapter_num,
        chapter_title=title,
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        beneficiary_name=request.beneficiary_name,
        pages=all_pages,
    )


ITERATE_SYSTEM_PROMPT = """Tu es le copilote pédagogique et directeur artistique d'élite de 'Marge de Manœuvre'.
L'utilisateur te fournit la structure actuelle d'un livret pédagogique (WorkbookSpec) ainsi qu'une consigne d'ajustement ou de retouche (feedback).

TON RÔLE :
1. Analyser précisément la demande de l'utilisateur (ex: ajouter un exercice, modifier une question, alléger des textes, changer le template d'une page, ajouter une échelle d'évaluation, etc.).
2. Appliquer les modifications demandées à la spécification du livret (WorkbookSpec) avec rigueur et intelligence pédagogique.
3. Préserver l'intégrité de toutes les autres pages et éléments qui ne sont pas concernés par la demande.
4. Respecter impérativement les règles de design system 'Marge de Manœuvre' :
   - AUCUN émoji ni pictogramme (☀️, 🎯, ✅, 🟢…) dans les textes : la police du PDF ne les affiche pas.
   - Pagination équilibrée selon le format souhaité : Court (6-7 pages), Standard (7-10 pages), Complet (+ de 10 pages).
   - Aération maximale : 2 à 3 composants maximum par page composite. Ne JAMAIS empiler un tableau de 3-4 lignes et une grille de cartes sur la même page (séparer en 2 pages si besoin).
   - Textes courts et percutants : titres 25-45 caractères max, questions 120 caractères max, exemples concrets sans préfixe de 90 caractères max, points de sommaire max 85 caractères.
   - Toujours conserver 'cover' en page 1, 'summary' en page 2, 'engagement' en avant-dernière page et 'closing' en dernière page (sauf demande explicite contraire).
   - Sur les pages composites ('composite') : ne JAMAIS créer de bloc vide ! Toujours remplir 'cards' (titre, sous-titre) pour 'cards_grid', 'headers' et 'rows' pour 'table', 'text' pour 'callout'.
   - Les textes ajoutés ou modifiés suivent le ton et le vocabulaire ci-dessous.
5. Rédiger un résumé clair, synthétique et courtois des modifications apportées (en 1 à 3 phrases percutantes en français).

STRUCTURE JSON DE RÉPONSE OBLIGATOIRE :
Tu dois impérativement répondre avec un objet JSON valide contenant exactement ces deux champs :
{
  "spec": {
    "chapter_num": 1,
    "chapter_title": "Titre du livret",
    "subtitle": "BILAN DE COMPÉTENCES & ALIGNEMENT",
    "beneficiary_name": "Nom",
    "pages": [...]
  },
  "changes_summary": "Résumé concis de ce que tu as modifié, ajouté ou supprimé suite à la consigne de l'utilisateur.",
  "pedagogical_note": "Courte justification pédagogique de ce choix."
}

""" + TONE_RULES


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

    current_json = json.dumps(
        request.current_spec.model_dump(), ensure_ascii=False, indent=2
    )

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
    new_spec = WorkbookSpec(**request.current_spec.model_dump())
    return IterateResponse(
        spec=new_spec,
        changes_summary="Ajustements enregistrés sur votre maquette.",
        pedagogical_note="Maquette révisée.",
    )


CUSTOMIZE_SYSTEM_PROMPT = """Tu es un ingénieur pédagogique et directeur artistique d'élite pour 'Marge de Manœuvre' (bilans de compétences 100 % à distance, pour salariés, cadres et futurs entrepreneurs).
Ton rôle est de prendre un livret pédagogique existant de référence (`WorkbookSpec`) et de le PERSONNALISER SUR-MESURE pour un bénéficiaire précis, selon son profil professionnel, son projet de transition et les consignes du consultant qui l'accompagne.

RÈGLES D'OR DE PERSONNALISATION :
1. PRÉSERVER L'OSSATURE PÉDAGOGIQUE ET LE DESIGN SYSTEM :
   - Conserve scrupuleusement l'ordre logique, les gabarits prévus (cover, summary, questions, meteo, quadrants, two_columns, enquete, roadmap, engagement, closing, composite) et le nombre de pages du livret modèle.
   - Ne modifie JAMAIS la structure des clés de paramètres ('params', 'blocks', 'quadrants', 'rows', 'questions', 'stages', 'lines', 'messages').
2. CONTEXTUALISER EN PROFONDEUR POUR LE BÉNÉFICIAIRE :
   - Renseigne `beneficiary_name` avec le prénom et nom du bénéficiaire.
   - Adapte les **exemples concrets** (`example` dans les questions et blocs) pour qu'ils soient directement issus ou représentatifs de son métier, secteur d'activité ou projet cible (ex: si le bénéficiaire est consultant IT voulant créer une marque de mobilier éco-conçu, donne des exemples liés à l'artisanat, au passage du salariat à l'entrepreneuriat, etc.).
   - Contextualise avec subtilité les consignes, les sous-titres et les questions pour qu'elles fassent directement écho à sa situation et à ses défis spécifiques.
   - Pour les matrices 4 quadrants, comparatifs 2 colonnes ou feuilles de route 30·60·90j, injecte des constats, leviers ou actions pertinents pour son profil.
   - Si des consignes spécifiques (`custom_instructions`) sont indiquées par le consultant, applique-les fidèlement.
3. RESPECT STRICT DES BUDGETS DE CARACTÈRES (AUCUN DÉBORDEMENT REPORTLAB) :
   - AUCUN émoji ni pictogramme (☀️, 🎯, ✅, 🟢…) dans les textes : la police du PDF ne les affiche pas.
   - Titre de page : 25 à 45 caractères max.
   - Intitulé de question : max 120 caractères.
   - Exemple concret : max 90 caractères (direct, percutant, sans préfixe 'Ex :').
   - Points de sommaire ('desc') : max 85 caractères.
   - Ne jamais surcharger une page : la respiration et les espaces blancs sont sacrés.

FORMAT DE SORTIE JSON STRICT :
Produis uniquement un objet JSON valide avec les clés suivantes :
{
  "spec": { ...WorkbookSpec complet personnalisé... },
  "customizations_summary": "Explication claire et valorisante en 3-5 points des adaptations clés apportées pour ce bénéficiaire.",
  "pedagogical_note": "Conseil méthodologique pour le consultant qui animera ce livret avec le bénéficiaire."
}

""" + TONE_RULES


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

    base_spec_json = base_spec.model_dump_json(indent=2)
    user_prompt = f"""Voici le livret pédagogique de référence (modèle existant) à personnaliser :
---
{base_spec_json}
---

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
        return CustomizeResponse(
            spec=WorkbookSpec(**data.get("spec", data)),
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
    """
    spec_dict = base_spec.model_dump()
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

    new_spec = WorkbookSpec(**spec_dict)
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


