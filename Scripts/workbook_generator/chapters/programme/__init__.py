"""Package Programme du Bilan de Compétences - Marge de Manœuvre."""

from .common import create_closing_page
from .cover import create_programme_cover
from .page_deroule_1 import create_programme_page_deroule_1
from .page_deroule_2 import create_programme_page_deroule_2
from .page_deroule_3 import create_programme_page_deroule_3
from .page_deroule_4 import create_programme_page_deroule_4
from .page_projets import create_programme_page_projets
from .page_tarifs_financement import create_programme_page_tarifs
from .page_infos_pratiques import create_programme_page_infos_pratiques

# Alias numérotés pour flexibilité
create_programme_page_1 = create_programme_page_deroule_1
create_programme_page_2 = create_programme_page_deroule_2
create_programme_page_3 = create_programme_page_deroule_3
create_programme_page_4 = create_programme_page_deroule_4
create_programme_page_5 = create_programme_page_projets
create_programme_page_6 = create_programme_page_tarifs
create_programme_page_7 = create_programme_page_infos_pratiques

__all__ = [
    "create_programme_cover",
    "create_programme_page_deroule_1",
    "create_programme_page_deroule_2",
    "create_programme_page_deroule_3",
    "create_programme_page_deroule_4",
    "create_programme_page_projets",
    "create_programme_page_tarifs",
    "create_programme_page_infos_pratiques",
    "create_programme_page_1",
    "create_programme_page_2",
    "create_programme_page_3",
    "create_programme_page_4",
    "create_programme_page_5",
    "create_programme_page_6",
    "create_programme_page_7",
    "create_closing_page",
]
