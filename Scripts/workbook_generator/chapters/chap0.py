import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm

from ..config import PDFStyle
from ..components import (
    draw_page_background, draw_dot_grid, draw_card, draw_side_panel, 
    draw_leaf, draw_title, draw_branding_logo, create_standard_cover,
    draw_circular_stamp, draw_pause_badge, draw_page_decorations,
    draw_page_footer, create_standard_summary_page
)
from ..templates import PageLayout
from ..forms import create_input_field

def create_cover_page(c):
    create_standard_cover(c, "CHAPITRE 0 : LE PRÉLUDE")

def create_summary_page(c):
    """Page: Au Programme."""
    intro_txt = (
        "Trouver sa place dans le monde d’aujourd’hui n’est pas chose facile ; on "
        "se réoriente, on se reforme, on réinvente la façon d’exercer son métier... "
        "Que ce soit pour une nécessité de réalisation personnelle, un besoin de "
        "vivre des expériences plus variées et stimulantes, une sérieuse remise en "
        "question du rapport à l’entreprise et au travail est en marche !<br/><br/>"
        "La question centrale pourrait être :<br/>"
        "<b>Quelle place dois-je accorder au travail dans mon existence et sous quelle forme ?</b><br/>"
        "Nous allons investiguer cette question (parmi beaucoup d’autres) dans ce travail.<br/><br/>"
        "En voici les grandes lignes :<br/><br/>"
        "<i>À votre disposition également, un site Notion réalisé par mes soins sur lequel "
        "vous pouvez trouver à tout moment des ressources ; sites, podcasts, articles...</i>"
    )
    
    steps = [
        ("05. Prendre du recul :", "sur vos choix passés et vos expériences."),
        ("13. Explorer votre personnalité :", "Vos forces, ce que vous aimez, vos besoins."),
        ("32. Actions concrètes :", "découvrir des secteurs et métiers qui me correspondent."),
        ("43. Plan d'action :", "Réussir votre projet.")
    ]
    
    create_standard_summary_page(c, "0", "AU PROGRAMME", intro_txt, steps)

