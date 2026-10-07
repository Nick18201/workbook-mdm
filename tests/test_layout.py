import pymupdf

from server.models import BlockSpec, PageSpec, WorkbookSpec
from server.pdf_compiler import compile_workbook_from_spec
from workbook_generator.utils import strip_unsupported_glyphs

CM = 28.3465
LONG = (
    "Décrivez précisément les situations concrètes vécues au quotidien, "
    "les irritants et les contournements mis en place par les équipes"
)


def _open(*pages):
    return pymupdf.open(stream=compile_workbook_from_spec(WorkbookSpec(pages=list(pages))), filetype="pdf")


def _page_titles(doc):
    """The large text of each page: the title, whose accent word is a span of its own."""
    titles = []
    for p in doc:
        lines = [
            "".join(s["text"] for s in l["spans"] if s["size"] > 18)
            for b in p.get_text("dict")["blocks"] for l in b.get("lines", [])
        ]
        titles.append(" ".join(" ".join(line for line in lines if line.strip()).split()))
    return titles


def _assert_nothing_off_page(doc):
    for page in doc:
        width, height = page.rect.width, page.rect.height
        for w in page.widgets():
            assert w.rect.y1 <= height - 1.6 * CM, (page.number, w.field_name)
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if span["text"].strip():
                        assert span["bbox"][2] <= width - 0.3 * CM, (page.number, span["text"])


def test_overflowing_content_continues_on_new_pages():
    doc = _open(
        PageSpec(template="questions", title="Questions", params={
            "questions": [{"question": f"Question {i} : {LONG} ?", "subtitle": LONG, "example": "Animer"} for i in range(1, 8)]
        }),
        PageSpec(template="two_columns", title="Colonnes", params={
            "col1_header": "Ce que j'imaginais au tout début (Fantasme / Crainte profonde)",
            "col2_header": "Ce que le terrain révèle vraiment (Réalité éprouvée sur place)",
            "rows": [{"label": f"{i}. {LONG}"} for i in range(1, 11)],
        }),
        PageSpec(template="enquete", title="Enquête", params={
            "questions": [{"title": f"{i}. Besoins", "subtitle": LONG + " " + LONG} for i in range(1, 7)]
        }),
        PageSpec(template="quadrants", title="Piliers", params={
            "instruction": LONG + " " + LONG,
            "quadrants": [{"title": f"Pilier {i} : un titre beaucoup trop long pour une pastille", "subtitle": LONG} for i in range(1, 7)],
        }),
        PageSpec(template="composite", title="Composite", blocks=[
            BlockSpec(type="table", headers=["Critère", "Niveau", "Parade"], rows=[["Finances", "Modéré", LONG]] * 14),
            BlockSpec(type="checklist", items=[f"Critère {i} {LONG}" for i in range(10)], columns=2),
            BlockSpec(type="scale", label=LONG + " ?"),
        ]),
    )

    titles = _page_titles(doc)
    for title in ("Questions", "Colonnes", "Enquête", "Piliers", "Composite"):
        assert title in titles and f"{title} (suite)" in titles
    _assert_nothing_off_page(doc)

    text = "".join(page.get_text() for page in doc)
    assert all(f"Question {i} :" in text for i in range(1, 8))
    two_columns_fields = [w for p in doc for w in p.widgets() if "_twocol_" in w.field_name]
    assert len(two_columns_fields) == 20


def test_roadmap_keeps_every_action_and_accepts_a_single_string():
    doc = _open(PageSpec(template="roadmap", title="Feuille de route", params={"stages": [
        {"period": "PALIER 1", "actions": ["A1", "A2", "A3", "A4", "A5"]},
        {"period": "PALIER 2", "actions": "Une seule action"},
    ]}))

    actions = {w.field_name: w.field_value for p in doc for w in p.widgets() if "_act_" in w.field_name}
    assert sorted(v for k, v in actions.items() if "_s1_" in k) == ["A1", "A2", "A3", "A4", "A5"]
    assert [v for k, v in actions.items() if "_s2_" in k] == ["Une seule action"]
    _assert_nothing_off_page(doc)


def test_scales_are_single_choice_radio_groups():
    doc = _open(
        PageSpec(template="meteo", title="Météo"),
        PageSpec(template="composite", title="Échelle", blocks=[BlockSpec(type="scale", label="Note", min_val=0, max_val=10)]),
    )

    for page in doc:
        radios = [w for w in page.widgets() if w.field_type == pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON]
        assert len(radios) == 11
        assert len({w.field_name for w in radios}) == 1  # one group: choosing a level clears the others
        assert sorted(int(w.on_state()) for w in radios) == list(range(11))


def test_pictograms_are_drawn_with_the_icon_font():
    doc = _open(
        PageSpec(template="meteo", title="Météo"),  # weather icons
        PageSpec(template="engagement", title="Engagement", params={"lines": ["Je m'engage"]}),  # stamp check mark
    )

    for page in doc:
        fonts = {s["font"] for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]}
        assert any(f.startswith("MaterialSymbolsOutlined") for f in fonts), fonts
        assert "ZapfDingbats" not in fonts


def test_spec_emojis_are_removed_without_leaving_gaps():
    doc = _open(PageSpec(template="questions", title="Mes questions 🎯", params={
        "questions": [{"question": "✅ Quelle est votre priorité ?", "example": "Lancer mon activité 🚀"}]
    }))

    text = doc[0].get_text()
    assert "Mes questions\n" in text
    assert "Quelle est votre priorité ?" in text
    assert "Exemple : Lancer mon activité\n" in text


def test_strip_unsupported_glyphs():
    assert strip_unsupported_glyphs("Soleil ☀️ et nuages") == "Soleil et nuages"
    assert strip_unsupported_glyphs("🎯 Objectif") == "Objectif"
    # Accents, typographic quotes and symbols the title, body and label fonts all have are kept as is
    assert strip_unsupported_glyphs("Être « sûr » · 1 800 € → œ") == "Être « sûr » · 1 800 € → œ"
    # Shapes the art direction fonts lack are dropped (pictograms are drawn as icons instead)
    assert strip_unsupported_glyphs("Avant ◀ ▶ après ✓") == "Avant après"
