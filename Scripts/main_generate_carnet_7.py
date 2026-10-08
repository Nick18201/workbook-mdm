from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_carnet_7(output_filename="Carnet_7.pdf"):
    """Carnet 7 · Confronter au terrain, compiled from workbooks/carnet-7.json."""
    build_reference_workbook("carnet-7", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet 7 PDF.", default_output="Carnet_7.pdf")
    generate_workbook_carnet_7(args.output)
