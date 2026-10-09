"""What Gemini is told: every prompt carries the rules of our carnets (prompt_rules.py)."""

import json

import pytest

import server.gemini_service as gemini_service
from server import prompt_rules
from server.models import ParseRequest
from workbook_generator.conformity import check_spec
from workbook_generator.spec import WorkbookSpec

CREATE = gemini_service.SYSTEM_PROMPT
ITERATE = gemini_service.ITERATE_SYSTEM_PROMPT
CUSTOMIZE = gemini_service.CUSTOMIZE_SYSTEM_PROMPT

# The sections each prompt must carry: creating needs the whole template, retouching the
# rules of an exercise and of the existing blocks, customizing what may change and what not
SECTIONS = {
    "TONE_RULES": (CREATE, ITERATE, CUSTOMIZE),
    "TEMPLATE_RULES": (CREATE,),
    "EXERCISE_RULES": (CREATE, ITERATE),
    "CHARGE_RULES": (CREATE, ITERATE),
    "ANSWER_RULES": (CREATE, ITERATE),
    "BLOCKS_DOC": (CREATE, ITERATE),
    "EXAMPLE_PAGE": (CREATE,),
    "REFERENCE_BLOCKS_RULES": (ITERATE, CUSTOMIZE),
    "PERSONALIZATION_RULES": (CUSTOMIZE,),
}


@pytest.mark.parametrize("section", list(SECTIONS))
def test_each_prompt_carries_its_rules(section):
    text = getattr(prompt_rules, section)
    for prompt in SECTIONS[section]:
        assert text in prompt


@pytest.mark.parametrize("phrase", [
    "Crash", "L'Étoile", "Maintien ARE", "STRICTEMENT", "1. TITRE", "'meteo' standard", "8 blocs de base",
])
def test_the_former_recipe_is_gone(phrase):
    # The creation recipe from before the restructuration (page météo, crash test, plan A / B)
    for prompt in (CREATE, ITERATE, CUSTOMIZE):
        assert phrase not in prompt


def test_the_rules_name_what_our_carnets_do():
    # A few rules, as the carnets apply them: they must reach Gemini word for word
    for rule in ("Exercice N · nom court · durée", "contrast_example", "épicène", "Ce qui m'étonne",
                 "trop lourd à faire hors séance", "Aujourd'hui, avec le recul, je sais que…", "150 caractères",
                 "jamais « présentiel »", "test des fonctionnements cognitifs",
                 "jamais une page « (suite) » qui ne porte qu'une case"):
        assert rule in CREATE
    assert "jamais un chiffre personnel" in CUSTOMIZE
    assert "ne touche jamais les questions du test" in CUSTOMIZE


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
