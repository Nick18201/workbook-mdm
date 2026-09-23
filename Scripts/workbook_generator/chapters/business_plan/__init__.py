"""
Package modulaire du Workbook 'Mon Business Plan — De l'idée au projet viable'.
Architecture en 35 pages structurée selon la norme 1 dossier = 1 livret du projet MDM.
"""

from .cover import (
    create_business_plan_cover,
    create_business_plan_summary,
)
from .fondations import (
    create_fondations_idee_page,
    create_fondations_vision_page,
)
from .cible_probleme import (
    create_cible_public_page,
    create_cible_persona_page,
    create_probleme_analyse_page,
    create_probleme_hypotheses_page,
)
from .offre_marche import (
    create_offre_definition_page,
    create_offre_valeur_page,
    create_marche_tendances_page,
    create_marche_concurrents_page,
    create_marche_benchmark_page,
)
from .positionnement import (
    create_positionnement_identite_page,
    create_positionnement_pitch_page,
)
from .modele_commercial import (
    create_modele_revenus_page,
    create_modele_canvas_page,
    create_commercial_offres_page,
    create_commercial_prix_page,
    create_commercial_acquisition_page,
    create_commercial_parcours_page,
)
from .organisation_finances import (
    create_communication_message_page,
    create_communication_plan_page,
    create_ressources_moyens_page,
    create_ressources_competences_page,
    create_juridique_cadre_page,
    create_finances_depenses_page,
    create_finances_previsionnel_page,
    create_finances_financement_page,
)
from .action_synthese import (
    create_action_mvp_page,
    create_action_risques_page,
    create_action_roadmap_page,
    create_synthese_executive_page,
    create_engagement_signature_page,
)

__all__ = [
    # Couverture & Cadrage
    "create_business_plan_cover",
    "create_business_plan_summary",
    # 1. Fondations
    "create_fondations_idee_page",
    "create_fondations_vision_page",
    # 2 & 3. Cible & Problème
    "create_cible_public_page",
    "create_cible_persona_page",
    "create_probleme_analyse_page",
    "create_probleme_hypotheses_page",
    # 4, 5 & 6. Offre, Marché & Benchmark
    "create_offre_definition_page",
    "create_offre_valeur_page",
    "create_marche_tendances_page",
    "create_marche_concurrents_page",
    "create_marche_benchmark_page",
    # 7. Positionnement
    "create_positionnement_identite_page",
    "create_positionnement_pitch_page",
    # 8, 9, 10 & 11. Modèle & Vente
    "create_modele_revenus_page",
    "create_modele_canvas_page",
    "create_commercial_offres_page",
    "create_commercial_prix_page",
    "create_commercial_acquisition_page",
    "create_commercial_parcours_page",
    # 12, 13, 14, 15, 16 & 17. Communication, Moyens & Finances
    "create_communication_message_page",
    "create_communication_plan_page",
    "create_ressources_moyens_page",
    "create_ressources_competences_page",
    "create_juridique_cadre_page",
    "create_finances_depenses_page",
    "create_finances_previsionnel_page",
    "create_finances_financement_page",
    # 18, 19, 20, 21 & 22. Action & Synthèse
    "create_action_mvp_page",
    "create_action_risques_page",
    "create_action_roadmap_page",
    "create_synthese_executive_page",
    "create_engagement_signature_page",
]
