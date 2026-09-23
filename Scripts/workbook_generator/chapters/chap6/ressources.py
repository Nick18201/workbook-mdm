from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from workbook_generator.config import PDFStyle
from workbook_generator.components import draw_card
from workbook_generator.templates import PageLayout, LayoutConfig, TextConfig


def _get_hex(color):
    if hasattr(color, "hexval"):
        val = color.hexval
        if callable(val):
            val = val()
        if val.startswith("#"):
            return val
        return f"#{val}"
    try:
        rgb = color.rgb()
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
    except Exception:
        return "#2F2EFA"


def _draw_paragraph(c, text, pos, width, style):
    p = Paragraph(text, style)
    w, h = p.wrap(width, 1000)
    p.drawOn(c, pos[0], pos[1] - h)
    return h


def create_ressources_page(c):
    """
    Page 11 : Ressources utiles pour vos recherches
    """
    layout = PageLayout(
        c,
        "Ressources utiles pour vos recherches",
        config=LayoutConfig(part_title="5. RESSOURCES UTILES"),
    )
    layout.add_text(
        "Voici quelques ressources recommandées pour explorer les métiers et enrichir vos fiches pratiques.",
        config=TextConfig(spacing_after=0.4 * cm),
    )

    y = layout.y_cursor
    x = layout.text_x
    w = layout.target_width

    # Link Style
    style = ParagraphStyle(
        "RessourcesParagraphStyle",
        fontName=PDFStyle.FONT_BODY,
        fontSize=9,
        leading=13,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
    )
    link_color = _get_hex(PDFStyle.COLOR_TEXT_MAIN)

    # Card 1: Témoignages & Podcasts
    h1 = 2.8 * cm
    draw_card(c, x, y - h1, w, h1)
    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "DÉCOUVRIR LE QUOTIDIEN DES MÉTIERS (AUDIOS / VIDÉOS)")
    
    t1 = f'• <a href="https://podcast.ausha.co/into-the-job"><font color="{link_color}"><b><u>Into the Job</u></b></font></a> (podcast) : Témoignages concrets sur le quotidien professionnel.'
    _draw_paragraph(c, t1, (x + 0.3 * cm, y - 1.2 * cm), w - 0.6 * cm, style)
    
    t2 = f'• <a href="https://www.youtube.com/c/Maintenantjaimelelundi/playlists"><font color="{link_color}"><b><u>Maintenant j\'aime le lundi</u></b></font></a> (YouTube) : Découvrir des parcours, des reconversions et des métiers.'
    _draw_paragraph(c, t2, (x + 0.3 * cm, y - 2.0 * cm), w - 0.6 * cm, style)

    y = y - h1 - 0.4 * cm

    # Card 2: Fiches Métiers
    h2 = 5.2 * cm
    draw_card(c, x, y - h2, w, h2)
    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "CONSULTER DES FICHES MÉTIERS COMPLÈTES")
    
    t3 = f'• <a href="https://www.apec.fr/tous-nos-metiers.html"><font color="{link_color}"><b><u>APEC</u></b></font></a> : Utile pour les métiers cadres, les fonctions supports et le management.'
    _draw_paragraph(c, t3, (x + 0.3 * cm, y - 1.1 * cm), w - 0.6 * cm, style)
    
    t4 = f'• <a href="https://www.cadremploi.fr/editorial/conseils/fiches-metiers.html"><font color="{link_color}"><b><u>Cadremploi</u></b></font></a> : Vision synthétique des missions, compétences et salaires.'
    _draw_paragraph(c, t4, (x + 0.3 * cm, y - 1.9 * cm), w - 0.6 * cm, style)
    
    t5 = f'• <a href="https://www.onisep.fr/decouvrir-les-metiers"><font color="{link_color}"><b><u>ONISEP</u></b></font></a> : Informations sur les formations, les secteurs et les débouchés.'
    _draw_paragraph(c, t5, (x + 0.3 * cm, y - 2.7 * cm), w - 0.6 * cm, style)
    
    t6 = f'• <a href="https://www.cidj.com/metiers/metiers-par-centres-d-interets"><font color="{link_color}"><b><u>CIDJ</u></b></font></a> : Exploration de listes de métiers classées par centres d\'intérêt.'
    _draw_paragraph(c, t6, (x + 0.3 * cm, y - 3.5 * cm), w - 0.6 * cm, style)
    
    t7 = f'• <a href="https://candidat.pole-emploi.fr/metierscope/centres-interet"><font color="{link_color}"><b><u>MétierScope (Pôle Emploi)</u></b></font></a> : Recherche de métiers par goût et état du marché.'
    _draw_paragraph(c, t7, (x + 0.3 * cm, y - 4.3 * cm), w - 0.6 * cm, style)

    y = y - h2 - 0.4 * cm

    # Card 3: Notion Link
    h3 = 1.8 * cm
    draw_card(c, x, y - h3, w, h3)
    c.setFont(PDFStyle.FONT_SUBTITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_RED)
    c.drawString(x + 0.3 * cm, y - 0.5 * cm, "VOTRE SITE DE TRANSITION Notion")
    
    t8 = f'• Retrouvez toutes vos ressources et guides pratiques sur : <a href="https://www.notion.so/Vos-ressources-aca96b6474d04acd9eaafa92523df7a6"><font color="{link_color}"><b><u>Vos ressources Notion</u></b></font></a>.'
    _draw_paragraph(c, t8, (x + 0.3 * cm, y - 1.1 * cm), w - 0.6 * cm, style)
    layout.render()
