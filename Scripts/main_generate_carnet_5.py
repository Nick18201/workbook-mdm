from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_carnet_5(output_filename="Carnet_5.pdf"):
    """Carnet 5 · Valeurs et moteurs profonds, compiled from workbooks/carnet-5.json."""
    build_reference_workbook("carnet-5", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet 5 PDF.", default_output="Carnet_5.pdf")
    generate_workbook_carnet_5(args.output)
