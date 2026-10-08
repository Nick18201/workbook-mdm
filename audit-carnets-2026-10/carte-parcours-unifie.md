# Carte du parcours unifié

Proposition du 8 octobre 2026, à valider par Nicolas et Lysiane avant toute ligne de code. Elle fixe, pour les PDF comme pour l'app, une seule liste de carnets, un seul ordre et un seul contenu. Elle s'appuie sur trois sources :

- le **programme** du bilan (`chapters/programme/`), qui est la référence contractuelle : séances, livrables promis, 10 à 20 h de travail personnel ;
- les **carnets PDF** (`chapters/chap0` à `chap6`, `livret`, `business_plan`) ;
- les **carnets de l'app** (`server/predefined_workbooks.py`) ;

et sur l'audit (`synthese.html` et `rapports/` dans ce dossier).

## 1. Le constat de départ

Le programme organise le bilan en 10 séances, en 3 temps.

| Temps | Séances | Livrables promis par le programme |
|---|---|---|
| 1 · Comprendre | S1 situation et cadre · S2 héritages · S3 parcours · S4 MBTI® · S5 argent · S6 valeurs et moteurs | Profil MBTI® et analyse d'impact de l'environnement · Cartographie des énergies de travail et des facteurs d'usure · Seuil de sécurité financière (4 seuils) |
| 2 · Confronter | S7 explorer : 10 pistes, 5 réalistes et 5 audacieuses · S8 confronter : 3 familles de scénarios, enquêtes, salaires et débouchés | Matrice de faisabilité · 3 scénarios comparés · Retours d'enquêtes terrain |
| 3 · Décider et agir | S9 choisir, et adapter le carnet de route au projet (formation pour une reconversion, modèle économique pour une création, argumentaire pour une évolution interne) · S10 synthèse, pistes A et B, actions sous 7 jours · suivi à 6 mois | Feuilles de route A et B · Premières actions sous 7 jours · Document de synthèse co-rédigé |

Les deux chaînes couvrent ce parcours de façon inverse :

- **les PDF** couvrent bien le temps 1 (carnets 0 à 5). Ils couvrent le début du temps 2 (carnet 6 : 10 pistes) et survolent le temps 3 (livret de compétences). Rien pour les enquêtes, la matrice, les scénarios, la feuille de route datée.
- **l'app** comprime le temps 1 en 5 carnets courts : ni MBTI®, ni liste de valeurs, ni ligne de vie. En revanche, elle développe le temps 2 (carnet 5 « terrain ») et le temps 3 (carnet 6 « plan d'action »).

Le parcours unifié prend donc **le temps 1 des PDF et les temps 2 et 3 de l'app**, puis rattache chaque livrable promis par le programme à un carnet.

## 2. Les règles du parcours

1. **Un carnet, un intervalle entre deux séances.** Le carnet N se remplit entre la séance N et la séance N+1 : il récapitule la séance N et prépare la séance N+1. Le carnet 0 se remplit avant la séance 1. C'est déjà la logique implicite des PDF (le carnet 4 récapitule la restitution MBTI® de la séance 4 et prépare la séance 5 sur l'argent).
2. **Sept carnets, comme le promet le programme**, plus un carnet de route pour le temps 3. Les deux derniers intervalles du temps 2 tiennent dans un carnet 6 en deux parties.
3. **1 h 30 à 3 h d'écriture par intervalle, 20 h au total au plus.** Les entretiens et les recherches sur le terrain ne comptent pas dans ce temps, et le carnet le dit.
4. **Une donnée, une saisie.** Une information est écrite là où elle est produite, puis seulement reportée sur une ligne, avec son origine (« Reportez vos seuils · carnet 4 »).
5. **Chaque livrable du programme a un carnet** qui le produit (section 6).
6. **Un gabarit commun** à tous les carnets (section 3), pour que la personne retrouve ses repères.

## 3. Le gabarit commun d'un carnet

