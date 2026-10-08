# Audit du carnet 4 · « Mon rapport à l'argent. »

Sources : PDF (17 pages, 39 champs texte, 12 cases à cocher), `Scripts/workbook_generator/chapters/chap4/`, ordre des pages dans `Scripts/main_generate_chap4.py:11-22`.

## 1. Synthèse

Verdict : carnet riche, au but clair (p. 2), sans conseil financier, mais long (environ 2 h 30, aucune durée affichée) et monotone (32 cases, dont 13 à deux ou trois questions).
1. Aucune sécurité émotionnelle : famille, honte, manque, pouvoir dans le couple (p. 5-7, 15) sans avertissement, droit de passer ni clôture ; rien sur la confidentialité des revenus demandés.
2. Seuils flous saisis deux fois (p. 10-12 : vital, sécurisant, « montant serein », plancher, sans unité) ; la p. 11 fait évaluer « cette piste », qui n'existe qu'au carnet 6.
3. Fil rouge rompu : seuils et tendances absents du carnet 6, minimum vital redemandé au livret sans renvoi, histoire familiale en doublon des carnets 1 et 2.
Les corrections P1 sont des ajouts de texte ; le reste demande surtout de resserrer et de relier.

## 2. Exercice par exercice

### Ouverture (p. 1-2)
- Promesse (`intro.py:11`) « Un salaire et un rythme de vie sécurisés. » : elle promet un résultat, et le rythme de vie n'est pas traité. Proposition : « Vos chiffres posés, pour choisir sans vous mettre en danger. »
- p. 2 (`intro.py:16-21`) : F bien traité. Manquent H et D (ni cadre, ni durée, ni découpage). Ajouter un encadré « Avant de commencer » :
  > « Ce carnet touche à votre histoire familiale, à vos revenus et parfois à des souvenirs de manque ou de gêne. Vos réponses vous appartiennent : vous choisissez ce que vous partagez en séance. Des ordres de grandeur suffisent. N'indiquez ni vos comptes, ni vos dettes, ni les revenus de vos proches. Si une question vous pèse, laissez-la vierge : nous l'aborderons ensemble. Comptez deux heures et demie environ, en trois fois : exercices 1 à 4, puis 5 et 6, puis 7 et 8. »

### Exercice 1 · Récapitulatif MBTI® (p. 3), 10-15 min
- E : récapitulatif guidé sur les dimensions du carnet 3 (`intro.py:41-45`), mais aucun champ pour le type, que redemandent le carnet 6 (p. 4, `chap6/exercices.py:14`) et le livret (p. 2). Aucun pont vers l'argent. A : aucune amorce.
- Recommandation : champ court « Mon type MBTI® (4 lettres) » ; Q3 remplacée par « Votre façon de décider se retrouve-t-elle dans vos choix d'argent : dépenser, épargner, négocier ? », amorce « Je me reconnais surtout quand… ».

### Exercice 2 · Situation actuelle (p. 4), 10 min
- D : la Q1 demande de choisir entre trois états (sécurité, tension, vigilance), dans une case de 4,5 cm (`psychologie.py:12`). En faire un bouton radio à trois valeurs, suivi d'un « pourquoi » d'une ligne.
- Doublon interne : la Q3 (`psychologie.py:15`) reprend Ex6 Q2 (p. 10) et Ex8 Q3 (p. 15). La supprimer ici.
- E : la note « Argent, finances » du carnet 0 (p. 8, `chap0/exercices.py:41`) n'est pas reprise. Proposition : « Dans le carnet 0, vous avez noté votre satisfaction "Argent, finances" sur 10. Quelle note donneriez-vous aujourd'hui, et pourquoi ? »

### Exercice 3 · Histoire avec l'argent (p. 5-6), 25-35 min
- G : l'exercice le plus chargé (manque, tabou, culpabilité, pouvoir dans le couple), sans aucun élément du protocole. La p. 6 Q3 (`psychologie.py:42-43`) peut viser le couple actuel : écrire seul un contrôle économique présent, dans un fichier parfois partagé, est un vrai risque. Reformulation : « Dans la famille où vous avez grandi, l'argent créait-il des rapports de pouvoir, de protection ou de dépendance ? Si cette question touche votre situation actuelle, gardez-la pour la séance. »
- A/F : sur 7 questions, 4 doubles et 5 fermées (« Avez-vous observé… ? ») qui appellent oui ou non. L'intro (`psychologie.py:24`) ne dit pas à quoi servira l'exercice. B : l'histoire est explorée, jamais triée.
- E : doublon avec le carnet 1 (Ex5 héritage 3FVS, Ex6 « stress, absences, argent ») et le « À lire » du carnet 2 (illégitimité, réparation, `chap2/concept.py:16-46`), jamais cités.
- Recommandation : 4 questions ouvertes (fusionner p. 6 Q1 et Q2), un renvoi (« Reprenez votre héritage familial du carnet 1. »), puis :
  - un avertissement : « Ces deux pages parlent de votre famille et de souvenirs parfois lourds. Avancez à votre rythme. » ;
  - un exemple contrasté :
    > Exemple. Réponse de surface : « L'argent n'était pas un problème chez nous. » Réponse exploitable : « On ne parlait jamais de salaire à table. Mon père, artisan, répétait qu'on ne se plaint pas. Aujourd'hui encore, je n'ose pas demander le salaire d'un poste avant l'entretien. »
  - une clôture : « De cette histoire, je garde… Je laisse… ».

