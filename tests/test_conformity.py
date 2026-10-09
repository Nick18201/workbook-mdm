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


def test_the_paper_workflow_is_flagged():
    # Everything is done on screen: the carnet is sent back complete before the session
    for text in ("Apportez ce carnet à la séance.", "Vous préférez écrire à la main ? Imprimez-le.",
                 "Remplissez ce PDF à l'écran ou sur papier."):
        page = {"template": "composite", "blocks": [{"type": "paragraphs", "items": [text]}]}
        assert (FIX, "papier") in _rules(_spec(page), structure=False), text
    ok = {"template": "composite", "blocks": [{"type": "paragraphs", "items": [
        "Ce que vous apportez à une équipe. Renvoyez ce carnet complété d'ici là."]}]}
    assert (FIX, "papier") not in _rules(_spec(ok), structure=False)


def test_a_precaution_that_treats_the_person_as_fragile_is_flagged():
    for text in ("Il peut remuer. Prenez-le à votre rythme.", "Si cet exercice vous semble trop lourd, passez-le.",
                 "Un mot suffit, ou laissez la case vierge pour la séance."):
        page = {"template": "composite", "blocks": [{"type": "protocol", "text": text}]}
        assert (CHECK, "precaution") in _rules(_spec(page), structure=False), text
    factual = {"template": "composite", "blocks": [{"type": "protocol", "text": (
        "Cet exercice parle de votre famille : ce que vous en avez retenu oriente encore vos choix.")}]}
    assert (CHECK, "precaution") not in _rules(_spec(factual), structure=False)


def test_a_forbidden_word_quoted_as_a_message_received_is_accepted():
    quoted = {"template": "composite", "blocks": [{"type": "paragraphs", "items": [
        "Les messages reçus sur le travail : « épanouissement », « passion », « devoir »…"]}]}
    ours = {"template": "composite", "blocks": [{"type": "paragraphs", "items": [
        "Ce carnet vise votre épanouissement."]}]}
    assert (FIX, "dev-perso") not in _rules(_spec(quoted), structure=False)
    assert (FIX, "dev-perso") in _rules(_spec(ours), structure=False)


def test_a_gendered_turn_of_phrase_is_flagged():
    page = {"template": "composite", "blocks": [{"type": "question", "question": "Ce qui m'a surpris"}]}
    neutral = {"template": "composite", "blocks": [{"type": "question", "question": "Ce que cette personne m'a appris"}]}
    assert (CHECK, "genre") in _rules(_spec(page), structure=False)
    assert (CHECK, "genre") not in _rules(_spec(neutral), structure=False)
    # An adverb in between, as Gemini wrote it (essais du lot 3)
    proud = {"template": "composite", "blocks": [{"type": "question", "question": "La compétence dont je suis le plus fier"}]}
    assert (CHECK, "genre") in _rules(_spec(proud), structure=False)


def test_each_example_takes_another_trade():
    # Carnet 7 customized by Gemini took « Scénographe » three times (essais du lot 3)
    example = {"type": "contrast_example", "title": "Scénographe", "surface": "Ça va.", "exploitable": "Une piste vérifiée."}
    pages = [{"template": "composite", "blocks": [example]}, {"template": "composite", "blocks": [dict(example)]}]
    findings = [f for f in check_spec(_spec(*pages), structure=False) if f.rule == "exemple-repete"]
    assert [(f.level, f.page) for f in findings] == [(CHECK, 2)] and "p. 1" in findings[0].message


def test_an_example_that_tells_the_person_s_own_situation_is_flagged():
    # Gemini wrote the person's story under a neighbouring trade (essais du lot 3)
    context = ("Comptable en cabinet depuis 15 ans, un foyer à deux revenus. Envisage une reconversion vers "
               "l'ébénisterie, puis un atelier à son compte.")
    mirror = {"type": "contrast_example", "title": "Céramiste", "surface": "On s'en sort.",
              "exploitable": "Je crains de financer une année de reconversion sans revenu, avant d'ouvrir mon atelier."}
    own_facts = {"type": "contrast_example", "title": "Libraire", "surface": "Ça va, je m'en sors.",
                 "exploitable": "En tension : le loyer passe, mais je repousse chaque réparation de la boutique."}
    findings = check_spec(_spec({"template": "composite", "blocks": [mirror, own_facts]}), structure=False,
                          context=context)
    flagged = [f for f in findings if f.rule == "exemple-personne"]
    assert len(flagged) == 1 and "Céramiste" in flagged[0].message and "« reconversion »" in flagged[0].message
    assert flagged[0].level == CHECK


def test_a_commitment_to_bring_the_carnet_is_the_paper_workflow():
    page = {"template": "engagement", "params": {"lines": ["J'apporte ce carnet à la séance 3."]}}
    sent = {"template": "engagement", "params": {"lines": ["Je renvoie ce carnet complété avant la séance 3.",
                                                           "J'apporte deux tâches de mon travail à essayer ensemble."]}}
    assert (FIX, "papier") in _rules(_spec(page), structure=False)
    assert (FIX, "papier") not in _rules(_spec(sent), structure=False)


