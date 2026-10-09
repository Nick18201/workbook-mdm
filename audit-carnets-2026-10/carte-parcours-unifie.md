# Carte du parcours unifié

Version du 8 octobre 2026. Elle intègre les décisions de Nicolas :
- plus de carnet 0 ;
- un carnet 1 qui réunit un état des lieux rapide et les héritages ;
- le carnet N prépare la séance N ;
- la séance libérée va au temps 2 ;
- le document du temps 3 s'appelle « carnet de route » ;
- le nouveau parcours vaut pour les futurs bénéficiaires, sans date de bascule ;
- l'option « Initiation à l'IA » ouvre la séance 6 ;
- on parle d'un « test des fonctionnements cognitifs », version maison conçue et éprouvée par Lysiane Brand, et plus jamais du MBTI, marque soumise à licence ;
- Hexa3D est abandonné.

Elle fixe, pour les PDF comme pour l'app, une seule liste de carnets, un seul ordre et un seul contenu. Elle s'appuie sur :
- le programme du bilan (`chapters/programme/`) ;
- les carnets PDF (`chapters/chap0` à `chap6`, `livret`, `business_plan`), retirés du dépôt en R11 (l'historique git les garde) ;
- les carnets de l'app (`server/predefined_workbooks.py`) ;
- l'audit (`synthese.html` et `rapports/` dans ce dossier).

Le récapitulatif destiné à l'agent du site est dans `recap-site-parcours.md`.

## 1. Le constat de départ

Le programme actuel organise le bilan en 10 séances, en 3 temps : comprendre (S1 à S6), confronter (S7 et S8), décider et agir (S9 et S10), plus un suivi à 6 mois.

Les deux chaînes couvrent ce parcours de façon inverse :
- **les PDF** couvrent bien le temps 1, puis s'essoufflent : rien pour les enquêtes, la matrice, les scénarios ni la feuille de route datée ;
- **l'app** comprime le temps 1 (ni test des fonctionnements cognitifs, ni liste de valeurs, ni ligne de vie), mais développe le terrain et le plan d'action.

L'audit a aussi relevé un déséquilibre :
- six séances d'introspection pour deux de terrain ;
- 1 à 2 semaines seulement pour obtenir des entretiens avec des professionnels ;
- des pistes qui partent de zéro à la séance 7 ;
- un doublon entre les carnets 0 et 1, qui demandent deux fois l'objectif, l'humeur et les domaines de vie.

Le parcours unifié prend **le temps 1 des PDF et les temps 2 et 3 de l'app**. Il fusionne le début du parcours et donne au terrain la séance libérée.

## 2. Le nouveau découpage des séances

Toujours 10 séances de 1 h 20 et un suivi de 40 min à 6 mois. La répartition passe de 6 / 2 / 2 à **5 / 3 / 2**.

| Temps | Séance | Sujet | Carnet qui la prépare | Livrables du temps |
|---|---|---|---|---|
| 1 · Comprendre | S1 | État des lieux et héritages : votre situation, ce qui vous pèse, ce qui tient encore, ce que vous avez reçu de votre milieu. Le cadre de travail. | Carnet 1 | Profil de fonctionnement cognitif et analyse d'impact de l'environnement · Cartographie des énergies de travail et des facteurs d'usure · Seuil de sécurité financière (4 seuils) |
| | S2 | Votre parcours réel | Carnet 2 | |
| | S3 | Votre fonctionnement cognitif | Carnet 3 | |
| | S4 | Votre rapport à l'argent | Carnet 4 | |
| | S5 | Vos valeurs et vos moteurs | Carnet 5 | |
| 2 · Explorer | S6 | Explorer : 10 pistes, 5 réalistes et 5 audacieuses ; choix des 3 pistes à explorer sur le terrain | Carnet 6 | Matrice de faisabilité · 3 scénarios comparés · Retours d'enquêtes terrain |
| | S7 | Explorer le terrain : les 3 pistes passées au crible de vos critères, enquêtes préparées et lancées, salaires et débouchés | Carnet 7, partie 1 | |
| | S8 | Tirer les leçons du terrain : ce que les enquêtes confirment ou contredisent, matrice de faisabilité, 3 familles de scénarios (pistes directes, passerelles courtes, angles morts) | Carnet 7, partie 2 | |
| 3 · Décider et agir | S9 | Choisir, et adapter le carnet de route au projet (formation pour une reconversion, modèle économique pour une création, argumentaire pour une évolution interne) | Carnet de route, partie 1 | Feuilles de route A et B · Premières actions sous 7 jours · Document de synthèse co-rédigé · Suivi à 6 mois |
| | S10 | Synthèse, piste A (projet d'élan) et piste B (refuge et tremplin), premières actions | Carnet de route, partie 2 | |
| | Suivi | Point à 6 mois (40 min) | — | |

L'option « Initiation à l'IA » ouvre **la séance 6**, celle de l'exploration.

## 3. Les règles du parcours

1. **Le carnet N prépare la séance N.** Il se remplit entre la séance N−1 et la séance N. Le carnet 1 se remplit avant la séance 1, après le premier échange de 30 min.
2. **Sept carnets de bord (1 à 7), comme le promet le programme, puis le carnet de route du temps 3.** Le carnet 7 et le carnet de route ont chacun deux parties, une par intervalle entre deux séances.
3. **1 h 30 à 3 h d'écriture par intervalle, 20 h au total au plus.** Les entretiens, les échanges avec les proches et les recherches ne comptent pas dans ce temps, et le carnet le dit.
4. **Une donnée, une saisie.** Une information est écrite là où elle est produite, puis seulement reportée sur une ligne, avec son origine (« Reportez vos seuils · carnet 4 »).
5. **Chaque livrable du programme a un carnet** qui le produit (section 5).
6. **Un gabarit commun** à tous les carnets (section 4).
7. **Le terrain commence avant le temps 2.** Le fil des pistes démarre au carnet 2, l'interview d'un professionnel est proposée dès le carnet 2, et les proches sont sollicités en fin de carnet 5.
8. **Deux semaines pour chaque intervalle de terrain** (S6 → S7 et S7 → S8), la borne haute du programme, qui annonce des séances espacées de 1 à 2 semaines. Des séances plus rapprochées pendant le temps 1 si la personne le souhaite.
9. **Le document de synthèse se prépare au fil de l'eau.** Chaque livrable de carnet en est une brique. La séance 10 sert à le relire et à décider, pas à l'assembler.

## 4. Le gabarit commun d'un carnet

| Page | Contenu | Source |
|---|---|---|
| Couverture | Promesse du carnet. | PDF |
| Ouverture | Le but du carnet, la liste des exercices avec leur durée, le total et le découpage conseillé. Un rappel du cadre en une ligne : « Vos réponses vous appartiennent. Vous pouvez passer une question. » Le mode d'emploi en une ligne. | PDF, à compléter |
| Météo | Une échelle d'énergie de 0 à 10 et une ligne « Ce chiffre s'explique surtout par… ». Deux minutes. Reprise à chaque carnet, elle mesure le chemin parcouru. | App |
| Récapitulatif guidé | À partir du carnet 2. Il relit le livrable du carnet précédent et la séance qui vient d'avoir lieu, avec des renvois explicites. | PDF, à généraliser |
| Exercices | Sourcil « Exercice N · nom · durée », et une phrase qui dit à quoi sert l'exercice. Des amorces, et un exemple contrasté (« En surface / Exploitable ») tiré d'un métier voisin. Des formats variés. Les irritants retournés en critères (« donc mon prochain poste doit… »). Le protocole de sécurité quand la charge est forte : avertissement, optionnalité, phrase d'ancrage. | Audit |
| Livrable | La sortie nommée du carnet : celle que le suivant reprend, et une brique du document de synthèse. Les engagements. Trois zones courtes : « Ce qui m'étonne en relisant mes réponses », « À aborder en séance », « Les questions que j'ai passées, à reprendre ensemble ». À partir du carnet 2, une ligne de plus : « Une idée de piste qui m'est venue en remplissant ce carnet » (le fil des pistes). | Audit |
| Dos | Prochaine étape. | PDF |

## 5. Le parcours, carnet par carnet

Légende des sources :
- **PDF C0 à C6** : exercice des carnets actuels du code ;
- **Livret** : l'actuel livret de compétences ;
- **App** : page des carnets actuels de l'app ;
- **Audit** : ajout ou réécriture proposé par l'audit.

Les durées sont des cibles d'écriture.

### Carnet 1 · L'état des lieux · avant S1 · cible 1 h 45

Prépare S1. Un état des lieux rapide, puis les héritages, qui en font partie.

| Exercice | Source | Décision |
|---|---|---|
| Le cadre de travail | App (trois règles) + Audit | Les trois règles de l'app (confidentialité, franchise, action), complétées : qui lit les réponses, droit de passer une question, ce qui est trop lourd se note pour la séance, mode d'emploi du PDF. |
| Mon engagement | PDF C0 ex. 1 | Garder la formule « Moi, … je décide d'investir … heures », avec un repère sourcé. |
| Faire le point, rapidement | PDF C0 ex. 2 + PDF C1 ex. 4 + App | Quatre questions au lieu de huit, environ 20 min. Où j'en suis (avec une amorce). Ce qui pèse et ce que je décide (le sac à dos, en deux colonnes comme dans l'app, avec le protocole sur la peur). Ce qui tient encore. Ce bilan vient-il de moi ou d'une demande extérieure ? |
| Vos domaines de vie | PDF C0 ex. 3 | Garder : c'est la notation de référence, reprise en fin de parcours. Ajouter « Donc, mon prochain projet devra… ». |
| Votre objectif, première version | PDF C0 + App | Une seule question d'objectif, avec un exemple. Et « Je m'autorise à explorer… ». Horizon unique : « d'ici la fin de votre bilan ». |
| Ce que vous avez reçu | PDF C1 ex. 5 et 6 + App | Fusion. D'abord « Ce que vous avez vu » (le travail des parents ou des adultes qui ont compté), puis « Ce que vous en faites », au format reçu / choisi de l'app. Remplace le « 3FVS » non expliqué. Protocole, et une alternative pour une famille absente ou douloureuse. |
| Vos modèles et anti-modèles | PDF C1 ex. 7 + App | Garder, avec « Donc, dans mon prochain poste, je veux… ». |
| Retirés | PDF C0 et C1 | Les quatre autres questions de « Faire le point ». La vision à 360° (doublon des domaines de vie). La météo séparée (elle passe dans le gabarit). L'entourage (déplacé au carnet 5, où l'on choisit les proches à solliciter). L'objectif boussole (déplacé au carnet 2, après la séance 1). |

