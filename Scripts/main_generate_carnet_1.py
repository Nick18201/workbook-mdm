from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_carnet_1(output_filename="Carnet_1.pdf"):
    """Carnet 1 · L'état des lieux, compiled from workbooks/carnet-1.json."""
    build_reference_workbook("carnet-1", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet 1 PDF.", default_output="Carnet_1.pdf")
    generate_workbook_carnet_1(args.output)
