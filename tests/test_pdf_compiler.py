import pymupdf

from server.models import BlockSpec, PageSpec, WorkbookSpec
from workbook_generator.compiler import compile_workbook_from_spec
from workbook_generator.config import PDFStyle
from server.predefined_workbooks import get_predefined_spec

CM = 72 / 2.54


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


def test_table_answer_fields_take_several_lines_when_tall_enough():
    def table(prefix, **kwargs):
        return BlockSpec(type="table", headers=["Hypothèse", "Ce que je crois"], field_prefix=prefix,
                         rows=[["Hypothèse 1", {"field_id": f"{prefix}_croyance"}]], **kwargs)

    page = _open(WorkbookSpec(pages=[PageSpec(template="composite", title="Tableaux", blocks=[
        table("haute", field_height_cm=2.0), table("basse"),
    ])]))[0]
    fields = {w.field_name: w for w in page.widgets()}

    assert fields["haute_croyance"].rect.height > 2 * fields["basse_croyance"].rect.height
    assert fields["haute_croyance"].field_flags & pymupdf.PDF_TX_FIELD_IS_MULTILINE
    assert not fields["basse_croyance"].field_flags & pymupdf.PDF_TX_FIELD_IS_MULTILINE


def test_answers_are_typed_in_a_fixed_size():
    """
    Never the automatic size (0) of PDF viewers, which shrinks a long answer down to
    unreadable; a full box scrolls rather than refusing the text.
    """
    templates = ("questions", "meteo", "quadrants", "two_columns", "enquete", "roadmap", "engagement")
    doc = _open(WorkbookSpec(pages=[PageSpec(template=t, title=t) for t in templates]))
    fields = [w for page in doc for w in page.widgets() if w.field_type == pymupdf.PDF_WIDGET_TYPE_TEXT]

    assert fields
    for w in fields:
        assert 0 < w.text_fontsize <= PDFStyle.SIZE_FIELD, w.field_name
        assert not w.field_flags & pymupdf.PDF_TX_FIELD_IS_DO_NOT_SCROLL, w.field_name


def test_answer_boxes_are_sized_for_the_answer_they_expect():
    page = _open(WorkbookSpec(pages=[PageSpec(template="composite", title="Tailles", blocks=[
        BlockSpec(type="question", question="Q1 ?", field_id="phrase", answer="phrase"),  # its French name
        BlockSpec(type="question", question="Q2 ?", field_id="paragraphe", answer="paragraph"),
        BlockSpec(type="fields_card", rows=[
            [["Pleine largeur", "pleine", "sentence"]],
            [["Demi-largeur", "demi", "sentence"], ["Un mot", "mot", "word"]],
        ]),
    ])]))[0]
    fields = {w.field_name: w for w in page.widgets()}
    height = {name: w.rect.height + 6 for name, w in fields.items()}  # the drawn box

    assert height["paragraphe"] > height["phrase"] >= 1.6 * CM - 0.5  # two handwritten lines at least
    assert height["demi"] > height["pleine"]  # a narrower box takes more lines
    assert not fields["mot"].field_flags & pymupdf.PDF_TX_FIELD_IS_MULTILINE


def test_a_table_row_takes_the_tallest_answer_of_its_cells():
    """A first name in a row of sentences is a word: it never sets the height of the row."""
    def table(prefix, name_answer):
        return BlockSpec(type="table", headers=["Prénom", "Ce que je lui demande"], answer="sentence",
                         col_widths_cm=[3.0, 14.0], rows=[[{"field_id": f"{prefix}_prenom", "answer": name_answer},
                                                            {"field_id": f"{prefix}_demande"}]])

    page = _open(WorkbookSpec(pages=[PageSpec(template="composite", title="Tableaux", blocks=[
        table("mot", "mot"), table("phrase", "sentence"),  # « mot » is the French name of 'word'
    ])]))[0]
    fields = {w.field_name: w for w in page.widgets()}

    assert fields["mot_demande"].rect.height == fields["mot_prenom"].rect.height  # one row, one height
    assert fields["phrase_prenom"].rect.height > 2 * fields["mot_prenom"].rect.height  # a sentence in 3 cm
    assert fields["mot_demande"].rect.height + 6 >= 1.6 * CM - 0.5
    assert fields["mot_demande"].field_flags & pymupdf.PDF_TX_FIELD_IS_MULTILINE


def test_a_questions_group_never_shrinks_a_box_below_its_minimum():
    """A question that would get less than min_box_height_cm continues on the next page."""
    questions = [{"question": f"Question {i} ?", "field_id": f"q{i}"} for i in range(8)]
    doc = _open(WorkbookSpec(pages=[PageSpec(template="composite", title="Groupe", blocks=[
        BlockSpec(type="questions_group", questions=questions, min_box_height_cm=3.0, max_box_height_cm=4.0),
    ])]))
    heights = [w.rect.height + 6 for page in doc for w in page.widgets()]

    assert len(heights) == 8 and doc.page_count == 2
    assert min(heights) >= 3.0 * CM - 0.5


def test_cards_fit_the_answer_they_expect():
    def grid(prefix, **kwargs):
        return BlockSpec(type="cards_grid", columns=2, field_prefix=prefix,
                         cards=[{"title": "Le cadre", "field_id": f"{prefix}_a"},
                                {"title": "Le test", "field_id": f"{prefix}_b"}], **kwargs)

    page = _open(WorkbookSpec(pages=[PageSpec(template="composite", title="Cartes", blocks=[
        grid("phrase", answer="sentence"), grid("basse", card_height_cm=3.0, answer="paragraph"),
    ])]))[0]
    height = {w.field_name: w.rect.height + 6 for w in page.widgets()}

    assert abs(height["phrase_a"] - 2.15 * CM) < 0.1 * CM  # a sentence in half the width
    assert height["basse_a"] > 4 * CM  # card_height_cm is only a minimum


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
