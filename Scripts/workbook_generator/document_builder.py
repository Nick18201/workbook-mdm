import os
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .config import PDFStyle
from .utils import register_fonts

class DocumentBuilder:
    """
    Orchestrates the creation and setup of a PDF workbook.
    Handles theme initialization, font registration, file permission checks,
    and the fluid chaining of pages.
    """
    def __init__(self, output_path, theme="indigo"):
        self.output_path = output_path

        # Set the theme globally
        PDFStyle.set_theme(theme)

        # Register fonts automatically
        register_fonts()

        # Fail-fast on permission errors (e.g., file open in another program)
        if os.path.isfile(self.output_path):
            try:
                # Attempt to open in append mode to check for locks without truncating
                with open(self.output_path, 'ab'):
                    pass
            except PermissionError:
            except PermissionError:
                print(f"Error: Cannot overwrite '{self.output_path}'. Please close the PDF if it is open in another program.")
                sys.exit(1)

        # Instantiate the canvas
        self.canvas = canvas.Canvas(self.output_path, pagesize=A4)

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
