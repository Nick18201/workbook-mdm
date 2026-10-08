# Audit du carnet 3 · « Mes fonctionnements propres »

## 1. Synthèse

- **Verdict** : un bon socle (17 mises en situation concrètes, vie personnelle et professionnelle, une dimension MBTI® par exercice, des exercices de 15 à 30 min), mais un questionnaire uniforme : aucune amorce, aucun exemple, aucune durée, aucun format court.
- **1.** L'exercice 6 (stress extrême, rumination à 3 h du matin) et la Q11 (critique blessante) n'ont aucun protocole de sécurité. Le carnet ne dit ni qui lira les réponses, ni qu'on peut passer une question.
- **2.** Le MBTI® n'est jamais expliqué : rien ne dit que ces questions ne donnent pas le type, que la personne le valide elle-même, ni qui fait la restitution. La Q16 fait s'étiqueter avec des adjectifs péjoratifs.
- **3.** La matière ne revient pas vers le projet : aucun irritant n'est retourné en critère, pas de zone « surpris / à aborder », rien pour noter le type validé que chap4, chap6 et le livret réclament.
- Aussi : plusieurs consignes orientent la réponse (Q4, Q8, Q13) ou contredisent l'engagement « situations vécues » (Q1, Q7). L'app web livre un tout autre carnet 3.

## 2. Exercice par exercice

### Ouverture : couverture, sommaire, « Avant de commencer » (p. 1, 2, 4) · 5 min

- **F** : la promesse (`intro.py:13`) et le sommaire (`intro.py:18-22`) donnent le but. Mais le MBTI® n'est défini nulle part (p. 2, 4, 13) : la personne ignore si elle passera un questionnaire officiel, qui le restitue, et que ces 17 questions ne calculent pas son type. « Cinq dimensions » (`intro.py:58`), pour un outil à quatre préférences, prépare une confusion à la restitution. « Ce qui se passe dans votre tête et dans votre corps (votre énergie) » (`intro.py:53-54`) mélange l'énergie (dimension 1) et le fonctionnement en général.
- **A** : « racontez le « pourquoi » et le « comment » » (`intro.py:55-56`) est une bonne consigne, mais aucun exemple de réponse terminée dans tout le carnet.
- **B** : l'opposition compétence / énergie est posée, jamais croisée ensuite.
- **H** : ni confidentialité, ni droit de passer, ni « ce qui est trop lourd se note pour la séance ». Seules traces : « le tri se fait en séance » (chap0 p. 3) et « Ce carnet reste le vôtre » (dos, p. 14).
- **D** : aucune durée ni « en plusieurs fois », alors que le DA prévoit « EXERCICE 2 · 20 MIN » (`DA-workbook.md:228`). Total estimé : 1 h 40 à 2 h 30.
- **Recommandations (p. 4)** :
  - Encadré « À savoir sur le MBTI® » : « Le MBTI® décrit des préférences : votre façon naturelle de puiser votre énergie, de recueillir l'information, de décider et de vous organiser. Il ne mesure ni vos compétences ni votre valeur. Aucun profil n'est meilleur qu'un autre. Ces questions ne calculent pas votre type : elles nourrissent l'échange. Votre profil vous est restitué en séance par un praticien certifié, et c'est vous qui validez le type qui vous ressemble le plus. » (à compléter avec le déroulé réel du questionnaire officiel).
  - Titre : « Quatre préférences, et vos réactions sous pression. »
  - Remonter ici l'engagement de fin (`cloture.py:10`) en consigne : « Partez de situations vécues. Répondez comme vous êtes quand personne n'attend rien de vous, pas comme votre poste vous demande d'être. »
  - Cadre : « Ce carnet vous appartient. Vous pouvez passer une question : notez son numéro, nous en parlerons en séance. Comptez environ deux heures, en trois ou quatre fois. »
  - Un exemple contrasté, sur un sujet absent du carnet pour ne pas ancrer une préférence : « Exemple · Comment choisissez-vous un restaurant ? Réponse de surface : « Ça dépend. » Réponse exploitable : « Je lis les avis et je réserve la veille. Le soir où des amis ont choisi au hasard, j'ai passé le repas à penser à l'autre adresse. » »

