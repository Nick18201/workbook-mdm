from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli, part_output


def generate_workbook_carnet_de_route(output_filename="Carnet_de_route.pdf", part=None):
    """
    Carnet de route · Décider et agir, compiled from workbooks/carnet-de-route.json: the file
    of one part (one per session, 9 then 10), or without a part both of them one after the other.
    """
    build_reference_workbook("carnet-de-route", output_filename, part)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet de route PDF, un fichier par partie "
                                  "(Carnet_de_route_partie_1.pdf…).", default_output="Carnet_de_route.pdf")
    for part in (1, 2):
        generate_workbook_carnet_de_route(part_output(args.output, part), part)
