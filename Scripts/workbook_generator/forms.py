from reportlab.lib import colors
from .config import PDFStyle


def reserve_field_name(form, name):
    """
    Returns a field name not yet used in this document. PDF viewers link widgets that
    share a name (typing in one fills the other), so a repeated name gets a numeric suffix.
    Dots are replaced because they denote parent/child fields in AcroForm names.
    """
    used = getattr(form, "_mdm_field_names", None)
    if used is None:
        used = form._mdm_field_names = set()

    base = str(name).replace(".", "_")
    unique, n = base, 2
    while unique in used:
        unique = f"{base}_{n}"
        n += 1
    used.add(unique)
    return unique


def create_input_field(
    form,
    name,
    pos,
    size,
    tooltip="",
    multiline=False,
    value="",
    fill_color=None,
    font_size=None,
    do_not_scroll=True,
):
    """Helper to create consistent input fields with auto-scaling font size."""
    bg_color = fill_color if fill_color else PDFStyle.COLOR_FIELD_BG
    border_color = PDFStyle.COLOR_FIELD_BG

    x, y = pos
    width, height = size

    flag_parts = []
    if multiline:
        flag_parts.append("multiline")
    if do_not_scroll:
        flag_parts.append("doNotScroll")
    flags = " ".join(flag_parts)

    # Font Size:
    # If font_size is None, use 0 (Auto/Fit) for multiline fields.
    # In the PDF standard, fontSize=0 instructs the PDF viewer to scale down
    # text dynamically to fit the bounding box without triggering scrollbars.
    # For single-line fields, use 0 if standard height (<= 28 pt), or 11 pt if tall.
    if font_size is None:
        if multiline:
            font_size = 0
        else:
            font_size = 0 if height <= 28 else 11

    form.textfield(
        name=reserve_field_name(form, name),
        tooltip=tooltip,
        value=value,
        x=x,
        y=y,
        width=width,
        height=height,
        borderStyle="solid",
        borderColor=border_color,
        borderWidth=0.5,
        forceBorder=True,
        fillColor=bg_color,
        fieldFlags=flags,
        fontSize=font_size,
        maxlen=0,
    )


def create_radio(form, group, value, pos, size=10, tooltip=""):
    """
    Adds one option to a radio group: every button created with the same `group` is
    mutually exclusive. Reserve the group name once with reserve_field_name() (not per button).
    Unlike ReportLab's default flags, the choice can be cleared by clicking it again.
    """
    x, y = pos
    form.radio(
        name=group,
        value=str(value),
        selected=False,
        tooltip=tooltip,
        x=x,
        y=y,
        size=size,
        buttonStyle="circle",
        shape="circle",
        borderStyle="solid",
        borderWidth=1,
        borderColor=colors.black,
        fillColor=colors.white,
        textColor=colors.black,
        forceBorder=False,
        fieldFlags="radio",
    )


def create_checkbox(form, name, pos, size=18, tooltip=""):
    """Helper to create consistent checkboxes."""
    x, y = pos
    form.checkbox(
        name=reserve_field_name(form, name),
        tooltip=tooltip,
        x=x,
        y=y,
        size=size,
        buttonStyle="check",
        borderStyle="solid",
        borderWidth=1,
        borderColor=colors.black,
        fillColor=colors.white,
        forceBorder=False,
    )