def create_editorial_page_card(c):
    """Page: Édito avec carte."""
    width, height = A4

    draw_page_background(c, width, height, use_blobs=True)

    card_x      = 3*cm
    card_y      = 3.2*cm
    card_w      = width - 2*card_x
    card_h      = height - 4.8*cm - card_y

    draw_card(c, card_x, card_y, card_w, card_h)

    draw_branding_logo(c, 1.5*cm, height - 1.5*cm, size=13)

    inner_x  = card_x + 1.0*cm
    inner_w  = card_w  - 2.0*cm
    title_y  = card_y + card_h - 1.5*cm

    new_y = draw_title(c, "Le mot d'accueil", inner_x, title_y, size=22, available_width=inner_w)

    if os.path.exists(PDFStyle.PATH_GUILLEMETS):
        c.drawImage(
            PDFStyle.PATH_GUILLEMETS,
            card_x + card_w - 4.5*cm, title_y - 0.5*cm,
            width=2.8*cm, height=2.8*cm,
            mask='auto', preserveAspectRatio=True
        )
    else:
        c.saveState()
        c.setFont(PDFStyle.FONT_HAND, 65)
        c.setFillColor(PDFStyle.COLOR_ACCENT_YELLOW)
        c.drawRightString(card_x + card_w - 1.0*cm, title_y + 0.2*cm, '\u201c\u201c')
        c.restoreState()

    text_y = new_y - 0.5*cm

    style = ParagraphStyle(
        'EditoBody',
        fontName=PDFStyle.FONT_BODY,
        fontSize=11,
        leading=17,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
        alignment=TA_JUSTIFY,
    )

    paragraphs = [
        "Si vous entamez la lecture de ces livrets, c\u2019est que vous \u00eates aujourd\u2019hui en questionnement sur votre parcours professionnel et que vous avez eu le courage de passer \u00e0 l\u2019action en entamant un bilan de comp\u00e9tences. Bravo\u00a0!",
        "Les livrets vont vous accompagner pendant cette p\u00e9riode de questionnement\u00a0; ils seront \u00e0 la fois source d\u2019id\u00e9es, d\u2019inspirations, de remises en question\u2026 Ils recueilleront votre histoire, votre parcours et vos ressentis. Ils seront votre boussole et vous les retrouverez entre chaque s\u00e9ance.",
        "Le bilan de comp\u00e9tences que nous vous proposons est un m\u00e9lange de questionnements, d\u2019activit\u00e9s cr\u00e9atives et d\u2019\u00e9changes r\u00e9flexifs. Ces exercices seront des supports de travail pour nos entretiens. N\u2019h\u00e9sitez pas \u00e0 rajouter des questions ou activit\u00e9s qui vous int\u00e9ressent et vous semblent pertinentes pour nourrir votre cheminement.",
        "Lors de votre travail personnel, je vous conseille de vous d\u00e9gager des moments de calme dans un endroit chaleureux o\u00f9 vous vous sentez \u00e0 l\u2019aise et o\u00f9 vous ne serez pas d\u00e9rang\u00e9(e). Ce sont des temps pour vous retrouver avec vous m\u00eame et laisser libre court \u00e0 votre intuition et \u00e0 votre part cr\u00e9ative.",
    ]

    for para in paragraphs:
        p = Paragraph(para, style)
        pw, ph = p.wrap(inner_w, height)
        if text_y - ph >= card_y + 0.5*cm:
            p.drawOn(c, inner_x, text_y - ph)
        text_y -= (ph + 0.5*cm)

    if os.path.exists(PDFStyle.PATH_PLANTE_BLEUE):
        plant_w = 10*cm
        plant_h = 12*cm

        if os.path.exists(PDFStyle.PATH_PLANTE_ROSE_OMBRE):
            c.drawImage(
                PDFStyle.PATH_PLANTE_ROSE_OMBRE,
                width - plant_w + 6.5*cm + 0.3*cm,
                height - plant_h + 3*cm - 0.2*cm,
                width=plant_w, height=plant_h,
                mask='auto', preserveAspectRatio=True
            )
        
        c.drawImage(
            PDFStyle.PATH_PLANTE_BLEUE,
            width - plant_w + 6.5*cm,
            height - plant_h + 3*cm,
            width=plant_w, height=plant_h,
            mask='auto', preserveAspectRatio=True
        )

        c.saveState()
        
        corner_x = -5.5*cm
        corner_y = -plant_h * 0.3
        
        if os.path.exists(PDFStyle.PATH_PLANTE_ROSE_OMBRE):
            c.drawImage(
                PDFStyle.PATH_PLANTE_ROSE_OMBRE,
                corner_x + 0.3*cm, corner_y - 0.2*cm,
                width=plant_w, height=plant_h,
                mask='auto', preserveAspectRatio=True
            )

        c.drawImage(
            PDFStyle.PATH_PLANTE_BLEUE,
            corner_x, corner_y,
            width=plant_w, height=plant_h,
            mask='auto', preserveAspectRatio=True
        )
        c.restoreState()

    draw_page_decorations(c, width, height)
    c.showPage()


