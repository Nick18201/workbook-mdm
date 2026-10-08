from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_chap1(output_filename="Workbook_Chapitre_1.pdf"):
    """Carnet 1 · L'état des lieux, compiled from workbooks/chap1.json."""
    build_reference_workbook("chap1", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le chapitre 1 PDF.", default_output="Workbook_Chapitre_1.pdf")
    generate_workbook_chap1(args.output)
