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
| R5 · Carnet 5 · Valeurs et moteurs profonds (`carnet-5.json`) | PR à ouvrir |
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
11. **Les anciens carnets restent dans l'app jusqu'à R11**, avec « (ancien parcours) » dans leur titre quand un nouveau carnet les remplace (`chap0` et `chap1` depuis R1, `chap2` depuis R2, `chap3` depuis R3, `chap4` depuis R4, `chap5` depuis R5).

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
| **R8 · Carnet de route** | Deux parties. D'abord : profil en reports, compétences prouvées, deux récits. Ensuite : pistes A et B, feuilles de route à 30, 60 et 90 jours, premières actions, garde-fous et alliés, chemin parcouru, préparation du suivi, place du module de projet. | Remplace le livret. Ses 28 exemples (un seul profil, peut-être une personne réelle) disparaissent au profit d'exemples contrastés tirés de métiers différents. |
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
  - mesures du carnet 5 : un tableau de cinq lignes de 2,2 cm, avec son en-tête, 13,7 cm ; neuf cartes de neuf cases à cocher sur trois colonnes, 19 cm ; treize cases à cocher sur trois colonnes, 4,9 cm ; une `fill_in_card` d'une ligne, 2,5 cm ; des `numbered_lines` sur deux colonnes avec une aide, 7,6 cm pour cinq lignes et 5,6 cm pour trois ; trois `info_cards` sur une rangée, 5,7 cm ; une frise et son intertitre, 4,4 cm ; une `fields_card` de trois rangées de cases de 1,6 cm, 10,2 cm ; un report de quatre lignes de 1,6 cm sur deux colonnes, 8,2 cm ; un tableau de cases d'une ligne, 0,75 cm d'en-tête puis 1,15 cm par ligne.

  Une ouverture de neuf lignes, avec une introduction de sept lignes, ne tient que sous un titre d'une ligne.
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
- **Les reprises du carnet 2** se font dans les carnets suivants : les compétences de vie et les expériences au carnet de route, l'interview au carnet 7, l'objectif boussole au chemin parcouru, les moteurs à la cartographie du carnet 6. Le fil rouge, les quatre zones et un moteur sont repris au récapitulatif du carnet 3 (R3). Les moteurs et les critères sont relus avant la grille anti-compromis du carnet 5 (R5).
- **Les reprises du carnet 3.**
  - La cartographie des énergies (`c3.energies`) se reporte au carnet 6 (cartographie) et au carnet de route (profil). Deux de ses lignes sont déjà reprises au récapitulatif du carnet 4 (R4), une autre avant la grille du carnet 5 (R5). Elle remplace « Ce qui vide mes batteries » et « Mes sources de stress » : on la reporte, on ne repose pas la question.
  - Les réponses à « Sous pression » (Q16 et Q17) restent dans le carnet 3, sans report.
- **Les reprises du carnet 4.**
  - Les seuils (`c4.seuils`) et la tendance dominante (`c4.tendance`) sont reportés au récapitulatif du carnet 5, et ses tensions y renvoient (R5).
  - Les seuils se reportent aussi à la cartographie du carnet 6, dans une zone « à garder pour vous » (R6). Sur chaque fiche du carnet 7, une ligne : « Rémunération observée · mon minimum est atteint : oui / à terme / non » (R7). Ils vont ensuite au carnet de route et au module création (R8, R9).
  - Le profil validé et ses deux forces (`c4.profil`) se reportent au carnet 6 et au carnet de route (« profil, forces, cartographie des énergies »).
  - Le livret business plan cite déjà les seuils, dans des encadrés fixes « Si vous avez fait le bilan ».
