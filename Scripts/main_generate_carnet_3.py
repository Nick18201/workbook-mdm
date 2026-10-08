from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_carnet_3(output_filename="Carnet_3.pdf"):
    """Carnet 3 · Mes fonctionnements propres, compiled from workbooks/carnet-3.json."""
    build_reference_workbook("carnet-3", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet 3 PDF.", default_output="Carnet_3.pdf")
    generate_workbook_carnet_3(args.output)
