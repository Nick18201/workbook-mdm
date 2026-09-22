"""
Test Suite & Showcase for the 8 Universal Workbook Templates.
Generates 'Test_All_Templates.pdf' displaying every template in production conditions.
"""

import os
import sys

# Ensure Scripts directory is in python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from workbook_generator import (
    DocumentBuilder,
    PDFStyle,
    PageLayout,
    LayoutConfig,
    QuestionItem,
    TextConfig,
    create_standard_cover,
    create_standard_summary_page,
    create_standard_engagement_page,
    create_standard_meteo_page,
    create_standard_quadrants_page,
    create_standard_two_columns_page,
    create_closing_page,
)


def page_1_cover(c):
    create_standard_cover(
        c,
        subtitle="DÉMONSTRATION DES 8 GABARITS UNIVERSELS",
        title="CATALOGUE DU DESIGN SYSTEM REPORTLAB",
    )


def page_2_summary(c):
    points = [
        ("Sommaire des Gabarits :", ""),
        ("1.", "Gabarit Couverture (Brand & Illustration)"),
        ("2.", "Gabarit Sommaire & Intentions (Fond Indigo & Filigrane)"),
        ("3.", "Gabarit Questions Auto-Fit (2 Questions équilibrées)"),
        ("4.", "Gabarit Questions Auto-Fit (3 Questions + Exemples ombrés)"),
        ("5.", "Gabarit Météo Intérieure & Jauge Énergie (0-10 + Émotions)"),
        ("6.", "Gabarit Matrice & 4 Quadrants (Vision 360°)"),
        ("7.", "Gabarit 2 Colonnes Miroir (Comparatif & Passerelle)"),
        ("8.", "Gabarit Engagement Moral & Signature"),
        ("9.", "Gabarit Clôture & Ancrage"),
    ]
    create_standard_summary_page(
        c,
        chapter_num_str="DS",
        chapter_title="DESIGN SYSTEM",
        intro_text=(
            "Ce document valide l'auto-calibrage et l'étanchéité visuelle des 8 gabarits "
            "universels. Chaque composant s'adapte automatiquement à son contenu sans "
            "jamais déborder sur les marges inférieures ou les décorations de pied de page."
        ),
        points_list=points,
    )


def page_3_two_questions_autofit(c):
    layout = PageLayout(
        c,
        "Exercice à 2 Questions Auto-Fit",
        config=LayoutConfig(part_title="3. QUESTIONS AUTO-FIT (2Q)"),
    )
    layout.add_text(
        "Ce gabarit détecte automatiquement qu'il n'y a que 2 questions et agrandit "
        "la hauteur des zones de saisie pour occuper harmonieusement l'espace vertical disponible.",
        config=TextConfig(spacing_after=0.6 * 28.35),  # 0.6 cm in points
    )

    questions = [
        QuestionItem(
            question="1. Quelle a été votre plus grande prise de conscience professionnelle cette année ?",
            form_field_id="demo_2q_1",
            subtitle="Pensez aux moments de bascule, aux réussites inattendues ou aux frustrations révélatrices.",
        ),
        QuestionItem(
            question="2. Si vous deviez résumer votre cap pour les 6 prochains mois en une intention claire ?",
            form_field_id="demo_2q_2",
            subtitle="Une phrase courte, affirmative et engageante.",
            example="Ex : 'Je priorise les missions où mon autonomie stratégique est respectée.'",
        ),
    ]
    layout.add_questions_group(questions)
    layout.render()


def page_4_three_questions_autofit(c):
    layout = PageLayout(
        c,
        "Exercice à 3 Questions Auto-Fit",
        config=LayoutConfig(part_title="4. QUESTIONS AUTO-FIT (3Q)"),
    )
    layout.add_text(
        "Avec 3 questions, le moteur réduit proportionnellement la hauteur des champs pour garantir "
        "une marge de sécurité stricte au-dessus de la pagination.",
        config=TextConfig(spacing_after=0.4 * 28.35),
    )

    questions = [
        QuestionItem(
            question="1. L'environnement idéal : Où et avec qui travaillez-vous le plus efficacement ?",
            form_field_id="demo_3q_1",
            subtitle="Décrivez l'ambiance sonore, l'autonomie et le style de management.",
        ),
        QuestionItem(
            question="2. Le déclencheur d'irritation : Qu'est-ce qui vous fait perdre patience immédiatement ?",
            form_field_id="demo_3q_2",
            example="Ex : Les réunions sans ordre du jour ou les consignes contradictoires.",
        ),
        QuestionItem(
            question="3. La ressource inexploitée : Quel talent utilisez-vous dans votre vie personnelle mais pas au travail ?",
            form_field_id="demo_3q_3",
            subtitle="Créativité, négociation, écoute, organisation d'événements...",
        ),
    ]
    layout.add_questions_group(questions)
    layout.render()


