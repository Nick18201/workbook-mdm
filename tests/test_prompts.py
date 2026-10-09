"""What Gemini is told: every prompt carries the rules of our carnets (prompt_rules.py)."""

import json

import pytest

import server.gemini_service as gemini_service
from server import prompt_rules
from server.models import CustomizeRequest, LayoutRequest, ParseRequest
from workbook_generator.conformity import check_spec
from workbook_generator.spec import WorkbookSpec

CREATE = gemini_service.SYSTEM_PROMPT
ITERATE = gemini_service.ITERATE_SYSTEM_PROMPT
CUSTOMIZE = gemini_service.CUSTOMIZE_SYSTEM_PROMPT
LAYOUT = gemini_service.LAYOUT_SYSTEM_PROMPT
PROMPTS = {"création": CREATE, "ajustement": ITERATE, "personnalisation": CUSTOMIZE, "mise en page": LAYOUT}

# The sections each prompt carries, and no other: creating needs the whole template,
# retouching the rules of an exercise and of the existing blocks, customizing what may
# change and what not; a faithful layout only the forbidden words, the boxes, the room on
# a page and the blocks (the tone, the template and the exercises would have it rewrite)
SECTIONS = {
    "TONE_RULES": ("création", "ajustement", "personnalisation"),
    "VOCABULARY_RULES": ("création", "ajustement", "personnalisation", "mise en page"),
    "TEMPLATE_RULES": ("création",),
    "EXERCISE_RULES": ("création", "ajustement"),
    "SPACE_RULES": ("création", "ajustement", "mise en page"),
    "CHARGE_RULES": ("création", "ajustement"),
    "ANSWER_RULES": ("création", "ajustement", "mise en page"),
    "BLOCKS_DOC": ("création", "ajustement", "mise en page"),
    "EXAMPLE_PAGE": ("création",),
    "REFERENCE_BLOCKS_RULES": ("ajustement", "personnalisation"),
    "PERSONALIZATION_RULES": ("personnalisation",),
    "FIDELITY_RULES": ("mise en page",),
}


@pytest.mark.parametrize("section", list(SECTIONS))
def test_each_prompt_carries_its_rules_and_no_other(section):
    text = getattr(prompt_rules, section)
    for name, prompt in PROMPTS.items():
        assert (text in prompt) is (name in SECTIONS[section]), name


@pytest.mark.parametrize("phrase", [
    "Crash", "L'Étoile", "Maintien ARE", "STRICTEMENT", "1. TITRE", "'meteo' standard", "8 blocs de base",
    # The former safety line and the paper workflow (charter of 9 October 2026)
    "trop lourd à faire hors séance", "Facultatif. Un mot suffit", "Apportez ce carnet", "à l'écran ou sur papier",
    "protocole de sécurité", "Confronter",
])
def test_the_former_recipe_is_gone(phrase):
    # The creation recipe from before the restructuration (page météo, crash test, plan A / B)
    for prompt in PROMPTS.values():
        assert phrase not in prompt


def test_the_rules_name_what_our_carnets_do():
    # A few rules, as the carnets apply them: they must reach Gemini word for word
    for rule in ("Exercice N · nom court · durée", "contrast_example", "épicène", "Ce qui m'étonne",
                 "Le droit de passer une question est dit une seule fois", "Aujourd'hui, avec le recul, je sais que…",
                 "150 caractères", "pouvoir d'agir", "ni une thérapie ni une psychanalyse", "une auto-évaluation",
                 "le renvoie complété avant la séance",
                 "jamais « présentiel »", "test des fonctionnements cognitifs",
                 "jamais une page « (suite) » qui ne porte qu'une case"):
        assert rule in CREATE
    assert "jamais un chiffre personnel" in CUSTOMIZE
    assert "ne touche jamais les questions du test" in CUSTOMIZE


def test_the_faithful_layout_keeps_the_support_and_suggests_apart():
    for rule in ("mot pour mot", "dans l'ordre du support", "N'ajoute rien", "ne fusionne pas deux questions",
                 "'suggestions'", "« Ajuster »", "jamais « présentiel »", "passé au vouvoiement",
                 "les numéros de page", "'checklist'", "'scale'", "un titre de page finit par un point"):
        assert rule in LAYOUT
    framed = gemini_service._layout_user_prompt(LayoutRequest(source_text="Une question ?"))
    bare = gemini_service._layout_user_prompt(LayoutRequest(source_text="Une question ?", frame=False, chapter_num=7))
    assert "Une question ?" in framed and "Couverture et dos : oui" in framed and "Numéro de carnet : aucun" in framed
    assert "Couverture et dos : non" in bare and "Numéro de carnet : 7" in bare


def test_the_example_page_comes_from_carnet_7():
    page = json.loads(prompt_rules.EXAMPLE_PAGE.split("\n", 1)[1])
    assert page["part_title"].startswith("Exercice 6")
    assert any(b["type"] == "contrast_example" for b in page["blocks"])


@pytest.fixture(autouse=True)
def fresh_gemini_clients():
    # Clients are cached per API key: a fake one must not outlive its test
    gemini_service._get_client.cache_clear()
    yield
    gemini_service._get_client.cache_clear()


def _gemini_answers(monkeypatch, payload):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    prompts = []

    class Response:
        text = json.dumps(payload)

    class Models:
        def generate_content(self, **kwargs):
            prompts.append(kwargs)
            return Response()

    class Client:
        def __init__(self, **kwargs):
            self.models = Models()

    monkeypatch.setattr(gemini_service.genai, "Client", Client)
    return prompts


