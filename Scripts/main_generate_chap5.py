from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters import chap5
from workbook_generator.components import create_closing_page


def generate_workbook_chap5(output_filename="Workbook_Chapitre_5.pdf"):
    builder = DocumentBuilder(output_path=output_filename, carnet=5)
    builder.set_title("Marge de Manœuvre - Chapitre 5 : Valeurs et moteurs profonds")

    builder.add_page(chap5.create_valeurs_cover)
    builder.add_page(chap5.create_concept_page)
    builder.add_page(chap5.create_intro_page)
    builder.add_page(chap5.create_alignement_pages)
    builder.add_page(chap5.create_desalignement_pages)
    builder.add_page(chap5.create_choix_difficiles_page)
    builder.add_page(chap5.create_liste_valeurs_page)
    builder.add_page(chap5.create_hierarchiser_valeurs_page)
    builder.add_page(chap5.create_incarner_valeur_1_page)
    builder.add_page(chap5.create_incarner_valeur_2_page)
    builder.add_page(chap5.create_incarner_valeur_3_page)
    builder.add_page(chap5.create_conditions_travail_page)
    builder.add_page(chap5.create_tensions_page)
    builder.add_page(chap5.create_synthese_page)
    builder.add_page(chap5.create_livrable_page)
    builder.add_page(create_closing_page)

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le workbook Chapitre 5 (Valeurs) PDF.",
        default_output="Workbook_Chapitre_5.pdf"
    )
    generate_workbook_chap5(output_filename=args.output)
