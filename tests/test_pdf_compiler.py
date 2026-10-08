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
