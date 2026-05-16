from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from ..utils import cached_simpleSplit as simpleSplit

from ..config import PDFStyle
from ..components import (
    draw_page_background,
    draw_side_panel,
    draw_title,
    draw_page_decorations,
    create_standard_cover,
    create_standard_summary_page,
    create_standard_recap_page,
)
from ..templates import PageLayout, QuestionConfig, LayoutConfig, TextConfig
from ..forms import create_checkbox

def create_chap4_cover(c):
    create_standard_cover(c, "CHAPITRE 4 : VALEURS, MOTEURS ET RELATION À L'ARGENT")


def create_concept_page(c):
    points = [
        ("Sommaire :", ""),
        ("1.", "Récapitulatif (Mon Profil MBTI)"),
        ("2.", "Les 10 Valeurs de Schwartz (Référence)"),
        ("3.", "Le Questionnaire PVQ-21"),
        ("4.", "Questions de Validation & Personnalité Pro"),
        ("5.", "Mes Moteurs Profonds (Valeurs & Actions)"),
        ("6.", "Mon Profil Financier (Money Script)"),
        ("7.", "Ma Biographie Financière (Les Racines)"),
        ("8.", "La Lettre à l'Argent (Acte Symbolique)"),
        ("9.", "Mon Archétype Sacré & Mindset de Surplus"),
        ("10.", "Ma Cartographie Personnelle (Synthèse S1 à S4)"),
        ("11.", "Travail Inter-Session S4/S5 (Exploration)"),
    ]
    create_standard_summary_page(c, "4", "CONCEPT", "", points)


def create_recap_seance_page(c):
    intro_txt = "Prenez un moment pour revenir sur la restitution de votre profil MBTI lors de la dernière séance. Cet exercice vous aide à consolider ces apprentissages avant d'explorer vos moteurs profonds."
    questions = [
        "Quelles sont les forces naturelles de votre profil MBTI dans lesquelles vous vous reconnaissez le plus ?",
        "Comment ce mode de fonctionnement (énergie, information, décision, action) s'illustre-t-il dans votre quotidien ?",
        "En quoi la compréhension de votre profil change-t-elle votre regard sur vous-même ou sur vos interactions ?",
    ]
    create_standard_recap_page(c, "1. RÉCAPITULATIF (MON PROFIL MBTI)", intro_txt, questions)


