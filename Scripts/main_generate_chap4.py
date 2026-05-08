import os
import sys
import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from workbook_generator.config import PDFStyle
from workbook_generator.chapters import chap4
from workbook_generator.utils import register_fonts
from workbook_generator.components import create_closing_page


def generate_workbook_chap4(output_filename="Workbook_Chapitre_4.pdf", theme="indigo"):
    PDFStyle.set_theme(theme)

    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except PermissionError:
            print(f"Error: Cannot overwrite {output_filename}. Please close the PDF if it is open.")
            return

    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setTitle("MDM - Workbook Chapitre 4")

    register_fonts()

    print("Generating Cover...")
    chap4.create_chap4_cover(c)

    print("Generating Concept Page...")
    chap4.create_concept_page(c)

    print("Generating Récapitulatif MBTI...")
    chap4.create_recap_seance_page(c)

    print("Generating Valeurs de Schwarz...")
    chap4.create_valeurs_page(c)

    print("Generating Verbes d'Action...")
    chap4.create_verbes_page(c)

    print("Generating Psycho-Éducation Financière...")
    chap4.create_psycho_edu_page(c)

    print("Generating KMSI Quiz...")
    chap4.create_kmsi_pages(c)

    print("Generating Biographie Financière...")
    chap4.create_biographie_page(c)

    print("Generating Dialogue avec l'Argent...")
    chap4.create_dialogue_page(c)

    print("Generating Archétypes Sacrés...")
    chap4.create_archetypes_page(c)

    print("Generating Mindset de Surplus...")
    chap4.create_mindset_surplus_page(c)

    print("Generating Cartographie Personnelle...")
    chap4.create_cartographie_page(c)

    print("Generating Exploration Inter-Session...")
    chap4.create_exploration_page(c)

    print("Generating Closing Page...")
    create_closing_page(c)

    c.save()
    print(f"PDF generated successfully: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer le chapitre 4 PDF.")
    parser.add_argument("--theme", choices=PDFStyle.THEMES, default="indigo", help="Le thème de couleurs à utiliser.")
    parser.add_argument("--output", type=str, default="Workbook_Chapitre_4.pdf", help="Le nom du fichier PDF généré.")
    args = parser.parse_args()
    generate_workbook_chap4(output_filename=args.output, theme=args.theme)