**Sortie** : votre point de départ. Il réunit la situation, ce qui pèse et ce qui tient, les domaines notés, l'objectif v1, « Je m'autorise à », l'héritage reçu et choisi, les modèles et anti-modèles.

### Carnet 2 · Mon parcours · S1 → S2 · cible 2 h 45

Récapitule S1 et prépare S2, qui porte sur le parcours réel : ce que vous savez faire, ce que vous aimez, ce qui ne vous correspond plus.

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 1 et objectif boussole | PDF C1 ex. 3 + App | Précise l'objectif v1 après la séance 1. Trois amorces du PDF (« je veux avoir clarifié… pour pouvoir… je saurai que j'ai réussi quand… ») et l'exemple de l'app. |
| À lire : comprendre ses racines | PDF C2 | Garder, allégé : trois notions annoncées, pas neuf. Protocole. Retirer « névrose de classe », ou la citer avec sa source. |
| Vos expériences et votre travail réel | PDF C2 ex. 2 + Livret thème 2 | Une fiche par expérience, quatre au choix. Chaque fiche porte : les missions, ce que la fiche de poste ne dit pas, ce qui me donnait de l'énergie, ce qui me coûtait, comment le poste a commencé et pourquoi il s'est terminé. Le programme rattache le travail réel à cette séance. |
| Le travail empêché | Livret thème 2 | Une page, qui applique l'activité empêchée expliquée dans l'« À lire ». Un seul terme pour les deux. Protocole. |
| Vos quatre zones | App (carnet 3) | Importer : zone d'excellence, zone à risque (je sais faire, mais cela m'épuise), etc. |
| Votre fil rouge, vos moteurs | PDF C2 ex. 3 + App | Le fil rouge enfin écrit en une phrase. Les trois verbes d'action de l'app. Pour chaque moteur : « je le veux / on l'attend de moi ». |
| Votre ligne de vie | PDF C2 ex. 4 | Garder, avec le protocole sur les vallées. |
| Vos compétences de vie | PDF C2 ex. 5 | Garder. Ligne « épreuves » facultative. Entourer celles qu'on veut utiliser demain. |
| L'arbre de vie | PDF C2 ex. 6 | Facultatif : c'est une synthèse de ce qui précède. |
| Interview d'une personne passionnée | PDF C2 bonus | Premier contact avec le terrain, facultatif, hors temps d'écriture. Si possible l'un des modèles du carnet 1. Le rendez-vous reste ouvert jusqu'au carnet 7. |

