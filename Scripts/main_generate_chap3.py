from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_chap3(output_filename="Workbook_Chapitre_3.pdf"):
    """Carnet 3 · Mes fonctionnements propres, compiled from workbooks/chap3.json."""
    build_reference_workbook("chap3", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le chapitre 3 PDF.", default_output="Workbook_Chapitre_3.pdf")
    generate_workbook_chap3(args.output)
