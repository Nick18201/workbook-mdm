# Essais du vrai Gemini : vérification des correctifs de la série 1

09/10/2026, 14 h 43 · modèle gemini-3.8-flash · 2 tirage(s) par cas · script `essais-gemini/essais.py`

## Dépense

4 appels : 28 760 jetons envoyés, 22 501 reçus, 5 601 de réflexion, soit 56 862 (plafond 70 000).

## Résultats

| Cas | Tirage | Durée | Jetons | Pages | À corriger | À vérifier | Ce que le cas attend |
|---|---|---|---|---|---|---|---|
| reconversion | 1 | 58,9 s | 18 032 | 17 | 0 | 4 | structure gardée ; fixe : 0 modifié(s), 0 perdu(s), rétablis ; 16 % des textes réécrits |
| reconversion | 2 | 62,4 s | 18 797 | 17 | 0 | 1 | structure gardée ; fixe : 0 modifié(s), 0 perdu(s), rétablis ; 21 % des textes réécrits |
| notes-lourdes | 1 | 26,1 s | 9 511 | 11 | 0 | 1 | 4 exercices, 1 h ; météo 1, annonces 1, ancrages 1 |
| notes-lourdes | 2 | 33,2 s | 10 522 | 10 | 0 | 0 | 4 exercices, 1 h ; météo 1, annonces 1, ancrages 1 |

## Stabilité (tirage 1 / tirage 2)

Forme : la ressemblance des suites de gabarits et de blocs (1 : identiques). Textes communs : la part des textes adaptables écrits à l'identique dans les deux tirages.

| Cas | Pages | Remarques (à corriger + à vérifier) | Forme | Textes communs |
|---|---|---|---|---|
| reconversion | 17 / 17 | 0 + 4 / 0 + 1 | 1,0 | 0,63 |
| notes-lourdes | 11 / 10 | 0 + 1 / 0 + 0 | 0,71 | 0,09 |

## Détail

### Reconversion : le carnet 4 pour une personne comptable qui vise l'ébénisterie

But : Un carnet sur l'argent : ses exemples doivent rester sans montant ni pourcentage, tirés d'un métier voisin, ni comptable ni ébéniste ; ce qui est fixe revient tel quel.

**Tirage 1** : ai, 58,9 s, 17 pages du PDF.

- Résumé de la réponse : 1. Contextualisation des consignes et sous-titres sur la faisabilité financière d'un projet de reconversion impliquant un an de formation et un foyer familial à deux revenus.
2. Révision des idées reçues (exercice 3) autour du passage d'un métier de bureau à un métier d'artisanat/manuel et des transitions à 40 ans passés.
3. Remplacement systématique des exemples contrastés par des métiers voisins épicènes (juriste, ergonome, géomètre, céramiste, architecte, graphiste, restauratrice) illustrant des arbitrages concrets sans jamais citer la comptabilité ni l'ébénisterie.
4. Maintien strict de l'ensemble des blocs fixes, des identifiants et des contraintes d'affichage PDF.
- Structure : gardée
- Fixe changé par Gemini puis rétabli : rien ; perdu puis rétabli : rien
- Textes réécrits : 16 % ; prénom : aucun
- Remarques du contrôle :
  - p. 4 · à vérifier · exemple-personne : l'exemple « Juriste » reprend la situation de la personne (« foyer », « revenus ») : le raconter avec les faits du métier voisin, elle le recopierait
  - p. 10 · à vérifier · exemple-personne : l'exemple « Architecte » reprend la situation de la personne (« atelier », « enfants ») : le raconter avec les faits du métier voisin, elle le recopierait
  - p. 12 · à vérifier · exemple-personne : l'exemple « Graphiste » reprend la situation de la personne (« reconversion », « baisse ») : le raconter avec les faits du métier voisin, elle le recopierait
  - p. 13 · à vérifier · metier-genre : exemple tiré d'un métier au nom genré : « Restauratrice » (prendre un nom épicène : juriste, ergonome…)
- Exemples :
  - Juriste : « Le foyer gagne bien sa vie, tout est simple. » → « En vigilance : deux revenus stables mais un crédit lourd. Un an de transition demande d'isoler l'épargne nécessaire. »
  - Ergonome : « On gérait tout au centime près. » → « Tout devait être justifié par facture. J'en garde le besoin de tout border avant d'oser investir dans un nouvel outil. »
  - Géomètre : « Un métier manuel ne paie pas assez. » → « Je me dis : repartir en bas d'échelle ruinerait le budget familial. Les faits : les artisans qualifiés manquent de bras et facturent leur juste prix. »
  - Céramiste : « Je n'ose pas chiffrer mes heures. » → « En fixant le prix d'un objet, j'oublie le temps de fabrication pour ne pas effrayer. Je crains de valoriser mon geste à son juste tarif. »
  - Architecte : « Je verrai bien selon mes contrats. » → « Minimum vital calculé à l'euro près : loyer et charges d'atelier. J'ai prévu 14 mois d'amortissement sans puiser dans l'épargne des études des enfants. »
  - Graphiste : « Je cherche juste la sécurité. » → « La sécurité m'aide à chiffrer une reconversion réaliste. Elle me freine quand elle m'empêche d'envisager une baisse temporaire. »
  - Restauratrice : « Travailler de mes mains sans stress. » → « Pour ma prochaine piste, l'argent doit sécuriser les charges fixes du foyer tout en finançant mon outillage initial. »

**Tirage 2** : ai, 62,4 s, 17 pages du PDF.

