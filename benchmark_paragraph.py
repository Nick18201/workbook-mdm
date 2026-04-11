import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'Scripts'))

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from workbook_generator.utils import register_fonts

def run_benchmark():
    register_fonts()
    c = canvas.Canvas("dummy2.pdf", pagesize=A4)
    width, height = A4
    style_body = ParagraphStyle("Body", fontName="Helvetica", fontSize=11, leading=15)

    start_time = time.time()
    for _ in range(1000):
        p_intro = Paragraph("This is a long introductory text that should be evaluated multiple times by the paragraph wrapping mechanism, triggering underlying calls. Because Paragraphs wrap differently, they compute text heavily.", style_body)
        w, h = p_intro.wrap(width - 50, height)
        p_intro.drawOn(c, 25, 25)
    end_time = time.time()
    print(f"Time taken for Paragraph wrap/draw: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
