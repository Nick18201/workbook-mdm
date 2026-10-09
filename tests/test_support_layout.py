"""
« Mettre en page un support »: a finished support laid out as it was written. Its reading,
the fallback that rewrites nothing, the coverage check and the API. The support below is
synthetic, written for these tests, and shaped like a copy of a PDF: a repeated header, page
numbers, text in capitals, a wrapped instruction, options without boxes.
"""

import json

import pytest
from fastapi.testclient import TestClient

import server.gemini_service as gemini_service
from server.app import app
from server.models import LayoutRequest
from workbook_generator.conformity import FIX, check_spec
from workbook_generator.coverage import check_coverage, normalize, read_support, sentence_case, spec_texts
from workbook_generator.spec import WorkbookSpec

SUPPORT = """marge
de manoeuvre
m a r g e   d e   m a n o e u v r e
FICHE D'ENTRETIEN
1
Préparer l'échange
Ce support vous accompagne avant, pendant et après un échange avec une personne qui exerce le
métier que vous explorez.
MÉTIER EXPLORÉ :
PERSONNE RENCONTRÉE :
DATE :
NOM DE L'ENTREPRISE :
COMMENT L'ÉCHANGE SE FAIT-IL ?
☐ Téléphone ☐ Visio ☐ Sur place
CE QUE JE SAIS DÉJÀ DE CE MÉTIER :
CE QUI M'ATTIRE À CE STADE :

marge
de manoeuvre
m a r g e   d e   m a n o e u v r e
PENDANT L'ÉCHANGE
2
Les questions à poser
Notez les réponses telles qu'elles viennent, sans les trier.
• Gardez ces questions sous les yeux.
• Laissez la personne finir ses phrases.
QUEL A ÉTÉ VOTRE PARCOURS JUSQU'À CE POSTE ?
COMMENT SE PASSE UNE SEMAINE ORDINAIRE ?
QUELLES TÂCHES PRENNENT LE PLUS DE TEMPS ?
AVEC QUI TRAVAILLEZ-VOUS AU QUOTIDIEN ?
QU'EST-CE QUI VOUS PLAÎT LE PLUS DANS CE TRAVAIL ?
QU'EST-CE QUI EST LE PLUS DIFFICILE ?
QUELLES COMPÉTENCES SONT LES PLUS UTILES ?
COMMENT LE MÉTIER A-T-IL CHANGÉ CES DERNIÈRES ANNÉES ?
QUEL TYPE DE CONTRAT EST LE PLUS COURANT ?
CDI
CDD
Indépendant
QUI D'AUTRE ME CONSEILLERIEZ-VOUS DE RENCONTRER ?

marge
de manoeuvre
m a r g e   d e   m a n o e u v r e
APRÈS L'ÉCHANGE
3
Faire le point
Notez à chaud ce que vous retenez de l'échange.
MON INTÉRÊT POUR CE MÉTIER APRÈS L'ÉCHANGE :
1
2
3
4
5
CE QUI A CONFIRMÉ OU MODIFIÉ MON IMAGE DU MÉTIER :
CE MÉTIER EST-IL COMPATIBLE AVEC MES PRIORITÉS ?
Oui
En partie
Non
POURQUOI ?
MA PROCHAINE ACTION :
"""

# What a person counts in this support: every line ending with « ? » or « : »
QUESTIONS_AND_LABELS = [line for line in SUPPORT.splitlines() if line.endswith(("?", ":"))]


def _layout(**kwargs):
    return gemini_service._build_fallback_layout(LayoutRequest(source_text=SUPPORT, **kwargs))


# --- Reading a support ----------------------------------------------------------------

