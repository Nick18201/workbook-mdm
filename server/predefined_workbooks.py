"""
Catalogue des livrets pédagogiques de référence (MDM Bilan de Compétences & Business Plan).
Fournit les spécifications canoniques (WorkbookSpec) prêtes à être personnalisées pour chaque bénéficiaire.
"""

from typing import Dict, List, Optional
from server.models import WorkbookSpec, PageSpec, BlockSpec, TemplateInfo


def _build_chap0_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=0,
        chapter_title="Le Prélude : Onboarding & Démarrage",
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        theme="indigo",
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="MON LIVRE DE TRANSITION",
                part_title="ACCUEIL & DÉMARRAGE",
                params={
                    "subtitle": "Chapitre 0 : Le Prélude",
                    "title": "BILAN DE COMPÉTENCES & ALIGNEMENT",
                },
            ),
            PageSpec(
                template="summary",
                title="AU PROGRAMME DU PRÉLUDE",
                part_title="0. CADRAGE INITIAL",
                params={
                    "intro_text": "Ce premier livret scelle notre alliance de travail et pose les fondations de votre transition.",
                    "points": [
                        {"label": "01", "desc": "Prendre du recul sur vos choix passés et vos expériences."},
                        {"label": "02", "desc": "Le pacte de confiance et les 3 règles du jeu."},
                        {"label": "03", "desc": "Votre intention majeure et l'autorisation personnelle."},
                        {"label": "04", "desc": "Engagement formel envers votre futur professionnel."},
                    ],
                },
            ),
            PageSpec(
                template="composite",
                title="Bienvenue dans votre Transition",
                part_title="1. MOT D'OUVERTURE",
                blocks=[
                    BlockSpec(
                        type="callout",
                        title="Le sens de cette démarche",
                        text="Si vous lisez ceci, c'est que vous avez choisi de vous mettre en mouvement. Ce livret n'est pas un simple rapport scolaire : c'est le réceptacle de votre histoire, de vos découvertes et de vos ambitions futures.",
                        variant="quote",
                    ),
                    BlockSpec(
                        type="scale",
                        label="Votre niveau d'enthousiasme et d'énergie au démarrage :",
                        min_val=0,
                        max_val=10,
                        min_label="0 · Hésitant",
                        max_label="10 · Déterminé",
                    ),
                ],
            ),
            PageSpec(
                template="two_columns",
                title="Le Cadre de Confiance : Les 3 Piliers",
                part_title="2. ALLIANCE DE TRAVAIL",
                params={
                    "intro_text": "Notre espace d'échange est sécurisé par trois engagements réciproques fondamentaux.",
                    "col1_header": "Pilier du Cadre",
                    "col2_header": "Ce que cela signifie concrètement",
                    "rows": [
                        {
                            "label": "1. Confidentialité totale",
                            "left_tooltip": "Espace protégé et sans jugement",
                            "right_tooltip": "Tout ce qui est déposé ici reste strictement entre nous.",
                        },
                        {
                            "label": "2. Authenticité sans masque",
                            "left_tooltip": "Oser dire vos vrais doutes",
                            "right_tooltip": "C'est votre vérité brute qui nous permettra de construire le bon cap.",
                        },
                        {
                            "label": "3. Action & Mouvement",
                            "left_tooltip": "L'expérimentation concrète",
                            "right_tooltip": "La clarté naît du mouvement et des petits pas, pas seulement de la pensée.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Mon Intention & Mon Autorisation",
                part_title="3. DIRECTION DU CŒUR",
                params={
                    "intro_text": "Avant de plonger dans le bilan, clarifions votre intention profonde et vos conditions de succès.",
                    "questions": [
                        {
                            "question": "D'ici 3 à 4 mois, quelle serait votre plus grande victoire à l'issue de cet accompagnement ?",
                            "subtitle": "Formulez le résultat concret qui changerait votre quotidien professionnel.",
                            "example": "Avoir un cap clair, validé financièrement, et me lever avec enthousiasme chaque matin.",
                            "field_id": "p0_q1_intention",
                        },
                        {
                            "question": "Quelle autorisation personnelle choisissez-vous de vous accorder dès aujourd'hui ?",
                            "subtitle": "Ce que vous vous interdisez d'habitude (douter, rêver grand, ralentir, dire non...).",
                            "example": "Je m'autorise à explorer sans me censurer par peur du regard des autres.",
                            "field_id": "p0_q2_autorisation",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Mon Pacte d'Engagement Initial",
                part_title="4. PACTE SOLENNEL",
                params={
                    "lines": [
                        "Je m'engage à investir au minimum 2 heures par semaine dans mes réflexions et exercices.",
                        "J'accepte de traverser les moments d'inconfort ou de doute comme des étapes normales d'apprentissage.",
                        "Je m'autorise à explorer des pistes nouvelles sans jugement prématuré de faisabilité.",
                        "Ce travail est un investissement bienveillant et prioritaire pour mon avenir.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Votre Parcours Commence",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Félicitations pour ce premier pas décisif.",
                        "Respirez, faites confiance au processus.",
                        "Rendez-vous à notre séance 1 pour poser l'état des lieux complet.",
                    ],
                },
            ),
        ],
    )


def _build_chap1_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=1,
        chapter_title="L'État des Lieux & La Boussole",
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        theme="indigo",
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="L'ÉTAT DES LIEUX",
                part_title="CHAPITRE 1",
                params={
                    "subtitle": "Chapitre 1 : L'État des Lieux 🧭",
                    "title": "BILAN DE COMPÉTENCES & ALIGNEMENT",
                },
            ),
            PageSpec(
                template="summary",
                title="AU PROGRAMME DU CHAPITRE",
                part_title="1. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Figer le point de départ pour mesurer le chemin parcouru à la fin de notre parcours.",
                    "points": [
                        {"label": "01", "desc": "Météo intérieure : état d'esprit et énergie du jour."},
                        {"label": "02", "desc": "Vision 360° : équilibre entre les 4 dimensions de vie."},
                        {"label": "03", "desc": "Objectif Boussole : le cap prioritaire à horizon 3 mois."},
                        {"label": "04", "desc": "Le Sac à dos : ce que vous choisissez de déposer."},
                        {"label": "05", "desc": "Pacte d'engagement pour franchir les premières étapes."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Mon État d'Esprit Actuel",
                part_title="1. MÉTÉO DU MOMENT",
                params={
                    "emotion_prompt": "Aujourd'hui, je me sens :",
                    "energy_prompt": "Mon niveau d'énergie actuel :",
                    "thought_prompt": "Ce qui prend le plus de place dans ma tête en arrivant :",
                },
            ),
            PageSpec(
                template="quadrants",
                title="Ma Vision 360°",
                part_title="2. ÉQUILIBRE GLOBAL",
                params={
                    "instruction": "Pour chaque domaine, notez en une phrase votre constat actuel et votre aspiration.",
                    "quadrants": [
                        {"title": "Professionnel", "subtitle": "Sens, Mission, Rémunération"},
                        {"title": "Personnel", "subtitle": "Temps pour soi, Santé, Rythme"},
                        {"title": "Social & Familial", "subtitle": "Relations, Présence aux proches"},
                        {"title": "Cadre & Autonomie", "subtitle": "Liberté vs Sécurité, Règles du jeu"},
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Mon Objectif Boussole",
                part_title="3. CAP STRATÉGIQUE",
                params={
                    "intro_text": "Clarifier votre enjeu prioritaire pour canaliser vos efforts tout au long du bilan.",
                    "questions": [
                        {
                            "question": "D'ici 3 à 6 mois, quel est l'enjeu professionnel que vous voulez impérativement avoir clarifié ?",
                            "subtitle": "Formulez un objectif stimulant, clair et libérateur.",
                            "example": "Avoir identifié 2 pistes professionnelles viables et cohérentes avec mes valeurs.",
                            "field_id": "p1_q1_boussole",
                        },
                        {
                            "question": "À quoi mesurerez-vous concrètement que votre bilan est une réussite totale ?",
                            "subtitle": "Un indicateur ou une situation concrète observable dans votre quotidien.",
                            "example": "J'aurai une offre signée ou un calendrier précis de lancement sans anxiété.",
                            "field_id": "p1_q2_kpi",
                        },
                    ],
                },
            ),
            PageSpec(
                template="two_columns",
                title="Le Sac à Dos : Ce que je dépose",
                part_title="4. ALLÉGEMENT & DÉPÔT",
                params={
                    "intro_text": "Pour avancer librement, nous identifions les charges et croyances que vous cessez de porter seul(e).",
                    "col1_header": "Ce qui pèse (Charge / Croyance)",
                    "col2_header": "Ce que je choisis (Levier / Dépôt)",
                    "rows": [
                        {
                            "label": "1. Exigence ou injonction",
                            "left_tooltip": "Ex: Je dois tout maîtriser avant d'oser en parler",
                            "right_tooltip": "Ex: L'action imparfaite m'apprendra plus que l'attente silencieuse.",
                        },
                        {
                            "label": "2. Situation subie",
                            "left_tooltip": "Ex: Accepter des urgences au détriment de mes priorités",
                            "right_tooltip": "Ex: Poser des limites explicites dès le début de semaine.",
                        },
                        {
                            "label": "3. Peur dominante",
                            "left_tooltip": "Ex: La peur de ne pas être légitime dans un nouveau secteur",
                            "right_tooltip": "Ex: M'appuyer sur mes compétences transférables et ma capacité d'apprentissage.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Mon Pacte d'Engagement",
                part_title="5. ANCRAGE",
                params={
                    "lines": [
                        "Je m'engage à préserver ce temps d'introspection comme un espace privilégié.",
                        "Je regarde mes freins avec curiosité et lucidité, sans autocritique.",
                        "Je teste au moins une action concrète entre chaque séance de coaching.",
                        "Ce travail est guidé par mon désir d'alignement et de liberté professionnelle.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Point de Départ Validé",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Bravo pour cette cartographie initiale posée avec franchise.",
                        "Laissez infuser ces prises de conscience jusqu'à notre prochain échange.",
                        "La boussole est prête : cap vers l'exploration de vos racines et forces.",
                    ],
                },
            ),
        ],
    )


def _build_chap2_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=2,
        chapter_title="L'Histoire, Les Racines & Les Mentors",
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        theme="indigo",
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="L'HISTOIRE & LES RACINES",
                part_title="CHAPITRE 2",
                params={
                    "subtitle": "Chapitre 2 : L'Histoire & Les Racines 🌳",
                    "title": "BILAN DE COMPÉTENCES & ALIGNEMENT",
                },
            ),
            PageSpec(
                template="summary",
                title="AU PROGRAMME DU CHAPITRE",
                part_title="2. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Explorer votre fil rouge professionnel pour comprendre les logiques de vos choix passés.",
                    "points": [
                        {"label": "01", "desc": "Météo d'ouverture et état d'esprit."},
                        {"label": "02", "desc": "L'héritage professionnel : ce que j'ai reçu vs ce que je choisis."},
                        {"label": "03", "desc": "Mes figures inspirantes et mentors de parcours."},
                        {"label": "04", "desc": "L'Arbre de Vie : compétences souterraines et fruits visibles."},
                        {"label": "05", "desc": "Pacte de reconnaissance envers mon parcours."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Mon Énergie d'Exploration",
                part_title="1. MÉTÉO DU MOMENT",
                params={
                    "emotion_prompt": "En repensant à mon parcours, je me sens :",
                    "energy_prompt": "Mon niveau d'énergie pour explorer mon histoire :",
                    "thought_prompt": "Le souvenir professionnel le plus saillant qui me revient en tête :",
                },
            ),
            PageSpec(
                template="two_columns",
                title="Héritage Professionnel : Reçu vs Choisi",
                part_title="2. TRANSMISSION & AFFRANCHISSEMENT",
                params={
                    "intro_text": "Distinguer les modèles inculqués par votre milieu de vos véritables aspirations intimes.",
                    "col1_header": "Ce que j'ai reçu (Modèle / Injonction)",
                    "col2_header": "Ce que je choisis d'incarner aujourd'hui",
                    "rows": [
                        {
                            "label": "1. Définition de la réussite",
                            "left_tooltip": "Ex: La sécurité du statut et la progression hiérarchique continue",
                            "right_tooltip": "Ex: L'autonomie, l'utilité sociale et la liberté d'organisation.",
                        },
                        {
                            "label": "2. Rapport au travail",
                            "left_tooltip": "Ex: Il faut souffrir pour mériter son salaire",
                            "right_tooltip": "Ex: Le plaisir et l'impact peuvent cohabiter avec l'effort.",
                        },
                        {
                            "label": "3. Rapport à l'échec",
                            "left_tooltip": "Ex: Changer de voie est un aveu de faiblesse",
                            "right_tooltip": "Ex: Se réinventer est une preuve d'intelligence et de courage.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Mes Mentors & Figures Inspirantes",
                part_title="3. INSPIRATION",
                params={
                    "intro_text": "Ceux qui nous inspirent nous révèlent nos propres potentiels encore endormis.",
                    "questions": [
                        {
                            "question": "Quelles sont les 2 personnes (réelles ou de fiction) dont le parcours ou la posture vous inspirent le plus ?",
                            "subtitle": "Expliquez brièvement ce qui résonne en vous chez chacune d'elles.",
                            "example": "Une ancienne manager qui savait écouter sans juger et un entrepreneur engagé dans la transition.",
                            "field_id": "p2_q1_mentors",
                        },
                        {
                            "question": "Quelle qualité fondamentale admirez-vous chez elles et souhaitez-vous développer chez vous ?",
                            "subtitle": "Cette qualité est déjà en germe dans votre personnalité.",
                            "example": "L'audace tranquille de dire ce qui est juste même quand c'est difficile.",
                            "field_id": "p2_q2_qualite",
                        },
                    ],
                },
            ),
            PageSpec(
                template="quadrants",
                title="Mon Arbre de Vie Professionnel",
                part_title="4. CARTOGRAPHIE DES FORCES",
                params={
                    "instruction": "Synthétisez vos ressources d'hier et de demain en 4 strates complémentaires.",
                    "quadrants": [
                        {"title": "Racines & Fondations", "subtitle": "Diplômes, valeurs familiales, premières victoires"},
                        {"title": "Tronc & Savoirs Solides", "subtitle": "Compétences techniques et managériales éprouvées"},
                        {"title": "Branches & Projets Marquants", "subtitle": "Réalisations dont je suis particulièrement fier(ère)"},
                        {"title": "Fruits & Graines Futures", "subtitle": "Compétences transférables vers mon futur métier"},
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Mon Pacte de Gratitude & Filiation",
                part_title="5. RECONNAISSANCE",
                params={
                    "lines": [
                        "Je reconnais la valeur de chacune de mes expériences, y compris les plus rudes.",
                        "Je cesse de regretter mes détours : ils ont forgé ma singularité.",
                        "Je prends la responsabilité pleine et entière de mes choix professionnels à venir.",
                        "Je construis mon avenir sur des racines solides et assumées.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Vos Racines Sont Posées",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Vous savez désormais d'où vous puisez votre force.",
                        "Prochaine étape : révéler vos zones d'excellence et talents cachés.",
                        "Prenez le temps d'honorer le chemin déjà parcouru.",
                    ],
                },
            ),
        ],
    )


def _build_chap3_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=3,
        chapter_title="Les Compétences, Talents & Moteurs",
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        theme="indigo",
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="COMPÉTENCES & TALENTS",
                part_title="CHAPITRE 3",
                params={
                    "subtitle": "Chapitre 3 : Compétences, Talents & Moteurs ⭐",
                    "title": "BILAN DE COMPÉTENCES & ALIGNEMENT",
                },
            ),
            PageSpec(
                template="summary",
                title="AU PROGRAMME DU CHAPITRE",
                part_title="3. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Démêler ce que vous savez faire par obligation de ce qui vous met véritablement en énergie.",
                    "points": [
                        {"label": "01", "desc": "Check-in vitalité et diagnostic d'énergie."},
                        {"label": "02", "desc": "Moteurs d'enthousiasme vs Fuites d'énergie."},
                        {"label": "03", "desc": "Matrice des 4 Zones de Compétences (dont la zone de génie)."},
                        {"label": "04", "desc": "Mes 3 Verbes d'Action privilégiés."},
                        {"label": "05", "desc": "Pacte de valorisation de mon expertise."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Mon Baromètre d'Énergie",
                part_title="1. VITALITÉ AU TRAVAIL",
                params={
                    "emotion_prompt": "Dans mon travail actuel, je me sens le plus souvent :",
                    "energy_prompt": "Niveau d'énergie moyen à la fin d'une journée type :",
                    "thought_prompt": "L'activité de ma semaine qui m'a procuré le plus de plaisir :",
                },
            ),
            PageSpec(
                template="two_columns",
                title="Moteurs d'Énergie vs Vampires d'Énergie",
                part_title="2. DYNAMIQUE VITALISANTE",
                params={
                    "intro_text": "Identifier avec précision les contextes et tâches qui vous ressourcent ou vous consument.",
                    "col1_header": "Ce qui m'épuise (Vampire d'énergie)",
                    "col2_header": "Ce qui me revitalise (Moteur de flow)",
                    "rows": [
                        {
                            "label": "1. Type de tâche",
                            "left_tooltip": "Ex: Remplir des tableaux de suivi et justifier les budgets en réunion",
                            "right_tooltip": "Ex: Résoudre un problème complexe avec une équipe motivée.",
                        },
                        {
                            "label": "2. Mode relationnel",
                            "left_tooltip": "Ex: Devoir gérer des micro-conflits d'ego sans vision claire",
                            "right_tooltip": "Ex: Transmettre une méthode et voir progresser un collaborateur.",
                        },
                        {
                            "label": "3. Temporalité",
                            "left_tooltip": "Ex: L'urgence permanente et le multitâche haché",
                            "right_tooltip": "Ex: Les blocs de travail profond sur un sujet porteur de sens.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="quadrants",
                title="La Matrice des 4 Zones de Compétences",
                part_title="3. ZONE D'EXCELLENCE",
                params={
                    "instruction": "Répartissez vos activités phares dans les 4 quadrants pour viser votre zone de flow.",
                    "quadrants": [
                        {"title": "Zone de Génie (Excellence)", "subtitle": "Facile pour moi + Me donne une énergie immense"},
                        {"title": "Zone de Compétence", "subtitle": "Je sais très bien faire, mais cela me laisse neutre"},
                        {"title": "Zone d'Apprentissage", "subtitle": "Je ne maîtrise pas encore, mais cela me stimule"},
                        {"title": "Zone de Risque (Piège)", "subtitle": "Je sais faire mais cela m'épuise profondément"},
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Mes Verbes d'Action Privilégiés",
                part_title="4. SIGNATURE D'ACTION",
                params={
                    "intro_text": "Les métiers changent, mais vos verbes d'action signature demeurent constants.",
                    "questions": [
                        {
                            "question": "Quels sont les 3 verbes d'action qui décrivent le mieux ce que vous aimez faire de bout en bout ?",
                            "subtitle": "Exemples : Fédérer, Analyser, Concevoir, Simplifier, Transmettre, Bâtir...",
                            "example": "Structurer des idées complexes, négocier des accords équilibrés, inspirer une équipe.",
                            "field_id": "p3_q1_verbes",
                        },
                        {
                            "question": "Dans quel cadre ou secteur aimeriez-vous que ces verbes s'expriment en priorité demain ?",
                            "subtitle": "Projetez-vous sur une mission ou un univers professionnel stimulant.",
                            "example": "Dans une organisation agile où les décisions sont rapides et orientées impact.",
                            "field_id": "p3_q2_cadre",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Mon Pacte de Juste Mobilisation",
                part_title="5. VALORISATION",
                params={
                    "lines": [
                        "Je reconnais mes talents naturels sans minimiser leur rareté ni leur valeur.",
                        "Je refuse désormais d'investir 80% de mon temps dans des activités qui m'épuisent.",
                        "Je choisis de cultiver ma zone d'excellence comme mon premier atout professionnel.",
                        "Je fais confiance à mes forces transférables pour aborder de nouveaux horizons.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Vos Talents Sont Éclairés",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Vous avez mis des mots précis sur ce qui vous rend singulier(ère).",
                        "Gardez vos verbes d'action comme boussole quotidienne.",
                        "Prochaine étape : aligner ces forces avec vos valeurs et votre équilibre financier.",
                    ],
                },
            ),
        ],
    )


def _build_chap4_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=4,
        chapter_title="Valeurs, Limites & Rapport à l'Argent",
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        theme="indigo",
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="VALEURS & RAPPORT À L'ARGENT",
                part_title="CHAPITRE 4",
                params={
                    "subtitle": "Chapitre 4 : Valeurs, Limites & Argent ⚖️",
                    "title": "BILAN DE COMPÉTENCES & ALIGNEMENT",
                },
            ),
            PageSpec(
                template="summary",
                title="AU PROGRAMME DU CHAPITRE",
                part_title="4. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Définir vos non-négociables et assainir votre équilibre économique pour un projet durable.",
                    "points": [
                        {"label": "01", "desc": "Météo et niveau de stress professionnel actuel."},
                        {"label": "02", "desc": "Les 4 Piliers de vie et la pose de limites protectrices."},
                        {"label": "03", "desc": "Passerelle des croyances financières : du blocage au levier."},
                        {"label": "04", "desc": "Mon Minimum Vital et mon Idéal d'Équilibre Financier."},
                        {"label": "05", "desc": "Pacte de respect de mes limites et de ma valeur marchande."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Mon État de Clarté & Charge Mentale",
                part_title="1. DIAGNOSTIC INTERNE",
                params={
                    "emotion_prompt": "Face à mes choix de carrière et de rémunération, je ressens :",
                    "energy_prompt": "Mon niveau de sérénité financière actuelle :",
                    "thought_prompt": "La limite que je laisse trop souvent franchir dans mon quotidien :",
                },
            ),
            PageSpec(
                template="quadrants",
                title="Mes 4 Piliers de Vie & Limites Saines",
                part_title="2. CADRE DE PROTECTION",
                params={
                    "instruction": "Pour chaque pilier, notez la règle d'or non négociable que vous vous engagez à respecter.",
                    "quadrants": [
                        {"title": "Pilier Professionnel", "subtitle": "Exigence de respect, éthique, charge de travail"},
                        {"title": "Pilier Personnel & Santé", "subtitle": "Sommeil, sport, déconnexion réelle le soir"},
                        {"title": "Pilier Relations & Proches", "subtitle": "Présence de qualité, temps partagé sans écran"},
                        {"title": "Pilier Économique & Cadre", "subtitle": "Rémunération juste, trésorerie de sécurité"},
                    ],
                },
            ),
            PageSpec(
                template="two_columns",
                title="Passerelle des Croyances Financières",
                part_title="3. DÉCONSTRUCTION DU RAPPORT À L'ARGENT",
                params={
                    "intro_text": "Transformer les peurs économiques en principes d'action pragmatiques et sécurisants.",
                    "col1_header": "Croyance limitante / Peur",
                    "col2_header": "Croyance ressource / Principe de réalité",
                    "rows": [
                        {
                            "label": "1. Légitimité et tarification",
                            "left_tooltip": "Ex: Si je demande un bon tarif, je vais faire fuir les opportunités",
                            "right_tooltip": "Ex: Un tarif juste garantit mon engagement et filtre les projets toxiques.",
                        },
                        {
                            "label": "2. Sécurité du salariat",
                            "left_tooltip": "Ex: Seul un CDI me protège des aléas de la vie",
                            "right_tooltip": "Ex: La vraie sécurité réside dans mon réseau et mon employabilité active.",
                        },
                        {
                            "label": "3. Éthique et rémunération",
                            "left_tooltip": "Ex: Gagner beaucoup d'argent n'est pas aligné avec l'impact social",
                            "right_tooltip": "Ex: La prospérité financière est un amplificateur de mon pouvoir d'action.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Mon Équilibre Économique Réel",
                part_title="4. CHIFFRES & SÉRÉNITÉ",
                params={
                    "intro_text": "Sortir du flou financier pour poser des seuils chiffrés libérateurs.",
                    "questions": [
                        {
                            "question": "Quel est votre montant mensuel net incompressible ('plancher de sérénité') ?",
                            "subtitle": "Ce dont vous avez absolument besoin pour couvrir vos charges sans angoisse.",
                            "example": "2 800 € net / mois en base incompressible, et 4 200 € en cible idéale d'équilibre.",
                            "field_id": "p4_q1_plancher",
                        },
                        {
                            "question": "Quelle limite ferme posez-vous désormais face aux sollicitations urgentes et gratuites ?",
                            "subtitle": "Un engagement verbal ou pratique pour préserver votre temps de travail de fond.",
                            "example": "Pas de réunion avant 10h le matin et aucun devis sans entretien de cadrage préalable.",
                            "field_id": "p4_q2_limite",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Mon Pacte de Respect & Juste Valeur",
                part_title="5. ALIGNEMENT FINANCIER",
                params={
                    "lines": [
                        "J'assume pleinement la valeur économique de mon travail et de mon temps.",
                        "Je m'engage à honorer mes limites personnelles avec autant de fermeté que mes contrats.",
                        "Je traite l'argent comme un outil au service de mon projet de vie, et non l'inverse.",
                        "Je m'autorise à viser une rémunération confortable sans culpabilité.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Vos Limites Sont Clarifiées",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Vous avez posé les garde-fous indispensables à votre liberté future.",
                        "La clarté sur vos chiffres désamorce les plus grandes peurs.",
                        "Prochaine étape : aller sonder le marché et mener vos enquêtes de terrain.",
                    ],
                },
            ),
        ],
    )


def _build_chap5_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=5,
        chapter_title="L'Exploration Terrain, Enquête & Marché",
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        theme="indigo",
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="EXPLORATION TERRAIN & MARCHÉ",
                part_title="CHAPITRE 5",
                params={
                    "subtitle": "Chapitre 5 : Exploration Terrain & Marché 🔍",
                    "title": "BILAN DE COMPÉTENCES & ALIGNEMENT",
                },
            ),
            PageSpec(
                template="summary",
                title="AU PROGRAMME DU CHAPITRE",
                part_title="5. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Sortir de l'analyse en chambre pour confronter vos idées à la réalité des acteurs du secteur.",
                    "points": [
                        {"label": "01", "desc": "Adopter la posture de l'enquêteur bienveillant."},
                        {"label": "02", "desc": "Fiche de conduite d'interview réseau et métier."},
                        {"label": "03", "desc": "Idées reçues vs Réalité du terrain : le décryptage."},
                        {"label": "04", "desc": "Démarche réseau et 3 contacts cibles à actionner."},
                        {"label": "05", "desc": "Pacte d'audace et de curiosité exploratoire."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Mon Énergie de Réseau & Rencontre",
                part_title="1. POSTURE EXTÉRIEURE",
                params={
                    "emotion_prompt": "À l'idée d'interviewer des professionnels inconnus, je me sens :",
                    "energy_prompt": "Mon niveau d'audace pour activer mon réseau :",
                    "thought_prompt": "Le doute principal qui pourrait me faire procrastiner l'action :",
                },
            ),
            PageSpec(
                template="enquete",
                title="Grille d'Enquête Métier & Réseau",
                part_title="2. INTERVIEWS QUALITATIVES",
                params={
                    "intro_text": "Lors de vos entretiens exploratoires de 20 minutes, explorez ces 3 dimensions clés.",
                    "questions": [
                        {
                            "title": "1. Le Quotidien Réel & Les Pièges du Métier",
                            "subtitle": "Ce que les fiches de poste ne disent jamais (pressions, horaires, frictions).",
                        },
                        {
                            "title": "2. Les Tendances & Besoins Non Satisfaits",
                            "subtitle": "Ce qui manque sur le marché et où se trouvent les budgets réels.",
                        },
                        {
                            "title": "3. Les Conseils Clés pour Réussir son Entrée",
                            "subtitle": "Les compétences indispensables à valoriser et les erreurs à éviter.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="two_columns",
                title="Idées Reçues vs Réalité du Terrain",
                part_title="3. CRASH-TEST INTELLECTUEL",
                params={
                    "intro_text": "Comparer vos représentations idéalisées ou anxiogènes avec les retours concrets des pairs.",
                    "col1_header": "Ce que j'imaginais (Fantasme / Crainte)",
                    "col2_header": "Ce que le terrain révèle (Réalité éprouvée)",
                    "rows": [
                        {
                            "label": "1. Accès au secteur",
                            "left_tooltip": "Ex: Il faut impérativement un master ou 10 ans de réseau local",
                            "right_tooltip": "Ex: La motivation, l'écoute et une expertise hybride ouvrent les portes.",
                        },
                        {
                            "label": "2. Charge de travail",
                            "left_tooltip": "Ex: Tous les professionnels du domaine travaillent 60h/semaine",
                            "right_tooltip": "Ex: Ceux qui posent un cadre clair préservent leurs week-ends.",
                        },
                        {
                            "label": "3. Modèle de revenus",
                            "left_tooltip": "Ex: Les débuts sont obligatoirement précaires pendant 2 ans",
                            "right_tooltip": "Ex: Avec une offre ciblée, les premières missions tombent en 60 jours.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Mes 3 Cibles Réseau & Prochains Pas",
                part_title="4. PLAN DE CONTACT",
                params={
                    "intro_text": "Transformer l'intention en démarche de prise de rendez-vous immédiate.",
                    "questions": [
                        {
                            "question": "Quelles sont les 3 personnes ou profils d'experts que vous allez solliciter sous 10 jours ?",
                            "subtitle": "Indiquez nom, fonction ou structure cible.",
                            "example": "Un consultant RSE indépendant, la directrice d'une coopérative locale et un pair alumni.",
                            "field_id": "p5_q1_cibles",
                        },
                        {
                            "question": "Quelle phrase d'accroche courtoise et curieuse allez-vous utiliser pour demander 20 min ?",
                            "subtitle": "Rappel : vous ne demandez pas un travail, vous sollicitez leur éclairage d'expert.",
                            "example": "« En démarche d'évolution vers l'éco-conception, vos réflexions récentes m'inspirent... »",
                            "field_id": "p5_q2_accroche",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Mon Pacte d'Exploration Terrain",
                part_title="5. ENGAGEMENT TERRAIN",
                params={
                    "lines": [
                        "J'aborde mes entretiens avec une curiosité désintéressée et chaleureuse.",
                        "J'accepte que certaines personnes ne répondent pas sans en faire une affaire personnelle.",
                        "Je m'engage à mener au moins 3 entretiens réels avant d'arrêter mon choix.",
                        "Je note chaque apprentissage précieux dans mon dossier de transition.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Le Terrain Vous Attend",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Chaque rencontre confirmera ou ajustera votre trajectoire.",
                        "Les opportunités naissent toujours à l'intersection de la curiosité et de l'action.",
                        "Prochaine étape : arbitrer votre cap et bâtir votre feuille de route 30·60·90 jours.",
                    ],
                },
            ),
        ],
    )


def _build_chap6_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=6,
        chapter_title="Le Plan d'Action, Arbitrage & Feuille de Route",
        subtitle="BILAN DE COMPÉTENCES & ALIGNEMENT",
        theme="indigo",
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="PLAN D'ACTION & CAP",
                part_title="CHAPITRE 6",
                params={
                    "subtitle": "Chapitre 6 : Plan d'Action & Cap 🚀",
                    "title": "BILAN DE COMPÉTENCES & ALIGNEMENT",
                },
            ),
            PageSpec(
                template="summary",
                title="AU PROGRAMME DU CHAPITRE",
                part_title="6. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Transformer toutes les pépites récoltées en une stratégie opérationnelle irréversible.",
                    "points": [
                        {"label": "01", "desc": "Check-in de clôture et état d'alignement."},
                        {"label": "02", "desc": "Arbitrage stratégique : Piste A vs Piste B."},
                        {"label": "03", "desc": "Feuille de route opérationnelle 30 · 60 · 90 Jours."},
                        {"label": "04", "desc": "Garde-fous anti-dispersion et réseau d'alliés."},
                        {"label": "05", "desc": "Le Grand Pacte d'engagement final."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Mon Énergie d'Action & Détermination",
                part_title="1. ÉLAN DE DÉPART",
                params={
                    "emotion_prompt": "À l'aube de déployer mon nouveau cap, je ressens :",
                    "energy_prompt": "Mon niveau d'alignement et de confiance globale :",
                    "thought_prompt": "Ce qui a le plus profondément changé en moi depuis le début du bilan :",
                },
            ),
            PageSpec(
                template="two_columns",
                title="Arbitrage Stratégique : Piste A vs Piste B",
                part_title="2. CHOIX ÉCLAIRÉ DE CAP",
                params={
                    "intro_text": "Mettre en miroir votre scénario prioritaire (L'Étoile) et votre filet de sécurité réaliste.",
                    "col1_header": "Piste A : Scénario Majeur (L'Étoile)",
                    "col2_header": "Piste B : Alternative / Étape Passerelle",
                    "rows": [
                        {
                            "label": "1. Intitulé & Nature du cap",
                            "left_tooltip": "Ex: Lancer mon cabinet de conseil indépendant à impact",
                            "right_tooltip": "Ex: Prendre un poste de direction RSE en transition dans une PME.",
                        },
                        {
                            "label": "2. Atouts & Enthousiasme",
                            "left_tooltip": "Ex: Liberté totale de décision et adéquation parfaite à mes valeurs",
                            "right_tooltip": "Ex: Salaire garanti immédiat et constitution d'un réseau solide.",
                        },
                        {
                            "label": "3. Risques & Points de vigilance",
                            "left_tooltip": "Ex: Pression commerciale initiale et gestion solitaire",
                            "right_tooltip": "Ex: Risque de retomber dans des schémas d'hyper-hiérarchie.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="roadmap",
                title="Feuille de Route : 30 · 60 · 90 Jours",
                part_title="3. TRAJECTOIRE OPÉRATIONNELLE",
                params={
                    "intro_text": "Découper la montagne en paliers digestes et cadencés pour garantir le succès.",
                    "stages": [
                        {
                            "period": "PALIER 1 · 0 À 30 JOURS",
                            "theme": "SÉCURISER & STRUCTURER",
                            "default_obj": "Valider le cadre financier et formaliser mes supports de communication.",
                            "default_kpi": "Tableau de trésorerie prêt + profil LinkedIn actualisé.",
                            "actions": [
                                "Finaliser les rendez-vous administratifs ou financiers",
                                "Poser mes 3 premiers créneaux de travail sanctuarisés par semaine",
                                "Informer 10 contacts proches de mon nouveau positionnement",
                            ],
                        },
                        {
                            "period": "PALIER 2 · 30 À 60 JOURS",
                            "theme": "EXPÉRIMENTER & TESTER",
                            "default_obj": "Confronter mon offre ou mes candidatures au terrain avec régularité.",
                            "default_kpi": "3 entretiens d'opportunité ou 2 propositions envoyées.",
                            "actions": [
                                "Diffuser ma proposition ou postuler aux missions cibles",
                                "Participer à 2 événements sectoriels professionnels",
                                "Faire le point d'étape avec mon allié de confiance",
                            ],
                        },
                        {
                            "period": "PALIER 3 · 60 À 90 JOURS",
                            "theme": "CONSOLIDER & ANCRER",
                            "default_obj": "Signer mon premier contrat ou acter la décision d'embauche définitive.",
                            "default_kpi": "Projet sur les rails et rythme de croisière équilibré.",
                            "actions": [
                                "Signer le contrat ou acter le début officiel d'activité",
                                "Célébrer l'accomplissement du parcours",
                                "Poser le bilan des 90 jours et réajuster les objectifs annuels",
                            ],
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Mes Garde-Fous & Mon Cercle d'Alliés",
                part_title="4. PÉRENNISATION",
                params={
                    "intro_text": "Anticiper les zones de turbulences pour rester fermement ancré(e) dans votre cap.",
                    "questions": [
                        {
                            "question": "Quel est votre plus grand risque de rechute (dispersion, doute, surmenage) et quelle parade activez-vous ?",
                            "subtitle": "Un mécanisme préventif simple et observable.",
                            "example": "Si je recommence à travailler le soir, mon alarme sonne à 19h et je coupe mes notifications.",
                            "field_id": "p6_q1_parade",
                        },
                        {
                            "question": "Quelle est la personne ressource (allié, mentor, coach) avec qui vous ferez un point d'étape mensuel ?",
                            "subtitle": "Nommez votre partenaire de redevabilité bienveillant.",
                            "example": "Mon ancien confrère Marc, avec qui j'ai fixé un déjeuner de suivi le premier jeudi de chaque mois.",
                            "field_id": "p6_q2_allie",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Mon Grand Pacte d'Alignement & d'Avenir",
                part_title="5. ENGAGEMENT SOLENNEL",
                params={
                    "lines": [
                        "J'assume mon cap professionnel avec fierté, conviction et humilité.",
                        "Je mesure le succès par la cohérence entre mes actes et mes valeurs fondamentales.",
                        "Je m'engage à célébrer chaque petit pas franchi sur ma feuille de route.",
                        "Je prends la pleine responsabilité de ma liberté et de ma trajectoire.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Bravo pour Votre Parcours !",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Le bilan de compétences s'achève, votre nouvelle aventure commence.",
                        "Faites confiance à votre discernement et à votre élan vital.",
                        "Marge de Manœuvre reste à vos côtés : à vous de tracer la suite !",
                    ],
                },
            ),
        ],
    )


def _build_business_plan_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=99,
        chapter_title="Mon Business Plan : De l'Idée au Projet Viable",
        subtitle="ENTREPRENEURIAT & PROJET VIABLE",
        theme="indigo",
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="MON BUSINESS PLAN",
                part_title="LIVRET PROJET",
                params={
                    "subtitle": "Mon Business Plan · De l'idée au projet viable 💼",
                    "title": "ENTREPRENEURIAT & MODÈLE ÉCONOMIQUE",
                },
            ),
            PageSpec(
                template="summary",
                title="AU PROGRAMME DU BUSINESS PLAN",
                part_title="SOMMAIRE EXÉCUTIF",
                params={
                    "intro_text": "Transformer une intuition entrepreneuriale en un modèle économique rentable et désirable.",
                    "points": [
                        {"label": "01", "desc": "Les 4 Piliers fondateurs : Vision, Cible, Offre & Avantage."},
                        {"label": "02", "desc": "Analyse du Problème Client & Matrice Valeur/Douleur."},
                        {"label": "03", "desc": "Offre Irrésistible, Tarification & Modèle de Revenus."},
                        {"label": "04", "desc": "Validation Terrain & Premières Ventes (Test MVP)."},
                        {"label": "05", "desc": "Feuille de Route Lancement 30 · 60 · 90 Jours."},
                        {"label": "06", "desc": "Pacte de l'Entrepreneur Responsable."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Mindset & Posture Entrepreneuriale",
                part_title="1. DIAGNOSTIC POSTURE",
                params={
                    "emotion_prompt": "À l'idée de vendre mes prestations ou mes produits, je ressens :",
                    "energy_prompt": "Mon niveau de confiance dans la viabilité économique du projet :",
                    "thought_prompt": "Le défi numéro un que je dois résoudre pour décoller commercialement :",
                },
            ),
            PageSpec(
                template="quadrants",
                title="Les 4 Fondations du Modèle Économique",
                part_title="2. MATRICE BUSINESS CORE",
                params={
                    "instruction": "Posez en quelques mots les 4 piliers indispensables à la viabilité de votre entreprise.",
                    "quadrants": [
                        {"title": "1. La Vision & La Promesse", "subtitle": "Le changement concret que vous apportez au monde"},
                        {"title": "2. La Cible Prioritaire (Persona)", "subtitle": "Le client idéal prêt à payer immédiatement"},
                        {"title": "3. L'Offre Signature", "subtitle": "La solution irrésistible qui résout sa douleur"},
                        {"title": "4. L'Avantage Compétitif", "subtitle": "Ce qui vous rend difficilement copiable"},
                    ],
                },
            ),
            PageSpec(
                template="two_columns",
                title="Matrice Problème / Solution : Valeur vs Douleur",
                part_title="3. ADÉQUATION OFFRE / MARCHÉ",
                params={
                    "intro_text": "Un client n'achète jamais une compétence, il achète la fin d'un problème qui lui coûte cher.",
                    "col1_header": "Douleur aiguë du client (Ce qui lui coûte)",
                    "col2_header": "Bénéfice de mon offre (Ce qu'il gagne)",
                    "rows": [
                        {
                            "label": "1. Problème de temps",
                            "left_tooltip": "Ex: Il passe 15h par semaine à bricoler des solutions inefficaces",
                            "right_tooltip": "Ex: Mon offre lui fait gagner 2 journées entières par mois.",
                        },
                        {
                            "label": "2. Problème financier / Risque",
                            "left_tooltip": "Ex: Il perd des clients par manque de clarté dans son positionnement",
                            "right_tooltip": "Ex: Mon accompagnement double son taux de conversion sous 60 jours.",
                        },
                        {
                            "label": "3. Problème émotionnel / Sérénité",
                            "left_tooltip": "Ex: Il vit dans l'angoisse permanente de commettre une erreur fatale",
                            "right_tooltip": "Ex: Un cadre éprouvé et rassurant qui sécurise chaque décision.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="enquete",
                title="Validation Terrain & Premières Ventes",
                part_title="4. INTERVIEWS PROSPECTS",
                params={
                    "intro_text": "Tester l'appétence de vos 5 premiers prospects avant de dépenser 1 € en développement.",
                    "questions": [
                        {
                            "title": "1. Les Objections Spontanées",
                            "subtitle": "Ce qui les retient d'acheter aujourd'hui (prix, timing, confiance, concurrence).",
                        },
                        {
                            "title": "2. La Valeur Perçue du Prix",
                            "subtitle": "À quel montant jugent-ils que la prestation est une excellente affaire ?",
                        },
                        {
                            "title": "3. Le Déclencheur d'Achat Réel",
                            "subtitle": "Quel événement précis dans leur calendrier va les faire signer ?",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Chiffres Clés & Seuil de Rentabilité",
                part_title="5. ÉQUILIBRE FINANCIER DU PROJET",
                params={
                    "intro_text": "Poser l'équation financière élémentaire pour piloter la rentabilité.",
                    "questions": [
                        {
                            "question": "Quel est votre panier moyen par client et le volume de ventes mensuel pour être à l'équilibre ?",
                            "subtitle": "Exemple : 4 clients à 1 500 € / mois ou 30 ventes à 200 €.",
                            "example": "5 clients mensuels à 1 200 € HT pour générer 6 000 € de chiffre d'affaires récurrent.",
                            "field_id": "bp_q1_rentabilite",
                        },
                        {
                            "question": "Quelle est la première action de vente directe programmée cette semaine ?",
                            "subtitle": "Le premier contact concret ou la première proposition commerciale à envoyer.",
                            "example": "Appeler mes 3 anciens collègues devenus directeurs pour leur présenter mon offre test.",
                            "field_id": "bp_q2_premiere_vente",
                        },
                    ],
                },
            ),
            PageSpec(
                template="roadmap",
                title="Lancement du MVP : 30 · 60 · 90 Jours",
                part_title="6. CADENCE DE LANCEMENT",
                params={
                    "intro_text": "Passer de la phase de conception à vos 3 premières factures encaissées.",
                    "stages": [
                        {
                            "period": "MOIS 1 · 0 À 30 JOURS",
                            "theme": "OFFRE & TEST DIRECT",
                            "default_obj": "Packager l'offre test et réaliser 5 entretiens de découverte.",
                            "default_kpi": "Fiche offre 1 page finalisée + 5 prospects qualifiés rencontrés.",
                            "actions": [
                                "Rédiger l'offre sur 1 page (Promesse, Méthode, Tarif)",
                                "Lister mes 20 premiers contacts chauds",
                                "Réaliser mes 5 entretiens de confrontation",
                            ],
                        },
                        {
                            "period": "MOIS 2 · 30 À 60 JOURS",
                            "theme": "PREMIERS CONTRATS",
                            "default_obj": "Signer mes 2 premiers clients bêtatesteurs avec conditions préférentielles.",
                            "default_kpi": "2 acomptes encaissés et missions démarrées.",
                            "actions": [
                                "Envoyer mes propositions commerciales simplifiées",
                                "Sécuriser les formalités de facturation et statuts",
                                "Démarrer la délivrance de la prestation",
                            ],
                        },
                        {
                            "period": "MOIS 3 · 60 À 90 JOURS",
                            "theme": "RÉFÉRENCES & VOLUME",
                            "default_obj": "Recueillir les témoignages de mes clients et lancer la prospection régulière.",
                            "default_kpi": "2 avis clients dithyrambiques et pipeline de 10 nouveaux prospects.",
                            "actions": [
                                "Interviewer mes premiers clients pour obtenir un verbatim fort",
                                "Publier un retour d'expérience sur LinkedIn",
                                "Poser un rituel commercial hebdomadaire inébranlable",
                            ],
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Mon Pacte d'Entrepreneur",
                part_title="7. ENGAGEMENT D'ACTION",
                params={
                    "lines": [
                        "Je m'engage à faire tester mon offre au contact du monde réel plutôt que de peaufiner dans l'ombre.",
                        "Je vends ma valeur avec conviction et je respecte le temps de mes clients comme le mien.",
                        "J'accepte les refus commerciaux comme des données gratuites pour perfectionner mon offre.",
                        "Je construis une entreprise rentable, pérenne et profondément alignée avec mon éthique.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Votre Projet Prend Vie",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Vous tenez entre vos mains les plans solides de votre entreprise.",
                        "Le succès appartient à ceux qui ont le courage de proposer leur valeur au monde.",
                        "Passez à l'action dès aujourd'hui : vos futurs clients ont besoin de votre solution !",
                    ],
                },
            ),
        ],
    )


# Dictionnaire des spécifications de référence
PREDEFINED_WORKBOOKS: Dict[str, WorkbookSpec] = {
    "chap0": _build_chap0_spec(),
    "chap1": _build_chap1_spec(),
    "chap2": _build_chap2_spec(),
    "chap3": _build_chap3_spec(),
    "chap4": _build_chap4_spec(),
    "chap5": _build_chap5_spec(),
    "chap6": _build_chap6_spec(),
    "business_plan": _build_business_plan_spec(),
}

# Résumés pour le sélecteur d'interface utilisateur
PREDEFINED_WORKBOOKS_INFO: List[TemplateInfo] = [
    TemplateInfo(
        id="chap0",
        chapter_num=0,
        title="Chapitre 0 · Le Prélude",
        subtitle="Onboarding, Cadre de Confiance & Alliance",
        description="Accueil solennel, pose du pacte de travail, clarification de l'intention et de l'autorisation personnelle.",
        page_count=7,
        icon="🕯️",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap1",
        chapter_num=1,
        title="Chapitre 1 · L'État des Lieux",
        subtitle="Boussole, Météo & Dépose du Sac à Dos",
        description="Figer le point de départ, cartographie 360° des équilibres de vie et identification de l'objectif boussole.",
        page_count=8,
        icon="🧭",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap2",
        chapter_num=2,
        title="Chapitre 2 · L'Histoire & Les Racines",
        subtitle="Héritage Professionnel, Mentors & Arbre de Vie",
        description="Comprendre le fil rouge du parcours, distinguer modèles reçus et choisis, honorer les mentors inspirants.",
        page_count=8,
        icon="🌳",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap3",
        chapter_num=3,
        title="Chapitre 3 · Compétences & Talents",
        subtitle="Zones d'Excellence, Moteurs & Verbes d'Action",
        description="Matrice des 4 zones de compétences, cartographie des flux d'énergie et identification des verbes d'action clés.",
        page_count=8,
        icon="⭐",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap4",
        chapter_num=4,
        title="Chapitre 4 · Valeurs & Rapport à l'Argent",
        subtitle="Piliers de Vie, Limites Protectrices & Minimum Vital",
        description="Déconstruire les croyances financières limitantes, sanctuariser ses non-négociables et définir son modèle économique personnel.",
        page_count=8,
        icon="⚖️",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap5",
        chapter_num=5,
        title="Chapitre 5 · Exploration Terrain & Marché",
        subtitle="Enquête Métier, Interviews Réseau & Benchmark",
        description="Posture d'enquêteur, grille d'entretien exploratoire en 3 axes, confrontation des idées reçues à la réalité du terrain.",
        page_count=8,
        icon="🔍",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap6",
        chapter_num=6,
        title="Chapitre 6 · Plan d'Action & Cap",
        subtitle="Arbitrage Stratégique, Roadmap 30·60·90j & Clôture",
        description="Choix éclairé de trajectoire (Piste A vs B), feuille de route opérationnelle cadencée et grand pacte d'engagement final.",
        page_count=8,
        icon="🚀",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="business_plan",
        chapter_num=99,
        title="Mon Business Plan · De l'Idée au Projet Viable",
        subtitle="Vision, Cible, Offre, Modèle Éco & MVP 90 Jours",
        description="Le livret complet pour structurer une création d'activité, tester son marché sans gaspillage et décrocher ses premières ventes.",
        page_count=10,
        icon="💼",
        category="Entrepreneuriat",
    ),
]


def get_predefined_spec(template_id: str) -> Optional[WorkbookSpec]:
    """Retourne une copie indépendante de la spécification de référence demandée."""
    spec = PREDEFINED_WORKBOOKS.get(template_id)
    if spec:
        # Retourne une copie profonde via Pydantic pour éviter de muter la référence
        return WorkbookSpec.model_validate(spec.model_dump())
    return None


def get_predefined_info_list() -> List[TemplateInfo]:
    """Retourne la liste des résumés de tous les modèles pré-intégrés."""
    return list(PREDEFINED_WORKBOOKS_INFO)
