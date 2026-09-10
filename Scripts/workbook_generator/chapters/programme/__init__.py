"""Package Programme du Bilan de Compétences - Marge de Manœuvre."""

from .common import create_programme_cover, create_closing_page
from .page_objectifs import create_programme_page_1
from .page_introspection import create_programme_page_2
from .page_exploration import create_programme_page_3
from .page_organisation_pedagogie import create_programme_page_4
from .page_accompagnateurs import (
    create_programme_page_5,
    create_programme_page_accompagnateurs,
)
from .page_formules_tarifs import create_programme_page_6
from .page_financement_suivi import create_programme_page_7
from .page_acces_cabinet import create_programme_page_8
from .page_indicateurs_satisfaction import create_programme_page_9

__all__ = [
    "create_programme_cover",
    "create_programme_page_1",
    "create_programme_page_2",
    "create_programme_page_3",
    "create_programme_page_4",
    "create_programme_page_5",
    "create_programme_page_accompagnateurs",
    "create_programme_page_6",
    "create_programme_page_7",
    "create_programme_page_8",
    "create_programme_page_9",
    "create_closing_page",
]
