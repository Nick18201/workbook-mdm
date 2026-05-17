from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters.chap0 import (
    create_cover_page,
    create_summary_page,
    create_editorial_page_card,
    create_intro_sense_page,
    create_form_page_card,
    create_premiere_etape_page,
    create_faire_le_point_pages,
    create_domaines_de_vie_page,
    create_entourage_page,
)
from workbook_generator.components import create_closing_page


def build_complete_pdf_v4(output_filename, theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("chapitre 0 : Le prélude")

    builder.add_page(create_cover_page)
    builder.add_page(create_summary_page)
    builder.add_page(create_editorial_page_card)
    builder.add_page(create_intro_sense_page)
    builder.add_page(create_form_page_card)
    builder.add_page(create_premiere_etape_page)
    builder.add_page(create_faire_le_point_pages)
    builder.add_page(create_domaines_de_vie_page)
    builder.add_page(create_entourage_page)
    builder.add_page(create_closing_page)

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le chapitre 0 PDF.",
        default_output="chapitre 0 _ Le prélude.pdf"
    )
    build_complete_pdf_v4(args.output, theme=args.theme)
