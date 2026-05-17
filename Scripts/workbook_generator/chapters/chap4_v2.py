from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from ..config import PDFStyle
from ..components import (
    create_standard_cover,
    create_standard_summary_page,
    create_standard_recap_page,
)
from ..templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig

def create_chap4_v2_cover(c):
    create_standard_cover(c, "CHAPITRE 4 : RAPPORT À L'ARGENT ET CHOIX PROFESSIONNELS")

def create_concept_page(c):
    points = [
        ("Sommaire :", ""),
        ("1.", "Votre situation actuelle"),
        ("2.", "Votre histoire avec l'argent"),
        ("3.", "Vos premières expériences financières"),
        ("4.", "Argent et projet professionnel"),
        ("5.", "Identifier votre minimum financier acceptable"),
        ("6.", "Repérer ce que l'argent représente pour vous (Archétypes)"),
        ("7.", "Synthèse")
    ]
    create_standard_summary_page(c, "4", "CONCEPT", "Ce temps d'exploration vise à repérer la manière dont votre rapport à l'argent influence vos choix professionnels : besoin de sécurité, capacité à prendre des risques, rapport à la rémunération, négociation, ambition, liberté, peur du manque ou sentiment de légitimité. L'objectif n'est pas d'analyser en profondeur votre gestion financière, mais d'identifier les éléments qui peuvent soutenir ou freiner votre projet professionnel.", points)

def create_recap_seance_page(c):
    intro_txt = "Prenez un moment pour revenir sur la restitution de votre profil MBTI lors de la dernière séance. Cet exercice vous aide à consolider ces apprentissages avant d'explorer vos moteurs profonds."
    questions = [
        "Quelles sont les forces naturelles de votre profil MBTI dans lesquelles vous vous reconnaissez le plus ?",
        "Comment ce mode de fonctionnement (énergie, information, décision, action) s'illustre-t-il dans votre quotidien ?",
        "En quoi la compréhension de votre profil change-t-elle votre regard sur vous-même ou sur vos interactions ?",
    ]
    create_standard_recap_page(c, "1. RÉCAPITULATIF (MON PROFIL MBTI)", intro_txt, questions)

def create_situation_actuelle_page(c):
    layout = PageLayout(c, "Votre situation actuelle", config=LayoutConfig(part_title="1. VOTRE SITUATION ACTUELLE"))
    layout.add_text("Commencez par observer votre situation actuelle de manière simple et concrète.", config=TextConfig(spacing_after=0.5*cm))
    
    layout.add_question_block(
        "Aujourd'hui, vous sentez-vous plutôt en sécurité, en tension ou en vigilance financière ?",
        "v2_sit_1",
        config=QuestionConfig(box_height=4*cm)
    )
    
    layout.add_question_block(
        "Votre situation économique vous laisse-t-elle une marge de manœuvre pour évoluer professionnellement, ou vous donne-t-elle le sentiment d'être contraint ?",
        "v2_sit_2",
        config=QuestionConfig(box_height=4*cm)
    )

    layout.add_question_block(
        "Quel niveau de sécurité financière vous semble nécessaire pour envisager un changement ?",
        "v2_sit_3",
        config=QuestionConfig(box_height=4*cm)
    )
    layout.render()

def create_histoire_argent_page(c):
    layout = PageLayout(c, "Votre histoire avec l'argent", config=LayoutConfig(part_title="2. VOTRE HISTOIRE AVEC L'ARGENT"))
    layout.add_text("Votre rapport à l'argent s'est construit à partir de votre histoire familiale, sociale et personnelle.", config=TextConfig(spacing_after=0.5*cm))

    layout.add_question_block(
        "Dans quel environnement économique avez-vous grandi ?",
        "v2_hist_1",
        config=QuestionConfig(box_height=3*cm)
    )
    layout.add_question_block(
        "Dans votre famille, l'argent était-il associé à la sécurité, au stress, à la réussite, au mérite, au conflit, au plaisir ou à la liberté ? Était-ce un sujet tabou ?",
        "v2_hist_2",
        config=QuestionConfig(box_height=3*cm)
    )
    layout.add_question_block(
        "Qui gagnait, gérait et décidait de l'argent ? Avez-vous grandi avec le sentiment d'avoir assez, pas assez, ou de devoir faire attention ?",
        "v2_hist_3",
        config=QuestionConfig(box_height=3*cm)
    )
    layout.add_question_block(
        "Avez-vous observé des différences importantes de moyens dans votre entourage ? Ont-elles créé de la gêne, de l'envie, de la culpabilité ou un besoin de réussir ?",
        "v2_hist_4",
        config=QuestionConfig(box_height=3*cm)
    )
    layout.render()

    # Page 2: Genre et rapports femmes-hommes
    layout2 = PageLayout(c, "Argent, genre et rapports femmes-hommes", config=LayoutConfig(part_title="2. VOTRE HISTOIRE AVEC L'ARGENT"))
    layout2.add_question_block(
        "Avez-vous observé des rapports d'autonomie ou de dépendance financière, notamment entre femmes et hommes ? Avaient-ils la même liberté financière ?",
        "v2_hist_genre_1",
        config=QuestionConfig(box_height=4*cm)
    )
    layout2.add_question_block(
        "Avez-vous reçu, directement ou indirectement, des messages différents sur ce qu'une femme ou un homme pouvait attendre, demander, gagner ou dépenser ?",
        "v2_hist_genre_2",
        config=QuestionConfig(box_height=4*cm)
    )
    layout2.add_question_block(
        "Avez-vous observé des situations où l'argent créait un rapport de pouvoir, de protection, de contrôle ou de dépendance dans le couple ou la famille ?",
        "v2_hist_genre_3",
        config=QuestionConfig(box_height=4*cm)
    )
    layout2.render()

