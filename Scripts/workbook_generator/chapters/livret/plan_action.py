from reportlab.lib.units import cm
from workbook_generator.config import PDFStyle
from workbook_generator.templates import (
    PageLayout,
    LayoutConfig,
    QuestionConfig,
    TextConfig,
)


def create_plan_securite_page(c):
    """
    P7.1 : MON CADRE DE SÉCURITÉ & MES DEUX PISTES DE PROJET.
    """
    layout = PageLayout(
        c,
        "P7.1 : CADRE DE SÉCURITÉ & DEUX PISTES",
        config=LayoutConfig(part_title="7. MON PLAN D'ÉMANCIPATION"),
    )

    layout.add_text(
        "Pour avancer l'esprit libre, il ne faut jamais se mettre en insécurité. "
        "Poser clairement vos impératifs matériels et familiaux est le premier rempart contre le stress. "
        "À partir de ce socle solide, nous dessinons deux chemins complémentaires.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "Mon Cadre de Sécurité Non-Négociable",
        "livret_p7_securite",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Vos critères de sérénité obligatoires : salaire net minimum vital pour le foyer, "
            "temps de trajet maximal (ex : 20 min max), préservation de votre rythme familial.",
            example="Ex : Maintien du revenu net cadre indispensable, temps de route limité à 20 min, aucun découchage, disponibilité pour mes 3 enfants.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Mes Deux Pistes de Travail (Projet A & Projet B)",
        "livret_p7_pistes",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Piste A (votre projet d'élan, de transmission et de sens) vs Piste B (votre projet refuge "
            "ou tremplin sécurisant).",
            example="Ex : Piste A : Enseignant / formateur technique | Piste B : Économe de flux territorial ou conseil indépendant en coopérative (CAE).",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()


def create_plan_pas_proximal_page(c):
    """
    P7.2 : MON « PROCHAIN PETIT PAS » À 7 JOURS & MES BESOINS D'AIDE.
    """
    layout = PageLayout(
        c,
        "P7.2 : PROCHAIN PETIT PAS & BESOINS",
        config=LayoutConfig(part_title="7. MON PLAN D'ÉMANCIPATION"),
    )

    layout.add_text(
        "Le plus grand piège d'une reconversion est de viser une montagne lointaine et de se sentir paralysé. "
        "Le secret de l'action réside dans le « pas proximal » : une toute petite démarche, simple et garantie "
        "à 100 %, réalisable dans les 7 prochains jours.",
        config=TextConfig(spacing_after=0.6 * cm),
    )

    layout.add_question_block(
        "Mon « Pas Proximal » (Action Concrète à 7 Jours)",
        "livret_p7_pas_proximal",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Quelle est la toute petite action (un coup de fil de 10 min, vérifier son compte CPF, contacter un pair) "
            "que vous vous engagez à réaliser d'ici notre prochain rendez-vous ?",
            example="Ex : Consulter le solde de mes droits CPF et envoyer un message à un ancien collègue devenu formateur pour prendre la température.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_RED,
        ),
    )

    layout.add_question_block(
        "Mes Besoins d'Étayage & Formations Courtes",
        "livret_p7_formation",
        config=QuestionConfig(
            box_height=5.2 * cm,
            subtitle="Quels modules courts (quelques dizaines d'heures finançables CPF), conseils ou démarches "
            "vous donneraient une pleine sérénité pour franchir le pas ?",
            example="Ex : Module court de pédagogie pour adultes (30 heures éligibles CPF) pour valider la posture d'animation sans surcharger mon emploi du temps.",
            color_alternation=False,
            color=PDFStyle.COLOR_ACCENT_BLUE,
        ),
    )

    layout.render()
