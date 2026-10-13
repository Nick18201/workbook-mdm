from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli, part_output


def generate_workbook_carnet_7(output_filename="Carnet_7.pdf", part=None):
    """
    Carnet 7 · Explorer le terrain, compiled from workbooks/carnet-7.json: the file of one
    part (one per session, 7 then 8), or without a part both of them one after the other.
    """
    build_reference_workbook("carnet-7", output_filename, part)


if __name__ == "__main__":
    args = create_cli(description="Générer le carnet 7 PDF, un fichier par partie (Carnet_7_partie_1.pdf…).",
                      default_output="Carnet_7.pdf")
    for part in (1, 2):
        generate_workbook_carnet_7(part_output(args.output, part), part)
