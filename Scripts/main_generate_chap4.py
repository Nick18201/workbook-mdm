import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters import chap4
from workbook_generator.components import create_closing_page


def generate_workbook_chap4(output_filename="Workbook_Chapitre_4.pdf", theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("MDM - Workbook Chapitre 4")

    builder.add_page(chap4.create_chap4_cover)
    builder.add_page(chap4.create_concept_page)
    builder.add_page(chap4.create_recap_seance_page)
    builder.add_page(chap4.create_psycho_edu_page)
    builder.add_page(chap4.create_kmsi_pages)
    builder.add_page(chap4.create_kmsi_impact_page)
    builder.add_page(chap4.create_biographie_page)
    builder.add_page(chap4.create_dialogue_page)
    builder.add_page(chap4.create_archetypes_page)
    builder.add_page(chap4.create_mindset_surplus_page)
    builder.add_page(chap4.create_synthese_psycho_page)
    builder.add_page(chap4.create_cartographie_page)
    builder.add_page(chap4.create_exploration_page)
    builder.add_page(create_closing_page)

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le chapitre 4 PDF.",
        default_output="Workbook_Chapitre_4.pdf"
    )
    generate_workbook_chap4(output_filename=args.output, theme=args.theme)