def create_premieres_experiences_page(c):
    layout = PageLayout(c, "Vos premières expériences financières", config=LayoutConfig(part_title="3. VOS PREMIÈRES EXPÉRIENCES"))
    layout.add_text("Certaines premières expériences laissent une empreinte durable dans la manière de gagner, dépenser, demander ou sécuriser l'argent.", config=TextConfig(spacing_after=0.5*cm))

    layout.add_question_block(
        "Avez-vous reçu de l'argent de poche ? Si oui, comment l'utilisiez-vous ? Était-ce de l'argent donné librement ou fallait-il le mériter ?",
        "v2_exp_1",
        config=QuestionConfig(box_height=2.5*cm)
    )
    layout.add_question_block(
        "Quand avez-vous commencé à gagner de l'argent par vous-même ? Que représentait ce premier argent gagné : liberté, fierté, sécurité, nécessité, obligation ?",
        "v2_exp_2",
        config=QuestionConfig(box_height=2.5*cm)
    )
    layout.add_question_block(
        "Aviez-vous plutôt tendance à dépenser, économiser, partager, cacher ou offrir ?",
        "v2_exp_3",
        config=QuestionConfig(box_height=2.5*cm)
    )
    layout.add_question_block(
        "Avez-vous un souvenir marquant lié à l'argent : manque, réussite, comparaison, conflit, honte, dépendance, fierté ?",
        "v2_exp_4",
        config=QuestionConfig(box_height=2.5*cm)
    )
    
    layout.add_text("Exemples de croyances possibles :", config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.1*cm))
    layout.add_text("« Il faut travailler dur pour mériter son argent. » • « Il ne faut dépendre de personne. » • « L'argent crée des conflits. » • « Je dois assurer pour les autres. » • « Je ne suis pas légitime à demander plus. »", config=TextConfig(font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY))
    layout.render()

def create_argent_projet_pro_page(c):
    # Page 1
    layout = PageLayout(c, "Argent et projet professionnel (1/2)", config=LayoutConfig(part_title="4. ARGENT ET PROJET PROFESSIONNEL"))
    layout.add_text("Dans un bilan de compétences, l'enjeu est surtout de comprendre comment l'argent influence vos choix professionnels.", config=TextConfig(spacing_after=0.5*cm))
    
    layout.add_question_block(
        "Votre revenu actuel vous semble-t-il cohérent avec votre contribution ? Vous sentez-vous suffisamment reconnu financièrement ?",
        "v2_pro_1",
        config=QuestionConfig(box_height=4.5*cm)
    )
    layout.add_question_block(
        "Avez-vous déjà renoncé à une envie professionnelle pour des raisons financières ? Ou accepté un poste principalement pour l'argent ?",
        "v2_pro_2",
        config=QuestionConfig(box_height=4.5*cm)
    )
    layout.add_question_block(
        "Avez-vous du mal à demander une augmentation, négocier, fixer un prix ou parler de rémunération ? Associez-vous le fait de gagner de l'argent au fait de beaucoup travailler ?",
        "v2_pro_3",
        config=QuestionConfig(box_height=4.5*cm)
    )
    layout.render()

    # Page 2
    layout2 = PageLayout(c, "Argent et projet professionnel (2/2)", config=LayoutConfig(part_title="4. ARGENT ET PROJET PROFESSIONNEL"))
    layout2.add_question_block(
        "Votre besoin de sécurité est-il parfois en tension avec votre besoin de sens, de liberté ou d'évolution ?",
        "v2_pro_4",
        config=QuestionConfig(box_height=5.0*cm)
    )
    layout2.add_question_block(
        "Votre genre, votre éducation ou votre histoire familiale influencent-ils votre manière de demander, négocier, gagner ou assumer votre ambition financière ? Qu'est-ce que vous n'osez pas demander, viser ou négocier aujourd'hui ?",
        "v2_pro_5",
        config=QuestionConfig(box_height=5.0*cm)
    )
    layout2.render()

