# Feuille de route : restructuration des carnets

Ce document prépare le chantier qui suit l'unification. Il a été écrit le 8 octobre 2026 pour être repris dans une nouvelle conversation. Il complète la carte du parcours (`carte-parcours-unifie.md`), qui reste la référence pour le contenu de chaque carnet. Sa section 9, « À prendre », est remplacée par les décisions ci-dessous.

## 1. Où on en est

| Étape | État |
|---|---|
| Audit, carte du parcours, récapitulatif pour le site | Fusionnés (PR #48 et #49) |
| Programme du bilan : séances 5 / 3 / 2, test des fonctionnements cognitifs, plus de Hexa3D | Fusionné (PR #50) |
| Unification : une seule source, `workbooks/*.json`, un seul moteur, MBTI retiré des carnets | Fusionné (PR #51) |
| R0 · Socle : nommage, palette, gabarit commun, langue du PDF | Fusionné (PR #52) |
| R0 bis · Format : fixe / adaptable, identifiants de données, reports | Fusionné (PR #53) |
| R1 · Carnet 1 · L'état des lieux (`carnet-1.json`) | Fusionné (PR #54) |
| R2 · Carnet 2 · Mon parcours (`carnet-2.json`) | Fusionné (PR #57) |
| R3 · Carnet 3 · Mes fonctionnements propres (`carnet-3.json`) | Fusionné (PR #58) |
| R4 · Carnet 4 · Mon rapport à l'argent (`carnet-4.json`) | Fusionné (PR #59) |
| R5 · Carnet 5 · Valeurs et moteurs profonds (`carnet-5.json`) | Fusionné (PR #60) |
| R6 · Carnet 6 · L'exploration (`carnet-6.json`) | Fusionné (PR #61) |
| R7 · Carnet 7 · Confronter au terrain (`carnet-7.json`), en deux parties | Fusionné (PR #62) |
| R8 · Carnet de route · Décider et agir (`carnet-de-route.json`), en deux parties | PR à ouvrir |
| R10 · Livret business plan : refonte et personnalisation partie par partie | Fusionné (PR #56), mené en parallèle de R1 à R8 (le livret ne reporte aucune donnée des carnets) |
| Site (`marge-de-manoeuvre`) | À faire par l'agent du site, avec `recap-site-parcours.md`, en même temps que le programme |

**Avant chaque PR : vérifier que la précédente est fusionnée**, puis partir d'une branche à jour de `main`. Ne pas empiler les branches.

## 2. Les décisions

**Prises le 8 octobre 2026 (rappel de la carte)**
- Plus de carnet 0. Le carnet N prépare la séance N : carnets 1 à 7, puis le carnet de route au temps 3.
- Séances réparties en 5 / 3 / 2. L'option « Initiation à l'IA » ouvre la séance 6.
- Le « test des fonctionnements cognitifs », conçu et éprouvé par Lysiane Brand, remplace le MBTI partout. Seule exception : la certification MBTI® de Lysiane, dans sa présentation. Hexa3D est abandonné.
- Pas de date de bascule : le nouveau parcours vaut pour les futurs bénéficiaires.
- La charge émotionnelle suit la ligne de James Pennebaker : des questions franches, avec le protocole en trois temps (avertissement, optionnalité stricte, phrase d'ancrage).

**Prises le 8 octobre 2026, suite**
1. **Le business plan existe en deux formats.**
   - Le **module création** du carnet de route, environ 12 pages (S9 → S10). Gemini le personnalise en une fois.
   - Le **livret complet**, un outil autonome pour l'accompagnement à la création après le bilan. L'app le personnalise partie par partie si besoin, car 36 pages d'un coup sont trop pour le modèle.
2. **Les quatre retraits sont validés.**
   - La vision à 360° (elle double les domaines de vie).
   - Quatre des huit questions de « Faire le point ».
   - L'arbre de vie devient facultatif.
   - Trois fiches métiers complètes au lieu de dix : les sept autres deviennent facultatives.
3. **Les modules reconversion et évolution interne viennent plus tard.** Leur chantier est décrit dans `chantier-modules-s9.md`. D'ici là, le carnet de route prévoit leur place, et la séance 9 traite le sujet à l'oral.
4. **« Carnet N » partout, identifiants compris.** « Carnet 1 » à « Carnet 7 » et « Carnet de route » s'affichent dans les PDF, l'app et le site. Les fichiers deviennent `carnet-1.json` … `carnet-7.json`, `carnet-de-route.json` et `business-plan.json` (plus `module-creation.json`). Le mot « chapitre » disparaît.
5. **Les cinq pièces de l'app reviennent, aux places prévues par la carte.**
   - Les trois règles, dans le cadre du carnet 1.
   - Les quatre zones, au carnet 2.
   - « Ce que je me dis → ce que montrent les faits », au carnet 4.
   - La grille d'entretien et le message d'approche, au carnet 7.
   - L'arbitrage A/B, les feuilles de route à 30, 60 et 90 jours et les garde-fous, au carnet de route.

   Leur texte d'origine se retrouve dans l'historique git : `git show 1696357:server/predefined_workbooks.py`.
6. **Découpage : un socle commun, puis une PR par carnet**, dans l'ordre du parcours.

**Prises pendant R0 (8 octobre 2026)**
7. **La palette suit les temps du programme** (choisie parmi quatre palettes comparées côte à côte, toutes pastels de la DA) :
   - temps 1, teintes froides : carnet 1 ciel, carnet 2 lilas, carnet 3 menthe, carnet 4 ciel, carnet 5 lilas ;
   - temps 2, teintes chaudes : carnet 6 amande, carnet 7 rose poudré ;
   - temps 3 : le carnet de route en jasmin.
   Écartées : le cycle des pastels sans logique, et les huit teintes distinctes, qui demandaient trois pastels nouveaux (pistache, pivoine, lagon) hors de la DA.

**Prises pendant R1 (8 octobre 2026)**
8. **La page « Avant de commencer » porte la météo**, dans chaque carnet. Au carnet 1, elle porte aussi l'engagement ; à partir du carnet 2, le récapitulatif guidé. Elle n'est pas numérotée : les exercices numérotés sont ceux qu'on écrit (cinq au carnet 1).
9. **Le carnet 1 s'ouvre par une page « Bienvenue »** : les trois temps du bilan sur une frise (carnets 1 à 5, 6 et 7, carnet de route) et le lien vers l'espace Notion. Puis le cadre de travail.
10. **Les huit domaines de vie**, notation de référence du parcours, reprise au carnet de route : travail, carrière · argent, finances · santé, énergie · famille · amis, vie sociale · temps pour soi, loisirs · lieu de vie, environnement · utilité, engagements. Bornes « Pas du tout satisfaisant » et « Pleinement satisfaisant ». Le carnet 4 reprend la note « Argent, finances ».
11. **Les anciens carnets restent dans l'app jusqu'à R11**, avec « (ancien parcours) » dans leur titre quand un nouveau carnet les remplace (`chap0` et `chap1` depuis R1, `chap2` depuis R2, `chap3` depuis R3, `chap4` depuis R4, `chap5` depuis R5, `chap6` depuis R6, le livret de compétences depuis R8).

**Prises pendant R2 (8 octobre 2026)**
12. **Les parties facultatives sont hors du total d'écriture.** Au carnet 2 : l'arbre de vie (15 min) et l'interview. L'ouverture le dit, et leur sourcil porte « facultatif ».
13. **Une fiche d'expérience par page**, quatre au choix, avec des cases de 2,9 cm. La première page porte aussi la consigne et l'exemple ; une note manuscrite occupe le blanc sous les trois autres.
14. **« Je le veux / on l'attend de moi » se fait par un tri en deux colonnes** : on range chaque moteur dans l'une ou l'autre, avec le numéro de l'expérience où on l'a vu. Aucun bloc ne permet de cocher sur une ligne qu'on écrit soi-même.
15. **Pas de protocole sur les compétences de vie.** La ligne « Défis et épreuves » est facultative, et la ligne de vie se ferme juste avant par un ancrage.
16. **L'« À lire » garde trois notions** : le bagage social (l'habitus), les loyautés familiales, le travail empêché. Sont retirés : « névrose de classe », la réparation (que le carnet 4 aborde), « réussir sans trahir » (doublon du carnet 1). Les « trois outils » deviennent la page « Et vous ? », facultative. Le renvoi à l'héritage du carnet 1 est écrit, sans report à recopier.
17. **Un seul terme, « travail empêché »**, dans l'« À lire » et dans l'exercice 2 (« activité empêchée » disparaît). Le carnet de route le reprendra tel quel.
18. **L'interview tient sur deux pages**, hors temps d'écriture : préparer (report des modèles du carnet 1, un message type pour demander), puis les questions et ce que la personne en retient. Le rendez-vous reste ouvert jusqu'au carnet 7.
19. **La ligne de vie compte six moments** (trois sommets, trois vallées), avec « Ce qui m'a donné de l'énergie » et « Ce qui m'a permis de traverser ».

**Prises pendant R3 (8 octobre 2026)**
20. **Le récapitulatif du carnet 3 reporte tout ce que la carte lui donne.** Le fil rouge et le moteur « qui se voit le plus dans ma façon de travailler » ont chacun une ligne. Les quatre zones tiennent en deux colonnes : le bloc `report` accepte désormais `"columns": 2`.
21. **Six exercices.**
    - Quatre pour les quatre préférences : l'énergie (Q1 à 3), l'information (Q4 à 7), les décisions (Q8 à 11), le temps et l'action (Q12 à 15).
    - Puis « Sous pression » (Q16 et 17) et « Ce que j'en retiens pour mon travail ».
    - La cartographie des énergies (`c3.energies`) est la page « Ce que j'en retiens ». Elle s'appuie sur les quatre zones relues au récapitulatif.
22. **La consigne « Partez de situations vécues » ouvre le carnet**, en gras dans l'ouverture. L'ouverture est donc fixe, comme les pages du test.
23. **L'encadré « À savoir sur le test » ne dit ni comment le test se passe, ni qui le restitue** : « En séance 3, votre profil vous est restitué ». Il est à compléter quand ces modalités seront précisées (section 7).
24. **Q11 garde sa question d'origine, rendue épicène** (« la dernière critique qui vous a fait mal »). La version du rapport, « qu'y avait-il de juste, d'injuste ? », pousserait vers l'analyse, que cette partie du test observe. Charge moyenne : une clôture, « Aujourd'hui, ce que j'en garde, c'est… », sans le protocole complet.
25. **Un seul exemple contrasté pour les 17 mises en situation**, sur un sujet absent du carnet : le choix d'un restaurant. Q16 n'a pas d'exemple, car ses quatre réactions équilibrées en tiennent lieu : un exemple de plus orienterait la réponse. « Ce que j'en retiens » a le sien (architecte).
26. **Une question du test qui demande deux choses a deux cases.**
    - Q3 : « Spontanément, je… », puis « La fois où j'ai dû faire l'inverse, et ce que cela m'a coûté ».
    - Q14 et Q15 : une échelle de 1 à 5 aux bornes concrètes (« Rien de prévu / Tout est réservé », « Ouvrir les possibles / Trancher, conclure »), puis un « pourquoi ».
    - Q16 : ce que voient les proches, puis « Ce qui m'aide à revenir à moi ».
27. **La fin du carnet 3 adapte une zone** : « Les questions où j'ai hésité, à aborder pendant la restitution » remplace « À aborder en séance ». Le profil validé ne s'écrit pas au carnet 3, mais une seule fois, au récapitulatif du carnet 4 (`c4.profil`).

**Prises pendant R4 (8 octobre 2026)**
28. **Le profil validé s'écrit en mots, une seule fois**, au récapitulatif du carnet 4, dans une carte fixe « Après la restitution » (`c4.profil`) : le profil (les quatre préférences du test, avec ses mots), les deux forces où la personne se reconnaît le plus (la Q1 de l'ancien récapitulatif, que le carnet de route reporte), « En séance 3, j'ai vu que… » et la question pont : « Mon profil se voit dans mes choix d'argent (dépenser, épargner, négocier) quand… ». Le champ « 4 lettres » du rapport est écarté (aucun code de type). La page reporte aussi deux lignes de la cartographie des énergies (`c3.energies`).
29. **Sept exercices, 2 h.** Votre situation (10 min), votre histoire avec l'argent (20 min, deux pages), premières expériences et idées reçues (15 min, deux pages), l'argent et votre projet (10 min), vos quatre seuils (20 min), vos tendances (15 min, deux pages), la synthèse (10 min).
30. **L'histoire avec l'argent tient en quatre questions ouvertes**, sous le protocole complet : l'argent dans l'enfance, ce qu'on en disait et taisait, qui gagnait et décidait (les deux questions sur le genre y sont fusionnées), puis la question franche sur le pouvoir et la dépendance, posée au passé, avec un renvoi vers la séance. Un tri « De cette histoire, je garde… / Je laisse… » précède l'ancrage.
31. **Le souvenir marquant (exercice 3) suit la charge moyenne**, comme Q11 au carnet 3 : une question franche facultative (« Un mot suffit, ou laissez la case vierge »), puis une clôture, « Avec le recul, ce souvenir m'apprend que… ». Pas de second protocole complet.
32. **« Ce que je me dis → Ce que montrent les faits » est une page composite** : l'ancien encadré des idées reçues sert de matière, puis trois rangées de deux cases et un exemple. Le gabarit `two_columns` de l'app, qui remplit la page et ne montre ses exemples qu'en infobulle, est écarté.
33. **Un choix exclusif en mots se fait par une `rating_grid` d'une ligne**, aux valeurs écrites (« En sécurité / En tension / En vigilance »), comme « Ma décision » au livret business plan, puis « Parce que… ». La note « Argent, finances » du carnet 1 est reportée, puis renotée en une phrase.
34. **La carte des seuils est fixe**, avec son paragraphe (calcul sur une feuille à part, seul le total est reporté). Les définitions sont dans les libellés : minimum vital (charges essentielles, sans marge), minimum sécurisant (avec une marge pour les imprévus), revenu cible (ce que vous visez à terme), durée acceptable d'une baisse (combien de temps vivre avec moins qu'aujourd'hui, sans passer sous le minimum vital). Unité : « En euros nets par mois, pour vous : votre part des charges du foyer. Une fourchette suffit. La durée, en mois. » Puis « Ce que j'accepte pendant la transition / Ce que je n'accepte pas ».
35. **L'argent et votre projet** : une grille d'aisance de 1 à 5 sur cinq situations (demander une augmentation, négocier un salaire à l'embauche, fixer un prix, parler de son salaire à un proche, réclamer ce qu'on me doit), puis deux cases côte à côte, fixes : « La situation la plus difficile pour moi, et pourquoi » et « Ce que je n'ose pas demander, viser ou négocier aujourd'hui », enfin le retournement « Je ne veux plus accepter un poste seulement pour… ». L'ouverture de l'exercice renvoie à l'« À lire » du carnet 2 : le bagage social « peut retenir de demander une augmentation ».
36. **Huit tendances aux noms neutres** : la sécurité, le mérite, l'indépendance, la générosité, l'évitement, l'ambition, le plaisir, la réparation. On en coche deux ou trois au plus. `c4.tendance` tient en quatre cases : la tendance dominante, la réponse à sa question clé, quand elle aide, quand elle freine. Une note manuscrite rappelle qu'une tendance n'est ni un défaut ni une qualité. La consigne renvoie aux moteurs du carnet 2 (la sécurité, la reconnaissance) et annonce la relecture au carnet 5.
37. **Retirés du carnet 4** : la question « cette piste » (les seuils s'appliquent aux fiches du carnet 7), le seuil plancher (doublon du minimum sécurisant), la question sur le niveau de sécurité nécessaire (doublon des seuils), « Associez-vous gagner de l'argent et beaucoup travailler ? » (doublon du mérite), la tension entre sécurité et utilité (aux tensions du carnet 5). La fin de carnet adapte une zone : « À aborder en séance : ce que je préfère dire de vive voix, une question non tranchée » (les deux zones proposées par le rapport en une).
39. **Les questions plus franches du rapport entrent dans des amorces existantes** : « ce que l'argent a coûté à votre famille, ou ce qu'il lui a permis » (histoire, Q1), « Gagner davantage, ou plus que mes parents, me gênerait parce que… » (synthèse, pour les loyautés du carnet 2). « Mon « assez » est plutôt un chiffre, ou une sensation difficile à atteindre » garde l'ancienne question de la synthèse sans doubler le minimum sécurisant. « Ce que j'en faisais / Ce que j'en fais aujourd'hui » a deux cases.
38. **Les noms des seuils suivent la carte et le livret business plan**, pas encore le programme. Le programme parle, en séance 4, de « revenu vital », de « revenu sécurisant » et de « délai de trésorerie ». À aligner au lot programme et site (section 7).

**Prises pendant R5 (8 octobre 2026)**
40. **Huit exercices, 2 h 15.** Alignement (15 min), désalignement (20 min, deux pages), choix difficiles (10 min), la liste de valeurs (10 min), hiérarchiser (10 min), vos tensions (10 min), la grille anti-compromis (25 min, deux pages), l'entourage et les proches (10 min). Avant eux, le récapitulatif (10 min) et une page « À lire » (5 min). L'ouverture découpe en trois fois : les situations (1 h), la liste, la hiérarchie et les tensions (30 min), puis la grille, les proches et la fin (45 min). Elle dit aussi que la question aux proches peut partir dès le début.
41. **Le récapitulatif reporte les quatre seuils et la tendance dominante** en deux colonnes, sans les commenter. Puis une carte « Après la séance 4 » : « Ce que l'argent protège pour moi », avec une aide qui renvoie à la liste de valeurs, et « En séance 4, j'ai vu que… ».
42. **Une page fixe « À lire · Valeur, moteur, besoin »** définit les trois mots avant les exercices. Une valeur, c'est ce qui compte pour vous (l'autonomie). Un moteur, c'est ce qui vous fait avancer, comme au carnet 2 (apprendre). Un besoin, c'est la condition concrète qui permet de vivre une valeur (choisir l'ordre de ses dossiers). La page porte aussi la frise de l'entonnoir (situations, liste, hiérarchie, tensions, grille) et la règle « Ne cherchez pas les valeurs les plus « belles » », reprise en gras dans l'ouverture.
43. **Alignement et désalignement renvoient par écrit au carnet 2** : les sommets et les vallées (exercice 5), et ce qui coûtait dans les expériences (exercice 1). La ligne de vie n'a pas d'identifiant : le renvoi est un paragraphe fixe.
    - L'alignement tient en trois lignes : « La situation » · « Ce que j'y trouvais » · « La valeur respectée ». Puis vient « Je suis à ma place quand… ». « Ce qui me donnait de l'énergie », proposé par le rapport, est écarté : la ligne de vie le demande déjà.
    - Le désalignement prend le protocole complet, sur deux pages. Trois situations sont retournées en besoin (« Donc, dans mon prochain poste, j'ai besoin de… »). La question franche a deux cases, « Une fois où j'ai agi contre l'une de mes valeurs » et « Ce qui m'a fait agir ainsi ». L'ancrage ferme l'exercice.
44. **Choix difficiles : un seul choix, sur une page, renommée « Ce que vos choix ont tranché »**. La Q8 du carnet 3 s'appelle déjà « La dernière place ». Les amorces du rapport deviennent deux cases : « J'ai choisi…, qui me permettait de garder… » et « J'ai renoncé à…, qui me permettait de garder… », après « Le choix, en quelques mots » et « La valeur qui l'a emporté ». La version courte du protocole suit la convention de charge moyenne : une question franche facultative en deux cases (« Le choix que je regrette encore » · « Ce qu'il dit de ce qui compte pour moi »), puis la clôture fixe « Avec le recul, ces choix m'apprennent que… ». Il n'y a pas de bloc protocole. « Je referais ce choix », une question fermée, est rouvert.
45. **La liste de valeurs compte 81 valeurs**, en neuf familles de neuf, et la page est fixe.
    - Retirés : les doublons (Responsabilité, Fiabilité et Engagement en double), les quasi-doublons (Confort, Esthétique) et un quasi-synonyme par famille (Choix, Continuité, Compétence, Soutien, Responsabilité sociale, Évolution, Joie, Structure, Capacité à orienter). Ces derniers retraits laissent la place des trois champs libres.
    - Ajoutés : les pôles des tensions (Rémunération juste, Appartenance, Affirmation de soi, Discrétion, Qualité de vie, Protection de soi, Changement, Stimulation), plus Santé et Constance. « Latitude » remplace « Marge de manœuvre ».
    - Les titres de famille tiennent sur une ligne. Les trois champs libres tiennent sur une ligne (`fill_in_card`, « Une valeur me manque : »).
    - La consigne fixe 15 à 20 valeurs et renvoie aux exercices 1 à 3, aux moteurs (carnet 2) et aux cinq mots pour le futur travail (carnet 1).
    - Pas d'exemple contrasté : il orienterait le choix, comme pour la Q16 du carnet 3.
46. **Hiérarchiser : dix lignes numérotées en deux colonnes**, « Mes cinq valeurs prioritaires » (01 à 05), puis « Les cinq suivantes » (06 à 10). On classe une fois, sans recopier une liste de cinq. Le test des six mois (« Gardez les trois dont l'absence vous ferait partir ») définit le « non négociable » et envoie les trois valeurs dans la grille : elles ne s'écrivent nulle part ailleurs. Puis « La valeur que je coche surtout parce qu'elle est attendue de moi » · « Attendue par qui ».
47. **Treize tensions, une seule détaillée.**
    - La tension sécurité / utilité vient du carnet 4 (décision 37). « Loyauté / besoin de changement » devient « Loyauté / changement », et chaque pôle se trouve dans la liste.
    - La carte détaillée : la tension, une situation où elle est apparue, « Jusqu'ici, je privilégie… » · « … au détriment de… », le compromis acceptable, et la question franche facultative « La valeur que j'affiche et que je ne m'accorde pas ». Elle est fixe.
    - « Ce que je n'arrive pas encore à trancher » passe dans la zone « À aborder en séance » de la fin de carnet. La consigne renvoie aux seuils et à la tendance, reportés en début de carnet.
48. **La grille anti-compromis tient sur deux pages.**
    - « Relire avant d'écrire » : un report en deux colonnes, les moteurs « je le veux » et les irritants déjà retournés en critères, « donc, mon poste devra… » (carnets 1, 2 et 3). Puis des renvois écrits à ce qui tient encore et aux modèles et anti-modèles (carnet 1, exercices 1 et 5), et aux besoins de l'exercice 2. Puis la carte « Mes limites, hors argent », reprise de l'app : au travail, face aux demandes urgentes ou non rémunérées, pour la santé, pour les proches. Elle a un nouvel identifiant, `c5.limites`. La limite d'argent, ce sont les seuils.
    - La grille est un tableau fixe (`c5.grille`) : une colonne par valeur, et cinq lignes (la valeur ; d'où elle me vient ; la condition observable ; le signal d'alerte, ce que je remarque quand elle manque ; la question à poser en entretien). Les renvois à l'héritage du carnet 1 et à l'« À lire » du carnet 2 (le bagage social) aident à trouver d'où vient une valeur.
    - Écartées : l'échelle « respectée aujourd'hui » du rapport (P3), que le signal d'alerte couvre, et « Je la garde parce que… », que la ligne « attendue de moi » couvre.
49. **L'entourage et les proches tiennent sur une page** (`c5.entourage`, posé sur la page).
    - D'abord la question de la carte, fixe. Puis deux tableaux, une case par information, comme le proposait le rapport 00 : « Mes soutiens · Ce que cette personne peut m'apporter · Question envoyée le » (quatre lignes ; la question part à trois d'entre eux, sans parler des pistes), puis « Les regards critiques · Ce que cette personne craint · Ce que je choisis de lui dire » (deux lignes).
    - Écartée : la question franche du rapport 00 (« la personne dont je redoute la réaction »). La carte dit « en quelques lignes », et la zone « À aborder en séance » l'accueille.
50. **Les questions plus franches du rapport sont toutes placées.**
    - Agir contre une valeur : au désalignement.
    - Le choix regretté : aux choix difficiles.
    - La valeur affichée : aux tensions.
    - La valeur attendue : à la hiérarchie.
    - « Ce que je ressens quand elle manque » devient, en termes observables, le signal d'alerte de la grille.
51. **Retirés de l'ancien carnet 5.**
    - Les synthèses des exercices 1 et 2 : chaque situation nomme sa valeur.
    - Le second choix difficile : la question franche le remplace.
    - La Q2 de « Incarner » (« Dans quelles situations passées… ») : elle double les exercices 1 à 3.
    - Le second détail de tension.
    - Dans la synthèse : « Je perds de l'énergie quand » (la cartographie des énergies, reportée) et « Ce qui compte vraiment pour moi » (la grille).
    - « Je veux davantage / moins » : les conditions de la grille et les critères le disent déjà.

**Prises pendant R6 (8 octobre 2026)**
52. **Cinq exercices, 2 h.**
    - Avant d'eux, la météo et le récapitulatif (10 min).
    - Puis votre cartographie (20 min), le retour de vos proches (20 min, deux pages), explorer les ressources (10 min), dix pistes (40 min, deux pages) et « Avant de choisir » (10 min).
    - La fin de carnet prend 10 min.
    - L'ouverture découpe en trois fois : le récapitulatif et la cartographie (30 min), les proches et les ressources (30 min), puis les pistes et la fin (1 h). Elle ajoute : « Une réponse de vos proches manque ? Relancez dès le début. » (rapport 06 : les sollicitations dès l'ouverture).
    - La promesse de couverture devient « Dix pistes, avant d'en choisir trois. » L'ancienne, « Des pistes confrontées au réel », annonçait le carnet 7.
53. **Les trois valeurs ne s'écrivent qu'une fois dans le carnet.** Le récapitulatif les reporte, une ligne par valeur (`c5.grille`), puis pose deux cases : « Ce que la séance a confirmé » et « Ce qu'elle a déplacé ». La cartographie reporte leurs conditions, pas les valeurs.
54. **La cartographie est une page de reports**, sur deux colonnes.
    - Les reports : le profil, en mots, et les deux forces (`c4.profil`) ; ce qui me recharge et « Pour mon énergie, mon poste devra… » (`c3.energies` : le critère retourné plutôt que le coût, que le rapport 06 jugeait resté à l'état de constat) ; les moteurs à moi (`c2.moteurs`) ; l'objectif boussole (`c2.boussole`, comme le demande le rapport 01) ; les trois conditions (`c5.grille`) ; les limites hors argent (`c5.limites`).
    - Les quatre seuils (`c4.seuils`) vont dans une seconde carte, « À garder pour vous », sans commentaire. La consigne dit de les masquer si l'on montre la page.
    - La page se ferme sur une question, fixe : « Le travail qui me ressemble, quel que soit le métier, c'est… ». Elle renvoie à la journée dans cinq ans (carnet 3, Q7). L'exemple est dans la question, faute de place pour un exemple contrasté.
55. **Le retour des proches tient sur deux pages, sous le protocole complet.**
    - L'avertissement porte le cadre : « vous choisissez ce que vous y notez, et ce que vous en partagez ».
    - Un tableau de trois lignes : le prénom, les métiers suggérés, « Ce qui, chez moi, l'y fait penser ». Le prénom est recopié avec un renvoi écrit au carnet 5 (exercice 8), sans bloc `report` : trois prénoms ne justifient pas une carte de plus.
    - Le tableau porte un nouvel identifiant, `c6.proches`. Le carnet de route le reprendra comme preuve extérieure (rapport 07).
    - La seconde page : « Ce qui me parle vraiment » et « Ce qui ressemble plutôt à ce qu'on attend de moi » ; la question franche en deux cases, « La suggestion qui m'a le plus fait réagir » et « Ce qu'elle a touché chez moi » ; l'ancrage.
56. **Les ressources sont l'exercice 3, avant les pistes.**
    - Les liens ont été vérifiés le 8 octobre 2026 :
      - « Into the Job » a disparu d'Ausha (erreur 404) et laisse place au podcast « Sur le métier » ;
      - MétierScope passe sur francetravail.fr, l'ONISEP sur `/metier`, et le CIDJ sur sa nouvelle page des centres d'intérêt.
    - L'adresse courte est écrite entre parenthèses dans la description, pour l'impression.
    - Six lignes, « Les métiers que je repère », sans exemple : il orienterait le repérage.
    - L'immersion (PMSMP), le guide d'entretien et les salaires vont au carnet 7.
57. **Les dix pistes tiennent sur deux pages**, en deux tableaux numérotés R1 à R5 et A1 à A5, pour en parler en séance.
    - Une piste réaliste est directe, avec vos compétences actuelles, ou passerelle courte, après une formation courte : le vocabulaire du programme, que la séance 8 reprend pour classer les pistes. Une piste audacieuse ne tient compte d'aucune contrainte.
    - Les colonnes : « D'où elle vient », puis « Ce qui m'attire » pour les réalistes, « Ce qu'elle dit de ce que je cherche » pour les audacieuses.
    - Le report de la première page donne le fil des pistes (`c2.livrable` à `c5.livrable`) et « Je m'autorise à » (`c1.autorisation`). La consigne renvoie aussi aux modèles (carnet 1, exercice 5), à l'interview (carnet 2), aux proches et aux ressources.
    - `c6.pistes` est posé sur le tableau des réalistes.
58. **« Avant de choisir » (exercice 5)** : on relit les dix pistes, la cartographie sous les yeux, puis on note les trois favorites (la piste, pourquoi elle, ce qui m'en fait douter). C'est un premier tri face aux critères ; la confrontation complète se fait sur les fiches du carnet 7. Puis la question franche facultative, « Le métier que je n'ai jamais osé envisager » et « Ce qui m'en empêche ». Enfin la clôture, « Ce que je garde de mes pistes audacieuses, même si je ne les exerce pas… ». La séance 6 tranche.
59. **La fin de carnet n'a pas de fil des pistes** : il s'arrête au carnet 6, qui l'utilise.
    - La zone adaptée : « À aborder en séance : une piste que je n'ose pas défendre, une suggestion qui me gêne ».
    - Les engagements : repérer une personne pour chaque favorite (le contact se prend au carnet 7), et apporter le carnet.
60. **L'option « Initiation à l'IA » est une ligne d'engagement adaptable** : « Si ma séance 6 s'ouvre par l'initiation à l'IA, j'apporte deux tâches de mon travail, actuel ou passé, à essayer ensemble. » « Actuel ou passé » vaut aussi entre deux emplois. Elle est hors temps d'écriture, et l'app peut la retirer.
61. **Retirés de l'ancien carnet 6.**
    - Les tensions du récapitulatif : elles restent au carnet 5.
    - Les fiches métiers : elles vont au carnet 7.
    - Trois engagements : « une fiche par semaine », « confronter chaque piste » et « contacter un professionnel ».
    - Deux questions plus franches du rapport sont écartées :
      - « La valeur que j'ai le plus sacrifiée » double « agir contre une valeur » et le choix regretté du carnet 5 ;
      - « Ce que je ne veux plus revivre, donc ma piste doit… » est inutile : les irritants sont retournés aux carnets 1 à 3, et la cartographie reporte le critère d'énergie du carnet 3.
    - Deux autres vont au carnet 7 : « Le compromis que cette piste me demande, et si je l'accepte », et « Ce qui pourrait me faire repousser ce contact ».

**Prises pendant R7 (8 octobre 2026)**
62. **Un seul fichier en deux parties, et une fin par partie.**
    - `carnet-7.json` déclare `parts` (« Confronter vos pistes », « Tirer les leçons du terrain ») : l'app le personnalise partie par partie, comme le livret business plan. La couverture, l'ouverture et le dos restent hors parties.
    - Chaque partie prépare une séance, donc chacune finit par un livrable validé en séance : « Votre premier livrable » (vos trois fiches, vos enquêtes lancées) avant la séance 7, « Votre second livrable » (`c7.livrable` : les retours d'enquêtes et la matrice) avant la séance 8.
63. **Six exercices, numérotés à la suite : 1 h 45, puis 2 h.**
    - Partie 1 : la météo et le récapitulatif (10 min), vos trois fiches (1 h 10 : où chercher, 10 min, puis 3 × 20 min), préparer vos enquêtes (20 min : la grille, puis les contacts), la fin de la partie 1 (5 min).
    - Partie 2 : « Avant de reprendre », la météo et le récapitulatif (10 min), vos comptes rendus (45 min : 15 min, puis 30 min pour deux), ce que le terrain vous a appris (15 min), la matrice de faisabilité (30 min), ce que vous acceptez (10 min), la fin de carnet (10 min).
    - La promesse de couverture est celle de l'ancien carnet 6, que l'audit jugeait non tenue : « Trois pistes, confrontées au réel. » L'ouverture pose la règle en gras : « Une enquête n'est pas une candidature : vous demandez un regard, pas un poste. »
    - Le découpage de l'ouverture donne deux semaines par partie, et fait commencer la partie 1 par le récapitulatif et les contacts (20 min) : un rendez-vous prend du temps. C'est la même logique que les sollicitations des proches dès l'ouverture du carnet 6 (rapport 06).
64. **Une météo par partie.** La seconde a un nouvel identifiant, `c7.meteo_2` (carte, section 7) : le chemin parcouru du carnet de route aura un point par intervalle.
65. **Le récapitulatif de la séance 6** est un tableau, « La piste retenue, et son numéro · Pourquoi elle », suivi de « Ce que la séance a déplacé ».
    - Les dix pistes sont citées par un renvoi écrit (carnet 6, exercice 4), comme les prénoms au carnet 6 : trois intitulés tiennent dans une colonne.
    - Les sept autres « restent dans votre carnet 6 : le terrain en fera peut-être revenir une ».
66. **Salaires et débouchés passent avant les fiches**, sur une page « Où chercher » qui ouvre l'exercice 1 : on cherche, puis on note, et le salaire ne s'écrit qu'une fois.
    - La page porte « Ma zone de recherche » en trois cases d'une ligne : les villes ou le département, le trajet que j'accepte, le télétravail.
    - Deux liens France Travail, vérifiés le 8 octobre 2026 :
      - Data Emploi : les offres, les salaires proposés et les embauches d'un métier, jusqu'au bassin d'emploi ;
      - l'enquête Besoins en main-d'œuvre.
      L'ancienne page « marché du travail » renvoie désormais vers MétierScope.
    - L'immersion (Immersion facilitée, la PMSMP) : « avec une convention : parlons-en en séance ».
    - Puis la définition fixe des valeurs de la grille.
    - Chaque fiche note la rémunération observée et sa source, et les débouchés dans la zone. Aucun chiffre n'est écrit dans le carnet.
67. **Une fiche par page, et trois rangées de critères fixes**, car une quatrième ne tient pas (mesuré).
    - Ce que fait le métier, adaptable : la piste et son numéro, ses missions d'après mes recherches (deux lignes), puis « Ce que je sais déjà faire » et « Ce qui me manque ».
    - « Face à mes critères » est une `rating_grid` : « Valeur 1 (2, 3) : condition remplie » et « Mon minimum est atteint », sur une seule échelle, « Oui / À terme / Non / À vérifier ». « Mon minimum » est le minimum sécurisant ; « à terme », il est atteint dans la durée acceptable d'une baisse. « À vérifier » devient une question d'enquête.
    - Puis la rémunération observée, sa source (deux cases d'une ligne), les débouchés dans ma zone (une phrase, deux lignes), ce qui me rechargerait, ce qui me coûterait, ce qu'il me reste à vérifier, auprès de qui.
    - « Ce que cette piste dit de ce que je cherche » n'est pas redemandé : c'est une colonne des pistes audacieuses du carnet 6, citée par un renvoi.
    - `c7.fiches` est posé sur la fiche 1.
68. **La question franche du compromis sort des fiches.** Elle est posée une fois, après le terrain, quand le compromis est concret : à l'exercice 6, « Ce que vous acceptez ».
    - « La piste », puis « Le compromis qu'elle me demande » · « À quelle condition je l'accepterais ».
    - Puis la question franche facultative « La piste qu'il me coûterait le plus de lâcher » · « Ce qu'elle représente pour moi ».
    - Enfin la clôture « Avec le recul, le terrain m'apprend que… ».
69. **La grille d'entretien compte sept questions communes.**
    - De l'app : le quotidien réel, ce qui change dans le métier, la façon d'y entrer.
    - De l'interview du carnet 2 : le parcours, ce qu'on aime, les difficultés, le conseil.
    - En plus : la rémunération pour débuter, et « Qui d'autre me conseilleriez-vous de rencontrer ? ».
    - L'IA y entre pour tout le monde, plutôt qu'en ligne sur les fiches : « Qu'est-ce qui change dans votre métier : les besoins, les recrutements, ce que l'IA déplace ? »
    - Puis le report des trois questions d'entretien de la grille (`c5.grille`), et un renvoi à ce qu'il reste à vérifier sur chaque fiche.
70. **Les contacts.**
    - Trois personnes à solliciter dans les dix jours, une par piste si possible : les modèles (carnet 1), la personne de l'interview (carnet 2), celles repérées en fin de carnet 6, par des renvois écrits. La page se fait « dès le début de la partie 1, sans attendre vos fiches ».
    - Le message d'approche du rapport 06 finit sur « seulement votre regard sur ce métier » (« un regard de professionnel » s'accordait).
    - Un tableau : la personne, pour quelle piste, comment la joindre, sollicitée le, rendez-vous le.
    - La charge moyenne suit la convention du carnet 4 : « Ce qui pourrait me faire repousser ce contact » (facultatif), puis « Pour me lancer, je commence par… ».
71. **Un compte rendu par entretien**, sur deux pages (le premier, puis le deuxième et le troisième). `c7.enquetes` est posé sur le premier.
    - La personne, son métier, la piste, la date (quatre cases d'une ligne) ; ce qui confirme ; « Ce qui contredit, ou m'étonne » ; ce que j'ai appris sur mes critères ; la suite.
    - Une immersion ou un salon se notent de la même façon.
72. **Ce que le terrain vous a appris** reprend les trois lignes de l'app (l'accès, le quotidien et le rythme, la rémunération et les débouchés), en « ce que j'imaginais » et « ce que le terrain montre ».
    - Les sept pistes non retenues trouvent leur place ici : une carte facultative « Une piste apparue ou revenue » (la piste, d'où elle vient, ce qui m'y attire).
    - Pas de quatrième fiche dans le PDF : l'app peut en ajouter.
73. **La matrice de faisabilité est un tableau fixe** (`c7.matrice`) : une colonne par piste, cinq lignes. Une phrase la définit d'abord : « Une piste est faisable quand vos compétences, le marché et les débouchés de votre zone le permettent, tout de suite ou après une passerelle. »
    - Les trois du programme : mes compétences, le marché, les débouchés dans ma zone.
    - Puis « Ce qu'il faudrait pour y aller : formation, délai, coût » et « Mes critères après le terrain ».
    - La personne ne classe pas ses pistes : les trois familles (pistes directes, passerelles courtes, angles morts) se font en séance 8.
74. **Pas de protocole complet au carnet 7** : le rapport 06 n'y voit aucune charge forte. Deux points de charge moyenne suivent la convention du carnet 4 (les contacts, l'exercice 6).
75. **Le moteur garde dans la carte les valeurs en mots d'une `rating_grid`.** « À vérifier », et « En vigilance » au carnet 4, en sortaient de quelques points. Seules changent les pages à échelle en mots : carnet 4 p. 4, business plan p. 41 et 46. Un test le vérifie.
76. **Retirés des fiches de l'ancien carnet 6.**
    - Sept des dix fiches : l'app peut en ajouter.
    - « Pourquoi ce métier vous attire » : déjà au carnet 6, et « Pourquoi elle » au récapitulatif.
    - « Missions et compétences utiles » : scindée en trois cases.
    - Du rapport 06, sont écartés « Ce que je garde de cette piste, même si je ne l'exerce pas » (déjà la clôture du carnet 6) et les exemples du guide de haute montagne et de la médiation culturelle, remplacés par six exemples de métiers nouveaux.
77. **Second passage sur l'audit** (demandé par Nicolas).
    - Corrigé :
      - une case par information : la rémunération et sa source, la personne et son métier, la piste et son compromis, les trois éléments de la zone de recherche ;
      - les débouchés, qui appellent une phrase, prennent deux lignes ;
      - les contacts se sollicitent dès le début de la partie 1 ;
      - la grille d'entretien pose le cadre de l'enquête (« Vous n'avez pas à raconter votre bilan : vous choisissez ce que vous dites de vous », rapport 06, cadre) ;
      - la matrice définit la faisabilité (synthèse, constat 7 : une phrase avant chaque notion).
    - Écarté, avec la raison :
      - un « parce que » sous la grille de chaque fiche : la page est pleine. Les réponses « non » et « à vérifier » vont dans « Ce qu'il me reste à vérifier », puis dans les comptes rendus et la ligne « Mes critères après le terrain » de la matrice, et la séance 7 les reprend ;
      - une page « Vos pistes face à vos critères » en partie 1 (rapport 06, P2) : la même rangée de critères sur chaque fiche et la matrice de la partie 2 en tiennent lieu ;
      - une case « Mon message, avec mes mots » (l'app) : le message est un modèle, que l'app peut adapter au secteur ;
      - un intitulé de piste à 1 cm (rapport 06, P3) : 0,85 cm, la hauteur d'une ligne d'écriture, comme dans les autres carnets.

**Prises pendant R8 (8 octobre 2026)**
78. **Les « angles morts » sont des pistes que vous ne regardiez pas** (Nicolas), apparues en chemin : un entretien, un proche, une compétence transférable. Le récapitulatif de la séance 8 les définit, fixe, à côté des pistes directes (avec vos compétences actuelles) et des passerelles courtes (après une formation courte).
79. **Un seul fichier en deux parties, comme le carnet 7.**
    - `carnet-de-route.json` déclare `parts` (« Prouver et préparer le choix », « Décider et agir »). La couverture, l'ouverture et le dos restent hors parties.
    - Chaque partie finit par son livrable. « Votre premier livrable », « Vos preuves » : le profil, les compétences prouvées, les deux récits, validés en séance 9. « Votre carnet de route » (`route.livrable`) : les feuilles de route A et B et les premières actions, qui entrent en séance 10 dans le document de synthèse co-rédigé.
    - La couverture : « Décider *et agir.* », promesse « Vos preuves, deux pistes, un plan daté. » Ni la couverture ni l'ouverture n'ont de grand numéro.
80. **Neuf exercices, numérotés à la suite : 1 h 30, puis 1 h 45.**
    - Partie 1 : la météo et le récapitulatif (10 min), votre profil (10 min), vos compétences prouvées (20 min, puis 15 min), deux récits d'action (2 × 15 min), la fin de la partie 1 (5 min).
    - Partie 2 : la météo et le récapitulatif (10 min), piste A et piste B (2 × 10 min), vos feuilles de route (15 min, puis 10 min), le module de votre projet (5 min), vos premières actions (10 min), garde-fous et soutiens (10 min), le chemin parcouru (2 × 10 min, suivi compris), la fin de carnet (5 min). Le module lui-même s'ajoute.
    - L'ouverture dit en gras ce qui se montre (le profil, les compétences, les récits) et ce qui reste à la personne (les seuils, les garde-fous, le chemin parcouru), comme le demandait le rapport 07. La page des pistes le rappelle (« masquez vos seuils »), et le premier livrable aussi.
81. **Le récapitulatif de la séance 8** : la matrice est citée par un renvoi écrit (carnet 7, exercice 5), puis un tableau des trois scénarios (« Le scénario, en quelques mots » · « Sa famille ») et trois cases : « Le scénario vers lequel je penche » · « Pourquoi lui » · « Ce qui me fait encore hésiter ». Dans tout le carnet, les scénarios se désignent « Scénario 1 » à « Scénario 3 ».
82. **Le profil, en une page de reports** : le profil en mots et les deux forces (`c4.profil`), ce qui recharge, ce qui coûte, le besoin et le critère retourné (`c3.energies`), sans code de type. Une seule question : « Dans le scénario vers lequel je penche, mon profil est un atout quand… ». Les moteurs (`c2.moteurs`) ne sont pas reportés : la grille du carnet 5 les a relus, et le carnet de route reporte ce qu'elle en a tiré, les trois valeurs et leurs conditions.
83. **Les compétences prouvées sont un tableau fixe de cinq lignes** (`route.competences`).
    - Les colonnes : la compétence (un verbe, un objet), où je l'ai prouvée, le résultat ou la trace, le niveau de 1 à 4, l'envie (oui, plutôt, non).
    - Le niveau est une colonne (Nicolas) : une `rating_grid` éloignerait la compétence de son niveau et prendrait une page de plus. Les paliers du livret (guidé, autonome, améliorateur, référent) s'accordaient : ils deviennent des verbes, apprendre, faire, améliorer, transmettre, définis au-dessus du tableau.
    - Le tableau part de renvois écrits au carnet 2 (exercices 1, 3 et 6) : une fiche d'expérience est trop longue pour un report.
84. **« Ce que les autres voient »** complète le tableau : le report du retour des proches (`c6.proches`, la preuve extérieure du rapport 07), l'épreuve du miroir (« Ce qu'on vient souvent me demander, et que je fais sans y penser »), la compétence qui ouvre la porte de chaque scénario (le rapport 07 le demandait pour les pistes réalistes du carnet 6 : les scénarios en sont issus), puis la question franche facultative « La compétence que je sous-estime » · « La preuve que je la maîtrise ».
85. **Deux récits d'action, fixes** (`route.recits` sur le premier) : la situation et ce qui posait problème, le signal qui m'a fait agir (plus de « déclic »), ce que j'ai fait pas à pas, le résultat, « Ce récit prouve que je sais… ». Le premier porte sur un savoir-faire. Le second se passe avec d'autres personnes, ou c'est « une fois où vous avez cru ne pas y arriver » : la question plus franche du rapport 07 devient une consigne. Puis chaque récit en trois phrases, pour un entretien. Le renvoi aux sommets de la ligne de vie (carnet 2, exercice 5) et à l'alignement (carnet 5, exercice 1) est écrit.
86. **Une météo par partie**, comme au carnet 7 : la seconde a un nouvel identifiant, `route.meteo_2` (carte, section 7). Le récapitulatif de la séance 9 tient en deux cases : « Ce que la séance a tranché » · « Ce qui reste ouvert ».
87. **Piste A, piste B, sur deux pages.**
    - La définition est fixe, avec les mots du programme : « Piste A, votre projet d'élan : le projet qui vous attire le plus. Piste B, votre refuge ou votre tremplin : le plus sûr, ou celui qui prépare la piste A. » « Transmission » disparaît.
    - Les critères sont reportés, pas redemandés : les trois valeurs et leurs conditions (`c5.grille`), les quatre seuils dans « À garder pour vous » (`c4.seuils`).
    - Un premier tableau A · B, adaptable (l'app y écrit les pistes pré-intitulées) : l'intitulé et son numéro de scénario, ce qui m'y attire, mes atouts (exercices 2 et 3). `route.pistes` y est posé.
    - Un second tableau, fixe, « Face à vos critères » : les risques, les valeurs que la piste respecte, le moment où le minimum sécurisant est atteint.
    - La charge moyenne (renoncer à un scénario) suit la convention du carnet 4 : « Le scénario que je laisse de côté » · « Ce qu'il me coûte de le laisser », facultatif, puis « Avec le recul, choisir m'apprend que… ».
88. **Une feuille de route par piste, en tableau** (`route.feuilles` sur la première) : trois paliers de 30, 60 et 90 jours, avec les thèmes de l'app (sécuriser, tester, conclure), face à « Mon objectif », « Le résultat que je pourrai constater » et « Mes actions, et leur date », en cases de 2,6 cm.
    - Le gabarit `roadmap` de l'app est écarté : il préremplit ses cases.
    - La piste A reporte « Ce qu'il faudrait pour y aller » de la matrice (`c7.matrice`). La piste B, qui ne vient pas toujours de la matrice, y renvoie par écrit, et ajoute « Le signal qui me fera passer à la piste B » · « Ou la date à laquelle je la lance ».
89. **Le module de votre projet a sa page** (Nicolas), adaptable.
    - Trois cartes (créer, se reconvertir, évoluer), puis un choix exclusif en mots : création, reconversion, évolution, aucun.
    - « Ce que la séance 9 a posé » : la formation ou la démarche visée, son financement ou la personne à voir, ma prochaine démarche, sa date. La personne en reconversion ou en évolution interne garde ainsi une trace de la séance 9 en attendant ses modules.
    - Deux liens officiels, vérifiés le 8 octobre 2026, remplacent les volumes d'heures CPF du livret : Mon Compte Formation et Mon CEP (France compétences, pour trouver un conseiller en évolution professionnelle).
90. **Les premières actions** (`route.actions`) : trois lignes, « Ce que je fais » · « La date » · « Je préviens ».
91. **Garde-fous et soutiens** (« alliés », au masculin générique, devient « soutiens », comme au carnet 5).
    - Les reports : les limites hors argent (`c5.limites`) et « Ce que m'ont appris les personnes rencontrées » (`c7.enquetes`).
    - Le risque de décrocher et sa parade, puis un tableau des soutiens (« Qui me soutient » · « Ce que je lui demande » · « Notre premier point, le ») : les deux questions de l'app. Les soutiens viennent du carnet 5 (exercice 8), par un renvoi écrit.
    - La question franche du rapport 07 sur le cadre de sécurité (« Le compromis que je ne referai plus, même pour un meilleur salaire ») est écartée : elle double les limites du carnet 5, « Ce que je n'accepte pas » au carnet 4 et le compromis du carnet 7 (exercice 6), et la page n'en a plus la place. Les seuils ne sont que reportés.
92. **Le chemin parcouru tient sur deux pages.**
    - D'abord la boussole (`c2.boussole`, deux lignes), puis « Ce qui est clarifié » · « Ce qui reste ouvert » (rapport 07). Les huit domaines de vie sont renotés avec la grille fixe du carnet 1, sans regarder les anciennes notes.
    - Ensuite les dix météos, recopiées dans une carte de dix cases avec un renvoi écrit (Nicolas) : dix reports auraient pris onze centimètres. Puis « Ce que me disent mes météos » · « Le domaine qui a le plus bougé » · « Ce qui l'explique ».
    - Le suivi à six mois ferme la page : « Ce que je veux pouvoir constater d'ici là » · « La question que je voudrai poser », avec ce qu'il faut relire avant.
93. **Les questions du livret.**
    - Thème 1 : remplacé par la page de reports.
    - Thème 2 (travail réel, travail empêché) : déjà au carnet 2, avec un renvoi.
    - Thème 3 : le tableau des compétences prouvées.
    - Thème 4 : les paliers deviennent une colonne. Le miroir et « la compétence qui ouvre la porte » vont à « Ce que les autres voient ». « Dans quels nouveaux métiers » est retiré : ce sont les dix pistes.
    - Thème 5 : deux récits.
    - Thème 6 : « Ce qui m'attire pour l'avenir » (des évolutions sociétales, abstraites, qui orientent la réponse) est retiré. « Ce que je décide moi-même » est couvert par les limites, reportées. « Qui interviewer » est retiré : les comptes rendus du carnet 7 le remplacent. Les réussites passées nourrissent le second récit.
    - Thème 7 : les seuils sont reportés, les pistes A et B ont leurs tableaux, le petit pas devient trois premières actions, un lien officiel remplace les heures CPF. « Garantie à 100 % », « pas proximal » et « le plus grand piège d'une reconversion » sont retirés.
    - Les 28 exemples d'un seul profil sont remplacés par huit exemples contrastés, un par exercice qui en a la place, chacun d'un métier différent.
94. **Second passage sur l'audit** (demandé par Nicolas).
    - Corrigé :
      - le travail empêché (carnet 2, exercice 2) rejoint les renvois des compétences prouvées, et la consigne dit combien en noter : cinq ;
      - une case, une chose : « La situation : ce qui posait problème », « Le résultat : ce qui a changé ensuite », « Mes atouts pour y aller (exercices 2 et 3) » ;
      - les mots du programme, « projet d'élan » et « refuge, ou tremplin », dans la définition et les en-têtes des pistes A et B ;
      - aucune répétition entre une page et ses engagements, comme le relevait le rapport 07 au livret : « à voix haute » reste sur la page des récits, la première action à l'exercice 7. Les engagements deviennent « Je laisse mûrir mon choix : il se fait en séance 9, pas avant » et « Avant chaque entretien, je relis mes compétences prouvées et mes deux récits » ;
      - le masculin générique : « alliés » devient « soutiens », « les professionnels rencontrés » devient « les personnes rencontrées » ;
      - le renvoi au carnet 7 de « Avant de reprendre » est marqué fixe ;
      - la consigne des météos nomme aussi les pages « Avant de reprendre » ;
      - la page du module reçoit un exemple, dans l'aide de « Ce que la séance 9 a posé », et « Face à vos critères » une phrase d'ouverture.
    - Écarté, avec la raison :
      - une ligne « Ce qu'elle me coûte » aux pistes A et B (rapport 07, thème 7) : les risques, le minimum sécurisant et le compromis du carnet 7 (exercice 6) le disent, et la page est pleine ;
      - un « pourquoi » après le niveau d'autonomie (rapport 07, thème 4) : la preuve et le résultat, sur la même ligne du tableau, en tiennent lieu ;
      - « Envie : oui, plutôt, non » reste une colonne fermée, comme le proposait le rapport 07 : c'est un palier, pas une question à rouvrir ;
      - la relecture de « Je m'autorise à » (rapport 07, fil rouge) : le carnet 6 l'a reportée aux pistes audacieuses, et la boussole relue au chemin parcouru la prolonge.

## 3. Les PR, dans l'ordre

Une PR par ligne, fusionnée par Nicolas avant de passer à la suivante.

| PR | Contenu | Points d'attention |
|---|---|---|
| **R0 · Socle** | Le gabarit commun et le système de nommage (détails en section 4). La carte : section 9 mise à jour. | Touche tous les documents. Comparer avant et après chaque document, et ne garder que les changements voulus. |
| **R0 bis · Format** | La marque « fixe / adaptable » et les identifiants de données, avec le bloc de report (« Reportez vos seuils · carnet 4, p. 12 ») et la règle de personnalisation qui en découle dans l'app. | Séparée de R0 pour garder le socle lisible. À fusionner avant R2, le premier carnet qui reporte des données. |
| **R1 · Carnet 1** | État des lieux et héritages, à partir du carnet 0 et du carnet 1 actuels et de l'app (carte, section 5). | Le cadre de travail est fixe et jamais personnalisé. Une alternative pour une famille absente ou douloureuse. |
| **R2 · Carnet 2** | Parcours : objectif boussole, expériences et travail réel, travail empêché, quatre zones, fil rouge, ligne de vie, arbre de vie facultatif, interview. | Il absorbe le travail réel du livret. Cible : 2 h 45. |
| **R3 · Carnet 3** | Fonctionnements : l'encadré « À savoir sur le test », les 17 mises en situation réécrites, la page « ce que j'en retiens ». | Aucune mention du MBTI. Q16 est réécrite du point de vue des proches. |
| **R4 · Carnet 4** | Argent : la seule saisie du profil validé, la carte des 4 seuils, « ce que je me dis → les faits ». | La question sur le couple est posée au passé. Aucun chiffre personnel en exemple. |
| **R5 · Carnet 5** | Valeurs : la liste corrigée, la grille anti-compromis (seul endroit des 3 valeurs), l'entourage et la demande aux proches. | Les réponses des proches arrivent avant la séance 6. |
| **R6 · Carnet 6** | Exploration : la cartographie en reports, le retour des proches, les ressources, 10 pistes. | Les seuils restent dans une zone « à garder pour vous ». |
| **R7 · Carnet 7** | Confronter, en deux parties : les 3 fiches à critères, la préparation des enquêtes, salaires et débouchés, puis les comptes rendus, le terrain et la matrice. | Des liens officiels, pas de chiffres écrits dans le carnet. |
| **R8 · Carnet de route** | Deux parties. D'abord : profil en reports, compétences prouvées, deux récits. Ensuite : pistes A et B, feuilles de route à 30, 60 et 90 jours, premières actions, garde-fous et soutiens, chemin parcouru, préparation du suivi, place du module de projet. | Remplace le livret. Ses 28 exemples (un seul profil, peut-être une personne réelle) disparaissent au profit d'exemples contrastés tirés de métiers différents. |
| **R9 · Module création** | Le business plan court, environ 12 pages : fondations, problème, offre, prix, point mort, test, synthèse. Il reprend les seuils, la grille anti-compromis et l'entretien prospects de l'app. | Il est personnalisable en une fois. |
| **R10 · Livret business plan** | Le livret complet autonome, avec les refontes de l'audit (rapport `08-business_plan.md`), et la personnalisation partie par partie dans l'app. | Informations réglementaires renvoyées vers les sources officielles. |
| **R11 · Nettoyage** | Supprimer `chap0` à `chap6.json` et `livret.json`, mettre à jour le catalogue de l'app, la CI et `test_cli_documents.py`. Vérifier la cohérence avec le programme et le récapitulatif du site. | Tant que R11 n'est pas fusionnée, les anciens carnets restent disponibles à côté des nouveaux. |
| Plus tard | Modules reconversion et évolution interne | Voir `chantier-modules-s9.md`. |

Pour chaque PR de carnet :
- **Contenu.** Suivre le tableau de la carte (section 5) et les recommandations du rapport du carnet (`rapports/`).
- **Charge émotionnelle.** Poser le protocole sur chaque exercice à forte charge.
- **Les données qui circulent.** Les écrire une seule fois (`data_id`) et les reporter avec un bloc `report` (carte, section 7, pour les identifiants). Les tests vérifient qu'un report vise une donnée déclarée.
- **Fixe ou adaptable.** Marquer `"fixed": true` ce que la personnalisation ne doit pas toucher (carte, section 8) : le cadre et les héritages (carnet 1), les questions du test (carnet 3), la liste de valeurs (carnet 5), les critères des fiches, la définition des seuils.
- **Durée.** Viser la durée cible, la mettre dans le sourcil des exercices et mettre à jour le budget (carte, section 6).
- **Vérifier le rendu de chaque page.**
- **Relire l'audit** (`synthese.html` et le rapport du carnet) une fois le carnet construit, recommandation par recommandation, et itérer.

## 4. Le socle (R0) en détail

**Nommage**
- `DocumentBuilder` accepte les carnets 1 à 7 (folio « carnet N/7 ») et le carnet de route (folio « carnet de route »). L'ouverture affiche « Carnet de bord · carnet N » au lieu de « chapitre N ».
- `PDFStyle.CARNET_PASTELS` est réattribué pour 1 à 7 et pour le carnet de route. **Fait** : palette « par temps » (section 2, point 7).
- Les scripts `main_generate_carnet_N.py`, le catalogue de l'app, la CI et les tests suivent.

**Gabarit commun** (carte, section 4 ; synthèse, lot 2)
- **Le bloc « protocole »**, en trois temps. Avant l'exercice : un avertissement, puis « Si cet exercice vous semble trop lourd à faire hors séance, laissez-le vierge : nous l'aborderons ensemble. » (« trop lourd seul » s'accordait avec la personne). Après l'exercice : un champ d'ancrage court, « Aujourd'hui, avec le recul, je sais que… ».
- **La durée dans le sourcil** (« Exercice 2 · 15-20 min »). La page d'ouverture donne le total et le découpage conseillé, avec une ligne de cadre (qui lit, droit de passer une question).
- **L'exemple contrasté**, avec un rendu commun « En surface / Exploitable ».
- **La météo et le récapitulatif** dans le gabarit de chaque carnet.
- **La fin de carnet en trois zones guidées**, avec le fil des pistes à partir du carnet 2. Elle remplace la grande zone « notes ».
- **Accessibilité** : la langue `fr` dans le catalogue du PDF.
- Chaque nouveau bloc suit la liste « Adding a new page template or atomic block » de `CLAUDE.md` : `spec.py`, `compiler.py`, aperçu dans l'app, test, planche de démonstration. Il s'ajoute aussi à `REFERENCE_BLOCKS_RULES` s'il ne doit pas être créé par Gemini.

**Format** (carte, section 10) : fait dans R0 bis
- **La marque « fixe / adaptable »** sur chaque bloc. Une seule règle de lecture pour la personnalisation : ce qui porte `"fixed": true` (une page entière ou un bloc) ne change pas, le reste est adaptable. Le protocole, l'ancrage, la météo et les reports sont toujours fixes. L'app ne se contente pas de le demander à Gemini : elle rétablit ce qui est fixe après chaque personnalisation (`keep_fixed`). La retouche d'un livret (« itérer ») suit la consigne du consultant, qui peut demander de modifier une page fixe.
- **Des identifiants stables pour les données** (par exemple `c4.seuils`), posés par `data_id` sur la page ou le bloc qui écrit la donnée. Le bloc `report` la reporte : « Vos quatre seuils · carnet 4 · p. 12 », la page étant lue dans le carnet 4 de `workbooks/` au moment de la génération. Sans fichier pour ce carnet, la ligne affiche « carnet 4 ». Les identifiants à utiliser sont dans la carte, section 7.

## 5. Comment travailler

- **Le contenu** est dans `workbooks/<id>.json`, au format de `Scripts/workbook_generator/spec.py` (la docstring de `BlockSpec` donne la forme de chaque bloc). On prend exemple sur les carnets existants.
- **Générer** un document : `python Scripts/main_generate_<id>.py --output <fichier>.pdf`, depuis la racine du dépôt.
- **Voir les pages** : les rendre en PNG avec pymupdf (`page.get_pixmap(dpi=60).save(...)`) dans `previews/` (ignoré par git), et les relire une à une.
- **Comparer** avant et après (pour le socle) : générer les PDF de `main` dans un dossier temporaire, puis comparer page par page l'image (`pixmap.samples`), le texte (`get_text`) et les champs (`widgets()`).
- **Tester** : `python -m pytest tests`. `tests/test_workbooks.py` vérifie :
  - que chaque fichier est au catalogue ;
  - qu'aucun `field_id` n'est en double ;
  - que les fichiers ne gardent que ce qu'ils définissent : pas de `null`, pas de valeur par défaut recopiée.
- **Les conventions posées par le carnet 1** (`workbooks/carnet-1.json`), à suivre dans les suivants :
  - en tête du fichier, `"carnet": N` (pastel, folio et sourcils viennent de là), sans `folio` ni `pastel` ;
  - les identifiants de champs commencent par `cN_` (`c1_objectif`), ceux de la météo par `cN_meteo` et ceux du livrable par `cN_livrable` ;
  - l'ouverture liste chaque élément avec sa durée (« Exercice 3 · Votre objectif, première version · 10 min »), donne `duration` et `split` ; la somme fait la cible de la carte ;
  - chaque page d'exercice a pour sourcil « Exercice N · nom court · durée », une page par partie quand l'exercice en a deux, et s'ouvre par une phrase qui dit à quoi il sert ;
  - un seul exemple contrasté par exercice, d'un métier au nom épicène et différent à chaque fois (juriste, cariste, commis de cuisine, comptable, ébéniste au carnet 1) ; un exemple de plus peut aller dans le champ `example` d'une question ;
  - le protocole ouvre la première page d'un exercice lourd, l'ancrage ferme la dernière ;
  - `fixed: true` sur la page entière quand tout y est fixe, sur le bloc sinon ; un paragraphe qui renvoie à un autre carnet (« vous la préciserez au carnet 2 ») est fixe, comme le dos ;
  - deux lignes manuscrites pour une réponse en phrase (case de 1,6 cm au moins), une ligne pour un mot (0,8 cm) ; `tests/test_workbooks.py` le vérifie pour chaque carnet, avec une info-bulle sur chaque champ ;
  - une page ne déborde jamais sur une page « (suite) » : passer des cases en grille de deux colonnes, raccourcir un libellé ou un exemple, plutôt que de descendre sous ces hauteurs.
- **Les conventions ajoutées par le carnet 2** (`workbooks/carnet-2.json`) :
  - un exercice sur plusieurs pages donne sa durée page par page, et l'ouverture leur somme (exercice 1 : 15 min, puis 3 × 10 min) ;
  - une partie facultative a pour sourcil « Exercice N · nom · facultatif · durée », ou « Pour aller plus loin · nom · facultatif » quand elle se fait hors temps d'écriture ; `split` dit qu'elle s'ajoute au total ;
  - une question franche est marquée `fixed`, avec le bloc qui la porte (une `fields_card` entière s'il le faut) ;
  - un report se recopie sur une ligne de 0,85 cm, sauf s'il reste la place d'une case de 1,6 cm ;
  - l'exemple de l'app peut aller dans le `hint` d'une `fields_card` quand la page n'a pas la place d'un exemple contrasté (récapitulatif) ;
  - une note manuscrite (`annotation`) peut occuper le blanc sous une fiche répétée ;
  - métiers déjà pris pour les exemples : juriste, cariste, commis de cuisine, comptable, ébéniste (carnet 1) ; gestionnaire de clientèle, aide à domicile, graphiste, géomètre, fleuriste, secrétaire, paysagiste (carnet 2) ;
  - la ligne de vie (`life_line`) accepte un troisième élément par moment, le libellé de sa case ; la ligne de vie et l'arbre de vie tiennent désormais les hauteurs du test.
- **Les conventions ajoutées par le carnet 3** (`workbooks/carnet-3.json`) :
  - des lignes de report courtes (les quatre zones) se mettent en deux colonnes, avec `"columns": 2`. Chaque ligne réserve la place de son origine (« CARNET 2 · P. 00 »), si bien qu'un numéro de page ne change jamais la mise en page ;
  - un texte dont la formulation ne doit pas bouger (un test, sa consigne) se marque `fixed` sur la page entière, ouverture comprise ;
  - une question qui demande deux choses a deux cases, ou une échelle suivie d'un « pourquoi » (bloc `scale`, bornes de 20 caractères au plus, sinon elles sont tronquées) ;
  - une réponse en quelques mots dans une carte de question prend 1,6 cm, car ces cases sont toujours multilignes ;
  - quand un exemple pourrait orienter la réponse (un test), il porte sur un sujet absent du carnet ;
  - métiers déjà pris pour les exemples : ceux des carnets 1 et 2, plus architecte (carnet 3).
- **Les conventions ajoutées par le carnet 4** (`workbooks/carnet-4.json`) :
  - un choix exclusif en mots est une `rating_grid` d'une ligne, avec ses valeurs écrites dans `values`, suivie de « Parce que… ». Le libellé d'une ligne de `rating_grid` tient en 6 cm, soit une trentaine de caractères : au-delà, il est tronqué ;
  - un `questions_group` remplit la page jusqu'en bas : on le met en dernier, et l'exemple contrasté passe avant lui. Sinon, on donne une hauteur à chaque case ;
  - une question à charge moyenne, hors protocole, est franche et facultative (« Un mot suffit, ou laissez la case vierge pour la séance »), suivie d'une clôture d'une phrase ; les deux sont fixes ;
  - un montant ou une fourchette prend une case d'une ligne (0,85 cm), et l'unité est écrite une seule fois, dans le `hint` de la carte ;
  - le titre de l'ouverture tient sur une ligne quand l'introduction a sept lignes ;
  - le `hint` d'une `fields_card` se lit avant les libellés : la carte prend alors un titre (« Après la restitution »), ou la consigne passe dans le libellé ;
  - métiers déjà pris pour les exemples : ceux des carnets 1 à 3, plus libraire, photographe, bibliothécaire, interprète, peintre en bâtiment, journaliste, orthophoniste (carnet 4).
- **Les conventions ajoutées par le carnet 5** (`workbooks/carnet-5.json`) :
  - classer plutôt que recopier : une liste classée court sur deux cartes de `numbered_lines`, la seconde avec son premier numéro en quatrième élément (`["Les cinq suivantes", "c5_valeur_rang", "aide", 6]`). Les identifiants se suivent (`c5_valeur_rang_1` à `_10`) ;
  - une sortie qui croise plusieurs données et plusieurs critères est un `table` : une colonne par donnée, une ligne par critère, `field_height_cm` 2,2. Chaque case porte un `placeholder`, qui devient son info-bulle ;
  - quelques champs libres courts tiennent sur une ligne, avec une `fill_in_card` (« Une valeur me manque : … ») ;
  - une donnée faite de plusieurs blocs d'une page porte son `data_id` sur la page (`c5.entourage`) ;
  - le générateur ne coupe jamais à U+00A0 : une espace insécable lie « carnet », « exercice » et « séance » à leur numéro, pour qu'il ne reste pas seul en début de ligne ;
  - un participe qui suit un pronom complément s'accorde avec la personne (« ce qui m'a poussé ») : on écrit « ce qui m'a fait agir ainsi », ou on tourne autrement ;
  - un exercice de tri (une liste à cocher) n'a pas d'exemple contrasté : il orienterait le choix ;
  - une liste de personnes avec plusieurs informations par personne est un `table` aux cases d'une ligne (`field_height_cm` 0,85) : une colonne par information, plutôt qu'une ligne « qui, et ce que… » ;
  - un report vise la donnée utile à l'exercice : avant la grille, le critère retourné (« donc, mon poste devra… »), pas l'irritant ;
  - métiers déjà pris pour les exemples : ceux des carnets 1 à 4, plus kinésithérapeute, biologiste, vétérinaire, urbaniste, documentaliste, ergothérapeute, notaire (carnet 5).
- **Les conventions ajoutées par le carnet 6** (`workbooks/carnet-6.json`) :
  - un libellé de report sur deux colonnes tient sur une ligne jusqu'à une vingtaine de caractères (la place de l'origine est réservée) : « Mes deux forces », « Ce qui me recharge ». Plus long, il passe sur deux lignes et coûte 0,45 cm par rangée ;
  - une liste longue (dix pistes) se partage en deux tableaux sur deux pages, avec un numéro par ligne (R1, A1) pour en parler en séance. Ce numéro est une cellule de texte : une cellule vide deviendrait une case à cocher ;
  - une donnée écrite sur deux pages porte son `data_id` sur le premier bloc : l'origine d'un report pointe sa première page ;
  - quelques informations recopiées d'un autre carnet, quand elles tiennent dans la colonne d'un tableau (des prénoms), passent par un renvoi écrit (« carnet 5, exercice 8 ») plutôt que par un bloc `report` ;
  - un lien porte son adresse courte entre parenthèses, à la fin de sa description, pour l'impression. Chaque lien se vérifie avant la PR : un podcast avait disparu ;
  - un titre dont le premier mot se termine par une apostrophe se met entièrement en accent (« *L'exploration.* ») : « L'*exploration.* » laisserait un blanc après l'apostrophe ;
  - métiers déjà pris pour les exemples : ceux des carnets 1 à 5, plus archiviste, économiste, topographe (carnet 6).
- **Les conventions ajoutées par le carnet 7** (`workbooks/carnet-7.json`) :
  - un carnet en deux parties déclare `parts`, et chaque page de partie son `part`. Ses exercices sont numérotés à la suite. Chaque partie finit par sa page de livrable (« Votre premier livrable », « Votre second livrable »), et la partie 2 s'ouvre sur « Avant de reprendre », avec sa météo (`cN.meteo_2`). Les sourcils de ces pages commencent par « Partie 1 · » ou « Partie 2 · » ;
  - une échelle en mots peut avoir quatre valeurs (« Oui / À terme / Non / À vérifier »). Le moteur garde les valeurs dans la carte, et le libellé d'une ligne tient toujours en une trentaine de caractères (« Valeur 1 : condition remplie ») ;
  - une fiche répétée qui n'a pas la place d'une consigne la reçoit sur la page qui ouvre l'exercice, avec l'exemple et les définitions ;
  - une piste se désigne par « Piste 1 » à « Piste 3 », dans l'ordre du récapitulatif, sans recopier son intitulé ailleurs que sur sa fiche ;
  - une donnée et sa source vont dans deux cases côte à côte (« Rémunération observée » · « Sa source ») ; plusieurs informations courtes (le lieu, le trajet, le télétravail) prennent chacune une case d'une ligne, sous un titre de carte, plutôt qu'une grande case qui pose trois questions ;
  - un lien dont la page s'affiche en JavaScript se vérifie dans le navigateur intégré, pas avec une simple requête ;
  - métiers déjà pris pour les exemples : ceux des carnets 1 à 6, plus frigoriste, pépiniériste, ergonome, chimiste, géologue, garagiste (carnet 7).
- **Les conventions ajoutées par le carnet de route** (`workbooks/carnet-de-route.json`) :
  - un document sans grand numéro met `"number": ""` sur sa couverture et `"num": ""` à son ouverture (sans `null` dans le fichier). L'ouverture gagne environ 4 cm : treize lignes d'exercices y tiennent ;
  - une réponse et son « pourquoi » vont dans deux cases (« Le scénario vers lequel je penche » · « Pourquoi lui ») ; un numéro reste avec ce qu'il désigne (« L'intitulé, et son numéro de scénario »), comme au carnet 7 ;
  - deux pistes se comparent dans un tableau A · B : ce qui s'adapte (l'intitulé, ce qui attire) dans un premier tableau, les lignes de critères dans un second, fixe ;
  - les paliers d'une feuille de route sont les lignes d'un `table`, pas le gabarit `roadmap`, qui préremplit ses cases ;
  - un niveau qui qualifie chaque ligne d'un tableau est une colonne étroite, ses paliers définis au-dessus, en verbes épicènes ;
  - une série de valeurs recopiées de plusieurs carnets (les météos) tient dans une carte de petites cases (0,85 cm), avec un renvoi écrit, plutôt que dans un report par carnet ;
  - un choix exclusif en mots de quatre valeurs tient si chacune fait une douzaine de caractères au plus : « Évolution interne » chevauchait « Aucun module » ;
  - métiers déjà pris pour les exemples : ceux des carnets 1 à 7, plus analyste de données, responsable logistique, réceptionniste, agronome, céramiste, chauffagiste, typographe, actuaire (carnet de route).
- **Mesurer avant de rendre.** Sous un titre d'une ligne, une page offre 23,4 cm (1,1 cm de moins sous un titre de deux lignes). Ordres de grandeur, écart compris :
  - protocole et ancrage : 5,1 cm chacun (5,6 cm pour un avertissement de trois lignes) ;
  - météo : 7,6 cm ;
  - exemple contrasté : 4,8 cm (5,3 cm sur quatre lignes) ;
  - report : 4,2 cm pour une ligne, 6 cm pour deux lignes, et autant pour quatre lignes en deux colonnes, puis 1,75 cm par ligne de plus ;
  - grille de notes (`rating_grid`) avec un titre : 4 cm pour une ligne, 7,8 cm pour cinq lignes et leurs bornes ;
  - cartes à lire (`info_cards`) en deux colonnes, avec titre, sous-titre, deux lignes de texte, une question clé et une case : 5,5 cm par rangée ;
  - échelle de 1 à 5 : 4 à 4,5 cm ;
  - carte de question : 2,1 cm de plus que sa case pour une question d'une ligne, puis environ 0,5 cm par ligne de plus (question ou consigne) ;
  - paragraphe d'une ligne : 1 cm ;
  - la ligne de vie et l'arbre de vie demandent au moins 14 cm ;
  - mesures du carnet 5 : un tableau de cinq lignes de 2,2 cm, avec son en-tête, 13,7 cm ; neuf cartes de neuf cases à cocher sur trois colonnes, 19 cm ; treize cases à cocher sur trois colonnes, 4,9 cm ; une `fill_in_card` d'une ligne, 2,5 cm ; des `numbered_lines` sur deux colonnes avec une aide, 7,6 cm pour cinq lignes et 5,6 cm pour trois ; trois `info_cards` sur une rangée, 5,7 cm ; une frise et son intertitre, 4,4 cm ; une `fields_card` de trois rangées de cases de 1,6 cm, 10,2 cm ; un report de quatre lignes de 1,6 cm sur deux colonnes, 8,2 cm ; un tableau de cases d'une ligne, 0,75 cm d'en-tête puis 1,15 cm par ligne ;
  - mesures du carnet 6 : un tableau de cases de 1,6 cm, 0,75 cm d'en-tête puis 1,9 cm par ligne (10,2 cm pour cinq lignes, 6,4 cm pour trois) ; un report de huit lignes sur deux colonnes, dont deux de 1,6 cm, 10,8 cm ; un report de quatre lignes sur deux colonnes, 5,7 cm ; trois `link_card` de deux, cinq et un liens, 14,4 cm avec leurs écarts ; deux cartes de `numbered_lines` côte à côte, trois lignes de 0,85 cm chacune, 5,2 cm ;
  - mesures du carnet 7 :
    - une `fields_card` de trois rangées (0,85, 1,6, puis deux cases de 1,6 cm), 8,3 cm, et de trois rangées de 1,6 cm (dont une de trois cases), 9 cm ;
    - une `rating_grid` de quatre lignes avec son titre, 6,5 cm : une fiche (ces trois blocs) remplit exactement une page, sans phrase d'ouverture ;
    - un compte rendu (titre, rangées de 0,85, 2,6 et 1,6 cm), 10,3 cm, deux par page ;
    - une `star_list` de sept questions, dont deux sur deux lignes, 7 cm ;
    - une `link_card` de deux liens de deux lignes, 5,1 cm, et d'un lien, 3,8 cm ;
    - un report de trois lignes de 0,85 cm, 7,75 cm ;
    - un tableau de trois lignes de 0,85 cm, dont l'en-tête tient sur deux lignes, 5,2 cm.
  - mesures du carnet de route :
    - un report d'une ligne de 1,6 cm, 5 cm ; de six lignes de 1,6 cm sur deux colonnes, 10 cm (0,45 cm de plus par libellé de deux lignes) ;
    - un tableau de cinq lignes de 1,6 cm, l'en-tête sur deux lignes, 11,2 cm ; un tableau A · B de trois lignes de 1,6 cm, 7,5 cm ; une feuille de route (trois lignes de 2,6 cm), 10,5 cm ;
    - un récit (titre, rangées de 1,6, 2,6 et 1,6 cm), 11 cm ;
    - trois `info_cards` sur une rangée, deux à trois lignes de texte, 4,8 cm ; une `rating_grid` d'une ligne avec titre, 4 cm ; de huit lignes avec titre et bornes, 9,3 cm ;
    - une carte de dix cases de 0,85 cm sur deux rangées, avec titre, 6,1 cm.

  Une ouverture de neuf lignes, avec une introduction de sept lignes, ne tient que sous un titre d'une ligne. Une ouverture de dix lignes tient avec une introduction de quatre lignes, une phrase en gras de deux lignes et un découpage de trois lignes.
- **Tester l'app en local** : `python -m uvicorn server.app:app --port 8080`. Sans clé Gemini, l'app fonctionne en mode de secours. Avec la vraie clé, tester la personnalisation des carnets 6, 7, du carnet de route et du module création, ceux qui s'y prêtent le plus (carte, section 8).

## 6. Les règles à garder en tête

- **Le ton (DA, section 7).**
  - Vouvoiement, phrases courtes et affirmatives, titres ponctués en casse de phrase.
  - Jamais « coach » : on dit « consultant en transformation » ou « la personne qui vous accompagne ».
  - Pas de registre de développement personnel, jamais « présentiel », aucun chiffre sans source.
- **Pas de formule genrée.** « Ce qui m'étonne », et non « Ce qui m'a surpris ».
- **Les exemples viennent d'un métier voisin**, jamais du métier de la personne, et d'un métier différent à chaque fois.
- **Ne sont jamais personnalisés** : le cadre, le protocole, les textes réglementaires et les renvois entre carnets.
- **Le programme est un texte réglementaire** : on le modifie seulement sur demande. Si un carnet change ce que le programme promet (séances, livrables, durées), le signaler à Nicolas et prévenir pour le site.

## 7. Ce qui reste ouvert

- **La politique des champs** : police fixe avec défilement, ou police automatique. À trancher après un test de saisie dans de vrais lecteurs PDF (Acrobat, Aperçu, navigateur).
- **Les 51 champs trop bas** pour l'écriture à la main : les agrandir au fil des PR de carnet. Depuis R1, un test le vérifie pour chaque nouveau carnet (1,6 cm pour une phrase, 0,8 cm pour un mot), et la case « Ce chiffre s'explique surtout par… » de la météo passe de 1,2 à 1,6 cm. Depuis R2, la ligne de vie et l'arbre de vie les tiennent aussi.
- **Les reprises du carnet 2** se font dans les carnets suivants : les compétences de vie et les expériences au carnet de route, l'interview au carnet 7, l'objectif boussole au chemin parcouru. Le fil rouge, les quatre zones et un moteur sont repris au récapitulatif du carnet 3 (R3). Les moteurs et les critères sont relus avant la grille anti-compromis du carnet 5 (R5). Les moteurs « je le veux » et l'objectif boussole sont reportés à la cartographie du carnet 6 (R6). Les questions de l'interview entrent dans la grille d'entretien du carnet 7, et la personne interviewée parmi ses contacts (R7). Les expériences, la zone d'excellence et les compétences de vie sont citées par un renvoi écrit aux compétences prouvées du carnet de route, et l'objectif boussole y est reporté au chemin parcouru (R8).
- **Les reprises du carnet 3.**
  - La cartographie des énergies (`c3.energies`) est reportée au profil du carnet de route : quatre lignes, le critère retourné compris (R8). Deux de ses lignes sont déjà reprises au récapitulatif du carnet 4 (R4), une autre avant la grille du carnet 5 (R5), deux à la cartographie du carnet 6 (R6). Elle remplace « Ce qui vide mes batteries » et « Mes sources de stress » : on la reporte, on ne repose pas la question.
  - Les réponses à « Sous pression » (Q16 et Q17) restent dans le carnet 3, sans report.
- **Les reprises du carnet 4.**
  - Les seuils (`c4.seuils`) et la tendance dominante (`c4.tendance`) sont reportés au récapitulatif du carnet 5, et ses tensions y renvoient (R5).
  - Les seuils sont reportés à la cartographie du carnet 6, dans une carte « À garder pour vous » (R6). Sur chaque fiche du carnet 7, « Mon minimum est atteint : oui / à terme / non / à vérifier » et la rémunération observée, avec un renvoi à la cartographie (R7). Ils sont reportés aux pistes A et B du carnet de route, dans « À garder pour vous » (R8), et iront au module création (R9).
  - Le profil validé et ses deux forces (`c4.profil`) sont reportés à la cartographie du carnet 6 (R6). Ils sont reportés au profil du carnet de route (R8).
  - Le livret business plan cite déjà les seuils, dans des encadrés fixes « Si vous avez fait le bilan ».
- **Les reprises du carnet 5.**
  - La grille anti-compromis (`c5.grille`) est reportée au carnet 6 : les valeurs au récapitulatif, leurs conditions à la cartographie (R6). Au carnet 7, les fiches jugent chaque piste sur ses trois conditions, et la grille d'entretien en reporte les trois questions (R7). Ses trois valeurs et leurs conditions sont reportées aux pistes A et B (R8). Elle ira au module création (R9).
  - Les limites hors argent (`c5.limites`) sont reportées à la cartographie du carnet 6 (R6). Elles sont reportées aux garde-fous du carnet de route (R8).
  - L'entourage (`c5.entourage`) est repris au retour des proches du carnet 6, par un renvoi écrit : une ligne par proche sollicité (R6). Il est cité aux soutiens du carnet de route, par un renvoi écrit (R8).
  - Les situations d'alignement (exercice 1) sont citées par un renvoi écrit aux récits d'action du carnet de route (R8).
  - Les tensions et la hiérarchie restent dans le carnet 5, sans report.
- **Les reprises du carnet 6.**
  - Les dix pistes (`c6.pistes`) sont citées au récapitulatif du carnet 7 par un renvoi écrit : les trois pistes retenues en séance 6, et pourquoi (R7). Le rapport 07 propose « Pour chacune de vos pistes réalistes (carnet 6), quelle compétence vous ouvre la porte ? », aux compétences prouvées du carnet de route : il la pose aux trois scénarios de la séance 8, qui en sont issus (R8).
  - Les réponses des proches (`c6.proches`) sont reportées au carnet de route, comme preuve extérieure (« Ce que les autres voient », R8). Le livret business plan en parle déjà dans ses encadrés fixes.
  - Les personnes repérées en fin de carnet 6 sont citées aux contacts d'enquête du carnet 7 (R7).
  - Les deux questions plus franches reportées au carnet 7 y sont posées : le compromis à l'exercice 6, après le terrain, et « Ce qui pourrait me faire repousser ce contact » aux contacts (R7).
- **Les reprises du carnet 7.**
  - Les fiches, les comptes rendus et la matrice (`c7.fiches`, `c7.enquetes`, `c7.matrice`) servent à la séance 8, qui en tire les trois scénarios. Le carnet de route les reprend (R8) :
    - la matrice est citée au récapitulatif de la séance 8 ;
    - « Ce que m'ont appris les personnes rencontrées » (« Les professionnels rencontrés, et ce que j'en retiens » au rapport 07) est reporté des comptes rendus aux garde-fous et soutiens ;
    - « Ce qu'il faudrait pour y aller » est reporté de la matrice à la feuille de route de la piste A, et « Ce qui me manque », sur les fiches, y est cité.
  - Les deux météos (`c7.meteo`, `c7.meteo_2`) sont recopiées au chemin parcouru du carnet de route (R8).
  - « Ma zone de recherche » n'a pas d'identifiant, et le carnet de route ne la cite pas : la feuille de route s'en sert sans la recopier.
  - Les questions plus franches restent dans le carnet 7, sans report.
- **Les reprises du carnet de route.**
  - Les compétences prouvées et les récits (`route.competences`, `route.recits`) iront aux modules reconversion et évolution interne (`chantier-modules-s9.md`).
  - Les pistes A et B, leurs feuilles de route et les premières actions (`route.pistes`, `route.feuilles`, `route.actions`) iront au module création (R9), au document de synthèse et au suivi à six mois.
  - Les deux météos du carnet de route (`route.meteo`, `route.meteo_2`) ferment la série du chemin parcouru. Le suivi à six mois n'a pas de document : la personne apporte son carnet de route.
- **Les trois familles de scénarios** (pistes directes, passerelles courtes, angles morts) viennent du programme, qui ne les définit pas. Le carnet 7 les nomme, la séance 8 fait le classement, et le récapitulatif du carnet de route les définit (R8, décision 78). Le programme est un texte réglementaire : il garde ses mots, sauf demande.
- **Le document de synthèse co-rédigé** n'a pas de modèle dans le dépôt. Ses briques sont les livrables des carnets, `route.livrable` compris. À créer si Nicolas le souhaite.
- **La page « Le module de votre projet »** du carnet de route dit que le module création « vous est remis après la séance 9 » et que la reconversion et l'évolution interne se travaillent en séance 9. À revoir quand chaque module existera (R9, puis les modules à venir).
- **L'immersion** (PMSMP) demande une convention signée par un organisme comme France Travail. Le carnet 7 dit seulement « parlons-en en séance ». Qui peut la signer pour une personne salariée en bilan reste à préciser.
- **L'option « Initiation à l'IA »** n'apparaît qu'en une ligne d'engagement, en fin de carnet 6. Le site dit que la personne explore ensuite ses pistes « en sachant ce que l'IA y déplace ». Au carnet 7, la grille d'entretien pose la question à chaque professionnel : « ce que l'IA déplace » (R7).
- **Les liens des ressources** vieillissent : en R6, un podcast avait disparu et trois adresses avaient changé ; en R7, la page « marché du travail » de France Travail renvoyait vers MétierScope (remplacée par Data Emploi). En R8, Mon Compte Formation annonçait de nouvelles règles du CPF pour les formations validées à partir du 2 octobre 2026 : le carnet de route n'en dit rien de chiffré. Les revérifier à chaque PR qui touche une page de ressources, et avant R11.
- **La personnalisation partie par partie du carnet 7 et du carnet de route** est à tester avec la vraie clé Gemini. Sans clé, les deux parties passent en mode de secours, et la partie personnalisée reprend sa place.
- **Les noms des seuils dans le programme.** En séance 4, le programme parle de « revenu vital », de « revenu sécurisant » et de « délai de trésorerie », sans revenu cible. Les carnets disent minimum vital, minimum sécurisant, revenu cible, durée acceptable d'une baisse. C'est un texte réglementaire : à aligner sur demande, au lot programme et site.
- **Les modalités du test** (passation, personne qui fait la restitution) restent à préciser dans l'encadré « À savoir sur le test » du carnet 3.
- **Les exemples du livret** décrivaient peut-être une personne réelle. Le carnet de route ne les reprend pas (R8). Le livret reste dans l'app jusqu'à R11, et l'historique git les garde ensuite.

## 8. Pour reprendre dans une nouvelle conversation

Message à coller, une fois la PR R8 (carnet de route) fusionnée :

```text
Reprends la restructuration des carnets avec la PR R9 : le module création, le business plan court du carnet de route. Il se remplit entre les séances 9 et 10, par les personnes dont la piste A est une création d'activité.

1. Prérequis
- Vérifie que la PR R8 (carnet de route, branche claude/demarrage-r8-d0d57b) est fusionnée dans main.
- Crée ensuite une branche depuis main à jour. N'empile pas les branches.
- D'autres sessions fusionnent parfois des PR pendant le travail. Avant de commiter, regarde si main a avancé (git fetch, puis git log HEAD..origin/main) et, si oui, synchronise la branche avec l'outil sync_with_base_branch. Avant de pousser sur une branche dont la PR existe, vérifie qu'elle n'est pas déjà fusionnée.

2. À lire, dans cet ordre
- audit-carnets-2026-10/feuille-de-route-restructuration.md, sections 2 à 7. La section 5 donne les conventions posées par les carnets 1 à 7 et le carnet de route, et les mesures qui disent si une page tient. La section 7 liste ce qui attend le module. Cette section 8 contient ce prompt.
- audit-carnets-2026-10/carte-parcours-unifie.md :
  - section 4 (gabarit commun) ;
  - section 5, « Le business plan · deux formats » et, au carnet de route, « Le module de votre projet » ;
  - sections 6 (budget : le module s'ajoute à la partie 2 du carnet de route), 7 (c4.seuils, c5.grille, et les données du carnet de route : route.pistes, route.feuilles) et 8 (pertinence forte : le module se personnalise en une fois ; la définition des seuils reste fixe).
- audit-carnets-2026-10/chantier-modules-s9.md : le cadre commun aux modules (place, durée, reports sans nouvelle saisie, aucun chiffre réglementaire écrit en dur).
- audit-carnets-2026-10/rapports/08-business_plan.md en entier, en particulier le parcours court de 12 pages qu'il propose (p. 4, 8, 9, 10, 20, 28 à 34 de l'ancien livret), la charge émotionnelle (le risque personnel) et le tableau des recommandations.
- workbooks/business-plan.json (R10, le livret complet) : ses parties, ses « Indispensable / Si utile », ses encadrés fixes « Si vous avez fait le bilan », ses tableaux de calcul guidés, ses liens officiels. Le module en est un extrait, pas un second texte.
- L'entretien prospects de l'ancienne app (objections, prix perçu, déclencheur d'achat) : git show 1696357:server/predefined_workbooks.py, fonction _build_business_plan_spec.
- workbooks/carnet-de-route.json (R8), en particulier la page « Le module de votre projet » (exercice 6) et les pistes A et B, puis workbooks/carnet-4.json (les seuils) et workbooks/carnet-5.json (la grille).
- La synthèse audit-carnets-2026-10/synthese.html : sections 02 (constats transversaux), 03 (charge de travail) et la fiche du livret projet.

3. Ce qu'il faut construire
workbooks/module-creation.json, environ 12 pages : fondations, problème, offre, prix, point mort, test, synthèse. Une couverture, une ouverture, une fin en trois zones et un dos.
- Les reports, sans nouvelle saisie : les quatre seuils (c4.seuils, dans une carte « À garder pour vous »), les trois valeurs et leurs conditions (c5.grille), la piste A et sa feuille de route (route.pistes, route.feuilles).
- Le point mort face au minimum sécurisant et à la durée acceptable d'une baisse, sans chiffre personnel dans les exemples.
- Le risque personnel (l'argent du foyer, la peur de l'échec) : le protocole, ou la convention du carnet 4, selon la charge que lui donne le rapport 08.
- L'entretien prospects de l'app dans l'étape « test » : les objections, le prix perçu, le déclencheur d'achat.
- Les informations réglementaires renvoyées vers les sources officielles (Urssaf, guichet unique, Bpifrance Création…), chaque lien vérifié. Aucun taux, plafond ni montant écrit en dur.
- À trancher dans le plan :
  - l'identité du fichier : "carnet": "route" (pastel jasmin, folio « carnet de route »), ou un folio et un pastel propres, comme le livret business plan. Le moteur cherche l'origine d'un report dans le premier fichier de workbooks/ dont le carnet est « route » (compiler.reference_data_pages) : un module qui déclarerait des données route.* les ferait chercher dans carnet-de-route.json. Proposer un module sans identifiant de données, ou adapter le moteur ;
  - la durée cible : la carte dit « environ 3 h », le chantier des modules « environ 1 h 30 » ;
  - ce que le module reprend mot pour mot du livret complet (et marque fixed), et ce qu'il condense ;
  - comment le module et le livret complet se renvoient l'un à l'autre : après le bilan, le livret prend le relais ;
  - sa place au catalogue de l'app : catégorie « Bilan de compétences » ou « Entrepreneuriat ».

4. Les règles à tenir
- Aucune mention du MBTI, ni de code de type.
- Un exemple contrasté par exercice, d'un métier au nom épicène, différent de ceux des carnets 1 à 7 et du carnet de route (liste en section 5 de la feuille de route). Jamais l'offre de MDM (un accompagnement individuel), que le rapport 08 a trouvée dans tous les exemples de l'ancien livret. Pas d'exemple sur un exercice de tri qu'il orienterait.
- Aucun chiffre sans source, aucun chiffre personnel dans un exemple. Les seuils restent ceux de la personne : on les reporte, on ne les commente pas.
- Le ton de la DA : vouvoiement, jamais « coach », pas de registre de développement personnel, pas de « déclic », ni « vibration » ni « effet whaou ».
- Aucune formule genrée : ni participe ni adjectif accordé dans les amorces en « je », ni point médian. « Celles et ceux » reste possible hors amorce.
- Le protocole ouvre la première page d'un exercice lourd, l'ancrage ferme la dernière. La charge moyenne suit la convention du carnet 4 : question franche facultative, puis une clôture.
- Une question qui demande deux choses a deux cases. Une réponse et son « pourquoi » vont dans deux cases.
- Les tailles de case : 1,6 cm au moins pour une phrase, 0,8 cm pour un mot. Un montant prend une case d'une ligne, et son unité est écrite une fois. tests/test_workbooks.py vérifie les tailles des carnets du bilan : si le module n'en est pas un, vérifie-les à la main.
- Aucune page « (suite) ». S'il manque de la place : une grille de deux colonnes, un libellé ou un exemple plus court. Mesure la hauteur des blocs avant de rendre (repères en section 5 de la feuille de route).

5. Méthode
a. Commence par me montrer le plan du module, page par page, avec les durées et leur total, et les choix à trancher en fin de message. Attends ma réponse avant d'écrire le JSON.
b. Écris le JSON. Ajoute Scripts/main_generate_module_creation.py, la ligne de tests/test_cli_documents.py, l'entrée module-creation du catalogue (server/predefined_workbooks.py) et module_creation à la liste des scripts de CLAUDE.md. Mets à jour la page « Le module de votre projet » du carnet de route si le module change ce qu'elle annonce.
c. Rends chaque page en PNG dans previews/ avec pymupdf et relis-les une à une. Mesure aussi la place libre en bas de chaque page.
d. Lance python -m pytest tests, puis génère tous les Scripts/main_generate_*.py. Vérifie chaque lien, dans le navigateur intégré si la page s'affiche en JavaScript.
e. Relis tout l'audit, point par point, dès ce premier tour :
   - le rapport 08 (le parcours court, la charge émotionnelle, les informations réglementaires, les recommandations) ;
   - la synthèse ;
   - le chantier des modules.
   Vérifie chaque point dans le JSON. Pour chaque page du parcours court du rapport 08, dis où elle va, ou pourquoi elle est retirée. Itère, puis dis-moi ce qui est traité, ce qui est écarté (avec la raison) et ce qui est reporté à une autre PR.
f. Mets à jour la feuille de route :
   - section 1 (état des PR : R8 fusionnée, R9 à ouvrir) ;
   - section 2 (décisions prises pendant R9) ;
   - section 5 (nouvelles conventions, s'il y en a) ;
   - section 7 (ce qui reste ouvert) ;
   - section 8 (le prompt de reprise pour R11, le nettoyage, rédigé sur ce modèle).
   Mets aussi à jour la carte, section 5 (le module création) et section 6 (son budget).
g. Commite sur la branche. J'ouvrirai la PR avec le bouton.

6. Environnement (Windows, dans un worktree)
- Le Python du venv est ../../../.venv/Scripts/python.exe.
- Pour importer le moteur hors des scripts : PYTHONPATH="Scripts;." (point-virgule sous Windows) et PYTHONIOENCODING=utf-8.
- Les outils du scratchpad des sessions précédentes ont disparu : réécris si besoin un script qui mesure la hauteur de chaque bloc et la place libre (en enveloppant compiler._add_block et PageLayout.render ; compile d'abord une fois le livret, pour que les carnets lus par les reports ne se compilent pas au milieu de la mesure) et un script qui rend chaque page en PNG et signale les pages « (suite) ».
```