def create_valeurs_page(c):
    layout = PageLayout(
        c,
        "Mes Moteurs Profonds (Valeurs)",
        config=LayoutConfig(part_title="2A. MES MOTEURS PROFONDS")
    )
    layout.add_text(
        "⏱ ~15 min | 🎯 Identifier vos valeurs fondamentales pour mieux comprendre vos choix",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text(
        "Vivre en accord avec ses valeurs nourrit l'Estime de Soi. Vivre en désaccord la détruit. À partir de la liste de valeurs de Schwarz, identifiez celles qui sont fondamentales pour vous.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout.add_question_block(
        "1. Identification : Illustrez vos 3 valeurs principales par un exemple de votre vie :",
        "valeurs_q1",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "2. Héritage : De qui avez-vous reçu ces valeurs ?",
        "valeurs_q2",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "3. Conflits de Valeurs : Identifiez un moment de conflit intérieur. Quelles étaient les valeurs en présence et comment ce conflit s'est-il résolu ?",
        "valeurs_q3",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Bilan : Ce que cet exercice m'apprend sur mes moteurs profonds et ce que ces conflits disent de positif sur moi :",
        "valeurs_q4",
        config=QuestionConfig(box_height=3.0 * cm),
    )

    layout.render()


def create_verbes_page(c):
    layout = PageLayout(
        c,
        "Mes Moteurs Profonds (Verbes d'Action)",
        config=LayoutConfig(part_title="2B. MES MOTEURS PROFONDS")
    )
    layout.add_text(
        "⏱ ~10 min | 🎯 Repérer les actions qui vous donnent de l'énergie au quotidien",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text(
        "Quels sont les verbes qui vous mettent en mouvement ? Voici quelques exemples par catégorie :",
        config=TextConfig(spacing_after=0.3 * cm),
    )
    
    categories = [
        "• Organiser : Planifier, gérer, coordonner, structurer...",
        "• Communiquer : Transmettre, écouter, interviewer, rédiger...",
        "• Créer : Concevoir, imaginer, innover, adapter...",
        "• Aider : Conseiller, soigner, guider, éclairer...",
        "• Analyser : Rechercher, étudier, observer, évaluer...",
        "• Diriger : Décider, manager, piloter, entreprendre..."
    ]
    for cat in categories:
        layout.add_text(cat, config=TextConfig(font_size=10, style_choice="italic", color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.1 * cm))
    layout.y_cursor -= 0.2 * cm

    layout.add_question_block(
        "1. Les verbes que je préfère (Ceux que j'aime conjuguer au quotidien) :",
        "verbes_q1",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "2. Les verbes que j'aime le moins (Ceux qui m'épuisent) :",
        "verbes_q2",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "Analyse : Quel lien faites-vous avec vos expériences passées et votre profil MBTI ?",
        "verbes_q3",
        config=QuestionConfig(box_height=3.0 * cm),
    )

    layout.render()


def create_psycho_edu_page(c):
    """Page d'introduction à la psychologie économique — refactorisée sur PageLayout."""
    layout = PageLayout(
        c,
        "Introduction à la Psychologie Économique",
        config=LayoutConfig(part_title="3. PSYCHOLOGIE ÉCONOMIQUE"),
    )

    layout.add_text(
        "Transition : Maintenant que vous connaissez vos moteurs, explorons ce qui peut les freiner...",
        config=TextConfig(style_choice="italic", font_size=11, color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.5 * cm),
    )

    layout.add_text(
        "Ce module vise à débloquer le 'thermostat financier' interne. La psychologie financière moderne repose largement sur les travaux du Dr. Bradley Klontz, qui a identifié quatre 'Money Scripts' (scénarios monétaires) inconscients, formés dès l'enfance, qui pilotent nos comportements d'adulte.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    # --- Les 4 Money Scripts ---
    layout.add_text(
        "1. Money Avoidance (Évitement)",
        config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1 * cm),
    )
    layout.add_text(
        "La croyance que l'argent est mauvais, sale, ou source d'anxiété. Ces individus ont tendance à sous-tarifier leurs services ou à ignorer leurs relevés bancaires.",
        config=TextConfig(font_size=10, spacing_after=0.4 * cm),
    )

    layout.add_text(
        "2. Money Worship (Adoration)",
        config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1 * cm),
    )
    layout.add_text(
        "La conviction que 'plus d'argent' résoudra tous les problèmes émotionnels. Cela conduit à un cycle de travail compulsif et à des achats compensatoires.",
        config=TextConfig(font_size=10, spacing_after=0.4 * cm),
    )

    layout.add_text(
        "3. Money Status (Statut)",
        config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1 * cm),
    )
    layout.add_text(
        "L'estime de soi est directement corrélée à la richesse nette. Ces profils sont à risque de dépenses ostentatoires et de fragilité en cas de perte d'emploi.",
        config=TextConfig(font_size=10, spacing_after=0.4 * cm),
    )

    layout.add_text(
        "4. Money Vigilance (Vigilance)",
        config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1 * cm),
    )
    layout.add_text(
        "Une prudence excessive, le secret et l'anxiété. Bien que favorable à l'épargne, ce script peut empêcher d'investir en soi par peur de manquer.",
        config=TextConfig(font_size=10, spacing_after=0.5 * cm),
    )

    # --- Money Biography intro ---
    layout.add_text(
        "La 'Money Biography' est un outil narratif qui connecte les souvenirs d'enfance aux comportements actuels. L'exercice consiste à remonter au premier souvenir d'argent pour décoder l'émotion associée et voir comment elle se réactive aujourd'hui.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout.render()


def _draw_kmsi_sections(layout, sections):
    c = layout.c
    form = c.acroForm
    
    for title, belief, questions, prefix in sections:
        layout.add_text(title, config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.1*cm))
        layout.add_text(belief, config=TextConfig(style_choice="italic", color=PDFStyle.COLOR_TEXT_SECONDARY, font_size=10, spacing_after=0.4*cm))
        
        for i, q in enumerate(questions):
            # Draw question text
            layout.add_text(q, config=TextConfig(font_size=10, spacing_after=0.1*cm))
            
            # Draw scale 1 to 6
            scale_y = layout.y_cursor - 0.2*cm
            start_x = layout.text_x
            
            for score in range(1, 7):
                x_pos = start_x + (score - 1) * 1.5 * cm
                create_checkbox(form, f"{prefix}_q{i+1}_{score}", pos=(x_pos, scale_y), size=0.4*cm)
                c.setFont(PDFStyle.FONT_BODY, 8)
                c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
                c.drawString(x_pos + 0.6*cm, scale_y + 0.1*cm, str(score))
            
            layout.y_cursor -= 0.8 * cm
        layout.y_cursor -= 0.5 * cm


