import os
import sys

# S'assurer que le dossier Scripts est résolu pour les imports workbook_generator
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from workbook_generator.utils import create_cli
from workbook_generator.document_builder import DocumentBuilder
from workbook_generator.components import create_closing_page
from workbook_generator.chapters import business_plan


def generate_workbook_business_plan(
    output_filename="Workbook_Business_Plan.pdf", theme="indigo"
):
    """
    Génère le livret complet 'Mon Business Plan — De l'idée au projet viable' (35 pages).
    Structure pédagogique en 6 temps, formulaires interactifs AcroForm et respect du Design System MDM.
    """
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("Mon Business Plan — De l'idée au projet viable")

    # --- 0. OUVERTURE & CADRAGE ---
    builder.add_page(business_plan.create_business_plan_cover)  # P1
    builder.add_page(business_plan.create_business_plan_summary)  # P2

    # --- PARTIE 1 : POSER LES FONDATIONS ---
    builder.add_page(business_plan.create_fondations_idee_page)  # P3
    builder.add_page(business_plan.create_fondations_vision_page)  # P4

    # --- PARTIES 2 & 3 : CIBLE, BESOIN & PROBLÈME ---
    builder.add_page(business_plan.create_cible_public_page)  # P5
    builder.add_page(business_plan.create_cible_persona_page)  # P6
    builder.add_page(business_plan.create_probleme_analyse_page)  # P7
    builder.add_page(business_plan.create_probleme_hypotheses_page)  # P8

    # --- PARTIES 4, 5 & 6 : OFFRE, MARCHÉ & BENCHMARK ---
    builder.add_page(business_plan.create_offre_definition_page)  # P9
    builder.add_page(business_plan.create_offre_valeur_page)  # P10
    builder.add_page(business_plan.create_marche_tendances_page)  # P11
    builder.add_page(business_plan.create_marche_concurrents_page)  # P12
    builder.add_page(business_plan.create_marche_benchmark_page)  # P13

    # --- PARTIE 7 : POSITIONNEMENT & IMAGE ---
    builder.add_page(business_plan.create_positionnement_identite_page)  # P14
    builder.add_page(business_plan.create_positionnement_pitch_page)  # P15

    # --- PARTIES 8, 9, 10 & 11 : MODÈLE ÉCONOMIQUE, OFFRES, PRIX & COMMERCIALISATION ---
    builder.add_page(business_plan.create_modele_revenus_page)  # P16
    builder.add_page(business_plan.create_modele_canvas_page)  # P17
    builder.add_page(business_plan.create_commercial_offres_page)  # P18
    builder.add_page(business_plan.create_commercial_prix_page)  # P19
    builder.add_page(business_plan.create_commercial_acquisition_page)  # P20
    builder.add_page(business_plan.create_commercial_parcours_page)  # P21

    # --- PARTIES 12, 13, 14, 15, 16 & 17 : COMMUNICATION, MOYENS, STATUT & FINANCES ---
    builder.add_page(business_plan.create_communication_message_page)  # P22
    builder.add_page(business_plan.create_communication_plan_page)  # P23
    builder.add_page(business_plan.create_ressources_moyens_page)  # P24
    builder.add_page(business_plan.create_ressources_competences_page)  # P25
    builder.add_page(business_plan.create_juridique_cadre_page)  # P26
    builder.add_page(business_plan.create_finances_depenses_page)  # P27
    builder.add_page(business_plan.create_finances_previsionnel_page)  # P28
    builder.add_page(business_plan.create_finances_financement_page)  # P29

    # --- PARTIES 18, 19, 20 & 21 : EXPÉRIMENTATION, RISQUES, ACTION & EXECUTIVE SUMMARY ---
    builder.add_page(business_plan.create_action_mvp_page)  # P30
    builder.add_page(business_plan.create_action_risques_page)  # P31
    builder.add_page(business_plan.create_action_roadmap_page)  # P32
    builder.add_page(business_plan.create_synthese_executive_page)  # P33

    # --- PARTIE 22 : ENGAGEMENT & CLÔTURE OFFICIELLE MDM ---
    builder.add_page(business_plan.create_engagement_signature_page)  # P34
    builder.add_page(create_closing_page)  # P35

    builder.save()


# Alias standardisé
build_workbook_business_plan = generate_workbook_business_plan


if __name__ == "__main__":
    args = create_cli(
        description="Générer le livret interactif 'Mon Business Plan' (PDF).",
        default_output="Workbook_Business_Plan.pdf",
    )
    generate_workbook_business_plan(args.output, theme=args.theme)
