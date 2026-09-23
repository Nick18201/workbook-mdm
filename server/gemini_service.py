"""
Gemini Flash Integration: Transforms raw coaching notes into a structured WorkbookSpec.
Uses google-genai SDK with strict Pydantic Structured Outputs.
"""

import os
import json
import logging
from typing import Optional
from google import genai
from google.genai import types

from .models import WorkbookSpec, PageSpec, ParseRequest

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Tu es un ingénieur pédagogique et directeur artistique d'élite pour 'Marge de Manœuvre' (bilans de compétences et coaching professionnel).
Ton rôle est de transformer des notes de séance brutes ou des comptes-rendus informels en une structure de livret pédagogique PDF élégant, synthétique et percutant.

RÈGLES D'OR DE STRUCTURATION :
1. Penser en pages : Chaque page a une intention pédagogique unique (max 1 concept ou 1 exercice par page).
2. Nombre de pages : Produis entre 5 et 8 pages équilibrées.
3. Ordre logique obligatoire :
   - Page 1 : 'cover' (Couverture standard avec titre et sous-titre)
   - Page 2 : 'summary' (Sommaire des étapes avec numéros et courtes descriptions)
   - Page 3 : 'meteo' (Ice-breaker météo / énergie si approprié pour entamer la séance)
   - Pages 4 à N-2 : Exercices variés choisissant le gabarit le plus percutant :
     * 'questions' : Pour du questionnement guidé (1 à 3 questions maximum par page). Intitulés courts (max 120 caractères), sous-titre explicatif et exemple concret (précédé de 'Ex :').
     * 'quadrants' : Pour 4 axes, piliers de vie, SWOT ou matrice 360°.
     * 'two_columns' : Pour les passages de cap (Avant / Après, Croyance limitante / Croyance ressource, Épreuve / Compétence).
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
   - Page N-1 : 'engagement' (Pacte moral, 4 à 6 puces affirmatives et bienveillantes + signature).
   - Page N : 'closing' (Page finale avec messages chaleureux et logo centré).
4. Calibrage des textes :
   - Titre de page : 25 à 45 caractères maximum.
   - Question : max 120 caractères.
   - Exemple : max 100 caractères.
   - Sur une page 'composite', limite-toi à 2 ou 3 blocs bien calibrés pour respecter la hauteur A4 sans débordement.
   - Sois synthétique, inspirant et orienté passage à l'action.
"""


def parse_notes_with_gemini(request: ParseRequest) -> WorkbookSpec:
    """
    Calls Gemini Flash to parse raw notes into a WorkbookSpec using Structured Outputs.
    Falls back to a smart heuristic mock if no API key is available.
    """
    api_key = request.api_key or os.environ.get("GEMINI_API_KEY")

    if not api_key:
        logger.warning(
            "GEMINI_API_KEY not found. Using structured heuristic mock for demonstration."
        )
        return _build_fallback_spec(request)

    client = genai.Client(api_key=api_key)

    user_prompt = f"""Voici les notes de séance à transformer en livret pédagogique :
---
Numéro de chapitre souhaité : {request.chapter_num}
Titre suggéré : {request.chapter_title or 'À déterminer selon les notes'}
Thème graphique : {request.theme}
Bénéficiaire : {request.beneficiary_name or 'Non spécifié'}