def create_intro_sense_page(c):
    """Page: Introduction 'Mettre du sens'."""
    width, height = A4
    
    draw_page_background(c, width, height, use_blobs=True)
    
    card_x      = 2*cm
    card_y      = 2.1*cm
    card_w      = width - 2*card_x
    card_h      = height - 3*cm
    
    draw_card(c, card_x, card_y, card_w, card_h)

    logo_x = card_x + 1*cm
    logo_y = card_y + card_h - 1*cm
    draw_branding_logo(c, logo_x, logo_y, size=13)

    text_x = card_x + 1.5*cm
    text_top = card_y + card_h - 4.5*cm
    content_width = card_w - 3*cm

    c.setFont(PDFStyle.FONT_TITLE, 10)
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.drawString(text_x, text_top + 1.2*cm, "INTRODUCTION")
    
    PURPLE_TITLE = colors.HexColor("#6C5CE7")
    new_y = draw_title(c, "Mettre du sens", text_x, text_top, size=28, color=PURPLE_TITLE, available_width=content_width)
    
    if os.path.exists(PDFStyle.PATH_STAMP):
        stamp_size = 4*cm
        c.saveState()
        c.translate(width - stamp_size/2 - 3*cm, height - stamp_size/2 - 1.5*cm)
        c.rotate(-10)
        c.drawImage(
            PDFStyle.PATH_STAMP,
            -stamp_size/2, -stamp_size/2,
            width=stamp_size, height=stamp_size,
            mask='auto', preserveAspectRatio=True
        )
        c.restoreState()
    
    text_y = new_y - 0.2*cm
    
    paragraphs = [
        "La question du sens est centrale dans nos vies : savoir pour quelles raisons nous faisons les choses, c’est reprendre notre pouvoir d’agir en conscience.",
        "En étudiant la psychologie et la sociologie, nous prenons conscience de l’importance de notre part inconsciente, des schémas et stéréotypes qui nous façonnent, des choses que nous croyons décider ou vouloir, alors que nous avons été conditionnés et influencés pour le faire. Notre travail s’attache aujourd’hui à aider les personnes à remettre du sens dans leurs décisions et leurs actions professionnelles.",
        "La question du sens va bien au-delà de l’activité professionnelle, mais c’est la porte d’entrée que nous choisissons ; pour une raison simple : elle concerne la majorité d’entre nous. Peu importe le milieu social ou l’origine, nous donnons tous de l’importance à nos vies par nos activités. Nous partons d’un point de vue clair : nous avons tous des moyens d’apprentissage, d’adaptation, de changement. Mais nous avons tous également une nature profonde qui nous donne des facilités pour certaines choses.",
        "Notre expérience, notre socialisation et d’autres facteurs innés font que nous avons une certaine personnalité. Elle se construit et se développe tout au long de la vie, mais nous sommes toujours différents de notre voisin. Nous avons des aptitudes différentes, des forces différentes, des goûts différents. Et c’est très bien ; c’est ce qui nous permet, en société, de pouvoir remplir des rôles et des fonctions complémentaires !",
        "Pourtant, malgré cette complémentarité potentielle, le lien entre qui nous sommes et ce que nous faisons au quotidien peut parfois se distendre ou se briser.",
        "Le mal-être au travail est plus que jamais un sujet central dans notre société ; la montée des burn-out, bore et brown-out en est malheureusement le témoin. Les phénomènes des Bullshits jobs (tâches inutiles, superficielles et vides de sens effectuées dans le monde du travail), les attentes différentes des nouvelles générations (millennials, Z), l’urgence climatique qui génère de l’écoanxiété… sont autant de raisons qui cohabitent. Notre objectif aujourd’hui est de vous accompagner à vous recentrer sur qui vous êtes, afin de pouvoir vous épanouir réellement dans vos choix professionnels.",
        "L’épanouissement professionnel est un objectif ambitieux, mais comme nous n'allons pas commencer un travail personnel avec des objectifs au ras des pâquerettes, allons-y !"
    ]
    
    style = ParagraphStyle(
        'IntroSenseBody',
        fontName=PDFStyle.FONT_BODY,
        fontSize=11.5,
        leading=16,
        textColor=PDFStyle.COLOR_ACCENT_BLUE,
        alignment=TA_JUSTIFY
    )
    
    for paragraph in paragraphs:
        p = Paragraph(paragraph, style)
        pw, ph = p.wrap(content_width, height)
        if text_y - ph < card_y + 0.5*cm:
            break
        p.drawOn(c, text_x, text_y - ph)
        text_y -= (ph + 0.5*cm)
    
    draw_page_footer(c, width, height)
    c.showPage()