- Résumé de la réponse : 1. Exemples contrastés réorientés vers des métiers voisins au nom épicène (céramiste, ergonome, juriste, géomètre, scénographe, paysagiste) illustrant les arbitrages d'une reconversion pratique et d'une formation longue sans dévoiler le projet exact.
2. Contextualisation des idées reçues et des questions sur la baisse transitoire de revenus, l'impact sur le budget familial et le financement d'une formation professionnelle.
3. Adaptation des libellés de l'exercice 4 (tarification d'une création, dialogue financier familial) pour résonner avec l'arbitrage entre salariat en cabinet et pratique artisanale.
4. Préservation intégrale de la structure, des champs data_id, des identifiants et des blocs fixes (dont le calcul des 4 seuils et le protocole).
- Structure : gardée
- Fixe changé par Gemini puis rétabli : rien ; perdu puis rétabli : rien
- Textes réécrits : 21 % ; prénom : aucun
- Remarques du contrôle :
  - p. 10 · à vérifier · exemple-repete : le métier « Céramiste » sert déjà d'exemple p. 4 (un métier différent à chaque exemple)
- Exemples :
  - Céramiste : « Je gagne bien ma vie actuellement. » → « En sécurité : nos deux salaires couvrent l'emprunt, mais financer un an d'études demande d'anticiper. »
  - Ergonome : « L'argent n'était pas un sujet chez nous. » → « Mes parents valorisaient la sécurité du statut cadre : envisager un métier manuel était perçu comme un déclassement risqué. »
  - Juriste : « Un changement de métier ruine le budget. » → « Je me dis : passer un diplôme manuel vide l'épargne. Les faits : les dispositifs de transition maintiennent une partie du revenu pendant les cours. »
  - Géomètre : « Je n'ose pas fixer mes tarifs. » → « En m'installant, j'avais peur de facturer mes journées au prix du marché, croyant que débuter imposait de travailler presque gratuitement. »
  - Céramiste : « Je réduirai les dépenses au maximum. » → « Minimum vital : scolarité et crédit couverts. J'accepte douze mois d'austérité sur les loisirs pour suivre les cours en atelier. »
  - Scénographe : « Je cherche avant tout la sécurité. » → « La sécurité m'aide à budgéter une reconversion sans dette, mais elle me freine pour quitter un CDI stable. »
  - Paysagiste : « Avoir de quoi vivre simplement. » → « L'argent doit me permettre de financer mon année d'apprentissage tout en assurant ma part du foyer sans anxiété. »

### Notes lourdes : après un licenciement et un épuisement, un document de 60 minutes

But : La charte v2 sur un sujet lourd : des questions franches, l'annonce avant les exercices intimes et la phrase d'ancrage après, sans formule de précaution ; la météo de l'énergie, puisque les notes parlent de fatigue ; les durées qui font 60 minutes.

**Tirage 1** : ai, 26,1 s, 11 pages du PDF.

- Gabarit : cover → summary → composite → composite → composite → composite → composite → engagement → closing
- Sourcils : Exercice 1 · Vos dix-huit ans · 15 min ; Exercice 2 · La rupture et vos repères · 15 min ; Exercice 3 · Vos points d'appui · 10 min ; Exercice 4 · Vos non-négociables et vos pistes · 13 min
- Ouverture : Météo · 2 min ; Exercice 1 · Vos dix-huit ans · 15 min ; Exercice 2 · La rupture et vos repères · 15 min ; Exercice 3 · Vos points d'appui · 10 min ; Exercice 4 · Vos non-négociables et vos pistes · 13 min ; Fin de carnet · 5 min (total 1 h)
- Météo 1, annonces 1, ancrages 1, prénom Karim
- Remarques du contrôle :
  - p. 4 · à vérifier · suite-presque-vide : sa page « (suite) » (p. 5 du PDF) ne porte presque rien : couper l'exercice en deux pages équilibrées ('page_break'), ou le resserrer
- Exemples :
  - Juriste : « J'ai géré beaucoup de dossiers difficiles. » → « J'ai monté la cellule conformité en 2017 et formé trois collaborateurs qui ont pris le relais lors de la réorganisation. »
  - Géomètre : « Je n'aurais pas dû craquer avant l'échéance. » → « La surcharge continue a provoqué l'arrêt. Les décisions de restructuration ne relevaient pas de ma responsabilité. »
  - Ergonome : « Je ne veux plus de stress ni de réunions inutiles. » → « Je refuse le reporting quotidien qui remplace la présence terrain. Mon prochain cadre aura une gouvernance courte et directe. »

**Tirage 2** : ai, 33,2 s, 10 pages du PDF.

- Gabarit : cover → summary → composite → composite → composite → composite → composite → engagement → closing
- Sourcils : Exercice 1 · Ce que j'ai bâti · 15 min ; Exercice 2 · La rupture et le recul · 18 min ; Exercice 3 · Ce que je refuse et mes appuis · 12 min ; Exercice 4 · Les premières pistes · 8 min
- Ouverture : Météo · 2 min ; Exercice 1 · Ce que j'ai bâti · 15 min ; Exercice 2 · La rupture et le recul · 18 min ; Exercice 3 · Ce que je refuse et mes appuis · 12 min ; Exercice 4 · Les premières pistes · 8 min ; Fin de carnet · 5 min (total 1 h)
- Météo 1, annonces 1, ancrages 1, prénom Karim
- Exemples :
  - Urbaniste : « J'ai géré beaucoup de dossiers difficiles. » → « J'ai piloté l'aménagement d'un quartier sous fortes contraintes de délais en maintenant la cohésion de six intervenants techniques. »
  - Juriste : « Je m'en veux d'être partie avant la fin. » → « Mon corps a dit stop après des mois d'alerte. Les décisions de restructuration venaient de la direction, pas de mon investissement. »
  - Ergonome : « Je ne veux plus de stress. » → « Je refuse le reporting quotidien sans valeur ajoutée. Mon prochain cadre devra privilégier l'autonomie et la confiance. »