- **Les reprises du carnet 5.**
  - La grille anti-compromis (`c5.grille`) se reporte au récapitulatif du carnet 6, une ligne par valeur (R6). Elle va aussi à sa cartographie, puis aux fiches du carnet 7 (la rangée de critères) et à ses enquêtes (les questions d'entretien) (R7), à la piste A et à la piste B (R8) et au module création (R9).
  - Les limites hors argent (`c5.limites`) vont à la cartographie du carnet 6 et aux garde-fous du carnet de route.
  - L'entourage (`c5.entourage`) va au retour des proches du carnet 6, une carte par proche sollicité, et aux alliés du carnet de route.
  - Les situations d'alignement (exercice 1) peuvent nourrir les deux récits d'action du carnet de route (rapport 07) : un renvoi écrit, sans identifiant.
  - Les tensions et la hiérarchie restent dans le carnet 5, sans report.
- **Les noms des seuils dans le programme.** En séance 4, le programme parle de « revenu vital », de « revenu sécurisant » et de « délai de trésorerie », sans revenu cible. Les carnets disent minimum vital, minimum sécurisant, revenu cible, durée acceptable d'une baisse. C'est un texte réglementaire : à aligner sur demande, au lot programme et site.
- **Les modalités du test** (passation, personne qui fait la restitution) restent à préciser dans l'encadré « À savoir sur le test » du carnet 3.
- **Les exemples du livret** décrivent peut-être une personne réelle. Ils disparaissent avec le carnet de route (R8), mais si c'est le cas, l'historique git les garde.

## 8. Pour reprendre dans une nouvelle conversation

Message à coller, une fois la PR R5 (carnet 5) fusionnée :

```text
Reprends la restructuration des carnets avec la PR R6 : le carnet 6, « L'exploration ».

1. Prérequis
- Vérifie que la PR R5 (carnet 5, branche claude/carnet-5-valeurs-moteurs-539887) est fusionnée dans main.
- Crée ensuite une branche depuis main à jour. N'empile pas les branches.
- D'autres sessions fusionnent parfois des PR pendant le travail. Avant de commiter, regarde si main a avancé (git fetch, puis git log HEAD..origin/main) et, si oui, synchronise la branche avec l'outil sync_with_base_branch. Avant de pousser sur une branche dont la PR existe, vérifie qu'elle n'est pas déjà fusionnée.

2. À lire, dans cet ordre
- audit-carnets-2026-10/feuille-de-route-restructuration.md, sections 2 à 7. La section 5 donne les conventions posées par les carnets 1 à 5, et les mesures qui disent si une page tient. Cette section 8 contient ce prompt.
- audit-carnets-2026-10/carte-parcours-unifie.md :
  - section 4 (gabarit commun) ;
  - section 5, carnet 6 ;
  - sections 6 (budget), 7 (identifiants c6.*, et les données des carnets 1 à 5 qu'il reprend) et 8 (fixe ou adaptable : carnet 6 = pertinence forte ; pistes pré-intitulées, ressources du secteur, exemples ; le gabarit, le protocole et la définition des seuils restent fixes).
- audit-carnets-2026-10/rapports/06-chap6.md en entier.
- Les passages des autres rapports qui citent le carnet 6 (cherche « carnet 6 » et « chap6 » dans rapports/) :
  - 00 : l'entourage, « Je m'autorise à », le lien Notion ;
  - 01 : l'objectif boussole à relire ;
  - 02 : les moteurs, sans champ dans la cartographie ;
  - 03 : les sources de stress, le profil ;
  - 04 : les seuils, « cette piste » ;
  - 05 : les 3 valeurs, les fiches sans critères ;
  - 07 et 08 : ce que le carnet de route et le business plan reprennent des pistes.
- La synthèse audit-carnets-2026-10/synthese.html en entier, en particulier les sections 02 (constats transversaux) et 06 (conditions de remplissage).
- workbooks/carnet-1.json à workbooks/carnet-5.json, les modèles à suivre, et workbooks/chap6.json, le contenu actuel.

3. Ce qu'il faut construire
workbooks/carnet-6.json, cible 2 h d'écriture.
- Une page « Avant de commencer » : la météo (c6.meteo) et le récapitulatif de la séance 5.
  - Une ligne par valeur, reportée de la grille du carnet 5 (c5.grille).
  - « Ce que la séance a confirmé » et « Ce qu'elle a déplacé » : deux cases.
- Les exercices de la carte :
  - votre cartographie : une seule page de reports. Le profil et ses forces (c4.profil), la cartographie des énergies (c3.energies), les moteurs (c2.moteurs), la grille anti-compromis (c5.grille), les limites hors argent (c5.limites). Les seuils (c4.seuils) vont dans une zone « à garder pour vous » ;
  - le retour de vos proches : trois cartes, une par proche sollicité au carnet 5 (c5.entourage), avec le prénom, les métiers suggérés et ce qui les y fait penser. Puis « Ce qui me parle vraiment » et « Ce qui ressemble plutôt à ce qu'on attend de moi ». Le protocole ouvre l'exercice ;
  - les ressources, placées avant les pistes, avec des liens à jour (MétierScope pointe encore vers pole-emploi.fr) ;
  - dix pistes (c6.pistes) : 5 réalistes et 5 audacieuses, avec une colonne « D'où vient cette piste ». Elles partent du fil des pistes (reports de c2.livrable à c5.livrable), des suggestions des proches et de « Je m'autorise à » (c1.autorisation).
- Une fin de carnet avec c6.livrable : les dix pistes qualifiées. La séance 6 en retient 3.
- Les marques fixed de la section 8 : le protocole, la définition des seuils, les renvois entre carnets. Le reste s'adapte.
- À trancher dans le plan : la place de l'option « Initiation à l'IA », qui ouvre la séance 6, et le fil des pistes en fin de carnet 6 (le carnet 6 le consomme).

4. Les règles à tenir
- Aucune mention du MBTI, ni de code de type.
- Aucun chiffre sans source, aucun chiffre personnel dans un exemple. Les seuils restent ceux de la personne : on les reporte, on ne les commente pas.
- Le ton de la DA : vouvoiement, jamais « coach », pas de registre de développement personnel.
- Aucune formule genrée : ni participe ni adjectif accordé dans les amorces en « je » (« Je suis à ma place quand », pas « Je me sens aligné·e » ; « ce qui m'a fait agir », pas « ce qui m'a poussé »), ni point médian.
- Un exemple contrasté par exercice, d'un métier au nom épicène, différent de ceux des carnets 1 à 5 (liste en section 5 de la feuille de route). Pas d'exemple sur un exercice de tri qu'il orienterait.
- Le protocole ouvre la première page d'un exercice lourd, l'ancrage ferme la dernière.
- Une question qui demande deux choses a deux cases. Une sous-question fermée (oui ou non) se rouvre.
- Les tailles de case : 1,6 cm au moins pour une phrase, 0,8 cm pour un mot. tests/test_workbooks.py le vérifie.
- Aucune page « (suite) ». S'il manque de la place : une grille de deux colonnes (report compris, avec "columns": 2), un libellé ou un exemple plus court. Mesure la hauteur des blocs avant de rendre (repères en section 5 de la feuille de route).

5. Méthode
a. Commence par me montrer le plan du carnet 6, page par page, avec les durées et leur total, et les choix à trancher en fin de message. Attends ma réponse avant d'écrire le JSON.
b. Écris le JSON. Ajoute Scripts/main_generate_carnet_6.py, la ligne de tests/test_cli_documents.py, et l'entrée carnet-6 du catalogue (server/predefined_workbooks.py), avec « (ancien parcours) » sur chap6. Ajoute carnet_6 à la liste des scripts de CLAUDE.md.
c. Rends chaque page en PNG dans previews/ avec pymupdf et relis-les une à une. Mesure aussi la place libre en bas de chaque page.
d. Lance python -m pytest tests, puis génère tous les Scripts/main_generate_*.py.
e. Relis tout l'audit, point par point, dès ce premier tour :
   - le rapport 06, section par section : exercice par exercice, charge émotionnelle (y compris les « questions plus franches »), fil rouge, écart avec l'app, tableau des recommandations ;
   - la synthèse en entier ;
   - les passages des autres rapports listés plus haut.
   Vérifie chaque point dans le JSON. Pour chaque question de l'ancien chap6.json, dis où elle va, ou pourquoi elle est retirée (les fiches métiers vont au carnet 7, R7). Itère, puis dis-moi ce qui est traité, ce qui est écarté (avec la raison) et ce qui est reporté à une autre PR.
f. Mets à jour la feuille de route :
   - section 1 (état des PR : R5 fusionnée, R6 à ouvrir) ;
   - section 2 (décisions prises pendant R6) ;
   - section 5 (nouvelles conventions, s'il y en a) ;
   - section 7 (ce qui reste ouvert) ;
   - section 8 (le prompt de reprise pour R7, rédigé sur ce modèle).
   Mets aussi à jour la carte, section 6 (budget du carnet 6), et section 7 si un identifiant change.
g. Commite sur la branche. J'ouvrirai la PR avec le bouton.

6. Environnement (Windows, dans un worktree)
- Le Python du venv est ../../../.venv/Scripts/python.exe.
- Pour importer le moteur hors des scripts : PYTHONPATH="Scripts;." (point-virgule sous Windows) et PYTHONIOENCODING=utf-8.
```