def test_the_support_is_read_as_its_author_wrote_it():
    sections = read_support(SUPPORT)
    assert [(s.eyebrow, s.title) for s in sections] == [
        ("FICHE D'ENTRETIEN", "Préparer l'échange"),
        ("PENDANT L'ÉCHANGE", "Les questions à poser"),
        ("APRÈS L'ÉCHANGE", "Faire le point"),
    ]
    items = [item for s in sections for item in s.items]
    elements = [item for item in items if item.kind in ("question", "label")]
    assert [item.text for item in elements] == QUESTIONS_AND_LABELS
    # The instruction cut by the copy of the PDF is whole again; the header and page numbers are gone
    assert items[0].text.endswith("une personne qui exerce le métier que vous explorez.")
    assert not any("marge" in item.text.lower() for item in items)
    by_text = {item.text: item for item in items}
    assert by_text["COMMENT L'ÉCHANGE SE FAIT-IL ?"].options == ["Téléphone", "Visio", "Sur place"]
    assert by_text["QUEL TYPE DE CONTRAT EST LE PLUS COURANT ?"].options == ["CDI", "CDD", "Indépendant"]
    assert by_text["CE MÉTIER EST-IL COMPATIBLE AVEC MES PRIORITÉS ?"].options == ["Oui", "En partie", "Non"]
    assert by_text["MON INTÉRÊT POUR CE MÉTIER APRÈS L'ÉCHANGE :"].scale == (1, 5)
    assert [item.text for item in items if item.kind == "bullet"] == [
        "Gardez ces questions sous les yeux.", "Laissez la personne finir ses phrases."]


def test_a_numbered_heading_starts_a_section_even_after_a_question():
    sections = read_support("Ma première question ?\nOui\nNon\n2. Le terrain\nLa question suivante ?")
    assert [s.title for s in sections] == ["", "2. Le terrain"]
    assert sections[0].items[0].options == ["Oui", "Non"]


def test_capitals_go_to_sentence_case_and_keep_their_acronyms():
    assert sentence_case("QU'EST-CE QUI VOUS PLAÎT ?") == "Qu'est-ce qui vous plaît ?"
    assert sentence_case("UN CDI OU UN CDD ?") == "Un CDI ou un CDD ?"
    assert sentence_case("Déjà en minuscules, CDI compris.") == "Déjà en minuscules, CDI compris."


# --- The fallback rewrites nothing ----------------------------------------------------

def test_the_fallback_keeps_every_element_word_for_word_in_order():
    spec = _layout().spec
    texts = spec_texts(spec)
    for line in QUESTIONS_AND_LABELS:
        assert sentence_case(line).rstrip(" :") in texts
    coverage = check_coverage(spec, SUPPORT)
    assert (coverage.found, coverage.total) == (len(QUESTIONS_AND_LABELS), len(QUESTIONS_AND_LABELS))
    assert coverage.options_found == coverage.options_total == 9
    assert coverage.missing == [] and coverage.out_of_order == []


def test_the_fallback_follows_our_rules_without_adding_anything():
    spec = _layout().spec
    findings = check_spec(spec, structure=False, layout=True)
    assert [f for f in findings if f.level == FIX] == []
    assert not any(f.rule == "suite-presque-vide" for f in findings)
    types = {b.type for p in spec.pages for b in p.blocks or []}
    assert not types & {"contrast_example", "protocol", "anchor", "energy", "annotation"}
    assert [p.template for p in spec.pages][0] == "cover" and spec.pages[-1].template == "closing"
    assert {p.template for p in spec.pages[1:-1]} == {"composite"}
    # The cover carries the title alone, the back cover no message
    assert spec.pages[0].params == {"cover_title": "Fiche d'entretien.", "number": ""}
    assert spec.pages[-1].params == {"messages": []}