**Sortie** : votre fil rouge. Il réunit les expériences avec énergie et coût, le travail réel et le travail empêché, les quatre zones, les moteurs et les verbes d'action, les compétences de vie, les irritants retournés en critères. Premières lignes du fil des pistes.

### Carnet 3 · Mes fonctionnements propres · S2 → S3 · cible 1 h 45

Récapitule S2 et prépare S3, la restitution du test des fonctionnements cognitifs.

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 2 | PDF C3 ex. 1 | Il relit le fil rouge et les quatre zones. |
| À savoir sur le test | Audit | Nouveau. Le test des fonctionnements cognitifs est une version maison, conçue et éprouvée par Lysiane Brand, psychologue du travail. Quatre préférences, pas « cinq dimensions ». Les mises en situation du carnet ne calculent pas le profil. Le profil est restitué en séance, et c'est la personne qui le valide. Aucune mention du MBTI. |
| Les 17 mises en situation | PDF C3 ex. 2 à 5 | Garder, avec les réécritures de l'audit (Q1, Q4, Q7, Q8, Q13). Q14 et Q15 passent en échelle suivie d'un « pourquoi ». |
| Sous pression | PDF C3 ex. 6 | Q16 réécrite du point de vue des proches, sans adjectifs péjoratifs. Protocole complet. |
| Ce que j'en retiens pour mon travail | Audit | Nouveau : « Je sais le faire, mais cela me coûte… », « Pour garder mon énergie, j'ai besoin de… ». |

**Sortie** : la **cartographie des énergies de travail et des facteurs d'usure** (livrable du programme). Elle assemble les quatre zones du carnet 2 et cette page.

### Carnet 4 · Mon rapport à l'argent · S3 → S4 · cible 2 h

Récapitule S3 et prépare S4.

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la restitution du test | PDF C4 ex. 1 | Avec le champ « le profil de fonctionnement que j'ai validé » : c'est la seule saisie du profil, reportée ensuite. |
| Votre situation | PDF C4 ex. 2 | Choix exclusif en boutons radio, puis un « pourquoi ». Reprend la note « Argent » des domaines de vie (carnet 1). |
| Votre histoire avec l'argent | PDF C4 ex. 3 | 4 questions ouvertes au lieu de 7. Protocole complet. La question sur le couple est posée au passé, avec un renvoi vers la séance. Renvoi à l'héritage du carnet 1. |
| Vos premières expériences, vos idées reçues | PDF C4 ex. 4 + App | L'encadré passif devient le format de l'app : « Ce que je me dis → Ce que montrent les faits ». |
| Argent et projet | PDF C4 ex. 5 | Grille d'aisance de 1 à 5 (demander une augmentation, négocier, fixer un prix…). « Ce que je n'ose pas demander » a sa propre case. |
| Vos quatre seuils | PDF C4 ex. 6 + App | Une carte unique, alignée sur le programme : minimum vital, minimum sécurisant, revenu cible, durée acceptable d'une baisse. En € nets par mois, pour vous. Une fourchette suffit. |
| Vos tendances | PDF C4 ex. 7 | Deux ou trois au plus, avec des noms neutres (la sécurité, le mérite…). |
| Synthèse | PDF C4 ex. 8 | Garder la question franche sur la peur du manque, suivie de la phrase d'ancrage. |