def create_minimum_financier_page(c):
    # Page 1
    layout = PageLayout(c, "Identifier votre minimum financier acceptable (1/3)", config=LayoutConfig(part_title="5. MINIMUM FINANCIER"))
    layout.add_text("Dans une réorientation, il est utile de clarifier le revenu minimum en dessous duquel le projet deviendrait trop insécurisant ou difficile à tenir.", config=TextConfig(spacing_after=0.5*cm))
    
    layout.add_question_block(
        "Quel revenu mensuel minimum vous permettrait de couvrir vos charges essentielles ?",
        "v2_min_1",
        config=QuestionConfig(box_height=4.5*cm)
    )
    layout.add_question_block(
        "Quel montant vous permettrait de rester suffisamment serein pendant une transition ?",
        "v2_min_2",
        config=QuestionConfig(box_height=4.5*cm)
    )
    layout.add_question_block(
        "Quel revenu cible souhaitez-vous atteindre à terme ?",
        "v2_min_3",
        config=QuestionConfig(box_height=4.5*cm)
    )
    layout.render()

    # Page 2
    layout2 = PageLayout(c, "Identifier votre minimum financier acceptable (2/3)", config=LayoutConfig(part_title="5. MINIMUM FINANCIER"))
    layout2.add_question_block(
        "Pendant combien de temps pourriez-vous accepter une baisse temporaire de revenus ?",
        "v2_min_4",
        config=QuestionConfig(box_height=4.5*cm)
    )
    layout2.add_question_block(
        "Quelles concessions seraient acceptables, et lesquelles ne le seraient pas ?",
        "v2_min_5",
        config=QuestionConfig(box_height=4.5*cm)
    )
    layout2.add_question_block(
        "Cette piste professionnelle permet-elle d'atteindre votre minimum financier, immédiatement ou à moyen terme ?",
        "v2_min_6",
        config=QuestionConfig(box_height=4.5*cm)
    )
    layout2.render()

    # Page 3
    layout3 = PageLayout(c, "Identifier votre minimum financier acceptable (3/3)", config=LayoutConfig(part_title="5. MINIMUM FINANCIER"))
    layout3.add_text("À compléter :", config=TextConfig(style_choice="subtitle", font_size=11, color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.2*cm))
    layout3.add_question_block("Mon minimum vital mensuel :", "v2_min_comp_1", config=QuestionConfig(box_height=2.0*cm))
    layout3.add_question_block("Mon minimum sécurisant mensuel :", "v2_min_comp_2", config=QuestionConfig(box_height=2.0*cm))
    layout3.add_question_block("Mon revenu cible :", "v2_min_comp_3", config=QuestionConfig(box_height=2.0*cm))
    layout3.add_question_block("Durée acceptable d'une baisse de revenus :", "v2_min_comp_4", config=QuestionConfig(box_height=2.0*cm))
    layout3.add_question_block("Seuil en dessous duquel je ne souhaite pas descendre :", "v2_min_comp_5", config=QuestionConfig(box_height=2.0*cm))
    layout3.render()

