import json

import pytest
from fastapi.testclient import TestClient

import server.gemini_service as gemini_service
from server.app import app


def _fake_genai_client(generate, created=None):
    class Models:
        def generate_content(self, **kwargs):
            return generate()

    class Client:
        def __init__(self, **kwargs):
            if created is not None:
                created.append(kwargs)
            self.models = Models()

    return Client


@pytest.fixture(autouse=True)
def fresh_gemini_clients():
    # Clients are cached per API key: each test must see its own fake
    gemini_service._get_client.cache_clear()
    yield
    gemini_service._get_client.cache_clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_parse_without_api_key_is_flagged_as_fallback(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    r = client.post("/api/parse", json={"raw_notes": "Notes de séance"})

    assert r.status_code == 200
    assert r.headers["X-MDM-Generation"] == "fallback"
    assert r.headers["X-MDM-Fallback-Reason"] == "no_api_key"


def test_a_key_sent_by_the_client_is_ignored(client, monkeypatch):
    # The key only comes from the server (Secret Manager): a request cannot bring its own
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    created = []
    monkeypatch.setattr(gemini_service.genai, "Client", _fake_genai_client(lambda: None, created))

    r = client.post("/api/parse", json={"raw_notes": "Notes de séance", "api_key": "client-key"})

    assert r.status_code == 200
    assert r.headers["X-MDM-Fallback-Reason"] == "no_api_key"
    assert created == []


def test_parse_is_flagged_as_fallback_when_every_model_fails(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    def fail():
        raise RuntimeError("model not found")

    monkeypatch.setattr(gemini_service.genai, "Client", _fake_genai_client(fail))

    r = client.post("/api/parse", json={"raw_notes": "Notes de séance"})

    assert r.status_code == 200
    assert r.headers["X-MDM-Generation"] == "fallback"
    assert r.headers["X-MDM-Fallback-Reason"] == "model_error"


def test_parse_is_flagged_as_ai_when_gemini_answers(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    class Response:
        text = '```json\n{"chapter_title": "Titre IA", "pages": []}\n```'

    monkeypatch.setattr(gemini_service.genai, "Client", _fake_genai_client(Response))

    r = client.post("/api/parse", json={"raw_notes": "Notes de séance"})

    assert r.headers["X-MDM-Generation"] == "ai"
    assert "X-MDM-Fallback-Reason" not in r.headers
    assert r.json()["chapter_title"] == "Titre IA"


def test_gemini_client_is_reused_and_has_a_timeout(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    created = []

    class Response:
        text = '{"chapter_title": "Titre IA", "pages": []}'

    monkeypatch.setattr(gemini_service.genai, "Client", _fake_genai_client(Response, created))

    for _ in range(2):
        assert client.post("/api/parse", json={"raw_notes": "Notes"}).status_code == 200

    assert len(created) == 1
    assert created[0]["http_options"].timeout == gemini_service.GEMINI_TIMEOUT_S * 1000


def test_iterate_and_customize_flag_fallback(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    spec = client.get("/api/templates/carnet-1").json()

    iterate = client.post("/api/iterate", json={"current_spec": spec, "feedback": "Allège la page 3"})
    customize = client.post(
        "/api/customize",
        json={"template_id": "carnet-1", "beneficiary_name": "Alex", "beneficiary_context": "Ingénieur"},
    )

    for r in (iterate, customize):
        assert r.status_code == 200
        assert r.headers["X-MDM-Generation"] == "fallback"


def test_customize_needs_no_beneficiary(client, monkeypatch):
    # A customization may aim at a trade or a theme rather than a person
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    r = client.post("/api/customize", json={"template_id": "carnet-6", "beneficiary_context": "Le métier de libraire"})
    assert r.status_code == 200
    assert "beneficiary_name" not in r.json()["spec"]


def test_customize_never_changes_what_is_fixed(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    base = {"carnet": 3, "pages": [{"template": "composite", "title": "Sous pression.", "blocks": [
        {"type": "protocol", "text": "Avertissement."},
        {"type": "question", "question": "Q ?", "field_id": "q", "subtitle": "À adapter."},
    ]}]}
    # Gemini rewrites everything, the protocol included, and keeps the references
    answer = {"spec": {"carnet": 3, "pages": [{"template": "composite", "title": "Sous pression.", "_ref": "p1",
                                               "blocks": [
        {"type": "protocol", "text": "Autre avertissement.", "_ref": "p1.b1"},
        {"type": "question", "question": "Q ?", "field_id": "q", "subtitle": "Adapté.", "_ref": "p1.b2"},
    ]}]}}

    class Response:
        text = json.dumps(answer)

    monkeypatch.setattr(gemini_service.genai, "Client", _fake_genai_client(Response))

    r = client.post("/api/customize", json={"base_spec": base, "beneficiary_name": "Alex",
                                            "beneficiary_context": "Libraire"})
    blocks = r.json()["spec"]["pages"][0]["blocks"]

    assert r.headers["X-MDM-Generation"] == "ai"
    assert blocks[0]["text"] == "Avertissement."
    assert blocks[1]["subtitle"] == "Adapté."
    assert "_ref" not in r.text


def test_customize_keeps_the_scale_labels_the_pdf_would_cut(client, monkeypatch):
    # Gemini lengthened the lines of carnet 4's rating grid beyond what the PDF shows (essais du lot 3)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    base = {"pages": [{"template": "composite", "title": "Mon aisance.", "blocks": [
        {"type": "rating_grid", "field_prefix": "a", "items": [["Demander une augmentation", "a_1"], ["Fixer un prix", "a_2"]]},
        {"type": "scale", "label": "Mon envie", "min_label": "Pas du tout", "max_label": "Tout à fait"},
    ]}]}
    answer = {"spec": {"pages": [{"template": "composite", "title": "Mon aisance.", "_ref": "p1", "blocks": [
        {"type": "rating_grid", "field_prefix": "a", "_ref": "p1.b1",
         "items": [["Demander un maintien de salaire en formation", "a_1"], ["Chiffrer un devis", "a_2"]]},
        {"type": "scale", "label": "Mon envie", "_ref": "p1.b2", "min_label": "Pas du tout",
         "max_label": "Tout à fait prêt à me lancer"},
    ]}]}}

    class Response:
        text = json.dumps(answer)

    monkeypatch.setattr(gemini_service.genai, "Client", _fake_genai_client(Response))

    r = client.post("/api/customize", json={"base_spec": base, "beneficiary_context": "Comptable"})
    grid, scale = r.json()["spec"]["pages"][0]["blocks"]

    assert grid["items"] == [["Demander une augmentation", "a_1"], ["Chiffrer un devis", "a_2"]]
    assert scale["max_label"] == "Tout à fait"


def test_customize_one_part_leaves_the_rest_as_it_was(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    base = {"parts": ["Les fondations", "Le test"], "pages": [
        {"template": "cover", "params": {"cover_title": "Mon *livret.*"}},
        {"template": "composite", "title": "Une.", "part": 1, "blocks": [
            {"type": "question", "question": "Q1 ?", "field_id": "a", "subtitle": "Texte de la partie 1."}]},
        {"template": "composite", "title": "Deux.", "part": 2, "blocks": [
            {"type": "protocol", "text": "Avertissement."},
            {"type": "question", "question": "Q2 ?", "field_id": "b", "subtitle": "Texte de la partie 2."}]},
        {"template": "closing", "params": {}},
    ]}
    # Gemini only answers with the pages of the part, rewritten, without their 'part'
    answer = {"beneficiary_name": "Alex", "pages": [{"template": "composite", "title": "Deux, adaptée.", "_ref": "p3",
                                                     "blocks": [
        {"type": "protocol", "text": "Autre avertissement.", "_ref": "p3.b1"},
        {"type": "question", "question": "Q2 ?", "field_id": "b", "subtitle": "Adapté.", "_ref": "p3.b2"},
    ]}]}
    prompts = []

    class Response:
        text = json.dumps({"spec": answer})

    class Models:
        def generate_content(self, **kwargs):
            prompts.append(kwargs["contents"])
            return Response

    class Client:
        def __init__(self, **kwargs):
            self.models = Models()

    monkeypatch.setattr(gemini_service.genai, "Client", Client)

    r = client.post("/api/customize", json={"base_spec": base, "beneficiary_name": "Alex",
                                            "beneficiary_context": "Libraire", "part": 2})
    spec = r.json()["spec"]
    cover, one, two, closing = spec["pages"]

    assert r.headers["X-MDM-Generation"] == "ai"
    assert "Texte de la partie 2." in prompts[0] and "Texte de la partie 1." not in prompts[0]
    assert "partie 2 sur 2, « Le test »" in prompts[0]
    assert spec["parts"] == base["parts"] and spec["beneficiary_name"] == "Alex"
    assert cover == base["pages"][0] and one == base["pages"][1] and closing == base["pages"][3]
    assert two["title"] == "Deux, adaptée." and two["part"] == 2
    assert two["blocks"][0]["text"] == "Avertissement."  # fixed, even part by part
    assert two["blocks"][1]["subtitle"] == "Adapté."


def _recording_client(answer, prompts):
    class Response:
        text = json.dumps(answer)

    class Models:
        def generate_content(self, **kwargs):
            prompts.append(kwargs["contents"])
            return Response

    class Client:
        def __init__(self, **kwargs):
            self.models = Models()

    return Client


RETOUCH_BASE = {"chapter_title": "Mes *enquêtes.*", "parts": ["Avant", "Après"], "pages": [
    {"template": "cover", "params": {"cover_title": "Mes *enquêtes.*"}},
    {"template": "composite", "title": "Une.", "part": 1, "blocks": [
        {"type": "question", "question": "Q1 ?", "field_id": "a", "subtitle": "Texte de la page 2."}]},
    {"template": "composite", "title": "Deux.", "part": 2, "blocks": [
        {"type": "question", "question": "Q2 ?", "field_id": "b", "subtitle": "Texte de la page 3."}]},
    {"template": "closing", "params": {}},
]}


def test_a_retouch_of_one_page_sends_it_alone_and_puts_it_back(client, monkeypatch):
    # « Retoucher cette page » : Gemini only gets the page, may cut it in two, and the rest cannot move
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    answer = {"spec": {"chapter_title": "Autre titre", "pages": [
        {"template": "composite", "title": "Deux, début.", "blocks": [
            {"type": "question", "question": "Q2 ?", "field_id": "b", "subtitle": "Allégé."}]},
        {"template": "composite", "title": "Deux, suite.", "blocks": [
            {"type": "question", "question": "Q3 ?", "field_id": "c"}]},
    ]}, "changes_summary": "Page coupée en deux."}
    prompts = []
    monkeypatch.setattr(gemini_service.genai, "Client", _recording_client(answer, prompts))

    r = client.post("/api/iterate", json={"current_spec": RETOUCH_BASE, "feedback": "Coupe-la en deux", "pages": [3]})
    spec = r.json()["spec"]

    assert r.status_code == 200 and r.headers["X-MDM-Generation"] == "ai"
    assert "Texte de la page 3." in prompts[0] and "Texte de la page 2." not in prompts[0]
    assert "page 3 « Deux. »" in prompts[0] and "sur les 4 du document" in prompts[0]
    assert spec["chapter_title"] == "Mes *enquêtes.*"
    assert [page["template"] for page in spec["pages"]] == ["cover", "composite", "composite", "composite", "closing"]
    assert spec["pages"][1] == RETOUCH_BASE["pages"][1]
    assert [page["title"] for page in spec["pages"][2:4]] == ["Deux, début.", "Deux, suite."]
    assert spec["pages"][2]["part"] == spec["pages"][3]["part"] == 2


def test_a_retouch_of_a_whole_carnet_in_one_file_per_part_keeps_its_files(client, monkeypatch):
    # Gemini may give the whole document back without its head: its files stay its files
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    base = dict(RETOUCH_BASE, part_files=True)
    answer = {"spec": {"chapter_title": "Mes *enquêtes.*", "pages": [
        dict(page, title=page.get("title", "") + " Retouchée") for page in RETOUCH_BASE["pages"]]}}
    prompts = []
    monkeypatch.setattr(gemini_service.genai, "Client", _recording_client(answer, prompts))

    r = client.post("/api/iterate", json={"current_spec": base, "feedback": "Allège tout"})
    spec = r.json()["spec"]

    assert r.headers["X-MDM-Generation"] == "ai"
    assert "un fichier par partie" in prompts[0]
    assert spec["part_files"] is True and spec["parts"] == ["Avant", "Après"]


def test_a_retouch_of_several_pages_must_give_them_back_one_for_one(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    answer = {"spec": {"pages": [{"template": "composite", "title": "Une et deux.", "blocks": []}]}}
    monkeypatch.setattr(gemini_service.genai, "Client", _recording_client(answer, []))

    r = client.post("/api/iterate", json={"current_spec": RETOUCH_BASE, "feedback": "Fusionne", "pages": [2, 3]})

    assert r.headers["X-MDM-Generation"] == "fallback"
    assert r.headers["X-MDM-Fallback-Reason"] == "model_error"
    assert [page.get("title", "") for page in r.json()["spec"]["pages"]] == ["", "Une.", "Deux.", ""]


def test_a_retouch_refuses_a_page_outside_the_document(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    r = client.post("/api/iterate", json={"current_spec": RETOUCH_BASE, "feedback": "Allège", "pages": [2, 9]})

    assert r.status_code == 422
    assert "page 9 : le document compte 4 pages" in r.json()["detail"]
