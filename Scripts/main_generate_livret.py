from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.components import create_closing_page
from workbook_generator.chapters.livret_competences import (
    create_livret_cover,
    create_profil_page,
    create_parcours_page,
    create_preuves_page,
    create_potentiel_page,
)


def build_livret_competences(output_filename, theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("Livret de Compétences Augmenté - Marge de Manœuvre")

    # --- COUVERTURE ---
    builder.add_page(create_livret_cover)

    # --- P1 : PROFIL ---
    builder.add_page(create_profil_page)

    # --- P2 : PARCOURS ---
    builder.add_page(create_parcours_page)

    # --- P3 : PREUVES ---
    builder.add_page(create_preuves_page)

    # --- P4 : POTENTIEL ---
    builder.add_page(create_potentiel_page)

    # --- CLOSING PAGE ---
    builder.add_page(create_closing_page)

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le Livret de Compétences PDF.",
        default_output="Livret_Competences.pdf"
    )

    # Always run from the root directory so assets path resolves correctly.
    # We cd into the root automatically or rely on the user running it from the root.
    build_livret_competences(args.output, theme=args.theme)
