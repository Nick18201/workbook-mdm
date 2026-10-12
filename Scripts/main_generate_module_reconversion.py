from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_module_reconversion(output_filename="Module_reconversion.pdf"):
    """Carnet de route · module reconversion, compiled from workbooks/module-reconversion.json."""
    build_reference_workbook("module-reconversion", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le module reconversion du carnet de route PDF.",
                      default_output="Module_reconversion.pdf")
    generate_workbook_module_reconversion(args.output)
