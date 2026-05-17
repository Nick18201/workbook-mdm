from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters import chap3
from workbook_generator.components import create_closing_page


def generate_workbook_chap3(output_filename="Workbook_Chapitre_3.pdf", theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("MDM - Workbook Chapitre 3")

    # 2. Generate Pages
    builder.add_page(chap3.create_chap3_cover)
    builder.add_page(chap3.create_concept_page)
    builder.add_page(chap3.create_recap_seance_page)
    builder.add_page(chap3.create_intro_page)
    builder.add_page(chap3.create_chap1_energie)
    builder.add_page(chap3.create_chap2_information)
    builder.add_page(chap3.create_chap3_decisions)
    builder.add_page(chap3.create_chap4_temps)
    builder.add_page(chap3.create_chap5_ombre)
    builder.add_page(create_closing_page)

    # 3. Save
    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le chapitre 3 PDF.",
        default_output="Workbook_Chapitre_3.pdf"
    )
    generate_workbook_chap3(output_filename=args.output, theme=args.theme)
