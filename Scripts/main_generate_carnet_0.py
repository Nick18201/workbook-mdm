from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_carnet_0(output_filename="Carnet_0.pdf"):
    """Carnet 0 · Mesurer votre marge, offert avant le bilan, compiled from workbooks/carnet-0.json."""
    build_reference_workbook("carnet-0", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet 0 PDF.", default_output="Carnet_0.pdf")
    generate_workbook_carnet_0(args.output)
