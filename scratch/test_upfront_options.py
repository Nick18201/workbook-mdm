"""
Unit & Integration tests for Upfront Workbook Configuration Options (meteo_option, session_focus, book_format, include_engagement).
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from server.app import app
from server.models import ParseRequest
from server.gemini_service import _build_fallback_spec
from server.pdf_compiler import compile_workbook_from_spec

client = TestClient(app)


def test_fallback_no_meteo():
    req = ParseRequest(
        raw_notes="Plan d'action direct sans état d'âme.",
        chapter_num=7,
        chapter_title="L'Arbitrage",
        theme="indigo",
        meteo_option="none",
        include_engagement=True,
    )
    spec = _build_fallback_spec(req)
    templates = [p.template for p in spec.pages]
    print(f"Templates generated with meteo_option='none': {templates}")
    assert "meteo" not in templates, "Meteo should NOT be present when meteo_option='none'"
    assert "cover" in templates
    assert "summary" in templates
    assert "engagement" in templates
    assert "closing" in templates

    # Check summary items do not mention meteo
    summary_page = next(p for p in spec.pages if p.template == "summary")
    summary_pts = [pt[1] for pt in summary_page.params.get("points", [])]
    print(f"Summary points: {summary_pts}")
    assert not any("météo" in pt.lower() or "énergie" in pt.lower() for pt in summary_pts)

    # Compile to PDF
    pdf_bytes = compile_workbook_from_spec(spec)
    assert len(pdf_bytes) > 10000
    print("[OK] test_fallback_no_meteo passed")


def test_fallback_classic_meteo():
    req = ParseRequest(
        raw_notes="Séance d'ouverture.",
        chapter_num=1,
        theme="earth",
        meteo_option="classic",
    )
    spec = _build_fallback_spec(req)
    templates = [p.template for p in spec.pages]
    print(f"Templates with classic: {templates}")
    assert "meteo" in templates
    print("[OK] test_fallback_classic_meteo passed")


def test_fallback_clarity_checkin():
    req = ParseRequest(
        raw_notes="Focus sur les objectifs.",
        chapter_num=2,
        theme="indigo",
        meteo_option="clarity",
    )
    spec = _build_fallback_spec(req)
    templates = [p.template for p in spec.pages]
    assert "meteo" not in templates
    # Should have composite page with clarity
    clarity_page = next((p for p in spec.pages if p.title == "Boussole & Clarté d'Intention"), None)
    assert clarity_page is not None
    assert clarity_page.template == "composite"
    pdf_bytes = compile_workbook_from_spec(spec)
    assert len(pdf_bytes) > 10000
    print("[OK] test_fallback_clarity_checkin passed")


def test_fallback_mental_load_checkin():
    req = ParseRequest(
        raw_notes="Épuisement et charge mentale.",
        chapter_num=3,
        theme="indigo",
        meteo_option="mental_load",
    )
    spec = _build_fallback_spec(req)
    ml_page = next((p for p in spec.pages if p.title == "Décharge Mentale & Disponibilité"), None)
    assert ml_page is not None
    assert ml_page.template == "composite"
    pdf_bytes = compile_workbook_from_spec(spec)
    assert len(pdf_bytes) > 10000
    print("[OK] test_fallback_mental_load_checkin passed")


def test_fallback_no_engagement():
    req = ParseRequest(
        raw_notes="Atelier express sans formalisme.",
        chapter_num=5,
        theme="indigo",
        meteo_option="none",
        include_engagement=False,
    )
    spec = _build_fallback_spec(req)
    templates = [p.template for p in spec.pages]
    print(f"Templates without engagement: {templates}")
    assert "engagement" not in templates
    pdf_bytes = compile_workbook_from_spec(spec)
    assert len(pdf_bytes) > 10000
    print("[OK] test_fallback_no_engagement passed")


def test_fallback_action_focus():
    req = ParseRequest(
        raw_notes="Construire le plan de lancement.",
        chapter_num=6,
        session_focus="action",
    )
    spec = _build_fallback_spec(req)
    templates = [p.template for p in spec.pages]
    assert "roadmap" in templates
    pdf_bytes = compile_workbook_from_spec(spec)
    assert len(pdf_bytes) > 10000
    print("[OK] test_fallback_action_focus passed")


def test_api_parse_with_options():
    payload = {
        "raw_notes": "Séance de décision finale sans météo.",
        "chapter_num": 7,
        "chapter_title": "Arbitrage Stratégique",
        "theme": "indigo",
        "beneficiary_name": "Thomas",
        "meteo_option": "none",
        "session_focus": "decision",
        "book_format": "short",
        "include_engagement": False,
    }
    res = client.post("/api/parse", json=payload)
    assert res.status_code == 200
    spec = res.json()
    templates = [p["template"] for p in spec["pages"]]
    print(f"API parse response templates: {templates}")
    assert "meteo" not in templates
    assert "engagement" not in templates

    # Quick generate
    res_quick = client.post("/api/quick-generate", json=payload)
    assert res_quick.status_code == 200
    assert len(res_quick.content) > 10000
    print(f"[OK] test_api_parse_with_options produced {len(res_quick.content)} bytes PDF")


if __name__ == "__main__":
    test_fallback_no_meteo()
    test_fallback_classic_meteo()
    test_fallback_clarity_checkin()
    test_fallback_mental_load_checkin()
    test_fallback_no_engagement()
    test_fallback_action_focus()
    test_api_parse_with_options()
    print("\n[ALL UPFRONT OPTIONS TESTS PASSED SUCCESSFULLY!]")
