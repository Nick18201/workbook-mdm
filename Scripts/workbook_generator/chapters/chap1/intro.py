import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.forms import create_input_field
from workbook_generator.components import (
    create_standard_cover,
    draw_title,
    draw_page_decorations,
    draw_side_panel,
    create_standard_engagement_page,
    create_standard_summary_page,
)
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig, QuestionConfig

def create_chap1_cover(c):
    """
    Cover Page for Chapter 1: L'État des Lieux.
    """
    create_standard_cover(c, "CHAPITRE 1 : L'ÉTAT DES LIEUX")




def create_engagement_page(c):
    """
    Page 1: Mon Engagement.
    Text heavy page with signature.
    """
    create_standard_engagement_page(c, "1. MON ENGAGEMENT")




def create_concept_page(c):
    """
    Page 2: Chapter Cover - 1. Concept
    Blue background, large watermark.
    """
    # Points
    points = [
        ("Sommaire :", ""),
        ("1.", "Mon Engagement"),
        ("2.", "Ma Météo Intérieure"),
        ("3.", "Ma Vision 360°"),
        ("4.", "Mon Objectif Boussole"),
        ("5.", "Le Sac à Dos"),
        ("6.", "Mon Héritage"),
        ("7.", "Image du Monde du Travail"),
        ("8.", "Mentors & Anti-Modèles"),
    ]

    create_standard_summary_page(c, "1", "CONCEPT", "", points)
