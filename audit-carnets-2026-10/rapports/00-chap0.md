# Audit du carnet 0 « Le prélude »

## 1. Synthèse

Verdict : un carnet court (environ 1 h 15), aéré, au ton juste, mais qui ne pose pas le cadre qu'il annonce (« Poser le cadre du bilan », p. 2) et reste proche du questionnaire : 11 zones d'écriture libre, aucune amorce, aucun exemple, aucune durée.
1. Cadre absent (axe H, P1) : rien sur la confidentialité, le droit de passer une question ou ce qu'on fait d'une question trop lourde, et aucun carnet suivant ne le pose.
2. Page blanche (axe A, P2) : les 8 questions de « Faire le point » et l'objectif sont abstraits, sans amorce ni exemple contrasté ; l'exercice 2 a deux doublons internes et dépasse 30 min.
3. Fil rouge (axe E, P2) : objectif, domaines de vie et humeur sont redemandés par le carnet 1, qui se dit lui aussi « point de départ », sans renvoi ; « Je m'autorise à » et l'entourage ne sont jamais repris.

## 2. Exercice par exercice

### Ouverture (p. 1-4) · lecture 5-8 min

- **Couverture et sommaire** (p. 1-2, `chap0/intro.py:10-30`) : promesse claire, question centrale forte (« quelle place voulez-vous donner au travail dans votre vie, et sous quelle forme ? », `intro.py:21-22`). **D** : aucune durée, ni par exercice ni pour le carnet, alors que le carnet 5 affiche « · 10 MIN » dans ses sourcils.
- **Mot d'accueil** (p. 3, `intro.py:33-62`). **H** : seuls éléments de cadre du parcours : « nous les relisons ensemble » et « Notez ce qui vous vient sans vous censurer : le tri se fait en séance » (`intro.py:43-44`). Manquent : qui lit les réponses, ce qui est transmis (employeur, financeur), le droit de laisser une question vierge, le sort d'une question trop lourde, la possibilité de remplir en plusieurs fois. Le bas de la page est vide (environ 7 cm) : la place existe. **I** : l'espace Notion est annoncé sans lien (`intro.py:57-61`) alors que l'URL existe dans `chap6/ressources.py:33-34` ; aucun mode d'emploi du PDF (lecteur, enregistrement après chaque session, impression possible). **F** : la frise (`intro.py:47-56`) donne quatre étapes sans les rattacher aux carnets : la personne ne sait pas où se situent les sept carnets et le livret.
- **Comprendre pour décider** (p. 4) : bonne annonce des héritages. « La psychologie et la sociologie le montrent » (`intro.py:71`) est un argument d'autorité non sourcé (P3).

Recommandations :
- Ajouter en bas de p. 3 un encadré (callout) « Le cadre de travail. » :
  > Vos réponses vous appartiennent. Seule la personne qui vous accompagne les lit, avec vous, en séance. Rien n'est transmis à un employeur ou à un financeur sans votre accord explicite.
  > Vous pouvez passer une question. Laissez-la vierge : nous en parlerons en séance, si vous le souhaitez.
  > Une question vous pèse ? Notez-la en fin de carnet, dans « À aborder en séance ». Nous la traiterons ensemble.
  > Chaque carnet se remplit en plusieurs fois : comptez 1 h 30 à 3 h au total. Enregistrez le fichier après chaque session, ou imprimez-le pour écrire à la main.

  Les deux repères sont sourcés par la brochure programme : `programme/page_organisation_pedagogie.py:44` (1 h 30 à 3 h par carnet) et `programme/page_infos_pratiques.py:61-62` (aucun tiers sans accord, art. L. 6313-4 du Code du travail).
