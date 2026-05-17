import os
import sys
import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from workbook_generator.config import PDFStyle
from workbook_generator.chapters import chap4_v2
from workbook_generator.utils import register_fonts
from workbook_generator.components import create_closing_page


def generate_workbook_chap4_v2(output_filename="Workbook_Chapitre_4_v2.pdf", theme="indigo"):
    PDFStyle.set_theme(theme)

    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except PermissionError:
            print(f"Error: Cannot overwrite {output_filename}. Please close the PDF if it is open.")
            return

    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setTitle("MDM - Workbook Chapitre 4 (v2)")

    register_fonts()

    print("Generating Cover...")
    chap4_v2.create_chap4_v2_cover(c)

    print("Generating Concept Page...")
    chap4_v2.create_concept_page(c)

    print("Generating Recap Seance Page...")
    chap4_v2.create_recap_seance_page(c)

    print("Generating Situation Actuelle...")
    chap4_v2.create_situation_actuelle_page(c)

    print("Generating Histoire Argent...")
    chap4_v2.create_histoire_argent_page(c)

    print("Generating Premières Expériences...")
    chap4_v2.create_premieres_experiences_page(c)

    print("Generating Argent et Projet Pro...")
    chap4_v2.create_argent_projet_pro_page(c)

    print("Generating Minimum Financier...")
    chap4_v2.create_minimum_financier_page(c)

    print("Generating Archétypes v2...")
    chap4_v2.create_archetypes_v2_page(c)

    print("Generating Synthèse v2...")
    chap4_v2.create_synthese_v2_page(c)

    print("Generating Closing Page...")
    create_closing_page(c)

    c.save()
    print(f"PDF generated successfully: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer le chapitre 4 v2 PDF.")
    parser.add_argument("--theme", choices=PDFStyle.THEMES, default="indigo", help="Le thème de couleurs à utiliser.")
    parser.add_argument("--output", type=str, default="Workbook_Chapitre_4_v2.pdf", help="Le nom du fichier PDF généré.")
    args = parser.parse_args()
    generate_workbook_chap4_v2(output_filename=args.output, theme=args.theme)
