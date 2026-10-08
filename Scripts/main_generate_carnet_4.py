from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_carnet_4(output_filename="Carnet_4.pdf"):
    """Carnet 4 · Mon rapport à l'argent, compiled from workbooks/carnet-4.json."""
    build_reference_workbook("carnet-4", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet 4 PDF.", default_output="Carnet_4.pdf")
    generate_workbook_carnet_4(args.output)