### Exercice 4 · Premières expériences (p. 7), 15-20 min
- D/I : 4 cases de 43 pt (1,5 cm, plancher de `templates.py:268`), y compris pour « un souvenir marquant : manque, honte, dépendance » (`psychologie.py:68`) : une ou deux lignes, police qui rétrécit, écriture à la main impossible. Couper la page après la Q2 (`layout.page_break()`).
- A : l'encadré « Idées reçues fréquentes » (`psychologie.py:56-61`), meilleur matériau du carnet, n'est exploité nulle part. Ajouter « La phrase que j'ai le plus entendue : … » et « La phrase que je choisis aujourd'hui : … » (ce que fait l'app web).
- G : clôture après la Q4 : « Avec le recul, ce souvenir m'apprend que… ».

### Exercice 5 · Argent et projet (p. 8-9), 20-25 min
- D/I : 6 questions pour 5 champs. La p. 9 Q2 (`moteurs.py:24-26`) colle deux questions, et la plus franche (« Qu'est-ce que vous n'osez pas demander, viser ou négocier aujourd'hui ? ») se perd en fin de libellé : la séparer.
- Doublons : genre (p. 6 et 9), mérite-travail (encadré p. 7, p. 8 Q3 `moteurs.py:18`, carte « Le méritant » p. 13). Retirer « Associez-vous gagner de l'argent et beaucoup travailler ? ».
- D : p. 8 Q3 en grille d'aisance de 1 à 5 (`add_rating_grid`) : demander une augmentation, négocier un salaire d'embauche, fixer un prix, parler de son salaire à un proche ; puis « La situation la plus difficile pour moi, c'est… ».
- B : la p. 8 Q2 (renoncements) appelle un retournement : « Je ne veux plus accepter un poste seulement pour… ».
- Exemple contrasté pour « n'osez pas » :
  > Exemple. Surface : « Je n'ose pas trop négocier. » Exploitable : « Lors de mon embauche comme comptable, j'ai accepté le premier chiffre proposé. Je n'ose pas demander le salaire avant le deuxième entretien, de peur de passer pour quelqu'un qui ne pense qu'à l'argent. »

### Exercice 6 · Minimum financier (p. 10-12), 25-40 min
- F : quatre notions voisines non définies (minimum vital, minimum sécurisant, « montant serein » : revenu ou épargne ?, seuil plancher), ni net ou brut, ni personnel ou foyer (le livret dit « pour le foyer »).
- D : p. 10, trois cases de 4,6 cm pour un chiffre, que la p. 12 fait reporter : double saisie.
- E/I : la p. 11 Q3 (`moteurs.py:47`) parle de « cette piste professionnelle » : aucune piste n'existe avant le carnet 6. La déplacer dans ses fiches métiers.
- Données sensibles : les chiffres sont justifiés (c'est le livrable) ; ni dettes ni patrimoine demandés, c'est bien. Manque « Une fourchette suffit ».
- Recommandation (refonte légère) : fusionner les p. 10 et 12 en une carte de seuils définis, unité affichée (« € nets par mois, pour vous ») :
  > « Minimum vital : vos charges essentielles couvertes, sans marge. Minimum sécurisant : ces charges, plus une marge pour les imprévus. Revenu cible : ce que vous visez à terme. Faites le calcul sur une feuille à part (logement, transport, enfants, assurances, remboursements) et ne reportez que le total. »
  
  Supprimer le « seuil en dessous duquel… » (doublon du minimum sécurisant). Garder la durée acceptable d'une baisse, puis « Ce que j'accepte pendant la transition » et « Ce que je n'accepte pas » en deux cases.

### Exercice 7 · Huit tendances (p. 13-14), 15-20 min
- F : bien expliqué. Les tendances « ne sont pas des cases » et peuvent être une ressource ou un frein (`archetypes.py:41-43`).
- D : « Cochez celles qui vous correspondent » : on peut cocher les huit. Proposer « Cochez deux ou trois tendances au plus. » La case finale (`archetypes.py:53-56`) mêle trois questions et les questions clés n'ont aucun champ : la découper en « Ma tendance principale : … », « Elle m'aide quand… », « Elle me freine quand… », « Ma réponse à sa question clé : … ».
- Ton : noms au masculin (« Le sécuritaire », « Le méritant »…), et « Le plaisir » rompt la série (`archetypes.py:25`). Nommer des tendances : la sécurité, le mérite, l'indépendance, la générosité, l'évitement, l'ambition, le plaisir, la réparation.
- G : « Le réparateur » (« blessure sociale, familiale ») et « L'évitant » touchent à la honte, sans filet.

### Exercice 8 · Synthèse (p. 15), 15 min
- G : « Qu'est-ce qui vous fait le plus peur dans le manque d'argent ? » (`cloture.py:10-11`), question franche bienvenue, ferme le carnet sans ancrage : on termine sur sa peur.
- A/B : ni amorce ni sortie vers la suite. Amorces proposées :
  > « Si j'avais plus d'argent, je m'autoriserais à… » / « Ce qui me fait peur dans le manque, c'est… » / « Gagner davantage me gênerait parce que… » / « Pour ma prochaine piste, l'argent doit me permettre de… » / « Aujourd'hui, avec le recul, je sais que… »

### Livrable et dos (p. 16-17), 5 min
- C : la zone « Mes notes pour la prochaine séance » (476 × 362 pt) n'a aucune consigne. La découper : « Ce qui m'étonne dans ce carnet : … », « Ce que je préfère aborder en séance plutôt que par écrit : … », « Une question que je n'ai pas tranchée : … » (la deuxième sert aussi de filet, axe H).
- Engagements (`cloture.py:24-26`) concrets et dans le ton ; « Je parle de rémunération sans m'en excuser » est réussi.

## 3. Charge émotionnelle

Aucun des trois éléments du protocole n'apparaît dans le carnet. Le carnet 0 ne pose pas de cadre non plus : on y lit seulement « le tri se fait en séance » et « nous les relisons ensemble ».

| Exercice | Niveau | Avertissement | Optionnalité | Clôture | Question plus franche possible (une fois le protocole posé) |
|---|---|---|---|---|---|
| Ex3 Histoire (p. 5-6) | fort | absent | absente | absente | « Ce que l'argent a coûté dans ma famille, c'est… » |
| Ex4 Premières expériences (p. 7) | fort (honte, manque) | absent | absente | absente | « Le souvenir d'argent que je n'ai jamais raconté (un mot suffit) : … » |
| Ex5 Argent et projet (p. 8-9) | moyen | absent | absente | absente | « Le chiffre que je n'ose pas dire à voix haute pour mon prochain poste : … » |
| Ex6 Minimum (p. 10-12) | moyen (confronte à la précarité) | absent | absente (pas de « fourchette suffit ») | annotation p. 12, sans ancrage | « Ce qu'un revenu plus bas me coûterait vraiment : … » |
| Ex7 Tendances (p. 13-14) | moyen | partiel (« ne sont pas des cases ») | absente | absente | « Si je gagnais plus que mes parents, je ressentirais… » (loyautés, carnet 2) |
| Ex8 Synthèse (p. 15) | fort (peur du manque) | absent | absente | absente | déjà franche : ajouter la clôture |

## 4. Fil rouge

**Entrées**
- Carnet 3 (MBTI®) : reprise explicite en Ex1, guidée sur les dimensions, mais sans le type et sans pont vers l'argent.
- Carnet 0, Ex3 (note « Argent, finances ») et carnet 2, Ex3 (le moteur « sécurité financière », p. 8) : entrées implicites, non reprises.
- Carnet 1 (Ex5-6) et « À lire » du carnet 2 (illégitimité qui « peut vous retenir de demander une augmentation », réparation, « Il faut souffrir pour réussir ») : le carnet en a besoin sans les citer.

**Sorties**
- Seuils chiffrés (p. 12), « pour évaluer chaque piste » : le carnet 6 s'y engage (`chap6/ressources.py:47`) sans leur donner de place, ni case « seuils » dans la cartographie (`chap6/exercices.py:12-18`), ni ligne rémunération dans les fiches (`chap6/exercices.py:62-67`). Ajouter « Mes seuils financiers » à la cartographie et, sur chaque fiche, « Rémunération observée · mon minimum est atteint : oui / à terme / non ».
- Livret, thème 7 (p. 14, `livret/plan_action.py:29-35`) : redemande le « salaire net minimum vital pour le foyer » sans renvoi, avec un exemple très typé (« revenu net cadre », « mes 3 enfants ») qui sera recopié. Écrire : « Reprenez vos seuils du carnet 4. »
- Tendances (Ex7) : jamais reprises. Les tensions du carnet 5 (« Sens / rémunération », « Liberté / sécurité », `chap5/synthese.py:14`) offrent un renvoi naturel.
- La séance sur l'argent n'est jamais récapitulée : le carnet 5 n'a pas d'exercice de récapitulatif, et le carnet 6 récapitule les valeurs.

**Doublons** : internes (sécurité ×3, mérite ×3, genre ×2, chiffres ×2) ; externes (carnet 1 Ex5-6, carnet 2 « À lire »).

**Ruptures** : « cette piste » p. 11 (une entrée jamais produite) ; seuils et tendances (des sorties sans case qui les reprenne).

## 5. Écart avec l'app web

`server/predefined_workbooks.py:554-687` décrit un autre carnet, « Valeurs, limites et argent. » : météo, limites par domaine (proches du 360° du carnet 1), idées reçues confrontées aux faits avec exemples, deux questions de seuils et quatre engagements.
L'exemple chiffré du web (« 2 800 € net… 4 200 € », l. 647) risque d'ancrer les réponses.
Absents du web : le récapitulatif MBTI®, l'histoire familiale et le genre, les premières expériences, l'argent et le projet, les huit tendances, la synthèse.
Absents du CLI : la météo, les limites non financières et le retournement « idée reçue → principe de réalité », plus utile que l'encadré passif de la p. 7.

## 6. Recommandations classées

| Priorité | Type | Page(s) | Constat | Recommandation |
|---|---|---|---|---|
| P1 | correction rapide | 2 | Aucun cadre : confidentialité, droit de passer, chiffres sensibles | Encadré « Avant de commencer » (texte en §2) |
| P1 | correction rapide | 5-7, 15 | Protocole absent sur les Ex3, Ex4 et Ex8 | Avertissement en tête de l'Ex3, phrase d'optionnalité, phrase d'ancrage à la fin des Ex3, Ex4 et Ex8 |
| P1 | correction rapide | 6 | La Q3 sur le pouvoir et le contrôle dans le couple peut viser la situation actuelle | Reformuler au passé, avec renvoi vers la séance (§2) |
| P2 | correction rapide | 7 | 4 cases de 1,5 cm, dont le souvenir de honte | `page_break()` après la Q2, cases d'au moins 4 cm |
| P2 | refonte | 10-12 | Seuils non définis, sans unité, saisis deux fois | Une carte de seuils définis, puis 3 questions |
| P2 | correction rapide | 11 | « Cette piste » n'existe pas avant le carnet 6 | Déplacer vers les fiches métiers du carnet 6 |
| P2 | refonte | carnet 6 p. 4, 7-10 ; livret p. 14 | Seuils et tendances jamais repris | Case « Mes seuils », ligne rémunération par fiche, renvoi au livret |
| P2 | refonte | carnet 5 | Séance sur l'argent jamais récapitulée | Récapitulatif en ouverture du carnet 5 |
| P2 | correction rapide | tout | Ni amorce ni exemple ; 13 cases doubles sur 32 ; questions fermées | `subtitle` et `example` de `QuestionItem` ; un exemple pour Ex3, Ex5, Ex6 |
| P2 | correction rapide | 9 | Deux questions dans un champ | Séparer |
| P2 | correction rapide | 15 | Synthèse sans amorce ni critère pour la suite | Amorces du §2 |
| P2 | correction rapide | 3 | Ni type MBTI® ni pont vers l'argent | Champ « 4 lettres », question pont |
| P2 | correction rapide | 7 | Idées reçues non exploitées | Champs « entendue » et « choisie » |
| P2 | correction rapide | 13-14 | Cochage illimité, case finale triple | 2 ou 3 tendances, puis 3 champs |
| P2 | correction rapide | 2, en-têtes | Aucune durée (environ 2 h 30) | Durée par exercice, trois temps |
| P2 | correction rapide | 16 | Notes sans consigne | Trois amorces (surprise, à aborder, non tranché) |
| P3 | correction rapide | 4, 8, 9 | Doublons internes | Supprimer p. 4 Q3 et fin de p. 8 Q3 |
| P3 | refonte | 8 | Format monotone | Grille d'aisance 1-5 |
| P3 | correction rapide | 4 | Choix à trois valeurs en grande case | Bouton radio, puis « pourquoi » |
| P3 | correction rapide | 5-6 | Doublon non cité des carnets 1 et 2 | Renvoi ; 4 questions au lieu de 7 |
| P3 | correction rapide | 13-14 | Noms au masculin, série incohérente | Nommer les tendances |
| P3 | correction rapide | 1 | Promesse de résultat, rythme de vie absent | Nouvelle promesse (§2) |
| P3 | refonte | web | Copie web divergente | Aligner ; porter « idée reçue → faits » dans le CLI |
