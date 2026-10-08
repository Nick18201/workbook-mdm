# Nouveau découpage des séances et des carnets : récapitulatif pour le site

Ce récapitulatif s'adresse à l'agent qui s'occupe du site (dépôt `marge-de-manoeuvre`). Il a été rédigé le 8 octobre 2026 à partir du dépôt `mdm-workbook`. La carte complète du parcours est dans `audit-carnets-2026-10/carte-parcours-unifie.md`.

## À lire d'abord

- **Le nouveau parcours vaut pour les futurs bénéficiaires.** Il n'y a pas de date de bascule : le site peut être mis à jour dès que les changements sont prêts.
- **Ne pas modifier le programme PDF depuis le site.** Il est généré dans `mdm-workbook`, puis copié dans `public/documents/` par `main_generate_programme.py`. Il sera mis à jour de son côté, avec les mêmes décisions. Préviens Nicolas quand la branche du site est prête : le site et le programme PDF partiront ensemble.

## Ce qui change

1. **Plus de carnet 0.** Les carnets sont numérotés de 1 à 7 : « carnet 1 » à « carnet 7 » remplacent « chapitre 0 » à « chapitre 6 ». Le carnet 1 réunit un état des lieux rapide et les héritages.
2. **Le carnet N prépare la séance N.** Le carnet 1 se remplit avant la séance 1, le carnet 2 entre les séances 1 et 2, et ainsi de suite. Le carnet 7 couvre deux intervalles (S6 → S7 et S7 → S8). Le carnet de route couvre le temps 3 (S8 → S9 et S9 → S10).
3. **La séance 1 regroupe l'état des lieux et les héritages.** La séance libérée passe au temps 2. La répartition passe de 6 / 2 / 2 à **5 / 3 / 2** :
   - temps 1 (Comprendre) : 5 séances ;
   - temps 2 (Confronter) : 3 séances ;
   - temps 3 (Décider et agir) : 2 séances.
4. **L'option « Initiation à l'IA » ouvre la séance 6**, puisque l'exploration passe de S7 à S6.
5. **Le document du temps 3 s'appelle « carnet de route »**, comme le site le dit déjà. Le nom « livret de compétences » disparaît : son contenu entre dans le carnet de route.
6. **Le questionnaire de préférences n'est pas le questionnaire officiel MBTI®.** C'est une version maison, conçue et éprouvée par Lysiane Brand, qui est praticienne certifiée MBTI®. Le site ne doit plus parler nulle part de « questionnaire officiel », de « passation officielle », de « test MBTI® officiel » ni de « rapport officiel complet ». Voir la section dédiée plus bas.
7. **Hexa3D est abandonné.** Le site n'en parle pas (vérifié) : ne pas l'ajouter.

## Ce qui ne change pas

- 10 séances de 1 h 20 en visio, un suivi de 40 min à 6 mois, 14 h d'accompagnement : `bilanOffer.ts` ne bouge pas.
- 10 à 20 h de travail personnel sur les carnets (`notebookHours`).
- « 7 carnets de bord guidés », puis « le carnet de route de votre projet ».
- Les trois temps : leurs noms, leurs postures et leurs livrables. Seule la répartition des séances change, et le libellé « Profil MBTI® complet » (voir plus bas).
- Le prix, le copilote IA, le suivi.

## Le nouveau déroulé (`src/data/bilanMethod.ts`)

Les champs suivent l'ordre du type `BilanSession` : `label`, `chapter`, `title`, `description`, `objective`. Les textes repris sans changement sont signalés.

### Temps 1 · Comprendre (5 séances)

Proposition pour l'intro du temps 1 : « Comprendre ce qui vous fait avancer : votre point de départ et vos héritages, votre parcours réel, votre fonctionnement, votre rapport à l'argent et vos valeurs. »

Livrables du temps 1 : remplacer « Profil MBTI® complet » par « Votre profil de préférences ». Les deux autres livrables ne changent pas.

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
- label : « Mes fonctionnements (MBTI®) »
- chapter : « Carnet 3 »
- title : inchangé.
- description : « On travaille votre fonctionnement en profondeur, avec un questionnaire de préférences conçu et éprouvé par Lysiane Brand, praticienne certifiée MBTI®. Vous comprenez comment vous prenez des décisions, ce qui vous stimule, ce qui vous fatigue, votre manière d'interagir. On le met en regard de votre vécu : les environnements qui vous conviennent, ceux qui vous épuisent. »
- objective : inchangé.