def create_kmsi_pages(c):
    # Page 1: Sections A & B
    layout = PageLayout(c, "Mon Profil Financier (KMSI)", config=LayoutConfig(part_title="3. PSYCHOLOGIE ÉCONOMIQUE"))
    layout.add_text("⏱ ~10 min | 🎯 Diagnostiquer votre scénario monétaire dominant", config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm))
    layout.add_text("Évaluez les affirmations suivantes de 1 (Pas du tout d'accord) à 6 (Tout à fait d'accord).", config=TextConfig(spacing_after=0.5*cm))
    
    sections_p1 = [
        ("A. Évitement de l'Argent (Money Avoidance)", "Croyance : L'argent est mauvais, sale ou source de corruption.", [
            "Je ne mérite pas d'argent quand d'autres ont moins.",
            "Les gens riches sont avides.",
            "Il n'est pas spirituel d'avoir de l'argent."
        ], "kmsi_avoidance"),
        ("B. Adoration de l'Argent (Money Worship)", "Croyance : L'argent est la clé du bonheur et de la résolution de tous les problèmes.", [
            "L'argent achète la liberté.",
            "Si j'avais plus d'argent, ma vie serait parfaite.",
            "On n'a jamais assez d'argent."
        ], "kmsi_worship")
    ]
    
    _draw_kmsi_sections(layout, sections_p1)
    layout.render()
    
    # Page 2: Sections C & D + Restitution
    layout2 = PageLayout(c, "Mon Profil Financier (KMSI) - Suite", config=LayoutConfig(part_title="3. PSYCHOLOGIE ÉCONOMIQUE"))
    sections_p2 = [
        ("C. Statut de l'Argent (Money Status)", "Croyance : Ma valeur nette est égale à ma valeur personnelle.", [
            "Je n'achète que les meilleures marques.",
            "Si je ne suis pas riche, je suis un échec.",
            "Les gens pauvres sont paresseux."
        ], "kmsi_status"),
        ("D. Vigilance Monétaire (Money Vigilance)", "Croyance : Il faut être secret et hyper-prudent avec l'argent.", [
            "Il ne faut pas parler d'argent.",
            "Je dois toujours épargner pour les coups durs.",
            "Je suis très anxieux si je n'ai pas de cash."
        ], "kmsi_vigilance")
    ]
    
    _draw_kmsi_sections(layout2, sections_p2)
    
    # Grille de scoring
    layout2.add_text("Grille d'interprétation des scores (par catégorie)", config=TextConfig(style_choice="subtitle", font_size=10, color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.1*cm))
    layout2.add_text("• 3 à 8 points : Tendance faible", config=TextConfig(font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.1*cm))
    layout2.add_text("• 9 à 13 points : Tendance modérée", config=TextConfig(font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.1*cm))
    layout2.add_text("• 14 à 18 points : Tendance forte", config=TextConfig(font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.4*cm))

    # Bilan
    layout2.add_question_block(
        "Bilan : Mon script dominant est...",
        "kmsi_bilan",
        config=QuestionConfig(box_height=2.5*cm, subtitle="Calculez votre score pour chaque catégorie. Le score le plus élevé indique votre script dominant.")
    )
    
    layout2.add_question_block(
        "Reformulation (Méthode HMW) :",
        "kmsi_hmw",
        config=QuestionConfig(box_height=3.5*cm, subtitle="Comment pourrais-je reformuler la croyance la plus limitante ?")
    )
    layout2.render()


