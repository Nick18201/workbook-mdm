import os
import sys
import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from workbook_generator.config import PDFStyle
from workbook_generator.chapters import valeurs
from workbook_generator.chapters import schwartz_pvq
from workbook_generator.utils import register_fonts
from workbook_generator.components import create_closing_page


def generate_workbook_valeurs(output_filename="Workbook_Valeurs.pdf", theme="indigo"):
    PDFStyle.set_theme(theme)

    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except PermissionError:
            print(f"Error: Cannot overwrite {output_filename}. Please close the PDF if it is open.")
            return

    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setTitle("MDM - Workbook Valeurs")

    register_fonts()

    print("Generating Cover...")
    valeurs.create_valeurs_cover(c)

    print("Generating Concept Page...")
    valeurs.create_concept_page(c)

    print("Generating Référence Valeurs de Schwartz...")
    schwartz_pvq.create_schwartz_reference_page(c)

    print("Generating PVQ-21 (Questionnaire de Schwartz)...")
    schwartz_pvq.create_pvq21_pages(c)

    print("Generating Questions de Validation...")
    schwartz_pvq.create_validation_pages(c)

    print("Generating Traits de Personnalité Pro...")
    schwartz_pvq.create_personality_pages(c)

    print("Generating Valeurs — Exercice Réflexif...")
    valeurs.create_valeurs_page(c)

    print("Generating Verbes d'Action...")
    valeurs.create_verbes_page(c)

    print("Generating Closing Page...")
    create_closing_page(c)

    c.save()
    print(f"PDF generated successfully: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer le workbook Valeurs PDF.")
    parser.add_argument("--theme", choices=PDFStyle.THEMES, default="indigo", help="Le thème de couleurs à utiliser.")
    parser.add_argument("--output", type=str, default="Workbook_Valeurs.pdf", help="Le nom du fichier PDF généré.")
    args = parser.parse_args()
    generate_workbook_valeurs(output_filename=args.output, theme=args.theme)