NOTES BRUTES :
{request.raw_notes}
---
Génère la structure complète du livret au format WorkbookSpec."""

    # We try gemini-2.5-flash or gemini-2.0-flash
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash"]
    last_err = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=WorkbookSpec,
                    temperature=0.2,
                    system_instruction=SYSTEM_PROMPT,
                ),
            )
            # When response_schema is provided, google-genai sets response.parsed
            if hasattr(response, "parsed") and response.parsed:
                parsed_data = response.parsed
                if isinstance(parsed_data, WorkbookSpec):
                    return parsed_data
                elif isinstance(parsed_data, dict):
                    return WorkbookSpec(**parsed_data)

            # Fallback if parsed as raw JSON string in response.text
            if response.text:
                data = json.loads(response.text)
                return WorkbookSpec(**data)
        except Exception as e:
            logger.warning(f"Error calling {model_name}: {e}")
            last_err = e

    logger.error(
        f"All Gemini models failed: {last_err}. Falling back to smart heuristic."
    )
    return _build_fallback_spec(request)


def _build_fallback_spec(request: ParseRequest) -> WorkbookSpec:
    """
    Constructs a high-quality pedagogical fallback WorkbookSpec when offline.
    """
    title = (
        request.chapter_title
        or f"Chapitre {request.chapter_num} : Exploration & Alignement"
    )
    ben = f" pour {request.beneficiary_name}" if request.beneficiary_name else ""

    # Simple keyword detection from notes
    notes_lower = request.raw_notes.lower()
    has_values = "valeur" in notes_lower or "principe" in notes_lower
    has_obstacle = (
        "frein" in notes_lower or "bloqu" in notes_lower or "peur" in notes_lower
    )

    pages = [
        # 1. Cover
        PageSpec(
            template="cover",
            title="BILAN DE COMPÉTENCES & ALIGNEMENT",
            params={
                "subtitle": f"Chapitre {request.chapter_num} : {title}",
                "title": "BILAN DE COMPÉTENCES & ALIGNEMENT",
            },
        ),
        # 2. Summary
        PageSpec(
            template="summary",
            title=title.upper(),
            params={
                "num": str(request.chapter_num),
                "intro_text": f"Ce livret personnel{ben} a été conçu pour structurer les enseignements de votre dernière séance et fixer vos prochains repères d'action.",
                "points": [
                    ("1.", "État des lieux & Énergie du moment"),
                    ("2.", "Vision 360° & Priorités fondamentales"),
                    (
                        "3.",
                        (
                            "Passerelle : Transformer les freins en ressources"
                            if has_obstacle
                            else "Mes Compétences & Moteurs d'action"
                        ),
                    ),
                    ("4.", "Questionnement d'approfondissement"),
                    ("5.", "Mon Engagement & Prochaines victoires"),
                ],
            },
        ),
        # 3. Meteo
        PageSpec(
            template="meteo",
            title="Ma Météo Intérieure & Énergie",
            part_title="1. MÉTÉO DU MOMENT",
            params={
                "emotion_prompt": "Aujourd'hui, je me sens :",
                "energy_prompt": "Mon niveau d'énergie actuel :",
                "thought_prompt": "Ce qui prend le plus de place dans mon esprit en ouvrant ce livret :",
                "field_prefix": "meteo",
            },
        ),
        # 4. Quadrants
        PageSpec(
            template="quadrants",
            title="Mes 4 Piliers d'Équilibre",
            part_title="2. MATRICE D'ALIGNEMENT",
            params={
                "instruction": "Pour chacun des 4 domaines, formulez en une phrase courte votre priorité absolue.",
                "quadrants": [
                    ("Professionnel", "Sens, Impact, Salaire", "p_pro"),
                    ("Personnel", "Temps pour soi, Santé", "p_perso"),
                    ("Social & Famille", "Relations, Équilibre", "p_social"),
                    (
                        (
                            "Mes Valeurs Clés"
                            if has_values
                            else "Cadre & Liberté"
                        ),
                        "Besoin d'autonomie",
                        "p_cadre",
                    ),
                ],
                "field_prefix": "quad",
            },
        ),
        # 5. Two Columns
        PageSpec(
            template="two_columns",
            title="Passerelle : Du Constat au Levier",
            part_title="3. ÉVOLUTION & DÉCISIONS",
            params={
                "intro_text": "Transformez chaque difficulté ou situation subie en apprentissage concret et levier d'émancipation.",
                "col1_header": "Situation Subie / Frein",
                "col2_header": "Décision / Levier Ressource",
                "rows": [
                    (
                        "1. Ma relation au temps et aux urgences",
                        "Ce qui me débordait",
                        "La règle que je pose",
                    ),
                    (
                        "2. Poser mes limites avec assertivité",
                        "Où j'avais du mal à dire non",
                        "Ce que je choisis d'honorer",
                    ),
                    (
                        "3. Reconnaissance et légitimité",
                        "Ce que j'attendais des autres",
                        "La valeur que je m'accorde",
                    ),
                    (
                        "4. Mon cap pour les semaines à venir",
                        "Ce que je quitte",
                        "Ce vers quoi j'avance",
                    ),
                ],
                "field_prefix": "twocol",
            },
        ),
        # 6. Questions
        PageSpec(
            template="questions",
            title="Questions d'Approfondissement",
            part_title="4. EXPLORATION",
            params={
                "intro_text": "Prenez quelques minutes au calme pour répondre avec honnêteté à ces questions de synthèse.",
                "questions": [
                    {
                        "question": "1. Quelle a été la prise de conscience la plus forte de notre dernier échange ?",
                        "field_id": "q_conscience",
                        "subtitle": "Le moment où quelque chose a cliqué ou changé de perspective pour vous.",
                    },
                    {
                        "question": "2. Quel est le premier pas, même minuscule, que vous pouvez accomplir d'ici 48h ?",
                        "field_id": "q_action",
                        "example": "Ex : Envoyer un mail de clarification, bloquer une plage blanche dans mon agenda.",
                    },
                ],
            },
        ),
        # 7. Engagement
        PageSpec(
            template="engagement",
            title="Mon Pacte avec Moi-Même",
            part_title="5. MON ENGAGEMENT",
            params={
                "lines": [
                    "Je m'engage à accorder à cette démarche toute l'attention qu'elle mérite.",
                    "À regarder ma trajectoire avec lucidité, bienveillance et sans complaisance.",
                    "À tester de nouvelles approches avant de décréter leur impossibilité.",
                    (
                        f"Ce parcours est le mien ({request.beneficiary_name}), et je décide d'en être pleinement l'acteur."
                        if request.beneficiary_name
                        else "Ce parcours est le mien, et je décide d'en être pleinement l'acteur."
                    ),
                ]
            },
        ),
        # 8. Closing
        PageSpec(
            template="closing",
            title="Clôture",
            params={
                "messages": [
                    "Bravo pour ce travail d'introspection.",
                    "Laissez infuser ces prises de conscience.",
                    "À très vite pour la suite de votre parcours.",
                ]
            },
        ),
    ]

    return WorkbookSpec(
        chapter_num=request.chapter_num,
        chapter_title=title,
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        theme=request.theme,
        beneficiary_name=request.beneficiary_name,
        pages=pages,
    )