def page_5_meteo(c):
    create_standard_meteo_page(
        c,
        title="Ma Météo Intérieure & Énergie",
        part_title="5. MÉTÉO DE DÉPART",
        emotion_prompt="Aujourd'hui, mon état d'esprit dominant :",
        energy_prompt="Mon niveau d'énergie actuel :",
        thought_prompt="Ce qui occupe le plus d'espace mental en arrivant :",
        field_prefix="test_meteo",
    )


def page_6_quadrants(c):
    create_standard_quadrants_page(
        c,
        title="Matrice d'Alignement 360°",
        part_title="6. LES 4 QUADRANTS",
        instruction="Instruction : Pour chaque domaine de votre équilibre, formulez votre priorité absolue.",
        quadrants_data=[
            ("Impact & Mission", "Sens, utilité, rémunération", "demo_quad_impact"),
            ("Santé & Énergie", "Sommeil, sport, récupération", "demo_quad_sante"),
            ("Relations & Entourage", "Alliés, famille, réseau", "demo_quad_relations"),
            ("Liberté & Cadre", "Horaires, télétravail, autonomie", "demo_quad_liberte"),
        ],
        field_prefix="demo_quad",
    )


def page_7_two_columns(c):
    create_standard_two_columns_page(
        c,
        title="Passerelle : Du Frein au Levier",
        part_title="7. DEUX COLONNES MIROIR",
        intro_text=(
            "Identifiez les croyances ou situations qui vous ralentissent, et traduisez-les "
            "immédiatement en compétences ou en décisions ressources."
        ),
        col1_header="Croyance Limitante / Situation Subie",
        col2_header="Croyance Ressource / Levier Concret",
        rows_data=[
            (
                "1. Légitimité professionnelle",
                "Ex : 'Je ne coche pas 100% des critères'",
                "Ex : 'Ma valeur réside dans ma capacité à apprendre vite'",
            ),
            (
                "2. Demande de rémunération",
                "Ex : 'Parler d'argent est inconfortable'",
                "Ex : 'Ma contribution génère des résultats mesurables'",
            ),
            (
                "3. Poser ses limites",
                "Ex : 'Si je dis non, on va douter de mon engagement'",
                "Ex : 'Dire non à l'accessoire me permet de dire oui à l'essentiel'",
            ),
            (
                "4. Transition de carrière",
                "Ex : 'Recommencer à zéro me fait peur'",
                "Ex : 'Je ne repars pas de zéro, je capitalise sur 10 ans d'acquis'",
            ),
        ],
        field_prefix="demo_twocol",
    )


def page_8_engagement(c):
    create_standard_engagement_page(
        c,
        part_title="8. MON ENGAGEMENT",
        title="Mon Pacte avec Moi-Même",
        custom_lines=[
            "Je m'engage à accorder à cette démarche toute l'attention qu'elle mérite.",
            "À accueillir mes doutes avec lucidité et sans jugement hâtif.",
            "À tester de nouvelles approches avant de conclure sur leur faisabilité.",
            "À célébrer chaque petite victoire sur le chemin de mon alignement.",
            "",
            "Ce travail d'exploration m'appartient et engage mon avenir.",
        ],
    )


def page_9_closing(c):
    create_closing_page(c)


def build_test_suite_pdf(output_filename="Test_All_Templates.pdf", theme="indigo"):
    builder = DocumentBuilder(output_path=output_filename, theme=theme)
    builder.set_title("Test Suite - 8 Universal Templates")

    # Add all 9 pages
    builder.add_page(page_1_cover)
    builder.add_page(page_2_summary)
    builder.add_page(page_3_two_questions_autofit)
    builder.add_page(page_4_three_questions_autofit)
    builder.add_page(page_5_meteo)
    builder.add_page(page_6_quadrants)
    builder.add_page(page_7_two_columns)
    builder.add_page(page_8_engagement)
    builder.add_page(page_9_closing)

    builder.save()


if __name__ == "__main__":
    output_pdf = os.path.join(os.path.dirname(CURRENT_DIR), "Test_All_Templates.pdf")
    build_test_suite_pdf(output_filename=output_pdf)
