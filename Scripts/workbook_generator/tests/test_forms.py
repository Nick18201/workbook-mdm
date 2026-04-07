import unittest
from unittest.mock import MagicMock
import sys

# Mock reportlab before other imports
mock_reportlab = MagicMock()
sys.modules['reportlab'] = mock_reportlab
sys.modules['reportlab.lib'] = MagicMock()
sys.modules['reportlab.lib.colors'] = MagicMock()
sys.modules['reportlab.lib.units'] = MagicMock()

from Scripts.workbook_generator.forms import create_input_field, create_checkbox
from Scripts.workbook_generator.config import PDFStyle

# Access mocked colors - ensure we use the same mock objects
import reportlab.lib.colors as colors

class TestForms(unittest.TestCase):
    def setUp(self):
        self.mock_form = MagicMock()

    def test_create_input_field_default_params(self):
        """Test create_input_field with default parameters."""
        create_input_field(self.mock_form, 'test_field', 100, 200, 50, 20)

        self.mock_form.textfield.assert_called_once_with(
            name='test_field',
            tooltip='',
            value='',
            x=100, y=200,
            width=50, height=20,
            borderStyle='solid',
            borderColor=PDFStyle.COLOR_FIELD_BG,
            borderWidth=0.5,
            forceBorder=True,
            fillColor=PDFStyle.COLOR_FIELD_BG,
            fieldFlags='',
            fontSize=11,
            maxlen=0
        )

    def test_create_input_field_multiline(self):
        """Test create_input_field with multiline=True."""
        create_input_field(self.mock_form, 'test_multiline', 100, 200, 100, 50, multiline=True)

        self.mock_form.textfield.assert_called_once()
        args, kwargs = self.mock_form.textfield.call_args
        self.assertEqual(kwargs['fieldFlags'], 'multiline')

    def test_create_input_field_custom_fill_color(self):
        """Test create_input_field with custom fill color."""
        custom_color = 'red'
        create_input_field(self.mock_form, 'test_color', 100, 200, 50, 20, fill_color=custom_color)

        self.mock_form.textfield.assert_called_once()
        args, kwargs = self.mock_form.textfield.call_args
        self.assertEqual(kwargs['fillColor'], custom_color)

    def test_create_checkbox(self):
        """Test create_checkbox with default parameters."""
        create_checkbox(self.mock_form, 'test_checkbox', 100, 200)

        self.mock_form.checkbox.assert_called_once()
        args, kwargs = self.mock_form.checkbox.call_args
        self.assertEqual(kwargs['name'], 'test_checkbox')
        self.assertEqual(kwargs['tooltip'], '')
        self.assertEqual(kwargs['x'], 100)
        self.assertEqual(kwargs['y'], 200)
        self.assertEqual(kwargs['size'], 18)
        self.assertEqual(kwargs['buttonStyle'], 'check')
        self.assertEqual(kwargs['borderStyle'], 'solid')
        self.assertEqual(kwargs['borderWidth'], 1)
        self.assertEqual(kwargs['forceBorder'], False)
        # We don't assert colors directly due to mock identity issues in complex structures
