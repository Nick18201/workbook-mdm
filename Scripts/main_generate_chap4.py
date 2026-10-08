from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_chap4(output_filename="Workbook_Chapitre_4.pdf"):
    """Carnet 4 · Mon rapport à l'argent, compiled from workbooks/chap4.json."""
    build_reference_workbook("chap4", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le chapitre 4 PDF.", default_output="Workbook_Chapitre_4.pdf")
    generate_workbook_chap4(args.output)