def test_a_figure_needs_its_source_in_the_same_block():
    for text in ("60 % des cadres changent de métier.", "7 personnes sur 10 regrettent leur choix.",
                 "Une personne sur deux y pense.", "Les études montrent que l'écriture aide à décider."):
        page = {"template": "composite", "blocks": [{"type": "paragraphs", "items": [text]}]}
        assert (CHECK, "statistique") in _rules(_spec(page), structure=False), text
    sourced = {"template": "composite", "blocks": [
        {"type": "paragraphs", "items": ["60 % des créations passent le cap des cinq ans (source : INSEE)."]},
        {"type": "link_card", "title": "Où chercher", "links": [["Baromètre", "https://example.org/barometre",
                                                                  "3 recrutements sur 10 passent par le réseau."]]},
    ]}
    plain = {"template": "composite", "blocks": [{"type": "paragraphs", "items": [
        "Notez votre énergie de 0 à 10, puis un regard sur deux pistes."]}]}
    assert (CHECK, "statistique") not in _rules(_spec(sourced), structure=False)
    assert (CHECK, "statistique") not in _rules(_spec(plain), structure=False)


def _opener(points, duration):
    return {"template": "summary", "params": {"points": points, "duration": duration}}


def _exercise(eyebrow):
    return {"template": "composite", "part_title": eyebrow,
            "blocks": [{"type": "question", "question": "Ce que je retiens", "answer": "sentence"}]}


def _durations(spec, **kwargs):
    return [f.message for f in check_spec(spec, **kwargs) if f.rule == "duree"]


def test_the_writing_times_add_up():
    consistent = _spec(
        {"template": "cover"},
        _opener(["Météo · 2 min", "Exercice 1 · Vos contraintes · 25 min", "Exercice 2 · Vos pistes · 1 h 05",
                 "Exercice 3 · Pour aller plus loin · facultatif · 15 min", "Fin de carnet · 5 min"], "1 h 37"),
        _exercise("Exercice 1 · Vos contraintes · 25 min"),
        _exercise("Exercice 2 · Vos pistes · 45 min"), _exercise("Exercice 2 · Vos pistes, suite · 20 min"),
        _exercise("Exercice 3 · Pour aller plus loin · facultatif · 15 min"),
        {"template": "engagement"}, {"template": "closing"},
    )
    assert _durations(consistent, duration_min=90) == []

    drifting = _spec(
        {"template": "cover"},
        _opener(["Exercice 1 · Vos contraintes · 15 min", "Exercice 2 · Vos pistes · 20 min"], "1 h"),
        _exercise("Exercice 1 · Vos contraintes · 25 min"),
        _exercise("Exercice 2 · Vos pistes · 20 min"),
        _exercise("Exercice 3 · Votre décision · 10 min"),
        {"template": "engagement"}, {"template": "closing"},
    )
    messages = _durations(drifting, duration_min=30)
    assert any("l'exercice 1 compte 15 min dans l'ouverture et 25 min" in m for m in messages)
    assert any("l'exercice 3 n'est pas dans la liste" in m for m in messages)
    assert any("annonce 1 h au total, et ses lignes font 35 min" in m for m in messages)
    assert any("durée d'écriture demandée était de 30 min" in m for m in messages)
    # A support laid out as written has no template to add up
    assert _durations(drifting, structure=False, duration_min=30) == []


def test_a_box_says_the_answer_it_expects():
    unsized = {"template": "composite", "blocks": [{"type": "question", "question": "Mon prochain pas"}]}
    one_line = {"template": "composite", "blocks": [{"type": "fields_card", "rows": [
        [["Date", "date"], ["Ce que je retiens de l'échange", "retiens"]]]}]}
    sized = {"template": "composite", "blocks": [
        {"type": "question", "question": "Mon prochain pas", "answer": "sentence"},
        {"type": "fields_card", "rows": [[["Date", "date"], ["Lieu", "lieu"]],
                                         [["Ce que je retiens", "retiens", "sentence"]]]},
        # A group shares the room left on the page between its boxes
        {"type": "questions_group", "questions": [{"question": "Pourquoi ce métier ?", "field_id": "pourquoi"}]},
    ]}
    assert (CHECK, "case-sans-taille") in _rules(_spec(unsized), structure=False)
    assert (CHECK, "case-sans-taille") in _rules(_spec(one_line), structure=False)
    assert (CHECK, "case-sans-taille") not in _rules(_spec(sized), structure=False)


def test_a_web_address_the_notes_do_not_give_is_flagged():
    page = {"template": "composite", "blocks": [{"type": "link_card", "title": "Où chercher", "links": [
        ["APEC", "https://www.apec.fr/", "les fiches métiers."],
        ["Fiches", "https://www.apec.fr/candidat/fiches-metiers.html", "les fiches."],
        ["Inventé", "https://www.metiers-de-demain.fr", "un site."]]}]}
    notes = "Pour ses recherches : l'APEC (apec.fr), sans plus."
    findings = [f for f in check_spec(_spec(page), structure=False, sources=notes) if f.rule == "adresse"]
    assert [f.level for f in findings] == [FIX, FIX]
    assert "fiches-metiers" in findings[0].message and "metiers-de-demain" in findings[1].message
    # Without the text of origin (a customization), nothing to compare
    assert not [f for f in check_spec(_spec(page), structure=False) if f.rule == "adresse"]
