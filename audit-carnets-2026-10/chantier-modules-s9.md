# Chantier : les modules « reconversion » et « évolution interne »

Le carnet de route se termine par **le module de votre projet**, choisi en séance 9 selon la piste retenue :
- **création** : le module création (`module-creation.json`, PR R9, 2 h) ;
- **reconversion** : formation et financement, **à créer** ;
- **évolution interne** : argumentaire de repositionnement, **à créer**.

Décision du 8 octobre 2026 : ces deux modules viennent plus tard. Le 9 octobre, une première réflexion a posé leur plan, page par page (sections 4 et 5). Elle attend vos réponses (sections 6 et 7) avant toute écriture dans `workbooks/`.

## 1. Où on en est

- **Prérequis : la fusion de R9.** Le module création a adapté le moteur. Un module du carnet de route déclare `"carnet": "route"` sans déclarer de données, et ses reports citent les pages du carnet de route (`compiler.reference_data_pages`). Les deux modules s'appuient sur ce changement : rien ne commence avant la fusion de R9, et on n'empile pas les branches.
- **Une PR par module**, depuis `main` à jour, dans l'ordre choisi en section 6.
- **Rien n'est écrit** dans `workbooks/` : les plans des sections 4 et 5 sont des propositions.

## 2. Le cadre commun aux deux modules

- **Place.** Carnet de route, partie 2 (S9 → S10), après les pistes A et B et les feuilles de route.
- **Format.** Comme le module création :
  - `"carnet": "route"` (pastel jasmin, folio « carnet de route »), aucun identifiant de données ;
  - une couverture (sourcil « Carnet de route · module reconversion »), une ouverture avec la durée et le découpage, la fin en trois zones et le dos ;
  - fichiers `module-reconversion.json` et `module-evolution-interne.json`, préfixes de champs `reconv_` et `evol_` ;
  - au catalogue, « Bilan de compétences », après le module création.
- **Durée.** Environ 1 h 45 chacun, proposé (section 6, choix 2). Le budget en tient compte :
  - avec le module création (2 h), l'intervalle S9 → S10 passe déjà à 3 h 45 et le total du bilan à 21 h 30, au-dessus des « 1 h 30 à 3 h entre deux séances » et des « 10 à 20 h » du programme ;
  - un module de 1 h 45 donne 3 h 30 et 21 h 15 ;
  - pour tenir 3 h entre les séances, un module doit tenir en 1 h 15.
- **Ce que le programme promet.** Le texte réglementaire (`chapters/programme/page_projets.py`) fixe ce que chaque module doit livrer.
  - Reconversion : « Sécurité financière : vos droits (indemnités, Transitions Pro, maintien de salaire) », « Formation : les seules formations courtes utiles, finançables CPF », « Terrain : enquêtes et immersions » (fait au carnet 7), « Candidature : CV de bifurcation, posture et récit d'entretien convaincant ». Livrable : « Plan d'action sécurisé et enquêtes validées ».
  - Évolution interne : « Travail empêché : repérer précisément ce qui bloque pour redéfinir votre poste », « Négociation : un argumentaire solide pour l'entretien annuel ou la mobilité interne », « Limites : protéger votre charge mentale et rééquilibrer vos horaires », « Pouvoir d'agir : reprendre durablement la main de l'intérieur ». Livrable : « Stratégie de repositionnement interne et plan de négociation ».
  - La première structure du 8 octobre oubliait la candidature (reconversion) et l'évolution du poste actuel (évolution interne). Les plans ci-dessous les intègrent.
- **Reports, sans nouvelle saisie.**

