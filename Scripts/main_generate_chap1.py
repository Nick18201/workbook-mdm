import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from workbook_generator.utils import register_fonts
from workbook_generator.config import PDFStyle
from workbook_generator.components import create_standard_cover, create_closing_page
from workbook_generator.chapters.chap1 import (
    create_engagement_page,
    create_concept_page,
    create_meteo_page,
    create_vision_page,
    create_boussole_page,
    create_sac_a_dos_page,
    create_heritage_page,
    create_work_image_page,
    create_mentors_page,
)


def create_chap1_main_cover(c):
    create_standard_cover(c, "Chapitre 1 : Mes héritages")


def build_wb_chap1_pdf(output_filename, theme="earth"):
    # Set the theme
    PDFStyle.set_theme(theme)
    # Register fonts first
    register_fonts()

    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setTitle("Marge de Manœuvre - Chapitre 1")

    # --- PAGE 1: COVER ---
    create_chap1_main_cover(c)

    # --- PAGE 2: CONCEPT ---
    create_concept_page(c)

    # --- PAGES 3-10: CHAPITRE 1 EXERCICES ---
    create_engagement_page(c)
    create_meteo_page(c)
    create_vision_page(c)
    create_boussole_page(c)
    create_sac_a_dos_page(c)

    # From old Chapitre 2
    create_heritage_page(c)
    create_work_image_page(c)
    create_mentors_page(c)

    # --- PAGE 11: CLOSING PAGE ---
    create_closing_page(c)

    # Total pages: 1 + 1 (concept) + 8 + 1 (closing) = 11 pages exactly

    c.save()
    print(f"PDF 'Workbook Chapitre 1' Generated: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer le chapitre 1 PDF.")
    parser.add_argument(
        "--theme",
        choices=PDFStyle.THEMES,
        default="earth",
        help="Le thème de couleurs à utiliser.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="Workbook_Chapitre_1.pdf",
        help="Le nom du fichier PDF généré.",
    )
    args = parser.parse_args()

    build_wb_chap1_pdf(args.output, theme=args.theme)
