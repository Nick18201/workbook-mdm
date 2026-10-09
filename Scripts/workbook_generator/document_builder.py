import os
from dataclasses import dataclass, field
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.rl_accel import fp_str
from .config import PDFStyle
from .utils import register_fonts


@dataclass
class DocumentStyle:
    """Per-document settings, kept on the canvas (not on PDFStyle) so that concurrent builds stay apart."""
    pastel: str = PDFStyle.DEFAULT_PASTEL
    folio: str = ""  # e.g. "carnet 3/7" or a short title; the page number is added after it
    carnet: object = None  # 1 to 7 or PDFStyle.CARNET_ROUTE for a carnet of the bilan, else None
    # Pages of PageLayout as (page number, share of the page height their content uses, True
    # on a « (suite) » page): a continuation that holds one small block is a layout to fix
    page_fills: list = field(default_factory=list)


def document_style(c):
    """The DocumentStyle of the document this canvas belongs to (defaults for a bare canvas)."""
    return getattr(c, "_mdm_style", None) or DocumentStyle()


def document_pastel(c):
    """The dominant pastel color of the document."""
    name = document_style(c).pastel
    return PDFStyle.PASTELS.get(name, PDFStyle.PASTELS[PDFStyle.DEFAULT_PASTEL])


def carnet_folio(carnet):
    """Folio of a carnet of the bilan: « carnet 3/7 » or « carnet de route »."""
    if carnet == PDFStyle.CARNET_ROUTE:
        return "carnet de route"
    return f"carnet {carnet}/{PDFStyle.CARNET_COUNT}"


def carnet_eyebrow(c, number=None):
    """
    Eyebrow of a cover or an opener: « Carnet de route » for the carnet de route,
    « Carnet de bord · carnet N » for a numbered document, « Carnet de bord » otherwise.
    """
    carnet = document_style(c).carnet
    if carnet == PDFStyle.CARNET_ROUTE:
        return "Carnet de route"
    if number in (None, "") and carnet is not None:
        number = carnet
    return f"Carnet de bord · carnet {number}" if number not in (None, "") else "Carnet de bord"


class _PageCanvas(canvas.Canvas):
    """
    Canvas whose pages are tinted with PDFStyle.COLOR_PAGE (warm ivory): the tint is
    put at the very start of each page's content when the page ends, so it stays under
    everything and an unused last page is not created by it.
    """

    def showPage(self):
        color = PDFStyle.COLOR_PAGE
        if color is not None:
            w, h = self._pagesize
            self._code.insert(0, f"q {fp_str(color.red, color.green, color.blue)} rg 0 0 {fp_str(w, h)} re f Q")
        super().showPage()


class DocumentBuilder:
    """
    Orchestrates the creation and setup of a PDF workbook.
    Handles font registration, file permission checks, and the fluid chaining of pages.

    carnet: a carnet of the bilan, 1 to 7 or "route" (PDFStyle.CARNET_ROUTE), which sets its
    pastel and the folio « carnet N/7 » or « carnet de route ». Otherwise pastel is a
    PDFStyle.PASTELS key (lilac by default) and folio what the page footer shows between
    the brand and the page number (a short title).
    """
    def __init__(self, output_path, pastel=None, folio="", carnet=None):
        self.output_path = output_path
        if carnet not in PDFStyle.CARNET_PASTELS:
            carnet = None
        if carnet is not None:
            pastel = pastel or PDFStyle.CARNET_PASTELS[carnet]
            folio = folio or carnet_folio(carnet)

        # Register fonts automatically
        register_fonts()

        # Fail-fast on permission errors (e.g., file open in another program)
        if isinstance(self.output_path, (str, bytes, os.PathLike)) and os.path.exists(self.output_path):
            try:
                os.remove(self.output_path)
            except PermissionError as e:
                raise PermissionError(
                    f"Cannot overwrite '{self.output_path}'. Please close the PDF if it is open in another program."
                ) from e

        # Instantiate the canvas
        self.canvas = _PageCanvas(self.output_path, pagesize=A4, lang=PDFStyle.PDF_LANG)
        self.canvas._mdm_style = DocumentStyle(
            pastel=pastel if pastel in PDFStyle.PASTELS else PDFStyle.DEFAULT_PASTEL,
            folio=folio or "",
            carnet=carnet,
        )

    def set_title(self, title):
        """Sets the metadata title of the PDF document."""
        self.canvas.setTitle(title)

    def add_page(self, page_func, *args, **kwargs):
        """
        Executes a page creation function, automatically injecting the canvas.

        Args:
            page_func (callable): A function that draws a page and takes a canvas as its first argument.
        """
        page_func(self.canvas, *args, **kwargs)

    def next_page(self):
        """
        Ends the current page and moves to a new one.
        Resets the canvas context.
        """
        self.canvas.showPage()

    def save(self):
        """Saves the PDF document to disk and prints a success message."""
        self.canvas.save()
        print(f"PDF generated successfully: {self.output_path}")
