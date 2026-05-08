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
        ("2.", "Mes Moteurs Profonds (Valeurs & Actions)"),
        ("3.", "Mon Profil Financier (Money Script)"),
        ("4.", "Ma Biographie Financière (Les Racines)"),
        ("5.", "La Lettre à l'Argent (Acte Symbolique)"),
        ("6.", "Mon Archétype Sacré & Mindset de Surplus"),
        ("7.", "Ma Cartographie Personnelle (Synthèse S1 à S4)"),
        ("8.", "Travail Inter-Session S4/S5 (Exploration)"),
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
        "Vivre en accord avec ses valeurs nourrit l'Estime de Soi. Vivre en désaccord la détruit. À partir de la liste de valeurs de Schwarz, identifiez celles qui sont fondamentales pour vous.",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout.add_question_block(
        "1. Identification : Illustrez vos 3 valeurs principales par un exemple de votre vie :",
        "valeurs_q1",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout.add_question_block(
        "2. Héritage : De qui avez-vous reçu ces valeurs ?",
        "valeurs_q2",
        config=QuestionConfig(box_height=3.0 * cm),
    )
    layout.add_question_block(
        "3. Conflits de Valeurs : Identifiez un moment de conflit intérieur. Quelles étaient les valeurs en présence et comment ce conflit s'est-il résolu ?",
        "valeurs_q3",
        config=QuestionConfig(box_height=4.5 * cm),
    )
    layout.add_question_block(
        "Bilan : Ce que cet exercice m'apprend sur mes moteurs profonds et ce que ces conflits disent de positif sur moi :",
        "valeurs_q4",
        config=QuestionConfig(box_height=4.5 * cm),
    )

    layout.render()


def create_verbes_page(c):
    layout = PageLayout(
        c,
        "Mes Moteurs Profonds (Verbes d'Action)",
        config=LayoutConfig(part_title="2B. MES MOTEURS PROFONDS")
    )
    layout.add_text(
        "Quels sont les verbes qui vous mettent en mouvement ? (Ex: Organiser, Communiquer, Créer, Aider, Analyser, Diriger...)",
        config=TextConfig(spacing_after=0.3 * cm),
    )

    layout.add_question_block(
        "1. Les verbes que je préfère (Ceux que j'aime conjuguer au quotidien) :",
        "verbes_q1",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout.add_question_block(
        "2. Les verbes que j'aime le moins (Ceux qui m'épuisent) :",
        "verbes_q2",
        config=QuestionConfig(box_height=6.0 * cm),
    )
    layout.add_question_block(
        "Analyse : Quel lien faites-vous avec vos expériences passées et votre profil MBTI ?",
        "verbes_q3",
        config=QuestionConfig(box_height=6.0 * cm),
    )

    layout.render()


def create_psycho_edu_page(c):
    """Page d'introduction à la psychologie économique."""
    width, height = A4
    draw_page_background(c, width, height)
    card_margin = 2 * cm
    draw_side_panel(c, card_margin, width, height)

    text_x = card_margin + 1.0 * cm
    text_top = height - 5.0 * cm

    new_y = draw_title(c, "Introduction à la Psychologie Économique", pos=(text_x, text_top))

    text_y = new_y - 0.2 * cm
    c.setFont(PDFStyle.FONT_BODY, 11)
    c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)

    lines = [
        "Ce module vise à débloquer le 'thermostat financier' interne. La psychologie",
        "financière moderne repose largement sur les travaux du Dr. Bradley Klontz,",
        "qui a identifié quatre 'Money Scripts' (scénarios monétaires) inconscients,",
        "formés dès l'enfance, qui pilotent nos comportements d'adulte.",
        "",
        "1. Money Avoidance (Évitement)",
        "La croyance que l'argent est mauvais, sale, ou source d'anxiété. Ces individus",
        "ont tendance à sous-tarifier leurs services ou à ignorer leurs relevés bancaires.",
        "",
        "2. Money Worship (Adoration)",
        "La conviction que 'plus d'argent' résoudra tous les problèmes émotionnels. Cela",
        "conduit à un cycle de travail compulsif et à des achats compensatoires.",
        "",
        "3. Money Status (Statut)",
        "L'estime de soi est directement corrélée à la richesse nette. Ces profils sont",
        "à risque de dépenses ostentatoires et de fragilité en cas de perte d'emploi.",
        "",
        "4. Money Vigilance (Vigilance)",
        "Une prudence excessive, le secret et l'anxiété. Bien que favorable à l'épargne,",
        "ce script peut empêcher d'investir en soi par peur de manquer.",
        "",
        "La 'Money Biography' est un outil narratif qui connecte les souvenirs",
        "d'enfance aux comportements actuels. L'exercice consiste à remonter au premier",
        "souvenir d'argent pour décoder l'émotion associée et voir comment elle se",
        "réactive aujourd'hui."
    ]

    for line in lines:
        for s in simpleSplit(line, PDFStyle.FONT_BODY, 11, width - text_x - 1 * cm):
            c.drawString(text_x, text_y, s)
            text_y -= 0.6 * cm

    draw_page_decorations(
        c, width, height, part_title="3. PSYCHOLOGIE ÉCONOMIQUE", x_offset=card_margin
    )
    c.showPage()


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

def create_biographie_page(c):
    layout = PageLayout(c, "Ma Biographie Financière", config=LayoutConfig(part_title="4. LES RACINES"))
    layout.add_text("Identifiez vos souvenirs clés liés à l'argent pour comprendre vos programmations inconscientes.", config=TextConfig(spacing_after=0.3*cm))
    
    layout.add_question_block(
        "1. Le Premier Souvenir (souvent vers 5-7 ans)",
        "bio_premier_souvenir",
        config=QuestionConfig(box_height=4.5*cm, subtitle="Quel âge aviez-vous ? Qui était là ? Quelle était la situation ? Quelle émotion avez-vous ressentie (Joie, Honte, Peur...) ?")
    )
    
    layout.add_question_block(
        "2. L'Adolescence",
        "bio_adolescence",
        config=QuestionConfig(box_height=4.5*cm, subtitle="Premier argent gagné vs Argent de poche. Sentiment dominant : Autonomie ou Dépendance ? Comparaison sociale ?")
    )
    
    layout.add_question_block(
        "3. Analyse & Lien avec le Projet Pro",
        "bio_analyse",
        config=QuestionConfig(box_height=5.0*cm, subtitle="Pour chaque souvenir marquant : Quelle croyance ai-je formée ce jour-là qui est encore active aujourd'hui ?")
    )
    
    layout.render()

def create_dialogue_page(c):
    layout = PageLayout(c, "La Lettre à l'Argent", config=LayoutConfig(part_title="5. ACTE SYMBOLIQUE"))
    layout.add_text("L'argent est souvent chargé de projections affectives. En le traitant comme une personne distincte, on peut révéler ces projections.", config=TextConfig(spacing_after=0.3*cm))
    
    layout.add_question_block(
        "Prenez un moment de calme. Imaginez que l'Argent est une personne assise en face de vous. Écrivez-lui une lettre.",
        "lettre_argent",
        config=QuestionConfig(box_height=10.0*cm, subtitle="Structure : 1. Salutation / 2. L'État des lieux / 3. Le Reproche (ou Gratitude) / 4. La Demande de Changement")
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
    layout = PageLayout(c, "Mon Archétype Sacré", config=LayoutConfig(part_title="6. MINDSET & ARCHÉTYPES"))
    layout.add_text("Identifiez votre style de gestion naturel pour transformer vos défauts en atouts (Inspiré des Sacred Money Archetypes).", config=TextConfig(spacing_after=0.3*cm))
    
    archetypes = [
        "1. L'Accumulateur (Prudence, mais peur du manque)",
        "2. Le Connecteur (Réseautage, mais naïveté financière)",
        "3. L'Alchimiste (Transformateur, mais rejette la richesse)",
        "4. Le Dirigeant (Bâtisseur d'empire, mais jamais satisfait)",
        "5. Le Nourricier (Généreux, mais se sacrifie)",
        "6. Le Maverick (Innovateur, mais paris risqués)",
        "7. La Célébrité (Charismatique, dépenses ostentatoires)",
        "8. Le Romantique (Hédoniste, mais déni des réalités)"
    ]
    
    col1_x = layout.text_x
    col2_x = layout.text_x + layout.target_width / 2 + 0.5 * cm
    
    y_start = layout.y_cursor - 0.2 * cm
    for i, arch in enumerate(archetypes):
        x = col1_x if i % 2 == 0 else col2_x
        y = y_start - (i // 2) * 0.8 * cm
        layout.c.setFont(PDFStyle.FONT_BODY, 9)
        layout.c.setFillColor(PDFStyle.COLOR_TEXT_MAIN)
        layout.c.drawString(x, y, arch)
    
    layout.y_cursor = y_start - 3.8 * cm
    
    layout.add_question_block(
        "Mon Top 3 des Archétypes :",
        "archetypes_top3",
        config=QuestionConfig(box_height=2.5*cm)
    )
    
    layout.add_question_block(
        "Plan d'Action Personnalisé :",
        "archetypes_action",
        config=QuestionConfig(box_height=6.0*cm, subtitle="Compte tenu de mon archétype dominant, quelle est la prochaine action la plus alignée (mais inconfortable) que je dois poser ?")
    )
    
    layout.render()

def create_mindset_surplus_page(c):
    pass

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
    
    layout.add_question_block(
        "Piste N°1 :",
        "explo_piste1",
        config=QuestionConfig(box_height=5.0*cm, subtitle="Quoi ? Pourquoi cela m'attire ? Quelles sont mes interrogations ?")
    )
    
    layout.add_question_block(
        "Piste N°2 :",
        "explo_piste2",
        config=QuestionConfig(box_height=5.0*cm, subtitle="Quoi ? Pourquoi cela m'attire ? Quelles sont mes interrogations ?")
    )
    
    layout.add_question_block(
        "Piste N°3 (Optionnelle) :",
        "explo_piste3",
        config=QuestionConfig(box_height=5.0*cm, subtitle="Quoi ? Pourquoi cela m'attire ? Quelles sont mes interrogations ?")
    )
    
    layout.render()
