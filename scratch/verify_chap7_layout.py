import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if os.path.join(PROJECT_ROOT, "Scripts") not in sys.path:
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "Scripts"))

import fitz
from server.models import WorkbookSpec, PageSpec, BlockSpec
from server.pdf_compiler import compile_workbook_from_spec as compile_workbook_to_pdf

chap7_spec = WorkbookSpec(
    chapter_num=7,
    chapter_title="De l'exploration terrain au choix validé",
    subtitle="LE CHAMP DES POSSIBLES",
    theme="indigo",
    beneficiary_name="Thomas",
    pages=[
        # 1. Cover
        PageSpec(
            template="cover",
            title="BILAN DE COMPÉTENCES & ALIGNEMENT",
            params={
                "subtitle": "LE CHAMP DES POSSIBLES",
                "title": "Chapitre 7 : De l'exploration terrain au choix validé",
            },
        ),
        # 2. Summary
        PageSpec(
            template="summary",
            title="Sommaire du Chapitre",
            params={
                "num": "7",
                "intro_text": "Ce chapitre constitue le pivot stratégique de votre démarche. Après l'immersion sur le terrain et le recueil d'expériences directes, vous prenez le temps de trier, d'analyser vos enseignements et de consolider un choix professionnel aligné et soutenable.",
                "points": [
                    ("01.", "L'entonnoir des idées : filtrer les pistes et assumer des renoncements lucides"),
                    ("02.", "Le reality check : confronter ses croyances initiales aux réalités du marché"),
                    ("03.", "Le crash test de viabilité : mesurer concrètement la faisabilité globale"),
                    ("04.", "L'arbitrage Plan A / Plan B : sceller le cap prioritaire et sécuriser l'alternative"),
                    ("05.", "Mon pacte d'action : s'engager avec discernement, audace et responsabilité"),
                ],
            },
        ),
        # 3. Questions
        PageSpec(
            template="questions",
            title="L'Entonnoir des Idées",
            part_title="1. CONVERGENCE",
            params={
                "intro_text": "L'exploration terrain vous a permis d'ouvrir grand les portes. Le moment est venu de faire converger vos réflexions : choisir, c'est aussi renoncer sereinement pour concentrer son énergie sur ce qui fait sens.",
                "questions": [
                    {
                        "question": "Quelles sont les 3 pistes phares explorées lors de vos démarches de terrain ?",
                        "subtitle": "Listez les options investiguées en précisant leur attractivité principale.",
                        "example": "Ex : Responsable RSE en PME, consultant indépendant en transition, chef de projet territorial.",
                        "field_id": "p7_q1",
                    },
                    {
                        "question": "Quelle piste décidez-vous d'écarter en priorité et pour quelles raisons objectives ?",
                        "subtitle": "Formulez un renoncement déculpabilisant fondé sur vos valeurs et vos constats.",
                        "example": "Ex : Consultant solo écarté car le besoin de collectif et la stabilité relationnelle priment.",
                        "field_id": "p7_q2",
                    },
                    {
                        "question": "Quelle est la pépite qui émerge comme votre évidence pour la suite de l'aventure ?",
                        "subtitle": "La direction qui conjugue motivation profonde, compétences transférables et opportunité réelle.",
                        "example": "Ex : Pilote de programmes à impact au sein d'une structure associative ou coopérative.",
                        "field_id": "p7_q3",
                    },
                ],
            },
        ),
        # 4. Reality Check Composite
        PageSpec(
            template="composite",
            title="Le Reality Check Terrain",
            part_title="2. CONFRONTATION",
            blocks=[
                BlockSpec(
                    type="callout",
                    title="PAROLE D'EXPERT & ENSEIGNEMENT CLÉ",
                    text="« Le terrain ne valide pas nos illusions, il éclaire nos forces véritables et révèle les règles tacites du jeu. Notez ici la parole la plus percutante ou le conseil décisif reçu lors de vos échanges. »",
                    variant="quote",
                ),
                BlockSpec(
                    type="cards_grid",
                    columns=2,
                    card_height_cm=4.5,
                    cards=[
                        {"title": "LE MYTHE INITIAL", "subtitle": "Ce que j'imaginais avant l'enquête de terrain", "field_id": "c_mythe"},
                        {"title": "LA RÉALITÉ CONSTATÉE", "subtitle": "Ce que les professionnels m'ont concrètement révélé", "field_id": "c_realite"},
                    ],
                ),
                BlockSpec(
                    type="scale",
                    label="Indice de viabilité et de confiance globale suite aux retours terrain :",
                    min_val=0,
                    max_val=10,
                    min_label="0 · Décalage trop fort",
                    max_label="10 · Pleine concordance et confiance",
                    field_id="sc_viabilite",
                ),
            ],
        ),
        # 5. Crash Test de Viabilité Composite
        PageSpec(
            template="composite",
            title="Le Crash Test de Viabilité",
            part_title="3. DÉCISION",
            blocks=[
                BlockSpec(
                    type="table",
                    title="Matrice de Faisabilité Opérationnelle",
                    headers=["PILIER ANALYSÉ", "NIVEAU DE RISQUE", "PLAN DE PARADE OU LEVIER D'ACTION IDENTIFIÉ"],
                    rows=[
                        ["Finances & Rémunération minimale", "🟡 Modéré", "Maintien ARE, négociation salariale, réduction des charges fixes."],
                        ["Temps, Rythme & Équilibre personnel", "🟢 Faible", "Télétravail partiel, limitation des temps de trajet hebdomadaires."],
                        ["Compétences clés & Passerelles", "🟡 Modéré", "Micro-formation ciblée, mise en avant du transfert d'expérience."],
                        ["Dynamique & Besoins réels du marché", "🟢 Porteur", "Cibler le marché caché via le réseau d'alumni et pairs experts."],
                    ],
                ),
                BlockSpec(
                    type="cards_grid",
                    columns=2,
                    card_height_cm=3.6,
                    cards=[
                        {"title": "PLAN A · L'ÉTOILE (PRIORITÉ ABSOLUE)", "subtitle": "La direction dans laquelle j'investis mon énergie", "field_id": "c_plan_a"},
                        {"title": "PLAN B · LE FILET (SÉRÉNITÉ ACTIVE)", "subtitle": "L'option alternative sécurisante en réserve", "field_id": "c_plan_b"},
                    ],
                ),
            ],
        ),
        # 6. Engagement
        PageSpec(
            template="engagement",
            title="Pacte d'Action & de Clarté",
            part_title="4. ALIGNEMENT",
            params={
                "lines": [
                    "J'assume pleinement mes renoncements pour concentrer toute ma force sur mon choix validé.",
                    "Je fonde mon jugement sur les faits observés sur le terrain plutôt que sur mes craintes imaginaires.",
                    "J'investis ma pleine énergie dans mon Plan A tout en gardant mon Plan B prêt et rassurant.",
                    "J'accepte les ajustements tactiques nécessaires sans jamais dévier de mes valeurs fondamentales.",
                    "Cette décision est le résultat d'un arbitrage conscient, courageux et profondément aligné.",
                ]
            },
        ),
        # 7. Closing
        PageSpec(
            template="closing",
            title="Clôture",
            params={
                "messages": [
                    "Félicitations pour cette étape d'arbitrage décisive et structurée.",
                    "Le doute cède désormais la place à une intention claire, mesurée et enthousiasmante.",
                    "Rendez-vous à la prochaine séance pour transformer cette vision en plan d'action opérationnel.",
                ]
            },
        ),
    ],
)


def main():
    print("Compiling Chapter 7 test PDF...")
    pdf_bytes = compile_workbook_to_pdf(chap7_spec)
    out_pdf = os.path.join(PROJECT_ROOT, "scratch", "chap7_fixed.pdf")
    with open(out_pdf, "wb") as f:
        f.write(pdf_bytes)
    print(f"Saved PDF to {out_pdf} ({len(pdf_bytes)} bytes)")

    doc = fitz.open(out_pdf)
    print(f"Total pages: {len(doc)}")
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(PROJECT_ROOT, "scratch", f"chap7_fixed_p{i+1}.png")
        pix.save(img_path)
        print(f"Rendered page {i+1} to {img_path}")

    print("\n[SUCCESS] Chapter 7 compilation and image rendering completed!")


if __name__ == "__main__":
    main()
