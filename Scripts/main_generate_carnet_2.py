from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_carnet_2(output_filename="Carnet_2.pdf"):
    """Carnet 2 · Mon parcours, compiled from workbooks/carnet-2.json."""
    build_reference_workbook("carnet-2", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet 2 PDF.", default_output="Carnet_2.pdf")
    generate_workbook_carnet_2(args.output)
