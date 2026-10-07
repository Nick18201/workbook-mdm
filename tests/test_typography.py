import pytest

from workbook_generator.primitives import title_runs, wrap_text
from workbook_generator.utils import NBSP, cached_simpleSplit, french_typography, split_words


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Consigne: notez ; puis relisez !", f"Consigne{NBSP}: notez{NBSP}; puis relisez{NBSP}!"),
        ("Quel est votre objectif?", f"Quel est votre objectif{NBSP}?"),
        ('Il dit "je change" puis « pars ».', f"Il dit «{NBSP}je change{NBSP}» puis «{NBSP}pars{NBSP}»."),
        ("“Prenez de la marge”", f"«{NBSP}Prenez de la marge{NBSP}»"),
        ("93 questions, 1 800 € et 10 %", f"93{NBSP}questions, 1{NBSP}800{NBSP}€ et 10{NBSP}%"),
        ("Le coeur de l'oeuvre, un oeil. COEUR.", "Le cœur de l'œuvre, un œil. CŒUR."),
        ("Profil MBTI et MBTI®", "Profil MBTI® et MBTI®"),
    ],
)
def test_french_typography(text, expected):
    assert french_typography(text) == expected
    assert french_typography(expected) == expected  # idempotent


@pytest.mark.parametrize(
    "text",
    [
        "Rendez-vous à 10:30, puis https://www.notion.so/page?x=1",
        "contact@margedemanoeuvre.fr et margedemanoeuvre.fr",
        "MARGEDEMANOEUVRE.FR · CONTACT@MARGEDEMANOEUVRE.FR",
        '<font color="#C22626">texte</font> &amp; <a href="https://x.fr/a?b">lien</a>',
    ],
)
def test_french_typography_leaves_times_urls_and_markup_alone(text):
    assert french_typography(text) == text


def test_french_typography_in_markup_only_touches_the_text():
    assert french_typography("<b>Exemple:</b> oui!") == f"<b>Exemple{NBSP}:</b> oui{NBSP}!"


def test_no_break_spaces_never_break_a_line():
    text = french_typography("Quel est votre objectif ? Notez 8 domaines et 1 800 € par mois.")
    assert split_words(text)[3] == f"objectif{NBSP}?"
    for lines in (cached_simpleSplit(text, "Helvetica", 10, 80), wrap_text(text, "Helvetica", 10, 80, tracking=0.1)):
        assert len(lines) > 2
        assert not any(line.endswith(("objectif", "1", "8")) for line in lines)
        assert all(not line.startswith(("?", "domaines", "€")) for line in lines)


def test_title_accent_keeps_its_punctuation():
    assert title_runs("Prenez de la marge !")[-1] == (f"marge{NBSP}!", True)
