from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.components import create_closing_page
from workbook_generator.chapters import chap1


def generate_workbook_chap1(output_filename="Workbook_Chapitre_1.pdf", theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("Marge de Manœuvre - Chapitre 1")

    # --- PAGE 1: COVER ---
    builder.add_page(chap1.create_chap1_cover)

    # --- PAGE 2: CONCEPT ---
    builder.add_page(chap1.create_concept_page)

    # --- PAGES 3-10: CHAPITRE 1 EXERCICES ---
    builder.add_page(chap1.create_engagement_page)
    builder.add_page(chap1.create_meteo_page)
    builder.add_page(chap1.create_vision_page)
    builder.add_page(chap1.create_boussole_page)
    builder.add_page(chap1.create_sac_a_dos_page)

    # From old Chapitre 2
    builder.add_page(chap1.create_heritage_page)
    builder.add_page(chap1.create_work_image_page)
    builder.add_page(chap1.create_mentors_page)

    # --- PAGE 11: CLOSING PAGE ---
    builder.add_page(create_closing_page)

    builder.save()


# Backwards compatibility alias
build_wb_chap1_pdf = generate_workbook_chap1


if __name__ == "__main__":
    args = create_cli(
        description="Générer le chapitre 1 PDF.",
        default_output="Workbook_Chapitre_1.pdf"
    )
    generate_workbook_chap1(args.output, theme=args.theme)
