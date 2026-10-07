"""Package Programme du Bilan de Compétences - Marge de Manœuvre."""

from workbook_generator.components import create_closing_page
from .cover import create_programme_cover
from .page_objectifs import create_programme_page_objectifs
from .page_deroule import (
    create_programme_page_deroule_1,
    create_programme_page_deroule_2,
    create_programme_page_deroule_3,
    create_programme_page_deroule_4,
)
from .page_projets import create_programme_page_projets
from .page_organisation_pedagogie import create_programme_page_organisation_pedagogie
from .page_accompagnateurs import create_programme_page_accompagnateurs
from .page_tarifs_financement import create_programme_page_tarifs
from .page_infos_pratiques import create_programme_page_infos_pratiques
from .page_indicateurs_satisfaction import create_programme_page_indicateurs_satisfaction

# Alias numérotés séquentiels (Pages 1 à 12)
create_programme_page_1 = create_programme_cover
create_programme_page_2 = create_programme_page_objectifs
create_programme_page_3 = create_programme_page_deroule_1
create_programme_page_4 = create_programme_page_deroule_2
create_programme_page_5 = create_programme_page_deroule_3
create_programme_page_6 = create_programme_page_deroule_4
create_programme_page_7 = create_programme_page_projets
create_programme_page_8 = create_programme_page_organisation_pedagogie
create_programme_page_9 = create_programme_page_accompagnateurs
create_programme_page_10 = create_programme_page_tarifs
create_programme_page_11 = create_programme_page_infos_pratiques
create_programme_page_12 = create_programme_page_indicateurs_satisfaction

__all__ = [
    "create_programme_cover",
    "create_programme_page_objectifs",
    "create_programme_page_deroule_1",
    "create_programme_page_deroule_2",
    "create_programme_page_deroule_3",
    "create_programme_page_deroule_4",
    "create_programme_page_projets",
    "create_programme_page_organisation_pedagogie",
    "create_programme_page_accompagnateurs",
    "create_programme_page_tarifs",
    "create_programme_page_infos_pratiques",
    "create_programme_page_indicateurs_satisfaction",
    "create_programme_page_1",
    "create_programme_page_2",
    "create_programme_page_3",
    "create_programme_page_4",
    "create_programme_page_5",
    "create_programme_page_6",
    "create_programme_page_7",
    "create_programme_page_8",
    "create_programme_page_9",
    "create_programme_page_10",
    "create_programme_page_11",
    "create_programme_page_12",
    "create_closing_page",
]
