# Audit du carnet 2 « Mon parcours »

PDF de 14 pages et 71 champs. Code : `Scripts/workbook_generator/chapters/chap2/`, ordre des pages dans `Scripts/main_generate_chap2.py:12-22`.

## 1. Synthèse

Verdict : un carnet riche aux formats variés, bien ancré dans les héritages du carnet 1, mais faible sur son axe central et sans aucun filet alors que c'est le plus intime du parcours.
1. Aucun protocole de sécurité ni rappel du cadre sur les pages à forte charge : À lire p. 3-4, vallées p. 9, épreuves p. 10 (P1).
2. L'analyse des expériences (p. 6-7) sépare les compétences du ressenti (« aimé / pas aimé »). Elle ne croise jamais ce qui coûte et ce qui recharge, et ne retourne aucun irritant en critère (P2).
3. Le « fil rouge » promis comme livrable n'est écrit dans aucun champ. Ses sorties (moteurs, compétences de vie) ne sont reprises ni par le carnet 6 ni par le livret (P2).

## 2. Exercice par exercice

### Ouverture (p. 1-2) · 2 min
- **D** : aucune durée, ni par exercice ni au total, alors que le carnet 5 en affiche (« · 10 MIN »). J'estime le total entre 2 h 35 et 3 h 35 hors bonus. Rien ne dit qu'on peut le faire en plusieurs fois.
- **H** : aucun rappel du cadre (`intro.py:16-19`). Le carnet 0 ne le pose pas non plus : on y lit seulement « le tri se fait en séance ».
- **Reco** : sous l'intro, écrire « Ce carnet vous appartient : vous choisissez ce que vous partagez en séance. Certaines pages touchent à la famille et aux moments difficiles. Vous pouvez passer une question : notez « à voir en séance ». Comptez environ trois heures, en trois ou quatre fois. »

