import os
import sys

# S'assurer que le dossier Scripts est résolu
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.chapters.programme import (
    create_programme_cover,
    create_programme_page_1,
    create_programme_page_2,
    create_programme_page_3,
    create_programme_page_4,
    create_programme_page_5,
    create_programme_page_6,
    create_programme_page_7,
    create_programme_page_8,
    create_programme_page_9,
    create_closing_page,
)


def build_programme_pdf(
    output_filename="Programme_Bilan_de_Competences.pdf",
    theme="indigo",
    with_cover=True,
    with_closing=True,
):
    """
    Orchestre la génération du PDF Programme du Bilan de Compétences
    conforme à 100% à la charte graphique des Workbooks de Marge de Manœuvre
    et aux exigences réglementaires Qualiopi.
    """
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("Programme du Bilan de Compétences - Marge de Manœuvre")

    # --- COUVERTURE OFFICIELLE WORKBOOK ---
    if with_cover:
        builder.add_page(create_programme_cover)

    # --- P1 : OBJECTIFS DU BILAN & COMPÉTENCES VISÉES ---
    builder.add_page(create_programme_page_1)

    # --- P2 : 1. PRÉSENTATION DE LA MÉTHODE & ÉTAPE A (INTROSPECTION) ---
    builder.add_page(create_programme_page_2)

    # --- P3 : ÉTAPE B (EXPLORATION) & ÉTAPE C (CONCRÉTISATION) ---
    builder.add_page(create_programme_page_3)

    # --- P4 : 2. ORGANISATION PRATIQUE & MOYENS PÉDAGOGIQUES ---
    builder.add_page(create_programme_page_4)

    # --- P5 : 3. VOS ACCOMPAGNATEURS (LYSIANE BRAND & NICOLAS BLUM FERRACCI) ---
    builder.add_page(create_programme_page_5)

    # --- P6 : 4. LES 3 FORMULES DE BILANS & TARIFS ---
    builder.add_page(create_programme_page_6)

    # --- P7 : 5. FINANCEMENT, MODALITÉS D'ACCÈS & SUIVI ---
    builder.add_page(create_programme_page_7)

    # --- P8 : 6. ACCÈS AU CABINET & MODALITÉS D'ACCUEIL ---
    builder.add_page(create_programme_page_8)

    # --- P9 : 7. INDICATEURS DE RÉSULTATS & SATISFACTION 2025 ---
    builder.add_page(create_programme_page_9)

    # --- PAGE DE CLÔTURE OFFICIELLE WORKBOOK ---
    if with_closing:
        builder.add_page(create_closing_page)

    builder.save()


# Standardized naming alias
generate_workbook_programme = build_programme_pdf


if __name__ == "__main__":
    args = create_cli(
        description="Générer le Programme du Bilan de Compétences PDF conforme aux Workbooks.",
        default_output="Programme_Bilan_de_Competences.pdf",
    )
    build_programme_pdf(args.output, theme=args.theme)
