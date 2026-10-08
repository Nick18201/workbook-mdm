# Audit · Livret projet « Mon business plan »

Fichiers cités : dossier `Scripts/workbook_generator/chapters/business_plan/`, sauf mention contraire. Pages = folio du PDF (36 pages, 316 champs).

## 1. Synthèse

Un modèle de business plan complet et bien ordonné, mais conçu comme un dossier d'école de commerce plutôt qu'un carnet MDM : linéaire, sans durée, sans lien avec le bilan, et ses exemples décrivent tous un accompagnement individuel vendu à des femmes.
Points forts : la séparation intuitions / à vérifier (p. 7), les critères « continuer ou pivoter » (p. 31), le ton juste des engagements (p. 35).

1. **Granularité et orientation** : 21 sections numérotées pour 6 parties annoncées, aucune durée (15 à 17 h de rédaction estimées, plus que le bilan), rien d'indispensable ni de facultatif. Fort risque d'évitement.
2. **Finances impossibles à remplir sans aide** : 161 cellules d'une ligne (136 d'une capacité estimée à 23 caractères au plus, saisie bloquée au-delà), totaux de la p. 30 dessinés sans champ, exemples cachés en infobulle, chiffres non sourcés ou datés, aucun lien avec le minimum financier du carnet 4.
3. **Risque personnel et viabilité absents** : aucun élément du protocole de sécurité ; ni argent du foyer, ni couple, ni peur de l'échec ; valeurs et énergie du bilan jamais reprises ; feuille de route préremplie (p. 33) alors que la p. 3 promet « Rien n'est prérempli ».

## 2. Partie par partie

### Ouverture (p. 1-3) · 10-15 min
- **A, F** : la p. 3 annonce six parties et une « boucle en six temps » (`cover.py:42-56`) que les pages n'utilisent jamais : les eyebrows vont de « 1. Poser les fondations » à « 21. Synthèse » (`fondations.py:18`, `action_synthese.py:198`) au lieu de « Exercice N · nom » (convention DA). Ni durée, ni total, ni mention d'un travail par modules. L'étape « décider » n'a pas de page.
- **H** : aucun cadre (qui lit, droit de passer, ce qui est trop lourd se note). Or le livret peut servir hors bilan, et la p. 34 vise un financeur : rien ne sépare le brouillon intime du document montrable.
- **I** : « Rien n'est prérempli » (`cover.py:54`) est faux (p. 33).
- **Recommandation** (refonte) : une page « Mode d'emploi » après la p. 3.
  > « Ce livret se travaille par parties, dans l'ordre qui vous sert. Comptez une à cinq heures par partie, en plusieurs fois. Les exercices marqués « Indispensable » suffisent pour une première version. Une page ne concerne pas votre projet : passez-la. Ce livret est à vous : la personne qui vous accompagne le lit avec vous en séance. Seule la synthèse (p. 34) est faite pour être montrée à un financeur. »

  Ajouter trois entrées (idée floue : parties 1, 2 et p. 31 ; offre claire : parties 4 et 5 ; reprise : page reprise, puis partie 5) et un parcours court de 12 pages : p. 4, 8, 9, 10, 20, 28 à 34.

