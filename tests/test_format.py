"""The format of R0 bis: data ids and reports between carnets, fixed and adaptable."""

import json

import pymupdf
import pytest
from pydantic import ValidationError

from workbook_generator import spec as spec_module
from workbook_generator.compiler import compile_workbook_from_spec, workbook_data_pages
from workbook_generator.spec import BlockSpec, PageSpec, WorkbookSpec, keep_fixed, tag_refs


def _flat_text(pdf):
    """The text of the PDF without spaces: tracked capitals come out letter by letter."""
    return "".join("".join(page.get_text().split()) for page in pymupdf.open(stream=pdf, filetype="pdf"))


def _page(title, blocks, **kwargs):
    return PageSpec(template="composite", title=title, part_title="", blocks=blocks, **kwargs)


def _question(field_id, **kwargs):
    return BlockSpec(type="question", question="Une question ?", field_id=field_id, **kwargs)


# --- Data ids and reports --------------------------------------------------------------

@pytest.mark.parametrize("data_id", ["seuils", "c8.seuils", "c4.Seuils", "carnet4.seuils", "c4."])
def test_a_data_id_names_its_carnet(data_id):
    with pytest.raises(ValidationError):
        _question("q", data_id=data_id)


def test_a_report_line_needs_a_data_id():
    with pytest.raises(ValidationError):
        BlockSpec(type="report", items=[["Vos seuils", "seuils", "f"]])


def test_data_pages_follow_pages_and_blocks():
    spec = WorkbookSpec(carnet=4, pages=[
        _page("Un.", [_question("a")]),
        _page("Deux.", [_question("b", data_id="c4.histoire")], data_id="c4.page"),
        PageSpec(template="engagement", title="Fin.", data_id="c4.livrable"),
    ])

    assert workbook_data_pages(spec) == {"c4.page": 2, "c4.histoire": 2, "c4.livrable": 3}


def test_report_names_the_carnet_and_page_of_its_data(tmp_path, monkeypatch):
    carnet_4 = WorkbookSpec(carnet=4, pages=[
        _page("Votre histoire.", [_question("histoire")]),
        _page("Vos quatre seuils.", [_question("seuils", data_id="c4.seuils")]),
    ])
    (tmp_path / "carnet-4.json").write_text(json.dumps(carnet_4.model_dump(exclude_unset=True)), encoding="utf-8")
    monkeypatch.setattr(spec_module, "WORKBOOKS_DIR", str(tmp_path))

    carnet_5 = WorkbookSpec(carnet=5, pages=[_page("Récapitulatif.", [BlockSpec(type="report", items=[
        ["Vos quatre seuils", "c4.seuils", "c5_seuils"],
        ["Votre profil", "c3.profil", "c5_profil"],  # carnet 3 has no file yet: no page
    ])])])
    text = _flat_text(compile_workbook_from_spec(carnet_5))

    assert "CARNET4·P.2" in text
    assert "CARNET3" in text and "CARNET3·P." not in text


def test_report_to_its_own_carnet_names_the_page(tmp_path, monkeypatch):
    monkeypatch.setattr(spec_module, "WORKBOOKS_DIR", str(tmp_path))
    route = WorkbookSpec(carnet="route", pages=[
        _page("Vos compétences.", [_question("competences", data_id="route.competences")]),
        _page("Vos pistes.", [BlockSpec(type="report", items=[["Vos compétences", "route.competences", "r"]])]),
    ])

    assert "CARNETDEROUTE·P.1" in _flat_text(compile_workbook_from_spec(route))


