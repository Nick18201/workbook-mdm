import functools
import io
import json
import os
import re

import pymupdf
import pytest
from fastapi.testclient import TestClient

from server.app import app
from server.predefined_workbooks import CATALOGUE, get_predefined_spec
from workbook_generator import components, forms
from workbook_generator import spec as spec_module
from workbook_generator.compiler import (
    build_reference_workbook,
    compile_workbook_from_spec,
    reference_data_locations,
    reference_page_count,
)
from workbook_generator.spec import (
    ANSWERS,
    WORKBOOKS_DIR,
    BlockSpec,
    PageSpec,
    WorkbookSpec,
    data_carnet,
    load_workbook,
    part_document,
    part_numbers,
    part_title,
)

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
    spec = client.get("/api/templates/carnet-2").json()
    pdf = client.post("/api/compile", json=spec)
    cli = io.BytesIO()
    build_reference_workbook("carnet-2", cli)

    app_doc = pymupdf.open(stream=pdf.content, filetype="pdf")
    cli_doc = pymupdf.open(stream=cli.getvalue(), filetype="pdf")
    assert pdf.status_code == 200
    assert app_doc.page_count == cli_doc.page_count
    assert [p.get_text() for p in app_doc] == [p.get_text() for p in cli_doc]


def test_app_shows_the_page_count_of_the_pdf():
    """The catalogue counts the PDF's pages, its « (suite) » pages included, not the file's."""
    info = next(t for t in TestClient(app).get("/api/templates").json() if t["id"] == "carnet-7")
    cli = io.BytesIO()
    build_reference_workbook("carnet-7", cli)

    assert info["page_count"] == pymupdf.open(stream=cli.getvalue(), filetype="pdf").page_count
    assert info["page_count"] > len(load_workbook("carnet-7").pages)  # carnet 7 has « (suite) » pages


def test_app_shows_the_page_count_of_the_pdf_of_its_spec():
    """The preview's badge, for a spec generated, customized, adjusted or imported: the PDF's pages."""
    client = TestClient(app)
    spec = client.get("/api/templates/carnet-7").json()  # as the UI holds it after a customization
    pdf = client.post("/api/compile", json=spec)

    r = client.post("/api/page-count", json=spec)

    assert r.status_code == 200
    assert r.json() == {"page_count": pymupdf.open(stream=pdf.content, filetype="pdf").page_count}
    assert r.json()["page_count"] > len(spec["pages"])  # carnet 7 has « (suite) » pages


def test_page_count_is_counted_again_when_the_file_changes(tmp_path, monkeypatch):
    monkeypatch.setattr(spec_module, "WORKBOOKS_DIR", str(tmp_path))
    path = tmp_path / "essai.json"

    def write(pages):
        page = {"template": "composite", "title": "Une page.", "part_title": "",
                "blocks": [{"type": "question", "question": "Une question ?", "field_id": "q"}]}
        path.write_text(json.dumps({"pages": [page] * pages}), encoding="utf-8")
        os.utime(path, (pages, pages))  # a new date, as an edit gives

    write(1)
    assert reference_page_count("essai") == 1
    write(2)
    assert reference_page_count("essai") == 2


def test_parts_are_named_and_hold_consecutive_pages():
    """A part is customized alone and put back where it was: its pages follow one another."""
    for workbook_id, raw in _raw_workbooks():
        pages_of_part = {}
        for i, page in enumerate(raw["pages"]):
            if "part" in page:
                pages_of_part.setdefault(page["part"], []).append(i)
        assert sorted(pages_of_part) == list(range(1, len(raw.get("parts", [])) + 1)), workbook_id
        for part, indexes in pages_of_part.items():
            assert indexes == list(range(indexes[0], indexes[-1] + 1)), (workbook_id, part)


# Gemini answers about 4 s per 1,000 characters of the spec it customizes (lot 3: the module
# création, 28,000 characters in one call, took 111 s): a longer workbook goes part by part
MAX_CHARS_PER_CALL = 24_000