def create_archetypes_v2_page(c):
    # Page 1
    layout = PageLayout(c, "Repérer ce que l'argent représente pour vous (1/2)", config=LayoutConfig(part_title="6. ARCHÉTYPES"))
    layout.add_text("L'argent n'a pas la même signification pour tout le monde. Pour certaines personnes, il représente d'abord la sécurité. Pour d'autres, la liberté, la réussite, l'indépendance, le plaisir, la reconnaissance ou encore la réparation d'une ancienne insécurité.", config=TextConfig(spacing_after=0.2*cm))
    layout.add_text("Les profils ci-dessous ne sont pas des cases fixes. Ils servent à repérer vos tendances dominantes, vos automatismes et les tensions qui peuvent influencer vos choix professionnels.", config=TextConfig(spacing_after=0.2*cm))
    layout.add_text("Prenez le temps de lire chaque tendance : elle peut être une ressource lorsqu'elle vous aide à faire des choix ajustés, mais peut aussi devenir limitante lorsqu'elle freine vos envies ou vous pousse à agir contre vos besoins réels.", config=TextConfig(spacing_after=0.5*cm))
    
    archs = [
        ("Le sécuritaire : l'argent comme protection", "L'argent sert d'abord à se sentir à l'abri, à anticiper et à éviter le manque.", "Question-clé : De quelle sécurité ai-je réellement besoin pour avancer sans me figer ?"),
        ("Le méritant : l'argent comme preuve d'effort", "L'argent doit être gagné, justifié, mérité. Il est souvent associé au travail, à l'effort ou au sacrifice.", "Question-clé : Est-ce que je confonds ma valeur avec mon niveau d'effort ?"),
        ("L'indépendant : l'argent comme liberté d'action", "L'argent représente l'autonomie. Il permet de choisir, partir, décider et ne pas dépendre.", "Question-clé : Comment construire mon autonomie sans tout transformer en obligation de contrôle ?"),
        ("Le généreux : l'argent comme lien", "L'argent sert à aider, offrir, soutenir, faire plaisir ou prendre soin des autres.", "Question-clé : Est-ce que ma générosité respecte aussi mes propres limites ?")
    ]
    for title, desc, q_cle in archs:
        layout.add_text(title, config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1*cm))
        layout.add_text(desc, config=TextConfig(font_size=10, spacing_after=0.1*cm))
        layout.add_text(q_cle, config=TextConfig(style_choice="italic", color=PDFStyle.COLOR_TEXT_SECONDARY, font_size=10, spacing_after=0.4*cm))
    layout.render()

    # Page 2
    layout2 = PageLayout(c, "Repérer ce que l'argent représente pour vous (2/2)", config=LayoutConfig(part_title="6. ARCHÉTYPES"))
    layout2.add_text("Lisez la suite des profils et repérez ce qui résonne le plus pour vous, que ce soit dans l'aspect ressource ou dans l'aspect limitant.", config=TextConfig(spacing_after=0.5*cm))
    archs2 = [
        ("L'évitant : l'argent comme inconfort", "L'argent est un sujet sensible, inconfortable ou chargé.", "Question-clé : Qu'est-ce que je cherche à ne pas ressentir quand j'évite l'argent ?"),
        ("L'ambitieux : l'argent comme réussite ou progression", "L'argent représente la progression, la réussite, l'impact, la reconnaissance ou le changement de niveau.", "Question-clé : Mon ambition financière est-elle au service de ma vie, ou est-ce ma vie qui sert mon ambition ?"),
        ("Le plaisir : l'argent comme expérience", "L'argent permet de vivre, profiter, expérimenter et se faire plaisir.", "Question-clé : Comment garder le plaisir sans compromettre ma sécurité future ?"),
        ("Le réparateur : l'argent comme réparation", "L'argent vient répondre à une ancienne insécurité, une injustice, une blessure sociale, familiale ou relationnelle.", "Question-clé : Quelle ancienne histoire mon rapport à l'argent essaie-t-il encore de réparer ?")
    ]
    for title, desc, q_cle in archs2:
        layout2.add_text(title, config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1*cm))
        layout2.add_text(desc, config=TextConfig(font_size=10, spacing_after=0.1*cm))
        layout2.add_text(q_cle, config=TextConfig(style_choice="italic", color=PDFStyle.COLOR_TEXT_SECONDARY, font_size=10, spacing_after=0.4*cm))
    
    layout2.add_question_block(
        "Quels archétypes vous correspondent le plus aujourd'hui ? Lesquels vous soutiennent, lesquels vous limitent ?",
        "v2_arch_choix",
        config=QuestionConfig(box_height=3.5*cm)
    )
    layout2.render()

def create_synthese_v2_page(c):
    layout = PageLayout(c, "Synthèse", config=LayoutConfig(part_title="7. SYNTHÈSE"))
    
    layout.add_question_block(
        "Si vous aviez plus d'argent, qu'est-ce que cela changerait vraiment pour vous ?",
        "v2_synth_1",
        config=QuestionConfig(box_height=4*cm)
    )
    layout.add_question_block(
        "Qu'est-ce qui vous fait le plus peur dans le manque d'argent ? Et qu'est-ce qui pourrait vous mettre mal à l'aise dans le fait de gagner davantage ?",
        "v2_synth_2",
        config=QuestionConfig(box_height=4*cm)
    )
    layout.add_question_block(
        "À partir de quoi vous sentez-vous « assez » en sécurité ? Est-ce que cet « assez » correspond à un chiffre concret, ou plutôt à une sensation intérieure difficile à atteindre ?",
        "v2_synth_3",
        config=QuestionConfig(box_height=4*cm)
    )
    layout.render()