def create_kmsi_impact_page(c):
    """Page dédiée : Impact de mon Money Script sur mon Projet Pro (P1.3)."""
    layout = PageLayout(
        c,
        "Impact de mon Money Script sur mon Projet Pro",
        config=LayoutConfig(part_title="3. PSYCHOLOGIE ÉCONOMIQUE"),
    )

    layout.add_text(
        "Votre script dominant identifié par le KMSI a des conséquences directes sur votre projet professionnel. Prenez le temps de lire l'analyse correspondant à votre dominante, puis répondez aux questions ci-dessous.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    # Les 4 paragraphes d'impact issus de Exercice_Inventaire_Croyances.md L39-43
    layout.add_text(
        "Dominante \"Évitement\"",
        config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1 * cm),
    )
    layout.add_text(
        "Risque de sous-tarification, difficulté à se vendre en freelance, sabotage des opportunités lucratives.",
        config=TextConfig(style_choice="italic", font_size=10, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.35 * cm),
    )

    layout.add_text(
        "Dominante \"Adoration\"",
        config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1 * cm),
    )
    layout.add_text(
        "Risque de burnout pour \"toujours plus\", insatisfaction chronique, décisions impulsives basées sur des promesses de gain rapide.",
        config=TextConfig(style_choice="italic", font_size=10, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.35 * cm),
    )

    layout.add_text(
        "Dominante \"Statut\"",
        config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1 * cm),
    )
    layout.add_text(
        "Risque de dépenses excessives pour \"paraître\", choix de carrière basés sur le prestige plutôt que le sens.",
        config=TextConfig(style_choice="italic", font_size=10, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.35 * cm),
    )

    layout.add_text(
        "Dominante \"Vigilance\"",
        config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1 * cm),
    )
    layout.add_text(
        "Risque de ne pas oser investir en soi (formation, coaching), peur paralysante de manquer, difficulté à profiter des fruits de son travail.",
        config=TextConfig(style_choice="italic", font_size=10, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.5 * cm),
    )

    # Questions de réflexion personnelle
    layout.add_question_block(
        "Quel impact mon script dominant a-t-il eu concrètement sur mes choix professionnels passés ?",
        "kmsi_impact_passe",
        config=QuestionConfig(box_height=3.5 * cm, subtitle="Repensez à une décision de carrière, de salaire ou d'investissement influencée par cette croyance."),
    )

    layout.add_question_block(
        "Quel risque ce script fait-il peser sur mon projet professionnel actuel ?",
        "kmsi_impact_futur",
        config=QuestionConfig(box_height=3.5 * cm, subtitle="Identifiez le piège principal à éviter dans votre projet de transition ou d'évolution."),
    )

    layout.render()


