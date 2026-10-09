import pymupdf
import pytest
from fastapi.testclient import TestClient

import server.app as app_module
from server.app import app
from server.models import MAX_LIST_ITEMS, MAX_NOTES_LENGTH, MAX_PAGES, PageSpec, WorkbookSpec
from workbook_generator.compiler import compile_workbook_from_spec
from workbook_generator import DocumentBuilder


@pytest.fixture
def client():
    return TestClient(app)


def _scale_page(min_val, max_val):
    return {
        "template": "composite",
        "title": "Échelle",
        "blocks": [{"type": "scale", "label": "Note", "min_val": min_val, "max_val": max_val}],
    }


def test_too_long_notes_are_rejected_with_a_readable_422(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    r = client.post("/api/parse", json={"raw_notes": "x" * (MAX_NOTES_LENGTH + 1)})

    assert r.status_code == 422
    assert r.json()["detail"].startswith("Requête invalide. Notes de séance : texte trop long")
    assert "xxxx" not in r.text  # the input is not echoed back


@pytest.mark.parametrize(
    "spec",
    [
        {"pages": [{"template": "questions", "title": "Q"}] * (MAX_PAGES + 1)},
        {"pages": [{"template": "questions", "params": {"questions": ["Q ?"] * (MAX_LIST_ITEMS + 1)}}]},
        {"pages": [{"template": "closing", "params": {"messages": ["x" * 5000]}}]},
        {"pages": [_scale_page(0, 10_000_000)]},
        {"pages": [_scale_page(10, 0)]},
        {"pages": [{"template": "composite", "blocks": [{"type": "cards_grid", "columns": 0}]}]},
    ],
    ids=["pages", "list", "text", "scale_span", "scale_reversed", "columns"],
)
def test_oversized_spec_is_rejected_before_compilation(client, spec):
    r = client.post("/api/compile", json=spec)

    assert r.status_code == 422
    assert isinstance(r.json()["detail"], str)


def test_raw_blocks_in_params_cannot_blow_up_a_scale():
    # params['blocks'] escapes BlockSpec validation: the compiler falls back to 0-10
    page = PageSpec(
        template="composite",
        title="Échelle",
        params={"blocks": [{"type": "scale", "label": "Note", "min_val": 0, "max_val": 10_000_000}]},
    )
    doc = pymupdf.open(stream=compile_workbook_from_spec(WorkbookSpec(pages=[page])), filetype="pdf")

    radios = [w for w in doc[0].widgets() if w.field_type == pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON]
    assert len(radios) == 11


@pytest.mark.parametrize(
    "endpoint, function, message",
    [
        ("/api/compile", "compile_workbook_from_spec", "La compilation du PDF a échoué"),
        ("/api/page-count", "workbook_page_count", "Le comptage des pages a échoué"),
    ],
)
def test_internal_errors_do_not_leak_exception_details(client, monkeypatch, endpoint, function, message):
    def boom(spec):
        raise RuntimeError("C:\\secret\\path token=abc")

    monkeypatch.setattr(app_module, function, boom)

    r = client.post(endpoint, json={"pages": []})

    assert r.status_code == 500
    assert "secret" not in r.text
    assert message in r.json()["detail"]


def test_customize_requires_a_known_base(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    profile = {"beneficiary_name": "Alex", "beneficiary_context": "Ingénieur"}

    unknown = client.post("/api/customize", json={"template_id": "carnet-99", **profile})
    missing = client.post("/api/customize", json={"template_id": None, **profile})

    assert unknown.status_code == 404
    assert missing.status_code == 422


def test_customize_refuses_a_part_the_workbook_lacks(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    profile = {"beneficiary_name": "Alex", "beneficiary_context": "Ingénieur"}

    no_parts = client.post("/api/customize", json={"template_id": "carnet-1", "part": 1, **profile})
    too_far = client.post("/api/customize", json={"template_id": "business-plan", "part": 7, **profile})
    out_of_bounds = client.post("/api/customize", json={"template_id": "business-plan", "part": 0, **profile})

    assert no_parts.status_code == too_far.status_code == out_of_bounds.status_code == 422
    assert "Partie 1" in no_parts.json()["detail"]


def test_no_cors_headers_for_other_origins(client):
    r = client.get("/api/templates", headers={"Origin": "https://evil.example"})
    preflight = client.options(
        "/api/compile",
        headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"},
    )

    assert "access-control-allow-origin" not in r.headers
    assert "access-control-allow-origin" not in preflight.headers


def test_document_builder_raises_instead_of_exiting(tmp_path, monkeypatch):
    target = tmp_path / "ouvert.pdf"
    target.write_bytes(b"%PDF")

    def locked(path):
        raise PermissionError("locked")

    monkeypatch.setattr("os.remove", locked)

    with pytest.raises(PermissionError, match="Cannot overwrite"):
        DocumentBuilder(str(target))