def create_form_page_card(c):
    """Page: Mon Engagement (Formulaire)."""
    width, height = A4
    
    draw_page_background(c, width, height)
    
    card_margin = 2*cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0*cm
    text_top = height - 4.0*cm
    
    new_y = draw_title(c, "Mon Engagement", text_x, text_top)

    form = c.acroForm
    start_y = new_y - 0.5*cm
    
    c.setFont(PDFStyle.FONT_BODY, 12)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    c.drawString(text_x, start_y, "Moi, ")
    
    create_input_field(form, 'nom_complet', 
                       x=text_x + 1.5*cm, y=start_y-5, width=8*cm, height=20, 
                       tooltip='Prénom Nom')
    
    start_y -= 2*cm
    c.drawString(text_x, start_y, "décide d'investir")
    
    create_input_field(form, 'engagement_hebdo',
                       x=text_x + 3.5*cm, y=start_y-5, width=1.5*cm, height=20,
                       tooltip='Nb')
                       
    c.drawString(text_x + 5.5*cm, start_y, "heures par semaine.")
    
    start_y -= 2*cm
    c.drawString(text_x, start_y, "Mon objectif principal :")
    start_y -= 0.5*cm
    
    create_input_field(form, 'objectif_3_mois',
                       x=text_x, y=start_y - 2*cm, width=width - text_x - 1*cm, height=2*cm,
                       tooltip='Objectif', multiline=True)
                       
    start_y -= 3*cm 
    c.drawString(text_x, start_y, "Je m'autorise à :")
    start_y -= 0.5*cm
    
    create_input_field(form, 'permission_personnelle',
                       x=text_x, y=start_y - 2*cm, width=width - text_x - 1*cm, height=2*cm,
                       tooltip='Permission', multiline=True)
    
    # Hidden Fields
    form.textfield(name='meta_doc_type', value='workbook_chap0', x=0, y=-10, width=0, height=0)
    form.textfield(name='meta_doc_version', value='1.3_da_v4', x=0, y=-10, width=0, height=0)

    draw_page_decorations(c, width, height, part_title="INTRODUCTION", x_offset=card_margin)
    c.showPage()