### Exercice 1 · Récapitulatif (p. 3) · 10-15 min

- **E** : bonne reprise explicite de la ligne de vie et de l'arbre de vie (`intro.py:42`). Q1 et Q3 (`intro.py:41`, `43`) sont mot pour mot celles du récapitulatif de chap2 ; le livrable de chap2 (fil rouge, moteurs) n'est pas repris.
- **F/D** : la longueur attendue n'est pas dite ; trois cases de 124 pt (4,4 cm), adaptées.
- **Recommandation** : Q3 devient « Parmi les moteurs notés au carnet 2, lequel se voit le plus dans votre façon de travailler ? » ; ajouter « Deux ou trois lignes par question suffisent. »

### Exercice 2 · Énergie (p. 5, Q1-3) · 15-20 min

- **A** : scénarios concrets, bons déclencheurs ; aucune amorce.
- **F** : l'intro « comment vous traitez l'information immédiate » (`exercices.py:89`) se confond avec l'exercice 3 « L'information ».
- **B** : « Racontez une fois où vous avez dû faire l'inverse » (Q3, `exercices.py:16-17`) est la meilleure question du carnet : elle touche le coût d'un mode non préféré. Il manque « et ce que cela vous a coûté ».
- **E/F** : Q1 demande la soirée « idéale » (`exercices.py:8-9`), contre l'engagement « situations vécues, pas ce que j'aimerais être » (`cloture.py:10`).
- **D/I** : les plus petites cases du carnet (3,5 cm, dues à `per_page=3`, `exercices.py:89`) portent les questions à deux volets (Q2, Q3 avec un récit) : en police automatique, le texte tapé rétrécit ; à la main, la place manque.
- **Recommandations** : `per_page=2` ; Q3 en deux champs (« Spontanément, je… » / « La fois où j'ai dû faire l'inverse, et ce que cela m'a coûté : … ») ; Q1 : « Pensez à la dernière fois que c'est arrivé. Qu'avez-vous fait de votre soirée, et cela vous a-t-il vraiment rechargé ? » ; amorce pour Q2 : « Quand on m'interrompt, la première chose qui se passe en moi, c'est… ».

### Exercice 3 · Information (p. 6-7, Q4-7) · 20-30 min

- **F** : Q4 (`exercices.py:20-23`) neutralise son ressort : en listant « ce que vous voyez, à quoi il sert, ce qu'il vous évoque », elle fait tout produire à tous, alors que l'exercice vaut par ce qui vient spontanément. Réécrire : « Choisissez un objet près de vous. Décrivez-le en 4 ou 5 phrases, dans l'ordre où les idées vous viennent. Ne relisez pas avant d'avoir fini. »
- **A** : Q6 (`exercices.py:28-30`) récolte un sujet, pas un ressort. Ajouter : « De quoi auriez-vous aimé parler ? »
- **E** : Q7 « votre vie idéale » dans 5 ans (`exercices.py:31-33`) double la vision à 360° (chap1) et les pistes « no limit » (chap6), et contredit l'engagement « situations vécues ». Recentrer : « Imaginez une journée ordinaire dans cinq ans. Décrivez le décor, les personnes, le rythme. Qu'est-ce qui vous donne de la fierté ce jour-là ? » (remplace « fier ou fière »).
- **D** : quatre cases de 7,3 cm, larges pour Q6.

### Exercice 4 · Décisions (p. 8-9, Q8-11) · 20-30 min

- **F** : Q8 « Décrivez votre malaise face à ce choix » (`exercices.py:37-38`) présuppose la réponse : qui tranche sans malaise ne sait plus quoi écrire. Réécrire : « Sur quoi fondez-vous votre choix ? Qu'est-ce qui vous reste en tête une fois la décision prise ? » Le titre « Le choix difficile » reprend celui de chap5 (Ex3) pour un autre exercice : renommer « La dernière place ».
- **G** : Q11 « la dernière critique qui vous a blessé·e » (`exercices.py:47-48`) : charge moyenne, sans clôture (section 3).
- **B** : Q10 et Q11 produisent des irritants (dispute, critique) jamais retournés en besoin.
- **D** : cases de 7,3 cm, adaptées (Q9 pose trois questions).

### Exercice 5 · Temps et action (p. 10-11, Q12-15) · 15-25 min

- **F** : le titre « L'adrénaline de l'échéance » (`exercices.py:54`) suggère le travail de dernière minute, et la question rate le ressort (quand on commence, comment l'effort se répartit). Réécrire : « 13. L'échéance. Pensez au dernier projet important à rendre à date fixe. Racontez comment le travail s'est réparti entre le lancement et la date limite. À quel moment avez-vous été le plus efficace ? »
- **D** : Q12, Q14 et Q15 sont neutres et bien posées, mais Q12 (« Que ressentez-vous ? ») reçoit 7,3 cm comme les autres. Q14 et Q15, choix à deux pôles, appellent une échelle 1-5 suivie d'un « pourquoi » de deux lignes, sans nommer de pôle MBTI® (l'auto-estimation se fait en séance). Amorce pour Q12 : « Ma première heure, ce samedi-là, ressemble à… ».

### Exercice 6 · Zone d'ombre (p. 12, Q16-17) · 10-20 min

- **G** : l'exercice le plus chargé (stress extrême, rumination nocturne), sans aucun élément du protocole. « (bonus) » laisse deviner que Q17 est facultative, sans le dire comme un droit.
- **F (MBTI®)** : Q16 (`exercices.py:65-68`) parle de « mauvais côté » et propose quatre portraits péjoratifs (« Tyrannique et cassant·e ? »…). C'est demander de s'étiqueter, à rebours de l'esprit de l'outil. La réaction sous stress n'est pas expliquée.
- **Ton** : cinq points médians en deux lignes (`exercices.py:67-68`) ; « poussé·e dans vos retranchements » (`exercices.py:109`).
- **Recommandations** :
  - En tête : « Ces deux questions touchent à des moments difficiles. Partez d'un souvenir que vous regardez aujourd'hui avec un peu de recul. Si une question vous semble trop lourde à aborder de votre côté, laissez-la vierge : nous en parlerons ensemble. »
  - Q16 : « 16. Sous pression. Sous l'effet d'un stress fort ou d'une grande fatigue, on réagit parfois d'une façon qui ne nous ressemble pas. Que remarquent vos proches ou vos collègues dans ces moments-là ? Par exemple : vous devenez plus critique, plus à fleur de peau, vous vous perdez dans les détails, ou vous agissez sur un coup de tête. »
  - Clôture, avec un champ court (`QuestionItem` accepte `box_height`, `templates.py:62-67`) : « Aujourd'hui, avec le recul, je sais que ce qui m'aide à revenir à moi, c'est… »
  - Intro : « Comment vous réagissez quand la pression devient trop forte. »

### Clôture : livrable et dos (p. 13-14) · 5-10 min

- **C** : « Mes notes pour la prochaine séance » occupe 17 × 12 cm (`components.py:463-468`) sans guidage : elle intimide et ne prépare pas la restitution.
- **E** : le livrable « Votre mode d'emploi » (`cloture.py:14-16`) se résume à « vos réponses », oublie la zone d'ombre, et rien ne permet de noter le résultat de la restitution.
- **F** : l'engagement « Je réponds à partir de situations vécues » (`cloture.py:10`) arrive après les 17 questions : c'est une consigne, à lire avant.
- **Recommandations** : remplacer la grande case par trois champs : « Ce qui m'étonne en répondant » (3 lignes), « Les questions où j'ai hésité entre deux réponses : n° … » (1 ligne), « Ce que je veux aborder pendant la restitution » (3 lignes). Ajouter un encadré « À compléter après la restitution » : « Le type que j'ai validé : … », « Ce qui me ressemble le plus : … », « Ce qui me ressemble moins : … ».

## 3. Charge émotionnelle

| Exercice | Niveau | Avertissement | Optionnalité | Clôture | Question plus franche possible (protocole en place) |
|---|---|---|---|---|---|
| Ex1 récap (vallées), Q8 exclusion, Q10 dispute | faible | absent | absente | absente | Inutile ; retirer de Q8 la présupposition du « malaise ». |
| Q11 · Critique blessante | moyen | absent | absente | absente | « Pensez à une critique récente qui vous a fait mal. Avec le recul, qu'y avait-il de juste, et qu'y avait-il d'injuste ? » Clôture : « Aujourd'hui, ce que j'en garde, c'est… » |
| Q16 · Point de rupture | fort | absent | absente | absente | « Qu'est-ce que vos proches voient de vous dans ces moments-là, que vous préféreriez qu'ils ne voient pas ? » |
| Q17 · Insomnie | moyen à fort (rumination écrite sans accompagnement) | absent | implicite (« bonus ») | absente | « Sur quoi votre cerveau boucle-t-il ces temps-ci ? Notez-le en quelques mots, sans le développer. » Clôture : « Ce que je préfère déposer en séance plutôt que de le ressasser : … » |

## 4. Fil rouge

**Entrées**
- Explicite : ligne de vie et arbre de vie (chap2 Ex4, Ex6), dans le récapitulatif p. 3.
- Implicites, non citées : le livrable de chap2 (fil rouge, moteurs) et ses colonnes « Ce que j'ai aimé / pas aimé » (Ex2), qui renseignent déjà sur l'énergie.

**Sorties**
- Les réponses nourrissent la restitution : objectif atteint. Chap0 p. 3 l'annonçait (« Explorer votre personnalité »).
- Chap4 Ex1 (récap MBTI®) : trois questions guidées sur les forces et le fonctionnement, bien posées, mais qui supposent un profil que chap3 ne permet pas de noter.
- Chap6 Ex2 (cartographie) : « Type MBTI® » et « Mes sources de stress » ; la seconde devrait renvoyer à Q16-17.
- Livret, thème 1 (p. 2-3) : « Mes préférences spontanées (ou mon type MBTI®) » et « Ce qui vide mes batteries » devraient renvoyer à Q1, Q2, Q6 et Q12. Le livret pose le cadre qui manque ici (« ni un examen ni une étiquette qui vous enferme ») : à remonter en chap3. À signaler : son exemple « ISFJ — … » donne un type en modèle.
- Chap5 Ex7 (conditions de travail) : destinataire naturel des irritants de chap3 (interruption, dispute, imprévu), sans lien.

**Doublons**
- Récap Q1 et Q3 identiques au récap de chap2 (Q1 et Q4).
- Q7 recoupe la vision à 360° (chap1 Ex2) et les métiers « no limit » (chap6 Ex4).
- Titre de Q8 « Le choix difficile » proche de chap5 Ex3 « Vos choix difficiles », pour un autre exercice.
- Ce qui vide l'énergie est demandé trois fois sans renvoi : chap3 Ex2, chap5 Synthèse (« Je perds de l'énergie quand : »), livret p. 3.

