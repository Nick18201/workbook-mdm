import os
import sys
import shutil

# S'assurer que le dossier Scripts est résolu
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters.programme import (
    create_programme_cover,
    create_programme_page_deroule_1,
    create_programme_page_deroule_2,
    create_programme_page_deroule_3,
    create_programme_page_deroule_4,
    create_programme_page_projets,
    create_programme_page_tarifs,
    create_programme_page_infos_pratiques,
    create_closing_page,
)


def build_programme_pdf(
    output_filename="Programme_Bilan_de_Competences.pdf",
    theme="indigo",
    with_cover=True,
    with_closing=False,
):
    """
    Orchestre la génération du PDF Programme du Bilan de Compétences (8 pages)
    conforme à 100% à la charte graphique des Workbooks de Marge de Manœuvre
    et aux exigences réglementaires Qualiopi.
    """
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("Programme du Bilan de Compétences - Marge de Manœuvre")

    # --- PAGE 1 : COUVERTURE OFFICIELLE WORKBOOK ---
    if with_cover:
        builder.add_page(create_programme_cover)

    # --- PAGE 2 : DÉROULÉ - TEMPS 1 : COMPRENDRE (PARTIE 1, S1 À S3) ---
    builder.add_page(create_programme_page_deroule_1)

    # --- PAGE 3 : DÉROULÉ - TEMPS 1 : COMPRENDRE (PARTIE 2, S4 À S6 + LIVRABLES) ---
    builder.add_page(create_programme_page_deroule_2)

    # --- PAGE 4 : DÉROULÉ - TEMPS 2 : CONFRONTER (S7 & S8 + LIVRABLES) ---
    builder.add_page(create_programme_page_deroule_3)

    # --- PAGE 5 : DÉROULÉ - TEMPS 3 : DÉCIDER ET AGIR (S9, S10, SUIVI + LIVRABLES) ---
    builder.add_page(create_programme_page_deroule_4)

    # --- PAGE 6 : BÉNÉFICES & TRAJECTOIRES (LES 3 PROJETS : RECONVERSION, CRÉATION, ÉVOLUTION) ---
    builder.add_page(create_programme_page_projets)

    # --- PAGE 7 : FORMULE UNIQUE (1 800 €), TARIFS & FINANCEMENT CPF ---
    builder.add_page(create_programme_page_tarifs)

    # --- PAGE 8 : NOUVELLE PAGE INFORMATIONS PRATIQUES (QUALIOPI INDICATEUR 1) ---
    builder.add_page(create_programme_page_infos_pratiques)

    # --- PAGE DE CLÔTURE OPTIONNELLE ---
    if with_closing:
        builder.add_page(create_closing_page)

    builder.save()

    # Synchronisation automatique optionnelle avec le site public marge-de-manoeuvre si accessible
    site_pdf_path = os.path.abspath(
        os.path.join(
            scripts_dir,
            "..",
            "..",
            "marge-de-manoeuvre",
            "public",
            "documents",
            "programme-tarifs-bilan.pdf",
        )
    )
    if os.path.exists(os.path.dirname(site_pdf_path)):
        try:
            shutil.copy2(output_filename, site_pdf_path)
            print(f"Synchronisé avec le site public: {site_pdf_path}")
        except Exception as e:
            print(f"Note: Synchronisation site non effectuée ({e})")


# Standardized naming alias
generate_workbook_programme = build_programme_pdf


if __name__ == "__main__":
    args = create_cli(
        description="Générer le Programme du Bilan de Compétences PDF conforme aux Workbooks.",
        default_output="Programme_Bilan_de_Competences.pdf",
    )
    build_programme_pdf(args.output, theme=args.theme)
