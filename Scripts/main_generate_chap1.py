from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
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


def build_wb_chap1_pdf(output_filename, theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("Marge de Manœuvre - Chapitre 1")

    # --- PAGE 1: COVER ---
    builder.add_page(create_chap1_main_cover)

    # --- PAGE 2: CONCEPT ---
    builder.add_page(create_concept_page)

    # --- PAGES 3-10: CHAPITRE 1 EXERCICES ---
    builder.add_page(create_engagement_page)
    builder.add_page(create_meteo_page)
    builder.add_page(create_vision_page)
    builder.add_page(create_boussole_page)
    builder.add_page(create_sac_a_dos_page)

    # From old Chapitre 2
    builder.add_page(create_heritage_page)
    builder.add_page(create_work_image_page)
    builder.add_page(create_mentors_page)

    # --- PAGE 11: CLOSING PAGE ---
    builder.add_page(create_closing_page)

    # Total pages: 1 + 1 (concept) + 8 + 1 (closing) = 11 pages exactly

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le chapitre 1 PDF.",
        default_output="Workbook_Chapitre_1.pdf"
    )
    build_wb_chap1_pdf(args.output, theme=args.theme)
