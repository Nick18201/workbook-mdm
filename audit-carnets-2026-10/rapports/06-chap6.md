# Audit du carnet 6 : « Phase d'exploration »

Sources : `SP/png/chap6/p01-p13.png`, `SP/text/chap6.txt`, `SP/fields/chap6.json`. Code : `Scripts/workbook_generator/chapters/chap6/` (`intro.py`, `exercices.py`, `ressources.py`), ordre des pages dans `Scripts/main_generate_chap6.py:11-21`.

## 1. Synthèse

Carnet clair et aéré, avec de bonnes idées (pistes « no limit » / réalistes, avis des proches recueilli sans leur parler des pistes). Mais il ne fait pas converger : il collecte des pistes sans les confronter aux critères des carnets 2 à 5, ni au terrain promis par la couverture et le programme. Les trois problèmes majeurs :
1. Les fiches métiers n'ont aucun champ valeurs, argent ou énergie, et il n'existe aucun support d'enquête métier.
2. La charge est mal séquencée : 10 fiches, 3 échanges et 5 contacts, sans durée ni priorisation, avec des ressources placées après les fiches.
3. Le retour des proches n'est pas cadré (qui, quoi montrer, comment recevoir) et n'a aucun protocole de sécurité.

## 2. Exercice par exercice

### Couverture et ouverture (p. 1-2)
- **F** : la promesse « Des pistes confrontées au réel. » (`intro.py:11`) n'est pas tenue. L'ouverture cite des « moteurs » et le verbe « tester » (`intro.py:16-19`), mais aucun exercice ne les reprend.
- **D** : aucune durée (`intro.py:20-28`), alors que le carnet 5 les affiche en eyebrow (`chap5/alignement.py:28`). Rien n'indique qu'on peut faire le carnet en plusieurs fois.
- **Recommandation** : « Ce carnet se remplit en plusieurs fois. Commencez par solliciter vos proches (exercice 3) : leurs réponses peuvent prendre quelques jours. »

### Exercice 1 · Récapitulatif valeurs (p. 3) · 10-15 min
- **E** : doublon du carnet 5, synthèse p. 17 (3 valeurs, besoins) et tensions p. 15. La cartographie redemande aussitôt valeurs et besoins (`exercices.py:16-17`) : les 3 valeurs sont écrites 4 fois en deux carnets.
- **D** : les 3 valeurs vont dans une seule case de 4,4 cm (`components.py:525`, `recap_q1`).
- **Bien traité** : le récapitulatif est guidé par des questions précises.
- **Recommandation** : trois lignes « Valeur 1, 2, 3 ». Remplacer la question 2 par « Qu'est-ce que la séance sur vos valeurs a confirmé, et qu'a-t-elle déplacé ? ».

### Exercice 2 · Cartographie (p. 4) · 30-45 min
- **F/E** : la consigne « Résumez les éléments clés issus de vos séances de bilan. » (`exercices.py:11`) ne dit pas où chercher. Il manque le minimum financier (carnet 4, p. 12), les moteurs (carnet 2), les conditions de travail (carnet 5, ex. 7) et les intérêts Hexa3D annoncés par le programme (`programme/page_organisation_pedagogie.py:29-30`). *Note du 8 octobre 2026 : Hexa3D est abandonné ; cette mention est sans objet, et toute mention de Hexa3D doit disparaître.*
- **B** : « Mes sources de stress » reste un constat, jamais retourné en critère.
- **H** : cette page est montrée aux proches (ex. 3), stress et besoins compris.
- **I** : le champ MBTI® fait 0,64 cm de haut, trop peu à la main.
- **Recommandation** :
  - un renvoi au carnet source dans le `hint` de chaque case (« Mes moteurs, carnet 2, exercice 3 ») ;
  - une case « Mes sources de stress, donc ce que ma piste doit éviter » ;
  - une zone « À garder pour vous » (seuils financiers).
  > **Exemple.** Surface : « Le stress, la pression. » Exploitable : « Les urgences imposées le vendredi soir. Donc ma piste doit offrir des échéances connues à l'avance. »

