"""
Catalogue des livrets pédagogiques de référence (MDM Bilan de Compétences & Business Plan).
Fournit les spécifications canoniques (WorkbookSpec) prêtes à être personnalisées pour chaque bénéficiaire.
Les textes suivent le ton de la DA (DA-workbook.md, section 7) : vouvoiement, phrases courtes,
titres ponctués dont la fin (ou les *mots marqués*) s'affiche en corail.
"""

from typing import Dict, List, Optional
from server.models import WorkbookSpec, PageSpec, BlockSpec, TemplateInfo

BILAN = "BILAN DE COMPÉTENCES"


def _build_chap0_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=0,
        chapter_title="Le prélude.",
        subtitle=BILAN,
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="Le prélude.",
                part_title="ACCUEIL",
                params={
                    "subtitle": "Chapitre 0 : Le prélude",
                    "title": BILAN,
                    "promise": "Du bilan à l'action.",
                },
            ),
            PageSpec(
                template="summary",
                title="Poser le cadre *du bilan.*",
                part_title="0. CADRAGE",
                params={
                    "intro_text": "Ce premier carnet pose le cadre de travail et l'objectif de votre bilan.",
                    "points": [
                        {"label": "01", "desc": "Votre point de départ : où vous en êtes en commençant."},
                        {"label": "02", "desc": "Le cadre de travail : trois règles pour avancer ensemble."},
                        {"label": "03", "desc": "Votre objectif et ce que vous vous autorisez à explorer."},
                        {"label": "04", "desc": "Vos engagements pour la durée du bilan."},
                    ],
                },
            ),
            PageSpec(
                template="composite",
                title="Bienvenue dans *votre bilan.*",
                part_title="1. OUVERTURE",
                blocks=[
                    BlockSpec(
                        type="callout",
                        title="À quoi sert ce carnet",
                        text="Vous avez décidé de faire le point sur votre parcours. Ce carnet garde la trace de votre travail entre les séances : vos réponses, vos constats, vos décisions.",
                        variant="quote",
                    ),
                    BlockSpec(
                        type="scale",
                        label="Votre niveau d'énergie au démarrage :",
                        min_val=0,
                        max_val=10,
                        min_label="0 · Hésitant",
                        max_label="10 · Déterminé",
                    ),
                ],
            ),
            PageSpec(
                template="two_columns",
                title="Le cadre de travail : *trois règles.*",
                part_title="2. CADRE DE TRAVAIL",
                params={
                    "intro_text": "Trois engagements réciproques encadrent nos échanges.",
                    "col1_header": "La règle",
                    "col2_header": "Ce qu'elle signifie concrètement",
                    "rows": [
                        {
                            "label": "1. Confidentialité totale",
                            "left_tooltip": "Ce qui se dit en séance reste en séance",
                            "right_tooltip": "Tout ce que vous écrivez ou dites ici reste strictement entre nous.",
                        },
                        {
                            "label": "2. Franchise",
                            "left_tooltip": "Dire vos vrais doutes",
                            "right_tooltip": "Ce sont vos vraies contraintes qui permettent de construire un projet réaliste.",
                        },
                        {
                            "label": "3. Action",
                            "left_tooltip": "Tester sur le terrain",
                            "right_tooltip": "Une décision se construit en testant, pas seulement en réfléchissant.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Votre objectif *pour ce bilan.*",
                part_title="3. OBJECTIF",
                params={
                    "intro_text": "Avant de commencer, précisez ce que vous attendez du bilan et ce que vous vous autorisez à explorer.",
                    "questions": [
                        {
                            "question": "D'ici 3 à 4 mois, quel résultat ferait de ce bilan une réussite ?",
                            "subtitle": "Formulez un résultat concret, qui changerait votre quotidien professionnel.",
                            "example": "Un projet clair, chiffré, avec un plan d'action pour les six prochains mois.",
                            "field_id": "p0_q1_intention",
                        },
                        {
                            "question": "Qu'est-ce que vous vous autorisez à explorer, que vous écartez d'habitude ?",
                            "subtitle": "Une piste, une question ou une décision que vous mettez de côté par réflexe.",
                            "example": "Étudier une reconversion sans l'écarter d'emblée pour des raisons de salaire.",
                            "field_id": "p0_q2_autorisation",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Votre livrable.",
                part_title="4. FIN DE CARNET",
                params={
                    "livrable_title": "Votre objectif de bilan",
                    "livrable_text": "Le résultat attendu et vos engagements, relus ensemble à la prochaine séance.",
                    "lines": [
                        "Je consacre au moins 2 heures par semaine aux exercices de ce carnet.",
                        "Je considère les moments de doute comme une étape normale du bilan.",
                        "J'étudie chaque piste avant de juger de sa faisabilité.",
                        "Je fais de ce bilan une priorité de mon agenda.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Votre bilan commence.",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Le premier pas est fait.",
                        "Relisez vos réponses avant la prochaine séance.",
                        "Rendez-vous en séance 1 pour l'état des lieux complet.",
                    ],
                },
            ),
        ],
    )


def _build_chap1_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=1,
        chapter_title="L'état des lieux.",
        subtitle=BILAN,
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="L'état des lieux.",
                part_title="CHAPITRE 1",
                params={
                    "subtitle": "Chapitre 1 : L'état des lieux",
                    "title": BILAN,
                    "promise": "Savoir d'où vous partez.",
                },
            ),
            PageSpec(
                template="summary",
                title="Fixer votre point *de départ.*",
                part_title="1. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Fixer le point de départ, pour mesurer le chemin parcouru à la fin du bilan.",
                    "points": [
                        {"label": "01", "desc": "Votre état d'esprit et votre énergie du moment."},
                        {"label": "02", "desc": "Vision à 360° : vos quatre domaines de vie."},
                        {"label": "03", "desc": "Votre objectif boussole : le cap prioritaire à 3 mois."},
                        {"label": "04", "desc": "Le sac à dos : ce que vous décidez de déposer."},
                        {"label": "05", "desc": "Votre livrable et vos engagements pour la suite."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Votre état d'esprit *du moment.*",
                part_title="1. MÉTÉO DU MOMENT",
                params={
                    "emotion_prompt": "Aujourd'hui, je me sens :",
                    "energy_prompt": "Mon niveau d'énergie actuel :",
                    "thought_prompt": "Ce qui prend le plus de place dans ma tête en ce moment :",
                },
            ),
            PageSpec(
                template="quadrants",
                title="Votre vision *à 360°.*",
                part_title="2. ÉQUILIBRE GLOBAL",
                params={
                    "instruction": "Pour chaque domaine, notez en une phrase votre constat actuel et ce que vous visez.",
                    "quadrants": [
                        {"title": "Professionnel", "subtitle": "Missions, salaire, perspectives"},
                        {"title": "Personnel", "subtitle": "Temps pour soi, santé, rythme"},
                        {"title": "Social et familial", "subtitle": "Relations, présence auprès des proches"},
                        {"title": "Cadre et autonomie", "subtitle": "Liberté ou sécurité, règles du jeu"},
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Votre objectif *boussole.*",
                part_title="3. CAP PRIORITAIRE",
                params={
                    "intro_text": "Précisez votre objectif prioritaire pour concentrer vos efforts pendant le bilan.",
                    "questions": [
                        {
                            "question": "D'ici 3 à 6 mois, quelle question professionnelle voulez-vous avoir tranchée ?",
                            "subtitle": "Formulez un objectif clair et vérifiable.",
                            "example": "Avoir identifié 2 pistes professionnelles réalistes et compatibles avec mes contraintes.",
                            "field_id": "p1_q1_boussole",
                        },
                        {
                            "question": "À quoi verrez-vous concrètement que votre bilan est réussi ?",
                            "subtitle": "Un indicateur ou une situation observable dans votre quotidien.",
                            "example": "Une offre signée ou un calendrier précis de lancement.",
                            "field_id": "p1_q2_kpi",
                        },
                    ],
                },
            ),
            PageSpec(
                template="two_columns",
                title="Le sac à dos : *ce que je dépose.*",
                part_title="4. CE QUI PÈSE",
                params={
                    "intro_text": "Repérez les contraintes et les idées toutes faites qui vous freinent, et décidez de ce que vous en faites.",
                    "col1_header": "Ce qui pèse (contrainte, idée reçue)",
                    "col2_header": "Ce que je décide (levier, dépôt)",
                    "rows": [
                        {
                            "label": "1. Exigence ou injonction",
                            "left_tooltip": "Ex : Je dois tout maîtriser avant d'en parler",
                            "right_tooltip": "Ex : Un premier essai imparfait m'apprendra plus que l'attente.",
                        },
                        {
                            "label": "2. Situation subie",
                            "left_tooltip": "Ex : Accepter des urgences au détriment de mes priorités",
                            "right_tooltip": "Ex : Poser des limites explicites dès le début de semaine.",
                        },
                        {
                            "label": "3. Peur dominante",
                            "left_tooltip": "Ex : La peur de ne pas être légitime dans un nouveau secteur",
                            "right_tooltip": "Ex : M'appuyer sur mes compétences transférables et ma capacité d'apprentissage.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Votre livrable.",
                part_title="5. FIN DE CARNET",
                params={
                    "livrable_title": "Votre état des lieux",
                    "livrable_text": "Vos quatre domaines de vie et votre objectif boussole, validés en séance.",
                    "lines": [
                        "Je réserve chaque semaine un créneau fixe à ce carnet.",
                        "Je regarde mes freins avec lucidité, sans me juger.",
                        "Je teste au moins une action concrète entre deux séances.",
                        "Je garde mon objectif boussole sous les yeux.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Point de départ validé.",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Votre point de départ est posé.",
                        "Relisez vos réponses avant la prochaine séance.",
                        "Prochaine étape : votre parcours et vos expériences.",
                    ],
                },
            ),
        ],
    )


def _build_chap2_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=2,
        chapter_title="Mon parcours.",
        subtitle=BILAN,
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="Mon parcours.",
                part_title="CHAPITRE 2",
                params={
                    "subtitle": "Chapitre 2 : Mon parcours",
                    "title": BILAN,
                    "promise": "Comprendre vos choix passés pour mieux décider.",
                },
            ),
            PageSpec(
                template="summary",
                title="Relire *votre parcours.*",
                part_title="2. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Repérer le fil rouge de votre parcours pour comprendre la logique de vos choix passés.",
                    "points": [
                        {"label": "01", "desc": "Votre état d'esprit en ouvrant ce carnet."},
                        {"label": "02", "desc": "L'héritage professionnel : ce que vous avez reçu, ce que vous choisissez."},
                        {"label": "03", "desc": "Les personnes dont le parcours vous inspire."},
                        {"label": "04", "desc": "L'arbre de vie : vos acquis et vos compétences transférables."},
                        {"label": "05", "desc": "Votre livrable et vos engagements."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Votre état *d'esprit.*",
                part_title="1. MÉTÉO DU MOMENT",
                params={
                    "emotion_prompt": "En repensant à mon parcours, je me sens :",
                    "energy_prompt": "Mon niveau d'énergie pour revenir sur mon parcours :",
                    "thought_prompt": "Le souvenir professionnel qui me revient en premier :",
                },
            ),
            PageSpec(
                template="two_columns",
                title="Ce que j'ai reçu, *ce que je choisis.*",
                part_title="2. HÉRITAGE PROFESSIONNEL",
                params={
                    "intro_text": "Distinguez les modèles transmis par votre milieu de ce que vous voulez vraiment pour la suite.",
                    "col1_header": "Ce que j'ai reçu (modèle, injonction)",
                    "col2_header": "Ce que je choisis aujourd'hui",
                    "rows": [
                        {
                            "label": "1. Définition de la réussite",
                            "left_tooltip": "Ex : La sécurité du statut et la progression hiérarchique",
                            "right_tooltip": "Ex : L'autonomie, l'utilité et la liberté d'organisation.",
                        },
                        {
                            "label": "2. Rapport au travail",
                            "left_tooltip": "Ex : Il faut souffrir pour mériter son salaire",
                            "right_tooltip": "Ex : L'intérêt pour le travail et l'effort peuvent aller ensemble.",
                        },
                        {
                            "label": "3. Rapport à l'échec",
                            "left_tooltip": "Ex : Changer de voie est un aveu d'échec",
                            "right_tooltip": "Ex : Changer de voie est une décision réfléchie.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Les parcours *qui vous inspirent.*",
                part_title="3. MODÈLES",
                params={
                    "intro_text": "Les parcours que vous admirez disent beaucoup de ce que vous cherchez.",
                    "questions": [
                        {
                            "question": "Quelles sont les 2 personnes (réelles ou de fiction) dont le parcours vous inspire le plus ?",
                            "subtitle": "Dites en une phrase ce qui vous parle chez chacune d'elles.",
                            "example": "Une ancienne manager qui savait trancher et un entrepreneur de la rénovation énergétique.",
                            "field_id": "p2_q1_mentors",
                        },
                        {
                            "question": "Quelle qualité admirez-vous chez elles et voulez-vous développer ?",
                            "subtitle": "Elle existe sans doute déjà chez vous, à un autre degré.",
                            "example": "Dire clairement ce qui ne va pas, même quand c'est difficile.",
                            "field_id": "p2_q2_qualite",
                        },
                    ],
                },
            ),
            PageSpec(
                template="quadrants",
                title="Votre arbre *de vie professionnel.*",
                part_title="4. CARTE DES ACQUIS",
                params={
                    "instruction": "Résumez vos acquis d'hier et vos ressources pour demain en quatre étages.",
                    "quadrants": [
                        {"title": "Racines et fondations", "subtitle": "Diplômes, valeurs familiales, premières réussites"},
                        {"title": "Tronc et savoirs solides", "subtitle": "Compétences techniques et managériales éprouvées"},
                        {"title": "Branches et projets marquants", "subtitle": "Réalisations dont vous êtes fier ou fière"},
                        {"title": "Fruits et pistes futures", "subtitle": "Compétences transférables vers votre futur métier"},
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Votre livrable.",
                part_title="5. FIN DE CARNET",
                params={
                    "livrable_title": "Votre fil rouge professionnel",
                    "livrable_text": "Votre héritage, vos modèles et votre arbre de vie, relus ensemble en séance.",
                    "lines": [
                        "Je reconnais la valeur de chacune de mes expériences, y compris les plus difficiles.",
                        "Je regarde mes détours comme des acquis, pas comme des erreurs.",
                        "Je décide de mes prochains choix professionnels en connaissance de cause.",
                        "Je m'appuie sur mes acquis pour construire la suite.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Votre parcours est relu.",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Vous savez sur quels acquis vous appuyer.",
                        "Relisez vos réponses avant la prochaine séance.",
                        "Prochaine étape : vos compétences et ce qui vous donne de l'énergie.",
                    ],
                },
            ),
        ],
    )


def _build_chap3_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=3,
        chapter_title="Compétences et moteurs.",
        subtitle=BILAN,
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="Compétences et moteurs.",
                part_title="CHAPITRE 3",
                params={
                    "subtitle": "Chapitre 3 : Compétences et moteurs",
                    "title": BILAN,
                    "promise": "Ce que vous faites bien, et ce qui vous donne de l'énergie.",
                },
            ),
            PageSpec(
                template="summary",
                title="Vos compétences, *vos moteurs.*",
                part_title="3. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Séparer ce que vous savez faire par obligation de ce qui vous donne vraiment de l'énergie.",
                    "points": [
                        {"label": "01", "desc": "Votre énergie au travail aujourd'hui."},
                        {"label": "02", "desc": "Ce qui vous donne de l'énergie, ce qui vous en prend."},
                        {"label": "03", "desc": "Les quatre zones de compétences, dont votre zone d'excellence."},
                        {"label": "04", "desc": "Vos trois verbes d'action."},
                        {"label": "05", "desc": "Votre livrable et vos engagements."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Votre énergie *au travail.*",
                part_title="1. ÉNERGIE AU TRAVAIL",
                params={
                    "emotion_prompt": "Dans mon travail actuel, je me sens le plus souvent :",
                    "energy_prompt": "Mon niveau d'énergie à la fin d'une journée type :",
                    "thought_prompt": "L'activité de ma semaine qui m'a le plus intéressé :",
                },
            ),
            PageSpec(
                template="two_columns",
                title="Ce qui vous donne de l'énergie, *ce qui vous en prend.*",
                part_title="2. SOURCES D'ÉNERGIE",
                params={
                    "intro_text": "Repérez avec précision les tâches et les contextes qui vous rechargent ou vous épuisent.",
                    "col1_header": "Ce qui m'épuise",
                    "col2_header": "Ce qui me donne de l'énergie",
                    "rows": [
                        {
                            "label": "1. Type de tâche",
                            "left_tooltip": "Ex : Remplir des tableaux de suivi et justifier les budgets en réunion",
                            "right_tooltip": "Ex : Résoudre un problème complexe avec une équipe motivée.",
                        },
                        {
                            "label": "2. Mode relationnel",
                            "left_tooltip": "Ex : Gérer des conflits de personnes sans cap clair",
                            "right_tooltip": "Ex : Transmettre une méthode et voir progresser un collaborateur.",
                        },
                        {
                            "label": "3. Rythme",
                            "left_tooltip": "Ex : L'urgence permanente et les tâches morcelées",
                            "right_tooltip": "Ex : De longues plages de travail sur un sujet qui m'intéresse.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="quadrants",
                title="Vos quatre zones *de compétences.*",
                part_title="3. ZONE D'EXCELLENCE",
                params={
                    "instruction": "Répartissez vos activités principales dans les quatre zones, pour viser votre zone d'excellence.",
                    "quadrants": [
                        {"title": "Zone d'excellence", "subtitle": "Facile pour moi, et cela me donne de l'énergie"},
                        {"title": "Zone de compétence", "subtitle": "Je sais très bien faire, mais cela me laisse neutre"},
                        {"title": "Zone d'apprentissage", "subtitle": "Je ne maîtrise pas encore, mais cela me stimule"},
                        {"title": "Zone à risque", "subtitle": "Je sais faire, mais cela m'épuise"},
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Vos verbes *d'action.*",
                part_title="4. VERBES D'ACTION",
                params={
                    "intro_text": "Les métiers changent, vos verbes d'action restent.",
                    "questions": [
                        {
                            "question": "Quels sont les 3 verbes d'action qui décrivent le mieux ce que vous aimez faire ?",
                            "subtitle": "Exemples : fédérer, analyser, concevoir, simplifier, transmettre, construire…",
                            "example": "Structurer des idées complexes, négocier des accords, animer une équipe.",
                            "field_id": "p3_q1_verbes",
                        },
                        {
                            "question": "Dans quel cadre ou quel secteur voulez-vous exercer ces verbes demain ?",
                            "subtitle": "Décrivez une mission ou un environnement de travail précis.",
                            "example": "Une organisation où les décisions sont rapides et l'impact mesuré.",
                            "field_id": "p3_q2_cadre",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Votre livrable.",
                part_title="5. FIN DE CARNET",
                params={
                    "livrable_title": "Votre carte de compétences",
                    "livrable_text": "Vos quatre zones, vos sources d'énergie et vos verbes d'action, validés en séance.",
                    "lines": [
                        "Je reconnais mes points forts sans les minimiser.",
                        "Je réduis le temps passé sur les activités qui m'épuisent.",
                        "Je fais de ma zone d'excellence mon premier argument professionnel.",
                        "Je m'appuie sur mes compétences transférables pour étudier de nouvelles pistes.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Vos compétences sont cartographiées.",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Vous savez ce qui vous distingue.",
                        "Gardez vos verbes d'action sous les yeux.",
                        "Prochaine étape : vos valeurs et votre équilibre financier.",
                    ],
                },
            ),
        ],
    )


def _build_chap4_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=4,
        chapter_title="Valeurs, limites et argent.",
        subtitle=BILAN,
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="Valeurs, limites et argent.",
                part_title="CHAPITRE 4",
                params={
                    "subtitle": "Chapitre 4 : Valeurs, limites et argent",
                    "title": BILAN,
                    "promise": "Un salaire et un rythme de vie sécurisés.",
                },
            ),
            PageSpec(
                template="summary",
                title="Vos limites *et vos chiffres.*",
                part_title="4. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Définir vos non-négociables et vos seuils financiers, pour un projet tenable dans la durée.",
                    "points": [
                        {"label": "01", "desc": "Votre état d'esprit face à l'argent et à la charge de travail."},
                        {"label": "02", "desc": "Vos quatre domaines de vie et les limites à poser."},
                        {"label": "03", "desc": "Vos idées reçues sur l'argent, à l'épreuve des faits."},
                        {"label": "04", "desc": "Votre minimum vital et votre revenu cible."},
                        {"label": "05", "desc": "Votre livrable et vos engagements."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Votre état *d'esprit.*",
                part_title="1. POINT DE DÉPART",
                params={
                    "emotion_prompt": "Face à mes choix de carrière et de rémunération, je ressens :",
                    "energy_prompt": "Mon niveau de tranquillité financière actuel :",
                    "thought_prompt": "La limite que je laisse trop souvent franchir dans mon quotidien :",
                },
            ),
            PageSpec(
                template="quadrants",
                title="Vos limites, *domaine par domaine.*",
                part_title="2. LIMITES",
                params={
                    "instruction": "Pour chaque domaine, notez la règle que vous décidez de ne plus négocier.",
                    "quadrants": [
                        {"title": "Professionnel", "subtitle": "Respect, éthique, charge de travail"},
                        {"title": "Personnel et santé", "subtitle": "Sommeil, sport, déconnexion le soir"},
                        {"title": "Relations et proches", "subtitle": "Temps de qualité, temps partagé sans écran"},
                        {"title": "Économique", "subtitle": "Rémunération juste, épargne de sécurité"},
                    ],
                },
            ),
            PageSpec(
                template="two_columns",
                title="Vos idées sur l'argent, *à l'épreuve des faits.*",
                part_title="3. RAPPORT À L'ARGENT",
                params={
                    "intro_text": "Remplacez chaque peur liée à l'argent par un principe concret, vérifiable sur le terrain.",
                    "col1_header": "Ce que je me dis (idée reçue, peur)",
                    "col2_header": "Ce que montrent les faits (principe de réalité)",
                    "rows": [
                        {
                            "label": "1. Légitimité et tarification",
                            "left_tooltip": "Ex : Si je demande un bon tarif, je vais perdre les opportunités",
                            "right_tooltip": "Ex : Un tarif juste garantit mon engagement et écarte les projets mal cadrés.",
                        },
                        {
                            "label": "2. Sécurité du salariat",
                            "left_tooltip": "Ex : Seul un CDI me protège des aléas",
                            "right_tooltip": "Ex : Ma sécurité tient aussi à mon réseau et à mes compétences à jour.",
                        },
                        {
                            "label": "3. Éthique et rémunération",
                            "left_tooltip": "Ex : Bien gagner sa vie n'est pas compatible avec un métier utile",
                            "right_tooltip": "Ex : Un revenu solide me donne plus de choix dans mes projets.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Vos seuils *en chiffres.*",
                part_title="4. CHIFFRES",
                params={
                    "intro_text": "Sortez du flou financier : posez vos seuils en chiffres.",
                    "questions": [
                        {
                            "question": "Quel est votre revenu mensuel net minimum, sous lequel vous ne descendez pas ?",
                            "subtitle": "Ce qu'il vous faut pour couvrir vos charges sans difficulté.",
                            "example": "2 800 € net par mois au minimum, 4 200 € en revenu cible.",
                            "field_id": "p4_q1_plancher",
                        },
                        {
                            "question": "Quelle limite posez-vous désormais face aux demandes urgentes ou non rémunérées ?",
                            "subtitle": "Une règle simple, pour protéger votre temps de travail de fond.",
                            "example": "Pas de réunion avant 10 h et aucun devis sans entretien de cadrage préalable.",
                            "field_id": "p4_q2_limite",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Votre livrable.",
                part_title="5. FIN DE CARNET",
                params={
                    "livrable_title": "Vos seuils et vos limites",
                    "livrable_text": "Votre minimum vital, votre revenu cible et vos règles non négociables, validés en séance.",
                    "lines": [
                        "J'assume la valeur économique de mon travail et de mon temps.",
                        "Je tiens mes limites personnelles avec la même fermeté que mes contrats.",
                        "Je traite l'argent comme un outil au service de mon projet.",
                        "Je vise une rémunération confortable, sans m'en excuser.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Vos limites sont posées.",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Vos chiffres sont posés.",
                        "Relisez vos réponses avant la prochaine séance.",
                        "Prochaine étape : confronter vos pistes au marché.",
                    ],
                },
            ),
        ],
    )


def _build_chap5_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=5,
        chapter_title="L'exploration du terrain.",
        subtitle=BILAN,
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="L'exploration du terrain.",
                part_title="CHAPITRE 5",
                params={
                    "subtitle": "Chapitre 5 : L'exploration du terrain",
                    "title": BILAN,
                    "promise": "Confronter vos pistes au marché réel.",
                },
            ),
            PageSpec(
                template="summary",
                title="Aller voir *le terrain.*",
                part_title="5. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Confronter vos idées à la réalité des professionnels du secteur.",
                    "points": [
                        {"label": "01", "desc": "Votre état d'esprit avant d'aller sur le terrain."},
                        {"label": "02", "desc": "La grille d'entretien métier et réseau."},
                        {"label": "03", "desc": "Idées reçues et réalité du terrain."},
                        {"label": "04", "desc": "Trois contacts à solliciter et votre message d'approche."},
                        {"label": "05", "desc": "Votre livrable et vos engagements."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Avant d'aller *sur le terrain.*",
                part_title="1. POINT DE DÉPART",
                params={
                    "emotion_prompt": "À l'idée de solliciter des professionnels que je ne connais pas, je me sens :",
                    "energy_prompt": "Mon niveau d'aisance pour solliciter mon réseau :",
                    "thought_prompt": "Le doute principal qui pourrait me faire repousser ces démarches :",
                },
            ),
            PageSpec(
                template="enquete",
                title="Votre grille *d'entretien.*",
                part_title="2. ENTRETIENS MÉTIER",
                params={
                    "intro_text": "Pendant vos entretiens de 20 minutes, abordez ces trois sujets.",
                    "questions": [
                        {
                            "title": "1. Le quotidien réel et les pièges du métier",
                            "subtitle": "Ce que les fiches de poste ne disent pas (pressions, horaires, frictions).",
                        },
                        {
                            "title": "2. Les tendances et les besoins non couverts",
                            "subtitle": "Ce qui manque sur le marché, et où sont les budgets.",
                        },
                        {
                            "title": "3. Les conseils pour réussir son entrée",
                            "subtitle": "Les compétences à mettre en avant et les erreurs à éviter.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="two_columns",
                title="Idées reçues, *réalité du terrain.*",
                part_title="3. TEST DE RÉALITÉ",
                params={
                    "intro_text": "Comparez ce que vous imaginiez avec ce que vous ont dit les professionnels rencontrés.",
                    "col1_header": "Ce que j'imaginais (espoir, crainte)",
                    "col2_header": "Ce que le terrain montre",
                    "rows": [
                        {
                            "label": "1. Accès au secteur",
                            "left_tooltip": "Ex : Il faut un master ou dix ans de réseau local",
                            "right_tooltip": "Ex : Une double compétence et une démarche active ouvrent des portes.",
                        },
                        {
                            "label": "2. Charge de travail",
                            "left_tooltip": "Ex : Tous les professionnels du domaine travaillent 60 h par semaine",
                            "right_tooltip": "Ex : Ceux qui posent un cadre clair préservent leurs week-ends.",
                        },
                        {
                            "label": "3. Modèle de revenus",
                            "left_tooltip": "Ex : Les débuts sont forcément précaires pendant deux ans",
                            "right_tooltip": "Ex : Avec une offre ciblée, les premières missions arrivent plus vite.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Trois contacts, *un message.*",
                part_title="4. PLAN DE CONTACT",
                params={
                    "intro_text": "Passez de l'intention à la prise de rendez-vous.",
                    "questions": [
                        {
                            "question": "Quelles sont les 3 personnes ou profils que vous allez solliciter dans les 10 prochains jours ?",
                            "subtitle": "Indiquez le nom, la fonction ou la structure.",
                            "example": "Un consultant RSE indépendant, la directrice d'une coopérative locale et un ancien camarade de promotion.",
                            "field_id": "p5_q1_cibles",
                        },
                        {
                            "question": "Quelle phrase d'approche allez-vous utiliser pour demander 20 minutes ?",
                            "subtitle": "Vous ne demandez pas un poste : vous demandez un avis de professionnel.",
                            "example": "« Je prépare une évolution vers l'éco-conception, et votre expérience m'intéresse… »",
                            "field_id": "p5_q2_accroche",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Votre livrable.",
                part_title="5. FIN DE CARNET",
                params={
                    "livrable_title": "Vos comptes rendus d'entretien",
                    "livrable_text": "Ce que le terrain confirme ou contredit, analysé ensemble en séance.",
                    "lines": [
                        "J'aborde mes entretiens avec curiosité, sans chercher à vendre.",
                        "J'accepte que certaines personnes ne répondent pas, sans le prendre personnellement.",
                        "Je mène au moins 3 entretiens avant d'arrêter mon choix.",
                        "Je note chaque information utile dans ce carnet.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Le terrain vous attend.",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Chaque entretien confirmera ou ajustera votre projet.",
                        "Notez vos retours avant la prochaine séance.",
                        "Prochaine étape : arbitrer et bâtir votre feuille de route à 30, 60 et 90 jours.",
                    ],
                },
            ),
        ],
    )


def _build_chap6_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=6,
        chapter_title="Le plan d'action.",
        subtitle=BILAN,
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="Le plan d'action.",
                part_title="CHAPITRE 6",
                params={
                    "subtitle": "Chapitre 6 : Le plan d'action",
                    "title": BILAN,
                    "promise": "Une décision éclairée et un plan d'action concret.",
                },
            ),
            PageSpec(
                template="summary",
                title="De la décision *à l'action.*",
                part_title="6. RÉCAPITULATIF DE LA SÉANCE",
                params={
                    "intro_text": "Transformer tout ce que vous avez appris pendant le bilan en un plan d'action daté.",
                    "points": [
                        {"label": "01", "desc": "Votre état d'esprit en fin de bilan."},
                        {"label": "02", "desc": "L'arbitrage entre la piste A et la piste B."},
                        {"label": "03", "desc": "Votre feuille de route à 30, 60 et 90 jours."},
                        {"label": "04", "desc": "Vos garde-fous et vos alliés."},
                        {"label": "05", "desc": "Votre livrable et vos engagements."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Votre état d'esprit *en fin de bilan.*",
                part_title="1. POINT DE DÉPART",
                params={
                    "emotion_prompt": "Au moment de passer à l'action, je ressens :",
                    "energy_prompt": "Mon niveau de confiance dans mon projet :",
                    "thought_prompt": "Ce qui a le plus changé depuis le début du bilan :",
                },
            ),
            PageSpec(
                template="two_columns",
                title="Piste A, piste B : *votre arbitrage.*",
                part_title="2. ARBITRAGE",
                params={
                    "intro_text": "Mettez face à face votre projet d'élan (piste A) et votre solution refuge et tremplin (piste B).",
                    "col1_header": "Piste A : projet d'élan",
                    "col2_header": "Piste B : refuge et tremplin",
                    "rows": [
                        {
                            "label": "1. Intitulé et nature du projet",
                            "left_tooltip": "Ex : Lancer mon activité de conseil indépendant",
                            "right_tooltip": "Ex : Prendre un poste de direction RSE dans une PME.",
                        },
                        {
                            "label": "2. Atouts et motivation",
                            "left_tooltip": "Ex : Liberté de décision et cohérence avec mes valeurs",
                            "right_tooltip": "Ex : Salaire garanti tout de suite et réseau solide.",
                        },
                        {
                            "label": "3. Risques et points de vigilance",
                            "left_tooltip": "Ex : Pression commerciale des débuts et travail en solitaire",
                            "right_tooltip": "Ex : Risque de retrouver une organisation très hiérarchique.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="roadmap",
                title="Feuille de route *à 30, 60 et 90 jours.*",
                part_title="3. FEUILLE DE ROUTE",
                params={
                    "intro_text": "Découpez votre passage à l'action en trois paliers, avec un objectif, un résultat observable et des actions datées.",
                    "stages": [
                        {
                            "period": "PALIER 1 · 0 À 30 JOURS",
                            "theme": "SÉCURISER ET STRUCTURER",
                            "default_obj": "Valider le cadre financier et mettre à jour mes supports de présentation.",
                            "default_kpi": "Budget prévisionnel prêt et profil LinkedIn à jour.",
                            "actions": [
                                "Finaliser les rendez-vous administratifs et financiers",
                                "Réserver 3 créneaux de travail fixes par semaine",
                                "Informer 10 contacts proches de mon nouveau projet",
                            ],
                        },
                        {
                            "period": "PALIER 2 · 30 À 60 JOURS",
                            "theme": "TESTER SUR LE TERRAIN",
                            "default_obj": "Confronter mon offre ou mes candidatures au terrain, chaque semaine.",
                            "default_kpi": "3 entretiens obtenus ou 2 propositions envoyées.",
                            "actions": [
                                "Diffuser ma proposition ou postuler aux missions visées",
                                "Participer à 2 événements professionnels du secteur",
                                "Faire un point d'étape avec une personne de confiance",
                            ],
                        },
                        {
                            "period": "PALIER 3 · 60 À 90 JOURS",
                            "theme": "CONCLURE ET CONSOLIDER",
                            "default_obj": "Signer mon premier contrat ou acter la décision d'embauche.",
                            "default_kpi": "Projet lancé et rythme de travail tenable.",
                            "actions": [
                                "Signer le contrat ou acter le début d'activité",
                                "Faire le point sur ce qui a marché et ce qui a coincé",
                                "Faire le bilan des 90 jours et ajuster les objectifs de l'année",
                            ],
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Vos garde-fous *et vos alliés.*",
                part_title="4. DANS LA DURÉE",
                params={
                    "intro_text": "Anticipez les moments difficiles pour garder votre cap.",
                    "questions": [
                        {
                            "question": "Quel est votre principal risque de décrochage (dispersion, doute, surmenage) et quelle parade prévoyez-vous ?",
                            "subtitle": "Une règle simple et vérifiable.",
                            "example": "Si je recommence à travailler le soir, je coupe mes notifications à 19 h.",
                            "field_id": "p6_q1_parade",
                        },
                        {
                            "question": "Avec quelle personne (allié, mentor, pair) ferez-vous un point d'étape chaque mois ?",
                            "subtitle": "Nommez la personne et fixez la date du premier point.",
                            "example": "Marc, un ancien collègue : déjeuner de suivi le premier jeudi de chaque mois.",
                            "field_id": "p6_q2_allie",
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Votre livrable.",
                part_title="5. FIN DE CARNET",
                params={
                    "livrable_title": "Votre plan d'action",
                    "livrable_text": "La piste retenue et la feuille de route à 90 jours, validées en séance.",
                    "lines": [
                        "J'assume mon projet professionnel et je le présente clairement.",
                        "Je vérifie que mes actes restent cohérents avec mes priorités.",
                        "Je fais le point sur ma feuille de route chaque fin de mois.",
                        "Je décide moi-même de la suite de ma trajectoire.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Votre plan est prêt.",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Le bilan s'achève, votre projet commence.",
                        "Votre feuille de route est votre outil de pilotage.",
                        "Marge de Manœuvre reste joignable pour le suivi à 6 mois.",
                    ],
                },
            ),
        ],
    )


def _build_business_plan_spec() -> WorkbookSpec:
    return WorkbookSpec(
        chapter_num=99,
        chapter_title="Mon business plan.",
        subtitle="ENTREPRENEURIAT & PROJET VIABLE",
        beneficiary_name=None,
        pages=[
            PageSpec(
                template="cover",
                title="Mon business plan.",
                part_title="LIVRET PROJET",
                params={
                    "subtitle": "Mon business plan",
                    "title": "ENTREPRENEURIAT & MODÈLE ÉCONOMIQUE",
                    "promise": "De l'idée au projet viable.",
                },
            ),
            PageSpec(
                template="summary",
                title="De l'idée *au projet viable.*",
                part_title="SOMMAIRE",
                params={
                    "intro_text": "Transformer une idée d'entreprise en un modèle économique rentable.",
                    "points": [
                        {"label": "01", "desc": "Les quatre fondations : vision, cible, offre et avantage."},
                        {"label": "02", "desc": "Le problème du client et ce que votre offre lui apporte."},
                        {"label": "03", "desc": "Les entretiens prospects et les premières ventes."},
                        {"label": "04", "desc": "Vos chiffres clés et votre seuil de rentabilité."},
                        {"label": "05", "desc": "Votre feuille de route de lancement à 90 jours."},
                        {"label": "06", "desc": "Votre livrable et vos engagements."},
                    ],
                },
            ),
            PageSpec(
                template="meteo",
                title="Votre posture *d'entrepreneur.*",
                part_title="1. POINT DE DÉPART",
                params={
                    "emotion_prompt": "À l'idée de vendre mes prestations ou mes produits, je ressens :",
                    "energy_prompt": "Mon niveau de confiance dans la viabilité économique du projet :",
                    "thought_prompt": "Le premier obstacle à lever pour démarrer commercialement :",
                },
            ),
            PageSpec(
                template="quadrants",
                title="Les quatre fondations *de votre modèle.*",
                part_title="2. FONDATIONS",
                params={
                    "instruction": "Posez en quelques mots les quatre piliers indispensables à la viabilité de votre entreprise.",
                    "quadrants": [
                        {"title": "1. La vision et la promesse", "subtitle": "Le changement concret que vous apportez à vos clients"},
                        {"title": "2. La cible prioritaire", "subtitle": "Le client prêt à payer tout de suite"},
                        {"title": "3. L'offre principale", "subtitle": "La solution qui règle son problème"},
                        {"title": "4. L'avantage concurrentiel", "subtitle": "Ce qui vous rend difficile à copier"},
                    ],
                },
            ),
            PageSpec(
                template="two_columns",
                title="Le problème du client, *votre réponse.*",
                part_title="3. OFFRE ET MARCHÉ",
                params={
                    "intro_text": "Un client n'achète pas une compétence : il achète la fin d'un problème qui lui coûte.",
                    "col1_header": "Le problème du client (ce qu'il lui coûte)",
                    "col2_header": "Le bénéfice de mon offre (ce qu'il gagne)",
                    "rows": [
                        {
                            "label": "1. Problème de temps",
                            "left_tooltip": "Ex : Il passe 15 h par semaine sur des solutions de fortune",
                            "right_tooltip": "Ex : Mon offre lui fait gagner deux journées par mois.",
                        },
                        {
                            "label": "2. Problème financier ou risque",
                            "left_tooltip": "Ex : Il perd des clients faute d'un positionnement clair",
                            "right_tooltip": "Ex : Un positionnement clarifié et une offre lisible pour ses clients.",
                        },
                        {
                            "label": "3. Inquiétude",
                            "left_tooltip": "Ex : Il craint en permanence de commettre une erreur coûteuse",
                            "right_tooltip": "Ex : Une méthode éprouvée qui sécurise chaque décision.",
                        },
                    ],
                },
            ),
            PageSpec(
                template="enquete",
                title="Entretiens prospects *et premières ventes.*",
                part_title="4. ENTRETIENS PROSPECTS",
                params={
                    "intro_text": "Testez l'intérêt de vos 5 premiers prospects avant de dépenser un euro en développement.",
                    "questions": [
                        {
                            "title": "1. Les objections spontanées",
                            "subtitle": "Ce qui les retient d'acheter aujourd'hui (prix, moment, confiance, concurrence).",
                        },
                        {
                            "title": "2. Le prix perçu",
                            "subtitle": "À quel montant jugent-ils que la prestation est une bonne affaire ?",
                        },
                        {
                            "title": "3. Le déclencheur d'achat",
                            "subtitle": "Quel événement précis de leur calendrier va les faire signer ?",
                        },
                    ],
                },
            ),
            PageSpec(
                template="questions",
                title="Chiffres clés *et seuil de rentabilité.*",
                part_title="5. ÉQUILIBRE FINANCIER",
                params={
                    "intro_text": "Posez l'équation financière de base pour piloter la rentabilité.",
                    "questions": [
                        {
                            "question": "Quel est votre panier moyen par client, et combien de ventes par mois vous faut-il pour être à l'équilibre ?",
                            "subtitle": "Exemple : 4 clients à 1 500 € par mois, ou 30 ventes à 200 €.",
                            "example": "5 clients par mois à 1 200 € HT, soit 6 000 € de chiffre d'affaires récurrent.",
                            "field_id": "bp_q1_rentabilite",
                        },
                        {
                            "question": "Quelle est la première action de vente prévue cette semaine ?",
                            "subtitle": "Le premier contact ou la première proposition commerciale à envoyer.",
                            "example": "Appeler 3 anciens collègues devenus directeurs pour leur présenter mon offre test.",
                            "field_id": "bp_q2_premiere_vente",
                        },
                    ],
                },
            ),
            PageSpec(
                template="roadmap",
                title="Lancement *à 30, 60 et 90 jours.*",
                part_title="6. LANCEMENT",
                params={
                    "intro_text": "Passer de la conception à vos trois premières factures encaissées.",
                    "stages": [
                        {
                            "period": "MOIS 1 · 0 À 30 JOURS",
                            "theme": "OFFRE ET TEST",
                            "default_obj": "Formaliser l'offre test et mener 5 entretiens de découverte.",
                            "default_kpi": "Offre rédigée sur une page et 5 prospects rencontrés.",
                            "actions": [
                                "Rédiger l'offre sur une page (promesse, méthode, tarif)",
                                "Lister mes 20 premiers contacts",
                                "Mener mes 5 entretiens de découverte",
                            ],
                        },
                        {
                            "period": "MOIS 2 · 30 À 60 JOURS",
                            "theme": "PREMIERS CONTRATS",
                            "default_obj": "Signer 2 premiers clients tests à des conditions préférentielles.",
                            "default_kpi": "2 acomptes encaissés et missions démarrées.",
                            "actions": [
                                "Envoyer mes propositions commerciales",
                                "Régler les formalités de statut et de facturation",
                                "Démarrer la première prestation",
                            ],
                        },
                        {
                            "period": "MOIS 3 · 60 À 90 JOURS",
                            "theme": "RÉFÉRENCES ET VOLUME",
                            "default_obj": "Recueillir l'avis de mes premiers clients et prospecter chaque semaine.",
                            "default_kpi": "2 avis clients obtenus et 10 nouveaux prospects identifiés.",
                            "actions": [
                                "Demander à mes premiers clients un retour écrit",
                                "Publier un retour d'expérience sur LinkedIn",
                                "Fixer un créneau de prospection chaque semaine",
                            ],
                        },
                    ],
                },
            ),
            PageSpec(
                template="engagement",
                title="Votre livrable.",
                part_title="7. FIN DE CARNET",
                params={
                    "livrable_title": "Votre business plan",
                    "livrable_text": "Votre modèle économique et votre plan de lancement à 90 jours, validés en séance.",
                    "lines": [
                        "Je teste mon offre auprès de vrais clients plutôt que de la peaufiner seul.",
                        "Je présente ma valeur avec conviction et je respecte le temps de mes clients.",
                        "Je traite chaque refus commercial comme une information pour améliorer mon offre.",
                        "Je construis une entreprise rentable et cohérente avec mes principes.",
                    ],
                },
            ),
            PageSpec(
                template="closing",
                title="Votre projet prend forme.",
                part_title="CLÔTURE",
                params={
                    "messages": [
                        "Les bases de votre entreprise sont posées.",
                        "Votre plan de lancement est votre outil de pilotage.",
                        "Première action : contacter vos premiers prospects cette semaine.",
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
        title="Chapitre 0 · Le prélude",
        subtitle="Cadre de travail, objectif et engagements",
        description="Poser le cadre de travail, préciser l'objectif du bilan et ce que le bénéficiaire s'autorise à explorer.",
        page_count=7,
        icon="flag",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap1",
        chapter_num=1,
        title="Chapitre 1 · L'état des lieux",
        subtitle="Météo, vision à 360° et objectif boussole",
        description="Fixer le point de départ : les quatre domaines de vie, l'objectif boussole et ce qui pèse.",
        page_count=8,
        icon="explore",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap2",
        chapter_num=2,
        title="Chapitre 2 · Mon parcours",
        subtitle="Héritage professionnel, modèles et arbre de vie",
        description="Repérer le fil rouge du parcours, distinguer les modèles reçus des choix personnels, cartographier les acquis.",
        page_count=8,
        icon="park",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap3",
        chapter_num=3,
        title="Chapitre 3 · Compétences et moteurs",
        subtitle="Zones de compétences, énergie et verbes d'action",
        description="Les quatre zones de compétences, ce qui donne ou prend de l'énergie, et les verbes d'action clés.",
        page_count=8,
        icon="star",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap4",
        chapter_num=4,
        title="Chapitre 4 · Valeurs, limites et argent",
        subtitle="Limites, idées reçues sur l'argent et minimum vital",
        description="Confronter les idées reçues sur l'argent aux faits, poser ses non-négociables et chiffrer son minimum vital.",
        page_count=8,
        icon="balance",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap5",
        chapter_num=5,
        title="Chapitre 5 · L'exploration du terrain",
        subtitle="Entretiens métier, réseau et test de réalité",
        description="Grille d'entretien en trois axes, idées reçues confrontées au terrain et plan de contact.",
        page_count=8,
        icon="travel_explore",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="chap6",
        chapter_num=6,
        title="Chapitre 6 · Le plan d'action",
        subtitle="Arbitrage A / B et feuille de route à 90 jours",
        description="Arbitrage entre la piste A et la piste B, feuille de route à 30, 60 et 90 jours, garde-fous et livrable final.",
        page_count=8,
        icon="route",
        category="Bilan de Compétences",
    ),
    TemplateInfo(
        id="business_plan",
        chapter_num=99,
        title="Mon business plan · De l'idée au projet viable",
        subtitle="Vision, cible, offre, modèle économique et lancement à 90 jours",
        description="Le livret complet pour structurer une création d'activité, tester son marché et obtenir ses premières ventes.",
        page_count=10,
        icon="business_center",
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