| Donnée | Module reconversion | Module évolution interne |
|---|---|---|
| `route.pistes` | Ex. 1 (piste A), ex. 8 (piste B) | Ex. 1 (piste A), ex. 8 (piste B) |
| `c7.fiches`, `c7.matrice` | Ex. 1 : ce qui me manque, ce qu'il faudrait pour y aller | — |
| `route.competences`, `route.recits` | Ex. 1 (l'écart), ex. 7 (la candidature) | Ex. 3 (vos preuves) |
| `c4.seuils` | Ex. 5, « À garder pour vous » | Ex. 4, « À garder pour vous » |
| `c5.grille` | Ex. 3 (le choix de la formation) | Ex. 4 (ce que je ne négocie pas) |
| `c2.travail_empeche`, `c5.limites` | — | Ex. 1 (ce qui bloque), ex. 4 (horaires, charge) |
| `c7.enquetes` | Ex. 4 (les arguments du dossier) | — |
| `route.feuilles` | Ex. 6 : ce que le calendrier change à la feuille de route | Ex. 8 : ce que le module change à la feuille de route |

- **La trace de la séance 9.** Proposé : déclarer `route.module` sur la carte « Ce que la séance 9 a posé » du carnet de route (exercice 6), et la reporter en tête de chaque module. La personne relit ce qu'elle a noté en séance au lieu de le réécrire. À faire dans la PR du premier module, car R9 modifie aussi cette page.
- **Personnalisation forte** dans l'app : secteur, métier visé, statut de la personne, exemples. Restent fixes : les dispositifs et leurs liens, les encadrés de règles (démission, démarchage, confidentialité), la définition des seuils.
- **Aucun chiffre réglementaire écrit en dur.** Montants, plafonds, délais et conditions changent : le carnet nomme le dispositif, dit quoi vérifier et renvoie à la source officielle.
- **Le gabarit commun.**
  - La durée dans le sourcil.
  - Un exemple contrasté par exercice, d'un métier au nom épicène, absent des carnets et du module création. Pas d'exemple sur un choix qu'il orienterait.
  - La charge moyenne ou le protocole, selon la page.
  - Des cases dimensionnées par la réponse attendue (`"answer": "sentence"`, ou `"sentence"` à la place d'une hauteur), 0,85 cm pour un mot.
  - Un exercice trop long se coupe en deux pages équilibrées (`page_break`), jamais un bloc seul sur la page « (suite) ».

## 3. Ce qui a changé depuis le 8 octobre

La loi n° 2025-989 du 24 octobre 2025 transpose les accords nationaux interprofessionnels sur l'emploi des salariés expérimentés et sur les transitions professionnelles. Elle change deux points de la première structure. Tout est à revérifier au moment de la rédaction, sur les sources officielles.

- **La période de reconversion.** Depuis le 1er février 2026 (décrets du 28 janvier 2026), elle remplace la reconversion ou promotion par alternance (Pro-A), que citait la première structure, et les Transitions collectives.
  - Elle est ouverte à tous les salariés, pour une mobilité interne (le contrat est maintenu) ou externe.
  - Elle demande un accord écrit entre la personne et son employeur.
  - Elle sert aux deux modules : la reconversion, et l'évolution interne qui demande une formation.
- **L'entretien de parcours professionnel.** Il remplace l'entretien professionnel : dans la première année, puis à intervalle régulier, avec des volets sur les compétences, l'évolution, la formation et le CPF. C'est le moment naturel d'une demande d'évolution interne.
- **La démission pour reconversion** (inchangée, à rappeler).
  - Demander un conseil en évolution professionnelle avant de démissionner.
  - Attendre que Transitions Pro valide le caractère réel et sérieux du projet avant d'envoyer la lettre.
  - C'est une règle d'ordre, sans chiffre : un encadré fixe.
- **Le CPF.** Depuis février 2026, il plafonne ses prises en charge selon le type de formation. Les sources consultées se contredisent sur les montants : le carnet n'en écrit aucun et renvoie à Mon Compte Formation.

Sources consultées le 9 octobre 2026 :
- [Centre Inffo · Période de reconversion](https://www.centre-inffo.fr/chapitre/transitions-collectives)
- [Banque des Territoires · les deux décrets](https://www.banquedesterritoires.fr/formation-des-salaries-la-periode-de-reconversion-definie-par-deux-decrets)
- [Centre Inffo · la loi « ANI salariés expérimentés et dialogue social »](https://www.centre-inffo.fr/site-droit-formation/actualites-droit/loi-ani-salaries-experimentes-et-dialogue-social-les-principales-mesures)
- [Legisocial · l'entretien de parcours professionnel](https://www.legisocial.fr/actualites-sociales/7608-reforme-entretien-professionnel-nouvel-entretien-parcours-professionnel.html)
- [Centre Inffo · les démissions pour reconversion](https://www.centre-inffo.fr/site-centre-inffo/les-associations-transitions-pro-verifieront-le-caractere-reel-et-serieux-des-demissions-pour-reconversion)
- [Centre Inffo · le projet de transition professionnelle](https://www.centre-inffo.fr/chapitre/projet-de-transition-professionnelle-mobilisant-le-compte-personnel-de-formation)

## 4. Module reconversion · formation et financement

**But.** Transformer la piste A en un plan de formation finançable et tenable avec les seuils de la personne, puis en une candidature de reconversion. Le principe vient du programme : la formation la plus courte qui ouvre le métier.

**Couverture.** « Changer *de métier.* » Promesse : « Une formation choisie, financée, tenable. »

**Plan : 13 pages, environ 1 h 45.**

| Page | Contenu | Durée |
|---|---|---|
| 1 | Couverture | |
| 2 | Ouverture : ce qui se montre (la candidature), ce qui reste à vous (les seuils, le budget) | |
| 3 | Exercice 1 · Ce que demande le métier | 15 min |
| 4 | Exercice 2 · Le chemin le plus court | 5 min |
| 5 | Exercice 3 · Vos formations repérées | 20 min |
| 6-7 | Exercice 4 · Le financement | 15 min |
| 8 | Exercice 5 · Tenir pendant la formation | 10 min |
| 9 | Exercice 6 · Votre calendrier | 10 min |
| 10 | Exercice 7 · Votre candidature | 15 min |
| 11 | Exercice 8 · Garde-fous et décision | 10 min |
| 12 | Fin du module | 5 min |
| 13 | Dos | |

**Exercice par exercice**
1. **Ce que demande le métier.**
   - Reports : la piste A et la trace de la séance 9, « ce qui me manque » (fiche du carnet 7) et « ce qu'il faudrait pour y aller » (matrice).
   - Le diplôme, en une ligne : « Obligatoire / Attendu / Inutile / À vérifier ». Puis le diplôme, le titre ou la certification, et sa source (fiche métier, offre d'emploi, personne rencontrée).
   - L'écart : trois compétences prouvées (report) qui servent au métier, trois à acquérir.
   - Liens fixes : les fiches métiers de France Travail, le répertoire de France compétences.
2. **Le chemin le plus court.** Page fixe.
   - Quatre cartes : sans formation (immersion, passerelle, candidature directe), formation courte (Répertoire spécifique), certification longue (RNCP), validation des acquis de l'expérience.
   - Un choix en mots, « Direct / Court / Certifiant / VAE », puis « Parce que… ».
   - Pas d'exemple : il orienterait le choix.
3. **Vos formations repérées.**
   - Un tableau de trois colonnes : l'organisme et l'intitulé, la certification visée et son enregistrement vérifié, la durée, le rythme et le format, le coût et les dates, les résultats publiés, ce qu'en disent des personnes qui l'ont suivie.
   - Puis la formation retenue face aux trois valeurs (report), et pourquoi.
   - Encadré fixe sur le démarchage : personne n'a à vous appeler pour votre CPF, et on ne donne jamais ses identifiants.
   - Les appels aux organismes se font hors temps d'écriture.
4. **Le financement** (deux pages).
   - Quatre cartes fixes selon la situation. En poste dans le privé : CPF, projet de transition professionnelle, période de reconversion, plan de développement des compétences, démission pour reconversion. En recherche d'emploi : CPF, aides de France Travail, région. À votre compte : CPF, fonds d'assurance formation de la profession. Dans la fonction publique : à écrire avec vous (section 7). La liste exacte est à vérifier à la rédaction.
   - Un tableau « Le dispositif · ce que je dois vérifier · auprès de qui · fait le ».
   - L'encadré fixe « Avant toute démission ».
   - Un renvoi aux enquêtes du carnet 7, qui nourrissent un dossier de financement.
   - Liens : Mon Compte Formation, Transitions Pro, le conseil en évolution professionnelle, France Travail.
5. **Tenir pendant la formation.**
   - Les seuils en « À garder pour vous ».
   - Mon revenu pendant la formation (une case, en euros nets par mois) et la durée de la formation (en mois).
   - Deux lignes, « Oui / Juste / Non / À vérifier » : mon revenu atteint mon minimum sécurisant ; la formation tient dans ma durée acceptable d'une baisse.
   - « Si c'est trop juste, ce que j'ajuste » : le rythme, le temps partiel, la date, l'épargne, une aide.
   - Charge moyenne : la question franche facultative « Ce qui m'inquiète le plus dans le fait de reprendre une formation », puis une clôture.
6. **Votre calendrier.**
   - On part de la date d'entrée en formation, et on remonte : le conseil en évolution professionnelle, le dossier déposé, la réponse attendue, l'immersion si elle n'est pas faite, l'entrée en formation, le stage ou l'alternance, la certification, le premier poste.
   - Un tableau « Étape · date visée · ce qui en dépend ».
   - Le report de la feuille de route, piste A, et « Ce que ce calendrier change à ma feuille de route ».
7. **Votre candidature.**
   - Reports : les récits (« ce récit prouve que je sais… ») et deux compétences prouvées.
   - Le titre de CV : le métier visé, pas l'ancien.
   - La phrase de reconversion, en trois temps : d'où je viens, ce que j'emporte, où je vais.
   - Trois compétences transférables et leur preuve.
   - La question redoutée en entretien, et ma réponse.
8. **Garde-fous et décision.**
   - Ce qui me ferait reporter ou renoncer (un financement refusé, une formation complète, un revenu trop juste), et ma réponse.
   - La piste B (report).
   - Ma décision : « Je me lance / Je vérifie / Je modifie / En pause », puis « Parce que… ».

**Fin du module.** Livrable : « Votre plan de formation et de financement » (exercices 3 à 6), relu en séance 10. Parmi les trois zones : « À aborder en séance : un dossier, une date, un chiffre dont je doute ».

## 5. Module évolution interne · argumentaire de repositionnement

**But.** Préparer une demande d'évolution dans l'entreprise actuelle, fondée sur des preuves : un autre poste, des missions en plus ou en moins, ou une autre organisation du travail (horaires, télétravail, charge).

**Couverture.** « Évoluer *de l'intérieur.* » Promesse : « Une demande préparée, des preuves, un plan d'échanges. »

**Plan : 13 pages, environ 1 h 40.**

| Page | Contenu | Durée |
|---|---|---|
| 1 | Couverture | |
| 2 | Ouverture : la confidentialité du bilan (section 6, choix 4), ce qui se montre (l'argumentaire), ce qui reste à vous (les seuils, le point de repli, les interlocuteurs) | |
| 3-4 | Exercice 1 · Ce qui bloque, ce que vous demandez | 15 min |
| 5 | Exercice 2 · Ce que l'entreprise y gagne | 10 min |
| 6 | Exercice 3 · Vos preuves | 15 min |
| 7 | Exercice 4 · Vos conditions | 15 min |
| 8 | Exercice 5 · Vos interlocuteurs, le bon moment | 10 min |
| 9 | Exercice 6 · Votre plan d'échanges | 10 min |
| 10 | Exercice 7 · Les objections | 10 min |
| 11 | Exercice 8 · Si la réponse est non | 10 min |
| 12 | Fin du module | 5 min |
| 13 | Dos | |

**Exercice par exercice**
1. **Ce qui bloque, ce que vous demandez** (deux pages).
   - Reports : le travail empêché (« pour faire un travail que je juge bien fait, j'ai besoin de… ») et la limite au travail.
   - Ce qui bloque aujourd'hui, sur une situation récente. Ce qui dépend de moi, ce qui dépend de l'organisation : deux cases.
   - La demande : « Un poste / Des missions / Mon rythme / Un mélange ». Puis l'intitulé ou le périmètre visé, ce qui change par rapport à aujourd'hui, ce que je garde, ce que je propose de transmettre.
2. **Ce que l'entreprise y gagne.**
   - Le besoin ou le problème que ma demande résout, et pour qui.
   - Ce que coûte à l'entreprise de ne rien changer.
   - Ce que je sais de ses priorités du moment, et d'où je le sais.
3. **Vos preuves.**
   - Reports : les compétences prouvées et les récits.
   - Un tableau de trois lignes : le besoin (exercice 2), ma preuve (une compétence, un récit), ce qu'elle a donné (un résultat, une trace).
4. **Vos conditions.**
   - Reports : les seuils en « À garder pour vous », les trois valeurs et leurs conditions, les limites au travail.
   - La rémunération que je demande, et mon point de repli : deux cases d'une ligne.
   - L'organisation : horaires, télétravail, charge.
   - Ce que je ne négocie pas, ce que je peux céder.
   - Lien : la convention collective et ses grilles (Code du travail numérique).
5. **Vos interlocuteurs, le bon moment.**
   - Un tableau : qui décide, qui influence, qui soutient, qui freine, et ce qui compte pour chaque personne.
   - Cartes fixes des moments : l'entretien de parcours professionnel, l'entretien annuel, un poste ouvert, un besoin nouveau (un départ, un projet).
   - Encadré fixe : si l'évolution demande une formation, la période de reconversion en mobilité interne, le plan de développement des compétences, le CPF.
6. **Votre plan d'échanges.**
   - Le moment choisi, et pourquoi.
   - La demande de rendez-vous : à qui, avec quel objet. Un message type, fixe.
   - L'argumentaire en trois phrases : le besoin, ma proposition, ce que je demande.
   - Une note : le dire à voix haute avant le rendez-vous.
7. **Les objections.** Un tableau de trois lignes : l'objection que j'attends, la crainte qu'elle exprime, ma réponse et ma preuve. Exemple contrasté sur « Ce n'est pas le moment ».
8. **Si la réponse est non.**
   - Quand reposer la question, et à quelle condition. Ce qui me fera passer à la piste B (report).
   - Encadré fixe si la demande est mal reçue : à qui en parler (section 6, choix 6).
   - Charge moyenne : la question franche facultative « Ce que je crains le plus dans cette démarche », puis une clôture.
   - Ma décision : « Je demande / Je prépare / Je modifie / En pause », puis « Parce que… » et « Ce que le module change à ma feuille de route » (report).

**Fin du module.** Livrable : « Votre argumentaire et votre plan d'échanges » (exercices 2, 3, 6 et 7), relu en séance 10. Parmi les trois zones : « À aborder en séance : la réaction que je redoute, ce que je n'ose pas demander ».

## 6. Choix à trancher

Chaque choix porte une proposition. Sans réponse de votre part, c'est elle qui s'applique.

1. **L'ordre.** Une PR par module, après R9. Lequel d'abord dépend de la part de chaque situation (section 7). Proposé, à défaut : l'évolution interne, qui n'a rien de réglementaire à vérifier.
2. **La durée.** Proposé : 1 h 45 et 1 h 40, proches des 2 h d'une création. Autre voie : 1 h 15, pour tenir 3 h entre les séances 9 et 10. On retirerait alors la candidature (reconversion), et on fusionnerait les interlocuteurs et le plan d'échanges (évolution interne).
3. **L'évolution du poste actuel** (missions, horaires, charge) entre dans le module évolution interne, comme le promet le programme. Proposé : oui.
4. **La confidentialité.** Texte proposé pour l'ouverture du module évolution interne : « Votre bilan vous appartient : ses résultats ne se communiquent qu'avec votre accord. Vous n'avez pas à en parler pour faire votre demande. Si vous le faites, dites ce que vous en retirez, pas ce qu'il contient. » À valider, surtout quand l'employeur finance le bilan, et à vérifier dans le Code du travail.
5. **La négociation.** Proposé : la préparation (conditions, point de repli, objections, plan d'échanges), sans script de négociation salariale.
6. **Une demande mal reçue.** Proposé : un encadré fixe qui dit à qui en parler (les ressources humaines, les représentants du personnel, le service de prévention et de santé au travail), sans conseil juridique. À valider : la liste.
7. **La charge émotionnelle.** Proposé : la charge moyenne (question franche facultative, puis une clôture) sur « Tenir pendant la formation » et « Si la réponse est non », sans protocole complet. Le module création met le protocole complet sur le risque, parce qu'il touche l'argent du foyer : à harmoniser si vous le préférez.
8. **Les dossiers.** Proposé : pas de trame de dossier ni de lettre de motivation. Le module renvoie au conseil en évolution professionnelle et à Transitions Pro, et rappelle que les enquêtes du carnet 7 nourrissent le dossier.
9. **La VAE.** Proposé : un des quatre chemins de l'exercice 2, pas un module à part.
10. **La trace de la séance 9.** Proposé : `route.module`, déclaré au carnet de route et reporté en tête des modules.
11. **Un seul module par personne**, celui de la piste A. Proposé : oui. Une piste B en évolution interne, refuge fréquent, reste traitée au carnet de route.

## 7. Ce dont j'ai encore besoin de votre part

Les questions du 8 octobre ont, pour la plupart, une proposition en section 6. Restent ouvertes :
1. **Votre pratique en séance 9** pour ces deux cas : les questions posées, les outils, ce que la personne doit avoir en sortant. Ce qui se prépare seul, et ce qui ne se travaille qu'ensemble.
2. **La part des situations** parmi vos bénéficiaires : reconversions, évolutions internes. Elle décide de l'ordre (choix 1).
3. **Les statuts que vous rencontrez**, en particulier la fonction publique : sa carte de financement s'écrit avec vous.
4. **Les dispositifs que vous mobilisez vraiment**, ceux que vous déconseillez, et pourquoi.
5. **Vos sources de confiance** : sites officiels, bases de formations, interlocuteurs. Je vérifierai chaque lien et chaque nom de dispositif à la rédaction.
6. **Les moments que vous recommandez** pour une demande d'évolution, au-delà de l'entretien de parcours professionnel et de l'entretien annuel.

Les situations types anonymisées deviennent facultatives : les exemples contrastés s'écrivent sur des métiers variés, comme pour les carnets, sans profil réel. Métiers épicènes encore libres, à vérifier : standardiste, ostéopathe, fiscaliste, ascensoriste, barista, géographe, accessoiriste, audioprothésiste.

## 8. Comment on les créera

1. Vous répondez aux sections 6 et 7, par écrit ou en vrac dans une conversation.
2. Une fois R9 fusionnée, je rédige le premier module dans `workbooks/`, en vérifiant les sources officielles, avec la méthode des carnets : plan validé, rendu page par page, mesure de la place libre, relecture de l'audit.
3. Vous le relisez, Lysiane et vous, et vous testez sa personnalisation dans l'app sur des profils types. Puis vient le second module.

**Autre voie :** les créer d'abord dans l'app à partir de vos notes, puis exporter le JSON. Dans ce cas, je relis le fichier (ton, sources, gabarit commun) avant de l'intégrer.