**Ruptures**
- Le type validé n'est noté nulle part avant chap6, alors que chap4 s'ouvre sur le profil.
- Le « mode d'emploi » annoncé (p. 2, p. 13) n'est jamais synthétisé.
- Les irritants ne deviennent jamais des critères.

## 5. Écart avec l'app web

- `_build_chap3_spec` (`server/predefined_workbooks.py:418-551`) est un autre carnet, « Compétences et moteurs » : météo de l'énergie, colonnes « m'épuise / me donne de l'énergie », quatre zones de compétences, verbes d'action.
- Aucune question MBTI®, pas de récapitulatif, pas de zone d'ombre ; le MBTI® n'apparaît nulle part dans l'app.
- À l'inverse, le web a ce qui manque au CLI : le croisement compétence × énergie (zone d'excellence, zone à risque) et des exemples par ligne.
- « m'a le plus intéressé » (ligne 457) y est genré.

## 6. Recommandations classées

| Priorité | Type | Page(s) | Constat | Recommandation |
|---|---|---|---|---|
| P1 | correction rapide | 12 | Ex6 (stress extrême, rumination) sans avertissement, optionnalité ni clôture | Avertissement et optionnalité en tête, champ de clôture (textes en section 2 ; `exercices.py:64-72`) |
| P1 | correction rapide | 12 | Q16 fait s'étiqueter (« mauvais côté », « Tyrannique et cassant·e ») | Reformulation « Sous pression » par le regard des proches, en verbes épicènes (section 2) |
| P2 | correction rapide | 9 | Q11 (critique blessante) sans clôture | Reformulation et clôture proposées en section 3 |
| P2 | correction rapide | 4 | MBTI® jamais expliqué ; « cinq dimensions » ; rien sur la validation du type par la personne | Encadré « À savoir sur le MBTI® » ; titre « Quatre préférences, et vos réactions sous pression » |
| P2 | correction rapide | 4 | Ni confidentialité ni droit de passer | Deux phrases de cadre (section 2, ouverture) |
| P2 | correction rapide | 6, 8, 10 | Consignes qui orientent : Q4 (liste des angles), Q8 (« votre malaise »), Q13 (« adrénaline ») | Réécritures proposées en section 2 |
| P2 | correction rapide | 4, 5, 7, 13 | L'engagement « situations vécues » arrive en fin ; Q1 et Q7 demandent l'« idéal » | En faire la consigne p. 4 ; réécrire Q1 et Q7 |
| P2 | correction rapide | 2, 4-12 | Aucune durée, pas de « en plusieurs fois » | Durée en sourcil (« EXERCICE 2 · 15-20 MIN ») et total p. 4 |
| P2 | correction rapide | 4 | Aucun exemple de réponse terminée | Un exemple contrasté sur un sujet hors questionnaire (le restaurant) |
| P2 | correction rapide | 5 | Cases de 3,5 cm pour Q2-Q3, questions à deux volets | `per_page=2` (`exercices.py:89`) ; Q3 en deux champs, avec « ce que cela m'a coûté » |
| P2 | refonte | 13 | Grande case de notes sans guidage ; pas de « surpris » ni « à aborder » | Trois champs guidés (paramètre à ajouter à `create_standard_engagement_page`) |
| P2 | refonte | 13 | Rien pour noter le type validé ; chap4, chap6 et le livret en ont besoin | Encadré « À compléter après la restitution » |
| P2 | refonte | nouvelle page avant 13 | Irritants jamais retournés en critères ; compétence × énergie jamais croisées | Page « Ce que j'en retiens pour mon futur travail » : « Je sais le faire, mais cela me coûte : … », « Je ne veux plus…, donc mon prochain poste doit… », « Pour garder mon énergie, j'ai besoin de… » |
| P3 | correction rapide | 4, 5, 7, 9, 12 | Formulations floues ou lourdes : « information immédiate », énergie « dans votre tête et dans votre corps », points médians en rafale, « fier ou fière » | « Comment vous vous rechargez, et ce que vous faites des sollicitations. » ; tournures épicènes (« en pleine concentration », « qui vous a fait mal ») |
| P3 | correction rapide | 3, 7, 8 | Récap générique ; Q7 double chap1 et chap6 ; titre de Q8 proche de chap5 | Q3 du récap sur les moteurs du carnet 2 ; recentrer Q7 ; renommer Q8 « La dernière place » |
| P3 | refonte | 10-11 | 17 réponses libres de même format | Échelle 1-5 + « pourquoi » pour Q14 et Q15, sans nommer de pôle |
| P3 | correction rapide | chap6, livret | Sorties de chap3 reprises sans renvoi | « Reprenez vos réponses 1, 2, 6 et 12 du carnet 3 » (livret p. 3) ; « sources de stress » ← Q16-17 (chap6) |
| P3 | refonte | app web | Carnet 3 web sans rapport avec le CLI | Choisir la version de référence ; envisager d'importer dans le CLI les quatre zones de compétences |
