import os
import sys

sys.path.insert(0, os.path.abspath("."))

from server.models import ParseRequest
from server.gemini_service import _build_fallback_spec
from server.pdf_compiler import compile_workbook_from_spec

SAMPLE_NOTES = """
Thème : Chapitre 4 - Les Valeurs & Limites professionnelles.
Bénéficiaire : Julien, manager en transition.

Notes de la séance :
- Intro : Julien ressent un épuisement lié à son incapacité à dire non aux demandes urgentes.
- Exercice 1 : Météo de départ. Julien arrive à 4/10 d'énergie, dispersé et sous pression.
- Exercice 2 : Les 4 Piliers de Vie (Pro, Perso, Social, Cadre).
- Exercice 3 : Passerelle Freins vers Leviers.
- Exercice 4 : 2 Questions de recul.
- Clôture : Pacte d'engagement sur 15 jours + signature.
"""

def test_formats():
    print("=== Testing Format Page Counts ===")
    
    # 1. Format Court (6 - 7 pages)
    req_short = ParseRequest(
        raw_notes=SAMPLE_NOTES,
        chapter_num=4,
        chapter_title="Format Court Test",
        theme="indigo",
        beneficiary_name="Julien",
        meteo_option="classic",
        book_format="short",
        include_engagement=True
    )
    spec_short = _build_fallback_spec(req_short)
    n_short = len(spec_short.pages)
    print(f"[SHORT] Generated {n_short} pages (expected: 6-7)")
    assert 6 <= n_short <= 7, f"Short format should have 6-7 pages, got {n_short}"
    pdf_short = compile_workbook_from_spec(spec_short)
    assert len(pdf_short) > 10000, "PDF should compile"
    print(f"  -> PDF compiled: {len(pdf_short)} bytes")

    # 1b. Format Court sans météo (6 pages)
    req_short_no_meteo = ParseRequest(
        raw_notes=SAMPLE_NOTES,
        chapter_num=4,
        chapter_title="Format Court Sans Meteo",
        theme="indigo",
        beneficiary_name="Julien",
        meteo_option="none",
        book_format="short",
        include_engagement=True
    )
    spec_short_no_meteo = _build_fallback_spec(req_short_no_meteo)
    n_short_no_meteo = len(spec_short_no_meteo.pages)
    print(f"[SHORT NO METEO] Generated {n_short_no_meteo} pages (expected: 6-7)")
    assert 6 <= n_short_no_meteo <= 7, f"Short no-meteo should have 6-7 pages, got {n_short_no_meteo}"
    pdf_short_no_meteo = compile_workbook_from_spec(spec_short_no_meteo)
    assert len(pdf_short_no_meteo) > 10000

    # 2. Format Standard (7 - 10 pages)
    req_std = ParseRequest(
        raw_notes=SAMPLE_NOTES,
        chapter_num=4,
        chapter_title="Format Standard Test",
        theme="indigo",
        beneficiary_name="Julien",
        meteo_option="classic",
        book_format="standard",
        include_engagement=True
    )
    spec_std = _build_fallback_spec(req_std)
    n_std = len(spec_std.pages)
    print(f"[STANDARD] Generated {n_std} pages (expected: 7-10)")
    assert 7 <= n_std <= 10, f"Standard format should have 7-10 pages, got {n_std}"
    pdf_std = compile_workbook_from_spec(spec_std)
    assert len(pdf_std) > 10000
    print(f"  -> PDF compiled: {len(pdf_std)} bytes")

    # 3. Format Complet (+ de 10 pages)
    req_deep = ParseRequest(
        raw_notes=SAMPLE_NOTES,
        chapter_num=4,
        chapter_title="Format Complet Test",
        theme="earth",
        beneficiary_name="Julien",
        meteo_option="classic",
        book_format="deep",
        include_engagement=True
    )
    spec_deep = _build_fallback_spec(req_deep)
    n_deep = len(spec_deep.pages)
    print(f"[DEEP] Generated {n_deep} pages (expected: > 10)")
    assert n_deep > 10, f"Deep format should have > 10 pages, got {n_deep}"
    for i, p in enumerate(spec_deep.pages):
        print(f"   p.{i+1}: template={p.template}, title='{p.title}'")
    pdf_deep = compile_workbook_from_spec(spec_deep)
    assert len(pdf_deep) > 10000
    print(f"  -> PDF compiled: {len(pdf_deep)} bytes")

    print("\n[SUCCESS] All format page counts verified perfectly!")

if __name__ == "__main__":
    test_formats()
