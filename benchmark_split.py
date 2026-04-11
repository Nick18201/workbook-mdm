import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'Scripts'))

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from workbook_generator.components import draw_title, create_standard_summary_page
from workbook_generator.utils import register_fonts

def run_benchmark():
    register_fonts()
    c = canvas.Canvas("dummy.pdf", pagesize=A4)

    start_time = time.perf_counter()
    for _ in range(1000):
        draw_title(c, "This is a test title that needs to be split over multiple lines because it is quite long and we want to see the performance of simpleSplit", pos=(100, 800), available_width=200)
    end_time = time.perf_counter()
    print(f"Time taken for draw_title: {end_time - start_time:.4f} seconds")

    start_time = time.perf_counter()
    for _ in range(100):
        # We pass a simple string as point for simplicity
        create_standard_summary_page(c, "01", "Chapitre Un: Introduction", "This is an introductory text that will be split by simpleSplit in the summary page function.", ["Point 1", "Point 2", "Point 3"])
    end_time = time.perf_counter()
    print(f"Time taken for create_standard_summary_page: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
