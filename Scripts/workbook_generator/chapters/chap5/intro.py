from workbook_generator.components import create_cover_page, create_standard_summary_page
from workbook_generator.config import PDFStyle
from workbook_generator.templates import PageLayout, LayoutConfig


def create_valeurs_cover(c):
    """Cover of chapter 5: Valeurs et moteurs profonds."""
    create_cover_page(c, "Valeurs et moteurs *profonds.*", number=5, tagline="Bilan de compétences",
                      promise="Ce qui doit compter dans votre prochain poste.")


def create_concept_page(c):
    """Chapter opener: the objective of the workbook and its exercises."""
    intro_txt = (
        "Ce carnet identifie les valeurs qui guident réellement vos choix, votre énergie et votre rapport au "
        "travail, puis les traduit en conditions de travail concrètes pour évaluer vos futures pistes."
    )
    exercises = [
        "Exercice 1 · Vos expériences d'alignement.",
        "Exercice 2 · Vos expériences de désalignement.",
        "Exercice 3 · Vos choix difficiles.",
        "Exercice 4 · Nommer ce qui compte : la liste de valeurs.",
        "Exercice 5 · Hiérarchiser vos valeurs.",
        "Exercice 6 · Incarner vos valeurs non négociables.",
        "Exercice 7 · Traduire vos valeurs en conditions de travail.",
        "Exercice 8 · Vos tensions de valeurs.",
        "Exercice 9 · Synthèse.",
    ]
    create_standard_summary_page(c, "5", "Ce qui compte *vraiment.*", intro_txt, exercises)


def create_intro_page(c):
    """Introduction: where values show, and what the workbook looks for."""
    layout = PageLayout(c, "Comprendre *vos valeurs.*", config=LayoutConfig(part_title="Introduction"))
    layout.add_paragraphs([
        "Ce carnet vous aide à identifier ce qui compte vraiment pour vous dans votre vie professionnelle.",
        "Les valeurs ne sont pas des idées abstraites. Elles se repèrent dans les situations où vous vous sentez :",
    ], size=PDFStyle.SIZE_LEAD)
    layout.add_star_list(["motivé·e ;", "fier ou fière ;", "utile ;", "libre ;", "reconnu·e ;", "en confiance ;"],
                         size=PDFStyle.SIZE_LEAD, spacing_after=0.3 * 28.35)
    layout.add_paragraphs([
        "mais aussi frustré·e, en colère, vidé·e, empêché·e ou en conflit intérieur.",
    ], size=PDFStyle.SIZE_LEAD)
    layout.add_callout(
        "Ne cherchez pas les valeurs qui semblent les plus « belles » ou les plus attendues : identifiez celles "
        "qui influencent réellement vos choix, votre énergie et votre rapport au travail.",
        title="L'objectif",
    )
    layout.render()