GEMINI_DOC = {
    "chapter_title": "Mes enquêtes métiers", "carnet": 3, "pastel": "mint", "folio": "Enquêtes",
    "beneficiary_name": "Camille",
    "pages": [
        {"template": "cover", "params": {"cover_title": "Mes enquêtes *métiers.*", "number": 1}},
        {"template": "summary", "params": {"num": "1", "points": ["Exercice 1 · Préparer · 15 min"], "duration": "15 min"}},
        {"template": "composite", "title": "Préparer.", "blocks": [{"type": "question", "question": "Votre doute ?"}]},
        {"template": "closing", "params": {"messages": ["À bientôt."]}},
    ],
}


def test_a_document_without_number_nor_beneficiary(monkeypatch):
    prompts = _gemini_answers(monkeypatch, GEMINI_DOC)
    spec, reason = gemini_service.parse_notes_with_gemini(ParseRequest(raw_notes="Notes", duration_min=75))
    assert reason is None
    assert "Durée d'écriture visée : 1 h 15" in prompts[0]["contents"]
    assert "Numéro de carnet : aucun" in prompts[0]["contents"]
    assert spec.carnet is None and spec.beneficiary_name is None
    assert spec.folio == "Enquêtes" and spec.pastel == "mint"
    assert spec.pages[0].params["number"] == "" and spec.pages[1].params["num"] == ""
    assert spec.pages[2].part_title == ""  # never « 1. TITRE »


def test_a_numbered_carnet_takes_its_identity(monkeypatch):
    _gemini_answers(monkeypatch, GEMINI_DOC)
    spec, _ = gemini_service.parse_notes_with_gemini(
        ParseRequest(raw_notes="Notes", chapter_num=5, beneficiary_name="Julien"))
    assert spec.carnet == 5 and spec.chapter_num == 5 and spec.beneficiary_name == "Julien"
    assert spec.folio is None and spec.pastel is None
    assert spec.pages[0].params["number"] == 5 and spec.pages[1].params["num"] == "5"


def test_former_length_formats_become_a_writing_time():
    assert ParseRequest(raw_notes="x", book_format="deep").writing_minutes() == 120
    assert ParseRequest(raw_notes="x", book_format="auto").writing_minutes() is None
    assert ParseRequest(raw_notes="x", duration_min=30, book_format="deep").writing_minutes() == 30
    assert ParseRequest(raw_notes="x", meteo_option="mental_load").wants_energy() is True


@pytest.mark.parametrize("request_args", [
    {"raw_notes": "Quelles missions ? Quel salaire pour débuter ?"},
    {"raw_notes": "Julien parle de son épuisement et de sa peur de l'échec.", "chapter_num": 5,
     "meteo_option": "classic", "duration_min": 90},
    {"raw_notes": "Une séance sur le réseau.", "meteo_option": "none", "book_format": "short"},
])
def test_the_fallback_follows_the_common_template(request_args):
    spec = gemini_service._build_fallback_spec(ParseRequest(**request_args))
    assert check_spec(spec) == []
    assert isinstance(spec, WorkbookSpec)


def test_the_fallback_keeps_the_questions_of_the_notes_and_protects_heavy_ones():
    spec = gemini_service._build_fallback_spec(ParseRequest(
        raw_notes="- Q1 : Quelle demande allez-vous refuser ?\nIl parle de sa peur du conflit."))
    blocks = [b for p in spec.pages for b in p.blocks or []]
    asked = [q.question for b in blocks for q in b.questions or []]
    assert asked == ["Quelle demande allez-vous refuser ?"]
    assert {"protocol", "anchor"} <= {b.type for b in blocks}


# --- Customization without a beneficiary: a profile, a trade or a theme ---------------

CARNET = {"carnet": 6, "pages": [
    {"template": "cover", "params": {"cover_title": "L'*exploration.*", "subtitle": "Carnet 6"}},
    {"template": "composite", "title": "Vos pistes.", "blocks": [
        {"type": "question", "question": "Q ?", "field_id": "q", "subtitle": "À adapter."}]},
]}


def test_customization_without_a_first_name(monkeypatch):
    prompts = _gemini_answers(monkeypatch, {"spec": dict(CARNET, beneficiary_name="Inventé")})
    result, reason = gemini_service.customize_spec_with_gemini(
        CustomizeRequest(base_spec=CARNET, beneficiary_context="Le métier de libraire"))
    assert reason is None
    assert "Prénom : non précisé" in prompts[0]["contents"] and "pour ce profil" in prompts[0]["contents"]
    assert result.spec.beneficiary_name is None  # a first name the consultant did not give is dropped


def test_customization_with_a_first_name_keeps_it(monkeypatch):
    prompts = _gemini_answers(monkeypatch, {"spec": CARNET})
    result, _ = gemini_service.customize_spec_with_gemini(
        CustomizeRequest(base_spec=CARNET, beneficiary_name="Alex", beneficiary_context="Libraire"))
    assert "Prénom : Alex" in prompts[0]["contents"]
    assert result.spec.beneficiary_name == "Alex"


def test_the_fallback_customization_names_no_one(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result, reason = gemini_service.customize_spec_with_gemini(
        CustomizeRequest(template_id="carnet-1", beneficiary_context="Le métier de libraire"))
    assert reason == "no_api_key"
    assert result.spec.beneficiary_name is None
    assert "Pour" not in str(result.spec.pages[0].params) and "None" not in result.customizations_summary
