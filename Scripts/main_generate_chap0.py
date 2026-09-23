from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters import chap0
from workbook_generator.components import create_closing_page


def generate_workbook_chap0(output_filename="chapitre 0 _ Le prélude.pdf", theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("chapitre 0 : Le prélude")

    builder.add_page(chap0.create_cover_page)
    builder.add_page(chap0.create_summary_page)
    builder.add_page(chap0.create_editorial_page_card)
    builder.add_page(chap0.create_intro_sense_page)
    builder.add_page(chap0.create_form_page_card)
    builder.add_page(chap0.create_premiere_etape_page)
    builder.add_page(chap0.create_faire_le_point_pages)
    builder.add_page(chap0.create_domaines_de_vie_page)
    builder.add_page(chap0.create_entourage_page)
    builder.add_page(create_closing_page)

    builder.save()


# Backwards compatibility alias
build_complete_pdf_v4 = generate_workbook_chap0


if __name__ == "__main__":
    args = create_cli(
        description="Générer le chapitre 0 PDF.",
        default_output="chapitre 0 _ Le prélude.pdf"
    )
    generate_workbook_chap0(args.output, theme=args.theme)