### Exercice 3 · Retour des proches (p. 5) · 15 min plus 3 échanges sur plusieurs jours
- **F** : la consigne (`exercices.py:27-30`) ne dit ni qui choisir, ni quoi dire, ni comment recevoir. Le carnet 0 (ex. 4) a pourtant repéré soutiens et « regards critiques ».
- **D** : une seule case pour au moins 3 personnes : on ne saura pas qui a suggéré quoi, ni pourquoi.
- **B** : c'est le bon endroit pour séparer désir réel et attente de l'entourage, et il n'est pas exploité.
- **G** : « Comment j'ai vécu cet exercice » ouvre un espace de vécu, mais ce n'est pas une phrase d'ancrage. Il n'y a ni avertissement ni optionnalité.
- **Recommandation** :
  > « Montrer sa cartographie, c'est s'exposer un peu. Choisissez des personnes bienveillantes, par exemple parmi les soutiens notés au carnet 0. Vous décidez de ce que vous montrez. Si cet échange vous semble trop lourd, laissez cette page vierge : nous en parlerons en séance. »

  - Une phrase à dire : « Si tu ne connaissais pas mon métier actuel, à quel métier penserais-tu pour moi ? Qu'est-ce qui, chez moi, t'y fait penser ? »
  - Trois cartes, une par personne (prénom, métiers suggérés, raison).
  - Deux cases : « Ce qui me parle vraiment », « Ce qui ressemble plutôt à ce qu'on attend de moi ».
  - Une clôture : « Après ces échanges, je sais que… »

### Exercice 4 · Dix métiers (p. 6) · 20-40 min
- **A** : principal risque de page blanche du parcours : 10 intitulés sans amorce, sans exemple, sans source. Pas de renvoi aux proches (ex. 3), à « Je m'autorise à » (`chap0/intro.py:124`), aux mentors (carnet 1), à l'interview (carnet 2) ni aux ressources, qui n'arrivent qu'en p. 11 (`main_generate_chap6.py:19`).
- **F** : « faisables concrètement aujourd'hui » est ambigu (une formation courte compte-t-elle ?). Le programme parle de « pistes directes, passerelles courtes » et de pistes « audacieuses » (`programme/page_deroule.py:124, 134-135`).
- **D** : champs bien dimensionnés (186×28 pt, 11 pt). La moitié basse de la page est vide.
- **Recommandation** :
  - « Puisez dans vos carnets : les suggestions de vos proches, votre « Je m'autorise à » (carnet 0), vos mentors (carnet 1), les ressources. » ;
  - réalistes = « accessibles avec vos compétences actuelles ou une formation courte » ;
  - une colonne « D'où vient cette piste ? ».
  > **Exemple.** Surface : « Artiste. » Exploitable : « Luthier ou luthière : travailler de mes mains, sur un objet qui dure. »

### Exercices 5 et 6 · Fiches métiers (p. 7-10) · 15-25 min par fiche, 2 h 30 à 4 h au total
- **E/B** : c'est la rupture centrale. Chaque fiche se limite à l'intitulé, « Pourquoi ce métier vous attire » et « Missions et compétences utiles » (`exercices.py:64-68`). Rien ne confronte la piste aux valeurs, au minimum financier ou à l'énergie. L'engagement « Je confronte chaque piste à mes valeurs et à mon minimum financier » (`ressources.py:47`) n'a donc aucun support.
- **F** :
  - « Missions et compétences utiles » est ambigu : les missions du métier ou mes compétences ?
  - L'annotation p. 6 (« disent souvent ce que vous cherchez vraiment ») n'est pas exploitée dans la fiche « no limit ».
