# Nouveau découpage des séances et des carnets : récapitulatif pour le site

Ce récapitulatif s'adresse à l'agent qui s'occupe du site (dépôt `marge-de-manoeuvre`). Il a été rédigé le 8 octobre 2026 à partir du dépôt `mdm-workbook`, et mis à jour le 9 octobre 2026 (R11) sur les carnets livrés : voir « Mise à jour du 9 octobre » en fin de document. La carte complète du parcours est dans `audit-carnets-2026-10/carte-parcours-unifie.md`.

## À lire d'abord

- **Le nouveau parcours vaut pour les futurs bénéficiaires.** Il n'y a pas de date de bascule : le site peut être mis à jour dès que les changements sont prêts.
- **Ne pas modifier le programme PDF depuis le site.** Il est généré dans `mdm-workbook`, puis copié dans `public/documents/` par `main_generate_programme.py`. Il sera mis à jour de son côté, avec les mêmes décisions. Préviens Nicolas quand la branche du site est prête : le site et le programme PDF partiront ensemble.

## Ce qui change

1. **Plus de carnet 0.** Les carnets sont numérotés de 1 à 7 : « carnet 1 » à « carnet 7 » remplacent « chapitre 0 » à « chapitre 6 ». Le carnet 1 réunit un état des lieux rapide et les héritages.
2. **Le carnet N prépare la séance N.** Le carnet 1 se remplit avant la séance 1, le carnet 2 entre les séances 1 et 2, et ainsi de suite. Le carnet 7 couvre deux intervalles (S6 → S7 et S7 → S8). Le carnet de route couvre le temps 3 (S8 → S9 et S9 → S10).
3. **La séance 1 regroupe l'état des lieux et les héritages.** La séance libérée passe au temps 2. La répartition passe de 6 / 2 / 2 à **5 / 3 / 2** :
   - temps 1 (Comprendre) : 5 séances ;
   - temps 2 (Explorer) : 3 séances ;
   - temps 3 (Décider et agir) : 2 séances.
4. **L'option « Initiation à l'IA » ouvre la séance 6**, puisque l'exploration passe de S7 à S6.
5. **Le document du temps 3 s'appelle « carnet de route »**, comme le site le dit déjà. Le nom « livret de compétences » disparaît : son contenu entre dans le carnet de route.
6. **Le MBTI disparaît du site.** On parle désormais d'un « test des fonctionnements cognitifs », une version maison conçue et éprouvée par Lysiane Brand, psychologue du travail. « MBTI » est une marque soumise à licence : plus aucune mention de l'outil, y compris les codes de type (ISFJ…). Seule exception : la certification MBTI® de Lysiane reste sur sa présentation. Voir la section dédiée plus bas.
7. **Hexa3D est abandonné.** Le site n'en parle pas (vérifié) : ne pas l'ajouter.

## Ce qui ne change pas

- 10 séances de 1 h 20 en visio, un suivi de 40 min à 6 mois, 14 h d'accompagnement : `bilanOffer.ts` ne bouge pas.
- 10 à 20 h de travail personnel sur les carnets (`notebookHours`).
- « 7 carnets de bord guidés », puis « le carnet de route de votre projet ».
- Les trois temps : leurs noms, leurs postures et leurs livrables. Seule la répartition des séances change, et le libellé « Profil MBTI® complet » devient « Profil de fonctionnement cognitif ».
- Le prix, le copilote IA, le suivi.

## Le nouveau déroulé (`src/data/bilanMethod.ts`)

Les champs suivent l'ordre du type `BilanSession` : `label`, `chapter`, `title`, `description`, `objective`. Les textes repris sans changement sont signalés.

### Temps 1 · Comprendre (5 séances)

Proposition pour l'intro du temps 1 : « Comprendre ce qui vous fait avancer : votre point de départ et vos héritages, votre parcours réel, votre fonctionnement, votre rapport à l'argent et vos valeurs. »

Livrables du temps 1 : remplacer « Profil MBTI® complet » par « Profil de fonctionnement cognitif » (dans `bilanMethod.ts` l. 69 et `BilanHero.astro` l. 58). Les deux autres livrables ne changent pas.

