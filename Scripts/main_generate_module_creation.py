from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_module_creation(output_filename="Module_creation.pdf"):
    """Carnet de route · module création, compiled from workbooks/module-creation.json."""
    build_reference_workbook("module-creation", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le module création du carnet de route PDF.",
                      default_output="Module_creation.pdf")
    generate_workbook_module_creation(args.output)
