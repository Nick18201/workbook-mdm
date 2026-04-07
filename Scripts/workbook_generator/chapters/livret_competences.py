from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from workbook_generator.config import PDFStyle
from workbook_generator.components import (
    draw_page_background,
    draw_side_panel,
    draw_title,
    draw_page_decorations,
    create_standard_cover,
    TitleStyle
)
from workbook_generator.forms import create_input_field

def create_livret_cover(c):
    """
    Couverture du Livret de Compétences Augmenté.
    """
    create_standard_cover(c, "Portfolio Dynamique de Potentiel", title="LIVRET DE COMPÉTENCES AUGMENTÉ")


def _draw_instruction_text(c, text, x, y, max_width):
    """Helper to draw multi-line instruction text using Paragraph for better wrapping."""
    style = ParagraphStyle(
        'Instruction',
        fontName=PDFStyle.FONT_BODY,
        fontSize=11,
        leading=15,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
        alignment=TA_LEFT
    )
    # Prévenir les sauts de ligne isolant la ponctuation typo française
    text = text.replace(' ?', '&nbsp;?').replace(' !', '&nbsp;!').replace(' :', '&nbsp;:')
    
    p = Paragraph(text, style)
    w, h = p.wrap(max_width, 1000)
    p.drawOn(c, x, y - h)
    return y - h


def _draw_form_section(c, form, current_y, title, text, input_name, input_height, content_x, content_w):
    current_y = draw_title(c, title, pos=(content_x, current_y), style=TitleStyle(size=16, color=PDFStyle.COLOR_ACCENT_RED))
    current_y = _draw_instruction_text(c, text, content_x, current_y - 0.3 * cm, content_w)
    
    current_y -= 0.5 * cm # Espacement avant la case
    
    create_input_field(form, input_name, pos=(content_x, current_y - input_height), size=(content_w, input_height), multiline=True)
    
    # On renvoie la position Y sous la box, avec une marge pour la section suivante
    return current_y - input_height - 1.2 * cm


def create_profil_page(c):
    """
    P1 : PROFIL (Qui je suis)
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)
    
    content_x = card_margin + 1.0 * cm
    content_w = width - content_x - 1.5 * cm
    current_y = height - 4.0 * cm
    
    current_y = draw_title(c, "P1 : PROFIL (Qui je suis)", pos=(content_x, current_y), style=TitleStyle(size=22))
    current_y = _draw_instruction_text(c, "Cartographie de votre identité professionnelle, au-delà de l'intitulé de poste.", content_x, current_y - 0.5 * cm, content_w)
    
    current_y -= 1.0 * cm
    form = c.acroForm
    
    current_y = _draw_form_section(c, form, current_y, "ADN : Valeurs & Moteurs", 
                                   "Quelles sont vos valeurs phares et ce qui vous donne de l'énergie ?", 
                                   'profil_adn', 3.5 * cm, content_x, content_w)
                                   
    current_y = _draw_form_section(c, form, current_y, "Style : Mode de collaboration", 
                                   "Décrivez votre type de personnalité (ex: MBTI) et vos conditions idéales de collaboration.", 
                                   'profil_style', 3.5 * cm, content_x, content_w)
                                   
    current_y = _draw_form_section(c, form, current_y, "Boussole : Vision à 3-5 ans", 
                                   "Vers quoi souhaitez-vous tendre professionnellement à moyen terme ?", 
                                   'profil_boussole', 3.5 * cm, content_x, content_w)
    
    draw_page_decorations(c, width, height, part_title="LIVRET DE COMPÉTENCES", x_offset=card_margin)
    c.showPage()


def create_parcours_page(c):
    """
    P2 : PARCOURS (D'où je viens)
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)
    
    content_x = card_margin + 1.0 * cm
    content_w = width - content_x - 1.5 * cm
    current_y = height - 4.0 * cm
    
    current_y = draw_title(c, "P2 : PARCOURS (D'où je viens)", pos=(content_x, current_y), style=TitleStyle(size=22))
    current_y = _draw_instruction_text(c, "Lecture narrative et analytique de votre expérience.", content_x, current_y - 0.5 * cm, content_w)
    
    current_y -= 1.0 * cm
    form = c.acroForm
    
    current_y = _draw_form_section(c, form, current_y, "Fil Rouge & Génogramme Pro", 
                                   "Quel est le narratif qui relie vos expériences ? Quels héritages ont influencé vos choix ?", 
                                   'parcours_fil', 6.0 * cm, content_x, content_w)
                                   
    current_y = _draw_form_section(c, form, current_y, "Carte aux Trésors : Top Compétences", 
                                   "Listez vos compétences clés (Hard & Soft) par niveau de maîtrise.", 
                                   'parcours_competences', 8.0 * cm, content_x, content_w)
    
    draw_page_decorations(c, width, height, part_title="LIVRET DE COMPÉTENCES", x_offset=card_margin)
    c.showPage()


def create_preuves_page(c):
    """
    P3 : PREUVES (Ce que j'ai réalisé)
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)
    
    content_x = card_margin + 1.0 * cm
    content_w = width - content_x - 1.5 * cm
    current_y = height - 4.0 * cm
    
    current_y = draw_title(c, "P3 : PREUVES (Réalisations)", pos=(content_x, current_y), style=TitleStyle(size=22))
    current_y = _draw_instruction_text(c, "Sélection de Chef-d'œuvres et Faits Marquants illustrant l'approche STAR.", content_x, current_y - 0.5 * cm, content_w)
    
    current_y -= 1.0 * cm
    form = c.acroForm
    
    current_y = _draw_form_section(c, form, current_y, "Situation - Tâche - Action - Résultat (STAR)", 
                                   "Détaillez ici 1 à 2 réalisations majeures qui démontrent votre valeur.", 
                                   'preuves_star', 8.0 * cm, content_x, content_w)
                                   
    current_y = _draw_form_section(c, form, current_y, "Témoignages & Verbatim", 
                                   "Citations de collègues, managers ou clients (issus d'un 360° par exemple).", 
                                   'preuves_temoignages', 6.0 * cm, content_x, content_w)
    
    draw_page_decorations(c, width, height, part_title="LIVRET DE COMPÉTENCES", x_offset=card_margin)
    c.showPage()


def create_potentiel_page(c):
    """
    P4 : POTENTIEL (Où je vais)
    """
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)
    
    content_x = card_margin + 1.0 * cm
    content_w = width - content_x - 1.5 * cm
    current_y = height - 4.0 * cm
    
    current_y = draw_title(c, "P4 : POTENTIEL (Où je vais)", pos=(content_x, current_y), style=TitleStyle(size=22))
    current_y = _draw_instruction_text(c, "Projection vers l'avenir : adaptabilité et apprentissage (Learning Agility).", content_x, current_y - 0.5 * cm, content_w)
    
    current_y -= 1.0 * cm
    form = c.acroForm
    
    current_y = _draw_form_section(c, form, current_y, "Projet Cible & Transférabilité", 
                                   "Quel est l'environnement, la mission et la culture recherchés ? En quoi vos compétences y répondent ?", 
                                   'potentiel_projet', 6.0 * cm, content_x, content_w)
                                   
    current_y = _draw_form_section(c, form, current_y, "Plan de Développement", 
                                   "Quelles compétences sont en cours d'acquisition ou prévues ?", 
                                   'potentiel_dev', 6.0 * cm, content_x, content_w)
    
    draw_page_decorations(c, width, height, part_title="LIVRET DE COMPÉTENCES", x_offset=card_margin)
    c.showPage()
