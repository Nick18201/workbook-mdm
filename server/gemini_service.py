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

SYSTEM_PROMPT = """Tu es un ingénieur pédagogique et directeur artistique d'élite pour 'Marge de Manœuvre' (bilans de compétences et coaching professionnel).
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
   - Page 1 : 'cover' (Couverture standard avec titre et sous-titre)
   - Page 2 : 'summary' (Sommaire fidèle des étapes du livret avec numéros et courtes descriptions)
   - Page 3 (Conditionnelle selon l'option Page Météo demandée) :
     * Si Check-in = 'none' : NE METS AUCUNE PAGE MÉTÉO NI ICE-BREAKER ! Passe immédiatement aux exercices de fond après le sommaire.
     * Si Check-in = 'classic' : Page 'meteo' standard (émotions ☀️/⛅/🌧️/⚡, jauge d'énergie 0-10, question de recentrage).
     * Si Check-in = 'auto' : N'insère une page 'meteo' QUE si les notes de séance décrivent explicitement un état d'esprit, une fatigue ou une météo d'ouverture. Si les notes abordent directement le sujet de fond, NE METS PAS de page météo.
   - Pages intermédiaires : Exercices variés choisissant le gabarit le plus percutant selon les besoins :
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
   - Page avant-dernière (Conditionnelle) : 'engagement' (Pacte moral, 4 à 6 puces affirmatives et bienveillantes + signature).
     * Si include_engagement est False : Ne PAS inclure de page 'engagement'.
   - Dernière page : 'closing' (Page finale avec messages chaleureux et logo centré).
4. Calibrage des textes & Aération visuelle :
   - Titre de page : 25 à 45 caractères maximum.
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
   - Sois synthétique, inspirant et orienté passage à l'action.

5. STRUCTURE DES PARAMÈTRES PAR GABARIT (dans "params") :
   - 'cover' : {"subtitle": "Sous-titre (ex: Chapitre 4 : ...)", "title": "BILAN DE COMPÉTENCES & ALIGNEMENT"}
   - 'summary' : {"intro_text": "Court texte d'introduction...", "points": [{"label": "01", "desc": "Titre et résumé de l'étape"}]}
   - 'meteo' : {"emotion_prompt": "Aujourd'hui, je me sens :", "energy_prompt": "Mon niveau d'énergie :", "thought_prompt": "Ce qui prend le plus de place dans ma tête :"}
   - 'quadrants' : {"instruction": "Consigne...", "quadrants": [{"title": "Professionnel", "subtitle": "Sens, Mission"}, {"title": "Personnel", "subtitle": "Santé, Équilibre"}, {"title": "Social", "subtitle": "Relations"}, {"title": "Cadre", "subtitle": "Limites, Règles"}]}
   - 'two_columns' : {"intro_text": "...", "col1_header": "Situation / Défi", "col2_header": "Enseignement / Levier", "rows": [{"label": "1. Titre ou thème", "left_tooltip": "Situation", "right_tooltip": "Enseignement"}]}
   - 'questions' : {"intro_text": "...", "questions": [{"question": "Intitulé...", "subtitle": "Précision...", "example": "Responsable RSE en PME..."}]}
   - 'enquete' : {"intro_text": "...", "questions": [{"title": "1. Besoins & Douleurs", "subtitle": "..."}, {"title": "2. Solutions & Limites", "subtitle": "..."}, {"title": "3. Recommandations", "subtitle": "..."}]}
   - 'roadmap' : {"intro_text": "...", "stages": [{"period": "PALIER 1 · 0 À 30 JOURS", "theme": "CONSOLIDER", "default_obj": "Objectif...", "actions": ["Action 1", "Action 2", "Action 3"], "default_kpi": "KPI..."}]}
   - 'engagement' : {"lines": ["Je m'engage à...", "À regarder...", "À tester...", "Ce travail est pour moi..."]}
   - 'closing' : {"messages": ["Félicitations pour ce temps pris pour vous.", "Laissez infuser ces réflexions.", "À très vite pour la prochaine étape."]}
   - 'composite' : la liste des composants va dans "blocks" (2 blocs idéalement, max 3 petits). RÈGLE CRITIQUE : Ne JAMAIS produire un bloc vide ! Chaque bloc DOIT contenir son contenu textuel complet :
     * 'callout' : {"type": "callout", "title": "Titre du repère", "text": "Citation percutante ou conseil clé...", "variant": "info|tip|quote"}
     * 'cards_grid' : {"type": "cards_grid", "title": "Titre de la grille", "columns": 2, "cards": [{"title": "1. Atout / Constat", "subtitle": "Ce qui a suscité de l'intérêt", "placeholder": "Notes du bénéficiaire..."}, {"title": "2. Friction / Risque", "subtitle": "Ce qui a freiné ou bloqué", "placeholder": "Notes du bénéficiaire..."}]}
     * 'scale' : {"type": "scale", "label": "Niveau d'alignement ou de confiance :", "min_val": 0, "max_val": 10, "min_label": "0 · Décalage", "max_label": "10 · Confiance totale"}
     * 'table' : {"type": "table", "title": "Tableau d'évaluation", "headers": ["Pilier / Critère", "Niveau de risque", "Plan de parade ou levier"], "rows": [["Finances & Rémunération", "🟡 Modéré", "Maintien ARE, négociation"], ["Temps & Équilibre", "🟢 Faible", "Télétravail partiel"]]}
     * 'checklist' : {"type": "checklist", "title": "Critères de validation", "items": ["Premier prospect contacté", "Proposition relue à voix haute", "Date butoir fixée"]}
     * 'question' : {"type": "question", "question": "Intitulé...", "subtitle": "Précision...", "example": "Pilote de projets à impact..."}

6. FORMAT GLOBAL JSON ATTENDU :
Produis UNIQUEMENT un objet JSON valide conforme à la structure suivante :
{
  "chapter_num": 1,
  "chapter_title": "Titre du livret",
  "subtitle": "BILAN DE COMPÉTENCES & ALIGNEMENT",
  "theme": "indigo",
  "beneficiary_name": "Nom ou prénom",
  "pages": [
    {
      "template": "cover|summary|meteo|quadrants|two_columns|questions|enquete|roadmap|engagement|closing|composite",
      "title": "Titre de la page",
      "part_title": "1. TITRE DE LA PARTIE",
      "params": {},
      "blocks": []
    }
  ]
}
"""


