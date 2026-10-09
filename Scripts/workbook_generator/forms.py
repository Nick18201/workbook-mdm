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


def field_font_size(height, multiline):
    """
    Size of the text typed in a field `height` high: PDFStyle.SIZE_FIELD, smaller only in a
    one-line field too low for it. Never 0, the automatic size of PDF viewers: it shrinks the
    text as it grows, down to unreadable.
    """
    if multiline:
        return PDFStyle.SIZE_FIELD
    return max(6, min(PDFStyle.SIZE_FIELD, int(height - 4)))


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
    do_not_scroll=False,
    framed=True,
):
    """
    Text field typed in a fixed size (field_font_size). A full field scrolls: viewers draw
    no scroll bar, and Chrome ignores do_not_scroll anyway, so a box is sized for the answer
    it expects (components.answer_height). framed=True: the widget draws its own white box
    with a `line-strong` border. framed=False: a transparent, borderless widget, to lay over
    a box drawn on the page (primitives.draw_field_box, rounded like the art direction).
    Form fields always use page coordinates: canvas translations and rotations do not apply.
    """
    x, y = pos
    width, height = size

    flag_parts = []
    if multiline:
        flag_parts.append("multiline")
    if do_not_scroll:
        flag_parts.append("doNotScroll")
    flags = " ".join(flag_parts)

    if font_size is None:
        font_size = field_font_size(height, multiline)

    if framed:
        frame = dict(
            borderStyle="solid",
            borderColor=PDFStyle.COLOR_LINE_STRONG,
            borderWidth=0.75,
            forceBorder=True,
            fillColor=fill_color if fill_color else PDFStyle.COLOR_SURFACE_CARD,
        )
    else:
        frame = dict(borderColor=None, borderWidth=0, fillColor=None)

    form.textfield(
        name=reserve_field_name(form, name),
        tooltip=tooltip,
        value=value,
        x=x,
        y=y,
        width=width,
        height=height,
        textColor=PDFStyle.COLOR_INK,
        fieldFlags=flags,
        fontSize=font_size,
        maxlen=0,
        **frame,
    )


def create_radio(form, group, value, pos, size=10, tooltip="", framed=True):
    """
    Adds one option to a radio group: every button created with the same `group` is
    mutually exclusive. Reserve the group name once with reserve_field_name() (not per button).
    Unlike ReportLab's default flags, the choice can be cleared by clicking it again.
    framed=False leaves out the circle, for a button laid over a disc drawn on the page.
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
        borderWidth=1 if framed else 0,
        borderColor=PDFStyle.COLOR_LINE_STRONG if framed else None,
        fillColor=PDFStyle.COLOR_SURFACE_CARD if framed else None,
        textColor=PDFStyle.COLOR_BLUE,
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
        borderColor=PDFStyle.COLOR_LINE_STRONG,
        fillColor=PDFStyle.COLOR_SURFACE_CARD,
        textColor=PDFStyle.COLOR_BLUE,
        forceBorder=False,
    )