| Page | Contenu | Source |
|---|---|---|
| Couverture | Promesse du carnet. | PDF |
| Ouverture | But du carnet, liste des exercices avec leur durée, total et découpage conseillé, rappel du cadre en une ligne (« Vos réponses vous appartiennent. Vous pouvez passer une question. »), mode d'emploi en une ligne. | PDF, à compléter |
| Météo | Échelle d'énergie de 0 à 10 et une ligne « Ce chiffre s'explique surtout par… ». Deux minutes. Reprise à chaque carnet, elle mesure le chemin parcouru. | App (météo en ouverture de chaque carnet) |
| Récapitulatif guidé | Relit le livrable du carnet précédent et la séance qui vient d'avoir lieu, avec des renvois explicites. | PDF (carnets 2 à 6), à généraliser |
| Exercices | Sourcil « Exercice N · nom · durée ». Une phrase qui dit à quoi sert l'exercice. Des amorces. Un exemple contrasté (« En surface / Exploitable ») tiré d'un métier voisin. Des formats variés. Les irritants retournés en critères (« donc mon prochain poste doit… »). Le protocole de sécurité quand la charge est forte : avertissement, optionnalité, phrase d'ancrage. | Audit |
| Livrable | La sortie nommée du carnet (celle que le suivant reprend), les engagements, puis trois zones courtes : « Ce qui m'étonne en relisant ce carnet », « À aborder en séance », « Ce que j'ai laissé vierge, à reprendre ensemble ». | Audit |
| Dos | Prochaine étape. | PDF |

## 4. Le parcours, carnet par carnet

Légende des sources : **PDF** = exercice existant dans les carnets du code ; **App** = page existante dans l'app ; **Audit** = ajout ou réécriture proposé par l'audit. Les durées sont des cibles d'écriture.

### Carnet 0 · Le prélude · avant S1 · cible 1 h

Prépare S1 « Faire le point sur votre situation actuelle ».

| Exercice | Source | Décision |
|---|---|---|
| Le cadre de travail | App (trois règles) + Audit | Nouveau. Les trois règles de l'app (confidentialité, franchise, action), complétées : qui lit les réponses, droit de passer une question, ce qui est trop lourd se note pour la séance, mode d'emploi du PDF. |
| Mon engagement | PDF ex. 1 | Garder la formule « Moi, … je décide d'investir … heures », avec un repère sourcé et l'objectif en amorce. |
| Faire le point | PDF ex. 2 | Alléger : 8 questions deviennent 2 parties de 15 min, sans doublons. Ajouter « Ce bilan vient-il de vous, ou d'une demande extérieure ? ». |
| Vos domaines de vie | PDF ex. 3 | Garder : c'est la notation de référence, reprise en fin de parcours. Ajouter « Donc, mon prochain projet devra… ». |
| Votre entourage | PDF ex. 4 | Garder, en fiche à trois colonnes. Il sera repris au carnet 6. |
| Votre objectif, première version | PDF + App | Une seule question d'objectif et « Je m'autorise à explorer… », avec un exemple. Horizon unique : « d'ici la fin de votre bilan ». |

**Sortie** : engagement, situation, domaines notés, entourage, objectif v1, « Je m'autorise à ».

### Carnet 1 · L'état des lieux · S1 → S2 · cible 1 h 30