**S1**
- label : « État des lieux et héritages »
- chapter : « Carnet 1 »
- title : « Faire le point sur votre situation et ce qui vous a construit »
- description : « On commence par revenir à l'essentiel : votre état actuel, votre énergie, ce qui vous pèse, ce qui tient encore. On regarde aussi ce que vous avez reçu de votre milieu sur le travail : les modèles, les messages, les attentes qui orientent encore vos choix, parfois sans que vous en ayez conscience. On pose enfin le cadre de travail : vos attentes, la confidentialité, la façon dont nous avancerons ensemble. »
- objective : « clarifier votre point de départ et repérer les influences qui orientent encore vos choix. »

**S2** (texte de l'actuelle S3)
- label : « Mon parcours réel »
- chapter : « Carnet 2 »
- title, description et objective : inchangés.

**S3** (actuelle S4, description modifiée)
- label : « Mes fonctionnements cognitifs »
- chapter : « Carnet 3 »
- title : inchangé.
- description : « On travaille votre fonctionnement en profondeur, avec un test des fonctionnements cognitifs conçu et éprouvé par Lysiane Brand, psychologue du travail. Vous comprenez comment vous prenez des décisions, ce qui vous stimule, ce qui vous fatigue, votre manière d'interagir. On le met en regard de votre vécu : les environnements qui vous conviennent, ceux qui vous épuisent. »
- objective : inchangé.

**S4** (texte de l'actuelle S5)
- label : « Mon rapport à l'argent »
- chapter : « Carnet 4 »
- title, description et objective : inchangés.

**S5** (texte de l'actuelle S6)
- label : « Valeurs et moteurs »
- chapter : « Carnet 5 »
- title, description et objective : inchangés.

### Temps 2 · Explorer (3 séances)

L'option « Initiation à l'IA » (`isOption`) se place juste avant S6. Son texte dit « la séance 6 » au lieu de « la séance 7 ».

**S6**
- label : « L'exploration »
- chapter : « Carnet 6 »
- title : « Explorer des métiers et des secteurs »
- description : « On ouvre le champ des possibles de manière structurée : 10 pistes qualifiées, 5 réalistes et 5 audacieuses, cohérentes avec votre profil, vos compétences et vos aspirations. Vous choisissez les trois pistes que vous allez confronter au terrain. »
- objective : « faire émerger des pistes alignées avec votre profil. »

**S7**
- label : « Enquêtes terrain »
- chapter : « Carnet 7 »
- title : « Explorer vos pistes sur le terrain »
- description : « On passe à une phase concrète. Vos trois pistes passent au crible de vos critères : valeurs, seuils financiers, énergie. Vous préparez vos enquêtes auprès de professionnels en poste (grille d'entretien, message d'approche, premiers contacts) et vous vérifiez salaires et débouchés dans votre bassin d'emploi. »
- objective : « préparer une exploration du terrain qui vous apprend vraiment quelque chose. »

**S8**
- label : « Crash-test et scénarios »
- chapter : « Carnet 7 »
- title : « Tirer les leçons du terrain »
- description : « On analyse ce que vos enquêtes confirment ou contredisent. La matrice de faisabilité croise vos compétences, le marché et les débouchés. Vos pistes sont classées en trois familles de scénarios : pistes directes, passerelles courtes, angles morts. »
- objective : « vérifier vos idées sur le terrain et affiner vos projections. »

### Temps 3 · Décider et agir (2 séances)

**S9**
- label : « Arbitrage et carnet de route »
- chapter : « Carnet de route »
- title, description et objective : inchangés.

**S10**
- label : « Synthèse et premières actions »
- chapter : « Carnet de route »
- title, description et objective : inchangés.

**Suivi** : inchangé.

## Les sept carnets (`src/data/bilanNotebooks.ts`)

Le champ `chapter` passe de 0 à 6 à **1 à 7**. Les textes ci-dessous décrivent le contenu réel des carnets du nouveau parcours, dans le ton des carnets : vouvoiement, phrases courtes, pas de vocabulaire de développement personnel. Le sous-titre peut être adapté au ton du site. Les exercices et les livrables doivent rester fidèles au contenu.

**Carnet 1 · L'état des lieux**
- Sous-titre : « Le point de départ et les héritages »
- Objectif : « Poser le cadre de travail, faire le point sur votre situation et repérer ce que vous avez reçu de votre milieu sur le travail. »
- Exercices :
  - « Cadre de travail et engagement »
  - « Ce qui pèse, ce qui tient encore »
  - « Roue des 8 domaines de vie »
  - « Héritages : ce que vous avez reçu, ce que vous en faites »
- Livrable : « Votre point de départ » — « Votre situation, vos domaines de vie, vos héritages et votre objectif de bilan, validés en séance 1. »

**Carnet 2 · Mon parcours**
- Sous-titre : « Du travail prescrit au travail réel »
- Objectif : « Révéler ce que vos expériences vous ont appris, au-delà d'un CV : ce que vous savez faire, ce qui vous donne de l'énergie, ce qui vous coûte. »
- Exercices :
  - « Vos expériences, entre énergie et coût »
  - « Le travail réel et le travail empêché »
  - « Les quatre zones de compétences »
  - « Ligne de vie (hauts et bas) »
- Livrable : « Votre fil rouge » — « Votre fil rouge, vos moteurs et vos compétences, validés en séance 2. »

**Carnet 3 · Mes fonctionnements propres**
- Sous-titre : « Votre façon de fonctionner »
- Objectif : « Préparer la restitution de votre test des fonctionnements cognitifs : où vous puisez votre énergie, comment vous décidez, comment vous réagissez sous pression. »
- Exercices :
  - « Test des fonctionnements cognitifs »
  - « 17 mises en situation »
  - « Sous pression : vos réactions »
  - « Ce que j'en retiens pour mon travail »
- Livrable : « Cartographie de vos énergies de travail » — « Ce qui vous recharge, ce qui vous use, et vos facteurs d'usure. »

**Carnet 4 · Mon rapport à l'argent**
- Garder ce titre tel quel : `comparisons/chance.ts` cherche ce carnet par son titre.
- Sous-titre : « Les chiffres de votre sécurité »
- Objectif : « Poser sans détour les chiffres de votre sécurité financière pour bâtir une trajectoire viable. » (inchangé)
- Exercices :
  - « Votre histoire avec l'argent »
  - « Idées reçues, à l'épreuve des faits »
  - « Les 4 seuils financiers »
  - « Vos tendances face à l'argent »
- Livrable : « Seuil de sécurité financière » — « Minimum vital, minimum sécurisant, revenu cible et durée acceptable d'une baisse, pour arbitrer vos pistes. »

**Carnet 5 · Valeurs et moteurs profonds**
- Sous-titre : « Le socle non négociable »
- Objectif : « Identifier vos 3 valeurs non négociables et les traduire en critères observables sur le terrain. »
- Exercices :
  - « Expériences d'alignement et de désalignement »
  - « Entonnoir des valeurs (10 → 5 → 3) »
  - « Tensions de valeurs »
  - « Grille anti-compromis »
- Livrable : « Grille anti-compromis » — « Pour chaque valeur : la condition observable, le signal d'alerte et la question à poser en entretien. »

**Carnet 6 · L'exploration**
- Sous-titre : « Ouvrir les possibles »
- Objectif : « Générer 10 pistes qualifiées (5 réalistes, 5 audacieuses) à partir de tout ce que vous avez appris sur vous. »
- Exercices :
  - « Cartographie personnelle de synthèse »
  - « Le regard de 3 proches »
  - « Ressources pour vos recherches »
  - « Les 10 pistes »
- Livrable : « 10 pistes qualifiées » — « Dont 3 retenues en séance 6 pour être explorées sur le terrain. »

**Carnet 7 · Explorer le terrain** (nouveau, en deux parties)
- Sous-titre : « Sonder le réel »
- Objectif : « Passer vos 3 pistes au crible de vos critères et les vérifier auprès de professionnels en poste. »
- Exercices :
  - « Fiches à critères de vos 3 pistes »
  - « Grille d'entretien et message d'approche »
  - « Comptes rendus d'enquêtes »
  - « Matrice de faisabilité »
- Livrable : « Retours d'enquêtes et matrice de faisabilité » — « Ce que le terrain confirme ou contredit, et vos 3 scénarios comparés en séance 8. »

**Le carnet de route** (temps 3, après le carnet 7)
- Une partie commune : compétences prouvées, deux récits d'action, piste A et piste B, feuilles de route à 30, 60 et 90 jours, premières actions sous 7 jours, garde-fous et soutiens, chemin parcouru.
- Un module selon le projet. Seul le module création (le business plan court, 2 h, entre les séances 9 et 10) existe. La reconversion (formation et financement) et l'évolution interne (argumentaire de repositionnement) se travaillent en séance 9, en attendant leurs modules : ne pas présenter ces deux modules comme des documents remis.
- Le site présente déjà « le carnet de route de votre projet » (section « Trois projets possibles ») : ce cadre reste juste.

## Le MBTI : supprimer toute mention

**La règle** : « MBTI » est une marque soumise à licence. Le bilan utilise un **test des fonctionnements cognitifs**, une version maison conçue et éprouvée par Lysiane Brand, psychologue du travail. Le site ne doit plus mentionner le MBTI nulle part : ni « MBTI® », ni « test MBTI », ni codes de type (ISFJ, ESFJ, ISTP…).

**Une exception** : la certification de Lysiane (« Certifiée MBTI® ») reste dans ses titres et qualifications (`BilanDuo.astro` l. 33, `l-equipe.astro` l. 24 et 29). Elle décrit sa qualification, pas l'outil du bilan. La garder à l'écart de la description du test, pour ne pas laisser croire que celui-ci dérive du MBTI.

Mentions visibles (relevé du 8 octobre 2026, hors tests) :

| Fichier | Texte actuel | Proposition |
|---|---|---|
| `src/data/bilanMethod.ts` (l. 69) | « Profil MBTI® complet » | « Profil de fonctionnement cognitif » |
| `src/data/bilanMethod.ts` (l. 99 et 103) | label « Mes fonctionnements (MBTI®) » ; « Avec le questionnaire officiel MBTI®, vous comprenez… » | La nouvelle S3 (section « Le nouveau déroulé ») |
| `src/components/bilan/BilanHero.astro` (l. 58) | « Profil MBTI® complet » | « Profil de fonctionnement cognitif » |
| `src/data/bilanNotebooks.ts` (l. 88, 89, 91, 98) | « L'écologie d'énergie (MBTI®) », « Passation et restitution du MBTI® officiel… », « Passation officielle du MBTI® (93 questions) », « Rapport officiel complet MBTI®… » | Le nouveau carnet 3 (section « Les sept carnets ») |
| `src/data/bilanKit.ts` (l. 30-31) | « Questionnaire officiel MBTI® » — « et son rapport complet » | « Test des fonctionnements cognitifs » — « et sa restitution ». L'identifiant interne `mbti` peut devenir `fonctionnements`. |
| `src/components/bilan/BilanStance.astro` (l. 19) | « Le MBTI® éclaire votre façon de fonctionner, il ne tranche pas. » | « Le test des fonctionnements cognitifs éclaire votre façon de fonctionner, il ne tranche pas. » |
| `src/components/bilan/BilanDuo.astro` (l. 33 et 37) | « Certifiée MBTI® » ; « la passation officielle du MBTI® » | Garder « Certifiée MBTI® » ; « le test des fonctionnements cognitifs et sa restitution » |
| `src/pages/l-equipe.astro` (l. 24, 25, 29) | « Certifiée MBTI® » (deux fois) ; « la lecture de votre fonctionnement (MBTI®) » | Garder « Certifiée MBTI® » ; « la lecture de votre fonctionnement » |
| `src/pages/l-equipe.astro` (l. 35) | « j'assure la passation et l'interprétation du questionnaire officiel MBTI® » | « j'ai conçu le test des fonctionnements cognitifs du bilan, et j'en assure la passation et la restitution » |
| `src/pages/l-equipe.astro` (l. 38-39) | commentaire ; lien « Découvrir le test MBTI® officiel avec Lysiane » | « Découvrir le test des fonctionnements cognitifs » |
| `src/data/team.ts` (l. 41) | `knowsAbout` : « MBTI » | Retirer |
| `src/components/villes/CityFinancing.astro` (l. 61) | « le questionnaire MBTI® » | « le test des fonctionnements cognitifs » |
| `src/data/villeFaqs.ts` (l. 29) | « le même questionnaire MBTI® officiel » | « le même test des fonctionnements cognitifs » |
| `src/content/faq/questions.json` (l. 144, 206 et 218) | « le questionnaire MBTI® officiel est inclus, restitution comprise » ; « inventaire certifié MBTI® » | « un test des fonctionnements cognitifs est inclus, restitution comprise » ; « test des fonctionnements cognitifs » |
| `src/components/sections/Trajectory.astro` (l. 55) | « Des repères solides sur votre personnalité et vos valeurs (MBTI) » | « Des repères solides sur votre fonctionnement et vos valeurs » |
| `src/data/bilanResults.ts` (l. 73) | indicateur « Pertinence des outils utilisés (questionnaire MBTI®, exercices) » | « Pertinence des outils utilisés ». Le score vient d'enquêtes passées : retirer la parenthèse plutôt que de renommer l'outil. |
| `src/data/comparisons/chance.ts` (l. 586, et le commentaire l. 11) | « le questionnaire MBTI® sert de support de dialogue, jamais de verdict » | « le test des fonctionnements cognitifs sert de support de dialogue, jamais de verdict » |
| `src/content/articles/le-cout-du-masque-social/index.md` (l. 23) | « (comme les types MBTI ISFJ et ESFJ) » | Retirer la parenthèse |
| `src/content/articles/introversion-bulle-professionnelle/index.md` (l. 12) | « (très fréquent chez les profils MBTI ISFJ ou ISTP) » | Retirer la parenthèse |
| `src/data/legacyRedirects.ts` (l. 58-59) | redirection de `/outil-de-personnalite-mbti/` | Garder la redirection (c'est une ancienne adresse), reformuler le commentaire et le champ `topic` |
| Commentaires (`ComparisonGuides.astro` l. 4, `Approach.astro` l. 44, `bilanKit.ts` l. 30, `l-equipe.astro` l. 38) | mentions du MBTI | À reformuler |
| Tests | `bilanNotebooks.test.ts`, `bilanKit.test.ts`, `bilanMethod.test.ts`, `bilanResults.test.ts`, `BilanDuo.test.ts`, `BilanHero.test.ts`, `BilanPricing.test.ts`, `BilanMethod.test.ts`, `BilanResults.test.ts`, `BilanBetweenSessions.test.ts`, `ComparisonGuides.test.ts`, `FAQ.test.ts`, `Expertise.test.ts`, `chance.test.ts` | À aligner sur les nouveaux textes |

## Les autres endroits à modifier

Relevé fait en lecture seule le 8 octobre 2026, au commit `89967a1`.

| Fichier | Ce qui est concerné |
|---|---|
| `src/data/bilanMethod.ts` | Les séances (section « Le nouveau déroulé »). Le commentaire d'en-tête, « chapitres 0 à 5 ». La position de l'option IA. |
| `src/data/bilanMethod.test.ts` | Les tests de répartition et de numérotation. |
| `src/data/bilanNotebooks.ts` et `bilanNotebooks.test.ts` | Les 7 carnets, avec `chapter` de 1 à 7. Le commentaire d'en-tête, « chapitres 0 à 6 ». Les libellés figés dans le test. |
| `src/data/bilanBetweenSessions.ts` (l. 28) | « Du chapitre 0 au chapitre 6 » devient « Du carnet 1 au carnet 7 ». |
| `src/components/bilan/BilanBetweenSessions.astro` | Vérifier l'affichage du numéro de carnet : pagination « 1 / 7 », onglets « Chapitres des carnets de bord ». |
| `src/components/bilan/BilanMethod.astro` (l. 31) | Les sourcils « Séance 7 · Chapitre 6 » et « ouverture de la séance 7 » deviennent « Séance 6 · Carnet 6 » et « ouverture de la séance 6 ». |
| `src/utils/llmsTxt.ts` (l. 108) et son test | « option de la séance 7 ». |
| `src/content/articles/bilan-de-competences-a-distance/index.md` (l. 39 et 67) | « du chapitre 0 au chapitre 6 » ; « la septième séance peut s'ouvrir par une initiation à l'IA » devient « la sixième séance ». |
| `src/content/faq/questions.json` (l. 138 et 154) | « livret individuel » et « livret de bord » deviennent « carnets de bord ». |
| `src/data/comparisons/chance.ts` | Rien à changer si le titre « Mon rapport à l'argent » est gardé. |

Pour être exhaustif, chercher aussi dans `src/` : « chapitre 0 », « Chapitre », « prélude », « séance 7 », « septième séance », « livret de compétences », « MBTI », « ISFJ », « officiel », « Hexa3D », et le champ `chapter:`.

## Mise à jour du 9 octobre 2026 (R11)

Les carnets sont livrés. Le site a déjà repris ce récapitulatif ; trois points ont changé depuis, à reporter dans `src/data/bilanNotebooks.ts` et son test :

| Où | Aujourd'hui sur le site | Dans les carnets |
|---|---|---|
| Carnet 5, `title` | « Valeurs & moteurs profonds » | « Valeurs et moteurs profonds » |
| Carnet 6, `title` | « Phase d'exploration » | « L'exploration » |
| Carnet de route | (le site ne détaille pas sa partie commune) | « garde-fous et soutiens », plus « alliés » |

Les modules reconversion et évolution interne n'existent pas encore : seul le module création est remis (voir « Le carnet de route » plus haut). Les phrases du site sur « le carnet de route de votre projet » restent justes, puisque la séance 9 et la personnalisation adaptent le carnet de route au projet.

Le programme PDF a été aligné en même temps (PR #69 de `mdm-workbook`). Le site reprend ses textes mot pour mot ; à reporter avec le nouveau PDF :

| Où | Aujourd'hui sur le site | Nouveau texte |
|---|---|---|
| `src/data/bilanMethod.ts`, description de S4 | « vos 4 seuils financiers, le revenu vital et le revenu sécurisant, le délai de trésorerie que vous pouvez tenir. » | « On pose les chiffres de votre sécurité financière : vos 4 seuils, le minimum vital, le minimum sécurisant, le revenu cible et la durée pendant laquelle vous pouvez accepter une baisse. Une transition viable se calcule, sans précariser l'équilibre de votre foyer. » |
| Travail personnel (`bilanBetweenSessions.ts`, et partout où le site donne les 10 à 20 h) | « 10 à 20 h … selon les personnes » | Ajouter : « Un projet de création ajoute un module d'environ 2 h entre les séances 9 et 10. » |
| `src/data/bilanProjects.ts`, trajectoire « Création » | « une offre pilote, testable sous 15 jours » ; « statut, ACRE ou ARCE, premiers clients » | Inchangé : le module création tient désormais ces promesses (test sur 15 jours au plus, ARCE et ACRE nommées). |

Les quatre exercices de chaque carnet restent fidèles aux carnets livrés (le site en impose exactement quatre) : au carnet 1, l'objectif de départ figure dans le livrable, et « ce que vous en faites » couvre les modèles et anti-modèles.

## Mise à jour du 9 octobre 2026 (charte v2)

Après les retours de Nicolas sur le carnet 1, le temps 2 du bilan s'appelle « Explorer » partout : le programme, les carnets et le site. Le programme PDF a changé sa page du temps 2 (PR « charte v2 » de `mdm-workbook`) ; à reporter avec le nouveau PDF :

| Où | Aujourd'hui sur le site | Nouveau texte |
|---|---|---|
| `src/data/bilanMethod.ts`, temps 2 | « Confronter » ; « Confronter l'idée au terrain. » ; « Confronter vos pistes au marché : ouvrir les possibles, puis vérifier métiers, salaires et débouchés… » | « Explorer » ; « Explorer le terrain. » ; « Explorer vos pistes : ouvrir les possibles, puis vérifier métiers, salaires et débouchés… » |
| `src/data/bilanMethod.ts`, S6 | « … les trois pistes que vous allez confronter au terrain. » | « … les trois pistes que vous allez explorer sur le terrain. » |
| `src/data/bilanMethod.ts`, S7 | « Confronter vos pistes au terrain » ; objectif « préparer une confrontation au réel… » | « Explorer vos pistes sur le terrain » ; « préparer une exploration du terrain qui vous apprend vraiment quelque chose. » |
| `src/data/bilanMethod.ts`, S8 | objectif « confronter vos idées à la réalité et affiner vos projections. » | « vérifier vos idées sur le terrain et affiner vos projections. » |
| Livrables du temps 2 | « À l'issue du temps 2 (confronter) » | « À l'issue du temps 2 (explorer) » |
| `src/data/bilanNotebooks.ts`, carnet 7 | « Confronter au terrain » ; « Trois pistes, confrontées au réel. » | « Explorer le terrain » ; « Trois pistes, vérifiées sur le terrain. » |

Le ton change aussi (DA, section 7) : plus d'énergie et de pouvoir d'agir, aucune formule de précaution (« à votre rythme », « cela peut remuer »), et tout se fait à l'écran (le carnet se renvoie complété avant la séance, jamais « apportez », « imprimez »). Le site peut chercher ces formules dans ses textes.

Trois passages du programme gardent le mot « confrontation », parce qu'ils décrivent la méthode ou les phases légales et non le nom du temps 2, en attendant la décision de Nicolas : les phases du Code du travail (« confronter les scénarios aux réalités du marché de l'emploi »), les enquêtes métiers (« confrontation au réel ») et le positionnement (« la confrontation au terrain »).