def test_the_fallback_shapes_each_element():
    blocks = [b for p in _layout().spec.pages for b in p.blocks or []]
    cards = [b for b in blocks if b.type == "fields_card"]
    assert [field[0] for row in cards[0].rows for field in row] == [
        "Métier exploré", "Personne rencontrée", "Date", "Nom de l'entreprise"]
    assert all(field[2] == "word" for row in cards[0].rows for field in row)
    checklists = {b.title: b.items for b in blocks if b.type == "checklist"}
    assert checklists["Comment l'échange se fait-il ?"] == ["Téléphone", "Visio", "Sur place"]
    scale = next(b for b in blocks if b.type == "scale")
    assert (scale.label, scale.min_val, scale.max_val) == ("Mon intérêt pour ce métier après l'échange", 1, 5)
    asked = [q.question for b in blocks for q in b.questions or []]
    assert "Ma prochaine action" in asked  # a reflective label asks for a sentence, not a word
    assert "• Gardez ces questions sous les yeux." in [i for b in blocks if b.type == "paragraphs" for i in b.items]


def test_a_long_section_is_cut_into_balanced_pages():
    page = next(p for p in _layout().spec.pages if p.title == "Les questions à poser.")
    assert [b.type for b in page.blocks].count("page_break") == 1
    assert page.part_title == "Pendant l'échange"


def test_the_fallback_keeps_a_forbidden_word_and_the_check_flags_it():
    support = SUPPORT.replace("☐ Sur place", "☐ Présentiel")
    spec = gemini_service._build_fallback_layout(LayoutRequest(source_text=support)).spec
    assert ("à corriger", "presentiel") in {(f.level, f.rule) for f in check_spec(spec, structure=False)}
    assert check_coverage(spec, support).missing == []


def test_the_suggestions_are_instructions_for_iterate():
    suggestions = _layout().suggestions
    assert any("ouverture" in s for s in suggestions)
    assert any("exemple contrasté" in s for s in suggestions)
    assert any("livrable" in s for s in suggestions)


def test_the_frame_number_and_beneficiary_are_the_consultant_s():
    framed = _layout(frame=False, chapter_num=7, beneficiary_name="Camille", chapter_title="Mon enquête")
    spec = framed.spec
    assert {p.template for p in spec.pages} == {"composite"}
    assert spec.carnet == 7 and spec.beneficiary_name == "Camille" and spec.chapter_title == "Mon enquête"
    assert all(p.part_title is not None for p in spec.pages)  # never « 7. TITRE »


def test_the_template_completes_the_model_s_suggestions_on_the_topics_it_left_aside():
    template = gemini_service._layout_suggestions(_layout().spec)
    merged = gemini_service._merge_suggestions(["Ajoute une durée indicative en tête de document."], template)
    assert merged[0] == "Ajoute une durée indicative en tête de document."
    assert not any(s.startswith("Donne à chaque page un sourcil") for s in merged)  # durations: already said
    assert any("ouverture" in s for s in merged) and any("livrable" in s for s in merged)


# --- Coverage --------------------------------------------------------------------------

def _spec_with(*texts):
    return WorkbookSpec(pages=[{"template": "composite", "blocks": [
        {"type": "questions_group", "questions": [{"question": t, "field_id": f"q{k}"} for k, t in enumerate(texts)]}]}])


def test_typography_case_and_accents_are_no_loss():
    source = "QU'EST-CE QUI VOUS PLAÎT LE PLUS ?\nCE QUE JE SAIS DÉJÀ :"
    spec = _spec_with("Qu’est-ce qui vous plaît le plus ?", "Ce que je sais déjà")
    assert check_coverage(spec, source).found == 2
    assert normalize("« Cœur »") == normalize("COEUR")


def test_a_missing_or_reworded_element_is_reported():
    source = "Pouvez-vous décrire votre métier et vos missions principales ?\nQuel a été votre parcours ?"
    spec = _spec_with("Vos missions ?")
    coverage = check_coverage(spec, source)
    assert coverage.found == 0
    assert [m.text for m in coverage.missing] == [
        "Pouvez-vous décrire votre métier et vos missions principales ?", "Quel a été votre parcours ?"]