def create_premiere_etape_page(c):
    """
    New Cover Page: Première étape : Faire le point.
    Blue background, large numbers, white text.
    Refined UI: 'Plume Texture', separate '1.'
    """
    width, height = A4
    
    c.setFillColor(PDFStyle.COLOR_ACCENT_BLUE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Faint Grid
    draw_dot_grid(c, width, height, color=PDFStyle.COLOR_WHITE, opacity=0.1)

    # Moved higher and to the left to avoid overlap, and made smaller/more transparent
    c.saveState()
    c.setFont(PDFStyle.FONT_BRANDING, 160) 
    c.setFillColor(PDFStyle.COLOR_WHITE, alpha=0.12) # Slightly more transparent
    c.drawString(1.5*cm, height - 9*cm, "1.")
    c.restoreState()

    # Shifted down slightly to be distinct from the watermarked number
    start_y = height - 10*cm
    c.setFont(PDFStyle.FONT_BRANDING, 32)
    c.setFillColor(PDFStyle.COLOR_WHITE)
    c.drawString(2.5*cm, start_y, "Première étape :")
    c.drawString(2.5*cm, start_y - 1.2*cm, "Faire le point")

    badge_y = start_y - 3*cm
    c.saveState()
    
    c.setFont(PDFStyle.FONT_BRANDING, 13)
    c.drawString(2*cm + 1.5*cm, badge_y, "APPUYER SUR PAUSE")
    
    draw_pause_badge(c, 2.5*cm, badge_y)
    
    c.restoreState()

    text_y = badge_y - 2*cm
    
    style_white = ParagraphStyle(
        'NormalWhite',
        fontName=PDFStyle.FONT_BODY,
        fontSize=12,
        leading=16,
        textColor=PDFStyle.COLOR_WHITE
    )
    
    text_content = [
        "Il est l'heure de faire le point sur votre situation actuelle ! Le début d'un bilan, c'est le bon moment pour enclencher le bouton PAUSE. Il est difficile de pouvoir réfléchir à ses besoins et à ses envies quand on est ancré•e dans une routine.",
        "Il est également difficile d'avoir accès à ces réflexions dans une vie où l'on est la tête sous l'eau, que ce soit par surcharge de travail, par ennui profond, ou par manque de sens."
    ]
    
    for block in text_content:
        p = Paragraph(block, style_white)
        w, h = p.wrap(width - 5*cm, height) # Slightly narrower for better reading
        p.drawOn(c, 2.5*cm, text_y - h) # Aligned with title
        text_y -= (h + 0.8*cm)

    # Replaced brindilles with plume texture, scaled down
    if os.path.exists(PDFStyle.PATH_PLUME_TEXTURE):
        # Top Right
        c.saveState()
        c.translate(width - 1*cm, height - 3*cm)
        c.rotate(75) # Rotated 45 degrees more to the left (30 + 45)
        # Smaller size: 5x5 cm approx
        c.drawImage(PDFStyle.PATH_PLUME_TEXTURE, 0, 0, width=5*cm, height=5*cm, mask='auto', preserveAspectRatio=True, anchor='ne')
        c.restoreState()

        # Bottom Left
        c.saveState()
        c.translate(0, 0)
        c.rotate(10)
        # Smaller size: 7x7 cm 
        c.drawImage(PDFStyle.PATH_PLUME_TEXTURE, -2*cm, -1*cm, width=7*cm, height=7*cm, mask='auto', preserveAspectRatio=True)
        c.restoreState()
    
    c.showPage()

def create_faire_le_point_pages(c):
    """
    Faire le Point : Ma Situation Actuelle.
    Split into 2 pages (4 questions each).
    """
    questions_part1 = [
        ("Comment je me sens actuellement ?", "feeling"),
        ("Quel a été le déclencheur de ce bilan ?", "trigger"),
        ("De quoi j’ai besoin en ce moment ?", "needs"),
        ("Qu’ai-je fait jusqu’à présent pour remédier à cette situation ?", "actions_taken")
    ]
    
    questions_part2 = [
        ("Qu’est ce que je n’ai pas encore changé ? Pourquoi ?", "not_changed"),
        ("Quels avantages ai-je à garder la situation telle quelle ?", "secondary_benefits"),
        ("Quels besoins sont insatisfaits dans ma vie aujourd’hui ?", "unmet_needs"),
        ("Quelles actions concrètes puis-je mettre en place ?", "concrete_actions")
    ]
    
    parts = [(questions_part1, "1/2"), (questions_part2, "2/2")]
    
    for idx_part, (questions, part_label) in enumerate(parts):
        layout = PageLayout(c, f"Faire le Point : Ma Situation ({part_label})", part_title="1. FAIRE LE POINT")
        
        if idx_part == 0:
            layout.add_text("Le début d’un bilan, c’est le bon moment pour enclencher le bouton PAUSE.", style_choice="italic", spacing_after=0.3*cm)
            
        for question, key in questions:
            layout.add_question_block(question, f's1_point_{key}', box_height=3.5*cm)

        layout.render()

def create_domaines_de_vie_page(c):
    """
    Les Domaines de Vie.
    Ratings + Reflection.
    """
    width, height = A4
    
    draw_page_background(c, width, height)
    
    card_margin = 2*cm
    draw_side_panel(c, card_margin, width, height)

    # Content
    text_x = card_margin + 1.0*cm
    text_top = height - 4.0*cm
    
    new_y = draw_title(c, "Les Domaines de Vie", text_x, text_top, size=22)
    
    # Intro Text (Psycho-education)
    style_intro = ParagraphStyle(
        'DomainIntro',
        fontName=PDFStyle.FONT_BODY,
        fontSize=11,
        leading=14,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
        alignment=TA_JUSTIFY
    )
    
    intro_txt = (
        "Notre vie est composée de multiples facettes qui interagissent toutes entre elles. "
        "Prendre le temps d'observer son niveau de satisfaction dans chacun de ces domaines "
        "permet d'obtenir une « photographie » de son équilibre actuel.<br/><br/>"
        "<b>Consigne :</b> Pour chacun des domaines ci-dessous, attribuez une note de 1 "
        "(très peu satisfait•e) à 10 (pleinement épanoui•e)."
    )
    
    p_intro = Paragraph(intro_txt, style_intro)
    w_i, h_i = p_intro.wrap(width - text_x - 1*cm, height)
    p_intro.drawOn(c, text_x, new_y - 0.2*cm - h_i)
    
    # 8 Domains
    domains = [
        "1. Argent / Finances",
        "2. Impact / Sens",
        "3. Dév. Personnel / Spiritualité",
        "4. Famille",
        "5. Santé / Énergie",
        "6. Lieu de vie / Environnement",
        "7. Loisirs / Passions",
        "8. Travail / Carrière"
    ]
    
    form = c.acroForm
    start_y = new_y - 0.2*cm - h_i - 1.5*cm
    panel_width = width - card_margin
    col_width = (panel_width - 2*cm) / 2
    
    # Grid layout for domains (2 columns)
    for i, domain in enumerate(domains):
        col = i % 2
        row = i // 2
        
        x_pos = text_x + (col * col_width)
        y_pos = start_y - (row * 1.5*cm)
        
        c.setFont(PDFStyle.FONT_BODY, 11)
        c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        c.drawString(x_pos, y_pos, domain)
        
        # Dotted lines for alignment
        text_w = c.stringWidth(domain, PDFStyle.FONT_BODY, 11)
        dot_start = x_pos + text_w + 0.2*cm
        dot_end = x_pos + 6.3*cm
        
        if dot_end > dot_start:
            c.saveState()
            c.setDash(1, 2)
            c.setStrokeColor(PDFStyle.COLOR_LINE, alpha=0.3)
            c.line(dot_start, y_pos + 0.1*cm, dot_end, y_pos + 0.1*cm)
            c.restoreState()
        
        # Rating Box
        create_input_field(form, f's1_domaine_note_{i+1}',
                           x=x_pos + 6.5*cm, y=y_pos - 0.1*cm,
                           width=1.5*cm, height=0.6*cm,
                           tooltip='Note /10')

    # Reflection Section
    reflection_y = start_y - (4 * 1.5*cm) - 1*cm
    
    style_refl = ParagraphStyle(
        'ReflBody',
        fontName=PDFStyle.FONT_BODY,
        fontSize=11,
        leading=15,
        textColor=PDFStyle.COLOR_TEXT_MAIN,
        alignment=TA_JUSTIFY
    )
    
    refl_intro = (
        "<b>Analyse de votre équilibre</b><br/>"
        "Prenez du recul sur vos notes : quels sont les domaines les plus satisfaisants ? "
        "Les moins satisfaisants ? Quel est l'impact de votre travail actuel "
        "(positif comme négatif) sur ces autres aspects de votre vie ?"
    )
    
    p_refl = Paragraph(refl_intro, style_refl)
    w_r, h_r = p_refl.wrap(width - text_x - 1*cm, height)
    p_refl.drawOn(c, text_x, reflection_y - h_r)
    
    # Large Text Area for Reflection
    area_top = reflection_y - h_r - 0.5*cm
    area_bottom = 2.5*cm # Margin from bottom
    area_height = area_top - area_bottom
    
    if area_height < 3*cm: area_height = 3*cm
    
    create_input_field(form, 's1_domaine_reflexion',
                       x=text_x, y=area_bottom,
                       width=width - text_x - 1*cm, height=area_height,
                       tooltip='Votre réflexion', multiline=True)

    draw_page_decorations(c, width, height, part_title="1. FAIRE LE POINT", x_offset=card_margin)
    c.showPage()

def create_entourage_page(c):
    """
    Mon Entourage.
    Soutiens vs Freins split.
    """
    layout = PageLayout(c, "Mon Entourage", part_title="1. FAIRE LE POINT")
    
    intro_txt = (
        "Le projet que vous menez ne se fait pas en vase clos. Votre entourage, "
        "qu'il soit proche ou plus lointain, joue un rôle crucial dans votre "
        "cheminement. Identifier vos alliés et les sources de tensions possibles "
        "est une étape importante pour sécuriser votre parcours."
    )
    layout.add_text(intro_txt, spacing_after=0.3*cm)
    
    # Needs two big areas: Soutiens (Blue) and Freins (Red)
    # The layout.add_question_block handles the alternate colors internally!
    
    layout.add_question_block("Soutien, conseil en positif", "s1_entourage_soutiens", 
                              subtitle="Qui peut vous soutenir ou vous conseiller utilement dans cette démarche ?", 
                              box_height=7.5*cm)
                              
    layout.add_question_block("Regard négatif ou anxiété des proches", "s1_entourage_freins", 
                              subtitle="Qui pourrait exprimer des doutes, des craintes ou un regard critique ?", 
                              box_height=7.5*cm)

    layout.render()
