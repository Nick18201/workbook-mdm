import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from workbook_generator.utils import register_fonts
from workbook_generator.config import PDFStyle
from workbook_generator.chapters.chap0 import (
    create_cover_page, create_summary_page, create_editorial_page_card,
    create_intro_sense_page, create_form_page_card, create_premiere_etape_page,
    create_faire_le_point_pages, create_domaines_de_vie_page, create_entourage_page
)
from workbook_generator.components import create_closing_page

def build_complete_pdf_v4(output_filename, theme="earth"):
    # Set the theme
    PDFStyle.set_theme(theme)
    # Register fonts first
    register_fonts()
    
    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setTitle("chapitre 0 : Le prélude")
    
    create_cover_page(c)
    create_summary_page(c)
    create_editorial_page_card(c)
    create_intro_sense_page(c)
    create_form_page_card(c)
    create_premiere_etape_page(c)
    create_faire_le_point_pages(c)
    create_domaines_de_vie_page(c)
    create_entourage_page(c)
    create_closing_page(c)
    
    c.save()
    print(f"PDF 'DA V4' Generated: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer le chapitre 0 PDF.")
    parser.add_argument("--theme", choices=["earth", "indigo"], default="earth", help="Le thème de couleurs à utiliser.")
    parser.add_argument("--output", type=str, default="chapitre 0 _ Le prélude.pdf", help="Le nom du fichier PDF généré.")
    args = parser.parse_args()

    build_complete_pdf_v4(args.output, theme=args.theme)
