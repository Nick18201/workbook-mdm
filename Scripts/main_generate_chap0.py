from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_chap0(output_filename="chapitre 0 _ Le prélude.pdf"):
    """Carnet 0 · Le prélude, compiled from workbooks/chap0.json."""
    build_reference_workbook("chap0", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le chapitre 0 PDF.", default_output="chapitre 0 _ Le prélude.pdf")
    generate_workbook_chap0(args.output)
