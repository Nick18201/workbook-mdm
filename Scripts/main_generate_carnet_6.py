from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_carnet_6(output_filename="Carnet_6.pdf"):
    """Carnet 6 · L'exploration, compiled from workbooks/carnet-6.json."""
    build_reference_workbook("carnet-6", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet 6 PDF.", default_output="Carnet_6.pdf")
    generate_workbook_carnet_6(args.output)
