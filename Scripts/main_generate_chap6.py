from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters import chap6
from workbook_generator.components import create_closing_page


def generate_workbook_chap6(output_filename="Workbook_Chapitre_6.pdf"):
    builder = DocumentBuilder(output_path=output_filename, carnet=6)
    builder.set_title("Marge de Manœuvre - Chapitre 6 : Phase d'exploration")

    builder.add_page(chap6.create_chap6_cover)
    builder.add_page(chap6.create_concept_page)
    builder.add_page(chap6.create_recap_seance_page)
    builder.add_page(chap6.create_cartographie_page)
    builder.add_page(chap6.create_retours_proches_page)
    builder.add_page(chap6.create_pistes_intro_page)
    builder.add_page(chap6.create_pistes_no_limit_page)
    builder.add_page(chap6.create_pistes_realistes_page)
    builder.add_page(chap6.create_ressources_page)
    builder.add_page(chap6.create_livrable_page)
    builder.add_page(create_closing_page)

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le chapitre 6 PDF.",
        default_output="Workbook_Chapitre_6.pdf"
    )
    generate_workbook_chap6(output_filename=args.output)
