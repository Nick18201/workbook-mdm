"""
Catalogue des livrets de référence proposés dans l'app (création et personnalisation).
Leur contenu est celui des PDF : les fichiers workbooks/<id>.json, compilés par le même
moteur (workbook_generator.compiler). Ce module n'ajoute que leur fiche d'affichage.
"""

import threading
from functools import lru_cache
from typing import List, Optional

from server.models import TemplateInfo, WorkbookSpec
from workbook_generator.compiler import reference_page_count
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
    ("carnet-4", 4, "Carnet 4 · Mon rapport à l'argent",
     "Profil validé, histoire avec l'argent, idées reçues et quatre seuils",
     "Préparer la séance 4 : le profil validé en séance 3, la situation et l'histoire avec l'argent, les idées "
     "reçues face aux faits, l'aisance à demander, les quatre seuils et la tendance dominante.",
     "balance", BILAN),
    ("carnet-5", 5, "Carnet 5 · Valeurs et moteurs profonds",
     "Situations vécues, liste de valeurs, tensions et grille anti-compromis",
     "Préparer la séance 5 : alignement, désalignement et choix difficiles, la liste de valeurs, la hiérarchie, "
     "les tensions, la grille anti-compromis (trois valeurs traduites en conditions), l'entourage et la question "
     "aux proches.",
     "favorite", BILAN),
    ("carnet-6", 6, "Carnet 6 · L'exploration",
     "Cartographie en reports, retour des proches, ressources et dix pistes",
     "Préparer la séance 6 : ce que la personne sait d'elle sur une page, les métiers suggérés par ses proches, "
     "les ressources pour explorer, puis dix pistes, cinq réalistes et cinq audacieuses, et ses trois favorites.",
     "travel_explore", BILAN),
    ("carnet-7", 7, "Carnet 7 · Confronter au terrain",
     "Trois fiches à critères, enquêtes métier, comptes rendus et matrice de faisabilité",
     "Préparer les séances 7 et 8, en deux parties : les trois pistes retenues face aux critères (valeurs, "
     "minimum, énergie), la grille d'entretien et trois contacts, puis les comptes rendus d'enquête, ce que le "
     "terrain apprend, la matrice de faisabilité et les compromis acceptables.",
     "handshake", BILAN),
    ("carnet-de-route", 8, "Carnet de route · Décider et agir",
     "Profil en reports, compétences prouvées, récits, pistes A et B, feuilles de route et premières actions",
     "Préparer les séances 9 et 10, en deux parties : le profil, les compétences prouvées et deux récits d'action, "
     "puis les pistes A et B face aux critères, les feuilles de route à 30, 60 et 90 jours, le module du projet, "
     "les premières actions, les garde-fous et le chemin parcouru.",
     "route", BILAN),
    ("module-creation", 8, "Carnet de route · Module création",
     "Fondations, offre, prix, point mort face aux seuils, risque, financement et test",
     "Pour une piste A de création d'activité, entre les séances 9 et 10 : le problème et l'offre, le prix, les "
     "dépenses et les charges, le point mort face aux quatre seuils, le risque pour la personne, le financement, "
     "le test et les entretiens prospects, puis la synthèse et la décision.",
     "storefront", BILAN),
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


# Compter les pages compile chaque livret (quelques secondes pour le catalogue, puis en cache) :
# un seul calcul à la fois, pour qu'une requête attende celui du démarrage au lieu de le refaire
_page_count_lock = threading.Lock()


def get_predefined_info_list() -> List[TemplateInfo]:
    """
    Retourne la liste des résumés de tous les modèles pré-intégrés. Leur nombre de pages est
    celui du PDF, pages « (suite) » comprises.
    """
    with _page_count_lock:
        page_counts = {entry[0]: reference_page_count(entry[0]) for entry in CATALOGUE}
    return [
        TemplateInfo(id=template_id, chapter_num=num, title=title, subtitle=subtitle, description=description,
                     page_count=page_counts[template_id], icon=icon, category=category,
                     parts=_reference_spec(template_id).parts or [])
        for template_id, num, title, subtitle, description, icon, category in CATALOGUE
    ]


def count_pages_in_background():
    """Calcule les nombres de pages dès le démarrage du serveur, sans le retarder."""
    threading.Thread(target=get_predefined_info_list, name="nombres-de-pages", daemon=True).start()
