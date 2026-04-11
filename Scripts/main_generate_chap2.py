import os
import sys
import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Add the current directory to sys.path to ensure we can import 'workbook_generator'
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from workbook_generator.config import PDFStyle
from workbook_generator.chapters import chap2
from workbook_generator.utils import register_fonts
from workbook_generator.components import create_closing_page


def generate_workbook_chap2(output_filename="Workbook_Chapitre_2.pdf", theme="earth"):
    # Set the theme
    PDFStyle.set_theme(theme)

    # Check if we can write to the file
    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except PermissionError:
            print(
                f"Error: Cannot overwrite {output_filename}. Please close the PDF if it is open."
            )
            return

    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setTitle("MDM - Workbook Chapitre 2")

    # 1. Register Fonts
    register_fonts()

    # 2. Generate Pages
    print("Generating Cover...")
    chap2.create_chap2_cover(c)

    print("Generating Concept Page...")
    chap2.create_concept_page(c)

    print("Generating Récapitulatif Page...")
    chap2.create_recap_seance_page(c)

    print("Generating Analysis Parcours Pages...")
    chap2.create_analysis_parcours_pages(c)

    print("Generating Timeline Page...")
    chap2.create_timeline_page(c)

    print("Generating Skills Transfer Page...")
    chap2.create_skills_transfer_page(c)

    print("Generating Tree of Life Page...")
    chap2.create_tree_of_life_page(c)

    print("Generating End Page...")
    create_closing_page(c)

    # 3. Save
    c.save()
    print(f"PDF generated successfully: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer le chapitre 2 PDF.")
    parser.add_argument(
        "--theme",
        choices=PDFStyle.THEMES,
        default="earth",
        help="Le thème de couleurs à utiliser.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="Workbook_Chapitre_2.pdf",
        help="Le nom du fichier PDF généré.",
    )
    args = parser.parse_args()

    generate_workbook_chap2(output_filename=args.output, theme=args.theme)
