# Audit du carnet 5 « Valeurs et moteurs profonds »

PDF de 19 pages, 163 champs (57 champs texte, 106 cases à cocher dont 90 pour la liste de valeurs p. 9). Code : `Scripts/workbook_generator/chapters/chap5/` (fichiers cités sans ce préfixe), ordre dans `Scripts/main_generate_chap5.py`.

## 1. Synthèse

Verdict : carnet solide, à l'entonnoir clair (situations, liste, hiérarchie, incarnation, conditions), qui donne au parcours ses critères de choix. Trois problèmes l'affaiblissent.
1. Durées sous-estimées de moitié : 95 min annoncées pour 2 h 30 à 3 h réelles (Ex. 6 : « 5 min » par valeur), sans mention d'un remplissage en plusieurs fois.
2. Désalignement et choix difficiles (Ex. 2-3) sans protocole de sécurité ; les irritants deviennent des valeurs, jamais un critère (« donc mon prochain poste doit… ») ; aucun exemple contrasté.
3. Fil rouge rompu : pas de récapitulatif de la séance argent, parcours du carnet 2 réécrit sans le citer, « moteurs » du titre jamais travaillés ; la sortie (3 valeurs vers des conditions) est éparpillée sur 4 pages, dans des champs trop petits (p. 8, 15-17).

## 2. Exercice par exercice

### Ouverture (p. 1-3) · `intro.py`
- **F** : le « pourquoi » est clair (p. 2 : « pour évaluer vos futures pistes »). Les « moteurs » du titre ne sont jamais définis ni travaillés.
- **B** : l'encadré p. 3 (« Ne cherchez pas les valeurs qui semblent les plus « belles » », `intro.py:44-48`) pose bien le désir réel face à l'attendu social. Aucun exercice ne le reprend.
- **D/H/E** : pas de durée totale ni de fractionnement ; cadre non rappelé (confidentialité, droit de passer) alors que l'Ex. 2 est chargé ; seul carnet de chap2 à chap6 sans « Récapitulatif de la séance précédente ».
- Charte : adjectifs accordés au point médian (« motivé·e », « reconnu·e », `intro.py:39-42`).
- Recommandations, p. 3 :
  - « Elles se repèrent dans vos moments de motivation, de fierté, d'utilité, de liberté, de reconnaissance, de confiance. Et aussi dans la frustration, la colère, l'épuisement ou le conflit intérieur. »
  - « Valeur : ce qui compte pour vous (l'autonomie). Moteur : ce qui vous fait avancer (apprendre). Besoin : la condition concrète qui permet de la vivre (choisir l'ordre de vos dossiers). »
  - « Comptez 2 h 30 à 3 h, en trois fois : exercices 1 à 3, 4 à 6, puis 7 à 9. »
  - « Ce carnet est à vous. Vous choisissez ce que vous partagez en séance. Une question vous pèse ? Passez-la et notez-la p. 18. »

