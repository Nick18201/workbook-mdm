from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_chap6(output_filename="Workbook_Chapitre_6.pdf"):
    """Carnet 6 · Phase d'exploration, compiled from workbooks/chap6.json."""
    build_reference_workbook("chap6", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le chapitre 6 PDF.", default_output="Workbook_Chapitre_6.pdf")
    generate_workbook_chap6(args.output)
