import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit

from ..config import PDFStyle
from ..components import (
    draw_page_background, draw_dot_grid, draw_side_panel, 
    draw_title, draw_page_decorations,
    create_standard_cover, create_standard_summary_page, create_standard_recap_page
)
from ..templates import PageLayout
from ..forms import create_input_field

def create_chap3_cover(c):
    create_standard_cover(c, "CHAPITRE 3 : DÉCOUVERTE DE MES FONCTIONNEMENTS PROPRES")

def create_concept_page(c):
    points = [
        ("Sommaire :", ""),
        ("1.", "Récapitulatif de la séance précédente"),
        ("2.", "Introduction au livret 'découverte de mes fonctionnements propres'"),
        ("3.", "Mon Énergie et mon Environnement"),
        ("4.", "Mon Regard sur le Réel (L'Information)"),
        ("5.", "Ma Boussole Intérieure (Les Décisions)"),
        ("6.", "Mon Rapport au Temps et à l'Action"),
        ("7.", "Ma Zone d'Ombre")
    ]
    create_standard_summary_page(c, "3", "CONCEPT", "", points)

def create_recap_seance_page(c):
    intro_txt = "Prenez un moment pour revenir sur nos précédents échanges. Cet exercice vous aide à consolider vos apprentissages avant d'entamer une nouvelle étape. Répondez spontanément."
    questions = [
        "Qu'est-ce que cette séance vous a permis de comprendre de plus sur vous-même ?",
        "Quels éléments de votre ligne de vie ou arbre de vie vous reviennent le plus en tête ?",
        "En quoi cela éclaire différemment la suite de votre bilan et vos pistes pour la suite ?"
    ]
    create_standard_recap_page(c, "1. RÉCAPITULATIF", intro_txt, questions)

def create_intro_page(c):
    """Page d'introduction sans bloc signature."""
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2*cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0*cm
    text_top = height - 5.0*cm
    
    new_y = draw_title(c, "Mode d'Emploi de Moi-Même", text_x, text_top)
    
    text_y = new_y - 0.2*cm
    c.setFont(PDFStyle.FONT_BODY, 12)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
    
    lines = [
        "Considérez ce document comme un journal intime. Il n'y a pas de",
        "bonnes ou de mauvaises réponses, ni de questions pièges.",
        "",
        "Ce qui nous intéresse, ce n'est pas ce que vous savez faire",
        "(vos compétences), mais ce qui se passe dans votre tête et dans",
        "votre corps (votre énergie).",
        "",
        "Prenez le temps de détailler vos pensées. Racontez-nous",
        "le 'pourquoi' et le 'comment'. N'hésitez pas à utiliser des",
        "exemples de votre vie personnelle (famille, loisirs) autant que",
        "professionnelle."
    ]
    
    for line in lines:
        for s in simpleSplit(line, PDFStyle.FONT_BODY, 12, width - text_x - 1*cm):
            c.drawString(text_x, text_y, s)
            text_y -= 0.6*cm
        
    draw_page_decorations(c, width, height, part_title="2. INTRODUCTION", x_offset=card_margin)
    c.showPage()


def create_chap1_energie(c):
    # Questions 1-3
    layout = PageLayout(c, "Mon Énergie et mon Environnement", "3. MON ÉNERGIE")
    layout.add_text("Ce chapitre explore comment vous vous rechargez et comment vous traitez l'information immédiate.", spacing_after=0.3*cm)
    
    layout.add_question_block("1. Le vendredi soir : La semaine a été intense, remplie d'imprévus et d'interactions. Votre 'batterie sociale' est à plat. Décrivez la soirée ou le week-end idéal qui vous permettra d'être à 100% lundi matin. ", "mbti_q1", box_height=3.5*cm)
    
    layout.add_question_block("2. L'interruption : Vous êtes plongé(e) dans une tâche qui demande de la concentration. Quelqu'un entre pour vous poser une question anodine. Décrivez votre réaction intérieure (agacement, soulagement, rupture du fil de pensée ?) et comment vous gérez la situation à l'extérieur.", "mbti_q2", box_height=3.5*cm)
    
    layout.add_question_block("3. Le processus de pensée : Face à un problème complexe et nouveau, avez-vous instinctivement besoin d'en parler à voix haute avec quelqu'un pour que vos idées se mettent en place, ou avez-vous un besoin vital de vous isoler dans le silence pour structurer votre pensée avant d'en discuter ? Racontez une fois où vous avez dû faire l'inverse.", "mbti_q3", box_height=3.5*cm)
    
    layout.render()


