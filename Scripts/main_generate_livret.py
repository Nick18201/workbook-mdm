import sys
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Add logic to make sure `workbook_generator` is found if run from root or Scripts directly.
# This prevents ModuleNotFoundError.
# Since we might be running this from standard dirs:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workbook_generator.utils import register_fonts
from workbook_generator.components import create_closing_page
from workbook_generator.chapters.livret_competences import (
    create_livret_cover,
    create_profil_page,
    create_parcours_page,
    create_preuves_page,
    create_potentiel_page
)

def build_livret_competences(output_filename):
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
    final_output = "Livret_Competences.pdf"
    # Always run from the root directory so assets path resolves correctly.
    # We cd into the root automatically or rely on the user running it from the root.
    build_livret_competences(final_output)