**S4** (texte de l'actuelle S5)
- label : « Mon rapport à l'argent »
- chapter : « Carnet 4 »
- title, description et objective : inchangés.

**S5** (texte de l'actuelle S6)
- label : « Valeurs et moteurs »
- chapter : « Carnet 5 »
- title, description et objective : inchangés.

### Temps 2 · Confronter (3 séances)

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
- title : « Confronter vos pistes au terrain »
- description : « On passe à une phase concrète. Vos trois pistes passent au crible de vos critères : valeurs, seuils financiers, énergie. Vous préparez vos enquêtes auprès de professionnels en poste (grille d'entretien, message d'approche, premiers contacts) et vous vérifiez salaires et débouchés dans votre bassin d'emploi. »
- objective : « préparer une confrontation au réel qui vous apprend vraiment quelque chose. »

**S8**
- label : « Crash-test et scénarios »
- chapter : « Carnet 7 »
- title : « Tirer les leçons du terrain »
- description : « On analyse ce que vos enquêtes confirment ou contredisent. La matrice de faisabilité croise vos compétences, le marché et les débouchés. Vos pistes sont classées en trois familles de scénarios : pistes directes, passerelles courtes, angles morts. »
- objective : « confronter vos idées à la réalité et affiner vos projections. »

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
- Objectif : « Préparer la restitution de votre profil de préférences : où vous puisez votre énergie, comment vous décidez, comment vous réagissez sous pression. »
- Exercices :
  - « Questionnaire de préférences, conçu par une praticienne certifiée MBTI® »
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

**Carnet 5 · Valeurs & moteurs profonds**
- Sous-titre : « Le socle non négociable »
- Objectif : « Identifier vos 3 valeurs non négociables et les traduire en critères observables sur le terrain. »
- Exercices :
  - « Expériences d'alignement et de désalignement »
  - « Entonnoir des valeurs (10 → 5 → 3) »
  - « Tensions de valeurs »
  - « Grille anti-compromis »
- Livrable : « Grille anti-compromis » — « Pour chaque valeur : la condition observable, le signal d'alerte et la question à poser en entretien. »

**Carnet 6 · Phase d'exploration**
- Sous-titre : « Ouvrir les possibles »
- Objectif : « Générer 10 pistes qualifiées (5 réalistes, 5 audacieuses) à partir de tout ce que vous avez appris sur vous. »
- Exercices :
  - « Cartographie personnelle de synthèse »
  - « Le regard de 3 proches »
  - « Ressources pour vos recherches »
  - « Les 10 pistes »
- Livrable : « 10 pistes qualifiées » — « Dont 3 retenues en séance 6 pour être confrontées au terrain. »

**Carnet 7 · Confronter au terrain** (nouveau, en deux parties)
- Sous-titre : « Sonder le réel »
- Objectif : « Passer vos 3 pistes au crible de vos critères et les confronter à des professionnels en poste. »
- Exercices :
  - « Fiches à critères de vos 3 pistes »
  - « Grille d'entretien et message d'approche »
  - « Comptes rendus d'enquêtes »
  - « Matrice de faisabilité »
- Livrable : « Retours d'enquêtes et matrice de faisabilité » — « Ce que le terrain confirme ou contredit, et vos 3 scénarios comparés en séance 8. »

**Le carnet de route** (temps 3, après le carnet 7)
- Une partie commune : compétences prouvées, deux récits d'action, piste A et piste B, feuilles de route à 30, 60 et 90 jours, premières actions sous 7 jours, garde-fous et alliés.
- Un module selon le projet : création (business plan), reconversion (formation et financement), évolution interne (argumentaire de repositionnement).
- Le site présente déjà « le carnet de route de votre projet » (section « Trois projets possibles ») : ce cadre reste juste.

## Le MBTI® : retirer « officiel » partout

**La règle** : le questionnaire est une version maison. On peut dire qu'il a été conçu et éprouvé par Lysiane Brand, praticienne certifiée MBTI®, et que le profil est restitué par elle. On ne peut pas dire « officiel ».

| Fichier | Texte actuel | Proposition |
|---|---|---|
| `src/data/bilanMethod.ts` (l. 103) | « Avec le questionnaire officiel MBTI®, vous comprenez… » | La nouvelle description de S3 (section précédente). |
| `src/data/bilanMethod.ts` (livrables du temps 1) | « Profil MBTI® complet » | « Votre profil de préférences » |
| `src/data/bilanNotebooks.ts` (l. 89, 91, 98) | « Passation et restitution du MBTI® officiel… », « Passation officielle du MBTI® (93 questions) », « Rapport officiel complet MBTI®… » | Le nouveau carnet 3 (section précédente). Ne pas reprendre le nombre de questions sans confirmation. |
| `src/data/bilanKit.ts` (l. 30-31) | « Questionnaire officiel MBTI® » — « et son rapport complet » | « Questionnaire de préférences » — « conçu et restitué par une praticienne certifiée MBTI® » |
| `src/components/bilan/BilanDuo.astro` (l. 37) | « la passation officielle du MBTI® » | « le questionnaire de préférences et sa restitution » |
| `src/pages/l-equipe.astro` (l. 35) | « j'assure la passation et l'interprétation du questionnaire officiel MBTI® » | « j'ai conçu le questionnaire de préférences du bilan, et j'en assure la passation et la restitution, en tant que praticienne certifiée MBTI® » |
| `src/pages/l-equipe.astro` (l. 39) | lien « Découvrir le test MBTI® officiel avec Lysiane » | « Découvrir le questionnaire de préférences » |
| `src/content/faq/questions.json` (l. 144, et l. 206 si concernée) | « le questionnaire MBTI® officiel est inclus, restitution comprise » | « un questionnaire de préférences, conçu par une praticienne certifiée MBTI®, est inclus, restitution comprise » |
| `src/data/villeFaqs.ts` (l. 29) | « le même questionnaire MBTI® officiel » | « le même questionnaire de préférences » |
| Tests | `bilanNotebooks.test.ts` (l. 143, 145, 152), `bilanKit.test.ts` (l. 43), `BilanDuo.test.ts` (l. 86), `Expertise.test.ts` (l. 159) | À aligner sur les nouveaux textes. |

**Point de vigilance, à vérifier avec Lysiane** : « MBTI® » est une marque déposée qui désigne l'instrument officiel. Pour une version maison, la mention la plus prudente décrit la certification de la personne (« praticienne certifiée MBTI® ») plutôt que le questionnaire. Les conditions de sa certification disent précisément ce qui est permis.

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

Pour être exhaustif, chercher aussi dans `src/` : « chapitre 0 », « Chapitre », « prélude », « séance 7 », « septième séance », « livret de compétences », « officiel », « Hexa3D », et le champ `chapter:`.