def create_chap2_information(c):
    # Questions 4-7 sur deux pages (4-5 puis 6-7)
    layout1 = PageLayout(c, "Mon Regard sur le Réel (L'Information) - 1/2", "4. LE RÉEL")
    layout1.add_text("Ce chapitre explore ce que votre cerveau remarque en premier et comment il apprend.", spacing_after=0.3*cm)
    
    layout1.add_question_block("4. L'exercice de l'objet : Choisissez un objet du quotidien près de vous (une table, une tasse, un stylo). Décrivez-le-moi en 4 ou 5 phrases. Laissez libre cours à vos pensées : que voyez-vous, à quoi sert-il, que vous évoque-t-il ? (Écrivez vraiment tout ce qui vous passe par la tête en le regardant).", "mbti_q4", box_height=6.0*cm)
    layout1.add_question_block("5. Le grand saut : On vous demande de réaliser une tâche manuelle ou technique que vous n'avez jamais faite (monter un meuble complexe, cuisiner un plat étranger, utiliser un nouveau logiciel). Quel est votre premier réflexe ? Qu'est-ce qui vous frustre le plus dans l'apprentissage ?", "mbti_q5", box_height=6.0*cm)
    layout1.render()

    layout2 = PageLayout(c, "Mon Regard sur le Réel (L'Information) - 2/2", "4. LE RÉEL")
    layout2.add_question_block("6. La conversation ennuyeuse : Pensez à une discussion lors d'un repas qui vous a profondément ennuyé(e) ou fait 'décrocher' mentalement. De quoi parlaient les gens ?", "mbti_q6", box_height=6.0*cm)
    layout2.add_question_block("7. La machine à voyager dans le temps : Projetez-vous dans 5 ans, dans votre vie idéale. Ne me donnez pas juste un titre de poste : décrivez-moi l'ambiance de votre journée. Qu'est-ce qui vous rend fier(e) ?", "mbti_q7", box_height=6.0*cm)
    layout2.render()


def create_chap3_decisions(c):
    # Questions 8-11
    layout1 = PageLayout(c, "Ma Boussole Intérieure (Les Décisions) - 1/2", "5. MES DÉCISIONS")
    layout1.add_text("Ce chapitre explore vos critères pour trancher et juger une situation.", spacing_after=0.3*cm)
    
    layout1.add_question_block("8. Le choix difficile : Vous devez organiser un événement avec des places très limitées. Vous devez exclure une personne de votre cercle (pro ou perso). Comment prenez-vous la décision ? Décrivez votre malaise intérieur face à ce choix.", "mbti_q8", box_height=6.0*cm)
    layout1.add_question_block("9. Le cadeau embarrassant : Un(e) ami(e) très proche vous offre un vêtement que vous trouvez vraiment laid. Il/elle vous demande avec enthousiasme si vous l'aimez. Que répondez-vous spontanément et pourquoi ? Qu'est-ce qui est le plus important pour vous ?", "mbti_q9", box_height=6.0*cm)
    layout1.render()

    layout2 = PageLayout(c, "Ma Boussole Intérieure (Les Décisions) - 2/2", "5. MES DÉCISIONS")
    layout2.add_question_block("10. L'arbitre : Deux collègues ou amis se disputent violemment. L'ambiance est gâchée. Qu'est-ce qui vous dérange le plus ? Comment intervenez-vous ?", "mbti_q10", box_height=6.0*cm)
    layout2.add_question_block("11. La critique : Pensez à la dernière fois qu'on vous a fait une critique qui vous a blessé(e). Qu'est-ce qui a été le plus dur à avaler ?", "mbti_q11", box_height=6.0*cm)
    layout2.render()


def create_chap4_temps(c):
    # Questions 12-15
    layout1 = PageLayout(c, "Mon Rapport au Temps et à l'Action - 1/2", "6. MON ACTION")
    layout1.add_text("Ce chapitre explore votre besoin de structure face à l'inconnu.", spacing_after=0.3*cm)
    
    layout1.add_question_block("12. La page blanche : Vous vous réveillez un samedi matin avec absolument rien de prévu pour les deux prochains jours. Que ressentez vous ?", "mbti_q12", box_height=6.0*cm)
    layout1.add_question_block("13. L'adrénaline de la limite : Pensez à un projet important que vous deviez rendre à une date précise. De quoi avez vous besoin pour être efficace ?", "mbti_q13", box_height=6.0*cm)
    layout1.render()

    layout2 = PageLayout(c, "Mon Rapport au Temps et à l'Action - 2/2", "6. MON ACTION")
    layout2.add_question_block("14. L'organisation des vacances : Vous partez deux semaines à l'étranger. À quel point votre voyage est-il préparé ? Si un événement annule votre programme de la journée, trouvez-vous cela excitant ou profondément agaçant ?", "mbti_q14", box_height=6.0*cm)
    layout2.add_question_block("15. La conclusion vs L'exploration : Qu'est-ce qui vous donne le plus de satisfaction : le moment où l'on brainstorme, ouvre toutes les possibilités et découvre de nouvelles idées, ou le moment où l'on tranche, ferme les dossiers et raye les tâches de la 'To-Do list' ?", "mbti_q15", box_height=6.0*cm)
    layout2.render()


def create_chap5_ombre(c):
    # Questions 16-17
    layout = PageLayout(c, "Ma Zone d'Ombre", "7. MA ZONE D'OMBRE")
    layout.add_text("Ce chapitre explore comment vous réagissez quand vous êtes poussé(e) dans vos retranchements.", spacing_after=0.3*cm)
    
    layout.add_question_block("16. Le point de rupture : Tout le monde a un 'mauvais côté' quand il est sous l'emprise d'un stress extrême ou d'une immense fatigue. Racontez-moi à quoi vous ressemblez dans ces moments-là. Devenez-vous tyrannique et cassant ? Hyper-émotif(ve) et susceptible ? Obsédé(e) par des détails insignifiants ? Ou impulsif(ve) et imprudent(e) ?", "mbti_q16", box_height=6.0*cm)
    layout.add_question_block("17. L'insomnie (Bonus) : Il est 3 heures du matin, vous n'arrivez pas à dormir car votre cerveau tourne à plein régime. Sur quoi boucle-t-il ?", "mbti_q17", box_height=6.0*cm)
    layout.render()