- **D/I** : les cases font 7,5×2,2 cm en police automatique (le texte rétrécit au-delà de quatre lignes) et l'intitulé 0,64 cm. Aucune priorisation des 10 fiches, et les pages 8 et 10 sont à moitié vides.
- **Recommandation** :
  - scinder en « Les missions du métier (d'après vos recherches) » et « Ce que je sais déjà faire, ce qui me manque » ;
  - ajouter une rangée de critères : valeurs respectées (oui, en partie, non), minimum financier (atteint, à moyen terme, à vérifier), « Ce qui me rechargerait, ce qui me coûterait », « À vérifier auprès de qui » ;
  - fiche « no limit » : « Ce que cette piste dit de ce que je cherche », avec en clôture « Ce que je garde de cette piste, même si je ne l'exerce pas : ».
  > **Exemple (ex. 5).** Surface : « J'aime être dehors. » Exploitable : « Guide de haute montagne : des décisions rapides, en pleine responsabilité. Ce que je garde : être dehors et décider vite. »
  > **Exemple (ex. 6).** Surface : « Le métier a l'air intéressant. » Exploitable : « Médiation culturelle : expliquer simplement, au contact du public, avec des horaires connus. Cela respecte ma valeur de transmission. »

### Ressources (p. 11)
- **I** : liens cliquables (`ressources.py:15-36`), vérifiés le 8 octobre 2026.
  - Into the Job, YouTube, ONISEP (redirigé vers `/metier`) et CIDJ (redirigé, toujours classé par centres d'intérêt) répondent.
  - MétierScope pointe vers l'ancien domaine `candidat.pole-emploi.fr` (`ressources.py:30`), qui redirige vers francetravail.fr.
  - APEC et Cadremploi renvoient une erreur 403 aux robots : non vérifiables.
  - Notion dépend du partage.
  - À l'impression, les URL sont invisibles.
- **Manques** : la page arrive après les fiches. Rien sur l'enquête métier, l'immersion (PMSMP via France Travail) ou les salaires du bassin d'emploi, pourtant promis par le programme (`page_deroule.py:135-136`).

### Livrable et dos (p. 12-13) · 10 min
- **C** : ni étonnement ni « à aborder en séance » : une zone de notes générique de 12,8 cm (`components.py:465`).
- **D/F** : « une fiche métier par semaine » (`ressources.py:46`) contredit le livrable « Vos dix pistes et leurs fiches métiers… validées en séance » (`:51`). « Je contacte un professionnel pour chacune de mes pistes réalistes » représente 5 contacts, sans guide ni compte rendu.
- **E** : le dos (`components.py:498`) ne prépare pas le livret. Le folio « carnet 6/7 » laisse croire qu'un carnet reste à venir.
- **Recommandation** :
  - trois amorces : « Ce qui m'étonne, à la relecture de ce carnet : », « Mes 3 pistes prioritaires, et pourquoi : », « À aborder en séance : » ;
  - engagements : « Je complète d'abord les fiches de mes trois pistes favorites. », « Je sollicite un professionnel pour chacune de mes trois pistes prioritaires. » ;
  - dos : « Prochaine étape : le livret de compétences. Vos pistes prioritaires y deviennent vos pistes A et B. »

**Total estimé** : 5 à 7 h de travail personnel plus les échanges, contre « 1 h 30 à 3 h par carnet » dans le programme (`page_organisation_pedagogie.py:44`).

## 3. Charge émotionnelle

| Exercice | Niveau | Présent | Absent | Question plus franche (protocole en place) |
|---|---|---|---|---|
| 1 · Récapitulatif valeurs | Faible | Sans objet | Sans objet | « La valeur que j'ai le plus sacrifiée jusqu'ici, et ce que cela m'a coûté : » |
| 2 · Cartographie | Faible | Sans objet | Retournement du stress en critère | « Ce que je ne veux plus revivre au travail, donc ma prochaine piste doit… » |
| 3 · Retour des proches | **Moyen** (regard de l'entourage, attentes familiales) | Espace de vécu | Avertissement, optionnalité, choix des personnes, phrase d'ancrage | « La suggestion qui m'a le plus fait réagir, et pourquoi : » ; « Ce qu'on attend de moi, et que je ne veux pas forcément : » |
| 4 · Dix métiers | Faible à moyen (rêves écartés) | Annotation bienveillante | Clôture | « Le métier que je n'ai jamais osé envisager, et ce qui m'en empêche : » |
| 5 · Fiches « no limit » | Faible à moyen (renoncer à un rêve) | Aucun | Clôture | « Ce que je garde de cette piste, même si je ne l'exerce pas : » |
| 6 · Fiches réalistes | Faible | Sans objet | Sans objet | « Le compromis que cette piste me demande, et si je l'accepte : » |
| Engagement « contacter un professionnel » | Moyen (peur de solliciter) | Aucun | Préparation, message type | « Ce qui pourrait me faire repousser ce contact : » |

**Cadre (H)** : confidentialité et droit de passer ne sont pas rappelés, alors que c'est le seul carnet où la personne montre ses réponses à des tiers. Une ligne dans l'exercice 3 suffit : « Ces pages vous appartiennent. Vous choisissez ce que vous partagez. »

## 4. Fil rouge

**Entrées explicites** :
- valeurs et tensions du carnet 5 (ex. 1) ;
- type MBTI® des carnets 3 et 4 (ex. 2) ;
- minimum financier, cité seulement dans un engagement (p. 12).

**Entrées implicites, jamais nommées** :
- carnet 0 : « Je m'autorise à », entourage ;
- carnet 1 : objectif boussole, mentors ;
- carnet 2 : moteurs, interview ;
- carnet 3 : question 7 ;
- carnet 4 : seuils de la p. 12 ;
- carnet 5 : conditions de travail ;
- programme : Hexa3D (abandonné depuis le 8 octobre 2026 : sans objet).

La cartographie ne reprend vraiment que le MBTI® et les valeurs. Point de départ et parcours n'y apparaissent qu'en intitulés génériques.

**Sorties** : 10 intitulés et 10 fiches. Le livret devrait les reprendre (thème 4 « nouveaux métiers », thème 6 « curiosités métiers », thème 7 « pistes A et B », `livret/plan_action.py:40`), mais aucun des deux documents ne renvoie à l'autre.

**Doublons** :
- les 3 valeurs, écrites 4 fois (carnet 5 p. 10 et 17, carnet 6 p. 3 et 4) ;
- le MBTI®, 3 fois (carnet 4 p. 3, carnet 6 p. 4, livret p. 2) ;
- « sources de stress » et « Ce qui vide mes batteries » (livret p. 3) ;
- la liste des métiers possibles (livret p. 9).

**Ruptures** :
1. Quatre carnets promettent d'« évaluer chaque piste » : carnet 2, carnet 4 (`chap4/cloture.py:24`) et carnet 5. Aucun champ ne le permet ici.
2. Le carnet 4 demande si « cette piste » atteint le minimum (`chap4/moteurs.py:47`) avant qu'aucune piste n'existe. La question manque justement ici.
3. Les suggestions des proches ne sont pas reprises dans l'exercice 4.
4. L'enquête est inversée : le carnet 6 engage à contacter des professionnels, puis le livret demande seulement qui interviewer (`livret/boussole.py:69`).
5. Le programme annonce une matrice de faisabilité, 3 scénarios comparés, des retours d'enquêtes et trois familles de pistes (`page_deroule.py:134-144`), sans aucun support dans le carnet.

**Pour passer au réel**, il manque :
- un tri forcé vers 3 pistes ;
- une grille d'entretien (celle du bonus du carnet 2, `chap2/cloture.py:13-16`, est réutilisable) ;
- un message d'approche : « Je réfléchis à une évolution vers votre métier. Accepteriez-vous un échange de 20 minutes ? Je ne cherche pas de poste, seulement un regard de professionnel. » ;
- un compte rendu « ce qui confirme, ce qui contredit, la suite ».

## 5. Écart avec l'app web

- `_build_chap6_spec` (`server/predefined_workbooks.py:834-996`) est un autre carnet, « Le plan d'action » : météo de fin de bilan, arbitrage A/B, feuille de route 30-60-90 jours, garde-fous. Il n'a ni cartographie, ni proches, ni 10 métiers, ni fiches, ni ressources.
- Ce qui manque au chap6 CLI est dans le chap5 web, « L'exploration du terrain » (`:690-832`) : grille d'entretien, « idées reçues et réalité », 3 contacts avec message d'approche.
- La numérotation diverge : personnaliser « chap6 » dans l'app ne produit pas le carnet 6 du PDF.
- Les exemples (« Ex : … ») n'existent que côté web.

## 6. Recommandations classées

| Priorité | Type | Page(s) | Constat | Recommandation |
|---|---|---|---|---|
| P1 | Correction rapide | 2, 3-12 | Aucune durée. 10 fiches attendues, soit 5 à 7 h estimées contre 1 h 30 à 3 h annoncées. « Une fiche par semaine » contredit le livrable. | Durées en eyebrow, mention « en plusieurs fois », exiger 10 intitulés et 3 fiches complètes (le reste en option), réécrire `ressources.py:46`. |
| P1 | Correction rapide | 5 | La cartographie est exposée aux proches sans cadre ni protocole, et l'exercice dépend de rencontres. | Avertissement, choix des personnes (carnet 0), « Vous décidez de ce que vous montrez », optionnalité, clôture « Après ces échanges, je sais que… », sollicitations lancées dès l'ouverture. |
| P2 | Refonte | 7-10 | Fiches sans critères (valeurs, argent, énergie). | Rangée de critères : radios valeurs et minimum, recharge et coût, « à vérifier auprès de qui ». |
| P2 | Refonte | Nouvelle page | Aucune convergence : ni matrice ni tri, contrairement au programme. | « Vos pistes face à vos critères » (`add_table` / `add_rating_grid`), puis « Mes 3 pistes à confronter au terrain ». |
| P2 | Refonte | Nouvelle page | Aucun support d'enquête métier, malgré la couverture, l'engagement 3 et le programme. | « Préparer vos enquêtes métier » : contact, message, 4 questions (bonus du carnet 2), compte rendu. |
| P2 | Correction rapide | 6, 11 | Page blanche pour 10 métiers, ressources placées après les fiches. | Sources (carnets 0 à 3, proches), exemple contrasté, définition « directe ou passerelle », ressources avant l'exercice 4 (`main_generate_chap6.py:19`). |
| P2 | Correction rapide | 4 | Cartographie sans renvois, sans argent, moteurs ni conditions. | Renvois dans les `hint`, cases « moteurs » et « conditions », zone « À garder pour vous », stress retourné en critère. |
| P2 | Correction rapide | 5 | Une case pour 3 personnes, pas de distinction « je veux » / « on attend de moi ». | Trois cartes par personne, puis « Ce qui me parle vraiment » et « Ce qu'on attend de moi ». |
| P2 | Correction rapide | 7-8 | La fiche « no limit » n'en tire pas l'ingrédient recherché. | « Ce que cette piste dit de ce que je cherche » et « Ce que je garde de cette piste… ». |
| P2 | Correction rapide | 12 | Ni étonnement ni « à aborder en séance ». | Trois amorces à la place de la zone de notes générique. |
| P3 | Correction rapide | 3 | Doublon du carnet 5, 3 valeurs dans une seule case. | Trois lignes, plus « confirmé, déplacé ». |
| P3 | Correction rapide | 7-10 | Case « Missions et compétences » ambiguë, champs serrés (0,64 cm et 2,2 cm). | Scinder la case, intitulé à 1 cm, utiliser l'espace libre des pages 8 et 10. |
| P3 | Correction rapide | 11 | MétierScope sur l'ancien domaine, URL invisibles imprimées, rien sur l'immersion. | Mettre à jour les URL, afficher une adresse courte, ajouter PMSMP et un guide d'entretien. |
| P3 | Correction rapide | 1, 2, 13 | Promesse non tenue, « moteurs » et « tester » sans suite, dos sans lien vers le livret, « no limit » contre « audacieuses ». | Aligner les textes, transition vers le livret au dos, vocabulaire du programme. |
| P3 | Correction rapide | 5 | Cadre non rappelé. | « Ces pages vous appartiennent. Vous choisissez ce que vous partagez. » |