**Sortie** : le **seuil de sécurité financière, en 4 seuils** (livrable du programme), et la tendance dominante.

### Carnet 5 · Valeurs et moteurs profonds · S4 → S5 · cible 2 h 15

Récapitule S4 et prépare S5.

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 4 | Audit | Nouveau : seuils retenus, tendance dominante, ce que l'argent protège. |
| Alignement, désalignement, choix difficiles | PDF C5 ex. 1 à 3 | Renvois aux sommets et aux vallées du carnet 2. Protocole sur le désalignement. Chaque irritant devient une condition. |
| La liste de valeurs | PDF C5 ex. 4 | Liste corrigée : sans doublons, avec les pôles des tensions, 15 à 20 valeurs à cocher. |
| Hiérarchiser | PDF C5 ex. 5 | Lignes numérotées 10, 5 puis 3, et le test « si elle manquait six mois ». Une ligne « la valeur que je coche surtout parce qu'elle est attendue de moi ». |
| Vos tensions | PDF C5 ex. 8 | Placées avant la grille, avec un renvoi aux seuils du carnet 4. |
| Votre grille anti-compromis | PDF C5 ex. 6, 7 et 9 + App | Une seule sortie. Pour chacune des 3 valeurs : d'où elle vient, la condition observable, le signal d'alerte, la question à poser en entretien. Les limites non financières de l'app y entrent. Les moteurs du carnet 2 y sont relus. |
| Votre entourage, et le retour de vos proches | PDF C0 ex. 4 + PDF C6 ex. 3 | Les soutiens et les regards critiques, en quelques lignes. Puis trois proches à qui envoyer la question : « Si tu ne connaissais pas mon métier actuel, à quel métier penserais-tu pour moi ? Qu'est-ce qui, chez moi, t'y fait penser ? ». Leurs réponses arriveront avant la séance 6. |

**Sortie** : la **grille anti-compromis**, le seul endroit où les 3 valeurs sont écrites. La demande aux proches est partie.

### Carnet 6 · L'exploration · S5 → S6 · cible 2 h

Récapitule S5 et prépare S6 « Explorer ».

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 5 | PDF C6 ex. 1 | Une ligne par valeur, reportée du carnet 5, et « ce que la séance a confirmé, ce qu'elle a déplacé ». |
| Votre cartographie | PDF C6 ex. 2 | Une seule page de reports : profil de fonctionnement, cartographie des énergies, moteurs, seuils, grille anti-compromis. Les seuils restent dans une zone « à garder pour vous ». |
| Le retour de vos proches | PDF C6 ex. 3 | Recueil des réponses : trois cartes, une par personne, puis « ce qui me parle vraiment / ce qui ressemble plutôt à ce qu'on attend de moi ». Protocole. |
| Les ressources | PDF C6 | Placées avant les pistes. Liens à jour. |
| Dix pistes | PDF C6 ex. 4 | 5 réalistes et 5 audacieuses. Elles partent du fil des pistes, des suggestions des proches et de « Je m'autorise à » (carnet 1). Une colonne « d'où vient cette piste ». |

**Sortie** : **10 pistes qualifiées**. La séance 6 en retient 3 à explorer sur le terrain.

### Carnet 7 · Explorer le terrain · en deux parties · cible 1 h 45, puis 2 h

**Partie 1 · S6 → S7 · deux semaines.** Prépare S7.

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 6 | Audit | Les 3 pistes retenues, et pourquoi. |
| Vos trois fiches | PDF C6 ex. 5 et 6 | Une fiche par piste retenue, avec une rangée de critères : grille anti-compromis, seuils, énergie, « à vérifier auprès de qui ». La fiche audacieuse garde « ce que cette piste dit de ce que je cherche ». Les autres pistes restent en option. |
| Préparer vos enquêtes | App (carnet 5) + PDF C2 bonus | La grille d'entretien de l'app, complétée par les questions de l'interview du carnet 2. Un message d'approche. Trois contacts à solliciter dans les 10 jours, si possible parmi les modèles du carnet 1. |
| Salaires et débouchés | Programme + Audit | Où chercher, et ce qu'il faut noter pour son bassin d'emploi. Des liens officiels, pas de chiffres écrits dans le carnet. |

**Partie 2 · S7 → S8 · deux semaines.** Prépare S8.

| Exercice | Source | Décision |
|---|---|---|
| Vos comptes rendus d'enquête | Audit | Un par entretien : ce qui confirme, ce qui contredit, la suite. |
| Ce que le terrain vous a appris | App (carnet 5) | « Ce que j'imaginais → Ce que le terrain montre ». |
| La matrice de faisabilité | Audit | Chaque piste face aux compétences, au marché et aux débouchés. Brouillon ici, finalisé en séance 8 avec le classement en trois familles : pistes directes, passerelles courtes, angles morts. |

