"""
Catalogue des livrets de référence proposés dans l'app (création et personnalisation).
Leur contenu est celui des PDF : les fichiers workbooks/<id>.json, compilés par le même
moteur (workbook_generator.compiler). Ce module n'ajoute que leur fiche d'affichage.
"""

from functools import lru_cache
from typing import List, Optional

from server.models import TemplateInfo, WorkbookSpec
from workbook_generator.spec import load_workbook

BILAN = "Bilan de Compétences"

# Fiche de chaque livret : (id, numéro, titre, sous-titre, description, icône, catégorie)
CATALOGUE = [
    ("carnet-1", 1, "Carnet 1 · L'état des lieux", "Cadre, point de situation, domaines de vie et héritages",
     "Préparer la séance 1 : cadre de travail, état des lieux rapide, domaines de vie, objectif de départ "
     "et ce que la personne a reçu de son milieu sur le travail.",
     "explore", BILAN),
    ("carnet-2", 2, "Carnet 2 · Mon parcours", "Expériences, travail réel, quatre zones, fil rouge et ligne de vie",
     "Préparer la séance 2 : objectif boussole, expériences avec ce qui donne de l'énergie et ce qui coûte, "
     "travail empêché, quatre zones, critères, moteurs, fil rouge, ligne de vie et compétences de vie.",
     "park", BILAN),
    ("carnet-3", 3, "Carnet 3 · Mes fonctionnements propres",
     "Test des fonctionnements cognitifs, 17 mises en situation et cartographie des énergies",
     "Préparer la séance 3, la restitution du test : énergie, information, décisions, temps et action, réactions "
     "sous pression, puis ce qui donne de l'énergie et ce qui use au travail.",
     "psychology", BILAN),
    # Former carnets 0 to 3, until the clean-up of the restructuring (R11)
    ("chap0", 0, "Carnet 0 · Le prélude (ancien parcours)", "Engagement, point de situation et entourage",
     "Poser le cadre et l'engagement, faire le point sur la situation actuelle, les domaines de vie et l'entourage.",
     "flag", BILAN),
    ("chap1", 1, "Carnet 1 · L'état des lieux (ancien parcours)",
     "Météo, vision à 360°, objectif boussole et héritages",
     "Fixer le point de départ : état d'esprit, domaines de vie, objectif boussole, sac à dos et héritages familiaux.",
     "explore", BILAN),
    ("chap2", 2, "Carnet 2 · Mon parcours (ancien parcours)",
     "Expériences, fil rouge, ligne de vie et arbre de vie",
     "Relire le parcours expérience par expérience, repérer le fil rouge et les moteurs, les compétences de vie.",
     "park", BILAN),
    ("chap3", 3, "Carnet 3 · Mes fonctionnements propres (ancien parcours)",
     "Énergie, information, décisions et rapport au temps",
     "Préparer la restitution du test des fonctionnements cognitifs : énergie, information, décisions, zone d'ombre.",
     "psychology", BILAN),
    ("chap4", 4, "Carnet 4 · Mon rapport à l'argent", "Histoire avec l'argent, seuils et tensions",
     "Situation actuelle, histoire avec l'argent, minimum financier acceptable et ce que l'argent représente.",
     "balance", BILAN),
    ("chap5", 5, "Carnet 5 · Valeurs et moteurs profonds", "Alignement, liste de valeurs et conditions de travail",
     "Expériences d'alignement et de désalignement, valeurs hiérarchisées, incarnées et traduites en conditions.",
     "favorite", BILAN),
    ("chap6", 6, "Carnet 6 · Phase d'exploration", "Cartographie, retour des proches et fiches métiers",
     "Cartographie personnelle, retour des proches, dix métiers à explorer et fiches métiers à confronter au réel.",
     "travel_explore", BILAN),
    ("livret", 7, "Livret de compétences", "Portfolio de compétences prouvées par des faits",
     "Préférences, travail réel, cartographie du métier, autonomie, récits d'action et plan de sécurité.",
     "workspace_premium", BILAN),
    ("business-plan", 99, "Mon business plan · De l'idée au projet viable",
     "Fondations, offre, marché, modèle économique, moyens et test",
     "Le livret complet pour structurer une création d'activité, tester son marché et obtenir ses premières ventes.",
     "business_center", "Entrepreneuriat"),
]


@lru_cache(maxsize=None)
def _reference_spec(template_id: str) -> WorkbookSpec:
    return load_workbook(template_id)


def get_predefined_spec(template_id: str) -> Optional[WorkbookSpec]:
    """Retourne une copie indépendante de la spécification de référence demandée."""
    if template_id not in {entry[0] for entry in CATALOGUE}:
        return None
    spec = _reference_spec(template_id)
    # Copie profonde via Pydantic pour ne jamais muter la référence en cache
    return WorkbookSpec.model_validate(spec.model_dump(exclude_unset=True))


def get_predefined_info_list() -> List[TemplateInfo]:
    """Retourne la liste des résumés de tous les modèles pré-intégrés."""
    return [
        TemplateInfo(id=template_id, chapter_num=num, title=title, subtitle=subtitle, description=description,
                     page_count=len(_reference_spec(template_id).pages), icon=icon, category=category,
                     parts=_reference_spec(template_id).parts or [])
        for template_id, num, title, subtitle, description, icon, category in CATALOGUE
    ]