def test_a_long_workbook_is_customized_part_by_part():
    for workbook_id, raw in _raw_workbooks():
        size = len(json.dumps(raw, ensure_ascii=False, separators=(",", ":")))
        if size <= MAX_CHARS_PER_CALL:
            continue
        assert raw.get("parts"), (workbook_id, size)
        for part in range(1, len(raw["parts"]) + 1):
            pages = [page for page in raw["pages"] if page.get("part") == part]
            assert len(json.dumps(pages, ensure_ascii=False, separators=(",", ":"))) <= MAX_CHARS_PER_CALL, (workbook_id, part)


def test_business_plan_is_customized_part_by_part(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    client = TestClient(app)
    info = next(t for t in client.get("/api/templates").json() if t["id"] == "business-plan")
    reference = client.get("/api/templates/business-plan").json()

    r = client.post("/api/customize", json={"template_id": "business-plan", "part": 4,
                                            "beneficiary_name": "Alex", "beneficiary_context": "Fleuriste"})

    assert len(info["parts"]) == 6
    assert r.status_code == 200
    assert r.json()["spec"]["pages"] == reference["pages"]  # the fallback adapts nothing in a part
    assert r.json()["spec"]["beneficiary_name"] == "Alex"


def test_customized_copy_does_not_change_the_reference():
    copy = get_predefined_spec("carnet-1")
    copy.pages[0].params["promise"] = "Autre promesse."
    assert get_predefined_spec("carnet-1").pages[0].params["promise"] != "Autre promesse."


# One block of each type, with its smallest content
BLOCKS = {
    "callout": {"text": "Repère."},
    "cards_grid": {"cards": [{"title": "Carte", "field_id": "carte"}]},
    "scale": {"label": "Niveau :"},
    "checklist": {"items": ["Case"]},
    "table": {"headers": ["A", "B"], "rows": [["1", "2"]]},
    "stat_boxes": {"stats": [{"value": "3", "label": "pistes"}]},
    "question": {"question": "Question ?", "field_id": "q", "answer": "paragraph"},
    "text": {"text": "Texte.", "style": "italic", "spacing_after_cm": 0.3},
    "questions_group": {"questions": [{"question": "Q1 ?", "field_id": "g1"}]},
    "heading": {"text": "Intertitre"},
    "paragraphs": {"items": ["Paragraphe.", "• Étoile"], "color": "blue"},
    "star_list": {"items": ["Un", "Deux"]},
    "annotation": {"text": "À la main."},
    "frise": {"steps": [["flag", "Départ", "Repère"], ["route", "Arrivée", "Repère"]]},
    "fields_card": {"rows": [[["Nom", "nom"], ["Date", "date", 0.85, 0.5]], [["Pourquoi", "pourquoi", "sentence"]]],
                    "color": "mint"},
    "numbered_lines": {"cards": [["Pistes", "piste"], ["Les suivantes", "piste", "", 3]], "count": 2},
    "rating_grid": {"items": [["Domaine", "note"]], "field_prefix": "grille"},
    "info_cards": {"cards": [{"title": "Profil", "text": "Texte.", "field_id": "profil"}], "check_label": "Me correspond"},
    "link_card": {"title": "Ressources", "links": [["Site", "https://example.org", "description"]]},
    "checklist_cards": {"groups": [["Groupe", ["Un", "Deux"]]], "field_prefix": "groupe"},
    "fill_in_card": {"rows": [["Moi,", ["nom_complet", None, "Prénom Nom"]]]},
    "life_line": {"items": [["Sommet", "summit"], ["Vallée", "valley"]], "headers": ["Haut", "Bas"]},
    "tree_of_life": {"items": [["1. Racines", "Votre histoire", "racines"]], "text": "Annotation."},
    "protocol": {},
    "anchor": {"field_id": "ancrage"},
    "contrast_example": {"title": "Chef de rayon", "surface": "J'aime le contact.", "exploitable": "Je fidélise."},
    "energy": {"field_prefix": "meteo"},
    "report": {"items": [["Vos quatre seuils", "c4.seuils", "report_seuils", "sentence"],
                         ["Votre zone à risque", "c2.zones", "report_zone"]], "columns": 2},
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


def test_numbered_lines_run_one_list_over_two_cards():
    """A card may give its first number: ten ranked lines, 01 to 05 then 06 to 10."""
    block = BlockSpec(type="numbered_lines", count=5,
                      cards=[["Les cinq premières", "rang"], ["Les cinq suivantes", "rang", "", 6]])
    pages = [PageSpec(template="composite", title="Classer", part_title="", blocks=[block])]
    page = pymupdf.open(stream=compile_workbook_from_spec(WorkbookSpec(pages=pages)), filetype="pdf")[0]
    assert sorted(w.field_name for w in page.widgets()) == sorted(f"rang_{n}" for n in range(1, 11))
    assert "06" in page.get_text() and "10" in page.get_text()


def _declared_data_ids(raw):
    """The data ids a workbook file declares, on its pages and its blocks."""
    ids = []
    for page in raw.get("pages", []):
        ids += [page["data_id"]] if "data_id" in page else []
        ids += [b["data_id"] for b in page.get("blocks") or [] if "data_id" in b]
    return ids


def _raw_workbooks():
    for workbook_id in WORKBOOK_IDS:
        with open(os.path.join(WORKBOOKS_DIR, f"{workbook_id}.json"), encoding="utf-8") as f:
            yield workbook_id, json.load(f)


def test_data_ids_are_unique_and_name_their_carnet():
    for workbook_id, raw in _raw_workbooks():
        ids = _declared_data_ids(raw)
        assert len(ids) == len(set(ids)), workbook_id
        if "carnet" in raw:
            assert all(data_carnet(i) == raw["carnet"] for i in ids), workbook_id
        else:
            assert ids == [], f"{workbook_id} : seul un carnet du bilan déclare des données"


def test_reports_point_to_declared_data():
    """A report to a carnet whose file exists must name a data id that file declares."""
    declared = {}  # a carnet and its modules (module-creation.json is a module of the carnet de route)
    for _, raw in _raw_workbooks():
        if "carnet" in raw:
            declared.setdefault(raw["carnet"], set()).update(_declared_data_ids(raw))
    for workbook_id, raw in _raw_workbooks():
        for page in raw.get("pages", []):
            for block in page.get("blocks") or []:
                for item in block.get("items") or [] if block.get("type") == "report" else []:
                    source = data_carnet(item[1])
                    if source in declared:
                        assert item[1] in declared[source], (workbook_id, item[1])


# --- Carnet 7 and the carnet de route: one file per part, one per session ------------------

PART_FILE_IDS = [workbook_id for workbook_id, raw in _raw_workbooks() if raw.get("part_files")]


def test_carnet_7_and_the_carnet_de_route_have_one_file_per_part():
    """The app of the bilan sends one file per session: these two carnets cover two sessions each."""
    assert PART_FILE_IDS == ["carnet-7", "carnet-de-route"]


@functools.lru_cache(maxsize=None)
def _part_pdf(workbook_id, part):
    buffer = io.BytesIO()
    build_reference_workbook(workbook_id, buffer, part)
    return buffer.getvalue()


def _flat(pdf_bytes):
    """The text of a PDF without spaces: tracked capitals come out letter by letter."""
    return "".join("".join(page.get_text().split()) for page in pymupdf.open(stream=pdf_bytes, filetype="pdf"))


@pytest.mark.parametrize("workbook_id", PART_FILE_IDS)
def test_each_part_reads_as_a_whole_carnet(workbook_id):
    """
    Its cover, its opener with only its exercises and its writing time, its exercises, its
    deliverable and its back cover; its folio names the part, and no text speaks of a part
    of the same file any more (« Fin de la partie 1 », « Je renvoie la partie 1 complétée »).
    """
    spec = load_workbook(workbook_id)
    assert all(page.part for page in spec.pages)
    for part in part_numbers(spec):
        document = part_document(spec, part)
        templates = [page.template for page in document.pages]
        assert templates[:2] == ["cover", "summary"] and templates[-2:] == ["engagement", "closing"], part
        assert templates.count("cover") == templates.count("summary") == 1, part

        opener = document.pages[1].params
        listed = {int(n) for n in re.findall(r"Exercice\s(\d+)", " ".join(opener["points"]))}
        written = {int(n) for page in document.pages for n in re.findall(r"^Exercice\s(\d+)", page.part_title or "")}
        assert listed == written and opener["duration"], part
        texts = " ".join(str(v) for page in document.pages for v in _strings(page.model_dump())).replace("\xa0", " ")
        assert not re.search(r"Fin de la partie|la partie \d complétée|\bPartie \d ·", texts), part

        doc = pymupdf.open(stream=_part_pdf(workbook_id, part), filetype="pdf")
        assert doc.metadata["title"] == f"Marge de Manœuvre · {part_title(spec, part)}"
        assert f"·PARTIE{part}·P.2" in "".join(doc[1].get_text().split())  # the folio of the opener


def _strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings(v)]
    return []


@pytest.mark.parametrize("workbook_id", PART_FILE_IDS)
def test_each_part_keeps_the_field_ids_of_the_carnet(workbook_id):
    """The app reads the answers by field: each field in one file only, with the id it had in the whole carnet."""
    spec = load_workbook(workbook_id)
    fields = [{w.field_name for page in pymupdf.open(stream=_part_pdf(workbook_id, part), filetype="pdf")
               for w in page.widgets()} for part in part_numbers(spec)]
    whole = {w.field_name for page in pymupdf.open(stream=_workbook_pdf(workbook_id), filetype="pdf")
             for w in page.widgets()}

    assert not set.intersection(*fields)
    assert set.union(*fields) == whole


@pytest.mark.parametrize("workbook_id", PART_FILE_IDS)
def test_each_part_has_unique_field_ids(workbook_id, monkeypatch):
    reserve = forms.reserve_field_name
    repeated = []

    def checking_reserve(form, name):
        if str(name).replace(".", "_") in getattr(form, "_mdm_field_names", set()):
            repeated.append(name)
        return reserve(form, name)

    monkeypatch.setattr(forms, "reserve_field_name", checking_reserve)
    for part in part_numbers(load_workbook(workbook_id)):
        build_reference_workbook(workbook_id, io.BytesIO(), part)
    assert repeated == []


def _field_ids(value):
    """The field ids and prefixes a page or a block names, in its rows and items too."""
    if isinstance(value, dict):
        own = [value[k] for k in ("field_id", "field_prefix") if isinstance(value.get(k), str)]
        return own + [i for v in value.values() for i in _field_ids(v)]
    if isinstance(value, list):
        # a fields_card field or a rating_grid line: [label, field_id, …]
        own = [value[1]] if len(value) > 1 and isinstance(value[0], str) and isinstance(value[1], str) else []
        return own + [i for v in value for i in _field_ids(v)]
    return []


def test_reports_name_the_part_and_the_page_of_its_file():
    """« carnet 7 · partie 2 · p. 9 »: the page of the part's own file where the data is written."""
    for workbook_id in PART_FILE_IDS:
        raw = dict(_raw_workbooks())[workbook_id]
        locations = reference_data_locations(raw["carnet"])
        assert set(locations) == set(_declared_data_ids(raw))
        for page in raw["pages"]:
            for holder in [page] + (page.get("blocks") or []):
                if "data_id" not in holder:
                    continue
                part, number = locations[holder["data_id"]]
                assert part == page["part"], holder["data_id"]
                pdf_page = pymupdf.open(stream=_part_pdf(workbook_id, part), filetype="pdf")[number - 1]
                names = {w.field_name for w in pdf_page.widgets()}
                assert any(name.startswith(i) for name in names for i in _field_ids(holder)), (holder["data_id"], number)

    # Every document that reports such data prints its part and its page
    for workbook_id, raw in _raw_workbooks():
        reported = {item[1] for page in raw["pages"] for block in page.get("blocks") or []
                    if block["type"] == "report" for item in block["items"]}
        expected = set()
        for data_id in reported:
            carnet = data_carnet(data_id)
            if carnet in (7, "route") and data_id in reference_data_locations(carnet):
                part, number = reference_data_locations(carnet)[data_id]
                expected.add(f"{'CARNETDEROUTE' if carnet == 'route' else 'CARNET7'}·PARTIE{part}·P.{number}")
        spec = load_workbook(workbook_id)
        pdfs = [_part_pdf(workbook_id, part) for part in part_numbers(spec)] if spec.part_files else [
            _workbook_pdf(workbook_id)]
        text = "".join(_flat(pdf) for pdf in pdfs)
        assert all(origin in text for origin in expected), (workbook_id, expected)


def test_app_downloads_a_part_under_its_standard_name():
    """The app of the bilan recognizes the carnet and its part by the name: « Carnet_7_partie_2 », then the person."""
    client = TestClient(app)
    spec = client.get("/api/templates/carnet-7").json()

    pdf = client.post("/api/compile?part=2", json=spec)
    named = client.post("/api/compile?part=2", json=dict(spec, beneficiary_name="Camille Roux"))
    whole = client.post("/api/compile?part=1", json=client.get("/api/templates/carnet-1").json())

    assert pdf.status_code == 200
    assert "filename=Carnet_7_partie_2.pdf" in pdf.headers["content-disposition"]
    assert "filename=Carnet_7_partie_2_Camille_Roux.pdf" in named.headers["content-disposition"]
    cli = pymupdf.open(stream=_part_pdf("carnet-7", 2), filetype="pdf")
    assert [p.get_text() for p in pymupdf.open(stream=pdf.content, filetype="pdf")] == [p.get_text() for p in cli]
    assert whole.status_code == 422  # carnet 1 is one file


def test_answer_sizes_of_the_format_are_those_of_the_layout():
    assert set(ANSWERS) == set(components.ANSWER_SIZES)


def test_answer_sizes_in_files_are_known():
    """An answer size given in a list is not validated: a typo would leave a one-line box."""
    for workbook_id, raw in _raw_workbooks():
        for page in raw["pages"]:
            for block in page.get("blocks") or []:
                given = [block.get("answer")] + [q.get("answer") for q in block.get("questions") or []]
                if block["type"] == "fields_card":
                    given += [field[2] for row in block.get("rows", []) for field in row if len(field) > 2]
                if block["type"] == "report":
                    given += [item[3] for item in block.get("items", []) if len(item) > 3]
                if block["type"] == "table":
                    given += [cell.get("answer") for row in block.get("rows", []) for cell in row
                              if isinstance(cell, dict)]
                for value in given:
                    assert not isinstance(value, str) or value in ANSWERS, (workbook_id, page.get("title"), value)


CARNET_IDS = [workbook_id for workbook_id, raw in _raw_workbooks() if "carnet" in raw]
# The documents written in: the carnets, their module and the two full livrets
WRITTEN_IDS = CARNET_IDS + ["business-plan", "livret-competences"]
CM = 72 / 2.54
FIELD_INSET = 3  # draw_answer_box lays its field 3 pt inside the drawn box


@functools.lru_cache(maxsize=None)
def _workbook_pdf(workbook_id):
    buffer = io.BytesIO()
    build_reference_workbook(workbook_id, buffer)
    return buffer.getvalue()


def _used_share(page):
    """How far down the content of a page goes, the folio aside (share of its height)."""
    limit = page.rect.height - 60
    bottoms = [b[3] for b in page.get_text("blocks") if b[3] < limit]
    bottoms += [d["rect"].y1 for d in page.get_drawings() if d["rect"].y1 < limit]
    return max(bottoms, default=0) / page.rect.height


@pytest.mark.parametrize("workbook_id", WRITTEN_IDS)
def test_exercises_split_into_balanced_pages(workbook_id):
    """
    An exercise too long for one page is cut between two blocks (page_break), so that its
    « (suite) » page is a page of its own: never a small block left alone at its top.
    """
    for page in pymupdf.open(stream=_workbook_pdf(workbook_id), filetype="pdf"):
        if "(suite)" in page.get_text():
            assert _used_share(page) >= 0.4, page.number + 1


@pytest.mark.parametrize("workbook_id", WRITTEN_IDS)
def test_fields_leave_room_to_write_by_hand(workbook_id):
    """
    A carnet or the business plan is filled on screen or printed: a box for a sentence
    leaves two handwritten lines (1.6 cm), a one-line box room for a word (0.8 cm), and
    every field has a tooltip.
    """
    for page in pymupdf.open(stream=_workbook_pdf(workbook_id), filetype="pdf"):
        for widget in page.widgets():
            where = (page.number + 1, widget.field_name)
            assert widget.field_label, where
            if widget.field_type != pymupdf.PDF_WIDGET_TYPE_TEXT:
                continue
            box_cm = (widget.rect.height + 2 * FIELD_INSET) / CM
            multiline = bool(widget.field_flags & pymupdf.PDF_TX_FIELD_IS_MULTILINE)
            assert box_cm >= (1.6 if multiline else 0.8) - 0.01, (*where, round(box_cm, 2))