### Partie 1 · Fondations et cible (p. 4-7) · 1 h 15-1 h 30
- **A** : p. 4, deux questions sur trois sans amorce. Les exemples des cartes (p. 5, 7) ne sont que des infobulles (`templates.py:369`), invisibles à l'impression.
- **B** : la p. 5 fait de l'introspection par le négatif (« Ce que je refuse absolument de construire », `fondations.py:87-90`) sans la retourner en critère. Rien ne distingue le désir réel d'entreprendre de l'attendu social, ni les tâches qui rechargent de celles qui épuisent.
- **Ton** : « déclic » (`fondations.py:40`), « écologie personnelle » (`fondations.py:63`), « l'entrepreneure » (`fondations.py:24`) genre la lectrice.
- **Doublons** : p. 2 et p. 4 Q2 (« Mon projet en une phrase ») ; p. 6 Q3 et p. 8 Q3 (les solutions actuelles).
- **Recommandations** :
  - p. 4 Q3, deux amorces : « Ce que je veux vraiment, c'est… » / « Ce que je crois devoir faire, parce qu'on l'attend de moi, c'est… ».
  - p. 5 Q4 : « Je refuse… donc mon activité devra… ». Exemple : « Je refuse de travailler le week-end, donc mon activité fonctionnera du lundi au vendredi. »
  - Nouvel exercice « Ma semaine type dans cette activité » (refonte) : Tâche | Heures par semaine | Me recharge / Me coûte | Donc je…
    > Exemple de surface : « J'aime le contact client. »
    > Exemple exploitable : « Je passerai une journée par semaine à prospecter. Cela me coûte : je la coupe en deux demi-journées et je m'appuie sur deux prescripteurs. »

