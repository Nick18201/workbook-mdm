"""
Integration tests for FastAPI server endpoints with Composite Page support.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "service": "mdm-workbook-generator"}
    print("[OK] Health check passed")


def test_index_html():
    res = client.get("/")
    assert res.status_code == 200
    assert "Marge de Manœuvre" in res.text
    assert "composite" in res.text
    print("[OK] Index HTML served with composite support")


def test_parse_and_quick_generate():
    payload = {
        "raw_notes": "Thème : Alignement et passage à l'action. 2 questions sur les priorités.",
        "chapter_num": 3,
        "chapter_title": "Priorités & Cap",
        "theme": "indigo",
        "beneficiary_name": "Sophie",
    }
    # Test Parse
    res_parse = client.post("/api/parse", json=payload)
    assert res_parse.status_code == 200
    spec = res_parse.json()
    assert spec["chapter_num"] == 3
    assert len(spec["pages"]) >= 5
    print(f"[OK] Parse returned {len(spec['pages'])} pages")

    # Test Quick Generate
    res_quick = client.post("/api/quick-generate", json=payload)
    assert res_quick.status_code == 200
    assert res_quick.headers["content-type"] == "application/pdf"
    assert len(res_quick.content) > 10000
    print(f"[OK] Quick generate produced {len(res_quick.content)} PDF bytes")


def test_composite_compile():
    composite_spec = {
        "chapter_num": 4,
        "chapter_title": "Mes Réflexions Composites Aérées",
        "subtitle": "BILAN DE COMPÉTENCES & ALIGNEMENT",
        "theme": "indigo",
        "beneficiary_name": "Thomas",
        "pages": [
            {
                "template": "composite",
                "title": "Clarification & Diagnostic",
                "part_title": "1. REPÈRES STRATÉGIQUES",
                "blocks": [
                    {
                        "type": "callout",
                        "title": "REPÈRE CLÉ",
                        "text": "Se concentrer sur une priorité à fort levier permet de libérer son potentiel sans s'épuiser.",
                        "variant": "info",
                    },
                    {
                        "type": "cards_grid",
                        "columns": 2,
                        "card_height_cm": 5.5,
                        "cards": [
                            {"title": "Frein Actuel", "subtitle": "Ce qui vous ralentit", "field_id": "c_frein"},
                            {"title": "Levier Ressource", "subtitle": "Ce qui vous propulse", "field_id": "c_levier"},
                        ],
                    },
                ],
            },
            {
                "template": "composite",
                "title": "Validation & Prochaine Étape",
                "part_title": "2. PASSAGE À L'ACTION",
                "blocks": [
                    {
                        "type": "scale",
                        "label": "Clarté de la trajectoire :",
                        "min_val": 0,
                        "max_val": 10,
                        "min_label": "0 : Incertain",
                        "max_label": "10 : Serein",
                        "field_id": "sc_trajectoire",
                    },
                    {
                        "type": "checklist",
                        "title": "Jalons à 72h :",
                        "items": [
                            {"label": "Partager le projet à un collègue", "field_id": "chk_t_1"},
                            {"label": "Fixer le point d'étape", "field_id": "chk_t_2"},
                        ],
                    },
                    {
                        "type": "question",
                        "question": "Quelle sera la première retombée positive dès vendredi prochain ?",
                        "field_id": "q_retombee",
                        "subtitle": "Un signal concret de réussite.",
                        "example": "Ex : Sentir que j'ai repris la maîtrise de mon agenda.",
                        "box_height_cm": 3.0,
                    },
                ],
            },
        ],
    }
    res_compile = client.post("/api/compile", json=composite_spec)
    assert res_compile.status_code == 200
    assert res_compile.headers["content-type"] == "application/pdf"
    assert len(res_compile.content) > 10000
    print(f"[OK] Composite compile produced {len(res_compile.content)} PDF bytes")


if __name__ == "__main__":
    test_health()
    test_index_html()
    test_parse_and_quick_generate()
    test_composite_compile()
    print("\n[SUCCESS] All server tests passed with flying colors!")