def parse_notes_with_gemini(request: ParseRequest) -> WorkbookSpec:
    """
    Calls Gemini Flash to parse raw notes into a WorkbookSpec.
    Uses response_mime_type='application/json' for 100% compatibility with Gemini Developer API
    (avoiding additionalProperties schema rejection).
    Falls back to a smart heuristic mock if no API key is available or on failure.
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

    # Priorité absolue sur Gemini 3.8 Flash avec repli sur Gemini 3.6 Flash
    models_to_try = ["gemini-3.8-flash", "gemini-3.6-flash"]
    last_err = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                    system_instruction=SYSTEM_PROMPT,
                ),
            )
            raw_text = response.text.strip() if response.text else ""
            if raw_text:
                # Strip markdown code blocks if wrapped by model
                if raw_text.startswith("```"):
                    lines = raw_text.splitlines()
                    if lines and lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    raw_text = "\n".join(lines).strip()

                data = json.loads(raw_text)
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
    Constructs a high-quality pedagogical fallback WorkbookSpec when offline,
    strictly respecting upfront options (meteo_option, session_focus, book_format, include_engagement).
    """
    title = (
        request.chapter_title
        or f"Chapitre {request.chapter_num} : Exploration & Alignement"
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
                    title="Boussole & Clarté d'Intention",
                    part_title="1. CLARIFICATION",
                    blocks=[
                        BlockSpec(
                            type="callout",
                            title="INTENTION DE SÉANCE",
                            text="Poser une intention claire transforme le temps de réflexion en levier concret d'alignement.",
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
            summary_items.append("Boussole & Clarté d'Intention")
        elif meteo_opt == "mental_load":
            content_pages.append(
                PageSpec(
                    template="composite",
                    title="Décharge Mentale & Disponibilité",
                    part_title="1. RECENTRAGE",
                    blocks=[
                        BlockSpec(
                            type="callout",
                            title="ESPACE MENTAL",
                            text="Déposer ce qui encombre l'esprit permet de consacrer 100% de son énergie aux décisions clés.",
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
            summary_items.append("Décharge Mentale & Disponibilité")
        else:  # classic or auto
            content_pages.append(
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
                )
            )
            summary_items.append("État des lieux & Énergie du moment")

    # 3. Core Exercises dynamically structured according to book_format:
    # - short: Court (6-7 pages total)
    # - standard / auto: Standard (7-10 pages total, e.g. 8-9 pages)
    # - deep: Complet (+ de 10 pages total, e.g. 11-12 pages)
    fmt = request.book_format or "standard"

    # Always: Quadrants & Two Columns
    content_pages.append(
        PageSpec(
            template="quadrants",
            title="Mes 4 Piliers d'Équilibre",
            part_title=f"{len(summary_items)+1}. MATRICE D'ALIGNEMENT",
            params={
                "instruction": "Pour chacun des 4 domaines, formulez en une phrase courte votre priorité absolue.",
                "quadrants": [
                    ("Professionnel", "Sens, Impact, Salaire", "p_pro"),
                    ("Personnel", "Temps pour soi, Santé", "p_perso"),
                    ("Social & Famille", "Relations, Équilibre", "p_social"),
                    (
                        "Mes Valeurs Clés" if has_values else "Cadre & Liberté",
                        "Besoin d'autonomie",
                        "p_cadre",
                    ),
                ],
                "field_prefix": "quad",
            },
        )
    )
    summary_items.append("Vision 360° & Priorités fondamentales")

    content_pages.append(
        PageSpec(
            template="two_columns",
            title="Passerelle : Du Constat au Levier",
            part_title=f"{len(summary_items)+1}. ÉVOLUTION & DÉCISIONS",
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
                ],
                "field_prefix": "twocol",
            },
        )
    )
    summary_items.append(
        "Passerelle : Transformer les freins en ressources"
        if has_obstacle
        else "Mes Compétences & Moteurs d'action"
    )

    # For Standard & Deep formats: add Questions and Roadmap
    if fmt in ("standard", "deep", "auto"):
        content_pages.append(
            PageSpec(
                template="questions",
                title="Questions d'Approfondissement",
                part_title=f"{len(summary_items)+1}. EXPLORATION",
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
            )
        )
        summary_items.append("Questionnement d'approfondissement")

    # For Deep format (+ de 10 pages): add Enquete, Crash-test table, and Options Cards Grid
    if fmt == "deep":
        content_pages.append(
            PageSpec(
                template="enquete",
                title="Enquête Métier & Démarche Réseau",
                part_title=f"{len(summary_items)+1}. EXPLORATION TERRAIN",
                params={
                    "intro_text": "Faites valider vos hypothèses par 2 ou 3 professionnels en poste pour confronter votre projet à la réalité.",
                    "questions": [
                        {"title": "1. Réalité du Quotidien", "subtitle": "Les missions effectives, le rythme et les contraintes non dites"},
                        {"title": "2. Compétences Clés & Attentes", "subtitle": "Les compétences indispensables et les profils recherchés"},
                        {"title": "3. Recommandations & Conseils", "subtitle": "Ce que mon interlocuteur ferait à ma place aujourd'hui"},
                    ],
                },
            )
        )
        summary_items.append("Enquête exploratoire & Réalité terrain")

        content_pages.append(
            PageSpec(
                template="composite",
                title="Le Crash Test de Viabilité",
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
                        title="Évaluation des 3 Piliers de Sécurisation",
                        headers=["Critère Analysé", "Niveau de Risque", "Plan de Parade Identifié"],
                        rows=[
                            ["Finances & Rémunération", "🟡 Modéré", "Maintien ARE, négociation salariale"],
                            ["Temps & Équilibre de vie", "🟢 Faible", "Télétravail partiel, horaires cadrés"],
                            ["Compétences & Passerelles", "🟢 Porteur", "Valorisation du transfert d'expérience"],
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
        summary_items.append("Crash Test de Viabilité & Parades")

        content_pages.append(
            PageSpec(
                template="composite",
                title="Arbitrage des Caps & Options",
                part_title=f"{len(summary_items)+1}. DÉCISION",
                blocks=[
                    BlockSpec(
                        type="cards_grid",
                        title="Comparatif des scénarios professionnels",
                        columns=2,
                        cards=[
                            {"title": "Scénario A (L'Étoile)", "subtitle": "Le projet qui mobilise 100% de ma motivation", "field_id": "c_opt_a"},
                            {"title": "Scénario B (Le Filet)", "subtitle": "L'alternative sécurisante et réaliste à court terme", "field_id": "c_opt_b"},
                        ],
                    ),
                    BlockSpec(
                        type="question",
                        question="Quel arbitrage décidez-vous de poser entre le scénario A et le scénario B ?",
                        field_id="q_arbitrage",
                        subtitle="La décision qui vous permet d'avancer sereinement dès aujourd'hui.",
                        example="Ex : Avancer sur le scénario A pendant 3 mois, avec le B en repli validé.",
                        box_height_cm=3.0,
                    ),
                ],
            )
        )
        summary_items.append("Arbitrage des Scénarios A & B")

    # For Standard & Deep formats: add Roadmap
    if fmt in ("standard", "deep", "auto"):
        content_pages.append(
            PageSpec(
                template="roadmap",
                title="Ma Feuille de Route Opérationnelle",
                part_title=f"{len(summary_items)+1}. PLAN D'ACTION",
                params={
                    "intro_text": "Voici vos 3 étapes clés pour concrétiser vos avancées dans la durée.",
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
                            "actions": ["Bilan d'étape", "Ajustement de cap", "Célébration"],
                            "default_kpi": "Trajectoire sécurisée",
                        },
                    ],
                },
            )
        )
        summary_items.append("Feuille de Route 30·60·90 jours")

    # 4. Engagement (Conditionnel)
    if request.include_engagement is not False:
        content_pages.append(
            PageSpec(
                template="engagement",
                title="Mon Pacte avec Moi-Même",
                part_title=f"{len(summary_items)+1}. MON ENGAGEMENT",
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
            )
        )
        summary_items.append("Mon Engagement & Prochaines victoires")

    # 5. Summary Page (Page 2) with exact numbering
    points = [(f"{i+1}.", item) for i, item in enumerate(summary_items)]
    summary_page = PageSpec(
        template="summary",
        title=title.upper(),
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
                "Bravo pour ce travail d'introspection.",
                "Laissez infuser ces prises de conscience.",
                "À très vite pour la suite de votre parcours.",
            ]
        },
    )

    all_pages = [pages[0], summary_page] + content_pages + [closing_page]

    return WorkbookSpec(
        chapter_num=request.chapter_num,
        chapter_title=title,
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        theme=request.theme,
        beneficiary_name=request.beneficiary_name,
        pages=all_pages,
    )


ITERATE_SYSTEM_PROMPT = """Tu es le copilote pédagogique et directeur artistique d'élite de 'Marge de Manœuvre'.
L'utilisateur te fournit la structure actuelle d'un livret pédagogique (WorkbookSpec) ainsi qu'une consigne d'ajustement ou de retouche (feedback).

TON RÔLE :
1. Analyser précisément la demande de l'utilisateur (ex: ajouter un exercice, modifier une question, alléger des textes, changer le template d'une page, ajouter une échelle d'évaluation, changer le thème en 'earth', etc.).
2. Appliquer les modifications demandées à la spécification du livret (WorkbookSpec) avec rigueur et intelligence pédagogique.
3. Préserver l'intégrité de toutes les autres pages et éléments qui ne sont pas concernés par la demande.
4. Respecter impérativement les règles de design system 'Marge de Manœuvre' :
   - Pagination équilibrée selon le format souhaité : Court (6-7 pages), Standard (7-10 pages), Complet (+ de 10 pages).
   - Aération maximale : 2 à 3 composants maximum par page composite. Ne JAMAIS empiler un tableau de 3-4 lignes et une grille de cartes sur la même page (séparer en 2 pages si besoin).
   - Textes courts et percutants : titres 25-45 caractères max, questions 120 caractères max, exemples concrets sans préfixe de 90 caractères max, points de sommaire max 85 caractères.
   - Toujours conserver 'cover' en page 1, 'summary' en page 2, 'engagement' en avant-dernière page et 'closing' en dernière page (sauf demande explicite contraire).
   - Sur les pages composites ('composite') : ne JAMAIS créer de bloc vide ! Toujours remplir 'cards' (titre, sous-titre) pour 'cards_grid', 'headers' et 'rows' pour 'table', 'text' pour 'callout'.
5. Rédiger un résumé clair, synthétique et courtois des modifications apportées (en 1 à 3 phrases percutantes en français).

STRUCTURE JSON DE RÉPONSE OBLIGATOIRE :
Tu dois impérativement répondre avec un objet JSON valide contenant exactement ces deux champs :
{
  "spec": {
    "chapter_num": 1,
    "chapter_title": "Titre du livret",
    "subtitle": "BILAN DE COMPÉTENCES & ALIGNEMENT",
    "theme": "indigo",
    "beneficiary_name": "Nom",
    "pages": [...]
  },
  "changes_summary": "Résumé concis de ce que tu as modifié, ajouté ou supprimé suite à la consigne de l'utilisateur.",
  "pedagogical_note": "Courte justification pédagogique de ce choix."
}
"""


def refine_spec_with_gemini(request: IterateRequest) -> IterateResponse:
    """
    Refines an existing WorkbookSpec based on conversational user feedback using Gemini Flash.
    Prioritizes gemini-3.8-flash with fallback to gemini-3.6-flash.
    """
    api_key = request.api_key or os.environ.get("GEMINI_API_KEY")

    if not api_key:
        logger.warning(
            "GEMINI_API_KEY not found. Using structured heuristic iteration fallback."
        )
        return _build_fallback_iteration(request)

    client = genai.Client(api_key=api_key)

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

    models_to_try = ["gemini-3.8-flash", "gemini-3.6-flash"]
    last_err = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                    system_instruction=ITERATE_SYSTEM_PROMPT,
                ),
            )
            raw_text = response.text.strip() if response.text else ""
            if raw_text:
                if raw_text.startswith("```"):
                    lines = raw_text.splitlines()
                    if lines and lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    raw_text = "\n".join(lines).strip()

                data = json.loads(raw_text)
                spec_data = data.get("spec", data)
                new_spec = WorkbookSpec(**spec_data)
                summary = data.get(
                    "changes_summary",
                    "Ajustements appliqués avec succès selon vos consignes.",
                )
                note = data.get("pedagogical_note", "")
                return IterateResponse(
                    spec=new_spec,
                    changes_summary=summary,
                    pedagogical_note=note,
                )
        except Exception as e:
            logger.warning(f"Error calling {model_name} in iteration: {e}")
            last_err = e

    logger.error(f"Iteration failed on all models: {last_err}. Using fallback.")
    return _build_fallback_iteration(request)


def _build_fallback_iteration(request: IterateRequest) -> IterateResponse:
    """
    Fallback heuristic when offline or when Gemini is unreachable.
    """
    spec_data = request.current_spec.model_dump()
    fb = request.feedback.lower()

    summary_parts = []
    if "earth" in fb:
        spec_data["theme"] = "earth"
        summary_parts.append("Thème graphique basculé sur 'Earth' (terracotta).")
    elif "indigo" in fb:
        spec_data["theme"] = "indigo"
        summary_parts.append("Thème graphique basculé sur 'Indigo'.")

    if not summary_parts:
        summary_parts.append("Ajustements enregistrés sur votre maquette.")

    new_spec = WorkbookSpec(**spec_data)
    return IterateResponse(
        spec=new_spec,
        changes_summary=" ".join(summary_parts),
        pedagogical_note="Maquette révisée.",
    )


CUSTOMIZE_SYSTEM_PROMPT = """Tu es un ingénieur pédagogique et directeur artistique d'élite pour 'Marge de Manœuvre' (bilans de compétences et coaching de cadres & entrepreneurs).
Ton rôle est de prendre un livret pédagogique existant de référence (`WorkbookSpec`) et de le PERSONNALISER SUR-MESURE pour un bénéficiaire précis, selon son profil professionnel, son projet de transition et les consignes du coach.

RÈGLES D'OR DE PERSONNALISATION :
1. PRÉSERVER L'OSSATURE PÉDAGOGIQUE ET LE DESIGN SYSTEM :
   - Conserve scrupuleusement l'ordre logique, les gabarits prévus (cover, summary, questions, meteo, quadrants, two_columns, enquete, roadmap, engagement, closing, composite) et le nombre de pages du livret modèle.
   - Ne modifie JAMAIS la structure des clés de paramètres ('params', 'blocks', 'quadrants', 'rows', 'questions', 'stages', 'lines', 'messages').
2. CONTEXTUALISER EN PROFONDEUR POUR LE BÉNÉFICIAIRE :
   - Renseigne `beneficiary_name` avec le prénom et nom du bénéficiaire.
   - Adapte les **exemples concrets** (`example` dans les questions et blocs) pour qu'ils soient directement issus ou représentatifs de son métier, secteur d'activité ou projet cible (ex: si le bénéficiaire est consultant IT voulant créer une marque de mobilier éco-conçu, donne des exemples liés à l'artisanat, au passage du salariat à l'entrepreneuriat, etc.).
   - Contextualise avec subtilité les consignes, les sous-titres et les questions pour qu'elles fassent directement écho à sa situation et à ses défis spécifiques.
   - Pour les matrices 4 quadrants, comparatifs 2 colonnes ou feuilles de route 30·60·90j, injecte des constats, leviers ou actions pertinents pour son profil.
   - Si des consignes spécifiques (`custom_instructions`) sont indiquées par le coach, applique-les fidèlement.
3. RESPECT STRICT DES BUDGETS DE CARACTÈRES (AUCUN DÉBORDEMENT REPORTLAB) :
   - Titre de page : 25 à 45 caractères max.
   - Intitulé de question : max 120 caractères.
   - Exemple concret : max 90 caractères (direct, percutant, sans préfixe 'Ex :').
   - Points de sommaire ('desc') : max 85 caractères.
   - Ne jamais surcharger une page : la respiration et les espaces blancs sont sacrés.
4. THÈME GRAPHIQUE :
   - Respecte le thème demandé ('indigo' ou 'earth').

FORMAT DE SORTIE JSON STRICT :
Produis uniquement un objet JSON valide avec les clés suivantes :
{
  "spec": { ...WorkbookSpec complet personnalisé... },
  "customizations_summary": "Explication claire et valorisante en 3-5 points des adaptations clés apportées pour ce bénéficiaire.",
  "pedagogical_note": "Conseil méthodologique pour le coach lors de l'animation de ce livret avec le bénéficiaire."
}
"""


def customize_spec_with_gemini(request: CustomizeRequest) -> CustomizeResponse:
    """
    Personnalise un livret existant (spécification de référence) en fonction du profil
    du bénéficiaire et des consignes du coach via Gemini Flash.
    """
    # 1. Résolution de la spécification de base
    base_spec = request.base_spec
    if not base_spec and request.template_id:
        base_spec = get_predefined_spec(request.template_id)

    if not base_spec:
        raise ValueError("Spécification de base introuvable. Veuillez sélectionner un modèle valide ou fournir une spécification.")

    api_key = request.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY non configurée. Utilisation du fallback.")
        return _build_fallback_customization(request, base_spec)

    client = genai.Client(api_key=api_key)

    base_spec_json = base_spec.model_dump_json(indent=2)
    user_prompt = f"""Voici le livret pédagogique de référence (modèle existant) à personnaliser :
---
{base_spec_json}
---

PROFIL DU BÉNÉFICIAIRE :
- Nom / Prénom : {request.beneficiary_name}
- Contexte & Métier / Projet : {request.beneficiary_context}
- Consignes spécifiques d'adaptation du coach : {request.custom_instructions or "Adapter harmonieusement l'ensemble des exemples et questions au profil du bénéficiaire."}
- Thème graphique souhaité : {request.theme or base_spec.theme}

MISSION :
Personnalise ce livret de référence pour {request.beneficiary_name}.
Adapte les exemples concrets, contextualise les questions et affine les exercices pour que le livret lui parle immédiatement.
Respecte scrupuleusement la structure des gabarits et les longueurs maximales de texte.
Génère le JSON complet avec 'spec', 'customizations_summary' et 'pedagogical_note'."""

    models_to_try = ["gemini-3.8-flash", "gemini-3.6-flash"]
    last_err = None

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                    system_instruction=CUSTOMIZE_SYSTEM_PROMPT,
                ),
            )
            raw_text = response.text.strip() if response.text else ""
            if raw_text:
                if raw_text.startswith("```"):
                    lines = raw_text.splitlines()
                    if lines and lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    raw_text = "\n".join(lines).strip()

                data = json.loads(raw_text)
                spec_data = data.get("spec", data)
                new_spec = WorkbookSpec(**spec_data)
                summary = data.get(
                    "customizations_summary",
                    f"Livret adapté avec succès pour {request.beneficiary_name} ({request.beneficiary_context}).",
                )
                note = data.get("pedagogical_note", "")
                return CustomizeResponse(
                    spec=new_spec,
                    customizations_summary=summary,
                    pedagogical_note=note,
                )
        except Exception as e:
            logger.warning(f"Error calling {model_name} in customize: {e}")
            last_err = e

    logger.error(f"Customize failed on all models: {last_err}. Using fallback.")
    return _build_fallback_customization(request, base_spec)


def _build_fallback_customization(
    request: CustomizeRequest, base_spec: WorkbookSpec
) -> CustomizeResponse:
    """
    Personnalisation déterministe hors-ligne lorsque l'API Gemini est indisponible.
    """
    spec_dict = base_spec.model_dump()
    spec_dict["beneficiary_name"] = request.beneficiary_name
    if request.theme:
        spec_dict["theme"] = request.theme

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
        f"Thème graphique '{new_spec.theme}' appliqué et intégration du profil ({request.beneficiary_context})."
    )
    pedagogical_note = f"Ce livret servira de support personnalisé pour votre travail avec {request.beneficiary_name}."

    return CustomizeResponse(
        spec=new_spec,
        customizations_summary=summary,
        pedagogical_note=pedagogical_note,
    )


