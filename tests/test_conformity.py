"""The conformity check: our reference workbooks pass it, and it catches what Gemini got wrong."""

import pytest

from workbook_generator.conformity import CHECK, FIX, check_spec
from workbook_generator.spec import WorkbookSpec, load_workbook
from server.predefined_workbooks import CATALOGUE


def _spec(*pages):
    return WorkbookSpec(pages=list(pages))


def _rules(spec, **kwargs):
    return {(f.level, f.rule) for f in check_spec(spec, **kwargs)}


# The full business plan keeps its gendered wording (« Traiteur », « Menuisier », « vos clients »):
# it was left out of that rule (feuille de route, decision 106)
KNOWN_EXCEPTIONS = {"business-plan": {"metier-genre"}}


@pytest.mark.parametrize("workbook_id", [entry[0] for entry in CATALOGUE])
def test_reference_workbooks_pass_the_check(workbook_id):
    # The rules come from these workbooks: a finding here means a rule is too strict
    allowed = KNOWN_EXCEPTIONS.get(workbook_id, set())
    assert [f for f in check_spec(load_workbook(workbook_id), layout=True) if f.rule not in allowed] == []


def test_a_continuation_page_holding_one_small_block_is_flagged():
    long_page = {"template": "composite", "title": "Un long exercice.", "part_title": "Exercice 1 · Long · 30 min",
                 "blocks": [{"type": "question", "question": f"Question {k}", "field_id": f"q{k}", "answer": "sentence"}
                            for k in range(7)]}
    findings = [f for f in check_spec(_spec(long_page), structure=False, layout=True) if f.rule == "suite-presque-vide"]
    assert [f.page for f in findings] == [1]


def test_examples_take_an_epicene_neighbouring_trade_without_amounts():
    page = {"template": "composite", "blocks": [
        {"type": "contrast_example", "title": "Formatrice bureautique", "surface": "Ça paie.",
         "exploitable": "Minimum sécurisant : 2 800 € par mois."},
        {"type": "contrast_example", "title": "Ergonome", "surface": "Ça va.", "exploitable": "Une fourchette, vue en séance."},
    ]}
    findings = check_spec(_spec(page), structure=False, context="Responsable logistique, future formatrice en gestion des stocks")
    assert {f.rule for f in findings} == {"metier-genre", "metier-personne", "montant"}
    assert all(f.level == CHECK for f in findings)


def test_forbidden_words_are_flagged():
    page = {"template": "composite", "title": "Votre coach.", "part_title": "Exercice 1 · Test · 10 min",
            "blocks": [{"type": "text", "text": "Une séance en présentiel pour retrouver la quête de sens."}]}
    rules = _rules(_spec(page), structure=False)
    assert {(FIX, "coach"), (FIX, "presentiel"), (FIX, "dev-perso")} <= rules


def test_tutoiement_is_flagged_except_in_a_quoted_message():
    told = {"template": "composite", "blocks": [{"type": "question", "question": "Que veux-tu changer ?"}]}
    quoted = {"template": "composite", "blocks": [{"type": "text", "text": "Envoyez : « Que ferais-tu à ma place ? »"}]}
    assert (FIX, "tutoiement") in _rules(_spec(told), structure=False)
    assert (FIX, "tutoiement") not in _rules(_spec(quoted), structure=False)


def test_a_table_needs_a_box_to_fill_in():
    read_only = {"template": "composite", "blocks": [{"type": "table", "headers": ["Indicateur", "Niveau de risque"],
                                                      "rows": [["Salaire", "À mesurer"]]}]}
    with_boxes = {"template": "composite", "blocks": [{"type": "table", "headers": ["Indicateur", "Ce que j'observe"],
                                                       "rows": [["Salaire", {"field_id": "salaire", "placeholder": "Salaire"}]]}]}
    assert (FIX, "tableau-sans-case") in _rules(_spec(read_only), structure=False)
    assert (FIX, "tableau-sans-case") not in _rules(_spec(with_boxes), structure=False)


def test_labels_the_pdf_cuts_are_flagged():
    page = {"template": "composite", "blocks": [
        {"type": "rating_grid", "items": [["Mon intérêt pour cette piste, après l'échange", "interet"]],
         "values": ["En baisse", "Stable", "En hausse"]},
        {"type": "scale", "label": "Confiance", "min_label": "0 · Aucune", "max_label": "10 · Confiance totale"},
    ]}
    findings = [f for f in check_spec(_spec(page), structure=False) if f.rule == "libelle-tronque"]
    assert len(findings) == 2


def test_the_common_template_is_checked():
    # A document like the one the former prompt made: old eyebrows, no duration, no deliverable
    spec = _spec(
        {"template": "cover"},
        {"template": "summary", "params": {"points": ["Cadrage"]}},
        {"template": "composite", "part_title": "1. CADRAGE INITIAL", "blocks": [{"type": "question", "question": "Votre hypothèse ?"}]},
        {"template": "roadmap", "part_title": "Exercice 2 · Feuille de route"},
        {"template": "closing"},
    )
    rules = _rules(spec)
    assert {(CHECK, "sourcil"), (CHECK, "duree"), (CHECK, "gabarit"), (CHECK, "exemple"), (CHECK, "roadmap")} <= rules
    # A document laid out as written skips the template, not the rest
    assert not {r for _, r in _rules(spec, structure=False)} & {"sourcil", "duree", "gabarit", "exemple"}


def test_a_heavy_question_needs_the_protocol_or_to_be_optional():
    question = {"type": "question", "question": "Ma plus grande peur face à ce changement", "answer": "sentence"}
    bare = {"template": "composite", "part_title": "Exercice 1 · Ce qui pèse · 10 min", "blocks": [question]}
    protected = {"template": "composite", "part_title": "Exercice 1 · Ce qui pèse · 10 min",
                 "blocks": [{"type": "protocol"}, question, {"type": "anchor", "field_id": "ancrage"}]}
    optional = {"template": "composite", "part_title": "Exercice 1 · Ce qui pèse · 10 min",
                "blocks": [dict(question, fixed=True)]}
    assert (CHECK, "charge") in _rules(_spec(bare), structure=False)
    assert (CHECK, "charge") not in _rules(_spec(protected), structure=False)
    assert (CHECK, "charge") not in _rules(_spec(optional), structure=False)


def test_a_gendered_turn_of_phrase_is_flagged():
    page = {"template": "composite", "blocks": [{"type": "question", "question": "Ce qui m'a surpris"}]}
    neutral = {"template": "composite", "blocks": [{"type": "question", "question": "Ce que cette personne m'a appris"}]}
    assert (CHECK, "genre") in _rules(_spec(page), structure=False)
    assert (CHECK, "genre") not in _rules(_spec(neutral), structure=False)
