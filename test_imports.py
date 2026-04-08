import sys
import os
from unittest.mock import MagicMock

# Add Scripts directory to path so workbook_generator can be found by the imported modules
sys.path.append(os.path.join(os.path.dirname(__file__), "Scripts"))

# We mock all required submodules to satisfy the imports without having reportlab installed
class MockModule(MagicMock):
    __path__ = []

sys.modules['reportlab'] = MockModule()
sys.modules['reportlab.pdfgen'] = MockModule()
sys.modules['reportlab.lib'] = MockModule()
sys.modules['reportlab.lib.pagesizes'] = MockModule()
sys.modules['reportlab.lib.colors'] = MockModule()
sys.modules['reportlab.lib.units'] = MockModule()
sys.modules['reportlab.lib.utils'] = MockModule()
sys.modules['reportlab.lib.styles'] = MockModule()
sys.modules['reportlab.lib.enums'] = MockModule()
sys.modules['reportlab.pdfbase'] = MockModule()
sys.modules['reportlab.pdfbase.pdfmetrics'] = MockModule()
sys.modules['reportlab.pdfbase.ttfonts'] = MockModule()
sys.modules['reportlab.platypus'] = MockModule()

# Import the actual scripts to ensure syntax and structure is correct
import Scripts.main_generate_chap0
import Scripts.main_generate_chap1
import Scripts.main_generate_chap2
import Scripts.main_generate_chap3
import Scripts.main_generate_livret

print("All scripts imported successfully.")
