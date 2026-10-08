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
    spec = client.get("/api/templates/chap1").json()

    iterate = client.post("/api/iterate", json={"current_spec": spec, "feedback": "Allège la page 3"})
    customize = client.post(
        "/api/customize",
        json={"template_id": "chap1", "beneficiary_name": "Alex", "beneficiary_context": "Ingénieur"},
    )

    for r in (iterate, customize):
        assert r.status_code == 200
        assert r.headers["X-MDM-Generation"] == "fallback"


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
