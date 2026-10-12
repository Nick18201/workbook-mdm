from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_module_evolution_interne(output_filename="Module_evolution_interne.pdf"):
    """Carnet de route · module évolution interne, compiled from workbooks/module-evolution-interne.json."""
    build_reference_workbook("module-evolution-interne", output_filename)


if __name__ == "__main__":
    args = create_cli(description="Générer le module évolution interne du carnet de route PDF.",
                      default_output="Module_evolution_interne.pdf")
    generate_workbook_module_evolution_interne(args.output)
