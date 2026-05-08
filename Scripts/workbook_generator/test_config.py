import pytest
from workbook_generator.config import PDFStyle

def test_set_theme_indigo():
    """Test setting the theme to indigo (default)."""
    PDFStyle.set_theme("indigo")
    assert PDFStyle.COLOR_BG_NUDE == "#FFF0E6"
    assert PDFStyle.COLOR_ACCENT_BLUE == "#2F2EFA"
    assert PDFStyle.COLOR_TEXT_MAIN == "#2F2EFA"

def test_set_theme_earth():
    """Test setting the theme to earth."""
    PDFStyle.set_theme("earth")
    assert PDFStyle.COLOR_BG_NUDE == "#FFFCE8"
    assert PDFStyle.COLOR_ACCENT_BLUE == "#D19B8D"
    assert PDFStyle.COLOR_TEXT_MAIN == "#8D6257"

def test_set_theme_default():
    """Test that set_theme defaults to indigo if no argument is provided."""
    PDFStyle.set_theme()
    assert PDFStyle.COLOR_BG_NUDE == "#FFF0E6"

def test_set_theme_unknown():
    """Test that set_theme defaults to indigo for an unknown theme."""
    PDFStyle.set_theme("unknown_theme")
    assert PDFStyle.COLOR_BG_NUDE == "#FFF0E6"
