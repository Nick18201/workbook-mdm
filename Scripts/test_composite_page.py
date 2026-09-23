"""
Test script for the Atomic Design System & Composite Page Engine.
Renders spacious, airy, and elegant modular pages following MDM design principles:
- Max 2 to 3 atomic components per page
- Generous white space (breathing room)
- Large, comfortable AcroForm input areas
- Renders high-resolution PNGs for visual inspection
"""

import os
import sys
import pymupdf  # PyMuPDF

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "Scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from workbook_generator import (
    DocumentBuilder,
    PageLayout,
    LayoutConfig,
    PDFStyle,
    QuestionConfig,
)
from server.models import WorkbookSpec, PageSpec, BlockSpec
from server.pdf_compiler import compile_workbook_from_spec


def test_direct_composite_pages():
    output_pdf = os.path.join(PROJECT_ROOT, "Test_Composite_Page.pdf")
    builder = DocumentBuilder(output_path=output_pdf, theme="indigo")
    builder.set_title("Test Composite Pages - Système Atomique Aéré")

    # PAGE 1: Repères & Diagnostic (2 composants spacieux : Callout + Grille 2 Cartes)
    def page_1_renderer(c):
        layout = PageLayout(
            c,
            "Diagnostic & Leviers Stratégiques",
            config=LayoutConfig(part_title="1. REPÈRES & CLARIFICATION"),
        )
        # 1. Callout d'ancrage avec bel espace intérieur
        layout.add_callout(
            "Le principe de Pareto : 20% de vos actions ciblées génèrent 80% de vos résultats durables. Identifiez votre priorité absolue avant de vous disperser.",
            title="REPÈRE STRATÉGIQUE",
            variant="info",
        )
        # 2. Grille de 2 grandes cartes d'analyse (hauteur 5.8 cm) pour un confort d'écriture maximal
        layout.add_cards_grid(
            [
                {
                    "title": "Axe 1 : La Zone de Friction",
                    "subtitle": "Quelle situation ou tâche draine votre énergie ?",
                    "field_id": "axe1_friction",
                    "placeholder": "Ex : Les réunions de cadrage non structurées...",
                },
                {
                    "title": "Axe 2 : Le Levier Décisif",
                    "subtitle": "Quelle règle simple ou décision posez-vous dès aujourd'hui ?",
                    "field_id": "axe2_decision",
                    "placeholder": "Ex : Exiger un ordre du jour écrit 24h avant...",
                },
            ],
            columns=2,
            card_height=5.8 * 28.3465,
            field_prefix="card_diagnostic",
        )
        layout.render()

    # PAGE 2: Évaluation & Passage à l'Action (3 composants aérés : Jauge + Checklist + Question)
    def page_2_renderer(c):
        layout = PageLayout(
            c,
            "Évaluation & Passage à l'Action",
            config=LayoutConfig(part_title="2. PLAN OPÉRATIONNEL"),
        )
        # 1. Jauge d'évaluation 0-10 avec belle hauteur et bornes dégagées
        layout.add_scale_gauge(
            "Niveau de clarté actuel sur votre prochaine étape :",
            min_val=0,
            max_val=10,
            min_label="0 : Flou total",
            max_label="10 : Alignement absolu",
            field_id="clarte_scale",
        )
        # 2. Checklist de 3 critères avec interligne confortable
        layout.add_checklist(
            [
                ("Valider mon hypothèse auprès d'au moins 2 personnes de confiance", "chk_action_1"),
                ("Poser une date butoir ferme dans mon calendrier", "chk_action_2"),
                ("Partager ma décision avec mon accompagnateur ou mentor", "chk_action_3"),
            ],
            title="ENGAGEMENTS D'ICI 72 HEURES :",
            columns=1,
            field_prefix="chk_validation",
        )
        # 3. Question de recul auto-fit
        layout.add_question_block(
            "Quel est le bénéfice le plus motivant si vous tenez cet engagement ?",
            form_field_id="q_benefice_cle",
            config=QuestionConfig(
                subtitle="Visualisez l'impact concret sur votre quotidien et votre sérénité.",
                example="Ex : Retrouver du calme mental le soir et libérer mes vendredis après-midi.",
                box_height=3.5 * 28.3465,
                color=PDFStyle.COLOR_ACCENT_BLUE,
            ),
        )
        layout.render()

    # PAGE 3: Tableau de Bord & Métriques (2 composants : Stat Boxes + Tableau)
    def page_3_renderer(c):
        layout = PageLayout(
            c,
            "Tableau de Bord des Avancées",
            config=LayoutConfig(part_title="3. MESURE D'IMPACT"),
        )
        # 1. Rangée de 3 Stat Boxes
        layout.add_stat_boxes([
            {"stat": "80%", "label": "Impact prioritaire"},
            {"stat": "48h", "label": "Délai de décision"},
            {"stat": "100%", "label": "Engagement personnel"},
        ])
        # 2. Tableau spacieux de 3 lignes
        layout.add_table(
            headers=["Action Concrète", "Porteur / Rôle", "Échéance", "Preuve de Réussite"],
            rows=[
                [
                    {"field_id": "tbl_act_1", "placeholder": "Ex : Entretien réseau"},
                    {"field_id": "tbl_resp_1", "placeholder": "Moi-même"},
                    {"field_id": "tbl_ech_1", "placeholder": "15/10"},
                    {"field_id": "tbl_res_1", "placeholder": "3 Fiches contact remplies"},
                ],
                [
                    {"field_id": "tbl_act_2", "placeholder": "Ex : Rédaction proposition"},
                    {"field_id": "tbl_resp_2", "placeholder": "Avec mentor"},
                    {"field_id": "tbl_ech_2", "placeholder": "22/10"},
                    {"field_id": "tbl_res_2", "placeholder": "Document 2 pages validé"},
                ],
                [
                    {"field_id": "tbl_act_3", "placeholder": "Ex : Présentation test"},
                    {"field_id": "tbl_resp_3", "placeholder": "Binôme"},
                    {"field_id": "tbl_ech_3", "placeholder": "30/10"},
                    {"field_id": "tbl_res_3", "placeholder": "Retours qualitatifs notés"},
                ],
            ],
            col_widths=[6.5 * 28.3465, 3.5 * 28.3465, 2.5 * 28.3465, 4.5 * 28.3465],
            field_prefix="suivi_actions",
        )
        layout.render()

    builder.add_page(page_1_renderer)
    builder.add_page(page_2_renderer)
    builder.add_page(page_3_renderer)
    builder.save()
    print(f"Successfully generated direct PDF: {output_pdf}")
    return output_pdf


