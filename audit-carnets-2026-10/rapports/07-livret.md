# Audit du livret de compétences « Votre portfolio de compétences »

PDF de 17 pages, 34 champs dont 28 zones libres. Code : `Scripts/workbook_generator/chapters/livret/` (fichiers cités sans chemin), ordre dans `Scripts/main_generate_livret.py:42-74`.

## 1. Synthèse

Livret aéré, aux intentions justes (travail réel, travail empêché, paliers, récit d'action), mais qui ne tient pas sa promesse et ne consolide pas le parcours. Trois problèmes dominent :
1. La preuve par les faits n'est guidée qu'une fois (un récit, p. 10-11) ; ailleurs, les compétences sont listées sans situation ni résultat, et aucune page ne les synthétise.
2. Aucun renvoi aux carnets : la personne refait MBTI®, conditions de travail, minimum vital, pistes ; valeurs, seuils, dix pistes et objectif boussole ne sont jamais repris.
3. Les exemples suivent un seul profil (une dizaine citent le bâtiment ou l'énergie, la piste formateur ou enseignant revient 4 fois) : recopie probable, peu d'aide ailleurs, détails personnels à vérifier.

Le reste (ouverture absente, cases toutes identiques, accords genrés, « déclic ») se corrige vite.

## 2. Thème par thème

### Structure, couverture et ouverture (p. 1) · total estimé 3 h 30-4 h 30
- **Structure** : la couverture enchaîne sur le thème 1 (`main_generate_livret.py:42-46`). Des thèmes plutôt que des « Exercice N » : choix défendable pour un portfolio, qu'on relit par rubrique. Mais rien n'oriente (but, moment, nombre de fois, carnets à ouvrir, définition d'une « compétence prouvée »), et pas de récapitulatif de séance, contrairement aux carnets 2 à 6.
- **D** : 14 pages identiques, 28 cases de même taille (450 × 122-141 pt : 5 lignes manuscrites, environ 900 caractères tapés avant que la police rétrécisse). Ni échelle, ni liste, ni tableau. Aucune durée, alors que le carnet 5 en affiche (`chap5/alignement.py:28`).
- **H** : le cadre se limite à « Ce carnet reste le vôtre » (p. 17). Or un portfolio se montre (« en entretien », « avant chaque candidature », `plan_action.py:101-102`), et le livret mêle pages présentables et pages privées (salaire, enfants, épuisement).
- **Couverture** : « Livret de compétences » et « … augmenté » font doublon ; « augmenté » est du jargon (`cover.py:9-10`).
- **Reco** : une ouverture `create_standard_summary_page` : « Ce livret rassemble vos compétences et leurs preuves. Remplissez-le après le carnet 6, en quatre à six fois, vos carnets ouverts à côté. Comptez 30 à 40 minutes par thème. Les thèmes 3 à 5 peuvent se montrer en entretien. Les autres restent pour vous. Une question vous bloque ? Passez-la et notez-la pour la séance. » Puis la liste des thèmes, et la durée dans chaque pastille (« Thème 1 · Profil et énergie · 30 min »).

### Thème 1 · Profil et énergie (p. 2-3) · 25-40 min
- **E** : type MBTI® et forces déjà demandés aux carnets 4 (ex. 1) et 6 (ex. 2) ; climat idéal et environnements à éviter aux carnets 5 (ex. 7, 9) et 6. « si exploré » (`profil.py:33`) ignore que le carnet 3 prépare la restitution MBTI®.
- **B** : la p. 3 croise recharge et coût, mais « ce qui vide mes batteries » (`profil.py:86`) n'est pas retourné en critère.
- **A** : l'exemple ISFJ (`profil.py:35`) livre une étiquette toute faite, au masculin.
- **Charte** : « quand vous êtes détendu » (`profil.py:22`) → « à l'aise ».
- **Reco** : une seule page de report : « Reportez votre type MBTI® restitué en séance (carnet 4, exercice 1). Notez les deux forces où vous vous reconnaissez le plus. » Puis : « Ce qui me vide : … Donc mon prochain poste doit : … ».

### Thème 2 · Travail réel (p. 4-5) · 30-40 min
- **A, F** : l'apport le plus original du livret. « Ce que ma fiche de poste ne dit pas » et « mes astuces maison » produisent de vraies preuves ; l'intro dit à quoi elles servent.
- **B** : p. 5, le travail empêché devient des « exigences pour demain » : bon retournement, mais qui refait le carnet 5, ex. 7.
- **F** : temps incohérents (« réalisez… n'étaient écrits », `travail_reel.py:33-34`). « Votre précédent poste » (l. 76) suppose un départ, contre « poste actuel » p. 9 (`autonomie.py:64`). « Travail empêché », « ergonomes » (l. 64-65) : le carnet 2 dit « activité empêchée », « psychologie du travail ». « Presque jamais de la paresse » : non sourcé et maladroit.
- **Charte** : « ne vous avaient pas freiné », « fier de votre geste » (l. 76, 87).
- **Reco** : amorce p. 4 : « Chaque semaine, sans que ce soit écrit nulle part, je… ». Pour la p. 5 : « Le carnet 2 parlait d'activité empêchée. Quel travail auriez-vous voulu mieux faire, si les moyens, les délais ou les règles l'avaient permis ? » Puis : « Pour faire un travail que je juge bien fait, j'ai besoin de… ».

### Thème 3 · Compétences en action (p. 6-7) · 25-35 min
- **E** : refait, sans la citer, la colonne « compétences développées (techniques, relationnelles) » du carnet 2 (ex. 2). Les compétences de vie (carnet 2, ex. 5) sont ignorées.
- **A, F** : questions déclaratives (`cartographie.py:32, 74`), exemples en listes sans preuve (« RE2020, CAO… », l. 34) : le format contredit la couverture. Aucun nombre d'items attendu.
- **Reco (refonte)** : à la p. 6, un `add_table` de 5 lignes : « Compétence (verbe + objet) », « Où je l'ai prouvée », « Résultat ou trace », « Envie de l'utiliser demain (oui / plutôt / non) ». Exemple contrasté, hors bâtiment :
  - *Réponse de surface* : « Gestion des stocks. »
  - *Réponse exploitable* : « Réorganiser un stock de pièces détachées · entrepôt, 2023 · les ruptures deviennent rares, l'équipe garde mon tableau · oui. »

### Thème 4 · Autonomie et transférabilité (p. 8-9) · 30-40 min
- **F** : paliers clairs (`autonomie.py:21-25`) ; « l'épreuve du miroir » est une excellente question.
- **D** : « 2 ou 3 compétences, un niveau, un pourquoi » dans une seule case (l. 34), « les 3 grandes compétences » aussi (l. 74).
- **B** : compétence et énergie ne sont jamais croisées, alors que le carnet 3 web le fait (« Je sais faire, mais cela m'épuise », `server/predefined_workbooks.py:497`).
- **E** : « Dans quels nouveaux métiers » refait les dix pistes du carnet 6. Le retour des proches (carnet 6, ex. 3), preuve extérieure, n'est pas repris.
- **Charte** : « seul » (l. 23), « un candidat précieux » (l. 86) → « un profil recherché ».
- **Reco** : `add_rating_grid` (une ligne radio 1 à 4 par compétence) puis un pourquoi court ; `add_numbered_lines` pour les trois compétences ; une page en quatre zones (`create_standard_quadrants_page`, `components.py:620`). Amorce miroir : « Ce qu'on vient souvent me demander, et que je fais sans y penser : … ». p. 9 : « Pour chacune de vos pistes réalistes (carnet 6), quelle compétence vous ouvre la porte ? »

### Thème 5 · Récit d'action (p. 10-11) · 30-45 min
- **A, F** : seul exercice proche de la méthode STAR (situation et mission, signal, actions, résultat), aux sous-questions précises ; « même simple ou modeste » (`recit_action.py:22`) rassure.
- **Limites** : une seule situation, pourtant l'appui des entretiens (engagement p. 16) ; rien ne dit ce qu'elle prouve ; pas de version orale ; champ 4 à double question (l. 83-84).
- **E** : rien n'invite à puiser dans les sommets de la ligne de vie (carnet 2) ou les situations d'alignement (carnet 5, ex. 1).
- **Charte** : « déclic » (l. 16, 38) est hors charte. « Bloqué sur un dossier » (l. 33) et « le plus fier » (l. 84) genrent, alors que le titre dit « fier ou fière » (l. 79). Titre p. 10 coupé après « le ».
- **Reco** : titre « Arrêt sur image : la situation et le signal. », champ 2 « Le signal qui vous a fait agir ». Exemple neutre : « Lundi, 8 h : deux formations sont prévues dans la même salle, vingt personnes arrivent à 9 h. » Un deuxième récit (un technique, un relationnel) en `add_fields_card`. Clore par « Ce récit prouve que je sais : 1. … 2. … » et « Mon récit en trois phrases, pour un entretien : … ».

### Thème 6 · Projection (p. 12-13) · 25-35 min
- **A** : « Quelles évolutions sociétales, écologiques ou techniques » (`boussole.py:32`) : abstrait, orienté par l'exemple (« sobriété d'usage »), valeurs évoquées sans renvoi au carnet 5.
- **E** : « qui interviewer » (l. 73) refait l'interview du carnet 2 et l'engagement du carnet 6 ; « mes réussites passées » recoupe les vallées de la ligne de vie. Rupture la plus nette : l'objectif boussole (carnet 1, ex. 3) n'est jamais relu, alors que le carnet 1 promet de servir « de référence pour mesurer le chemin parcouru ».
- **Charte** : « il faut mener des enquêtes » (l. 63) ; « subir passivement » (l. 22-23) culpabilise.
- **Reco** : « Relisez votre objectif boussole (carnet 1, exercice 3). Ce qui est clarifié : … Ce qui reste ouvert : … » ; « Mes 3 valeurs non négociables (carnet 5) et la piste qui les respecte le mieux : … » ; « Les professionnels rencontrés depuis le carnet 6, et ce que j'en retiens : … ».

### Thème 7 · Plan d'action (p. 14-15) · 25-35 min
- **E** : « salaire net minimum vital » (`plan_action.py:33`) refait les seuils du carnet 4 (ex. 6) ; les pistes A et B ne sont pas tirées des dix pistes du carnet 6.
- **F** : la piste A est un « projet d'élan, de transmission et de sens » (l. 44). « Transmission » vient du profil des exemples : la personne lit qu'une bonne piste doit transmettre.
- **D** : A et B dans une même case ; le « petit pas », une seule action, dispose de 5,2 cm (l. 74) sans date ni personne à prévenir.
- **Chiffres, jargon** : « garantie à 100 % », « pas proximal » (l. 65-66) ; heures « finançables CPF » (l. 86-88), non sourcées ; « le plus grand piège d'une reconversion » (l. 64) suppose une reconversion ; exemple très personnel (« 3 enfants », « aucun découchage », l. 35).
- **Reco** : « Reportez vos seuils du carnet 4 : minimum vital, minimum sécurisant, durée acceptable d'une baisse » (`add_fields_card`). Deux colonnes A / B : intitulé, carnet d'origine, valeurs respectées, coût ; « Piste A : le projet qui vous attire le plus. Piste B : le projet le plus sûr, ou un tremplin. » « Votre premier pas : une démarche simple, faisable dans les 7 jours. Ce que je fais : … Le : … Je préviens : … » Un `add_link_card` vers moncompteformation.gouv.fr à la place des volumes d'heures.

### Livrable (p. 16) · 10 min
- **C** : « Mes notes » (476 × 362 pt, 15 lignes) n'est pas guidé : ni étonnement, ni « à aborder en séance ». Le livrable annonce « vos compétences », qu'aucune page ne rassemble. Le 3e engagement (l. 103) répète la p. 15.
- **Reco** : avant le livrable, une page « Mes compétences prouvées » (`add_table` : compétence, preuve, niveau 1 à 4, envie). Notes en trois zones : « Ce qui m'étonne en relisant mon parcours : … », « La compétence dont je doute encore : … », « La question à trancher en séance : … ».

## 3. Charge émotionnelle

Charge globalement faible (livret de valorisation ; le récit d'action, p. 10-11, est rassurant). Deux pages montent à moyen, sans protocole.

| Exercice (page) | Niveau | Présent | Absent | Question plus franche (protocole en place) |
|---|---|---|---|---|
| Ce qui vide mes batteries (p. 3) | faible à moyen (fort en cas d'épuisement) | rien | avertissement, optionnalité, clôture | « La situation de travail que je ne veux plus revivre, et ce qu'elle m'apprend pour la suite. » |
| Travail empêché (p. 5) | moyen | normalisation (`travail_reel.py:64`) ; le 2e champ tourne vers demain (clôture partielle) | avertissement, optionnalité, phrase d'ancrage | « Le travail que j'ai dû mal faire, et qui me reste en travers. » |
| Degrés d'autonomie (p. 8) | faible | « ni bon ni mauvais » (`autonomie.py:21`) | sans objet | « La compétence que je sous-estime, et la preuve que je la maîtrise. » |
| Réussites passées (p. 13) | faible à moyen | cadrage positif | optionnalité | « La fois où j'ai cru ne pas y arriver, et ce qui m'a permis de passer. » |
| Cadre de sécurité (p. 14) | moyen (argent, famille) | intro rassurante mais injonctive (`plan_action.py:22`) | avertissement, optionnalité, confidentialité | « Le compromis que je ne referai plus, même pour un meilleur salaire. » |

Protocole à poser p. 5 (et adapter p. 14), par exemple avec `add_annotation` :
1. Avant : « Cette page revient sur des moments où vous n'avez pas pu bien faire votre travail. Elle peut réveiller de la frustration. »
2. Optionnalité : « Si elle vous pèse, laissez-la vierge : nous l'aborderons ensemble en séance. »
3. Clôture : « Aujourd'hui, avec le recul, je sais que ce frein venait de… et que demain je demanderai… »

## 4. Fil rouge

Le livret ne cite aucun carnet. Le mot « carnet » n'y apparaît qu'au dos (p. 17).

| Thème | Carnet(s) source(s) | Reprise explicite | Doublon | Rupture ou manque |
|---|---|---|---|---|
| 1 Profil et énergie | 3 ; 4 ex. 1 ; 5 ex. 7 et 9 ; 6 ex. 2 | non (« si exploré ») | fort : MBTI®, forces et conditions demandés une 3e fois | météo du carnet 1 non relue |
| 2 Travail réel | 2 ex. 2 et « À lire » ; 5 ex. 2 ; 1 (« Je ne veux plus subir ») | non | partiel : « exigences pour demain » = carnet 5 ex. 7 | concept renommé (« travail empêché ») |
| 3 Compétences | 2 ex. 2 et 5 | non | fort : même découpage technique / relationnel | compétences de vie ignorées |
| 4 Autonomie | 2 ex. 5 et arbre (tronc) ; 6 ex. 3 à 6 | non | p. 9 = dix pistes du carnet 6 | retour des proches non repris |
| 5 Récit | 2 ex. 4 (sommets) ; 5 ex. 1 | non | non (méthode nouvelle) | sans objet |
| 6 Projection | 0 ex. 1 ; 1 ex. 3 ; 2 ex. 3 et bonus ; 5 | non (« vos valeurs » sans renvoi) | p. 13 = interview du carnet 2 | boussole, « Je m'autorise à », moteurs : jamais relus |
| 7 Plan d'action | 4 ex. 6 ; 5 ex. 8 ; 6 ; 0 ex. 4 | non | minimum vital redemandé | tensions de valeurs et soutiens (carnet 0) absents |

Bilan : l'énergie est consolidée, mais par répétition. Valeurs, argent, pistes métiers et moteurs ne le sont pas. Les irritants le sont à moitié (p. 3, sans critère).

## 5. Écart avec l'app web

Le livret n'existe pas dans l'app web : `PREDEFINED_WORKBOOKS` ne contient que chap0 à chap6 et `business_plan` (`server/predefined_workbooks.py:1202-1210`), donc pas de personnalisation par `/api/customize`. L'app web a en revanche deux éléments qui manquent au livret CLI : les quatre zones de compétences croisées avec l'énergie (l. 489-497) et l'arbitrage piste A / piste B avec feuille de route à 30, 60 et 90 jours (l. 878, 905).

## 6. Recommandations classées

| Priorité | Type | Page(s) | Constat | Recommandation |
|---|---|---|---|---|
| P1 | Correction rapide | ouverture, pastilles | Ni but, ni durée (3 h 30-4 h 30), ni « en plusieurs fois », ni carnets à ouvrir : risque d'abandon devant 14 pages identiques | Page d'ouverture (texte en section 2) et durée dans chaque pastille de thème |
| P2 | Refonte | 6-9, nouvelle page avant 16 | Compétences listées sans preuve, aucune synthèse | Tableau compétence / preuve / résultat / envie ; page « Mes compétences prouvées » |
| P2 | Refonte | 10-11 | Un seul récit, sans « ce qu'il prouve » ni version orale | Deuxième récit ; « Ce récit prouve que je sais… » ; « Mon récit en trois phrases » |
| P2 | Correction rapide | 2-3, 9, 13, 14 | Aucun renvoi ; doublons MBTI®, conditions, minimum vital, métiers | Phrases de report (« carnet 4, exercice 6 ») ; thème 1 réduit à une page |
| P2 | Refonte | 9, 12, 14 | Valeurs, seuils, dix pistes, boussole, moteurs, retour des proches jamais consolidés | Questions de relecture (textes en section 2) |
| P2 | Correction rapide | toutes | Exemples d'un seul profil, sans contraste ; détails personnels (BTS puis ingénieur, 3 enfants) | Un exemple contrasté par thème, métiers variés ; vérifier qu'ils ne viennent pas d'un dossier réel |
| P2 | Correction rapide | 14 | « Transmission » dans la définition de la piste A | « Piste A : le projet qui vous attire le plus. Piste B : le plus sûr, ou un tremplin. » |
| P2 | Refonte | 8, 9, 14, 15 | Plusieurs items dans une seule case | `add_rating_grid`, `add_numbered_lines`, colonnes A / B, champs action / date / personne |
| P2 | Refonte | 6-9 | Compétence et énergie jamais croisées | Page en quatre zones (`create_standard_quadrants_page`) |
| P2 | Correction rapide | 3 | Irritants non retournés en critères | « Ce qui me vide : … Donc mon prochain poste doit : … » |
| P2 | Correction rapide | 5, 14 | Charge moyenne sans protocole | Avertissement, optionnalité, phrase d'ancrage (section 3) |
| P2 | Correction rapide | ouverture, 14 | Portfolio à montrer, mais pages privées, sans confidentialité ni droit de passer | Dire ce qui se montre et ce qui reste privé |
| P3 | Correction rapide | 2, 5, 8-11, 15 | Accords genrés (détendu, freiné, fier, seul, candidat, bloqué, paralysé) ; « déclic » hors charte | Formulations neutres ; « la situation et le signal » (section 2) |
| P3 | Correction rapide | 5, 15 | « À 100 % », heures CPF, « paresse » non sourcés ; « pas proximal » ; « ergonomes » ; départ supposé (« précédent poste », « reconversion ») | Supprimer ou sourcer ; « activité empêchée » du carnet 2 ; « votre poste actuel ou le dernier » ; lien CPF |
| P3 | Correction rapide | 16 | Notes non guidées | Trois zones : étonnement, doute, question à trancher |
| P3 | Correction rapide | 1 | « Augmenté », eyebrow et tagline redondants | Tagline « Bilan de compétences », comme les carnets |
