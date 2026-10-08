import io
import json
import os

import pymupdf
import pytest
from fastapi.testclient import TestClient

from server.app import app
from server.predefined_workbooks import CATALOGUE, get_predefined_spec
from workbook_generator import forms
from workbook_generator.compiler import build_reference_workbook, compile_workbook_from_spec
from workbook_generator.spec import WORKBOOKS_DIR, BlockSpec, PageSpec, WorkbookSpec, load_workbook

WORKBOOK_IDS = sorted(name[:-5] for name in os.listdir(WORKBOOKS_DIR) if name.endswith(".json"))


def test_every_workbook_file_is_in_the_app_catalogue():
    assert WORKBOOK_IDS == sorted(entry[0] for entry in CATALOGUE)


@pytest.mark.parametrize("workbook_id", WORKBOOK_IDS)
def test_workbook_field_ids_are_unique(workbook_id, monkeypatch):
    """A repeated id would be renamed with a _2 suffix, silently: an authoring mistake."""
    reserve = forms.reserve_field_name
    repeated = []

    def checking_reserve(form, name):
        if str(name).replace(".", "_") in getattr(form, "_mdm_field_names", set()):
            repeated.append(name)
        return reserve(form, name)

    monkeypatch.setattr(forms, "reserve_field_name", checking_reserve)
    build_reference_workbook(workbook_id, io.BytesIO())
    assert repeated == []


@pytest.mark.parametrize("workbook_id", WORKBOOK_IDS)
def test_workbook_file_keeps_only_what_it_sets(workbook_id):
    """The files stay readable: no null field, nothing the spec does not set."""
    with open(os.path.join(WORKBOOKS_DIR, f"{workbook_id}.json"), encoding="utf-8") as f:
        raw = json.load(f)
    spec = load_workbook(workbook_id)
    assert spec.model_dump(exclude_unset=True)["pages"] == raw["pages"]


def test_app_compiles_a_reference_workbook_like_the_cli():
    client = TestClient(app)
    spec = client.get("/api/templates/chap2").json()
    pdf = client.post("/api/compile", json=spec)
    cli = io.BytesIO()
    build_reference_workbook("chap2", cli)

    app_doc = pymupdf.open(stream=pdf.content, filetype="pdf")
    cli_doc = pymupdf.open(stream=cli.getvalue(), filetype="pdf")
    assert pdf.status_code == 200
    assert app_doc.page_count == cli_doc.page_count
    assert [p.get_text() for p in app_doc] == [p.get_text() for p in cli_doc]


def test_customized_copy_does_not_change_the_reference():
    copy = get_predefined_spec("chap1")
    copy.pages[0].params["promise"] = "Autre promesse."
    assert get_predefined_spec("chap1").pages[0].params["promise"] != "Autre promesse."


# One block of each type, with its smallest content
BLOCKS = {
    "callout": {"text": "Repère."},
    "cards_grid": {"cards": [{"title": "Carte", "field_id": "carte"}]},
    "scale": {"label": "Niveau :"},
    "checklist": {"items": ["Case"]},
    "table": {"headers": ["A", "B"], "rows": [["1", "2"]]},
    "stat_boxes": {"stats": [{"value": "3", "label": "pistes"}]},
    "question": {"question": "Question ?", "field_id": "q"},
    "text": {"text": "Texte.", "style": "italic", "spacing_after_cm": 0.3},
    "questions_group": {"questions": [{"question": "Q1 ?", "field_id": "g1"}]},
    "heading": {"text": "Intertitre"},
    "paragraphs": {"items": ["Paragraphe.", "• Étoile"], "color": "blue"},
    "star_list": {"items": ["Un", "Deux"]},
    "annotation": {"text": "À la main."},
    "frise": {"steps": [["flag", "Départ", "Repère"], ["route", "Arrivée", "Repère"]]},
    "fields_card": {"rows": [[["Nom", "nom"], ["Date", "date", 0.85, 0.5]]], "color": "mint"},
    "numbered_lines": {"cards": [["Pistes", "piste"]], "count": 2},
    "rating_grid": {"items": [["Domaine", "note"]], "field_prefix": "grille"},
    "info_cards": {"cards": [{"title": "Profil", "text": "Texte.", "field_id": "profil"}], "check_label": "Me correspond"},
    "link_card": {"title": "Ressources", "links": [["Site", "https://example.org", "description"]]},
    "checklist_cards": {"groups": [["Groupe", ["Un", "Deux"]]], "field_prefix": "groupe"},
    "fill_in_card": {"rows": [["Moi,", ["nom_complet", None, "Prénom Nom"]]]},
    "life_line": {"items": [["Sommet", "summit"], ["Vallée", "valley"]], "headers": ["Haut", "Bas"]},
    "tree_of_life": {"items": [["1. Racines", "Votre histoire", "racines"]], "text": "Annotation."},
    "space": {"height_cm": 0.5},
    "page_break": {},
}


def test_every_block_type_compiles():
    types = set(BlockSpec.model_fields["type"].annotation.__args__)
    assert set(BLOCKS) == types
    pages = [PageSpec(template="composite", title=t, part_title="", blocks=[BlockSpec(type=t, **data)])
             for t, data in BLOCKS.items()]
    doc = pymupdf.open(stream=compile_workbook_from_spec(WorkbookSpec(pages=pages)), filetype="pdf")
    assert doc.page_count >= len(BLOCKS)