### Partie 2 · Problème et offre (p. 8-11) · 1 h 30, plus deux à trois semaines d'entretiens
- **D, I** : p. 9, tableau des hypothèses en cellules d'une ligne de 12,9 pt : 18 à 23 caractères estimés, puis police rétrécie et saisie bloquée (`cible_probleme.py:161-202`, `templates.py:535`). Une hypothèse n'y tient pas. P1.
- **Ordre** : la p. 9 demande ce que le terrain a appris avant le guide d'entretien (p. 31) ; ses hypothèses ne sont reprises ni p. 31 ni p. 32.
- **A** : exemple visible p. 9, bon. Exemple p. 10 (`offre_marche.py:34`) : « accompagnement individuel en 5 séances avec livret d'exercices », soit le métier de MDM, recopiable. Formule p. 11 « J'accompagne [Cible]… » (`:90`) : inutilisable pour une boulangerie.
- **Ton** : « la cliente », « Être précise » (`offre_marche.py:23-24`).
- **Recommandations** :
  - p. 9 : trois hypothèses en cartes de deux à trois lignes.
  - p. 8 Q1, un exemple contrasté :
    > Surface : « Les gens manquent de temps. »
    > Exploitable : « Trois des cinq artisans interrogés rédigent leurs devis le soir, après le chantier ; l'un a perdu un client faute de réponse rapide. »
  - p. 11 Q3 : « [Mon activité] permet à [qui] de [résultat], sans [ce qui les gêne aujourd'hui]. »

### Partie 3 · Marché et positionnement (p. 12-16) · environ 3 h, recherches comprises
- **D** : p. 12, tendances en deux lignes (60 pt) ; p. 14, 16 cellules d'une ligne ; p. 16, tailles inversées : trois versions en trois lignes (72 pt), six lignes (150 pt) pour la seule phrase retenue (`positionnement.py:96, 104`).
- **F** : « normes ERP » sans définition (`offre_marche.py:145`) ; question réglementaire sans aucune source.
- **I** : p. 13, la consigne ne dit pas ce que signifie cocher une famille d'acteurs (`offre_marche.py:169-178`). Deux cartes pour quatre familles : l'inaction n'a pas sa case.
- **A** : exemple p. 16 « J'aide les femmes en reconversion… » (`positionnement.py:106`), soit l'offre de MDM.
- **Ton** : « vibration » (`positionnement.py:36`). Doublons : la phrase de pitch revient cinq fois (p. 2, 4, 11, 16, 34) ; ton et lignes rouges, p. 15 et 23.
- **Recommandations** : marquer p. 14 à 16 « Si utile ». Écrire « établissement recevant du public (ERP) ». Exemple p. 16 : « Je révise et revends des vélos d'occasion, garantis six mois, aux étudiants de ma ville. » Ajouter à la p. 13 une carte « L'inaction : ce que vos clients font s'ils ne font rien ».

### Partie 4 · Modèle économique et vente (p. 17-22) · 2 h 30-3 h
- **F** : le Business Model Canvas arrive sans explication (« écosystème en 9 blocs interdépendants », `modele_commercial.py:74-77`) et recopie des pages déjà faites. Jargon non défini : « core offer », « cross-sell », « B2B », « OPCO », « SEO », « effet whaou » (`:402`).
  - Définition proposée : « Le Business Model Canvas est une grille de neuf cases sur une page. Elle montre d'un coup d'œil à qui vous vendez, quoi, par quel chemin, avec quelles dépenses et quelles recettes. Reportez-y en quelques mots ce que vous avez écrit p. 6, 11, 17, 21, 25 et 28. »
- **D** : p. 19, le prix tient dans 11 caractères et la colonne « Marge » n'a pas de méthode : « La marge, c'est ce qui reste du prix une fois payé ce que coûte la prestation (matériel, sous-traitance, déplacement). » p. 20 : quatre cases d'une ligne manuscrite (`:275`).
- **Ordre** : le prix plancher (p. 20) demande les coûts, qui n'arrivent qu'aux p. 28-29 : « Revenez à cette page après la page 29. »
- **G** : le prix touche à la légitimité sans amorce. Proposer : « Le prix que j'ose annoncer à voix haute : … € · Le prix que mes calculs demandent : … € · L'écart vient de… »
- **I** : « Le parcours client en 7 étapes » pour un tableau de 4 lignes (`:351, 373-394`).

### Partie 5 · Moyens, finances et cadre (p. 23-30) · 4-5 h, plus devis et rendez-vous
- **A** : huit pages, la partie la plus lourde ; la communication (p. 23-24) peut attendre le test (« Si utile »).
- **D, E** : p. 26, « Niveau actuel (1 à 5) » se tape en texte libre, alors que le livret de compétences compte 4 niveaux (`organisation_finances.py:220-261`). « Une légitimité indiscutable » (`:268`) met la pression. Reformuler : « Quelles réussites passées montrent que vous savez déjà faire une partie de ce métier ? Reprenez votre récit d'action (livret de compétences). »
- **F (p. 27)** : statuts listés sans aucune différence expliquée ; cases ambiguës (obligatoire ? fait ?) et en partie inexactes (§5, `:301-312`).
- **Finances (p. 28-30)** : une personne sans culture entrepreneuriale ne peut pas les remplir seule.
  - p. 28 : exemples en infobulle seulement, quatre lignes, pas de total, cellules de 14 à 33 caractères ; ni CFE, ni TVA, ni expert-comptable.
  - p. 29 : « Faire comprendre le raisonnement économique » (`:441`) est une note de conception. Scénarios en trois lignes (77 pt). « 2 à 3 ventes / mois » (`:449`) impose un modèle de service.
  - p. 30 : « Besoin initial », « Trésorerie », « Total global » dessinés sans champ (`:501-506`).
- **Recommandations** (refonte) : une grille de calcul guidée sur la p. 29.
  - Ventes par mois × prix moyen = chiffre d'affaires ; − charges (total p. 28) ; − cotisations (taux selon votre activité, voir §5) ; = ce qui reste pour vous ; à comparer avec votre minimum vital (carnet 4).
  - Définition : « Le point mort est le chiffre d'affaires à partir duquel votre activité paie toutes ses charges. En dessous, elle vous coûte ; au-dessus, elle commence à vous payer. Ici, nous y ajoutons votre rémunération minimale : c'est le chiffre d'affaires dont vous avez besoin pour vivre de votre activité. »

### Partie 6 · Test et synthèse (p. 31-34) · 2 h-2 h 30, plus le test
- **p. 31** : la carte « Critères de décision » est la meilleure idée du livret, mais l'exemple n'est qu'en infobulle. Exemple contrasté à rendre visible :
  > Surface : « Si ça marche, je continue. »
  > Exploitable : « Je continue si trois des dix personnes contactées acceptent un essai payant. Je revois l'offre si personne ne paie. »
- **p. 32** : seize cellules d'une ligne ; « Gravité & probabilité » sans échelle ; aucun risque personnel ; les « 5 hypothèses vitales » refont la p. 9.
- **p. 33** : 15 champs préremplis (`action_synthese.py:144-178`, valeurs posées par `components.py:958-960`) avec une feuille de route d'accompagnement (« 3 clientes accompagnées »). Cases d'une ligne manuscrite.
- **p. 34** : cases de deux à trois lignes, la carte finances deux (63 pt). « Executive Summary », « déclic personnel » (`action_synthese.py:202, 210`). Il manque la décision, le test, les risques et la viabilité personnelle. Ajouter : « Ma décision aujourd'hui : je lance / je teste encore / je modifie / je mets en pause, parce que… » et « Ce projet respecte mes 3 valeurs non négociables et mon minimum vital : oui / en partie / non ».

### Clôture (p. 35-36) · 10 min
- **C** : une zone de notes de 13 lignes, sans structure ; nulle part « Ce qui m'étonne » ni « À aborder en séance ». Ajouter en fin de partie : « À aborder en séance : deux ou trois points non tranchés. » En fin de livret : « Ce qui m'étonne en relisant ce livret : … »
- 36 pages ne se valident pas en une séance de 1 h 20 : écrire « validé partie par partie ».

## 3. Charge émotionnelle

Aucun exercice n'a le protocole complet. Seuls trois éléments partiels existent : « sans censure » (p. 4), « Cette phrase évoluera : c'est voulu » (p. 2), « Être lucide… n'est pas être pessimiste » (p. 32).

| Exercice | Niveau | Protocole présent / absent | Question plus franche possible |
|---|---|---|---|
| p. 4 Q3 Pourquoi ce projet | faible | aucun | « Ce projet, je le fais pour moi ou pour prouver quelque chose à quelqu'un : … » |
| p. 20 Prix | moyen | aucun | « Le prix que je n'ose pas annoncer, et ce que je crains d'entendre : … » |
| p. 26 Compétences | moyen | aucun | « La compétence qui me manque et qui me fait douter de tout le projet : … » |
| p. 29 Point mort | moyen | aucun | « Si le projet ne couvre pas mon minimum vital au bout de … mois, je… » |
| p. 30 Financement, apport personnel | fort | aucun | « La somme que je peux perdre sans mettre mon foyer en difficulté : … € » |
| p. 32 Risques | fort | avertissement partiel | « Ce qui me ferait le plus mal si le projet s'arrêtait : l'argent, le regard des autres, autre chose : … » |
| absent : couple, entourage | fort | — | « Ce que la personne qui partage ma vie pense de ce projet, et ce qu'elle craint : … » |

Recommandation (refonte) : une page « Le risque, pour vous », placée avant la p. 30.
1. Avertissement : « Cette page parle de votre argent personnel, de votre foyer et de vos peurs. Elle est engageante. »
2. Optionnalité : « Si elle vous semble trop lourde à remplir sans appui, laissez-la vierge : nous l'aborderons ensemble en séance. »
3. Clôture : « Aujourd'hui, ce qui me permet d'avancer malgré ce risque, c'est… »

## 4. Fil rouge

**Avec le bilan.** Les mots « bilan » et « carnet » n'apparaissent jamais : aucune entrée n'est reprise. Le livret pouvant servir hors bilan, chaque renvoi commencera par « Si vous avez fait le bilan : ».

| Source | Sortie du bilan | Où l'utiliser | Formulation proposée |
|---|---|---|---|
| chap4 p. 12 | minimum vital, minimum sécurisant, revenu cible | p. 29 (rémunération), p. 20 (plancher) | « Reportez votre minimum vital mensuel (carnet 4) : votre point mort doit au moins le couvrir. » |
| chap4 p. 12 | durée acceptable d'une baisse de revenus | p. 30 (trésorerie) | remplace « 3 à 6 mois » : « Votre matelas couvre la durée que vous jugez acceptable (carnet 4). » |
| chap4 p. 13-14 | tendances (sécuritaire, évitant…) | p. 30, p. 32 | « Votre tendance dominante face à l'argent pèse-t-elle sur ce choix de financement ? » |
| chap5 p. 10, 14, 17 | 3 valeurs non négociables, conditions de travail | p. 5, p. 32 (hypothèse 5), p. 34 | « Ce projet respecte-t-il vos 3 valeurs non négociables ? Oui / en partie / non. » |
| chap5 p. 15 | tensions (liberté / sécurité, sens / rémunération) | p. 30 | « Quelle tension ce projet réveille-t-il ? » |
| chap6 p. 6-10 | pistes métiers | p. 4 | « Si ce projet est l'une de vos pistes (carnet 6), reprenez sa fiche. » |
| chap0 ex. 4, chap6 ex. 3 | soutiens, regards critiques, retour des proches | p. 26, page risque | regard de l'entourage sur le risque |
| livret p. 3, 10-11, 14 | ce qui vide les batteries, récit d'action, cadre de sécurité | p. 26, semaine type, p. 29 | « Reprenez votre récit d'action : il fonde votre légitimité. » |

Doublons avec le bilan : « Mes forces et expériences piliers » (p. 26) refait le récit d'action du livret ; « La place dans ma vie » (p. 5) refait les conditions de travail du carnet 5.

**À l'intérieur du livret.**

| Sortie | Reprise ? |
|---|---|
| Hypothèses p. 9 | non : la p. 31 n'y renvoie pas, la p. 32 en écrit de nouvelles |
| Charges p. 28 | non : pas de total, et la p. 29 n'y renvoie pas |
| Prix p. 20 | seulement par l'exemple (750 €), pas dans la consigne de la p. 29 |
| Point mort p. 29 | p. 33 palier 3, mais dans un texte prérempli |
| Totaux p. 30 | impossibles à saisir, donc la carte 6 de la p. 34 n'a pas d'entrée |
| Critères p. 31, risques p. 32, feuille de route p. 33 | absents de la synthèse p. 34 |
| Refus p. 5, 14, 15, 23 | quatre fois demandés, jamais transformés en critère |

## 5. Exactitude

| Page | Code | Constat | Action |
|---|---|---|---|
| p. 27 | `organisation_finances.py:303` | La micro-entreprise est un régime de l'entreprise individuelle, pas un statut. Depuis le 15 mai 2022 (loi du 14 février 2022), l'EI sépare par défaut le patrimoine professionnel : nuancer « protection du patrimoine » (`:318`). « Coopérative » est vague (CAE ? SCOP ?). | Carte d'information de quatre lignes ; renvoi vers Bpifrance Création et le guichet unique (formalites.entreprises.gouv.fr), via `add_link_card`. |
| p. 27 | `:304`, `:297` | RC Pro rangée parmi les « obligations » (intro : « assurances obligatoires ») : elle ne l'est que pour certaines activités réglementées (santé, droit, bâtiment avec décennale…). | « Vérifiez si une assurance est obligatoire pour votre activité ; sinon, elle reste recommandée. » |
| p. 27 | `:305` | Le compte professionnel est obligatoire en société. En micro-entreprise, un compte dédié (pas forcément professionnel) ne l'est qu'au-delà de 10 000 € de chiffre d'affaires deux années de suite. | Préciser. |
| p. 27 | `:308` | Médiateur de la consommation (B2C) : exact (Code de la consommation, art. L612-1). | Ajouter la source. |
| p. 28 | `:405-406` | Infobulle « 21 % du CA », mêlé à des frais « bancaires ». Le taux micro dépend de l'activité : 12,3 % pour la vente, 21,2 % pour les services commerciaux et artisanaux, davantage pour une partie des libéraux (hausse 2024-2026). « ACRE 1ère année » : dispositif réformé par la LFSS 2025. | Supprimer les taux. Renvoyer vers autoentrepreneur.urssaf.fr et urssaf.fr, à la date d'usage. |
| p. 28 | `:358-360` | « Immatriculation 150 € » : c'est gratuit pour une micro-entreprise dans la plupart des cas ; une société paie greffe et annonce légale. | Renvoyer vers le guichet unique. |
| p. 28 | `:419-424` | « Marge d'imprévus de 15 % à 20 % » présentée comme une règle, sans source. | « une marge pour imprévus, à fixer avec votre expert-comptable ou votre conseiller ». |
| p. 30 | `:497` | « 3 à 6 mois de charges » : non sourcé. | Relier à la durée du carnet 4. |
| p. 30 | `:532-541` | ARE, ARCE et prêt d'honneur en infobulle, avec montants. Les règles d'ARE et d'ARCE suivent l'assurance chômage ; les prêts d'honneur viennent d'Initiative France, Réseau Entreprendre ou France Active. | Renvoyer vers francetravail.fr et ces réseaux. |
| p. 29 | `:477` | Calcul juste (300 + 700 + 2 000 = 4 × 750), mais cotisations en montant fixe alors qu'elles sont proportionnelles ; « salaire net » impropre en micro (on se verse une rémunération) et sous-estimé en SASU (charges en plus). | Corriger les mots. |
| — | — | TVA (franchise en base, seuils récemment modifiés) et CFE (due à partir de la deuxième année) absentes. | Deux lignes p. 28, renvoi vers impots.gouv.fr. |
| p. 17, 19, 21 | `modele_commercial.py:55, 215, 305` | « 30 % » d'acompte, « 80 % de votre énergie », « 2 à 3 canaux » : repères non sourcés présentés comme des règles. | Les présenter comme des exemples. |

## 6. Écart avec l'app web

- Web (`server/predefined_workbooks.py:999-1198`) : 10 pages contre 36 ; ni marché, ni prix, ni statut, ni financement, ni risques.
- Le web ouvre sur une « météo » émotionnelle (« À l'idée de vendre mes prestations, je ressens », l. 1037), absente du PDF : à reprendre dans le PDF.
- Feuille de route à 90 jours sur le web, 6 mois dans le PDF ; les deux sont préremplies.
- Web au masculin (« posture d'entrepreneur », « peaufiner seul »), PDF au féminin.
- Exemples chiffrés différents (1 200 € HT contre 750 €) : aucune des deux versions ne suit l'autre.

## 7. Recommandations classées

| Priorité | Type | Page(s) | Constat | Recommandation |
|---|---|---|---|---|
| P1 | refonte | p. 3 et toutes | 36 pages, 21 sections contre 6 parties, aucune durée, rien d'indispensable | « Mode d'emploi » (§2) ; eyebrow « Partie N · Exercice · 20 min » ; « Indispensable / Si utile » ; parcours court |
| P1 | correction rapide | p. 33 | 15 champs préremplis avec une feuille de route d'accompagnement | Textes par défaut en infobulle ; « Reprenez vos critères (p. 31) et votre point mort (p. 29). » |
| P1 | correction rapide | p. 30 | Totaux dessinés sans champ | Trois champs montant, plus « total p. 28 + matelas = à financer » |
| P1 | refonte | p. 9, 14, 19, 22, 24, 26, 28, 30, 32 | 161 cellules d'une ligne, 136 de 23 caractères au plus | Cellules de deux lignes minimum, moins de lignes, ou cartes |
| P1 | refonte | p. 28-30 | Finances inaccessibles à un non-initié | Grille de calcul guidée (§2), lignes total, exemples visibles, définitions |
| P1 | refonte | nouvelle page | Argent du foyer, couple, peur de l'échec absents ; aucun protocole | Page « Le risque, pour vous » avec les trois éléments du protocole (§3) |
| P1 | correction rapide | p. 27, 28, 30 | Informations réglementaires inexactes ou non sourcées | Corrections du §5 et liens officiels |
| P2 | correction rapide | p. 5, 20, 29, 30, 32, 34 | Carnets 4 et 5 jamais repris | Encarts « Si vous avez fait le bilan » (§4) |
| P2 | refonte | partie 1 | Énergie au quotidien, désir réel ou attendu, refus jamais retournés | « Ma semaine type », amorces « je veux / je crois devoir », « Je refuse… donc… » |
| P2 | correction rapide | p. 10, 16, 20, 29, 32, 33 | Exemples tous dans l'accompagnement individuel pour femmes | Un exemple par exercice, métiers variés (vélo, artisan, commerce, reprise) |
| P2 | refonte | nouvelle page | « Reprendre une activité » annoncé, jamais traité | Page reprise : cédant, trois derniers bilans, bail, clientèle, salariés, prix ; renvoi vers la CCI ou la CMA |
| P2 | correction rapide | p. 9, 31, 32 | Guide d'entretien après les résultats ; hypothèses non reprises | Déplacer le guide à la p. 9 ; « Reprenez vos hypothèses p. 9 » p. 31 et 32 |
| P2 | correction rapide | p. 34 | Ni décision ni viabilité ; cases de deux à trois lignes | Cartes « Ma décision aujourd'hui » et « viable pour moi » ; agrandir la carte finances |
| P2 | correction rapide | p. 2, 4, 6, 8, 11, 13, 15, 16, 23 | Pitch demandé cinq fois, alternatives trois fois, refus quatre fois | Fusionner : intuition p. 2, version finale p. 16 seulement |
| P2 | correction rapide | p. 18, 19, 29, 31 | Jargon non expliqué (BMC, point mort, marge, MVP, core offer) | Définitions écrites au §2 |
| P2 | correction rapide | p. 20 | Prix fixé avant les coûts | Renvoi vers la p. 29 et amorce « le prix que j'ose annoncer » |
| P2 | correction rapide | fin de partie, p. 35 | Ni « Ce qui m'étonne » ni « À aborder en séance » | Deux zones courtes |
| P2 | correction rapide | toutes les cartes | Exemples en infobulle seulement | Rendre l'exemple principal visible |
| P3 | correction rapide | p. 26 | Échelle 1 à 5 tapée ; le livret compte 4 niveaux | Radios 1 à 4 alignées sur le livret |
| P3 | correction rapide | p. 4, 10, 22, 33, 34 | Genre : « l'entrepreneure », « la cliente », « Être précise », « Ambassadrice » | Formes épicènes : « votre clientèle », « La précision sur ce qui est fourni… » |
| P3 | correction rapide | p. 4, 5, 15, 22, 25, 26, 34 | « déclic », « écologie personnelle », « vibration », « effet whaou », « énergie vitale », « indiscutable » | « l'origine de votre décision », « votre équilibre », « l'ambiance », « l'attention qui surprend », « votre énergie », « solide » |
| P3 | correction rapide | p. 13, 16, 22, 27 | Cases à cocher ambiguës ; tailles inversées ; « 7 étapes » pour 4 lignes | « Cochez ce qui s'applique à votre activité. » ; versions sur cinq lignes, phrase retenue sur deux ; « Le parcours client en quatre temps. » |
| P3 | correction rapide | p. 6, 10, 13, 27, 29, 30, 32 | Ton injonctif (« Ne… jamais », « impérativement »), note de conception p. 29, titres en majuscules initiales | « Commencez par les personnes. » ; « Calculez votre chiffre d'affaires : ventes × prix moyen. » ; minuscules sauf la première lettre |
