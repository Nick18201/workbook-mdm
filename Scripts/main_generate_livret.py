from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def build_livret_competences(output_filename="Livret_Competences.pdf"):
    """Le livret de compétences, compiled from workbooks/livret.json."""
    build_reference_workbook("livret", output_filename)


generate_workbook_livret = build_livret_competences


if __name__ == "__main__":
    args = create_cli(description="Générer le Livret de Compétences Augmenté PDF.", default_output="Livret_Competences.pdf")
    build_livret_competences(args.output)
