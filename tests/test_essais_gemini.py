"""The trials of the real Gemini (essais-gemini/): their cases stay valid requests, and the script measures them, in fallback mode (no key, no call)."""

import importlib.util
import json
import logging
import types
from pathlib import Path

import pytest

import server.gemini_service as gemini_service
from workbook_generator.spec import load_workbook, tag_refs

ESSAIS = Path(__file__).resolve().parent.parent / "essais-gemini" / "essais.py"


@pytest.fixture(scope="module")
def essais():
    spec = importlib.util.spec_from_file_location("essais_gemini", ESSAIS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_case_runs_in_fallback_mode(essais, tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    cases = essais.load_cases()
    assert {"reconversion", "notes-lourdes", "creation", "evolution-interne", "carnet-7-parties",
            "retouche-feuille-de-route"} <= {case["id"] for case in cases if case["serie"] == 1}

    results = essais.run(cases, tmp_path, pdf=False)

    assert [r["cas"] for r in results] == [case["id"] for case in cases]
    assert all(r["generation"] == "fallback" and r["pages_pdf"] > 0 for r in results)
    by_case = {r["cas"]: r for r in results}
    assert by_case["carnet-7-parties"]["mesures"]["structure"] == []
    assert by_case["notes-lourdes"]["mesures"]["prenom"] == "Karim"
    assert (tmp_path / "creation-t1.json").is_file()
    assert essais.report(results, 1, None, False).startswith("# Essais en mode de secours")


def test_the_plan_calls_nothing(essais, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    calls, sent, received, thinking = essais.estimate(essais.load_cases(ids=["carnet-7-parties"])[0])
    assert calls == 2 and sent > 5000 and received > 3000 and 0 < thinking < received
    assert "GEMINI_API_KEY" not in __import__("os").environ


def test_fixed_changes_counts_what_keep_fixed_puts_back(essais):
    base = tag_refs(load_workbook("carnet-2"))
    out = json.loads(json.dumps(base))
    fixed_blocks = [(page, block) for page in out["pages"] for block in page.get("blocks") or []
                    if block["type"] in ("protocol", "anchor", "energy")]
    first, second = fixed_blocks[0], fixed_blocks[1]
    first[1]["text"] = "Un texte réécrit."
    second[0]["blocks"].remove(second[1])

    changes = essais.fixed_changes(base, out)

    assert changes["modifies"] == [first[1]["_ref"]] and changes["perdus"] == [second[1]["_ref"]]


def test_the_retouch_measure_finds_a_full_roadmap_table(essais):
    before = {"pages": [{"template": "cover", "params": {"cover_title": "Titre."}}]}
    row = lambda days: [f"À {days} jours", {"field_id": f"obj_{days}"}, {"field_id": f"res_{days}"}]
    after = {"pages": before["pages"] + [{"template": "composite", "title": "Ma feuille de route.", "blocks": [
        {"type": "table", "headers": ["Palier", "Objectif", "Résultat"], "rows": [row(30), row(60), row(90)]}]}]}

    measures = essais.measure_retouch(before, after)

    assert measures["nouveaux_tableaux"] == [{"en_tetes": ["Palier", "Objectif", "Résultat"], "lignes": 3,
                                              "paliers_30_60_90": True, "toutes_les_cases": True}]
    assert measures["pages_identiques"] == "1/1"


def test_the_depth_of_a_customization_is_measured_by_kind_of_text(essais):
    # Lot 4: a medium level rewrites the instructions and examples, a strong one also some questions
    page = {"template": "composite", "title": "Un titre de page.", "blocks": [
        {"type": "paragraphs", "items": ["Une consigne de départ."]},
        {"type": "contrast_example", "title": "Ergonome", "surface": "Ça va bien.", "exploitable": "Une réponse précise."},
        {"type": "question", "question": "Ce que je veux garder ?", "field_id": "q"},
        {"type": "protocol", "text": "Une annonce fixe."},
    ]}
    customized = json.loads(json.dumps(page))
    customized["blocks"][0]["items"] = ["Une consigne pour une personne libraire."]
    customized["blocks"][1]["exploitable"] = "Une autre réponse précise."
    customized["blocks"][3]["text"] = "Une annonce réécrite."  # fixed: not counted

    depth = essais.rewritten_by_kind({"pages": [page]}, {"pages": [customized]})

    assert depth == {"consignes": [1, 1], "exemples": [1, 2], "questions et amorces": [0, 1], "titres": [0, 1]}


def test_each_call_logs_its_tokens(monkeypatch):
    usage = types.SimpleNamespace(prompt_token_count=1200, candidates_token_count=800, thoughts_token_count=None)

    class Client:
        def __init__(self, **kwargs):
            self.models = self

        def generate_content(self, **kwargs):
            return types.SimpleNamespace(text='{"ok": true}', usage_metadata=usage)

    records = []

    class Handler(logging.Handler):
        def emit(self, record):
            records.append(record)

    monkeypatch.setattr(gemini_service.genai, "Client", Client)
    gemini_service._get_client.cache_clear()
    handler = Handler()
    monkeypatch.setattr(gemini_service.usage_logger, "level", logging.INFO)
    gemini_service.usage_logger.addHandler(handler)
    try:
        assert gemini_service._generate_json("cle-factice", "système", "notes", lambda data: data, "parse") == {"ok": True}
    finally:
        gemini_service.usage_logger.removeHandler(handler)
        gemini_service._get_client.cache_clear()

    usage_log = [r.gemini_usage for r in records if hasattr(r, "gemini_usage")]
    assert usage_log and usage_log[0]["prompt"] == 1200 and usage_log[0]["candidates"] == 800
    assert usage_log[0]["thoughts"] == 0 and usage_log[0]["label"] == "parse"
