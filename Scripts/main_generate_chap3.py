import os
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from workbook_generator.config import PDFStyle
from workbook_generator.chapters import chap3
from workbook_generator.utils import register_fonts
from workbook_generator.components import create_closing_page

def generate_workbook_chap3():
    output_filename = "Workbook_Chapitre_3.pdf"
    
    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except PermissionError:
            print(f"Error: Cannot overwrite {output_filename}. Please close the PDF if it is open.")
            return

    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setTitle("MDM - Workbook Chapitre 3")
    
    # 1. Register Fonts
    register_fonts()
    
    # 2. Generate Pages
    print("Generating Cover...")
    chap3.create_chap3_cover(c)

    print("Generating Concept Page...")
    chap3.create_concept_page(c)

    print("Generating Récapitulatif Page...")
    chap3.create_recap_seance_page(c)

    print("Generating Intro Page...")
    chap3.create_intro_page(c)
    
    print("Generating Chap 1: Energie...")
    chap3.create_chap1_energie(c)
    
    print("Generating Chap 2: Information...")
    chap3.create_chap2_information(c)
    
    print("Generating Chap 3: Decisions...")
    chap3.create_chap3_decisions(c)
    
    print("Generating Chap 4: Temps...")
    chap3.create_chap4_temps(c)
    
    print("Generating Chap 5: Ombre...")
    chap3.create_chap5_ombre(c)
    
    print("Generating End Page...")
    create_closing_page(c)

    # 3. Save
    c.save()
    print(f"PDF generated successfully: {output_filename}")

if __name__ == "__main__":
    generate_workbook_chap3()
