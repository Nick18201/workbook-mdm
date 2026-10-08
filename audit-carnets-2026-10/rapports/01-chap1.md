# Audit du carnet 1 : « L'état des lieux »

## 1. Synthèse

Carnet soigné (chaque zone a son champ, amorces sur la boussole et le sac à dos, rythme varié), mais premier carnet à toucher à la peur et à la famille, sans filet. Les trois problèmes principaux :
1. **Ni protocole de sécurité ni rappel du cadre** sur les exercices 4 à 6 (peur, dette familiale, souffrance des parents) : pas d'avertissement, pas de droit de laisser vierge, pas de clôture (P1).
2. **Des cases inversées par rapport à la profondeur attendue**, sans exemple ni durée nulle part : 13 cm pour l'humeur du jour, 1,1 cm pour « l'effet de leur travail sur la vie de famille » (P2).
3. **Un fil rouge fragile** : triple doublon avec chap0 (objectif, état d'esprit, domaines de vie), doublons internes (Ex4, 5, 7), et des sorties que personne ne reprend ensuite (boussole, météo, anti-modèles, mentors) (P2).

## 2. Exercice par exercice

### Ouverture (p. 1-2) · 2 min
- **F** : le but est clair (« Il servira de référence pour mesurer le chemin parcouru », `intro.py:12-16`). En revanche, « matrice 3FVS » (`intro.py:22`) n'est expliquée nulle part dans le dépôt.
- **D** : aucune durée, pas de total, pas de « en plusieurs fois ». Le carnet 5 affiche pourtant « · 10 MIN » dans ses en-têtes. Durée réelle estimée : **1 h 50 à 2 h 30**.
- **H** : aucun rappel du cadre ; chap0 dit seulement « nous les relisons ensemble » (p. 3).
- **Reco (p. 2)** : « Comptez environ 2 h. Faites-le en deux ou trois fois : les exercices 1 à 4 portent sur votre situation, les exercices 5 à 7 sur ce que vous avez reçu. Vos réponses vous appartiennent : vous choisissez ce que vous partagez en séance. Vous pouvez passer une question. »

### Exercice 1 · Météo (p. 3) · 5-10 min
- **I** : les quatre météos sont des cases à cocher indépendantes (`components.py:578`) : « Soleil » et « Orageux » se cochent ensemble.
- **D** : l'échelle 0-10 est un bon format rapide, mais aucun « pourquoi » ne la suit. La case « Ce qui prend le plus de place dans ma tête » mesure 13,3 cm de haut : elle intimide.
- **Charte** : « Épuisé (0) » / « Plein d'énergie (10) » sont genrés (`components.py:591`), alors que chap0 écrit « satisfait·e ».
- **E** : doublon avec chap0 « Comment je me sens actuellement ? » (`chap0/exercices.py:9`). La météo n'est jamais remesurée.
- **Reco** : radio « Cochez la météo qui domine » ; « À plat (0) » / « Pleine forme (10) » ; une ligne « Ce chiffre s'explique surtout par : » ; diviser la grande case par deux.

### Exercice 2 · Vision à 360° (p. 4) · 15-20 min
- **D / F** : la consigne demande « une phrase de synthèse », mais chaque case mesure 8,4 cm, car le template remplit la page (`components.py:655`).
- **A** : ni amorce ni exemple.
- **E** : chap0 Ex3 a noté la satisfaction sur 8 domaines (`chap0/exercices.py:33-49`). Chap1 en propose 4 autres sans y renvoyer. « Cadre et autonomie » est une condition de travail, pas un domaine de vie, et « Argent » disparaît.
- **Reco** : « Reprenez vos notes du carnet 0 (p. 8). » Deux amorces par carte (« Aujourd'hui : » / « Ce que je vise : »), puis un choix forcé : « Le domaine que je veux faire bouger en premier : ».
  > Exemple. Surface : « Un travail qui me plaît. » Exploitable : « Des missions de terrain deux jours par semaine, un salaire au moins égal à l'actuel, des résultats que je vois chaque mois. »

### Exercice 3 · Objectif boussole (p. 5) · 15-20 min
- **A / F** : c'est le meilleur exercice du carnet. Ses trois amorces s'enchaînent (« je veux avoir clarifié » → « Pour pouvoir » → « Je saurai que j'ai réussi quand »), avec une aide (`exercices.py:40-45`). Il manque un exemple, sinon « y voir plus clair » sera la réponse type.
- **D** : cases de 4,8 cm pour une phrase ; 3 cm suffisent.
- **E** : il double chap0 « Mon objectif principal », dont le champ s'appelle `objectif_3_mois` (`chap0/intro.py:122`). L'horizon varie (« 3 mois » ici, « fin du bilan » en chap0, « 3 à 6 mois » sur le web), et aucun carnet ne relit la boussole.
- **Reco** : « Reprenez votre objectif du carnet 0 (p. 5) et précisez-le. » « D'ici la fin de votre bilan ».
  > Exemple. Surface : « Y voir plus clair. » Exploitable : « Clarifier si je reste comptable dans une autre structure ou si je me forme à un autre métier. Pour pouvoir choisir une formation avant l'été. Je saurai que j'ai réussi quand j'aurai envoyé un dossier de formation. »

### Exercice 4 · Sac à dos (p. 6) · 15-20 min
- **F** : « Aujourd'hui, je décide de déposer : » ne colle pas aux champs (on ne « dépose » pas une peur). « Je lâche cette idée reçue » exige une décision avant tout repérage. L'image du sac à dos n'est expliquée qu'en chap2 (p. 3), et avec un autre sens (l'habitus).
- **B** : « Je ne veux plus subir : » reste sans retournement en critère (risque de rumination), et la distinction « je dois / je veux » est absente.
- **G** : « Ma plus grande peur est : » n'a aucun protocole. « … et je décide de la regarder en face » (`exercices.py:59`) est une injonction sans champ, pas une clôture.
- **Reco** : « Une phrase que je me répète sur le travail (« il faut… ») : » → « Ce que je veux, moi : » ; « Je ne veux plus subir : » → « Donc, dans mon prochain poste, j'ai besoin de : » ; « Ma plus grande peur face à ce changement : » → « Ce que je ferais si elle se réalisait : ». Puis la clôture (section 3).
  > Exemple. Surface : « Le stress. » Exploitable : « Je ne veux plus subir les réunions qui finissent à 20 h. Donc, dans mon prochain poste, j'ai besoin de finir à heure fixe quatre soirs sur cinq. »

### Exercice 5 · Héritage familial (p. 7) · 20-25 min
- **F** : « 3FVS » (`exercices.py:67`) n'est pas expliqué ; « comptes » renvoie au « livre de comptes » défini seulement en chap2 (p. 3).
- **B** : « Qu'est-ce qu'on voulait pour moi ? » nomme l'attendu familial, sans contrepartie « je veux ».
- **G** : le texte suppose une famille présente et racontable, sans alternative en cas de deuil ou de rupture. « On ne trahit pas ses origines… On les honore différemment » (`exercices.py:78`) ne convient pas à une famille vécue comme nocive, et ne clôt rien.
- **E** : « Quels comportements… je décide de ne pas reproduire ? » double l'Ex7 et l'Ex4 (« idée reçue »).
- **Reco** : « Trois questions pour faire le tri : ce que vous gardez (forces), ce que vous laissez (vigilances), ce que l'on attendait de vous (souhaits). » Amorce « Ce que je veux, moi : » sous la rubrique 3. « Si votre histoire familiale est absente ou douloureuse, pensez aux adultes qui ont compté dans votre enfance, ou passez à l'exercice suivant. »
  > Exemple. Surface : « Le courage. » Exploitable : « Ma grand-mère tenait une épicerie : j'en garde l'habitude de tenir mes comptes au jour le jour. »

### Exercice 6 · Image du travail (p. 8) · 25-30 min
- **D / I** : les quatre questions les plus riches (relation au travail, effet sur la famille, influence sur vos choix) ont des cases de 1,1 cm (`exercices.py:95-100`), et « parents ou grands-parents » peut viser six personnes. En taille automatique, le texte rétrécit ; à la main, c'est intenable. Les « 5 mots » tiennent dans un seul bloc.
- **F** : « Fermez les yeux » est contradictoire dans un PDF que l'on lit. La rubrique « 2. L'héritage familial » reprend le titre de l'Ex5. L'Ex5 fait trier avant que l'Ex6 fasse observer : l'ordre est inversé.
- **Charte** : « des personnes qui vous ont élevé » (`exercices.py:90-91`).
- **B** : « Changer de regard » (5 mots reçus → 5 mots choisis) est réussi.
- **Reco** : fusionner Ex5 et Ex6 sur deux pages, « Ce que vous avez vu » (cases de 2,5 cm) puis « Ce que vous en faites » (3FVS, 5 mots en `add_numbered_lines`). « Lisez la consigne, puis fermez les yeux une minute avant d'écrire. » « (ou des personnes qui ont pris soin de vous) ».

### Exercice 7 · Mentors et anti-modèles (p. 9) · 10-15 min
- **A / D** : les amorces sont glissées entre parenthèses, dans deux cases de 7,3 cm sans structure. Le titre dit « mentors », la question « votre modèle ».
- **B / E** : les anti-modèles ne mènent à aucun critère. L'exercice prépare le bonus interview (chap2 p. 12) et chap5 Ex7, mais ne le dit pas.
- **Reco** : deux emplacements « La personne · Ce que j'admire · Ce que je veux retrouver dans mon travail » ; côté anti-modèles, « Donc, dans mon prochain poste, je veux… ».
  > Exemple. Surface : « J'admire les entrepreneurs. » Exploitable : « J'admire mon ancienne responsable d'atelier pour sa façon de dire non à un client sans le perdre. Je veux retrouver ça : poser mes limites tôt. »

### Livrable et quatrième de couverture (p. 10-11) · 5-10 min
- **C** : ni étonnement ni « à aborder en séance ». La case de notes (12,8 cm, `components.py:463-468`) n'a pas de consigne.
- **I** : « je le note quand cela revient » ne dit pas où, et « une action concrète » n'est définie nulle part.
- **Reco** : scinder les notes en « Ce qui m'étonne en relisant ce carnet : » et « À aborder en séance (un point de friction, une question non tranchée, un exercice laissé vierge) : ». Ajouter « Mon action d'ici la prochaine séance : ». (« Ce qui m'a surpris » genrerait la personne.)

## 3. Charge émotionnelle

Aucun carnet ne contient « vierge », « trop lourd » ni phrase d'ancrage (recherche sur `text/*.txt`).

| Exercice | Niveau | Avertissement | Optionnalité | Clôture | Question plus franche possible |
|---|---|---|---|---|---|
| Ex1 Météo (p. 3) | faible | absent | absente | absente | — |
| Ex4 Sac à dos (p. 6) | **fort** | absent | absente | partielle (annotation sans champ) | « Ma plus grande peur face à ce changement : » + « Ce que je ferais si elle se réalisait : » |
| Ex5 Héritage (p. 7) | **moyen à fort** | absent | absente | non (citation) | « Ce que je n'ai jamais dit à ma famille sur mes choix professionnels : » |
| Ex6 Image du travail (p. 8) | **moyen à fort** | absent | absente | absente | « Ce que leur travail a pris à notre vie de famille : » |
| Ex7 Anti-modèles (p. 9) | moyen | absent | absente | absente | « La personne avec qui j'ai le plus mal travaillé, et ce que je ne lui ai jamais dit : » |

Encadré à placer avant l'Ex4 et avant l'Ex5 (`add_callout`) : « Les pages suivantes parlent de vos peurs et de votre famille. Elles peuvent réveiller des souvenirs forts. Répondez à votre rythme. Si un exercice vous semble trop lourd à faire sans accompagnement, laissez-le vierge : nous l'aborderons ensemble en séance. » En fin d'Ex4 et d'Ex6, une ligne à compléter : « Aujourd'hui, avec le recul, je sais que… ».

## 4. Fil rouge

- **Entrées** : aucune n'est explicite. Le carnet aurait besoin de chap0 (objectif p. 5, domaines p. 8) sans jamais y renvoyer. Il emploie des notions que chap2 explique seulement après (sac à dos social, livre de comptes, p. 3-4). Il n'a pas de récapitulatif de la séance chap0, alors que chap2, chap4 et chap6 en ont un.
- **Sorties** :
  - Les héritages sont repris par le récapitulatif de chap2 (`chap2/intro.py:41-42`), qui refait le tri « garder / faire évoluer » sans citer l'Ex5. Mieux : « Relisez votre page Héritage du carnet 1 : qu'est-ce qui a bougé ? »
  - La boussole n'est jamais relue. Elle a sa place dans chap6 Ex2 (« Mes envies et objectifs ») et dans le livret, thème 7 : « Votre objectif boussole : atteint, en partie, déplacé ? »
  - La météo n'est jamais remesurée.
  - « Je ne veux plus subir », les anti-modèles et « Cadre et autonomie » sont à reprendre dans chap5 Ex7 (« éviter les environnements où… ») et dans le cadre de sécurité du livret.
  - Les mentors sont à relier au bonus interview de chap2.
  - Les « 5 mots pour mon futur travail » sont un pont vers chap5 Ex4.
- **Doublons** : avec chap0, l'objectif (Ex1 ↔ Ex3), l'état d'esprit (Ex2 ↔ Ex1), les domaines de vie (Ex3 ↔ Ex2, deux découpages incompatibles), et deux carnets qui se disent « point de départ ». En interne : « ne pas reproduire » (Ex5 ↔ Ex7), « idée reçue » (Ex4 ↔ Ex5), « héritage familial » (Ex5 ↔ Ex6). Léger recoupement avec chap4 Ex3.
- **Ruptures** : boussole, météo, anti-modèles et mentors ne sont jamais repris. Pour l'héritage, la pratique (chap1) précède l'explication (chap2).

## 5. Écart avec l'app web

`_build_chap1_spec` (`server/predefined_workbooks.py:146-279`) n'a que quatre exercices : il n'a ni héritage, ni image du travail, ni mentors.
- **Boussole** : deux questions, avec des exemples visibles et un horizon de « 3 à 6 mois ».
- **360°** : le web demande « constat actuel et ce que vous visez ».
- **Sac à dos** : deux colonnes « Ce qui pèse → Ce que je décide », avec exemples. Les irritants y sont mieux retournés que dans le CLI, mais le texte emploie « injonction » (l. 234).
- **Résumé** : il est mal étiqueté « 1. RÉCAPITULATIF DE LA SÉANCE » (l. 166).

## 6. Recommandations classées

| Priorité | Type | Page(s) | Constat | Recommandation |
|---|---|---|---|---|
| P1 | correction rapide | 6, 7, 8 | Peur, dette familiale, souffrance des parents, sans protocole | Encadré avant Ex4 et Ex5 ; ligne « Aujourd'hui, avec le recul, je sais que… » en fin d'Ex4 et d'Ex6 (section 3) |
| P1 | correction rapide | 7, 8 | Famille supposée présente et racontable | Alternative « Si votre histoire familiale est absente ou douloureuse… » (section 2) |
| P1 | correction rapide | 2 | Cadre absent (confidentialité, droit de passer), ici comme en chap0 | « Vos réponses vous appartiennent… Vous pouvez passer une question. » |
| P2 | refonte | 3, 4, 8, 9 | Cases : 1,1 cm pour la famille, 13,3 cm pour l'humeur, 8,4 cm pour « une phrase » | Ex6 sur deux pages (cases de 2,5 cm) ; plafonner météo, 360° et mentors ; 5 mots sur 5 lignes |
| P2 | correction rapide | 2-9 | Aucune durée affichée | Durée dans chaque en-tête ; « environ 2 h, en deux ou trois fois » p. 2 |
| P2 | correction rapide | 4-7, 9 | Aucun exemple contrasté (`example=` existe déjà) | Un exemple étiqueté par exercice (section 2) |
| P2 | correction rapide | 6, 9 | Irritants et anti-modèles non retournés | « Donc, dans mon prochain poste, j'ai besoin de : » |
| P2 | correction rapide | 6, 7 | « Je dois / je veux » absent | « Une phrase que je me répète… » → « Ce que je veux, moi : » |
| P2 | correction rapide | 2, 7 | « 3FVS », « comptes » et « sac à dos » ne sont pas expliqués | Une phrase d'explication, ou retirer l'acronyme |
| P2 | refonte | 3, 4, 5 | Doublons avec chap0 | Renvois explicites au carnet 0, ou suppression côté chap0 ; harmoniser les domaines |
| P2 | refonte | 6-9 | Doublons internes ; ordre trier → observer inversé | Fusionner Ex5 et Ex6 (« Ce que vous avez vu » → « Ce que vous en faites ») |
| P2 | refonte | 10 | Ni étonnement ni « à aborder en séance » | Paramètre du composant d'engagement : deux zones guidées |
| P2 | refonte | chap5, chap6, livret | Sorties jamais reprises | Reprises explicites (chap5 Ex7, chap6 Ex2, livret thème 7) |
| P3 | correction rapide | 3 | Météos cochables ensemble ; échelle sans « pourquoi » | Radio ; « Ce chiffre s'explique surtout par : » |
| P3 | correction rapide | 3, 8 | Genre : « Épuisé », « Plein d'énergie », « vous ont élevé » | « À plat (0) » / « Pleine forme (10) » ; « qui ont pris soin de vous » |
| P3 | correction rapide | 8 | « Fermez les yeux » dans un document à lire | « Lisez la consigne, puis fermez les yeux une minute. » |
| P3 | correction rapide | 5 | Horizon incohérent (3 mois, fin du bilan, 3 à 6 mois) | « D'ici la fin de votre bilan » partout |
| P3 | correction rapide | 10 | « je le note » (où ?) ; action non définie | « …je le note ci-dessous » ; « Mon action d'ici la prochaine séance : » |
| P3 | correction rapide | 3 | Même info-bulle « Niveau : 0 » sur les 11 pastilles (inventaire ; ReportLab la met sur le groupe, `forms.py:98`) | Info-bulle générique « Niveau d'énergie, de 0 à 10 » |
