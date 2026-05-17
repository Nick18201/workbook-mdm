from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters import chap4
from workbook_generator.components import create_closing_page


def generate_workbook_chap4(output_filename="Workbook_Chapitre_4_v2.pdf", theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("MDM - Workbook Chapitre 4 (v2)")

    builder.add_page(chap4.create_chap4_v2_cover)
    builder.add_page(chap4.create_concept_page)
    builder.add_page(chap4.create_recap_seance_page)
    builder.add_page(chap4.create_situation_actuelle_page)
    builder.add_page(chap4.create_histoire_argent_page)
    builder.add_page(chap4.create_premieres_experiences_page)
    builder.add_page(chap4.create_argent_projet_pro_page)
    builder.add_page(chap4.create_minimum_financier_page)
    builder.add_page(chap4.create_archetypes_v2_page)
    builder.add_page(chap4.create_synthese_v2_page)
    builder.add_page(create_closing_page)

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le chapitre 4 v2 PDF.",
        default_output="Workbook_Chapitre_4.pdf"
    )
    generate_workbook_chap4(output_filename=args.output, theme=args.theme)
