from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters import chap5
from workbook_generator.components import create_closing_page


def generate_workbook_chap5(output_filename="Workbook_Chapitre_5.pdf", theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("MDM - Workbook Chapitre 5 (Valeurs)")

    builder.add_page(chap5.create_valeurs_cover)
    builder.add_page(chap5.create_concept_page)
    builder.add_page(chap5.create_intro_page)
    builder.add_page(chap5.create_alignement_pages_part1)
    builder.add_page(chap5.create_alignement_pages_part2)
    builder.add_page(chap5.create_desalignement_pages_part1)
    builder.add_page(chap5.create_desalignement_pages_part2)
    builder.add_page(chap5.create_choix_difficiles_page1)
    builder.add_page(chap5.create_choix_difficiles_page2)
    builder.add_page(chap5.create_liste_valeurs_page1)
    builder.add_page(chap5.create_liste_valeurs_page2)
    builder.add_page(chap5.create_hierarchiser_valeurs_page)
    builder.add_page(chap5.create_incarner_valeur_1_page)
    builder.add_page(chap5.create_incarner_valeur_2_page)
    builder.add_page(chap5.create_incarner_valeur_3_page)
    builder.add_page(chap5.create_conditions_travail_page)
    builder.add_page(chap5.create_tensions_page1)
    builder.add_page(chap5.create_tensions_page2)
    builder.add_page(chap5.create_synthese_page)
    builder.add_page(create_closing_page)

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le workbook Chapitre 5 (Valeurs) PDF.",
        default_output="Workbook_Chapitre_5.pdf"
    )
    generate_workbook_chap5(output_filename=args.output, theme=args.theme)
