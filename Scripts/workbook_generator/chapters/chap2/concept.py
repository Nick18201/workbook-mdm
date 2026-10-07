from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit

from ...config import PDFStyle
from ...components import (
    draw_page_background,
    draw_card,
    draw_side_panel,
    draw_title,
    draw_page_decorations,
)


def create_psycho_edu_pages(c):
    """
    Psycho-education pages: Comprendre ses Racines.
    Expanded to 3 pages to cover all content from Psycho-education.md.
    """
    width, height = A4
    card_margin = 2 * cm
    text_x = card_margin + 1.0 * cm
    text_top = height - 4.0 * cm
    target_width = width - text_x - 1.2 * cm
    line_height = 14

    def draw_paragraph_block(
        canvas, title, lines, y_start, color_title=PDFStyle.COLOR_ACCENT_RED
    ):
        curr_y = y_start
        if title:
            canvas.setFont(PDFStyle.FONT_SUBTITLE, 12)
            canvas.setFillColor(color_title)
            canvas.drawString(text_x, curr_y, title)
            curr_y -= line_height * 1.4

        canvas.setFont(PDFStyle.FONT_BODY, 10)
        canvas.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        for item in lines:
            if not item.strip():
                curr_y -= line_height * 0.4
            else:
                for sub in item.split("\n"):
                    if not sub.strip():
                        curr_y -= line_height * 0.4
                    else:
                        wrapped_lines = simpleSplit(sub, PDFStyle.FONT_BODY, 10, target_width)
                        for line in wrapped_lines:
                            canvas.drawString(text_x, curr_y, line)
                            curr_y -= line_height
        return curr_y - line_height * 1.0

    # --- PAGE 1: INTRO & HABITUS ---
    draw_page_background(c, width, height)
    draw_side_panel(c, card_margin, width, height)
    new_y = draw_title(
        c, "Comprendre ses racines.", pos=(text_x, text_top)
    )
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, new_y - 0.2 * cm, "Pour choisir la suite en connaissance de cause")

    text_y = new_y - 1.2 * cm

    # Introduction
    intro_lines = [
        "Lister vos savoir-faire ne suffit pas pour décider de la suite. Vous n'êtes pas une somme de compétences techniques : vous êtes aussi le résultat d'une histoire.",
        "",
        "Votre façon de travailler, votre rapport à l'argent, à l'autorité ou à la réussite ont été façonnés par votre famille et votre milieu d'origine. Ces pages vous aident à repérer ces « bagages invisibles » et à faire le tri : ce que vous gardez, et ce que vous laissez de côté pour votre projet.",
    ]
    text_y = draw_paragraph_block(
        c, "Pourquoi regarder en arrière ?", intro_lines, text_y
    )

    habitus_lines = [
        "L'habitus, c'est votre manière spontanée de réagir, de parler, de vous tenir, héritée de vos parents et de votre milieu social. Il agit comme un logiciel installé depuis l'enfance.",
        "",
        "Quand vous changez de milieu professionnel (d'une famille d'ouvriers à un poste de cadre, ou l'inverse), ce logiciel peut créer un décalage : une gêne diffuse, l'impression de porter un costume mal taillé.",
    ]
    text_y = draw_paragraph_block(
        c, "1. Le « sac à dos » social (l'habitus)", habitus_lines, text_y
    )

    # Sentiment d'illégitimité
    illegitimite_lines = [
        "« Un jour, ils vont se rendre compte que je ne suis pas à la hauteur. » Cette pensée signale souvent un conflit lié au changement de milieu social, ce que la sociologie appelle la névrose de classe. Ce n'est pas une maladie.",
        "",
        "• Vous réussissez mieux que vos parents : vous pouvez ressentir de la culpabilité, la peur de vous éloigner d'eux.",
        "• Votre situation est moins prestigieuse que la leur : vous pouvez ressentir de la honte.",
        "",
        "Ce sentiment a des effets concrets : il peut vous retenir de demander une augmentation, ou vous pousser au surmenage.",
    ]
    text_y = draw_paragraph_block(
        c,
        "Le sentiment d'illégitimité",
        illegitimite_lines,
        text_y,
        color_title=PDFStyle.COLOR_TEXT_MAIN,
    )

    draw_page_decorations(
        c, width, height, part_title="2. MES RACINES", x_offset=card_margin
    )
    c.showPage()

    # --- PAGE 2: CONTRAT & SOUFFRANCE ---
    draw_page_background(c, width, height)
    draw_side_panel(c, card_margin, width, height)
    new_y = draw_title(
        c, "Comprendre ses racines. (suite)", pos=(text_x, text_top)
    )
    text_y = new_y - 1.0 * cm

    contrat_lines = [
        "Chaque famille tient un « livre de comptes » invisible : ce que l'on pense devoir à ses parents.",
        "",
        "• Les loyautés invisibles :\n  il arrive de s'arrêter juste avant le but, pour ne pas dépasser ses parents. L'échec devient une façon de leur rester fidèle.",
        "",
        "• La réparation :\n  avez-vous choisi votre métier par goût, ou pour réparer une histoire familiale (injustice, maladie) ?",
        "",
        "• Le mythe familial :\n  « Chez nous, on est des intellectuels », « Chez nous, on est solidaires… ».\n  Un projet qui contredit ce mythe rencontre des résistances, chez vous comme autour de vous.",
    ]
    text_y = draw_paragraph_block(
        c, "2. Le contrat familial implicite", contrat_lines, text_y
    )

    souffrance_lines = [
        "Travailler, ce n'est pas seulement exécuter une tâche : c'est y mettre du sien. Quand vous ne pouvez pas faire votre travail « bien », selon vos propres critères, vous en souffrez. La psychologie du travail parle d'activité empêchée.",
        "",
        "Cette souffrance n'est pas une faiblesse : elle montre que vous tenez à la qualité de votre travail. L'enjeu est de la transformer en pouvoir d'agir, c'est-à-dire de retrouver une marge de manœuvre.",
    ]
    text_y = draw_paragraph_block(
        c, "3. Souffrance et plaisir au travail", souffrance_lines, text_y
    )

    draw_page_decorations(
        c, width, height, part_title="2. MES RACINES", x_offset=card_margin
    )
    c.showPage()

    # --- PAGE 3: PISTES ET OUTILS ---
    draw_page_background(c, width, height)
    draw_side_panel(c, card_margin, width, height)
    new_y = draw_title(c, "Trois outils pour avancer.", pos=(text_x, text_top))
    text_y = new_y - 1.0 * cm

    pistes_lines = [
        "Trois outils pour faire le tri dans votre héritage et décider en connaissance de cause :",
    ]
    text_y = draw_paragraph_block(c, "4. Pistes pour votre bilan", pistes_lines, text_y)

    # A. Supports in the family history
    geno_lines = [
        "Au-delà de l'arbre généalogique officiel, repérez les personnes qui vous ont donné confiance ou transmis des repères solides. Appuyez-vous sur elles plutôt que sur celles qui vous ont jugé.",
    ]
    text_y = draw_paragraph_block(
        c,
        "A. Vos appuis dans l'histoire familiale",
        geno_lines,
        text_y,
        color_title=PDFStyle.COLOR_ACCENT_BLUE,
    )

    # B. Roman Familial
    roman_lines = [
        "Repérez les répétitions et les phrases qui reviennent (« Il faut souffrir pour réussir »). Les identifier, c'est les empêcher de décider à votre place.",
    ]
    text_y = draw_paragraph_block(
        c,
        "B. Le roman familial",
        roman_lines,
        text_y,
        color_title=PDFStyle.COLOR_ACCENT_BLUE,
    )

    # C. Objectif
    obj_lines = [
        "Vous avez le droit de changer, de réussir, de gagner de l'argent, sans renier votre famille. La question devient : comment garder ses valeurs (courage, honnêteté) sous une forme qui vous appartient ? C'est la différenciation : rester en lien, tout en décidant pour vous-même.",
    ]
    text_y = draw_paragraph_block(
        c,
        "C. L'objectif : réussir sans trahir",
        obj_lines,
        text_y,
        color_title=PDFStyle.COLOR_ACCENT_BLUE,
    )

    # Conclusion Box
    card_w = width - card_margin - 2.0 * cm
    card_h = 2.5 * cm
    card_y = text_y - 2.8 * cm
    draw_card(c, text_x, card_y, card_w, card_h)
    c.setFont(PDFStyle.FONT_ITALIC, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    center_x = text_x + card_w / 2.0
    c.drawCentredString(
        center_x, card_y + 1.4 * cm, "Repérer ces héritages,"
    )
    c.drawCentredString(
        center_x, card_y + 0.8 * cm, "c'est reprendre la main sur vos choix."
    )

    draw_page_decorations(
        c, width, height, part_title="2. MON PARCOURS", x_offset=card_margin
    )
    c.showPage()
