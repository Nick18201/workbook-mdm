import os
from dataclasses import dataclass
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .config import PDFStyle
from .utils import register_fonts


@dataclass
class DocumentStyle:
    """Per-document settings, kept on the canvas (not on PDFStyle) so that concurrent builds stay apart."""
    pastel: str = PDFStyle.DEFAULT_PASTEL
    folio: str = ""  # e.g. "carnet 3/7" or a short title; the page number is added after it


def document_style(c):
    """The DocumentStyle of the document this canvas belongs to (defaults for a bare canvas)."""
    return getattr(c, "_mdm_style", None) or DocumentStyle()


def document_pastel(c):
    """The dominant pastel color of the document."""
    name = document_style(c).pastel
    return PDFStyle.PASTELS.get(name, PDFStyle.PASTELS[PDFStyle.DEFAULT_PASTEL])


class DocumentBuilder:
    """
    Orchestrates the creation and setup of a PDF workbook.
    Handles font registration, file permission checks, and the fluid chaining of pages.

    carnet: number of a core workbook (0 to 6), which sets its pastel and the folio
    "carnet N/7". Otherwise pastel is a PDFStyle.PASTELS key (lilac by default) and folio
    what the page footer shows between the brand and the page number (a short title).
    """
    def __init__(self, output_path, pastel=None, folio="", carnet=None):
        self.output_path = output_path
        if carnet in PDFStyle.CARNET_PASTELS:
            pastel = pastel or PDFStyle.CARNET_PASTELS[carnet]
            folio = folio or f"carnet {carnet}/{len(PDFStyle.CARNET_PASTELS)}"

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
        self.canvas = canvas.Canvas(self.output_path, pagesize=A4)
        self.canvas._mdm_style = DocumentStyle(
            pastel=pastel if pastel in PDFStyle.PASTELS else PDFStyle.DEFAULT_PASTEL,
            folio=folio or "",
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
