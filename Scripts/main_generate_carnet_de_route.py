from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_carnet_de_route(output_filename="Carnet_de_route.pdf"):
    """Carnet de route · Décider et agir, compiled from workbooks/carnet-de-route.json."""
    build_reference_workbook("carnet-de-route", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet de route PDF.", default_output="Carnet_de_route.pdf")
    generate_workbook_carnet_de_route(args.output)