**Sortie** : les **retours d'enquêtes** et la **matrice de faisabilité** (livrables du programme). La séance 8 en tire les **3 scénarios comparés**.

### Le carnet de route · temps 3 · en deux parties · cible 1 h 30, puis 1 h 45

C'est l'actuel livret de compétences, recentré et renommé.

**Partie 1 · S8 → S9 · Prouver et préparer le choix.**

| Exercice | Source | Décision |
|---|---|---|
| Récapitulatif de la séance 8 | Audit | Les 3 scénarios, et vers lequel vous penchez. Les trois familles y sont définies : les pistes directes (avec vos compétences actuelles), les passerelles courtes (après une formation courte), les angles morts (des pistes que vous ne regardiez pas, apparues en chemin). |
| Votre profil, en une page | Livret thème 1 | Reports seulement : profil de fonctionnement, forces, cartographie des énergies. On ne refait plus rien. Sans l'exemple « ISFJ » ni aucun code de type. |
| Vos compétences prouvées | Livret thèmes 3 et 4 | Un tableau : compétence, où je l'ai prouvée, résultat ou trace, niveau d'autonomie de 1 à 4, envie de l'utiliser. Il part des expériences, du travail réel et des compétences de vie du carnet 2. |
| Deux récits d'action | Livret thème 5 | Deux récits au lieu d'un, « Ce récit prouve que je sais… », et une version orale en trois phrases. |

**Partie 2 · S9 → S10 · Décider et agir.**

| Exercice | Source | Décision |
|---|---|---|
| Piste A, piste B | App (carnet 6) + Livret thème 7 | Le format de l'app : projet d'élan et refuge-tremplin, atouts, risques. Les pistes viennent des scénarios. |
| Feuilles de route à 30, 60 et 90 jours | App (carnet 6) | Importer. Une par piste, comme le promet le programme. |
| Vos premières actions sous 7 jours | Livret thème 7 | Action, date, personne à prévenir. |
| Garde-fous et soutiens | App (carnet 6) | Importer. Les soutiens viennent de l'entourage noté au carnet 5. |
| Le chemin parcouru | Audit | Relire l'objectif boussole, renoter les domaines de vie du carnet 1, comparer les météos. |
| Préparer le suivi à 6 mois | Audit | Ce qu'il faut relire et apporter à l'entretien de suivi. |
| Le module de votre projet | Programme (S9) | Selon le projet : création (module court du business plan), reconversion (formation et financement, à créer), évolution interne (argumentaire, à créer). |

**Sortie** : les **feuilles de route A et B** et les **premières actions** (livrables du programme). Le document de synthèse co-rédigé reste un document à part, mais ses briques sont prêtes (section 7).

### Le business plan · deux formats