def test_spec_composite_compilation():
    """Validates compile_workbook_from_spec with an airy composite spec (2-3 blocks)."""
    spec = WorkbookSpec(
        chapter_num=5,
        chapter_title="Test Spécification Composite Aérée",
        subtitle="ASSEMBLAGE HARMONIEUX & RESPIRANT",
        theme="indigo",
        beneficiary_name="Alexandre",
        pages=[
            PageSpec(
                template="composite",
                title="Mon Plan d'Exploration Structuré",
                part_title="1. SYNTHÈSE & DÉCISIONS",
                blocks=[
                    BlockSpec(
                        type="callout",
                        title="CONSEIL PÉDAGOGIQUE",
                        text="Pour maximiser votre apprentissage, concentrez-vous sur deux axes complémentaires sans surcharger votre emploi du temps.",
                        variant="tip",
                    ),
                    BlockSpec(
                        type="cards_grid",
                        columns=2,
                        card_height_cm=5.2,
                        cards=[
                            {
                                "title": "Option A : La Voie Directe",
                                "subtitle": "Les opportunités immédiatement accessibles",
                                "field_id": "spec_opt_a",
                            },
                            {
                                "title": "Option B : L'Exploration Audacieuse",
                                "subtitle": "Le projet à fort impact à défricher",
                                "field_id": "spec_opt_b",
                            },
                        ],
                    ),
                    BlockSpec(
                        type="question",
                        question="Quel premier engagement formel prenez-vous pour avancer sur ces deux options ?",
                        field_id="q_spec_engagement",
                        subtitle="Formulez une intention concrète et mesurable.",
                        example="Ex : Bloquer 2 heures ce jeudi matin pour contacter 3 interlocuteurs.",
                        box_height_cm=3.2,
                    ),
                ],
            )
        ],
    )
    pdf_bytes = compile_workbook_from_spec(spec)
    assert len(pdf_bytes) > 5000, "PDF bytes should be substantial"
    spec_pdf_path = os.path.join(PROJECT_ROOT, "Test_Spec_Composite.pdf")
    with open(spec_pdf_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"Successfully compiled WorkbookSpec composite PDF: {spec_pdf_path} ({len(pdf_bytes)} bytes)")
    return spec_pdf_path


def render_pdf_to_images(pdf_path, output_dir, prefix="preview"):
    os.makedirs(output_dir, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    image_paths = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=150)
        out_path = os.path.join(output_dir, f"{prefix}_p{page_num+1}.png")
        pix.save(out_path)
        image_paths.append(out_path)
        print(f"Rendered page {page_num+1} to {out_path}")
    doc.close()
    return image_paths


if __name__ == "__main__":
    pdf1 = test_direct_composite_pages()
    pdf2 = test_spec_composite_compilation()

    artifacts_dir = r"C:\Users\nblum\.gemini\antigravity\brain\6263769c-38df-4954-b871-c361934e47b8"
    imgs1 = render_pdf_to_images(pdf1, artifacts_dir, prefix="airy_composite")
    imgs2 = render_pdf_to_images(pdf2, artifacts_dir, prefix="airy_spec")
    print("All airy tests and visual renderings completed successfully.")
