from workbook_generator.compiler import build_reference_workbook
from workbook_generator.utils import create_cli


def generate_workbook_livret_competences(output_filename="Livret_Competences.pdf"):
    """Le livret de compétences « Votre portfolio », compiled from workbooks/livret-competences.json."""
    build_reference_workbook("livret-competences", output_filename)


build_workbook_livret_competences = generate_workbook_livret_competences


if __name__ == "__main__":
    args = create_cli(description="Générer le livret de compétences « Votre portfolio » (PDF).",
                      default_output="Livret_Competences.pdf")
    generate_workbook_livret_competences(args.output)