- **Le module création du carnet de route** (S9 → S10, 2 h, `module-creation.json`, R9). C'est le parcours court proposé par l'audit, en 13 pages d'exercices : les seize exercices indispensables du livret, condensés en dix (fondations, problème, offre, prix, dépenses et charges, point mort face aux seuils, le risque pour vous, financement, test et entretiens prospects, synthèse et décision).
  - Il reporte la piste A et sa feuille de route (`route.pistes`, `route.feuilles`), le critère d'énergie (`c3.energies`), les trois valeurs et leurs conditions (`c5.grille`), les quatre seuils (`c4.seuils`, « À garder pour vous »), sans nouvelle saisie.
  - Il reprend l'entretien prospects de l'app (objections, prix perçu, déclencheur d'achat), sur une page qui se remplit au fil des entretiens, hors temps d'écriture.
  - Seule la synthèse se montre. Le risque pour vous prend le protocole complet. Aucun taux ni montant : des liens officiels (Urssaf, impots.gouv.fr, Bpifrance Création, France Travail, réseaux de prêts d'honneur).
  - Il déclare `"carnet": "route"` : la couleur et le folio du carnet de route. Le livret complet prend le relais après le bilan.
- **Le livret projet complet**, outil autonome pour l'accompagnement à la création après le bilan. Il s'ouvre par un mode d'emploi et des renvois « Si vous avez fait le bilan : … ». Il intègre les refontes de l'audit : finances guidées, page « Le risque, pour vous », reprise d'activité, informations réglementaires renvoyées vers les sources officielles.

## 6. Le budget de temps

| Intervalle | Carnet | Cible | Correspond aujourd'hui à | Estimation actuelle |
|---|---|---|---|---|
| avant S1 | Carnet 1 | 1 h 45 | `carnet-1.json` (R1), issu du carnet 0 et d'une partie du carnet 1 | 1 h 45, affiché exercice par exercice (avant : ≈ 1 h 15, plus 1 h 50 – 2 h 30) |
| S1 → S2 | Carnet 2 | 2 h 45 | `carnet-2.json` (R2), issu du carnet 2 et du travail réel du livret | 2 h 45, affiché exercice par exercice, plus l'arbre de vie (15 min) et l'interview, facultatifs (avant : 2 h 35 – 3 h 35, plus le bonus) |
| S2 → S3 | Carnet 3 | 1 h 45 | `carnet-3.json` (R3), issu du carnet 3 | 1 h 45, affiché exercice par exercice (avant : 1 h 40 – 2 h 30) |
| S3 → S4 | Carnet 4 | 2 h | `carnet-4.json` (R4), issu du carnet 4 et des idées reçues de l'app | 2 h, affiché exercice par exercice (avant : ≈ 2 h 30) |
| S4 → S5 | Carnet 5 | 2 h 15 | `carnet-5.json` (R5), issu du carnet 5 et des limites hors argent de l'app | 2 h 15, affiché exercice par exercice (avant : 2 h 30 – 3 h, affiché 95 min) |
| S5 → S6 | Carnet 6 | 2 h | `carnet-6.json` (R6), issu de la partie exploration du carnet 6 | 2 h, affiché exercice par exercice (avant : 5 – 7 h pour tout le carnet 6) |
| S6 → S7 | Carnet 7, partie 1 | 1 h 45 | `carnet-7.json` (R7), partie 1, issue des fiches du carnet 6 et du carnet terrain de l'app | 1 h 45, affiché exercice par exercice : trois fiches à critères au lieu de dix (avant : 2 h 30 – 4 h pour les dix fiches) |
| S7 → S8 | Carnet 7, partie 2 | 2 h | `carnet-7.json` (R7), partie 2 | 2 h, affiché exercice par exercice (n'existait pas) ; les entretiens se font hors temps d'écriture |
| S8 → S9 | Carnet de route, partie 1 | 1 h 30 | `carnet-de-route.json` (R8), partie 1, issue des thèmes 1, 3, 4 et 5 du livret | 1 h 30, affiché exercice par exercice (avant : 3 h 30 – 4 h 30 pour tout le livret) |
| S9 → S10 | Carnet de route, partie 2 | 1 h 45 (+ module) | `carnet-de-route.json` (R8), partie 2, issue du thème 7 du livret et du plan d'action de l'app | 1 h 45, affiché exercice par exercice, plus le module de projet (n'existait pas) |
| S9 → S10, création | Module création | 2 h | `module-creation.json` (R9), issu des exercices indispensables du livret business plan et de l'entretien prospects de l'app | 2 h, affiché exercice par exercice, entretiens prospects hors temps d'écriture (avant : 7 h 20 pour les indispensables du livret, 15 h pour tout le livret) |
| **Total** | | **≈ 19 h 30**, dans les 10-20 h du programme | | 19 h 30 affichées, carnet par carnet (avant : ≈ 21 – 27 h) ; 21 h 30 avec le module création |

L'interview du carnet 2, les échanges avec les proches, les entretiens du carnet 7 et les entretiens prospects du module création se font hors temps d'écriture. Le module de projet s'ajoute pour les personnes concernées : avec le module création, l'intervalle S9 → S10 passe à 3 h 45 et le total à 21 h 30, au-dessus de la fourchette du programme, qui le dit désormais (PR #69 : « Un projet de création ajoute un module d'environ 2 h entre les séances 9 et 10. »).

Depuis R11, les documents d'où viennent les carnets (anciens carnets 0 à 6, livret de compétences) ne sont plus dans le dépôt ni dans l'app : les estimations « avant » restent ici pour mémoire. Le programme annonce 10 à 20 h de travail personnel, soit 1 h 30 à 3 h entre deux séances : sans module, aucun intervalle ne dépasse 2 h 45 (carnet 2).

## 7. Les données qui circulent

Pour chaque donnée : où elle est écrite (une seule fois), où elle est reportée, et son identifiant. Le carnet qui l'écrit pose l'identifiant (`data_id`) sur la page ou le bloc, et le carnet qui la reporte le cite dans un bloc `report` : la ligne affiche alors son origine, par exemple « carnet 4 · p. 12 », calculée à la génération.

| Donnée | Écrite dans | Reportée dans | Identifiant |
|---|---|---|---|
| Météo (énergie de 0 à 10) | Ouverture de chaque carnet, et de chaque partie du carnet 7 et du carnet de route | Carnet de route (le chemin parcouru) · suivi à 6 mois | `c1.meteo` … `c7.meteo`, `c7.meteo_2`, `route.meteo`, `route.meteo_2` |
| Domaines de vie notés | Carnet 1 | Carnet 4 (note « Argent ») · carnet de route (nouvelle notation) | `c1.domaines` |
| Objectif v1, « Je m'autorise à » | Carnet 1 | Carnet 2 (boussole) · carnet 6 (pistes audacieuses) | `c1.objectif`, `c1.autorisation` |
| Ce qui pèse, héritage reçu et choisi | Carnet 1 | Carnet 2 (À lire) · carnet 4 (histoire avec l'argent) | `c1.sac_a_dos`, `c1.heritage` |
| Modèles, anti-modèles | Carnet 1 | Carnet 2 (interview) · carnet 7 (contacts d'enquête) | `c1.modeles` |
| Objectif boussole | Carnet 2 | Carnet de route (le chemin parcouru) | `c2.boussole` |
| Expériences, travail réel, travail empêché, irritants retournés | Carnet 2 | Carnet 5 (grille anti-compromis) · carnet de route (compétences prouvées) | `c2.experiences`, `c2.travail_empeche`, `c2.criteres` |
| Quatre zones, fil rouge, moteurs, verbes d'action | Carnet 2 | Carnet 3 (cartographie des énergies) · carnet 5 · carnet 6 | `c2.zones`, `c2.fil_rouge`, `c2.moteurs` |
| Compétences de vie | Carnet 2 | Carnet de route (compétences prouvées) | `c2.competences_vie` |
| Première interview | Carnet 2 (facultatif) | Carnet 7 (grille d'entretien, contacts) | `c2.interview` |
| Fil des pistes | Livrables des carnets 2 à 5 | Carnet 6 (dix pistes) | `c2.livrable` … `c5.livrable` (sur la page du livrable) |
| Cartographie des énergies | Carnet 3 | Carnet 6 · carnet de route · module création | `c3.energies` |
| Profil de fonctionnement validé | Carnet 4 (récapitulatif) | Carnet 6 · carnet de route | `c4.profil` |
| 4 seuils, tendance dominante | Carnet 4 | Carnet 5 (récapitulatif, tensions) · fiches du carnet 7 · carnet de route · module création | `c4.seuils`, `c4.tendance` |
| Grille anti-compromis (3 valeurs) | Carnet 5 | Carnet 6 · fiches et enquêtes du carnet 7 · piste A et piste B · module création | `c5.grille` |
| Limites hors argent (travail, demandes urgentes, santé, proches) | Carnet 5, avant la grille | Carnet 6 (cartographie) · carnet de route (garde-fous) | `c5.limites` |
| Entourage, proches sollicités | Carnet 5 | Carnet 6 (réponses) · carnet de route (soutiens) | `c5.entourage` |
| Retour des proches (métiers suggérés, et pourquoi) | Carnet 6 | Carnet de route (preuve extérieure) | `c6.proches` |
| 10 pistes | Carnet 6 | Séance 6 (3 pistes retenues) · carnet 7 | `c6.pistes` |
| Fiches, comptes rendus, matrice | Carnet 7 | Séance 8 (3 scénarios) · carnet de route | `c7.fiches`, `c7.enquetes`, `c7.matrice` |
| Compétences prouvées, récits | Carnet de route, partie 1 | Partie 2 · module évolution interne | `route.competences`, `route.recits` |
| Pistes A et B, feuilles de route, actions | Carnet de route, partie 2 | Module création (la piste A et sa feuille de route) · document de synthèse · suivi à 6 mois | `route.pistes`, `route.feuilles`, `route.actions` |
| Livrable de chaque carnet | Fin de chaque carnet | Document de synthèse, assemblé au fil du parcours | `c1.livrable` … `c7.livrable`, `route.livrable` |

## 8. Personnalisation dans l'app

L'app a deux usages : créer un livret de toutes pièces, puis exporter son JSON pour l'intégrer à la base, et personnaliser un livret existant.

**Créer de toutes pièces.** Les candidats naturels sont les deux modules qui manquent au carnet de route : reconversion (formation et financement) et évolution interne (argumentaire de repositionnement). Une fois le format unifié, un livret exporté de l'app s'intègre en déposant son fichier JSON dans le dossier des carnets.

**Personnaliser.** Chaque bloc du format porte une marque « fixe » ou « adaptable ». La personnalisation ne touche que les blocs adaptables.

| Pertinence | Carnets | Ce qui s'adapte | Ce qui reste fixe |
|---|---|---|---|
| Forte | Carnets 6 et 7, carnet de route et ses modules, business plan | Pistes pré-intitulées, ressources du secteur, nombre de fiches, contacts suggérés, exemples, module de projet | Gabarit, protocole, critères des fiches, définitions des seuils |
| Moyenne | Carnets 2 et 4 | Vocabulaire du secteur, situation (reconversion, évolution, retour à l'emploi), nombre de fiches d'expérience, exemples. Au carnet 4, le statut (salarié, indépendant, demandeur d'emploi), jamais de chiffres personnels | Protocole, questions franches, carte des seuils |
| Faible | Carnets 1, 3 et 5 | Au plus le prénom et les exemples. Avant la séance 1, on connaît peu la personne | Le cadre et les héritages (carnet 1), les questions du test des fonctionnements cognitifs (carnet 3 : les personnaliser biaiserait la restitution), la liste de valeurs et l'entonnoir (carnet 5) |

Deux règles valent partout :
- **les exemples viennent d'un métier voisin**, jamais du métier de la personne, sinon ils sont recopiés ;
- **ne sont jamais modifiés** : le cadre, les annonces des exercices qui touchent à l'intime, les textes réglementaires et les renvois entre carnets.

## 9. Les décisions

**Prises le 8 octobre 2026**
- Plus de carnet 0. Le carnet 1 réunit un état des lieux rapide et les héritages. Les éléments facultatifs du carnet 0 sont retirés.
- Le carnet N prépare la séance N.
- La séance libérée va au temps 2 : répartition 5 / 3 / 2.
- Le document du temps 3 s'appelle « carnet de route ».
- Les ajustements d'équilibre : fil des pistes, interview dès le carnet 2, proches sollicités en fin de carnet 5, deux semaines pour chaque intervalle de terrain, synthèse préparée au fil de l'eau, travail réel au carnet 2.

- Pas de date de bascule : le nouveau parcours vaut pour les futurs bénéficiaires.
- L'option « Initiation à l'IA » ouvre la séance 6.
- On parle d'un « test des fonctionnements cognitifs », version maison conçue et éprouvée par Lysiane Brand. La mention « MBTI » disparaît de tous les supports (carnets, programme, site, app, prompts), y compris les codes de type (ISFJ…) : c'est une marque soumise à licence. Seule exception : la certification MBTI® de Lysiane reste dans sa présentation.
- Hexa3D est abandonné et disparaît de tous les supports.

**Prises le 8 octobre 2026, suite** (détail dans `feuille-de-route-restructuration.md`, section 2)
1. **Le business plan en deux formats** : le module création du carnet de route (environ 12 pages, personnalisé en une fois) et le livret complet autonome, pour l'accompagnement après le bilan (personnalisé partie par partie dans l'app).
2. **Les retraits sont validés** : vision à 360°, quatre des huit questions de « Faire le point », arbre de vie facultatif, 3 fiches métiers obligatoires au lieu de 10.
3. **Les modules reconversion et évolution interne viennent plus tard** (`chantier-modules-s9.md`). Le carnet de route leur garde une place, et la séance 9 traite le sujet à l'oral.
4. **« Carnet 1 » à « carnet 7 » et « carnet de route » partout** (PDF, app, site), identifiants compris (`carnet-1.json`…). Le mot « chapitre » disparaît.
5. **Les cinq pièces de l'app reviennent** aux places prévues en section 5.
6. **Un pastel par temps du programme** : ciel, lilas, menthe, ciel, lilas pour les carnets 1 à 5 ; amande et rose poudré pour les carnets 6 et 7 ; jasmin pour le carnet de route.

## 10. Ce que cela implique pour le format technique

Le format unifié doit savoir décrire :
- **les blocs des PDF** que l'app ne connaît pas encore : heading, paragraphs, fields_card, annotation, link_card, numbered_lines, info_cards, frise, checklist_cards, rating_grid, star_list, page_break ;
- **les gabarits dessinés** : ligne de vie, arbre de vie, cartographie, matrice ;
- **les composants du gabarit commun** : météo, récapitulatif avec reports, protocole de sécurité, exemple contrasté, durée dans le sourcil, livrable à trois zones avec le fil des pistes ;
- **la marque « fixe / adaptable »** de chaque bloc ;
- **des identifiants stables pour les données** (par exemple `c4.seuils`). Un renvoi (« Reportez vos seuils ») pourrait alors être résolu au moment de la génération en « carnet 4, p. 12 », sans numéro de page écrit à la main.

Ces deux derniers points sont faits (PR R0 bis) : `"fixed": true` sur une page ou un bloc, toujours vrai pour le protocole, la météo et les reports ; `data_id` et le bloc `report`, dont l'origine est calculée à la génération (section 7).

Ce que Gemini a le droit de produire reste un sous-ensemble de ce que le moteur sait dessiner. La numérotation passe de `chap0`…`chap6` à des carnets 1 à 7 et un carnet de route, avec des couleurs par carnet à réattribuer.

## 11. Ce qu'il faut mettre à jour ailleurs

| Où | Quoi | Quand |
|---|---|---|
| Programme du bilan (`chapters/programme/`, texte réglementaire) | Le déroulé : séances S1 à S10, temps 1 en 5 séances, temps 2 en 3 séances, livrables. « 7 carnets de bord guidés » reste juste. Toute mention du MBTI disparaît : « test des fonctionnements cognitifs » à la place (`page_deroule.py`, `page_organisation_pedagogie.py`, `page_tarifs_financement.py`, `page_accompagnateurs.py`). Hexa3D disparaît aussi (`page_organisation_pedagogie.py:30`). L'indicateur de satisfaction « Pertinence des outils utilisés (MBTI®, Hexa3D, exercices) » (`page_indicateurs_satisfaction.py:23`) résume des enquêtes passées : retirer la parenthèse plutôt que de renommer les outils, pour ne pas fausser ce qui a été mesuré. | Fait (PR #50). Écarts relevés en R11, tranchés le 9 octobre (feuille de route, section 7) : noms des seuils et charge de travail d'une création corrigés, module création aligné sur la trajectoire « Création » (PR #69) ; la séance 9 reste telle quelle en attendant les modules reconversion et évolution interne |
| Site (dépôt `marge-de-manoeuvre`) | Voir `recap-site-parcours.md`, mis à jour en R11 (« Mise à jour du 9 octobre » : titres des carnets 5 et 6, « soutiens » au lieu d'« alliés », le seul module création). Le design system (`design-system/`) garde « Du chapitre 0 au chapitre… » et `NumeroChapitre`. | Dès que prêt, en même temps que le programme |
| Carnets PDF et app | Unification et renumérotation. Toute mention du MBTI disparaît des carnets 3, 4 et 6, du livret (`profil.py`, exemple « ISFJ ») et du prompt Gemini (`server/gemini_service.py`). La règle typographique qui ajoute « ® » après MBTI (`utils.french_typography`, `tests/test_typography.py`) et les mentions de la documentation (`CLAUDE.md`, `DA-workbook.md`, `Agent.md`, `design-system/`) sont à retirer. | Fait : unification et MBTI (PR #51), nouveaux carnets (R0 à R10), retrait des anciens carnets et du livret de compétences (R11) |
