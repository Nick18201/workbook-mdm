import pytest
from fastapi.testclient import TestClient

import server.gemini_service as gemini_service
from server.app import app


def _fake_genai_client(generate):
    class Models:
        def generate_content(self, **kwargs):
            return generate()

    class Client:
        def __init__(self, **kwargs):
            self.models = Models()

    return Client


@pytest.fixture
def client():
    return TestClient(app)


def test_parse_without_api_key_is_flagged_as_fallback(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    r = client.post("/api/parse", json={"raw_notes": "Notes de séance"})

    assert r.status_code == 200
    assert r.headers["X-MDM-Generation"] == "fallback"
    assert r.headers["X-MDM-Fallback-Reason"] == "no_api_key"


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
