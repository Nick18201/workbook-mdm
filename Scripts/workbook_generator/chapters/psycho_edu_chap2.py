import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

from ..config import PDFStyle
from ..components import (
    draw_page_background, draw_dot_grid, draw_card, draw_side_panel, 
    draw_leaf, draw_title, draw_branding_logo, draw_section_separator,
    create_standard_cover, draw_circular_stamp, draw_pause_badge, draw_page_decorations
)
from ..forms import create_input_field

def create_psycho_edu_pages(c):
    """
    Psycho-education pages: Comprendre ses Racines.
    Expanded to 3 pages to cover all content from Psycho-education.md.
    """
    width, height = A4
    
    # --- PAGE 1: INTRO & HABITUS ---
    # Side Panel (Full Height)
    card_margin = 2*cm
    draw_side_panel(c, card_margin, width, height)
    draw_title(c, "Comprendre ses Racines", card_margin + 0.5*cm, height - 2.5*cm)
    c.setFont(PDFStyle.FONT_SUBTITLE, 12)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(card_margin + 0.5*cm, height - 3.2*cm, "Pour choisir son avenir")

    text_x = card_margin + 0.5*cm
    text_y = height - 4.5*cm
    line_height = 14 # Slightly tighter
    
    def draw_paragraph_block(canvas, title, lines, y_start, color_title=PDFStyle.COLOR_ACCENT_RED):
        curr_y = y_start
        if title:
            canvas.setFont(PDFStyle.FONT_SUBTITLE, 12)
            canvas.setFillColor(color_title)
            canvas.drawString(text_x, curr_y, title)
            curr_y -= line_height * 1.5
        
        canvas.setFont(PDFStyle.FONT_BODY, 10)
        canvas.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        for line in lines:
            if line.strip() == "":
                curr_y -= line_height * 0.5
            else:
                canvas.drawString(text_x, curr_y, line)
                curr_y -= line_height
        return curr_y - line_height * 1.5

    # Introduction
    intro_lines = [
        "Dans un bilan de compétences, on pense souvent qu'il suffit de lister ses savoir-faire pour trouver sa",
        "voie. C'est une erreur. Vous n'êtes pas seulement une somme de compétences techniques ; vous êtes",
        "le résultat d'une histoire.",
        "",
        "Votre façon de travailler, votre rapport à l'argent, à l'autorité ou à la réussite ne viennent pas de",
        "nulle part. Ils ont été façonnés par votre famille et votre milieu d'origine. Ce document a pour but",
        "de vous aider à repérer ces « bagages invisibles » pour faire le tri : que voulez-vous garder ?",
        "Que devez-vous laisser au vestiaire pour enfin vous épanouir professionnellement ?"
    ]
    text_y = draw_paragraph_block(c, "Introduction : Pourquoi regarder en arrière ?", intro_lines, text_y)

    habitus_lines = [
        "Imaginez que vous avez un logiciel installé en vous depuis l'enfance. Ce logiciel, c'est l'Habitus :",
        "votre manière spontanée de réagir, de parler, de vous tenir, héritée de vos parents et de votre",
        "milieu social.",
        "",
        "Pourquoi c'est important ? Si vous changez de milieu professionnel (exemple : d'une famille",
        "d'ouvriers vers un poste de cadre, ou l'inverse), ce logiciel peut bugger.",
        "Vous pouvez ressentir un décalage permanent, une gêne, comme si vous portiez un costume mal taillé."
    ]
    text_y = draw_paragraph_block(c, "1. Le « Sac à Dos » Social (L'Habitus)", habitus_lines, text_y)

    # Sentiment d'illégitimité
    imposteur_lines = [
        "« Un jour, ils vont se rendre compte que je ne suis pas à la hauteur »...",
        "C'est souvent le signe d'une Névrose de Classe. Ce n'est pas une maladie, mais un conflit intérieur.",
        "",
        "• Le Parvenu : Si vous réussissez mieux que vos parents, vous pouvez ressentir une culpabilité",
        "  (peur de les abandonner).",
        "• Le Déclassé : Si votre situation est moins prestigieuse, vous pouvez ressentir de la honte.",
        "",
        "Ce sentiment freine : il peut empêcher de demander une augmentation ou pousser à l'épuisement."
    ]
    text_y = draw_paragraph_block(c, "Le sentiment d'illégitimité (Syndrome de l'Imposteur)", imposteur_lines, text_y, color_title=PDFStyle.COLOR_TEXT_MAIN)

    draw_page_decorations(c, width, height, part_title="2. MES RACINES", x_offset=card_margin)
    c.showPage()
    
    # --- PAGE 2: CONTRAT & SOUFFRANCE ---
    draw_page_background(c, width, height)
    draw_side_panel(c, card_margin, width, height)
    draw_title(c, "Comprendre ses Racines (suite)", text_x, height - 2.5*cm)
    text_y = height - 4.5*cm

    contrat_lines = [
        "Chaque famille possède un « Grand Livre de Comptes » invisible. On y inscrit ce que l'on doit",
        "à ses parents.",
        "",
        "• Les Loyautés Invisibles (Le « Pilote Automatique ») :",
        "  Parfois, on s'auto-sabote juste avant le but. Pourquoi ? Peut-être pour ne pas dépasser",
        "  inconsciemment ses parents. L'échec devient une façon de dire « Je reste comme vous ».",
        "",
        "• La Réparation :",
        "  Avez-vous choisi votre métier par passion ou pour réparer un drame familial (injustice, maladie) ?",
        "",
        "• Le Mythe Familial :",
        "  « Chez nous, on est des intellectuels », « Chez nous, on est solidaires... ».",
        "  Si votre projet contredit ce mythe, vous rencontrerez une résistance interne."
    ]
    text_y = draw_paragraph_block(c, "2. Le Contrat Familial Secret", contrat_lines, text_y)

    souffrance_lines = [
        "Le travail, ce n'est pas juste exécuter une tâche. C'est y mettre du sien.",
        "Quand on ne peut pas faire son travail « bien » (selon ses propres critères), on souffre.",
        "C'est l'activité empêchée.",
        "",
        "Votre souffrance n'est pas une faiblesse. C'est un signal d'intelligence : elle montre que",
        "vous tenez à ce que vous faites.",
        "Le but est de transformer cette plainte en pouvoir d'agir : retrouver une marge de manœuvre."
    ]
    text_y = draw_paragraph_block(c, "3. La Souffrance et le Plaisir au Travail", souffrance_lines, text_y)

    draw_page_decorations(c, width, height, part_title="2. MES RACINES", x_offset=card_margin)
    c.showPage()

    # --- PAGE 3: PISTES ET OUTILS ---
    draw_page_background(c, width, height)
    draw_side_panel(c, card_margin, width, height)
    draw_title(c, "Les Outils pour Avancer", text_x, height - 2.5*cm)
    text_y = height - 4.5*cm

    pistes_lines = [
        "Voici trois pistes pour débloquer votre situation et transformer votre héritage :",
        ""
    ]
    text_y = draw_paragraph_block(c, "4. Pistes pour votre Bilan", pistes_lines, text_y)

    # A. Génogramme du Coeur
    geno_lines = [
        "Ne restez pas seul avec votre arbre généalogique officiel. Identifiez vos « tuteurs de résilience ».",
        "Qui vous a donné confiance ? Qui vous a transmis des valeurs positives ?",
        "Appuyez-vous sur eux plutôt que sur les figures qui vous ont jugé."
    ]
    text_y = draw_paragraph_block(c, "A. Le Génogramme du Cœur", geno_lines, text_y, color_title=PDFStyle.COLOR_ACCENT_BLUE)

    # B. Roman Familial
    roman_lines = [
        "Repérez les répétitions et les « phrases poisons » (« Il faut souffrir pour réussir »).",
        "Prendre conscience de ces phrases, c'est ne plus les laisser diriger votre vie."
    ]
    text_y = draw_paragraph_block(c, "B. Le Roman Familial", roman_lines, text_y, color_title=PDFStyle.COLOR_ACCENT_BLUE)

    # C. Objectif
    obj_lines = [
        "L'objectif est de Réussir sans Trahir.",
        "Vous avez le droit de changer, de réussir, de gagner de l'argent, sans que cela soit une insulte",
        "à votre famille.",
        "Comment honorer les valeurs familiales (courage, honnêteté) sous une forme qui VOUS appartient ?",
        "C'est la différenciation : rester en lien, tout en étant libre d'être soi-même."
    ]
    text_y = draw_paragraph_block(c, "C. L'Objectif : La Différenciation", obj_lines, text_y, color_title=PDFStyle.COLOR_ACCENT_BLUE)

    # Conclusion Box
    draw_card(c, card_margin + 0.5*cm, text_y - 3*cm, width - card_margin - 1.5*cm, 2.5*cm)
    c.setFont(PDFStyle.FONT_ITALIC, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    center_x = card_margin + (width - card_margin) / 2.0
    c.drawCentredString(center_x, text_y - 1.5*cm, "En éclairant ces zones d'ombre, vous transformez")
    c.drawCentredString(center_x, text_y - 2*cm, "des chaînes invisibles en tremplins.")

    draw_page_decorations(c, width, height, part_title="2. MON PARCOURS", x_offset=card_margin)
    c.showPage()
