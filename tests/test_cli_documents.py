import importlib
import io

import pymupdf
import pytest

from test_layout import _assert_nothing_off_page
from workbook_generator.components import create_cover_page
from workbook_generator.config import PDFStyle
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.primitives import draw_folio

# (script module, generator function) of the CLI documents built from workbooks/
DOCUMENTS = [
    ("main_generate_carnet_1", "generate_workbook_carnet_1"),
    ("main_generate_carnet_2", "generate_workbook_carnet_2"),
    ("main_generate_carnet_3", "generate_workbook_carnet_3"),
    ("main_generate_carnet_4", "generate_workbook_carnet_4"),
    ("main_generate_carnet_5", "generate_workbook_carnet_5"),
    ("main_generate_carnet_6", "generate_workbook_carnet_6"),
    ("main_generate_chap0", "generate_workbook_chap0"),
    ("main_generate_chap1", "generate_workbook_chap1"),
    ("main_generate_chap2", "generate_workbook_chap2"),
    ("main_generate_chap3", "generate_workbook_chap3"),
    ("main_generate_chap4", "generate_workbook_chap4"),
    ("main_generate_chap5", "generate_workbook_chap5"),
    ("main_generate_chap6", "generate_workbook_chap6"),
    ("main_generate_livret", "build_livret_competences"),
    ("main_generate_business_plan", "generate_workbook_business_plan"),
]


@pytest.mark.parametrize("module, function", DOCUMENTS)
def test_cli_document_stays_on_its_pages(module, function):
    buffer = io.BytesIO()
    getattr(importlib.import_module(module), function)(buffer)
    doc = pymupdf.open(stream=buffer.getvalue(), filetype="pdf")

    _assert_nothing_off_page(doc)
    # Every inner page carries the folio; the cover and the back cover do not
    for page in list(doc)[1:-1]:
        assert "MARGE DE MANŒUVRE" in page.get_text(), page.number


def _rgb(color):
    return tuple(round(v * 255) for v in color.rgb())


def test_cover_illustration_takes_the_document_pastel():
    buffer = io.BytesIO()
    builder = DocumentBuilder(buffer, carnet=7)
    builder.add_page(create_cover_page, "Confronter *au terrain.*", 7, None, None, "Un salaire et un rythme de vie.")
    builder.save()
    page = pymupdf.open(stream=buffer.getvalue(), filetype="pdf")[0]

    fills = {tuple(round(v * 255) for v in d["fill"]) for d in page.get_drawings() if d.get("fill")}
    assert _rgb(PDFStyle.COLOR_BLUE) in fills  # the open notebook of the illustration
    assert _rgb(PDFStyle.PASTELS["blush"]) in fills  # carnet 7's pastel...
    assert _rgb(PDFStyle.PASTELS["lilac"]) not in fills  # ...in place of the SVG's placeholder
    assert "Un salaire et un rythme de vie." in " ".join(page.get_text().split())


@pytest.mark.parametrize("carnet, eyebrow, folio", [
    (3, "CARNETDEBORD·CARNET3", "CARNET3/7"),
    ("route", "CARNETDEROUTE", "CARNETDEROUTE·P.2"),
])
def test_carnet_names_its_cover_and_folio(carnet, eyebrow, folio):
    buffer = io.BytesIO()
    builder = DocumentBuilder(buffer, carnet=carnet)
    builder.add_page(create_cover_page, "Un *titre.*", None if carnet == "route" else carnet)
    builder.add_page(lambda c: (draw_folio(c), c.showPage()))
    builder.save()
    doc = pymupdf.open(stream=buffer.getvalue(), filetype="pdf")

    # Tracked capitals come out letter by letter: compare without spaces
    assert eyebrow in "".join(doc[0].get_text().split()).upper()
    assert folio in "".join(doc[1].get_text().split()).upper()


def test_pdf_declares_its_language():
    buffer = io.BytesIO()
    builder = DocumentBuilder(buffer)
    builder.add_page(lambda c: c.showPage())
    builder.save()
    doc = pymupdf.open(stream=buffer.getvalue(), filetype="pdf")

    assert doc.xref_get_key(doc.pdf_catalog(), "Lang") == ("string", "fr-FR")
