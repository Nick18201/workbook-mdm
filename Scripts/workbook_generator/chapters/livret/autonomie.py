from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)


def create_autonomie_paliers_page(c):
    """
    P4.1 : MES DEGRÉS D'AISANCE & D'AUTONOMIE (Les 4 paliers d'autonomie expliqués et exercice miroir).
    """
    layout = PageLayout(
        c,
        "P4.1 : MES DEGRÉS D'AUTONOMIE EXPLIQUÉS",
        config=LayoutConfig(part_title="4. AUTONOMIE & TRANSFÉRABILITÉ"),
    )

    layout.add_text(
        "Face à une mission, nous ne sommes jamais « bon » ou « mauvais ». Nous évoluons selon 4 paliers naturels :\n"
        "• Niveau 1 (Guidé) : J'apprends les bases, j'ai besoin de consignes claires et d'un référent pour me rassurer.\n"
        "• Niveau 2 (Autonome) : Je réalise mon travail courant seul et je résous les petits imprévus habituels sans aide.\n"
        "• Niveau 3 (Améliorateur) : Je maîtrise très bien : je crée des astuces, je simplifie les méthodes et j'aide mes pairs.\n"
        "• Niveau 4 (Référent) : Je suis la personne ressource : je forme les autres, j'explique le métier et j'arbitre.",
        config=TextConfig(font_size=9, spacing_after=0.4 * cm),
    )

    layout.add_question_block(
        "Où se situent mes Compétences Clés ?",
        "livret_p4_paliers",
        config=QuestionConfig(
            box_height=4.5 * cm,
            subtitle="Choisissez 2 ou 3 de vos compétences phares : à quel niveau (1, 2, 3 ou 4) vous situez-vous aujourd'hui et pourquoi ?",
            example="Ex : Modélisation technique : Niveau 3 (Améliorateur) — je conçois des outils partagés pour fluidifier le travail de l'équipe.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "L'Épreuve du Miroir (Ce qui me paraît évident)",
        "livret_p4_miroir",
        config=QuestionConfig(
            box_height=4.5 * cm,
            subtitle="Qu'est-ce qui vous semble tellement naturel dans votre métier qu'un débutant mettrait des mois à assimiler ?",
            example="Ex : Repérer une incohérence thermique d'un simple coup d'œil sur un plan sans avoir besoin de tout recalculer.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()


def create_autonomie_transfert_page(c):
    """
    P4.2 : MON PASSEPORT DE COMPÉTENCES TRANSFÉRABLES.
    """
    layout = PageLayout(
        c,
        "P4.2 : MON PASSEPORT DE TRANSFÉRABILITÉ",
        config=LayoutConfig(part_title="4. AUTONOMIE & TRANSFÉRABILITÉ"),
    )

    layout.add_text(
        "Qu'est-ce qu'une compétence transférable ? C'est un savoir-faire ou une méthode que vous pouvez "
        "« décrocher » de votre poste actuel pour l'« accrocher » avec succès dans un univers professionnel "
        "totalement différent (ex : la pédagogie, le chiffrage, l'organisation de projets, l'audit de qualité).",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "Mes Savoir-Faire Tout-Terrain",
        "livret_p4_transferabilite",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Quelles sont les 3 grandes compétences méthodologiques ou humaines que vous possédez "
            "et qui marcheraient instantanément dans un tout autre secteur ?",
            example="Ex : Diagnostic d'efficacité énergétique, animation d'ateliers pédagogiques pour adultes, chiffrage financier de dossiers.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Dans Quels Nouveaux Métiers Pourraient-elles Servir ?",
        "livret_p4_metiers_cibles",
        config=QuestionConfig(
            box_height=5.0 * cm,
            subtitle="Imaginez des contextes, structures ou métiers (même différents du vôtre) où ces compétences "
            "feraient de vous un candidat précieux.",
            example="Ex : Enseignant technique en lycée/CFA, économe de flux territorial en collectivité, conseiller technique en coopérative (CAE).",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()
