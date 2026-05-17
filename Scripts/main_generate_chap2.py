from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters import chap2
from workbook_generator.components import create_closing_page


def generate_workbook_chap2(output_filename="Workbook_Chapitre_2.pdf", theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("MDM - Workbook Chapitre 2")

    # 2. Generate Pages
    builder.add_page(chap2.create_chap2_cover)
    builder.add_page(chap2.create_concept_page)
    builder.add_page(chap2.create_recap_seance_page)
    builder.add_page(chap2.create_analysis_parcours_pages)
    builder.add_page(chap2.create_timeline_page)
    builder.add_page(chap2.create_skills_transfer_page)
    builder.add_page(chap2.create_tree_of_life_page)
    builder.add_page(create_closing_page)

    # 3. Save
    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le chapitre 2 PDF.",
        default_output="Workbook_Chapitre_2.pdf"
    )
    generate_workbook_chap2(output_filename=args.output, theme=args.theme)
