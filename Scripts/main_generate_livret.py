import os
import sys

# S'assurer que le dossier Scripts est résolu pour les imports workbook_generator
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.components import create_closing_page
from workbook_generator.chapters.livret import (
    create_livret_cover,
    create_profil_mbti_page,
    create_profil_ecologie_page,
    create_travail_reel_coulisses_page,
    create_travail_reel_empeche_page,
    create_cartographie_metier_page,
    create_cartographie_humain_page,
    create_autonomie_paliers_page,
    create_autonomie_transfert_page,
    create_recit_contexte_page,
    create_recit_impact_page,
    create_boussole_regard_page,
    create_boussole_confiance_page,
    create_plan_securite_page,
    create_plan_pas_proximal_page,
)


def build_livret_competences(output_filename="Livret_Competences.pdf", theme="indigo"):
    """
    Génère le Livret de Compétences Augmenté - Marge de Manœuvre.
    Format étendu en 16 pages : très pédagogique, sans jargon ésotérique,
    avec des explications approfondies et de grands espaces d'écriture (5.0 cm).
    """
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("Livret de Compétences Augmenté - Marge de Manœuvre")

    # --- COUVERTURE OFFICIELLE MDM ---
    builder.add_page(create_livret_cover)

    # --- THÈME 1 : MON PROFIL & MON ÉCOLOGIE DE TRAVAIL ---
    builder.add_page(create_profil_mbti_page)
    builder.add_page(create_profil_ecologie_page)

    # --- THÈME 2 : LES COULISSES DE MON TRAVAIL RÉEL ---
    builder.add_page(create_travail_reel_coulisses_page)
    builder.add_page(create_travail_reel_empeche_page)

    # --- THÈME 3 : MA CARTOGRAPHIE DES COMPÉTENCES EN ACTION ---
    builder.add_page(create_cartographie_metier_page)
    builder.add_page(create_cartographie_humain_page)

    # --- THÈME 4 : MES REPÈRES D'AUTONOMIE & MA TRANSFÉRABILITÉ ---
    builder.add_page(create_autonomie_paliers_page)
    builder.add_page(create_autonomie_transfert_page)

    # --- THÈME 5 : ARRÊT SUR IMAGE (RÉCIT D'UNE RÉUSSITE CONCRÈTE) ---
    builder.add_page(create_recit_contexte_page)
    builder.add_page(create_recit_impact_page)

    # --- THÈME 6 : MA BOUSSOLE D'AVENIR ---
    builder.add_page(create_boussole_regard_page)
    builder.add_page(create_boussole_confiance_page)

    # --- THÈME 7 : MON PLAN D'ÉMANCIPATION & MON PROCHAIN PETIT PAS ---
    builder.add_page(create_plan_securite_page)
    builder.add_page(create_plan_pas_proximal_page)

    # --- CLOSING PAGE OFFICIELLE MDM ---
    builder.add_page(create_closing_page)

    builder.save()


if __name__ == "__main__":
    args = create_cli(
        description="Générer le Livret de Compétences Augmenté PDF (Version Aérée & Pédagogique).",
        default_output="Livret_Competences.pdf",
    )

    build_livret_competences(args.output, theme=args.theme)
