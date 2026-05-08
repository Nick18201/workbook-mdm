import sys
from unittest.mock import MagicMock

class MockModule(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__path__ = []
        self.__spec__ = MagicMock()

# Create the main mock structure
reportlab = MockModule()
lib = MockModule()
colors = MockModule()
units = MockModule()

# Link them to ensure consistency between 'import reportlab.lib.colors'
# and 'from reportlab.lib import colors'
reportlab.lib = lib
lib.colors = colors
lib.units = units

# Configure sys.modules
sys.modules['reportlab'] = reportlab
sys.modules['reportlab.lib'] = lib
sys.modules['reportlab.lib.colors'] = colors
sys.modules['reportlab.lib.units'] = units

# Specific configurations for mocks to facilitate testing
colors.HexColor = lambda x: x
units.cm = 1.0

# Mock other submodules
other_submodules = [
    'reportlab.rl_config',
    'reportlab.pdfgen',
    'reportlab.pdfgen.canvas',
    'reportlab.lib.pagesizes',
    'reportlab.lib.utils',
    'reportlab.lib.styles',
    'reportlab.lib.enums',
    'reportlab.pdfbase',
    'reportlab.pdfbase.pdfmetrics',
    'reportlab.pdfbase.ttfonts',
    'reportlab.platypus',
]

for mod_name in other_submodules:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = MockModule()
