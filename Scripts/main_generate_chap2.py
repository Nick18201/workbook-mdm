from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_chap2(output_filename="Workbook_Chapitre_2.pdf"):
    """Carnet 2 · Mon parcours, compiled from workbooks/chap2.json."""
    build_reference_workbook("chap2", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le chapitre 2 PDF.", default_output="Workbook_Chapitre_2.pdf")
    generate_workbook_chap2(args.output)