Récapitule S1, prépare S2 « Comprendre ce qui vous a construit et l'impact de vos héritages ».

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 1 | Audit | Nouveau (le carnet 1 n'en a pas). Relit l'objectif v1 du carnet 0. |
| Votre objectif boussole | PDF ex. 3 + App | Garder les trois amorces du PDF (« je veux avoir clarifié… pour pouvoir… je saurai que j'ai réussi quand… ») et ajouter l'exemple de l'app. Il précise l'objectif v1, il ne le remplace pas. |
| Le sac à dos | PDF ex. 4 + App | Prendre la forme de l'app, en deux colonnes « Ce qui pèse → Ce que je décide », sans le mot « injonction ». Protocole sur la peur. |
| Ce que vous avez reçu | PDF ex. 5 et 6 + App | Fusion. D'abord « Ce que vous avez vu » (image du travail des parents ou des adultes qui ont compté), puis « Ce que vous en faites », dans le format reçu / choisi de l'app. Remplace le « 3FVS » non expliqué. Protocole et alternative pour une famille absente ou douloureuse. |
| Vos modèles et anti-modèles | PDF ex. 7 + App | Garder, avec « Donc, dans mon prochain poste, je veux… ». |
| Météo, vision à 360° | PDF ex. 1 et 2 | Retirer : la météo passe dans le gabarit commun. La vision à 360° double les domaines de vie du carnet 0. |

**Sortie** : objectif boussole, ce que je dépose, héritage reçu et choisi, modèles et anti-modèles.

**Titre** : à décider. Le contenu porte désormais surtout sur les héritages (S2).

### Carnet 2 · Mon parcours · S2 → S3 · cible 2 h 15

Récapitule S2, prépare S3 « Analyser et comprendre votre parcours » : ce que vous savez faire, ce que vous aimez, ce qui ne vous correspond plus.

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 2 | PDF ex. 1 | Garder. Il relit « reçu / choisi » au lieu de refaire le tri. |
| À lire : comprendre ses racines | PDF | Garder, allégé (trois notions annoncées, pas neuf), avec le protocole. Retirer « névrose de classe » ou le citer avec sa source. |
| Vos expériences, une par une | PDF ex. 2 | Remplacer « aimé / pas aimé » par « ce qui me donnait de l'énergie / ce qui me coûtait ». Ajouter comment le poste a commencé et pourquoi il s'est terminé. Quatre fiches au choix. |
| Vos quatre zones | App (carnet 3) | Importer. La zone d'excellence, la zone à risque (je sais faire, mais cela m'épuise), etc. C'est la pièce qui manque aux PDF. |
| Votre fil rouge, vos moteurs | PDF ex. 3 + App | Garder, en écrivant enfin le fil rouge en une phrase. Ajouter les trois verbes d'action de l'app et « je le veux / on l'attend de moi ». |
| Votre ligne de vie | PDF ex. 4 | Garder, avec le protocole sur les vallées. |
| Vos compétences de vie | PDF ex. 5 | Garder. Ligne « épreuves » facultative. Entourer celles qu'on veut utiliser demain. |
| L'arbre de vie | PDF ex. 6 | Facultatif : c'est une synthèse de ce qui précède. |
| Interview d'une personne passionnée | PDF bonus | Déplacer au carnet 6 (enquêtes). |

**Sortie** : expériences avec énergie et coût, quatre zones, fil rouge, moteurs, verbes d'action, compétences de vie, irritants retournés en critères.

### Carnet 3 · Mes fonctionnements propres · S3 → S4 · cible 1 h 45

Récapitule S3, prépare S4, la restitution du MBTI®.

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 3 | PDF ex. 1 | Garder. Il relit le fil rouge et les quatre zones. |
| À savoir sur le MBTI® | Audit | Nouveau. Quatre préférences et non « cinq dimensions ». Ces questions ne calculent pas le type. Le type est restitué en séance et c'est la personne qui le valide. |
| Les 17 mises en situation | PDF ex. 2 à 5 | Garder, avec les réécritures de l'audit (Q1, Q4, Q7, Q8, Q13). Q14 et Q15 passent en échelle suivie d'un « pourquoi ». |
| Sous pression | PDF ex. 6 | Réécrire Q16 du point de vue des proches, sans adjectifs péjoratifs. Protocole complet. |
| Ce que j'en retiens pour mon travail | Audit | Nouveau. « Je sais le faire, mais cela me coûte… », « Pour garder mon énergie, j'ai besoin de… ». |

**Sortie** : la **cartographie des énergies de travail et des facteurs d'usure** (livrable du programme), qui assemble les quatre zones du carnet 2 et cette page.

### Carnet 4 · Mon rapport à l'argent · S4 → S5 · cible 2 h

Récapitule S4, prépare S5 « Poser sans tabou votre rapport à l'argent ».

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la restitution MBTI® | PDF ex. 1 | Garder. Ajouter le champ « le type que j'ai validé » : c'est la seule saisie du type, reportée ensuite. |
| Votre situation | PDF ex. 2 | Choix exclusif en boutons radio, puis un « pourquoi ». Reprend la note « Argent » du carnet 0. |
| Votre histoire avec l'argent | PDF ex. 3 | 4 questions ouvertes au lieu de 7, protocole complet. La question sur le couple est reformulée au passé, avec un renvoi vers la séance. |
| Vos premières expériences, vos idées reçues | PDF ex. 4 + App | L'encadré passif devient le format de l'app « Ce que je me dis → Ce que montrent les faits ». |
| Argent et projet | PDF ex. 5 | Grille d'aisance de 1 à 5 (demander une augmentation, négocier, fixer un prix…). La question « ce que vous n'osez pas demander » a sa propre case. |
| Vos quatre seuils | PDF ex. 6 + App | Une carte unique, alignée sur le programme : minimum vital, minimum sécurisant, revenu cible, durée acceptable d'une baisse. En € nets par mois, pour vous. Une fourchette suffit. « Cette piste » part au carnet 6. |
| Vos tendances | PDF ex. 7 | Deux ou trois au plus. Noms de tendances neutres (la sécurité, le mérite…). |
| Synthèse | PDF ex. 8 | Garder la question franche sur la peur du manque, puis la phrase d'ancrage. |

**Sortie** : le **seuil de sécurité financière, en 4 seuils** (livrable du programme), et la tendance dominante.

### Carnet 5 · Valeurs et moteurs profonds · S5 → S6 · cible 2 h 15

Récapitule S5, prépare S6 « Clarifier vos valeurs et vos moteurs ».

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 5 | Audit | Nouveau : seuils retenus, tendance dominante, ce que l'argent protège. |
| Alignement, désalignement, choix difficiles | PDF ex. 1 à 3 | Garder. Renvois aux sommets et vallées du carnet 2. Protocole sur le désalignement. Chaque irritant devient une condition. |
| La liste de valeurs | PDF ex. 4 | Garder, corrigée : sans doublons, avec les pôles des tensions, et 15 à 20 valeurs à cocher. |
| Hiérarchiser | PDF ex. 5 | Lignes numérotées 10, 5 puis 3. Test « si elle manquait six mois ». Une ligne « la valeur que je coche surtout parce qu'elle est attendue de moi ». |
| Incarner | PDF ex. 6 | Garder, avec l'origine de la valeur et une échelle « respectée aujourd'hui ». |
| Vos tensions | PDF ex. 8 | Placer avant les conditions. Renvoi aux seuils du carnet 4. |
| Votre grille anti-compromis | PDF ex. 7 et 9 + App | Fusion en une seule sortie : valeur, condition observable, signal d'alerte, question à poser en entretien. Les limites non financières de l'app (domaine par domaine) y entrent. Les moteurs du carnet 2 y sont relus. |

**Sortie** : la **grille anti-compromis** (le mot du programme), le seul endroit où les trois valeurs sont écrites.

### Carnet 6 · Explorer et confronter · en deux parties · cible 2 h, puis 2 h 30

**Partie 1 · S6 → S7.** Récapitule S6, prépare S7 « Explorer des métiers et des secteurs ».

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 6 | PDF ex. 1 | Une ligne par valeur, reportée depuis le carnet 5, et « ce que la séance a confirmé, ce qu'elle a déplacé ». |
| Votre cartographie | PDF ex. 2 | Une seule page de reports : type MBTI®, quatre zones, moteurs, seuils, grille anti-compromis, intérêts Hexa3D. Les seuils restent dans une zone « à garder pour vous ». |
| Le retour de vos proches | PDF ex. 3 | Lancé dès l'ouverture (les réponses prennent des jours). Proches choisis parmi les soutiens du carnet 0, une phrase à leur dire, trois cartes, « ce qui me parle / ce qu'on attend de moi », protocole. |
| Les ressources | PDF | Placées avant les pistes, liens à jour. |
| Dix pistes | PDF ex. 4 | 5 réalistes et 5 audacieuses (le mot du programme, à la place de « no limit »). Une colonne « d'où vient cette piste ». Relire « Je m'autorise à » (carnet 0). |

**Partie 2 · S7 → S8.** Prépare S8 « Approfondir et confronter vos pistes ».

| Exercice | Source | Décision |
|---|---|---|
| Vos trois pistes prioritaires | PDF ex. 5 et 6 | 3 fiches complètes au lieu de 10, les autres en option. Chaque fiche porte une rangée de critères : grille anti-compromis, seuils, énergie, « à vérifier auprès de qui ». La fiche audacieuse garde « ce que cette piste dit de ce que je cherche ». |
| Préparer vos enquêtes | App (carnet 5) + PDF bonus | Grille d'entretien de l'app, complétée par les questions de l'interview du carnet 2. Message d'approche. Trois contacts dans les 10 jours, choisis si possible parmi les modèles du carnet 1. |
| Ce que le terrain vous a appris | App (carnet 5) | Format de l'app « Ce que j'imaginais → Ce que le terrain montre », puis un compte rendu par entretien : ce qui confirme, ce qui contredit, la suite. |
| La matrice de faisabilité | Audit | Nouveau, à compléter en séance 8 : chaque piste face aux compétences, au marché et aux débouchés. Classement en trois familles : pistes directes, passerelles courtes, angles morts. |

**Sortie** : la **matrice de faisabilité** et les **retours d'enquêtes** (livrables du programme).

### Le carnet de route · temps 3 · en deux parties · cible 1 h 45, puis 1 h 45

C'est l'actuel livret de compétences, recentré. Le programme parle de « carnet de route » pour le temps 3. Le nom est à décider (section 8).

**Partie 1 · S8 → S9 · Prouver et comparer.**

| Exercice | Source | Décision |
|---|---|---|
| Votre profil, en une page | Livret thème 1 | Reports seulement (type, forces, cartographie des énergies). On ne refait plus rien. |
| Le travail réel | Livret thème 2 | Garder : « Ce que ma fiche de poste ne dit pas » est l'apport le plus original. Le travail empêché reprend le terme du carnet 2. Protocole. |
| Vos compétences prouvées | Livret thèmes 3 et 4 | Un tableau : compétence, où je l'ai prouvée, résultat ou trace, niveau d'autonomie de 1 à 4, envie de l'utiliser. Il part des compétences de vie et des expériences du carnet 2. |
| Deux récits d'action | Livret thème 5 | Deux récits au lieu d'un, « Ce récit prouve que je sais… », et une version orale en trois phrases. |
| Trois scénarios comparés | Audit | Nouveau (livrable du programme) : les trois pistes prioritaires, face aux critères et aux retours d'enquêtes. |

**Partie 2 · S9 → S10 · Décider et agir.**

| Exercice | Source | Décision |
|---|---|---|
| Piste A, piste B | App (carnet 6) + livret thème 7 | Format de l'app : projet d'élan et refuge-tremplin, atouts, risques. Les pistes viennent des scénarios. Neutre (sans « transmission »). |
| Feuille de route à 30, 60 et 90 jours | App (carnet 6) | Importer. Une feuille par piste (le programme promet les deux). |
| Vos premières actions sous 7 jours | Livret thème 7 | Action, date, personne à prévenir. |
| Garde-fous et alliés | App (carnet 6) | Importer. Les alliés viennent de l'entourage du carnet 0. |
| Le chemin parcouru | Audit | Nouveau : relire l'objectif boussole, renoter les domaines de vie du carnet 0, comparer les météos. |
| Préparer le suivi à 6 mois | Audit | Nouveau : ce qu'il faut relire et apporter à l'entretien de suivi. |
| Le module de votre projet | Programme (S9) | Selon le projet : création (module court du business plan), reconversion (formation et financement, à créer), évolution interne (argumentaire, à créer). |

**Sortie** : les **feuilles de route A et B** et les **premières actions** (livrables du programme). Elles nourrissent le document de synthèse co-rédigé, qui reste un document à part.

### Le business plan · deux formats

- **Le module création du carnet de route** (S9 → S10, environ 3 h) : le parcours court de 12 pages proposé par l'audit (fondations, problème, offre, prix, point mort, test, synthèse). Il reprend les seuils et la grille anti-compromis, avec l'entretien prospects de l'app (objections, prix perçu, déclencheur d'achat).
- **Le livret projet complet**, outil autonome pour l'accompagnement à la création après le bilan. Il s'ouvre par un mode d'emploi, avec des renvois « Si vous avez fait le bilan : … ». Il intègre les refontes de l'audit (finances guidées, page « Le risque, pour vous », reprise d'activité, informations réglementaires renvoyées vers les sources officielles).

## 5. Le budget de temps

| Intervalle | Carnet | Cible | Estimation actuelle |
|---|---|---|---|
| avant S1 | Carnet 0 | 1 h | ≈ 1 h 15 |
| S1 → S2 | Carnet 1 | 1 h 30 | 1 h 50 – 2 h 30 |
| S2 → S3 | Carnet 2 | 2 h 15 | 2 h 35 – 3 h 35 |
| S3 → S4 | Carnet 3 | 1 h 45 | 1 h 40 – 2 h 30 |
| S4 → S5 | Carnet 4 | 2 h | ≈ 2 h 30 |
| S5 → S6 | Carnet 5 | 2 h 15 | 2 h 30 – 3 h |
| S6 → S7 | Carnet 6, partie 1 | 2 h | 5 – 7 h pour tout le carnet |
| S7 → S8 | Carnet 6, partie 2 | 2 h 30 (hors entretiens) | |
| S8 → S9 | Carnet de route, partie 1 | 1 h 45 | 3 h 30 – 4 h 30 pour tout le livret |
| S9 → S10 | Carnet de route, partie 2 | 1 h 45 (+ module) | |
| **Total** | | **≈ 18 h 45**, dans les 10-20 h du programme | ≈ 21 – 27 h |

Le module de projet (création, reconversion, évolution) s'ajoute pour les personnes concernées. Il reste dans l'enveloppe si la partie 2 du carnet de route s'allège d'autant pour elles.

## 6. Les données qui circulent

Chaque ligne : où la donnée est écrite (une seule fois), et où elle est reportée.

| Donnée | Écrite dans | Reportée dans |
|---|---|---|
| Météo (énergie de 0 à 10) | Ouverture de chaque carnet | Carnet de route : le chemin parcouru · suivi à 6 mois |
| Domaines de vie notés | Carnet 0 | Carnet de route, partie 2 (nouvelle notation) |
| Objectif v1, « Je m'autorise à » | Carnet 0 | Carnet 1 (boussole) · carnet 6 (pistes audacieuses) |
| Entourage | Carnet 0 | Carnet 6 (retour des proches) · carnet de route (alliés) |
| Objectif boussole | Carnet 1 | Carnet de route (le chemin parcouru) |
| Ce que je dépose, héritage reçu et choisi | Carnet 1 | Carnet 2 (récapitulatif) · carnet 4 (histoire avec l'argent) |
| Modèles, anti-modèles | Carnet 1 | Carnet 6 (contacts d'enquête) |
| Expériences avec énergie et coût, irritants retournés | Carnet 2 | Carnet 5 (grille anti-compromis) · carnet de route (preuves) |
| Quatre zones, fil rouge, moteurs, verbes d'action | Carnet 2 | Carnet 3 (cartographie des énergies) · carnet 5 · carnet 6 |
| Compétences de vie | Carnet 2 | Carnet de route (compétences prouvées) |
| Cartographie des énergies | Carnet 3 | Carnet 6 · carnet de route |
| Type MBTI® validé | Carnet 4 (récapitulatif) | Carnet 6 · carnet de route |
| 4 seuils, tendance dominante | Carnet 4 | Carnet 5 (récapitulatif, tensions) · fiches du carnet 6 · carnet de route · module création |
| Grille anti-compromis (3 valeurs) | Carnet 5 | Fiches et enquêtes du carnet 6 · piste A / piste B · module création |
| Intérêts Hexa3D | Séance (à préciser) | Carnet 6 (cartographie) |
| 10 pistes | Carnet 6, partie 1 | Carnet 6, partie 2 (3 prioritaires) |
| Fiches, enquêtes, matrice | Carnet 6, partie 2 | Carnet de route (scénarios) |
| Compétences prouvées, récits | Carnet de route, partie 1 | Partie 2 · module évolution interne |
| Pistes A et B, feuilles de route, actions | Carnet de route, partie 2 | Document de synthèse · suivi à 6 mois |

## 7. Personnalisation dans l'app

L'app a deux usages : créer un livret de toutes pièces, puis exporter son JSON pour l'intégrer à la base, et personnaliser un livret existant.

**Créer de toutes pièces.** Les candidats naturels sont les deux modules qui manquent au carnet de route : reconversion (formation et financement) et évolution interne (argumentaire de repositionnement). Une fois le format unifié, un livret exporté de l'app s'intègre en déposant son fichier JSON dans le dossier des carnets, sans retranscription.

**Personnaliser.** Chaque bloc du format porte une marque « fixe » ou « adaptable ». La personnalisation ne touche que les blocs adaptables.

| Pertinence | Carnets | Ce qui s'adapte | Ce qui reste fixe |
|---|---|---|---|
| Forte | Carnet 6, carnet de route et ses modules, business plan | Pistes pré-intitulées, ressources du secteur, nombre de fiches, contacts suggérés, exemples, module de projet | Gabarit, protocole, critères des fiches, définitions des seuils |
| Moyenne | Carnets 1, 2 et 4 | Vocabulaire du secteur, situation (reconversion, évolution, retour à l'emploi), nombre de fiches d'expérience, exemples. Au carnet 4, le statut (salarié, indépendant, demandeur d'emploi), jamais de chiffres personnels | Protocole, questions franches, carte des seuils |
| Faible | Carnets 0, 3 et 5 | Au plus le prénom et les exemples | Le cadre (carnet 0), les questions MBTI® (les personnaliser biaiserait la restitution), la liste de valeurs et l'entonnoir (carnet 5) |

Deux règles valent partout :
- **les exemples viennent d'un métier voisin**, jamais du métier de la personne, sinon ils sont recopiés ;
- **ne sont jamais modifiés** : le cadre, le protocole de sécurité, les textes réglementaires et les renvois entre carnets.

## 8. Les décisions à prendre

1. **La règle « un carnet entre la séance N et la séance N+1 »** : la valider.
2. **Le carnet de route** : faut-il renommer le livret de compétences « carnet de route », puisque le programme emploie ce mot pour le temps 3 et ne nomme pas le livret ? Ou garder « livret de compétences » et l'ajouter au programme ? Le programme est un texte réglementaire.
3. **Le carnet 6 en deux parties** (on reste à 7 carnets), ou deux carnets séparés (il faudrait alors changer le programme, qui annonce 7 carnets).
4. **Le titre du carnet 1**, dont le contenu porte désormais surtout sur les héritages.
5. **Le business plan en deux formats** : un module court dans le bilan et un livret complet autonome.
6. **Hexa3D** : à quelle séance le test est-il passé et restitué ? Aucun carnet n'en parle aujourd'hui.
7. **Les retraits** : vision à 360° et météo séparée (carnet 1), arbre de vie facultatif (carnet 2), interview déplacée (carnet 2 vers le carnet 6), 10 fiches réduites à 3 obligatoires (carnet 6).
8. **Les deux modules à créer** : formation et financement (reconversion), argumentaire (évolution interne). Faut-il les créer avec l'app ?

## 9. Ce que cela implique pour le format technique

Une fois la carte validée, le format unifié doit savoir décrire :
- **les blocs des PDF** que l'app ne connaît pas encore : heading, paragraphs, fields_card, annotation, link_card, numbered_lines, info_cards, frise, checklist_cards, rating_grid, star_list, page_break ;
- **les gabarits dessinés** : ligne de vie, arbre de vie, cartographie, matrice ;
- **les composants du gabarit commun** : météo, récapitulatif avec reports, protocole de sécurité, exemple contrasté, durée dans le sourcil, livrable à trois zones ;
- **la marque « fixe / adaptable »** de chaque bloc ;
- **des identifiants stables pour les données** (par exemple `c4.seuils`). Un renvoi (« Reportez vos seuils ») pourrait alors être résolu au moment de la génération en « carnet 4, p. 12 », sans numéro de page écrit à la main.

Ce que Gemini a le droit de produire reste un sous-ensemble de ce que le moteur sait dessiner.
