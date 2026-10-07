from reportlab.lib.units import cm

from workbook_generator.components import create_standard_engagement_page
from workbook_generator.primitives import pastel_cycle
from workbook_generator.templates import PageLayout, LayoutConfig


def create_ressources_page(c):
    """Useful resources to explore jobs, with clickable links."""
    layout = PageLayout(c, "Ressources *pour vos recherches.*", config=LayoutConfig(part_title="Ressources"))
    layout.add_paragraphs([
        "Quelques ressources pour explorer les métiers et compléter vos fiches.",
    ], spacing_after=0.45 * cm)
    pastels = pastel_cycle(c)
    layout.add_link_card("Le quotidien des métiers (audio, vidéo)", [
        ("Into the Job", "https://podcast.ausha.co/into-the-job",
         "podcast, des témoignages concrets sur le quotidien professionnel."),
        ("Maintenant j'aime le lundi", "https://www.youtube.com/c/Maintenantjaimelelundi/playlists",
         "YouTube, des parcours, des reconversions et des métiers."),
    ], color=pastels[0])
    layout.add_link_card("Des fiches métiers complètes", [
        ("APEC", "https://www.apec.fr/tous-nos-metiers.html",
         "les métiers cadres, les fonctions support et le management."),
        ("Cadremploi", "https://www.cadremploi.fr/editorial/conseils/fiches-metiers.html",
         "une vue synthétique des missions, des compétences et des salaires."),
        ("ONISEP", "https://www.onisep.fr/decouvrir-les-metiers",
         "les formations, les secteurs et les débouchés."),
        ("CIDJ", "https://www.cidj.com/metiers/metiers-par-centres-d-interets",
         "des listes de métiers classées par centres d'intérêt."),
        ("MétierScope (France Travail)", "https://candidat.pole-emploi.fr/metierscope/centres-interet",
         "des métiers par centres d'intérêt, avec l'état du marché."),
    ], color=pastels[1])
    layout.add_link_card("Votre espace Notion", [
        ("Vos ressources Notion", "https://www.notion.so/Vos-ressources-aca96b6474d04acd9eaafa92523df7a6",
         "toutes les ressources et les guides pratiques du bilan."),
    ], color=pastels[2])
    layout.render()


def create_livrable_page(c):
    """End of the workbook: the deliverable validated in session, and the commitments."""
    create_standard_engagement_page(
        c,
        "Fin de carnet",
        custom_lines=[
            "Je complète au moins une fiche métier par semaine.",
            "Je confronte chaque piste à mes valeurs et à mon minimum financier.",
            "Je contacte un professionnel pour chacune de mes pistes réalistes.",
        ],
        livrable_title="Vos pistes métiers",
        livrable_text="Vos dix pistes et leurs fiches métiers, prêtes à être confrontées au terrain, validées en séance.",
        field_prefix="livrable_chap6",
    )