### À lire · Comprendre ses racines (p. 3-4) · 10-15 min
- **F (lisibilité)** : les phrases sont courtes et les images parlent (logiciel, costume mal taillé, livre de comptes). Mais on compte neuf notions en deux pages, alors que l'ouverture en annonce trois. « Névrose de classe » (`concept.py:31-33`) est un terme clinique qui inquiète plus qu'il n'éclaire, même suivi de « Ce n'est pas une maladie ». La section sur l'activité empêchée (`concept.py:52-59`) n'est reliée à aucun exercice du carnet. Le livret la reprend p. 5 sous un autre nom (« travail empêché »).
- **G** : la charge est forte (honte, culpabilité, « L'échec devient une façon de leur rester fidèle »). Il n'y a ni avertissement ni clôture.
- **A** : la lecture est passive. Les « trois outils » (`concept.py:65-78`) ne sont appliqués nulle part.
- **E** : au carnet 1 (Ex. 4), le « sac à dos » désigne ce que l'on dépose ; ici, il désigne l'habitus. « Réussir sans trahir » répète l'annotation du carnet 1, p. 7.
- **Ton** : « celles qui vous ont jugé » (`concept.py:68`) impose un genre.
- **Reco** :
  - Ouvrir sur : « Ces pages parlent de famille, de loyauté, parfois de honte. Lisez-les à votre rythme. Si une idée vous remue, notez-la pour la séance. »
  - Écrire « le malaise de changer de milieu (le sociologue Vincent de Gaulejac parle de « névrose de classe ») ».
  - Renommer la section « Le bagage social (l'habitus) ». Écrire « celles qui portaient un jugement sur vous ».
  - Changer l'encadré « À retenir » en « Et vous ? » facultatif : « Une personne de ma famille qui m'a donné confiance : … » / « Une phrase de famille qui revient : « … » » / « Aujourd'hui, avec le recul, je sais que… ».

### Exercice 1 · Récapitulatif (p. 5) · 15-20 min
- **E** : la séance n'est pas nommée, alors que les carnets 4 et 6 nomment la leur. Aucun renvoi à l'objectif boussole ni à la matrice 3FVS du carnet 1. La question 3, « que voulez-vous garder, et que voulez-vous faire évoluer ? » (`intro.py:42`), refait cette matrice : c'est un doublon.
- **A** : pas d'amorce. **D** : quatre cases de 2,7 cm, bien adaptées.
- **Reco** : « Revenez sur la séance consacrée à votre état des lieux (carnet 1). » Puis ces amorces : « En séance, j'ai vu que… » / « Mon objectif boussole reste, ou devient : … » / « Ce que je veux vérifier dans ce carnet : … ».

### Exercice 2 · Analyse du parcours (p. 6-7) · 45-60 min
- **B (constat central)** :
  - Compétences et ressenti occupent des cases séparées (`exercices.py:37-39`). Rien ne distingue « je sais le faire et cela me recharge » de « je sais le faire et cela m'épuise ».
  - « Ce que je n'ai pas aimé » n'est jamais retourné en critère : la personne risque de ruminer.
  - Rien ne demande comment le poste a commencé ni pourquoi il s'est terminé. Or l'exercice 3 attend justement ce type de schéma (« partir au bout d'un an », `exercices.py:56`).
- **F** : la consigne dit « Détaillez chaque expérience significative » (`exercices.py:26`), mais il n'y a que quatre fiches. Le champ parle de « sujet d'étude », l'intro de « emploi, stage, bénévolat ».
- **A** : pas d'exemple. **D** : les cases « missions » et « compétences » mesurent 7,5 × 1,7 cm, soit deux lignes manuscrites. Pourtant, 3 à 4 cm restent libres en bas des p. 6-7.
- **Reco** :
  - Consigne : « Choisissez les quatre expériences qui vous ont le plus appris, pas forcément les plus récentes. Faites-le en deux fois si besoin. »
  - Remplacer « aimé / pas aimé » par « Ce qui me donnait de l'énergie » / « Ce qui me coûtait ». Ajouter « Comment ce poste a commencé, pourquoi il s'est terminé ».
  - Exemple contrasté, avec l'étiquette « Exemple · un poste en centre d'appels ». Surface : « Le contact client. » Exploitable : « Rattraper au téléphone un client qui voulait résilier, trouver la solution pendant l'appel, et le garder. »
  - Après les fiches, ajouter une page « Vos quatre zones », reprise du carnet 3 web, puis trois fois « Je ne veux plus… donc mon prochain poste doit… ». Agrandir les cases de 1,9 à 2,4 cm.

### Exercice 3 · Fil rouge et moteurs (p. 8) · 15-20 min
- **A** : l'exemple est visible et étiqueté, mais c'est une liste et non un contraste. Pas d'amorce.
- **F** : « moteur » n'est pas défini. Ses exemples recoupent la liste de valeurs du carnet 5. On ignore s'il faut cinq moteurs ni s'il faut les classer.
- **B** : rien ne distingue « je le veux » de « on l'attend de moi », alors que l'À lire vient d'en parler (mythe familial, réparation).
- **E** : le fil rouge n'est jamais formulé, alors que c'est le livrable (`cloture.py:31`). Environ 6 cm restent libres en bas de page.
- **Reco** :
  - Amorces : « Je choisis souvent… » / « Je pars quand… » / « Je reste quand… ».
  - Exemple contrasté. Surface : « Je change souvent de poste. » Exploitable : « Je pars quand je n'apprends plus, et je reste là où un nouveau projet arrive chaque semestre. »
  - Pour chaque moteur : « Vu dans l'expérience n° … » et une case « Je le veux / On l'attend de moi ».
  - Ajouter : « Mon fil rouge en une phrase : ce qui relie mes expériences, c'est… ».

### Exercice 4 · Ligne de vie (p. 9) · 25-35 min
- **G** : la charge est forte. L'intro invite au « personnel » sans aucun élément du protocole. Le bandeau « Les vallées · apprentissages » et le champ « Ce que j'en retiens » obligent à tirer une leçon de chaque épreuve.
- **D** : l'ordre est imposé (sommet, vallée, sommet, vallée, sommet, `exercices.py:69-72`). L'intensité n'est jamais demandée. Les cases « date et événement » mesurent 5 mm de haut (`exercices.py:92`), trop peu pour l'écriture manuscrite.
- **B** : l'énergie est citée dans l'intro mais ne figure dans aucun champ.
- **Reco** :
  - Dans l'intro : « Ces moments peuvent être lourds à revivre. Vous choisissez ce que vous notez : un mot suffit. Si une vallée vous semble trop lourde à écrire, laissez la case vierge : nous l'aborderons ensemble. »
  - Libellés : « Ce qui m'a donné de l'énergie » et « Ce qui m'a permis de traverser ». Ancrage final : « Aujourd'hui, avec le recul, je sais que… ».
  - Consigne : « Placez vos moments dans l'ordre où ils sont arrivés ; laissez vides les cases inutiles. »

### Exercice 5 · Compétences de vie (p. 10) · 20-25 min
- C'est un bon exercice : catégories claires, flèche de l'expérience vers la compétence, un exemple par ligne.
- **G** : « divorce » est le premier exemple de l'en-tête (`exercices.py:156`). La ligne « Défis et épreuves » n'est pas présentée comme facultative.
- **B** : aucune question sur l'envie : une compétence née d'une épreuve n'est pas forcément une compétence qu'on veut exercer. **E** : aucun fait n'est demandé, alors que le livret promet des « compétences prouvées par des faits ».
- **I** : les infobulles sont vides dans la colonne 1 et valent « Enseignement N » dans la colonne 2 (`components.py:716-719`, appelé par `exercices.py:158-164`).
- **Reco** :
  - En-tête : « (ex : déménagement, voyage, association…) ». Ligne 2 : « (facultatif) ».
  - Consigne finale : « Entourez les compétences que vous avez envie d'utiliser dans votre prochain poste. »
  - Exemple contrasté. Surface : « Aidant → organisation. » Exploitable : « Coordonner pendant deux ans les rendez-vous médicaux d'un parent, avec trois frères et sœurs → planifier sous contrainte, répartir les tâches. »

### Exercice 6 · Arbre de vie (p. 11) · 20-30 min
- **F** : l'intro dit « le tronc (vos forces) », l'étiquette « Vos compétences et vos valeurs » (`exercices.py:191` et `236`). Les fruits portent une double consigne (« Vos réussites, ce que vous avez reçu ») qui recoupe les racines.
- **E** : la consigne ne dit pas que l'arbre est une synthèse des exercices 2 à 5. Les feuilles reprennent l'exercice 4 du carnet 0.
- **D** : les racines (8,8 × 1,1 cm, `exercices.py:240`) et le sol (4,4 × 1,3 cm) tiennent en une ligne manuscrite. Ce sont pourtant « votre histoire, vos origines ».
- **G** : l'annotation « Les épreuves font partie de l'arbre, sans le résumer » est une bonne touche.
- **Reco** : « Reprenez ce que vous avez noté dans ce carnet : trois compétences des exercices 2 et 5 pour le tronc, vos sommets pour les fruits. Quelques mots par zone suffisent. » Libellés « Vos forces » et « Vos réussites ». Racines de 1,3 à 2 cm.

### Bonus · Interview (p. 12) · 45-90 min, rendez-vous compris
- **E** : l'exercice relève de l'exploration (carnet 6). Il ignore les mentors notés au carnet 1 (Ex. 7).
- **F** : aucune aide pour choisir ni solliciter la personne. Obtenir un rendez-vous entre deux séances est souvent irréaliste. Les questions sont bonnes.
- **Reco** : « Choisissez si possible l'un des mentors notés au carnet 1. Si le rendez-vous n'est pas possible avant la prochaine séance, gardez cette page pour la phase d'exploration. » Ajouter la question « Quel a été votre parcours jusqu'à ce métier ? ».

### Livrable (p. 13) · 5-10 min
- **C** : « Mes notes pour la prochaine séance » est une case unique de 16,8 × 12,8 cm, sans amorce (`components.py:464-468`) : elle intimide. Le texte du livrable oublie les compétences de vie (`cloture.py:32`).
- **G** : l'engagement « Je reconnais la valeur de chacune de mes expériences, y compris les plus difficiles » (`cloture.py:27`) demande de cocher un sentiment.
- **Reco** : découper la case en trois zones : « Ce qui m'étonne dans ce carnet » / « À aborder en séance (2 ou 3 points) » / « Ce que j'ai laissé vierge, et pourquoi ». Remplacer l'engagement par « Je regarde mes expériences difficiles à mon rythme, en séance si besoin. »

## 3. Charge émotionnelle

| Exercice | Niveau | Avertissement / optionnalité / clôture | Question plus franche, une fois le protocole en place |
|---|---|---|---|
| À lire p. 3-4 | Fort | Absent / absent / absent | « La phrase de famille qui décide encore parfois à ma place : … » |
| Ex. 1 Récap (Q2-Q3) | Moyen | Absent / absent / absent | « Ce que je n'ose pas faire, de peur de décevoir ma famille : … » |
| Ex. 2 « pas aimé » | Faible à moyen | Absent / absent / absent | « Ce que je ne veux plus jamais revivre dans un poste : … donc mon prochain poste doit… » |
| Ex. 3 Schémas | Moyen | Absent / absent / absent | « Le schéma que je répète et qui me coûte le plus : … » |
| Ex. 4 Vallées | Fort | Absent / absent / partiel (« Ce que j'en retiens » force la leçon) | « La vallée dont je parle le moins : … » |
| Ex. 5 Défis et épreuves | Moyen à fort | Absent / absent / absent | « L'épreuve qui m'a appris ce que personne ne sait de moi : … » |
| Ex. 6 Racines | Moyen | Absent / absent / partiel (annotation) | Inutile : la page est une synthèse |
| Livrable, engagement 1 | Moyen | Sans objet | Assouplir plutôt que durcir |

## 4. Fil rouge

**Entrées.** Le récap et l'À lire reprennent le carnet 1 (matrice 3FVS, image du travail), et l'arbre reprend le carnet 0 (entourage), mais sans jamais le dire. Les mentors du carnet 1 et l'objectif boussole ne servent pas. L'ordre aussi pose problème : l'À lire explique après coup des notions que le carnet 1 a déjà fait travailler.

**Sorties.**
- La ligne de vie et l'arbre sont repris explicitement par le récap du carnet 3. C'est le seul relais.
- Les moteurs sont annoncés dans l'intro du carnet 6, mais sa cartographie n'a pas de champ « moteurs ». Les fiches métiers ne les utilisent pas non plus, malgré l'engagement « Je garde mes moteurs en tête pour évaluer chaque piste ».
- Les compétences de vie et l'analyse du parcours devraient nourrir le livret (savoir-faire, transférables, récit d'action, socle de confiance). Le livret ne cite aucun carnet.
- Les « pas aimé » et les vallées devraient alimenter les exercices 2 et 7 du carnet 5 et la page « Ce qui vide mes batteries » du livret.

**Doublons.** Récap Q3 et matrice 3FVS. « Réussir sans trahir » et le carnet 1, p. 7. « Réparation » et le « réparateur » du carnet 4. Moteurs et valeurs du carnet 5, lui-même intitulé « moteurs profonds ». Feuilles et entourage du carnet 0. « Activité empêchée » et le « travail empêché » du livret. Interview et enquêtes métier du carnet 6.

**Ruptures.** Le « fil rouge professionnel » n'est formulé nulle part. Les outils de l'À lire ne servent à rien ensuite. Aucun carnet ne croise énergie et compétence avant le livret.

## 5. Écart avec l'app web

- Le carnet 2 web (`server/predefined_workbooks.py:282-415`) contient : météo, héritage « reçu / choisi », modèles inspirants, arbre en 4 quadrants, livrable.
- On n'y trouve ni À lire, ni récap, ni analyse des expériences, ni moteurs, ni ligne de vie, ni compétences de vie, ni interview.
- L'héritage et les mentors sont au carnet 1 côté CLI, au carnet 2 côté web.
- Les fruits de l'arbre web sont les « compétences transférables ». Le web emploie aussi « injonction » (l. 330).
- Les « quatre zones » qui croisent énergie et compétence (l. 488-499) n'existent que dans le carnet 3 web : c'est la pièce qui manque au carnet 2 CLI.

## 6. Recommandations classées

| Priorité | Type | Page(s) | Constat | Recommandation |
|---|---|---|---|---|
| P1 | Correction rapide | 2 | Aucun cadre (confidentialité, droit de passer), ici comme au carnet 0 | Encadré « Ce carnet vous appartient… notez « à voir en séance » » |
| P1 | Correction rapide | 3-4 | Charge forte, « névrose de classe » sans précaution | Avertissement, périphrase sourcée, ancrage final |
| P1 | Correction rapide + refonte légère | 9 | Vallées personnelles sans protocole ; leçon imposée | Avertissement, case vierge autorisée, « Ce qui m'a permis de traverser », ancrage |
| P2 | Refonte | 6-7 | Compétences et ressenti séparés | « Énergie / Coût » par expérience, plus une page « quatre zones » |
| P2 | Refonte légère | 7 | Irritants jamais retournés en critères | Trois lignes « Je ne veux plus… donc mon prochain poste doit… » |
| P2 | Correction rapide | 6-7 | « Chaque expérience » contre 4 fiches ; pas d'exemple ; ni début ni fin de poste | Consigne de choix, exemple contrasté, champ « Comment ce poste a commencé, pourquoi il s'est terminé » |
| P2 | Correction rapide | 6-7 | Cases de 1,7 cm, alors que 3 à 4 cm restent libres | Hauteur 1,9 → 2,4 cm (`exercices.py:37-39`) |
| P2 | Correction rapide | 8 | Le fil rouge, livrable du carnet, n'est écrit nulle part | « Mon fil rouge en une phrase : … » |
| P2 | Refonte légère | 8 | Moteurs non définis, sans lien aux expériences ni « je veux / on attend de moi » | Colonne « expérience n° », case « Je le veux / On l'attend de moi » |
| P2 | Correction rapide | 10 | « Divorce » en exemple, épreuves non facultatives, aucune question d'envie | « Déménagement », « (facultatif) », « Entourez les compétences… » |
| P2 | Correction rapide | 5 | Récap vague et doublon de la matrice 3FVS | Nommer la séance, amorces reliées à l'objectif boussole |
| P2 | Correction rapide (autres carnets) | Carnet 6 p. 4, livret p. 8-9 | Moteurs et compétences de vie jamais repris | Champ « Mes moteurs (carnet 2) » ; « Reprenez vos compétences de vie (carnet 2, p. 10) » |
| P2 | Refonte légère (composant partagé) | 13 | Case de notes sans amorce ; engagement qui fait cocher un sentiment | Trois zones (surpris / à aborder / laissé vierge) ; reformuler l'engagement |
| P2 | Correction rapide | Toutes | Aucune durée ni mention « en plusieurs fois » | Durée dans les eyebrows, total d'environ 3 h annoncé p. 2 |
| P2 | Refonte | 3-4 | Lecture passive, outils jamais appliqués | Encadré « Et vous ? » facultatif |
| P2 | Correction rapide | 11 | Racines et sol sur une ligne ; libellés incohérents | Agrandir, aligner les libellés, dire « reprenez… » |
| P3 | Correction rapide | 3 | « Sac à dos » au sens différent du carnet 1 | « Le bagage social (l'habitus) » |
| P3 | Correction rapide | 4 | « qui vous ont jugé » impose un genre | « qui portaient un jugement sur vous » |
| P3 | Correction rapide | 4 / livret p. 5 | Activité empêchée et travail empêché désignent la même notion | Un seul terme |
| P3 | Correction rapide | 12 | Bonus hors thème, sans mode d'emploi | Mentors du carnet 1, report permis, question sur le parcours |
| P3 | Correction rapide | 10 | Infobulles vides ou « Enseignement N » | Passer `left` et `right` dans `rows_data` |
| P3 | Correction rapide | 6 | « Sujet d'étude » contre « emploi, stage, bénévolat » | Harmoniser |
