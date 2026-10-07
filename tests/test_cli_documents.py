import importlib
import io

import pymupdf
import pytest

from test_layout import _assert_nothing_off_page

# (script module, generator function) of the 10 CLI documents
DOCUMENTS = [
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
