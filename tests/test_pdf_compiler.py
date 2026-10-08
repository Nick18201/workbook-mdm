import pymupdf

from server.models import BlockSpec, PageSpec, WorkbookSpec
from workbook_generator.compiler import compile_workbook_from_spec
from server.predefined_workbooks import get_predefined_spec


def _open(spec):
    return pymupdf.open(stream=compile_workbook_from_spec(spec), filetype="pdf")


def test_summary_intro_markup_is_rendered_as_plain_text():
    intro = (
        'Voir <a href="https://exemple.test">ce lien</a> '
        '<img src="assets/illustrations/logo_qualiopi.jpg" width="80" height="40"/> & <b'
    )
    page = _open(
        WorkbookSpec(pages=[PageSpec(template="summary", title="S", params={"intro_text": intro, "points": []})])
    )[0]

    assert page.get_links() == []
    assert page.get_images() == []  # the injected logo is not drawn
    assert "href" in page.get_text()


def test_field_names_are_unique_across_the_document():
    def twice(template, params):
        return [PageSpec(template=template, title=f"{template} {i}", params=params) for i in (1, 2)]

    pages = (
        twice("questions", {"questions": [{"question": "Q1 ?"}, {"question": "Q2 ?"}]})
        + twice("meteo", {})
        + twice("quadrants", {})
        + twice("two_columns", {"rows": [{"label": "1. Ligne"}]})
        + twice("enquete", {})
        + twice("roadmap", {})
        + twice("engagement", {})
        # Gemini may also repeat explicit ids from one page to the next
        + twice("questions", {"questions": [{"question": "Q ?", "field_id": "meme_id"}]})
    )
    doc = _open(WorkbookSpec(pages=pages))

    # Radio buttons of one scale share their group name on purpose: one entry per group
    pages_by_name = {}
    names = []
    for page in doc:
        seen_radio_groups = set()
        for w in page.widgets():
            pages_by_name.setdefault(w.field_name, set()).add(page.number)
            if w.field_type == pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON:
                if w.field_name in seen_radio_groups:
                    continue
                seen_radio_groups.add(w.field_name)
            names.append(w.field_name)

    duplicates = {n for n in names if names.count(n) > 1}
    assert names and duplicates == set()
    assert all(len(p) == 1 for p in pages_by_name.values())


def test_table_block_without_headers_compiles_with_default_headers():
    spec = WorkbookSpec(
        pages=[
            PageSpec(
                template="composite",
                title="Tableau",
                blocks=[BlockSpec(type="table", rows=[["Finances", "Modéré", "Plan B"]])],
            )
        ]
    )
    text = _open(spec)[0].get_text()

    assert "Finances" in text
    assert "CRITÈRE" in text.upper()


def test_predefined_workbook_pdf_stays_light():
    pdf = compile_workbook_from_spec(get_predefined_spec("chap1"))

    assert len(pdf) < 1_500_000


def _words(page):
    return " ".join(page.get_text().split())


def test_opener_of_a_carnet_gives_its_duration_and_frame():
    spec = WorkbookSpec(carnet=2, pages=[PageSpec(template="summary", title="Mon *parcours.*", params={
        "num": "2", "points": ["Exercice 1 · Vos expériences · 40 min"], "duration": "2 h 45",
        "split": "En trois fois : exercices 1 et 2, 3 à 5, puis 6 à 8.",
    })])
    text = _words(_open(spec)[0])

    assert "Comptez 2 h 45 d'écriture, hors entretiens et recherches." in text
    assert "En trois fois" in text
    assert "Vous pouvez passer une question." in text
    # Outside the carnets of the bilan, no frame: the reference documents keep their opener
    other = _words(_open(WorkbookSpec(pages=[PageSpec(template="summary", title="S", params={"points": ["Un"]})]))[0])
    assert "passer une question" not in other


def test_end_of_carnet_has_guided_zones_and_the_thread_of_leads():
    spec = WorkbookSpec(pages=[PageSpec(template="engagement", title="Votre livrable.", params={
        "lines": ["Je relis mes réponses."], "field_prefix": "fin", "pistes": True,
    })])
    page = _open(spec)[0]
    names = {w.field_name for w in page.widgets()}

    assert {"fin_zone_1", "fin_zone_2", "fin_zone_3", "fin_piste"} <= names
    assert "À aborder en séance" in _words(page)
    assert not any(n.startswith("notes_") for n in names)


def test_protocol_texts_are_fixed():
    spec = WorkbookSpec(pages=[PageSpec(template="composite", title="Votre histoire.", blocks=[
        BlockSpec(type="protocol", text="Cet exercice revient sur votre enfance."),
        BlockSpec(type="question", question="Q ?", field_id="q"),
        BlockSpec(type="anchor", field_id="ancrage"),
    ])])
    page = _open(spec)[0]
    text = _words(page)

    assert "Cet exercice revient sur votre enfance." in text
    assert "laissez-le vierge : nous l'aborderons ensemble." in text
    assert "Aujourd'hui, avec le recul, je sais que…" in text
    assert "ancrage" in {w.field_name for w in page.widgets()}