### Exercice 1 · Alignement (p. 4-5) · `alignement.py:25-38`. Affiché 10 min, réaliste 20-25 min
- **A** : trois situations sans amorce ni exemple, alors que le carnet 2 les fournit déjà (sommets, « ce que j'ai aimé »).
- **F/D** : trois questions dans un cadre de 79 pt, soit 3 lignes manuscrites (`alignement.py:35`). La valeur, que l'Ex. 4 doit cocher, se noie dans le récit.
- Recommandations :
  - Consigne : « Repensez à trois situations où vous étiez à votre place. Vous pouvez repartir de vos sommets du carnet 2 (exercice 4). »
  - Scinder le champ : « Ce qui me donnait de l'énergie » (multiligne) et « La valeur respectée, en un ou deux mots » (une ligne).
  - Exemple, un seul : « *Exemple.* En surface : « J'aimais bien ce poste. » Exploitable : « Comptable dans une PME, on me confiait la clôture de bout en bout, sans validation à chaque étape. Valeur respectée : l'autonomie. » »

### Exercice 2 · Désalignement (p. 6-7) · `alignement.py:41-54`. Affiché 10 min, réaliste 20-25 min
- **B** : l'introspection par le négatif est présente et la synthèse p. 7 retourne l'irritant en valeur. Il manque le critère, d'où un risque de rumination ; l'Ex. 7 ne cite pas cet exercice.
- **G** : « bafouée », « limite franchie », « vidé·e » peuvent raviver un épuisement ou un conflit grave : ni avertissement, ni optionnalité, ni clôture.
- **A** : pas d'exemple ; libellé triple (`alignement.py:51`), comme à l'Ex. 1.
- Recommandations :
  - En tête : « Cet exercice peut raviver des moments pénibles. Choisissez des situations dont vous pouvez parler sans que cela vous submerge. Si une situation reste trop lourde, notez un mot-clé et laissez le reste vierge : nous l'aborderons ensemble. »
  - Par situation, un champ d'une ligne : « Donc, dans mon prochain poste, j'ai besoin de… ».
  - Après la synthèse : « Aujourd'hui, avec le recul, je sais que… ».
  - Exemple : « *Exemple.* En surface : « Mauvaise ambiance. » Exploitable : « En logistique, on me demandait de signer des réceptions non vérifiées pour tenir les délais. Valeur bafouée : la rigueur. Donc mon prochain poste doit me laisser le temps de contrôler avant de signer. » »
  - Consigne neutre : « Repensez à trois situations de frustration, d'épuisement ou de conflit intérieur » (au lieu de « senti·e… frustré·e, vidé·e », `alignement.py:47`).

### Exercice 3 · Choix difficiles (p. 8) · `alignement.py:57-76`. Affiché 10 min, réaliste 15-20 min
- **D/I** : 8 champs de 37 pt, soit une seule ligne manuscrite (`alignement.py:68-70`), pour des contenus doubles. « Ce que l'option A et l'option B permettaient chacune de préserver » tient dans un seul cadre.
- **F** : « préserver » reste abstrait, et rien n'indique à quoi ressemble une réponse terminée.
- **G** : charge moyenne (renoncements, regrets), sans protocole.
- Recommandations :
  - Une ligne à deux champs (`add_fields_card` le permet) : « Option A : ce qu'elle me permettait de garder » et « Option B : ce qu'elle me permettait de garder ».
  - Amorces : « J'ai choisi… et j'ai renoncé à… », puis « Avec le recul, je referais ce choix, parce que… ».
  - Hauteur de 2,2 cm. La page 8 est déjà pleine : passer à une page par choix.

### Exercice 4 · Liste de valeurs (p. 9) · `valeurs.py:5-63`. Affiché 10 min, réaliste 10-15 min
- **D** : le tri sur 90 cases de 9 pt est rapide, mais sans volume fixé. À 40 valeurs cochées, la réduction à 10 de l'Ex. 5 devient longue ; sous 10, l'étape 1 n'a pas de sens.
- **Cohérence de la liste** :
  - Trois doublons, donc 87 valeurs distinctes : Responsabilité (`valeurs.py:8` et `:48`), Fiabilité (`:13` et `:43`), Engagement (`:28` et `:44`). Quasi-doublons : Confort et Confort de vie, Beauté et Esthétique.
  - Manquent « Rémunération », « Appartenance », « Affirmation de soi », « Discrétion » : ce sont les pôles des tensions p. 15 (`synthese.py:7-20`), et l'argent sort du carnet 4. Pas de case « autre ».
  - « Marge de manœuvre » est le nom du cabinet : risque de la cocher par politesse.
- **E** : la consigne renvoie bien aux Ex. 1-3, pas aux cinq moteurs du carnet 2.
- Recommandations :
  - Consigne : « Cochez 15 à 20 valeurs, sans vous attarder. Reprenez les valeurs de vos synthèses p. 5 et 7 et vos cinq moteurs du carnet 2. Une valeur vous manque ? Ajoutez-la ci-dessous. »
  - Ajouter 3 champs libres.
  - Remplacer les doublons par Rémunération juste, Appartenance et Affirmation de soi.

### Exercice 5 · Hiérarchie (p. 10) · `valeurs.py:66-86`. Affiché 10 min, réaliste 10-15 min
- **D** : trois grands cadres de 90 pt, sans emplacements numérotés, pour 10, 5 puis 3 mots. On ne peut pas classer, et il faut recopier à la main ce qu'on vient de cocher.
- **F** : aucun critère de réduction (« les plus fortes », « les plus vitales »). La définition du « non négociable » arrive après les cadres (`valeurs.py:81`).
- **B** : la distinction entre « je veux » et « on attend de moi » est absente, alors que c'est le bon moment pour la poser.
- Recommandations :
  - Utiliser `add_numbered_lines` : 10 lignes sur deux colonnes, puis 5, puis 3.
  - Placer l'encadré « À retenir » avant l'étape 3.
  - Critère : « Pour chaque valeur, demandez-vous : si elle manquait pendant six mois, est-ce que je partirais ? »
  - Ajouter une ligne : « La valeur que je coche surtout parce qu'elle est attendue de moi : … »

### Exercice 6 · Incarner (p. 11-13) · `valeurs.py:89-114`. Affiché 3 × 5 min, réaliste 30-40 min
- **D** : 4 questions en 2 lignes manuscrites, trois fois de suite : rythme monotone, nom de la valeur recopié (p. 10, 11-13, 17).
- **E/A** : la Q2 (« Dans quelles situations passées… », `valeurs.py:97`) refait les Ex. 1-3 ; la Q4 anticipe l'Ex. 7.
- **B** : l'origine de la valeur manque, lien naturel avec le 3FVS (carnet 1) et l'habitus (carnet 2).
- Recommandations :
  - Durée : « 10 min par valeur ».
  - Remplacer la Q2 par : « Cette valeur me vient de… Je la garde parce que… ».
  - Ajouter une échelle de 1 à 5, « Dans mon poste actuel, elle est respectée », suivie d'un « pourquoi » d'une ligne (`add_rating_grid`).
  - Exemple pour la Q1 : « *Exemple.* En surface : « L'autonomie, c'est important. » Exploitable : « Graphiste, je choisis l'ordre de mes projets de la semaine ; on me fixe le résultat, pas la méthode. » »

### Exercice 7 · Conditions de travail (p. 14) · `valeurs.py:117-142`. Affiché 10 min, réaliste 15-20 min
- **A** : deux exemples en listes de six items génériques, faciles à recopier (`valeurs.py:129-130`, `:138-139`) ; « je me sens utile » n'est pas observable, contrairement à la consigne.
- **B** : la zone « éviter » recueille les irritants sans renvoi à l'Ex. 2 ni retournement en critère.
- **E** : le minimum financier du carnet 4 n'est pas cité ; l'engagement p. 18 « J'emporte ma liste de conditions de travail en entretien » n'a pas d'outil.
- Recommandations :
  - Un seul exemple contrasté : « *Exemple.* En surface : « Une bonne ambiance. » Exploitable : « Une équipe stable, un point d'équipe par semaine, pas de réunion après 18 h. » »
  - Consigne : « Reprenez vos irritants de l'exercice 2 : chacun devient une condition à rechercher. Ajoutez votre minimum sécurisant du carnet 4. »
  - Ajouter une colonne « La question à poser en entretien pour le vérifier » (par exemple « Comment se passe une semaine type dans l'équipe ? »).

### Exercice 8 · Tensions (p. 15-16) · `synthese.py:23-43`. Affiché 10 min, réaliste 15-20 min
- **D** : bon format (cocher, puis détailler deux tensions). Mais champs de 37 pt (une ligne manuscrite), dont le premier redemande les valeurs déjà cochées (`synthese.py:36`) ; p. 16 vide à 60 %.
- **E** : « Sens / rémunération » et « Liberté / sécurité » doublonnent le carnet 4, p. 9, sans le citer.
- **C** : l'équilibre reste souvent non tranché, sans place pour le dire.
- Recommandations :
  - Libellés : « Une situation où elle est apparue » (2,2 cm), « Jusqu'ici, je privilégie… au détriment de… », « Le compromis acceptable pour moi », « Ce que je n'arrive pas encore à trancher (pour la séance) ».
  - Ajouter : « Pour sens / rémunération ou liberté / sécurité, reprenez vos seuils du carnet 4, p. 12. »
  - Placer l'exercice avant l'Ex. 7, pour que les conditions intègrent les compromis.

### Exercice 9 · Synthèse (p. 17) · `synthese.py:46-63`. Affiché 10 min, réaliste 10 min
- **D/I** : 7 champs de 1,2 cm ; `templates.py:740` ne passe en multiligne qu'au-delà. D'où une ligne en 11 pt fixe et `doNotScroll` (`forms.py:61`), environ 80 caractères : « Pour les respecter, j'ai besoin de : » est censuré.
- **Doublons** : les 3 valeurs sont saisies pour la quatrième fois ; « Je me sens aligné·e » et « Je perds de l'énergie » répètent les synthèses p. 5 et 7.
- **Charte/C** : l'amorce « Je me sens aligné·e » (`synthese.py:55`) accorde un participe ; pas de zone « Ce qui m'étonne ».
- Recommandations :
  - Remplacer l'amorce par « Je suis à ma place quand : ».
  - Passer les champs à 1,8 cm.
  - Remplacer les lignes 57-58 par une grille de 3 lignes : Valeur | Condition observable | Signal d'alerte | Question d'entretien (`add_table`). C'est le livrable réutilisable.
  - Ajouter « Ce qui m'étonne dans ce carnet : ».

### Livrable et dos (p. 18-19) · `synthese.py:67-80`
- **C** : la zone de notes de 362 pt (15 lignes) n'est pas guidée. Les engagements sont concrets et bien formulés.
- Recommandation : la découper en trois zones de 3 lignes. « Ce qui m'étonne », « Ce que je n'arrive pas à trancher », « À aborder en séance ».

## 3. Charge émotionnelle

| Exercice | Niveau | Avertissement | Optionnalité | Clôture | Question plus franche possible (une fois le protocole posé) |
|---|---|---|---|---|---|
| Ex. 2 Désalignement (p. 6-7) | Fort | Absent | Absente | Absente (la synthèse nomme des valeurs, sans phrase d'ancrage) | « Une situation où j'ai agi contre l'une de mes valeurs, et ce qui m'y a poussé. » |
| Ex. 3 Choix difficiles (p. 8) | Moyen | Absent | Absente | Absente | « Le choix que je regrette encore, et ce qu'il dit de ce qui compte pour moi. » |
| Ex. 8 Tensions (p. 15-16) | Faible à moyen (« celle que vous sacrifiez », « engagement / protection de soi ») | Absent | Absente | Partielle (« le compromis à rechercher ») | « La valeur que j'affiche et que je ne m'accorde pas. » |
| Ex. 6 Q3 (p. 11-13) | Faible | Non requis | Non requise | Non requise | « Ce que je ressens quand elle manque depuis longtemps. » |
| Ex. 1, 4, 5, 7, 9 | Faible | Non requis | Non requise | Non requise | Ex. 5 : « La valeur que je coche surtout parce qu'elle est attendue de moi. » |

## 4. Fil rouge

**Entrées.**
- Aucune entrée explicite venue d'un carnet précédent. Les seuls renvois sont internes (Ex. 4 vers Ex. 1-3, Ex. 5 vers Ex. 4).
- Entrées implicites non citées :
  - carnet 2 : « ce que j'ai aimé / pas aimé » (Ex. 2), moteurs fondamentaux (Ex. 3), sommets et vallées (Ex. 4) ;
  - carnet 1 : « Je ne veux plus subir » (Ex. 4), mentors et anti-modèles (Ex. 7), « 5 mots pour mon futur travail » (Ex. 6), valeurs familiales du 3FVS (Ex. 5) ;
  - carnet 4 : tension sécurité / utilité (p. 9), seuils (p. 12), huit tendances (p. 13-14), qui se rapprochent des familles de valeurs (sécuritaire et Sécurité, indépendant et Liberté, ambitieux et Réussite).
- Le récapitulatif de la séance sur l'argent manque. C'est la seule séance du parcours qui n'est jamais consolidée.

**Sorties.**
- Carnet 6, Ex. 1 : reprend exactement les 3 valeurs, les conditions et les tensions. Bien fait. Ex. 2 : reprise implicite (« Mes valeurs, mes besoins, mes sources de stress »).
- Les fiches métiers du carnet 6 (p. 7-10) n'ont aucune ligne pour confronter une piste aux 3 valeurs : l'engagement p. 18 (« J'évalue chaque piste à l'aune de mes 3 valeurs ») reste sans outil.
- Livret : le thème 6, p. 12, renvoie aux valeurs sans citer le carnet 5 ; le « cadre de sécurité non négociable » du thème 7, p. 14, est purement matériel et devrait intégrer les 3 valeurs.

**Doublons.**
- Ex. 1-2 avec la ligne de vie et l'« aimé / pas aimé » du carnet 2.
- Ex. 7 avec le livret p. 3 (« climat idéal », « ce qui vide mes batteries ») et p. 5 (« exigences de qualité : autonomie, relations saines… »).
- Ex. 8 avec le carnet 4, p. 9.
- Le titre « choix difficile » existe déjà dans le carnet 3 (Q8).
- Les 3 valeurs sont saisies quatre fois dans le carnet.

**Ruptures.**
- Les « moteurs » du titre ne sont jamais travaillés, alors que le carnet 2 en a produit cinq.
- La séance sur l'argent n'est pas récapitulée.
- Les valeurs ne sont pas confrontées aux pistes dans le carnet 6.

## 5. Écart avec l'app web

- `_build_chap5_spec` (`server/predefined_workbooks.py:690`) est un autre carnet : « L'exploration du terrain » (météo, grille d'entretien métier, idées reçues et réalité, plan de contact).
- Aucune liste de valeurs, ni hiérarchie, ni non-négociables, ni tensions n'existe côté web.
- Les valeurs ne figurent que dans le titre du chap4 web, « Valeurs, limites et argent » (limites par domaine, seuils), et dans l'annonce de clôture du chap3 web (ligne 546).
- La numérotation est décalée (chap6 web = plan d'action). Personnaliser « chap5 » via `/api/customize` produit donc un carnet terrain.

## 6. Recommandations classées

| Priorité | Type | Page(s) | Constat | Recommandation |
|---|---|---|---|---|
| P1 | Correction rapide | 6-7 | Ex. 2 fortement chargé, sans protocole | Avertissement, optionnalité (« laissez-le vierge, nous l'aborderons ensemble »), clôture « Aujourd'hui, avec le recul, je sais que… » |
| P1 | Correction rapide | 4-17 | Durées sous-estimées de moitié (95 min contre 2 h 30-3 h), sans mention du fractionnement | Durées : 20, 20-25, 15-20, 10-15, 10-15, 10 par valeur, 15-20, 15-20, 10 min. Ajouter le total et « en trois fois » p. 3 |
| P2 | Correction rapide | 8 | Ex. 3 chargé, sans protocole | Même protocole, en version courte |
| P2 | Refonte légère | 6-7, 14 | Irritants non retournés en critère | Champ « Donc, dans mon prochain poste, j'ai besoin de… » ; Ex. 7 relié à l'Ex. 2 |
| P2 | Correction rapide | 4, 6, 11, 14 | Aucun exemple contrasté ; exemples de l'Ex. 7 recopiables | Un exemple « en surface / exploitable » par exercice (textes en section 2) |
| P2 | Correction rapide | 9 | 3 doublons, pôles des tensions absents (Rémunération, Appartenance…), pas de champ libre, pas de volume | Liste corrigée, 3 champs libres, consigne « 15 à 20 valeurs » |
| P2 | Correction rapide | 10 | Pas d'emplacements numérotés ; définition placée après ; aucun critère | `add_numbered_lines` 10/5/3, encadré avant l'étape 3, test « si elle manquait six mois » |
| P2 | Correction rapide | 10-13 | Distinction « je veux / on attend de moi » absente | Q2 de l'Ex. 6 : « Cette valeur me vient de… Je la garde parce que… » ; ligne dédiée à l'Ex. 5 |
| P2 | Correction rapide | 17 | Champs d'une ligne limités à environ 80 caractères | Hauteur 1,8 cm (multiligne) |
| P2 | Refonte | 17-18 | Sortie dispersée, rien de prêt à reprendre en carnet 6 ou en entretien | Grille Valeur, condition, signal d'alerte, question d'entretien ; à reprendre dans les fiches du carnet 6 |
| P2 | Refonte | 3 | Pas de récapitulatif de la séance sur l'argent ; entrées des carnets 1, 2, 4 non citées | Page récap (seuil retenu, tendance dominante, ce que l'argent protège) ; renvois explicites aux Ex. 1, 4, 7, 8 |
| P2 | Correction rapide | 8, 15-16 | Champs de 37 pt (1 ligne manuscrite) pour des contenus doubles | Champs scindés côte à côte, hauteur 2,2 cm |
| P2 | Correction rapide | 18 | Notes non guidées ; pas de « Ce qui m'étonne » ni « À aborder en séance » | Trois zones guidées |
| P2 | Correction rapide | 3 | Cadre non rappelé alors que le carnet est chargé | Phrase de cadre (propriété, droit de passer) |
| P3 | Correction rapide | 3, 4, 6, 17 | Accords au point médian dans les consignes et dans l'amorce p. 17 | Formulations en noms, « Je suis à ma place quand » |
| P3 | Correction rapide | 3 | « Moteurs » jamais définis | Définition valeur / moteur / besoin |
| P3 | Refonte légère | 11-13 | Trois pages identiques ; aucune échelle | Échelle 1-5 « respectée aujourd'hui » suivie d'un « pourquoi » |
| P3 | Correction rapide | 14-16 | Tensions placées après les conditions | Ex. 8 avant l'Ex. 7 |
| P3 | Correction rapide | 9 | « Marge de manœuvre » dans la liste | Remplacer par « Latitude » |
