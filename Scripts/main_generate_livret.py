import sys
import os
import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Add logic to make sure `workbook_generator` is found if run from root or Scripts directly.
# This prevents ModuleNotFoundError.
# Since we might be running this from standard dirs:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workbook_generator.utils import register_fonts
from workbook_generator.config import PDFStyle
from workbook_generator.components import create_closing_page
from workbook_generator.chapters.livret_competences import (
    create_livret_cover,
    create_profil_page,
    create_parcours_page,
    create_preuves_page,
    create_potentiel_page
)

def build_livret_competences(output_filename, theme="earth"):
    # Set the theme
    PDFStyle.set_theme(theme)
    # Register fonts first
    register_fonts()
    
    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setTitle("Livret de Compétences Augmenté - Marge de Manœuvre")
    
    # --- COUVERTURE ---
    create_livret_cover(c)
    
    # --- P1 : PROFIL ---
    create_profil_page(c)

    # --- P2 : PARCOURS ---
    create_parcours_page(c)
    
    # --- P3 : PREUVES ---
    create_preuves_page(c)
    
    # --- P4 : POTENTIEL ---
    create_potentiel_page(c)
    
    # --- CLOSING PAGE ---
    create_closing_page(c)
    
    c.save()
    print(f"PDF 'Livret de Compétences' Generated: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer le Livret de Compétences PDF.")
    parser.add_argument("--theme", choices=["earth", "indigo"], default="earth", help="Le thème de couleurs à utiliser.")
    parser.add_argument("--output", type=str, default="Livret_Competences.pdf", help="Le nom du fichier PDF généré.")
    args = parser.parse_args()

    # Always run from the root directory so assets path resolves correctly.
    # We cd into the root automatically or rely on the user running it from the root.
    build_livret_competences(args.output, theme=args.theme)