def test_a_forbidden_word_replaced_is_noted():
    source = "Comment se fait l'échange ?\nTéléphone\nPrésentiel"
    spec = WorkbookSpec(pages=[{"template": "composite", "blocks": [
        {"type": "checklist", "title": "Comment se fait l'échange ?", "items": ["Téléphone", "Sur place"]}]}])
    coverage = check_coverage(spec, source)
    assert (coverage.found, coverage.options_found, coverage.options_total) == (1, 1, 2)
    assert coverage.missing[0].kind == "option" and coverage.missing[0].of == "Comment se fait l'échange ?"
    assert "mot proscrit" in coverage.missing[0].note


def test_a_short_element_counts_as_whole_words_only():
    spec = _spec_with("Ma candidature", "Mon CDI actuel")
    assert check_coverage(spec, "CDI :").found == 1
    assert check_coverage(_spec_with("Ma candidature"), "CDI :").found == 0


def test_an_element_out_of_order_is_reported():
    source = "Quel a été votre parcours jusqu'ici ?\nComment se passe une semaine ordinaire ?"
    spec = _spec_with("Comment se passe une semaine ordinaire ?", "Quel a été votre parcours jusqu'ici ?")
    coverage = check_coverage(spec, source)
    assert coverage.found == 2 and coverage.out_of_order == ["Comment se passe une semaine ordinaire ?"]


# --- The API ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def fresh_gemini_clients():
    gemini_service._get_client.cache_clear()
    yield
    gemini_service._get_client.cache_clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_layout_without_a_key_is_the_faithful_fallback(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    r = client.post("/api/layout", json={"source_text": SUPPORT})
    assert r.status_code == 200
    assert r.headers["X-MDM-Generation"] == "fallback"
    body = r.json()
    assert body["spec"]["chapter_title"] == "Fiche d'entretien" and body["suggestions"]
    coverage = client.post("/api/coverage", json={"spec": body["spec"], "source_text": SUPPORT}).json()
    assert coverage["found"] == coverage["total"] == len(QUESTIONS_AND_LABELS)
    assert coverage["missing"] == [] and coverage["out_of_order"] == []


def test_layout_refuses_an_empty_support(client):
    r = client.post("/api/layout", json={"source_text": ""})
    assert r.status_code == 422
    assert "Texte du support" in r.json()["detail"]


def test_gemini_s_layout_takes_the_consultant_s_choices(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    answer = {"spec": {"chapter_title": "Fiche d'entretien", "folio": "Entretien", "pastel": "mint",
                       "beneficiary_name": "Inventé", "pages": [
        {"template": "cover", "params": {"cover_title": "Fiche *d'entretien.*", "promise": "Une promesse ajoutée."}},
        {"template": "composite", "title": "Préparer l'échange.", "blocks": [
            {"type": "question", "question": "Comment l'échange se fait-il ?", "field_id": "enq_q1"}]},
        {"template": "closing", "params": {"messages": ["Un message ajouté."]}},
    ]}, "changes_summary": "Capitales passées en minuscules.", "suggestions": []}
    prompts = []

    class Response:
        text = json.dumps(answer)

    class Models:
        def generate_content(self, **kwargs):
            prompts.append(kwargs)
            return Response

    class Client:
        def __init__(self, **kwargs):
            self.models = Models()

    monkeypatch.setattr(gemini_service.genai, "Client", Client)
    r = client.post("/api/layout", json={"source_text": SUPPORT})
    body = r.json()
    spec = body["spec"]

    assert r.headers["X-MDM-Generation"] == "ai"
    assert SUPPORT in prompts[0]["contents"] and "Bénéficiaire : non précisé" in prompts[0]["contents"]
    assert prompts[0]["config"].system_instruction == gemini_service.LAYOUT_SYSTEM_PROMPT
    assert "beneficiary_name" not in spec and spec["folio"] == "Entretien"
    assert spec["pages"][0]["params"] == {"cover_title": "Fiche *d'entretien.*", "number": ""}
    assert spec["pages"][-1]["params"] == {"messages": []}
    assert spec["pages"][1]["part_title"] == ""  # never « 1. TITRE »
    assert body["changes_summary"] == "Capitales passées en minuscules."
    assert body["suggestions"]  # Gemini gave none: the common template's
