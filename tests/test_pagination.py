"""The page breaks of a generated document: none when a page fits, balanced pages otherwise."""

import json

import pytest

import server.gemini_service as gemini_service
from server.models import IterateRequest, ParseRequest
from workbook_generator.compiler import workbook_page_fills
from workbook_generator.conformity import CONTINUATION_MIN_SHARE
from workbook_generator.pagination import balance_breaks, balance_page
from workbook_generator.spec import PageSpec, WorkbookSpec


def _question(k, answer="sentence"):
    return {"type": "question", "question": f"Question {k} ?", "field_id": f"q{k}", "answer": answer}


def _fills(page):
    return [f["used"] for f in workbook_page_fills(WorkbookSpec(pages=[page]))]


def _breaks(page):
    return [b.type for b in page.blocks].count("page_break")


def test_a_needless_page_break_of_the_model_goes_and_a_needed_one_stays():
    short = {"template": "composite", "title": "Court.", "blocks": [_question(1), {"type": "page_break"}, _question(2)]}
    long = {"template": "composite", "title": "Long.", "blocks": [
        _question(k, "paragraph") for k in range(4)] + [{"type": "page_break"}] + [
        _question(k, "paragraph") for k in range(4, 8)]}
    spec = balance_breaks(WorkbookSpec(pages=[short, long]))
    assert [_breaks(p) for p in spec.pages] == [0, 1]


def test_an_almost_empty_continuation_is_cut_again_into_balanced_pages():
    # Seven questions: six on the first page, the last one alone on its « (suite) » page
    page = PageSpec(template="composite", title="Un long exercice.", part_title="Exercice 1 · Long · 30 min",
                    blocks=[{"type": "paragraphs", "items": ["À quoi sert l'exercice."]}]
                    + [_question(k) for k in range(7)])
    assert min(_fills(page)) < CONTINUATION_MIN_SHARE
    balanced = balance_page(page)
    assert _breaks(balanced) == 1
    fills = _fills(balanced)
    assert len(fills) == 2 and min(fills) >= CONTINUATION_MIN_SHARE
    # The instruction stays with what follows it, and every block is still there, in order
    assert balanced.blocks[1].type != "page_break"
    assert [b.field_id for b in balanced.blocks if b.type == "question"] == [f"q{k}" for k in range(7)]


def test_a_cut_of_the_model_that_leaves_a_small_block_alone_is_moved():
    blocks = [_question(k) for k in range(6)]
    page = PageSpec(template="composite", title="Un exercice coupé trop tard.",
                    blocks=blocks[:5] + [{"type": "page_break"}] + blocks[5:])
    assert min(_fills(page)) < CONTINUATION_MIN_SHARE
    assert min(_fills(balance_page(page))) >= CONTINUATION_MIN_SHARE


def test_a_page_that_fills_its_pages_keeps_its_breaks():
    page = PageSpec(template="composite", title="Bien coupé.", blocks=[
        _question(k, "paragraph") for k in range(4)] + [{"type": "page_break"}] + [
        _question(k, "paragraph") for k in range(4, 8)])
    assert balance_page(page) == page


def test_fixed_pages_and_other_templates_are_left_alone():
    fixed = PageSpec(template="composite", title="Fixe.", fixed=True,
                     blocks=[_question(1), {"type": "page_break"}, _question(2)])
    cover = PageSpec(template="cover", params={"cover_title": "Titre."})
    assert balance_page(fixed) == fixed
    assert balance_page(cover) == cover


# --- In the app: documents created, laid out or retouched; never a customized carnet --

@pytest.fixture(autouse=True)
def fresh_gemini_clients():
    # Clients are cached per API key: a fake one must not outlive its test
    gemini_service._get_client.cache_clear()
    yield
    gemini_service._get_client.cache_clear()


def _gemini_answers(monkeypatch, payload):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    class Response:
        text = json.dumps(payload)

    class Models:
        def generate_content(self, **kwargs):
            return Response()

    class Client:
        def __init__(self, **kwargs):
            self.models = Models()

    monkeypatch.setattr(gemini_service.genai, "Client", Client)


LONG_EXERCISE = {"template": "composite", "title": "Un long exercice.", "part_title": "Exercice 1 · Long · 30 min",
                 "blocks": [_question(k) for k in range(7)]}


def test_a_created_document_comes_back_balanced(monkeypatch):
    _gemini_answers(monkeypatch, {"chapter_title": "Mes enquêtes", "pages": [
        {"template": "cover", "params": {"cover_title": "Mes *enquêtes.*"}}, LONG_EXERCISE, {"template": "closing"}]})
    spec, reason = gemini_service.parse_notes_with_gemini(ParseRequest(raw_notes="Notes"))
    assert reason is None
    assert _breaks(spec.pages[1]) == 1 and min(_fills(spec.pages[1])) >= CONTINUATION_MIN_SHARE


def test_a_retouched_document_is_balanced_but_never_a_customized_carnet(monkeypatch):
    created = WorkbookSpec(pages=[LONG_EXERCISE])
    customized = WorkbookSpec(pages=[dict(LONG_EXERCISE, data_id="c2.zones")])
    for current, balanced in ((created, True), (customized, False)):
        _gemini_answers(monkeypatch, {"spec": current.model_dump(exclude_unset=True), "changes_summary": "Fait."})
        response, reason = gemini_service.refine_spec_with_gemini(IterateRequest(current_spec=current, feedback="Ajuste."))
        assert reason is None
        assert (_breaks(response.spec.pages[0]) == 1) is balanced
