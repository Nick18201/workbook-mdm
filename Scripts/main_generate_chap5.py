from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_chap5(output_filename="Workbook_Chapitre_5.pdf"):
    """Carnet 5 · Valeurs et moteurs profonds, compiled from workbooks/chap5.json."""
    build_reference_workbook("chap5", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le workbook Chapitre 5 (Valeurs) PDF.", default_output="Workbook_Chapitre_5.pdf")
    generate_workbook_chap5(args.output)