- Frise : écrire les carnets sous chaque étape (« Carnets 1-2 · Choix passés », « Carnets 3-5 · Forces, envies », « Carnet 6 · Métiers », « Livret · Plan d'action »).
- Remplacer le callout Notion par `add_link_card` avec l'URL du carnet 6.

### Exercice 1 · Mon engagement (p. 5) · 10-15 min

- **F** : seul exercice sans chapeau qui dit pourquoi (`intro.py:91-126`). Proposition : « Un bilan avance au rythme du temps que vous lui donnez. Fixez ce temps, puis votre point d'arrivée. Nous relisons cet engagement en séance : il peut évoluer. »
- **D/F** : le champ heures (39 × 18 pt) n'a aucun repère ; la personne peut promettre un volume intenable et culpabiliser ensuite. Ajouter sous la phrase : « Repère : un carnet demande 1 h 30 à 3 h, et les séances sont espacées d'une à deux semaines » (`programme/page_organisation_pedagogie.py:14,44`). En option, une ligne « Mes créneaux (jour, moment) : … », plus concrète qu'un nombre d'heures.
- **A** : « Mon objectif principal » est la question la plus abstraite du carnet, dans une case de 5,3 cm (`max_box_height=5.5 * cm`, `intro.py:126`) qui appelle un paragraphe flou. Amorce et exemple :
  > À la fin du bilan, je veux savoir si… et pouvoir…
  > **Exemple.** Réponse de surface : « Trouver ma voie. » Réponse exploitable : « À la fin du bilan, je veux savoir si je reste dans la restauration en changeant de poste, ou si je me forme à un métier de bureau, et pouvoir annoncer une première démarche datée. »

  Ramener les deux cases à 2,5-3 cm.
- « Je m'autorise à » est la meilleure question du carnet (la seule projective). Amorce : « Je m'autorise à étudier… même si… ».
- **E** : l'horizon « fin du bilan » (champ `objectif_3_mois`, `intro.py:122`) diffère du carnet 1 (« D'ici 3 mois », `chap1/exercices.py:41`) et du web (« 3 à 4 mois »).

### Exercice 2 · Faire le point (p. 6-7) · 30-40 min

- **A** : 8 questions ouvertes, 8 cases identiques (450 × 90 pt), aucune amorce, aucun exemple : c'est la partie la plus « questionnaire RH » du carnet, et elle dépasse la granularité de 15-30 min.
- **F** : deux doublons internes (`exercices.py:8-17`) : Q3 « De quoi j'ai besoin en ce moment ? » et Q7 « Quels besoins sont insatisfaits dans ma vie aujourd'hui ? » ; Q4 « Qu'ai-je fait… pour remédier à cette situation ? » et Q5 « Qu'est-ce que je n'ai pas encore changé ? Pourquoi ? » (question double). « Cette situation » présuppose un problème, alors qu'on peut venir pour évoluer. Q8 « Quelles actions concrètes puis-je mettre en place ? » arrive trop tôt : avant toute exploration, elle produit du vague ou de la pression.
- **B** : Q6 « Quels avantages ai-je à garder la situation telle quelle ? » (`exercices.py:14`) est la question la plus riche, mais rien n'explique pourquoi on la pose ; elle peut sonner comme un reproche. Rien ne distingue « je veux » de « on attend de moi » : le déclencheur (Q2) est l'endroit naturel. Les irritants (Q5, Q7) ne débouchent sur aucun critère.
- **G** : charge moyenne, aucun élément du protocole (section 3).
- **D** : police automatique dans des cases de 3,2 cm : une longue réponse rétrécit.

