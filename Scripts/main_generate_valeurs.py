from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters import valeurs
from workbook_generator.chapters import schwartz_pvq
from workbook_generator.components import create_closing_page


def generate_workbook_valeurs(output_filename="Workbook_Valeurs.pdf", theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("MDM - Workbook Valeurs")

    builder.add_page(valeurs.create_valeurs_cover)
    builder.add_page(valeurs.create_concept_page)
    builder.add_page(schwartz_pvq.create_schwartz_reference_page)
    builder.add_page(schwartz_pvq.create_pvq21_pages)
    builder.add_page(schwartz_pvq.create_validation_pages)
    builder.add_page(schwartz_pvq.create_personality_pages)
    builder.add_page(valeurs.create_valeurs_page)
    builder.add_page(valeurs.create_verbes_page)
    builder.add_page(create_closing_page)

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le workbook Valeurs PDF.",
        default_output="Workbook_Valeurs.pdf"
    )
    generate_workbook_valeurs(output_filename=args.output, theme=args.theme)
