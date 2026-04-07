from reportlab.lib import colors
from .config import PDFStyle

def create_input_field(form, name, pos, size, tooltip='', multiline=False, value='', fill_color=None):
    """Helper to create consistent input fields."""
    bg_color = fill_color if fill_color else PDFStyle.COLOR_FIELD_BG
    border_color = PDFStyle.COLOR_FIELD_BG
    
    x, y = pos
    width, height = size

    # Flags: 'multiline' allows multiple lines. 
    # 'doNotScroll' is NOT set, so it should scroll if text exceeds area.
    flags = 'multiline' if multiline else ''
    
    # Font Size: Use a fixed size to ensure it doesn't auto-scale to huge if empty, 
    # but small enough to fit lines. 
    # For multiline, 10 or 11 is good. 
    font_size = 11
    
    form.textfield(
        name=name,
        tooltip=tooltip,
        value=value, x=x, y=y, width=width, height=height,
        borderStyle='solid',
        borderColor=border_color,
        borderWidth=0.5,
        forceBorder=True,
        fillColor=bg_color,
        fieldFlags=flags,
        fontSize=font_size,
        maxlen=0
    )

def create_checkbox(form, name, pos, size=18, tooltip=''):
    """Helper to create consistent checkboxes."""
    x, y = pos
    form.checkbox(
        name=name,
        tooltip=tooltip,
        x=x, y=y,
        size=size,
        buttonStyle='check',
        borderStyle='solid',
        borderWidth=1,
        borderColor=colors.black,
        fillColor=colors.white,
        forceBorder=False
    )