Recommandations (mêmes composants, `page_break()` déjà en place) :
- Deux parties affichées « 15-20 min » chacune. **Partie 1, où vous en êtes** : Q1 avec amorce « En ce moment, je me sens… surtout quand… » ; Q2 suivie de « Ce bilan vient-il d'abord de vous, ou d'une demande extérieure (employeur, proche, conseiller) ? » ; Q3 et Q7 fusionnées en « Mes trois besoins les plus urgents » (trois cases d'une ligne).
- **Partie 2, ce qui vous retient** : Q4 et Q5 fusionnées (« Ce que j'ai déjà essayé, et ce qui m'a arrêté ») ; Q6 précédée de « Chaque situation, même pesante, apporte quelque chose. Le repérer dit ce que votre projet devra préserver. » ; Q8 remplacée par une ligne « Une seule chose que je peux faire d'ici la prochaine séance : ».
- Exemple unique, sous Q6 :
  > **Exemple.** Réponse de surface : « Aucun. » Réponse exploitable : « Un salaire régulier, une équipe que j'apprécie, et le confort de ne pas tout réapprendre. »

### Exercice 3 · Vos domaines de vie (p. 8) · 12-15 min

- **D** : bon format rapide (une échelle radio 1-10 par domaine, `exercices.py:50-53`) suivi d'une écriture : la seule respiration du carnet. Pastilles lisibles à l'écran comme à l'impression.
- **D/F** : « Analyse de votre équilibre » pose trois questions dans une seule case de 7,3 cm (`exercices.py:54-60`). Trois cases courtes avec amorces : « Mes deux domaines les plus solides : … » ; « Les deux qui me pèsent le plus : … » ; « Mon travail actuel nourrit… et il abîme… ».
- **B** : une note basse ne devient pas un critère. Ajouter « Donc, mon prochain projet devra… ». Exemple :
  > **Exemple.** Réponse de surface : « Ça va à peu près partout. » Réponse exploitable : « Santé, énergie : 3. Mes horaires décalés en entrepôt me prennent mes week-ends. Donc mon prochain poste devra suivre un rythme de journée. »
- **F** (P3) : « Temps pour soi, engagements » mêle deux notions ; la vie sociale n'a pas de ligne. Les bornes « satisfait·e » qualifient la personne : « 1 · Pas du tout satisfaisant » / « 10 · Pleinement satisfaisant » qualifient le domaine et évitent le point médian.
- **E** : doublon avec la « vision à 360° » du carnet 1, sur une autre liste de domaines (`chap1/intro.py:13-19`).

### Exercice 4 · Votre entourage (p. 9) · 10-15 min

- **F** : le but est dit (« sécuriser votre projet »). Bien traité.
- **D** : deux cases de 7,3 cm (207 pt) pour une liste de noms : trop grandes et non structurées. Remplacer par `add_fields_card` ou `add_table` à trois colonnes : « Qui » | « Ce que cette personne peut m'apporter, ou ce qu'elle craint » | « Ce que je fais : la solliciter, l'informer, la préserver », trois lignes par catégorie.
- **B/G** : le « regard négatif » s'arrête au constat (`exercices.py:74-75`) : risque de rumination, charge moyenne (conjoint, parents). Ajouter « Ce que je choisis de lui dire, et quand : … ».
- **A** : exemple unique :
  > **Exemple.** Réponse de surface : « Ma famille. » Réponse exploitable : « Ma sœur, qui a changé de métier il y a deux ans : je lui demande comment elle a financé sa formation. »
- **E** : cette liste est la matière naturelle du carnet 6 (« au moins 3 personnes de votre entourage », `chap6/exercices.py:28`), sans renvoi.

### Fin de carnet (p. 10-11) · 5 min

- **C** : « Mes notes pour la prochaine séance » est une case de 12 cm sans consigne (`components.py:463-468`) : elle intimide et ne joue ni le rôle « Ce qui m'étonne » ni « À aborder en séance ». Remplacer, dans le composant partagé (tous les carnets en profitent), par trois zones courtes :
  > Ce qui m'étonne en remplissant ce carnet : …
  > Une question ou un point de friction à aborder en séance : …
  > Ce que j'ai laissé vierge, à reprendre ensemble : …

  La troisième rend opérationnel le cadre proposé p. 3.
- **F** (P3) : le livrable (`cloture.py:14-15`) oublie l'entourage. Les engagements cochables (`cloture.py:9-13`) prolongent bien l'exercice 1. Le dos (`components.py:498`) est le seul rappel de propriété du parcours.

## 3. Charge émotionnelle

| Exercice | Niveau | Avertissement | Optionnalité | Clôture cadrée | Question plus franche possible (protocole en place) |
|---|---|---|---|---|---|
| Ex. 1 Engagement | faible | absent | absente | absente (inutile) | « Ce que je n'ose pas encore dire à voix haute sur ce que je veux : … » |
| Ex. 2 Faire le point | moyen (épuisement, conflit, licenciement dès Q1-Q2 ; culpabilité possible à Q5-Q6) | absent | absente (seul « sans vous censurer », p. 3) | absente | « Si rien ne change d'ici un an, ce que je risque : … » |
| Ex. 3 Domaines de vie | faible à moyen (famille, santé, argent mal notés) | absent | absente | partielle (l'analyse) | « Le domaine que mon travail abîme le plus aujourd'hui : … » |
| Ex. 4 Entourage | moyen (désaccord du conjoint, des parents) | absent | absente | absente | « La personne dont je redoute le plus la réaction, et ce que je crains qu'elle dise : … » |

Aucun exercice n'est à forte charge : elle arrive dès le carnet 1 (héritage familial, « Ma plus grande peur est »), ce qui rend le cadre de ce carnet d'autant plus nécessaire. Textes à ajouter :
- Chapeau des exercices 2 et 4 : « Ces questions touchent à votre situation personnelle. Si l'une d'elles vous semble trop lourde pour ce travail en autonomie, laissez-la vierge : nous l'aborderons ensemble. »
- Clôture de l'exercice 2 : « Pour clore. Aujourd'hui, ce qui tient encore dans ma situation, c'est… »
- Clôture de l'exercice 4 : « Pour avancer, je peux compter sur… »

## 4. Fil rouge

**Entrées** : aucune attendue (premier carnet). Le déclencheur (Q2) recoupe le premier échange de 30 min ; acceptable.

**Sorties**

| Sortie du carnet 0 | Reprise attendue | Constat |
|---|---|---|
| Heures par semaine (p. 5) | Point d'étape en cours de parcours | Jamais reprise. |
| Objectif principal (p. 5) | Carnet 1 Ex. 3 « objectif boussole » ; fin de livret | Redemandé au carnet 1 sans renvoi ; jamais confronté au résultat. |
| « Je m'autorise à » (p. 5) | Carnet 6 Ex. 4 (pistes « no limit ») | Rupture : jamais repris. |
| Besoins, avantages à garder la situation (p. 6-7) | Carnet 5 Ex. 7, carnet 6 Ex. 2 « Mes besoins » | Implicite seulement. |
| Domaines de vie (p. 8) | Carnet 1 Ex. 2 ; nouvelle notation en fin de bilan | Doublon ; le carnet 1 promet de « mesurer le chemin parcouru » (`chap1/intro.py:13-14`), aucun carnet ne le fait. |
| Entourage (p. 9) | Carnet 6 Ex. 3 « Le retour de vos proches » | Rupture : aucun renvoi. |

**Doublons**
- Q1 « Comment je me sens actuellement ? » et la météo du carnet 1 (« Aujourd'hui, je me sens : », `components.py:543`).
- Domaines de vie et vision à 360° du carnet 1 ; objectif principal et objectif boussole du carnet 1.
- Les deux carnets se présentent comme le « point de départ » (`cloture.py:14` ; « Fixer votre point de départ », `chap1/intro.py:26`).
- Besoins (Q3, Q7) et soutiens (Ex. 4) recoupent l'arbre de vie du carnet 2 (« Sol : vos besoins actuels », « Feuilles : vos soutiens »).

**Ruptures**
- Le carnet 1 est le seul sans « Récapitulatif de la séance précédente » (les carnets 2 à 6 en ont un, via `create_standard_recap_page`) : la séance sur le carnet 0 n'est pas récapitulée.
- Le cadre n'est rappelé dans aucun carnet suivant.

**Recommandation** : carnet 0 = cadre, engagement, situation, entourage, première formulation de l'objectif, notation des domaines. Carnet 1 : ouvrir par un récapitulatif guidé (« Relisez votre objectif du carnet 0, page 5. Qu'est-ce qui a bougé depuis la première séance ? »), faire partir la vision à 360° des trois domaines les moins bien notés, garder une seule question d'humeur. Carnet 6 Ex. 3 : « Choisissez ces personnes parmi les soutiens notés dans le carnet 0, page 9. » Carnet 6 Ex. 4 : « Relisez votre phrase « Je m'autorise à… » du carnet 0. Cette piste figure-t-elle dans vos dix métiers ? » Fin du livret : renoter les huit domaines.

## 5. Écart avec l'app web

- Le web (`server/predefined_workbooks.py:66-92`) a une page « Le cadre de travail : trois règles » (confidentialité, franchise, action) et une échelle d'énergie 0-10 ; le PDF n'a ni l'une ni l'autre, alors qu'il manque justement de cadre.
- Le PDF a « Faire le point » (8 questions), les domaines de vie, l'entourage et la phrase « Moi, … je décide d'investir … heures » ; le web n'en a aucun.
- Le web met un exemple sous chaque question d'objectif (horizon « 3 à 4 mois ») ; le PDF aucun (horizon « fin du bilan »).
- Engagement web figé à « au moins 2 heures par semaine » (chiffre sans source, `predefined_workbooks.py:123`) ; livrables différents (« Votre objectif de bilan » contre « Votre engagement et votre point de départ »).

## 6. Recommandations classées

| Priorité | Type | Page(s) | Constat | Recommandation |
|---|---|---|---|---|
| P1 | correction rapide | 3 | Aucun cadre : confidentialité, droit de passer, question trop lourde, plusieurs fois, mode d'emploi du PDF. | Encadré « Le cadre de travail. » (texte section 2), dans l'espace libre de p. 3 (`intro.py:57-61`). |
| P2 | refonte (composant) | tous carnets | Le cadre n'est rappelé nulle part ensuite, alors que les carnets 1, 2 et 4 sont à forte charge. | Une ligne de rappel dans `create_standard_summary_page` : « Rappel : vos réponses restent confidentielles, chaque question peut rester vierge. » |
| P2 | correction rapide | 6-7, 9 | Exercices 2 et 4 à charge moyenne sans avertissement, optionnalité ni clôture. | Chapeau d'optionnalité et phrases d'ancrage (section 3). |
| P2 | correction rapide | 5-9 | Aucune amorce ni exemple contrasté dans le carnet. | Amorces et un exemple par exercice (section 2), via `QuestionItem(example=…)`. |
| P2 | refonte | 6-7 | Ex. 2 : 30-40 min, doublons Q3/Q7 et Q4/Q5, Q8 prématurée, Q6 non expliquée. | Deux parties de 15-20 min, fusions, Q8 en une ligne, chapeau pour Q6. |
| P2 | correction rapide | 6 | Pas de distinction entre choix personnel et demande extérieure. | Sous-question au déclencheur (Q2). |
| P2 | correction rapide | 2, 5-9 | Aucune durée affichée, total inconnu. | Durées en sourcil (Ex. 1 : 10-15 min ; Ex. 2 : 2 × 15-20 min ; Ex. 3 : 15 min ; Ex. 4 : 10-15 min) et total « environ 1 h 15 » au sommaire. |
| P2 | correction rapide | 5 | Heures sans repère ; pas de chapeau ; objectif abstrait dans une case de 5,3 cm. | Chapeau, repère sourcé, amorce, cases de 2,5-3 cm. |
| P2 | correction rapide | 8 | Trois questions dans une case ; note basse non retournée en critère. | Trois cases avec amorces et ligne « Donc, mon prochain projet devra… ». |
| P2 | refonte | 9 | Listes de noms dans deux grandes cases ; regard négatif sans suite. | Fiche à trois colonnes (`add_fields_card` ou `add_table`) et ligne « Ce que je choisis de lui dire, et quand ». |
| P2 | refonte (composant) | 10 | Case de notes de 12 cm sans consigne ; ni étonnement ni « à aborder ». | Trois zones guidées dans `create_standard_engagement_page` (`components.py:463-468`). |
| P2 | refonte | carnets 1 et 6 | Doublons avec le carnet 1 ; « Je m'autorise à » et l'entourage jamais repris ; pas de récapitulatif au carnet 1. | Répartition et renvois explicites (section 4) ; récapitulatif au carnet 1 ; nouvelle notation des domaines en fin de livret. |
| P3 | correction rapide | 3 | Notion annoncé sans lien cliquable. | `add_link_card` avec l'URL de `chap6/ressources.py:33-34`. |
| P3 | correction rapide | 3 | Frise non rattachée aux carnets. | Numéros de carnets sous chaque étape. |
| P3 | correction rapide | 5 | Horizon de l'objectif incohérent (fin du bilan, 3 mois, 3 à 4 mois). | Un seul horizon dans les trois supports. |
| P3 | correction rapide | 8 | « Temps pour soi, engagements » ambigu ; vie sociale absente ; bornes genrées. | Scinder ou renommer ; bornes « Pas du tout satisfaisant / Pleinement satisfaisant ». |
| P3 | correction rapide | 4 | « La psychologie et la sociologie le montrent » sans source. | « Le bilan part d'un constat : une part de nos choix vient de notre histoire… » |
| P3 | correction rapide | 10 | Le livrable oublie l'entourage. | « Votre engagement, votre situation, vos domaines de vie et votre entourage, relus ensemble en séance. » |
| P3 | refonte | 6-7 | Police automatique : les longues réponses rétrécissent dans les cases de 3,2 cm. | Cases plus courtes et ciblées après les fusions, ou taille de police fixe à arbitrer pour tous les carnets. |