def create_biographie_page(c):
    layout = PageLayout(c, "Ma Biographie Financière", config=LayoutConfig(part_title="4. LES RACINES"))
    layout.add_text(
        "Transition : Votre score KMSI révèle une tendance. Remontons à sa source...",
        config=TextConfig(style_choice="italic", font_size=11, color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.5 * cm),
    )
    layout.add_text(
        "⏱ ~20 min | 🎯 Retracer l'origine de vos croyances financières | 💡 Il est normal de ressentir de l'inconfort",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text("Identifiez vos souvenirs clés liés à l'argent pour comprendre vos programmations inconscientes.", config=TextConfig(spacing_after=0.3*cm))
    
    layout.add_question_block(
        "1. Le Premier Souvenir (souvent vers 5-7 ans)",
        "bio_premier_souvenir",
        config=QuestionConfig(
            box_height=5.5*cm, 
            subtitle="Quel âge aviez-vous ? Qui était là ? Quelle était la situation ? Quelle émotion avez-vous ressentie (Joie, Honte, Peur...) ?",
            example="Souvenir : Père critiquant mère pour une dépense 'inutile'. Croyance formée : 'Dépenser pour soi est égoïste et dangereux'. Impact : Difficulté à investir dans sa propre formation ou reconversion."
        )
    )
    
    layout.add_question_block(
        "2. L'Adolescence",
        "bio_adolescence",
        config=QuestionConfig(
            box_height=3.5*cm, 
            subtitle="Premier argent gagné vs Argent de poche. Sentiment dominant : Autonomie ou Dépendance ? Comparaison sociale ?",
            example="Souvenir : Recevoir de l'argent pour de bonnes notes. Croyance formée : 'Je ne vaux quelque chose que si je suis performant'. Impact : Burnout, incapacité à refuser du travail supplémentaire non payé."
        )
    )
    
    layout.add_question_block(
        "3. Analyse & Lien avec le Projet Pro",
        "bio_analyse",
        config=QuestionConfig(
            box_height=4.0*cm, 
            subtitle="Pour chaque souvenir marquant : Quelle croyance ai-je formée ce jour-là qui est encore active aujourd'hui ?"
        )
    )
    
    layout.render()

def create_dialogue_page(c):
    layout = PageLayout(c, "La Lettre à l'Argent", config=LayoutConfig(part_title="5. ACTE SYMBOLIQUE"))
    layout.add_text(
        "⏱ ~20 min | 🎯 Révéler vos projections affectives sur l'argent | 💡 Laissez parler vos émotions sans filtre",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text("L'argent est souvent chargé de projections affectives. En le traitant comme une personne distincte, on peut révéler ces projections.", config=TextConfig(spacing_after=0.3*cm))
    
    layout.add_question_block(
        "Prenez un moment de calme. Imaginez que l'Argent est une personne assise en face de vous. Écrivez-lui une lettre.",
        "lettre_argent",
        config=QuestionConfig(box_height=5.0*cm, subtitle="Structure : 1. Salutation / 2. L'État des lieux / 3. Le Reproche (ou Gratitude) / 4. La Demande de Changement")
    )
    
    layout.add_question_block(
        "Insight & Analyse : Qui l'Argent représente-t-il vraiment ?",
        "lettre_analyse",
        config=QuestionConfig(box_height=3.5*cm, subtitle="Un père exigeant ? Une mère insécurisante ? Un amant capricieux ?")
    )
    
    layout.add_question_block(
        "Nouvelle Alliance (Réponse de l'Argent) :",
        "lettre_reponse",
        config=QuestionConfig(box_height=3.5*cm, subtitle='"Cher [Votre Prénom], je suis prêt à être ton partenaire pour..."')
    )
    
    layout.render()

def create_archetypes_page(c):
    # --- Page 1 : Les 8 Archétypes ---
    layout1 = PageLayout(c, "Mon Archétype Sacré (1/2)", config=LayoutConfig(part_title="6. MINDSET & ARCHÉTYPES"))
    layout1.add_text(
        "Transition : Vous avez dialogué avec l'argent. Découvrons maintenant votre style naturel de gestion...",
        config=TextConfig(style_choice="italic", font_size=11, color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.5 * cm),
    )
    layout1.add_text(
        "⏱ ~15 min | 🎯 Identifier votre style naturel de gestion financière",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout1.add_text("Identifiez votre style de gestion naturel pour transformer vos défauts en atouts (Inspiré des Sacred Money Archetypes).", config=TextConfig(spacing_after=0.5*cm))
    
    archetypes = [
        ("1. L'Accumulateur", "Force : Épargne, prudence, respecte l'argent.", "Ombre : Peur de dépenser, avarice, peur du manque constante."),
        ("2. Le Connecteur", "Force : Réseautage, relations humaines avant l'argent.", "Ombre : Dépendance financière, naïveté, ne se soucie pas des factures."),
        ("3. L'Alchimiste", "Force : Idées transformatrices, utilise l'argent pour le bien social.", "Ombre : Relation amour/haine avec l'argent, risque de rejeter la richesse matérielle."),
        ("4. Le Dirigeant", "Force : Bâtisseur d'empire, ambitieux, à l'aise avec les gros chiffres.", "Ombre : Obsession du travail, jamais satisfait, tyrannie."),
        ("5. Le Nourricier", "Force : Généreux, prend soin des autres.", "Ombre : Se sacrifie, se laisse 'vampiriser', a du mal à fixer des limites financières."),
        ("6. Le Maverick", "Force : Prise de risque, innovation, rebelle.", "Ombre : Paris risqués, instabilité financière, 'montagnes russes'."),
        ("7. La Célébrité", "Force : Charisme, image de marque, attire l'attention (et l'argent).", "Ombre : Dépenses ostentatoires pour le statut, vide intérieur."),
        ("8. Le Romantique", "Force : Profite de la vie, esthète, hédoniste.", "Ombre : Déni des réalités financières, dettes de 'plaisir'.")
    ]
    
    for title, force, ombre in archetypes:
        layout1.add_text(title, config=TextConfig(style_choice="subtitle", color=PDFStyle.COLOR_ACCENT_BLUE, font_size=11, spacing_after=0.1 * cm))
        layout1.add_text(force, config=TextConfig(style_choice="italic", font_size=10, color=PDFStyle.COLOR_TEXT_MAIN, spacing_after=0.05 * cm))
        layout1.add_text(ombre, config=TextConfig(style_choice="italic", font_size=10, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.4 * cm))
        
    layout1.render()

    # --- Page 2 : Plan d'Action ---
    layout2 = PageLayout(c, "Mon Archétype Sacré (2/2)", config=LayoutConfig(part_title="6. MINDSET & ARCHÉTYPES"))
    
    layout2.add_question_block(
        "Mon Top 3 des Archétypes :",
        "archetypes_top3",
        config=QuestionConfig(box_height=4.0*cm)
    )
    
    layout2.add_text("Plan d'Action Personnalisé", config=TextConfig(style_choice="subtitle", font_size=12, color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.2*cm))
    layout2.add_text("L'objectif n'est pas de changer d'archétype, mais de jouer avec ses forces. Voici quelques exemples de défis :", config=TextConfig(font_size=10, spacing_after=0.4*cm))
    
    actions = [
        ("Si vous êtes Accumulateur :", "Action : Définir un budget 'Investissement Pro' et le dépenser obligatoirement."),
        ("Si vous êtes Connecteur :", "Action : Comment puis-je créer une offre qui connecte les gens (et être payé pour ça) ?"),
        ("Si vous êtes Nourricier :", "Action : Fixer des tarifs justes et apprendre à dire 'Non' ou 'Voici mon tarif'."),
        ("Si vous êtes Alchimiste :", "Action : Visualiser l'argent comme un amplificateur de votre impact social.")
    ]
    
    for title, action in actions:
        layout2.add_text(title, config=TextConfig(style_choice="subtitle", font_size=10, color=PDFStyle.COLOR_TEXT_MAIN, spacing_after=0.1*cm))
        layout2.add_text(action, config=TextConfig(style_choice="italic", font_size=10, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm))
        
    layout2.add_question_block(
        "Ma prochaine action :",
        "archetypes_action",
        config=QuestionConfig(box_height=4.5*cm, subtitle="Compte tenu de mon archétype dominant, quelle est la prochaine action la plus alignée (mais inconfortable) que je dois poser ?")
    )
    
    layout2.render()

def create_mindset_surplus_page(c):
    """Page Mindset de Surplus : diagnostic Scarcity vs Surplus + actions de générosité stratégique."""
    # --- Page 1 : Diagnostic Scarcity vs Surplus ---
    layout = PageLayout(
        c,
        "Mindset de Surplus (Diagnostic)",
        config=LayoutConfig(part_title="6. MINDSET & ARCHÉTYPES"),
    )
    layout.add_text(
        "⏱ ~15 min | 🎯 Diagnostiquer vos zones de manque et initier une dynamique d'abondance",
        config=TextConfig(style_choice="italic", font_size=9, color=PDFStyle.COLOR_TEXT_SECONDARY, spacing_after=0.3*cm)
    )
    layout.add_text(
        "Passer du Manque (Scarcity) à l'Abondance (Surplus). Identifiez dans quelle zone vous vous situez pour chacun des domaines ci-dessous.",
        config=TextConfig(spacing_after=0.5 * cm),
    )

    # Grille comparative Scarcity vs Surplus (4 domaines)
    domains = [
        (
            "Ressources",
            "Manque : \"Il n'y en a pas assez pour tout le monde.\" (Compétition)",
            "Surplus : \"Il y a assez pour tout le monde.\" (Création)",
        ),
        (
            "Dépense",
            "Manque : Peur, culpabilité, restriction excessive.",
            "Surplus : Investissement conscient, joie, flux.",
        ),
        (
            "Don",
            "Manque : \"Je donnerai quand j'en aurai plus.\"",
            "Surplus : \"Je donne pour faire circuler et recevoir.\"",
        ),
        (
            "Sécurité",
            "Manque : Thésauriser, peur de perdre.",
            "Surplus : Confiance en sa capacité à générer des ressources.",
        ),
    ]

    for domain_name, scarcity, surplus in domains:
        layout.add_text(
            domain_name,
            config=TextConfig(
                style_choice="subtitle",
                color=PDFStyle.COLOR_ACCENT_BLUE,
                font_size=11,
                spacing_after=0.1 * cm,
            ),
        )
        layout.add_text(
            scarcity,
            config=TextConfig(
                style_choice="italic",
                font_size=9,
                color=PDFStyle.COLOR_TEXT_SECONDARY,
                spacing_after=0.05 * cm,
            ),
        )
        layout.add_text(
            surplus,
            config=TextConfig(
                style_choice="italic",
                font_size=9,
                color=PDFStyle.COLOR_TEXT_SECONDARY,
                spacing_after=0.4 * cm,
            ),
        )

    layout.add_question_block(
        "Bilan : Dans quel(s) domaine(s) suis-je le plus en Scarcity ?",
        "surplus_bilan",
        config=QuestionConfig(
            box_height=3.5 * cm,
            subtitle="Identifiez vos zones de manque dominantes et ce qui les alimente.",
        ),
    )

    layout.render()

    # --- Page 2 : Générosité Stratégique & Projection ---
    layout2 = PageLayout(
        c,
        "Générosité Stratégique",
        config=LayoutConfig(part_title="6. MINDSET & ARCHÉTYPES"),
    )
    layout2.add_text(
        "Pour basculer vers le Surplus, il faut agir comme si le surplus existait déjà. Définissez 3 actions concrètes :",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout2.add_question_block(
        "1. Donner pour recevoir :",
        "surplus_action1",
        config=QuestionConfig(
            box_height=2.0 * cm,
            subtitle="Ex: Offrir du temps, un conseil, un petit montant à une cause.",
        ),
    )
    layout2.add_question_block(
        "2. Investir pour croître :",
        "surplus_action2",
        config=QuestionConfig(
            box_height=2.0 * cm,
            subtitle="Ex: S'offrir un livre, une formation, un outil de qualité.",
        ),
    )
    layout2.add_question_block(
        "3. Célébrer la réussite d'autrui :",
        "surplus_action3",
        config=QuestionConfig(
            box_height=2.0 * cm,
            subtitle="Au lieu d'envier, choisissez de célébrer. Quelle action concrète ?",
        ),
    )

    layout2.add_question_block(
        "La Question Clé de Projection :",
        "surplus_projection",
        config=QuestionConfig(
            box_height=4.0 * cm,
            subtitle="Si l'argent n'était plus un problème, quelle valeur créerais-je pour le monde ? Quel projet oserais-je lancer ?",
        ),
    )

    layout2.render()

def create_synthese_psycho_page(c):
    layout = PageLayout(
        c,
        "Synthèse : Mon Rapport à l'Argent",
        config=LayoutConfig(part_title="6. MINDSET & ARCHÉTYPES")
    )
    
    layout.add_text(
        "Ce que je retiens de mon rapport à l'argent",
        config=TextConfig(style_choice="subtitle", font_size=12, color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.3*cm)
    )
    
    layout.add_question_block(
        "La prise de conscience la plus importante que j'ai eue dans cette section :",
        "synth_psycho_q1",
        config=QuestionConfig(box_height=4.0*cm)
    )
    
    layout.add_question_block(
        "Ce dont je choisis de me libérer (croyance, habitude) à partir d'aujourd'hui :",
        "synth_psycho_q2",
        config=QuestionConfig(box_height=4.0*cm)
    )
    
    # Encadré croisé
    layout.add_text(
        "Mon Profil Financier Intégré",
        config=TextConfig(style_choice="subtitle", font_size=12, color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.2*cm)
    )
    layout.add_text(
        "En croisant votre scénario dominant (KMSI) et votre style naturel (Archétype), vous obtenez votre profil financier intégré. Ce profil éclaire votre façon de gérer l'argent et de prendre des décisions professionnelles.",
        config=TextConfig(font_size=10, spacing_after=0.4*cm)
    )
    
    layout.add_question_block(
        "Mon Money Script (KMSI) × Mon Archétype Sacré =",
        "synth_psycho_croise",
        config=QuestionConfig(
            box_height=4.5*cm,
            subtitle="Comment ces deux dimensions interagissent-elles ? Est-ce qu'elles se renforcent (ex: Vigilance + Accumulateur) ou créent-elles une tension (ex: Évitement + Connecteur) ?"
        )
    )
    
    layout.render()

def create_cartographie_page(c):
    layout = PageLayout(c, "Ma Cartographie Personnelle", config=LayoutConfig(part_title="7. SYNTHÈSE INTROSPECTIVE"))
    layout.add_text("Cette cartographie synthétise l'ensemble de votre travail d'introspection des séances 1 à 4. Elle servira de boussole pour la phase d'exploration.", config=TextConfig(spacing_after=0.3*cm))
    
    layout.add_question_block(
        "1. Mon Profil (Identité professionnelle)",
        "carto_profil",
        config=QuestionConfig(box_height=3.5*cm, subtitle="Type MBTI, Code RIASEC, Forces et Talents naturels")
    )
    
    layout.add_question_block(
        "2. Mes Moteurs (Sens et énergie)",
        "carto_moteurs",
        config=QuestionConfig(box_height=3.5*cm, subtitle="Valeurs fondamentales, Sujets et activités vibrants")
    )
    
    layout.add_question_block(
        "3. Mes Besoins (Écologie personnelle)",
        "carto_besoins",
        config=QuestionConfig(box_height=3.5*cm, subtitle="Besoins essentiels pour être bien, Sources de stress à éviter")
    )
    
    layout.add_question_block(
        "4. Mes Objectifs & Feedback Entourage",
        "carto_objectifs",
        config=QuestionConfig(box_height=3.5*cm, subtitle="Ce que j'aime faire, Envies pour demain, Pistes suggérées par les proches")
    )
    
    layout.render()

def create_exploration_page(c):
    layout = PageLayout(c, "Travail Inter-Session (S4/S5)", config=LayoutConfig(part_title="8. EXPLORATION"))
    layout.add_text("Il est temps d'ouvrir le champ des possibles ! Identifiez 2 à 3 pistes de métiers ou projets que vous aimeriez explorer.", config=TextConfig(spacing_after=0.3*cm))
    
    layout.add_text("Méthodes de recherche suggérées :", config=TextConfig(style_choice="subtitle", font_size=10, color=PDFStyle.COLOR_ACCENT_BLUE, spacing_after=0.1*cm))
    layout.add_text("• Interviews professionnelles (Réseau, LinkedIn)", config=TextConfig(font_size=9, color=PDFStyle.COLOR_TEXT_MAIN, spacing_after=0.1*cm))
    layout.add_text("• Immersion (Vis ma vie, stage d'observation)", config=TextConfig(font_size=9, color=PDFStyle.COLOR_TEXT_MAIN, spacing_after=0.1*cm))
    layout.add_text("• Recherche documentaire (ONISEP, fiches métiers, webinaires)", config=TextConfig(font_size=9, color=PDFStyle.COLOR_TEXT_MAIN, spacing_after=0.5*cm))
    
    layout.add_question_block(
        "Piste N°1 :",
        "explo_piste1",
        config=QuestionConfig(box_height=4.5*cm, subtitle="Métier ou projet envisagé ? Qu'est-ce qui résonne avec mes valeurs et moteurs ?")
    )
    
    layout.add_question_block(
        "Piste N°2 :",
        "explo_piste2",
        config=QuestionConfig(box_height=4.5*cm, subtitle="Alternative ou pivot possible ? En quoi cela répond à mes besoins essentiels ?")
    )
    
    layout.add_question_block(
        "Piste N°3 (Optionnelle) :",
        "explo_piste3",
        config=QuestionConfig(box_height=4.5*cm, subtitle="Une idée plus audacieuse (rêve d'enfant, projet passion) ? Qu'est-ce qui me retient de l'explorer ?")
    )
    
    layout.render()
