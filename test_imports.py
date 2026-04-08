import sys
from unittest.mock import MagicMock

# Create a mock that acts like a package
class MockPackage(MagicMock):
    __path__ = []

sys.modules['reportlab'] = MockPackage()
sys.modules['reportlab.pdfgen'] = MagicMock()
sys.modules['reportlab.lib'] = MockPackage()
sys.modules['reportlab.lib.pagesizes'] = MagicMock()
sys.modules['reportlab.lib.colors'] = MagicMock()
sys.modules['reportlab.lib.units'] = MagicMock()
sys.modules['reportlab.lib.utils'] = MagicMock()
sys.modules['reportlab.pdfbase'] = MockPackage()
sys.modules['reportlab.pdfbase.pdfmetrics'] = MagicMock()
sys.modules['reportlab.pdfbase.ttfonts'] = MagicMock()
sys.modules['reportlab.platypus'] = MagicMock()

import Scripts.main_generate_chap0
import Scripts.main_generate_chap1
import Scripts.main_generate_chap2
import Scripts.main_generate_chap3
import Scripts.main_generate_livret

print("All scripts imported successfully.")