def test_module_of_a_carnet_reports_the_pages_of_the_carnet(tmp_path, monkeypatch):
    """A module shares the carnet de route's identity but declares no data: its reports name the carnet's pages."""
    route = WorkbookSpec(carnet="route", pages=[
        _page("Votre profil.", [_question("profil")]),
        _page("Vos pistes.", [_question("pistes", data_id="route.pistes")]),
    ])
    module = WorkbookSpec(carnet="route", pages=[
        _page("Vos fondations.", [BlockSpec(type="report", items=[["Ma piste A", "route.pistes", "m"]])]),
    ])
    for name, spec in [("carnet-de-route.json", route), ("carnet-de-route-module.json", module)]:
        (tmp_path / name).write_text(json.dumps(spec.model_dump(exclude_unset=True)), encoding="utf-8")
    monkeypatch.setattr(spec_module, "WORKBOOKS_DIR", str(tmp_path))

    assert "CARNETDEROUTE·P.2" in _flat_text(compile_workbook_from_spec(module))


# --- Fixed and adaptable ------------------------------------------------------------------

def _base():
    return WorkbookSpec(carnet=3, pages=[
        PageSpec(template="cover", params={"cover_title": "Mes *fonctionnements.*", "promise": "Promesse."}),
        _page("Le test.", [_question("test", subtitle="Texte du test.")], fixed=True),
        _page("Sous pression.", [
            BlockSpec(type="protocol", text="Avertissement."),
            _question("adaptable", subtitle="À adapter."),
            _question("fige", subtitle="Fixe.", fixed=True),
            BlockSpec(type="contrast_example", title="Libraire", surface="A.", exploitable="B."),
        ], data_id="c3.pression"),
    ])


def _customized(base):
    """What a customization could send back: everything rewritten, a fixed block dropped."""
    out = json.loads(json.dumps(base))
    out["carnet"] = 6
    out["pages"][0]["params"]["promise"] = "Promesse adaptée."
    out["pages"][1]["blocks"][0]["subtitle"] = "Test réécrit."
    blocks = out["pages"][2]["blocks"]
    blocks[0]["text"] = "Avertissement réécrit."
    blocks[1]["subtitle"] = "Adapté."
    blocks[3]["title"] = "Menuisier"
    del blocks[2]
    del out["pages"][2]["data_id"]
    return out


def test_customization_keeps_what_is_fixed():
    base = tag_refs(_base())
    spec = WorkbookSpec.model_validate(keep_fixed(base, _customized(base)))
    cover, test, pression = spec.pages

    assert spec.carnet == 3
    assert cover.params["promise"] == "Promesse adaptée."  # adaptable
    assert test.blocks[0].subtitle == "Texte du test."  # fixed page
    assert [b.type for b in pression.blocks] == ["protocol", "question", "question", "contrast_example"]
    assert pression.blocks[0].text == "Avertissement."  # the protocol never changes
    assert pression.blocks[1].subtitle == "Adapté."
    assert pression.blocks[2].field_id == "fige"  # dropped, put back in its place
    assert pression.blocks[3].title == "Menuisier"
    assert pression.data_id == "c3.pression"
    assert "_ref" not in json.dumps(spec.model_dump())


def test_customization_keeps_the_parts():
    base = tag_refs(WorkbookSpec(parts=["Les fondations"], pages=[_page("Un.", [_question("a")], part=1)]))
    out = json.loads(json.dumps(base))
    out["parts"] = ["Autre partie", "En plus"]
    del out["pages"][0]["part"]

    spec = WorkbookSpec.model_validate(keep_fixed(base, out))

    assert spec.parts == ["Les fondations"]
    assert spec.pages[0].part == 1


def test_customization_without_references_is_matched_by_position():
    base = tag_refs(_base())
    out = json.loads(json.dumps(base).replace('"_ref"', '"_autre"'))
    out["pages"][1]["blocks"][0]["subtitle"] = "Test réécrit."

    spec = WorkbookSpec.model_validate(keep_fixed(base, out))

    assert spec.pages[1].blocks[0].subtitle == "Texte du test."


def test_customization_that_lost_the_structure_is_refused():
    base = tag_refs(_base())
    out = {"pages": [{"template": "cover", "params": {}}, {"template": "questions", "params": {}}]}

    with pytest.raises(ValueError):
        keep_fixed(base, out)
