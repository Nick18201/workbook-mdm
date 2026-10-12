# Chantier : les modules « reconversion » et « évolution interne »

Le carnet de route se termine par **le module de votre projet**, choisi en séance 9 selon la piste retenue :
- **création** : le module création (`module-creation.json`, R9, 2 h) ;
- **reconversion** : formation et financement (`module-reconversion.json`, 1 h 45) ;
- **évolution interne** : argumentaire de repositionnement (`module-evolution-interne.json`, 1 h 45).

Décision du 8 octobre 2026 : ces deux modules viennent plus tard. Le 9 octobre, une première réflexion a posé leur plan, page par page, et onze choix avec une proposition par défaut. Le 12 octobre, à la demande de Nicolas (« un draft abouti des deux autres modules »), les deux modules sont rédigés dans `workbooks/` avec ces propositions par défaut. Ce document décrit ce qui est écrit (sections 4 et 5), ce qui a été tranché et comment (section 6), et ce qui attend encore vos réponses (section 7).

## 1. Où on en est

- **Les deux brouillons sont aboutis** : ils se génèrent, passent le contrôle de conformité et les tests, et l'app les propose à la personnalisation (catalogue « Bilan de compétences », après le module création). Reconversion : 12 pages de spec, 19 pages de PDF. Évolution interne : 13 pages de spec, 18 pages de PDF.
- **Une seule PR pour les deux** (branche `claude/modules-reconversion-evolution`), et non une par module comme prévu : les deux touchent la même page du carnet de route (la carte des modules, la trace de la séance 9), et deux PR auraient dû s'empiler.
- **Le carnet de route change sur une page** (exercice 6, « Le module de votre projet ») : les cartes « Se reconvertir » et « Évoluer » annoncent les modules et leur durée, et la carte « Ce que la séance 9 a posé » déclare `route.module`.
- **Ce qui reste** : vos réponses à la section 7, une relecture des textes réglementaires par vous et Lysiane, et un essai de la personnalisation avec la vraie clé Gemini (deux parties par module, de l'ordre de 60 000 jetons pour les deux d'après les mesures du module création : à chiffrer et annoncer avant).

## 2. Le cadre commun aux deux modules

- **Place.** Carnet de route, partie 2 (S9 → S10), après les pistes A et B et les feuilles de route.
- **Format.** Comme le module création :
  - `"carnet": "route"` (pastel jasmin, folio « carnet de route »), aucun identifiant de données ;
  - une couverture (sourcil « Carnet de route · module reconversion »), une ouverture avec la durée et le découpage, la fin en trois zones et le dos ;
  - préfixes de champs `reconv_` et `evol_` ;
  - deux parties chacun, pour que l'app les personnalise en deux appels : « Choisir et financer votre formation » puis « Tenir, planifier, candidater » ; « Préparer votre demande » puis « Porter votre demande » ;
  - un script CLI chacun (`Scripts/main_generate_module_reconversion.py`, `main_generate_module_evolution_interne.py`), construit par la CI.
- **Durée.** 1 h 45 chacun (section 6, choix 2). Avec l'un d'eux, l'intervalle S9 → S10 passe à 3 h 30 et le total du bilan à 21 h 15, au-dessus des « 1 h 30 à 3 h entre deux séances » et des « 10 à 20 h » du programme. Le programme ne le dit que pour la création (PR #69) : à étendre aux trois modules si vous le décidez.
- **Ce que le programme promet** (`Scripts/workbook_generator/chapters/programme/page_projets.py`), et où les modules le tiennent :

| Promesse du programme | Module reconversion |
|---|---|
| Sécurité financière : vos droits (indemnités, Transitions Pro, maintien de salaire) | Exercices 4 (le financement, « Avant toute démission ») et 5 (tenir pendant la formation) |
| Formation : les seules formations courtes utiles, finançables CPF | Exercices 1 à 3 (l'écart, le chemin le plus court, les formations comparées) |
| Terrain : enquêtes et immersions | Carnet 7 ; le module reporte ce qui manque et la matrice, cite les enquêtes pour le dossier de financement, place l'immersion au calendrier |
| Candidature : CV de bifurcation, posture et récit d'entretien | Exercice 7 (titre de CV, phrase de reconversion, compétences transférables, la question redoutée) |
| Livrable : plan d'action sécurisé et enquêtes validées | « Votre plan d'action sécurisé » (exercices 2 à 7) |

| Promesse du programme | Module évolution interne |
|---|---|
| Travail empêché : repérer ce qui bloque pour redéfinir votre poste | Exercice 1 (le travail empêché du carnet 2 reporté, une situation récente, la demande) |
| Négociation : un argumentaire pour l'entretien annuel ou la mobilité interne | Exercices 2, 3, 6 et 7 (ce que l'entreprise y gagne, les preuves, le plan d'échanges, les objections) |
| Limites : charge mentale, horaires | Exercices 1 (la limite du carnet 5 reportée) et 4 (mon organisation : ce que je ne négocie pas, ce que je peux céder) |
| Pouvoir d'agir : reprendre la main de l'intérieur | Exercices 5 et 8 (le bon moment, si la réponse est non, la décision) |
| Livrable : stratégie de repositionnement interne et plan de négociation | « Votre argumentaire et votre plan de négociation » |

- **Reports, sans nouvelle saisie.**

| Donnée | Module reconversion | Module évolution interne |
|---|---|---|
| `route.pistes` | Ex. 1 (piste A), ex. 8 (piste B) | Ex. 1 (piste A), ex. 8 (piste B) |
| `route.module` (nouveau) | Ex. 1 : ce que la séance 9 a posé | Ex. 1 : ce que la séance 9 a posé |
| `c7.fiches`, `c7.matrice` | Ex. 1 : ce qui me manque, ce qu'il faudrait pour y aller | — |
| `c5.grille` | Ex. 3 (le choix de la formation) | Ex. 4 (vos conditions) |
| `c4.seuils` | Ex. 5, « À garder pour vous » | Ex. 4, « À garder pour vous » |
| `c2.travail_empeche`, `c5.limites` | — | Ex. 1 (ce qui bloque) |
| `route.feuilles` | Ex. 6 : ce que le calendrier change à la feuille de route | Ex. 8 : ce que le module change à la feuille de route |
| `route.competences`, `route.recits` | Ex. 7, par un renvoi écrit (la colonne « preuve » des compétences transférables) | Ex. 3, par un renvoi écrit (la colonne « preuve ») |
| `c7.enquetes` | Ex. 4, par un renvoi écrit (elles nourrissent un dossier de financement) | — |

- **Personnalisation forte** dans l'app (`PERSONALIZATION_RULES` : « carnet de route et ses modules ») : secteur, métier visé, statut, exemples. Restent fixes : les dispositifs et leurs liens, les encadrés de règles (démission, démarchage, confidentialité, demande mal reçue), les cartes par situation et des bons moments, la page du chemin le plus court, l'annonce et l'ancrage, les questions franches, les décisions.
- **Aucun chiffre réglementaire écrit en dur.** Ni montant, ni plafond, ni délai, ni périodicité : le module nomme le dispositif, dit quoi vérifier et renvoie à la source officielle.
- **Le gabarit commun** : la durée dans chaque sourcil, un exemple contrasté par exercice (sauf le chemin le plus court, qui orienterait le choix), d'un métier au nom épicène absent des autres documents, des cases dimensionnées par la réponse attendue, des exercices coupés en deux pages équilibrées.

## 3. Ce qui a changé depuis le 8 octobre (vérifié le 12 octobre)

La loi n° 2025-989 du 24 octobre 2025 transpose les accords nationaux interprofessionnels sur l'emploi des salariés expérimentés et sur les transitions professionnelles.

- **La période de reconversion.** Depuis le 1er février 2026, elle remplace la reconversion ou promotion par alternance (Pro-A) et les Transitions collectives. Ouverte à tous les salariés, pour une mobilité interne (le contrat continue) ou externe (le contrat est suspendu), elle demande un accord écrit entre la personne et son employeur ; l'opérateur de compétences finance la formation, le CPF peut s'y ajouter avec l'accord de la personne. Le module reconversion la cite dans la carte « En poste », le module évolution interne dans l'encadré « Si votre évolution demande une formation ». Les durées de formation (minimum et maximum) ne sont pas écrites.
- **L'entretien de parcours professionnel.** Il remplace l'entretien professionnel (article L6315-1) : dans la première année, puis à intervalle régulier, sur les compétences, le parcours, la formation et les souhaits d'évolution ; il n'évalue pas le travail. Le module évolution interne en fait la première carte des bons moments, sans sa périodicité.
- **La démission pour reconversion.** Inchangée : un CDI de droit privé, une durée d'activité minimale, un conseil en évolution professionnelle demandé avant la démission, puis l'attestation de Transitions Pro sur le caractère réel et sérieux du projet. L'encadré fixe « Avant toute démission » donne l'ordre et renvoie à demission-reconversion.gouv.fr, sans chiffre.
- **Le CPF.** Depuis 2026, ses prises en charge sont plafonnées selon le type de formation, et une participation forfaitaire est demandée (relevée en avril 2026), avec des exceptions. Les sources se contredisent encore sur les plafonds : le module n'écrit aucun montant et renvoie à Mon Compte Formation.
- **Le démarchage pour le CPF** est interdit depuis la loi du 19 décembre 2022 : un encadré fixe le dit, avec « ne donnez jamais vos identifiants ».
- **La confidentialité du bilan** : l'article L6313-10 du Code du travail fait de la personne la seule destinataire des résultats détaillés et du document de synthèse, qui ne sont communiqués à un tiers qu'avec son accord. Pour un agent de l'État, une convention type prévoit au contraire que le document de synthèse est communicable aux ressources humaines, sauf opposition expresse (section 7, question 7).

Sources consultées le 9 et le 12 octobre 2026 :
- [Code du travail numérique · la période de reconversion](https://code.travail.gouv.fr/fiche-ministere-travail/la-periode-de-reconversion)
- [Centre Inffo · Période de reconversion](https://www.centre-inffo.fr/chapitre/transitions-collectives)
- [Banque des Territoires · les deux décrets](https://www.banquedesterritoires.fr/formation-des-salaries-la-periode-de-reconversion-definie-par-deux-decrets)
- [Code du travail numérique · article L6315-1](https://code.travail.gouv.fr/code-du-travail/l6315-1)
- [France Travail · démissionner pour un projet de reconversion](https://www.francetravail.fr/candidat/mes-droits-aux-aides-et-allocati/a-chaque-situation-son-allocatio/quelle-est-ma-situation-professi/je-perds-ou-je-quitte-un-emploi/je-veux-demissionner-et-jai-un-p.html)
- [Centre Inffo · les démissions pour reconversion](https://www.centre-inffo.fr/site-centre-inffo/les-associations-transitions-pro-verifieront-le-caractere-reel-et-serieux-des-demissions-pour-reconversion)
- [Centre Inffo · le projet de transition professionnelle](https://www.centre-inffo.fr/chapitre/projet-de-transition-professionnelle-mobilisant-le-compte-personnel-de-formation)
- [Service-public · formation professionnelle, participation au CPF](https://www.service-public.gouv.fr/particuliers/actualites/A17364?lang=fr)
- [France compétences · recherche de certifications](https://www.francecompetences.fr/recherche-resultats/)

Les adresses des modules répondent toutes le 12 octobre 2026 : Mon Compte Formation, Transitions Pro, mon-cep.org, France Travail (« En formation »), MétierScope, France compétences, France VAE, le Code du travail numérique (convention collective). demission-reconversion.gouv.fr est cité en texte : il parle encore de « pôle emploi ».

## 4. Module reconversion · formation et financement

**But.** Transformer la piste A en un plan de formation finançable et tenable avec les seuils de la personne, puis en une candidature de reconversion. Le principe vient du programme : la formation la plus courte qui ouvre le métier.

**Couverture.** « Changer *de métier.* » Promesse : « Une formation choisie, financée, tenable. » **Ouverture** : « De votre piste *à votre métier.* » Ce qui se montre : le plan et la candidature ; ce qui reste à vous : les seuils et le budget.

| Page du PDF | Exercice | Durée |
|---|---|---|
| 1-2 | Couverture, ouverture | |
| 3-4 | 1 · Ce que demande le métier | 15 min |
| 5 | 2 · Le chemin le plus court (page fixe) | 5 min |
| 6-7 | 3 · Vos formations repérées | 15 min |
| 8-9 | 4 · Votre financement | 15 min |
| 10-11 | 5 · Tenir pendant la formation | 15 min |
| 12-13 | 6 · Votre calendrier | 10 min |
| 14-15 | 7 · Votre candidature | 15 min |
| 16-17 | 8 · Garde-fous et décision | 10 min |
| 18-19 | Fin du module, dos | 5 min |

**Exercice par exercice.**
1. **Ce que demande le métier.** Reports : la piste A, ce que la séance 9 a posé, « ce qui me manque » (fiche du carnet 7), « pour y aller, il faudrait… » (matrice). Le diplôme en une ligne : « Obligatoire / Attendu / Inutile / À vérifier », puis lequel et sa source. Liens : MétierScope, France compétences. Puis l'écart : trois compétences, ce que je sais déjà faire (et sa preuve), ce qu'il me reste à acquérir, et la compétence qui manque le plus. Exemple : audioprothésiste.
2. **Le chemin le plus court.** Page fixe, sans exemple. Quatre cartes : sans formation, une formation courte (Répertoire spécifique, bloc de compétences), une certification (RNCP), la VAE. Le choix « Direct / Court / Certifiant / VAE », puis « Parce que… ». Lien : France VAE.
3. **Vos formations repérées** (« Comparer, *puis choisir.* »). Un tableau de trois formations sur six lignes : l'organisme et l'intitulé, la certification et son enregistrement vérifié, la durée et le rythme, le coût et les dates, les résultats publiés, ce qu'en disent des personnes qui l'ont suivie. Exemple : barista. Puis les trois valeurs et leurs conditions (reports), la formation retenue, pourquoi, ce qu'il reste à vérifier. Encadré fixe « Démarchage ».
4. **Votre financement.** Quatre cartes fixes par situation : en poste dans le privé (CPF, projet de transition professionnelle, période de reconversion, plan de formation de l'entreprise), en recherche d'emploi (CPF, aides de France Travail et allocation pendant une formation validée, région), à votre compte (CPF, fonds d'assurance formation), dans la fonction publique (CPF, congé de formation professionnelle, plan de formation de l'administration, à préciser avec vous). Encadré fixe « Avant toute démission ». Les enquêtes du carnet 7 nourrissent le dossier. Puis un tableau « Le dispositif · Ce que je dois vérifier · Auprès de qui · Fait le ». Exemple : cartographe. Liens : Mon Compte Formation, Transitions Pro, le conseil en évolution professionnelle, France Travail.
5. **Tenir pendant la formation.** Annonce (`protocol`) : la page parle du revenu et du foyer. Les seuils en « À garder pour vous », le revenu pendant la formation, d'où il vient et sa durée, deux lignes « Oui / Juste / Non / À vérifier » (minimum sécurisant, durée acceptable). Puis « Si c'est trop juste, ce que j'ajuste », exemple (ascensoriste), deux questions franches (ce qui m'inquiète le plus, ce qu'en pense la personne qui partage ma vie) et l'ancrage.
6. **Votre calendrier, à rebours.** Un tableau fixe de huit étapes (conseil en évolution professionnelle, dossier, réponse, immersion, entrée, stage, certification, premier poste), la date visée et auprès de qui. Exemple : accessoiriste. Puis l'étape dont tout dépend, les objectifs de la feuille de route (report) et ce que le calendrier y change.
7. **Votre candidature.** Renvoi écrit aux compétences prouvées et aux récits. Le titre du CV (le métier visé), la phrase de reconversion en trois temps (d'où je viens, ce que j'emporte, où je vais), exemple (fiscaliste), trois compétences transférables avec leur preuve et ce qu'elles apportent, la question redoutée en entretien et la réponse, à dire à voix haute.
8. **Garde-fous et décision.** Un tableau « Si… · Ma réponse » (financement refusé, formation complète, revenu trop juste, un autre aléa), exemple (ostéopathe), la piste B (report), le signal qui y fera passer, la décision « Je me lance / Je vérifie / Je modifie / En pause » et « Parce que… ».

**Fin du module.** Livrable : « Votre plan d'action sécurisé » (exercices 2 à 7), relu en séance 10, puis le livret de compétences pour aller plus loin. Engagements : vérifier chaque dispositif à sa source, déposer le dossier à la date fixée, garder la piste B ouverte jusqu'à la réponse. Zone : « À aborder en séance : un dossier, une date, un dispositif dont je doute ».

## 5. Module évolution interne · argumentaire de repositionnement

**But.** Préparer une demande d'évolution dans l'entreprise actuelle, fondée sur des preuves : un autre poste, des missions en plus ou en moins, ou une autre organisation du travail (horaires, télétravail, charge).

**Couverture.** « Évoluer *de l'intérieur.* » Promesse : « Une demande préparée, des preuves, un plan d'échanges. » **Ouverture** : « Préparer *votre demande.* » Ce qui se montre : l'argumentaire ; ce qui reste à vous : les seuils, le point de repli, les interlocuteurs.

| Page du PDF | Exercice | Durée |
|---|---|---|
| 1-2 | Couverture, ouverture | |
| 3-4 | 1 · Ce qui bloque, ce que vous demandez | 15 min |
| 5 | 2 · Ce que l'entreprise y gagne | 10 min |
| 6 | 3 · Vos preuves | 15 min |
| 7-8 | 4 · Vos conditions | 15 min |
| 9-10 | 5 · Vos interlocuteurs, le bon moment | 10 min |
| 11-12 | 6 · Votre plan d'échanges | 10 min |
| 13 | 7 · Les objections | 10 min |
| 14-16 | 8 · Si la réponse est non (10 min), votre décision (5 min) | 15 min |
| 17-18 | Fin du module, dos | 5 min |

**Exercice par exercice.**
1. **Ce qui bloque, ce que vous demandez.** Reports : la piste A, ce que la séance 9 a posé, « pour bien travailler, j'ai besoin de… » (travail empêché, carnet 2), la limite au travail (carnet 5). Une situation récente, ce qui dépend de moi, ce qui dépend de l'organisation. Puis exemple (gestionnaire de paie), la demande « Un poste / Des missions / Mon rythme / Un mélange », l'intitulé ou le périmètre, ce qui change, ce que je garde, ce que je propose de transmettre ou d'arrêter, pour quand.
2. **Ce que l'entreprise y gagne.** Exemple (responsable qualité). Le besoin que la demande règle et pour qui, ce que coûte de ne rien changer, les priorités de l'entreprise et d'où je les connais.
3. **Vos preuves.** Renvoi écrit aux compétences prouvées et aux récits. Un tableau de trois lignes : le besoin, ma preuve, ce qu'elle a donné. Exemple (cuisiniste). La preuve qui manque encore, et comment l'obtenir avant le rendez-vous.
4. **Vos conditions.** « Si vous montrez ce module, masquez cette page. » Reports en « À garder pour vous » : minimum sécurisant, revenu cible, les trois valeurs et leurs conditions. La rémunération demandée et le point de repli, le salaire observé et sa source. Lien : la convention collective (Code du travail numérique). Puis mon organisation (horaires, charge, télétravail ; ce que je ne négocie pas, ce que je peux céder), exemple (prothésiste dentaire), « Si j'obtiens le poste, mais pas mes conditions, je… ».
5. **Vos interlocuteurs, le bon moment** (« Qui convaincre, *et quand.* »). Un tableau : qui décide, qui influence, qui soutient, qui peut freiner, et ce qui compte pour chacun. Exemple (standardiste). Quatre cartes fixes des bons moments : l'entretien de parcours professionnel, l'entretien annuel, un poste ouvert, un besoin nouveau. Le moment choisi et pourquoi. Encadré fixe « Si votre évolution demande une formation » (période de reconversion, plan de formation, CPF).
6. **Votre plan d'échanges.** Les échanges informels avant le rendez-vous (avec qui, pour quoi faire, quand), la demande de rendez-vous (à qui, l'objet, avec un message type en aide), l'encadré fixe « Votre bilan » (confidentialité, section 6, choix 4). Puis l'argumentaire en trois phrases (le besoin, ma proposition, ce que je demande), exemple (orthoptiste), « Si l'on me demande « pourquoi maintenant ? », je réponds… », à dire à voix haute.
7. **Les objections.** Quatre objections fréquentes citées, exemple (podologue) sur « Ce n'est pas le moment », puis un tableau de trois lignes : l'objection, la crainte qu'elle exprime, ma réponse et ma preuve.
8. **Si la réponse est non, votre décision.** La piste B (report), quand reposer la question et à quelle condition, le signal qui fera passer à la piste B. Encadré fixe « Si votre demande est mal reçue ». Exemple (géographe). Charge moyenne : « Ce que je crains le plus dans cette démarche », « La réaction que je redoute », puis la clôture « Pour mener cette démarche, je m'appuie sur… ». Puis la page de décision : les objectifs de la feuille de route (report), ce que le module y change, « Je demande / Je prépare / Je modifie / En pause » et « Parce que… ».

**Fin du module.** Livrable : « Votre argumentaire et votre plan de négociation » (exercices 2, 3, 6 et 7), relu en séance 10, puis le livret de compétences pour aller plus loin. Engagements : demander le rendez-vous à la date fixée, appuyer chaque demande sur une preuve, protéger ses horaires et sa charge pendant la démarche. Zone : « À aborder en séance : la réaction que je redoute, ce que je n'ose pas demander ».

## 6. Les choix, et ce qui a été appliqué

Le 9 octobre, chaque choix portait une proposition, à appliquer sans réponse de votre part. Le 12 octobre, elles sont appliquées, avec trois écarts signalés.

1. **L'ordre.** Proposé : une PR par module, l'évolution interne d'abord. **Appliqué autrement** : les deux modules dans une seule PR (section 1).
2. **La durée.** Proposé : 1 h 45 et 1 h 40. **Appliqué** : 1 h 45 chacun ; la décision de l'évolution interne a pris sa propre page (5 min). Autre voie, toujours possible : 1 h 15, pour tenir 3 h entre les séances 9 et 10, en retirant la candidature (reconversion) et en fusionnant les interlocuteurs et le plan d'échanges (évolution interne).
3. **L'évolution du poste actuel** (missions, horaires, charge) entre dans le module évolution interne. **Appliqué** (« Mon rythme », « Mon organisation »).
4. **La confidentialité.** **Appliqué**, dans un encadré fixe de l'exercice 6 plutôt qu'à l'ouverture (la personnalisation ne touche pas un encadré fixe) : « Votre bilan vous appartient : ses résultats ne sont communiqués à personne sans votre accord. Vous n'avez pas à en parler pour faire votre demande. Si vous le faites, dites ce que vous en retirez, pas ce qu'il contient. » Conforme à l'article L6313-10 ; voir la section 7, question 7, pour la fonction publique.
5. **La négociation.** **Appliqué** : la préparation (conditions, point de repli, objections, plan d'échanges), sans script de négociation salariale.
6. **Une demande mal reçue.** **Appliqué** : un encadré fixe qui dit à qui en parler (les ressources humaines, les représentants du personnel, le service de prévention et de santé au travail, et la séance), sans conseil juridique.
7. **La charge émotionnelle.** **Appliqué autrement pour la reconversion** : « Tenir pendant la formation » parle de l'argent du foyer, comme le risque du module création ; depuis la charte v2, l'annonce est une phrase factuelle et l'ancrage une case : la page prend les deux, harmonisée avec le module création. « Si la réponse est non » garde la charge moyenne (les questions franches et leur clôture, fixes), sans « facultatif » (charte v2).
8. **Les dossiers.** **Appliqué** : pas de trame de dossier ni de lettre de motivation. Le module renvoie au conseil en évolution professionnelle et à Transitions Pro, et rappelle que les enquêtes du carnet 7 nourrissent le dossier.
9. **La VAE.** **Appliqué** : un des quatre chemins de l'exercice 2, avec le lien France VAE.
10. **La trace de la séance 9.** **Appliqué** : `route.module`, déclaré sur la carte « Ce que la séance 9 a posé » du carnet de route, reporté en tête des deux modules. Le module création ne le reporte pas.
11. **Un seul module par personne**, celui de la piste A. **Appliqué** : la piste B est reportée et sert de garde-fou, sans module.

## 7. Ce dont j'ai encore besoin de votre part

Les brouillons répondent par défaut ; vos réponses les ajusteront.
1. **Votre pratique en séance 9** pour ces deux cas : les questions posées, les outils, ce que la personne doit avoir en sortant. Ce qui se prépare seul, et ce qui ne se travaille qu'ensemble. Les modules supposent que la séance 9 a posé la démarche visée, son financement ou la personne à voir, et la prochaine démarche.
2. **La part des situations** parmi vos bénéficiaires : reconversions, évolutions internes. Elle dira lequel relire en premier.
3. **La fonction publique.** La carte « Dans la fonction publique » de l'exercice 4 (reconversion) reste générale : CPF, congé de formation professionnelle, plan de formation de l'administration, le service des ressources humaines. À préciser avec vous selon les statuts que vous rencontrez (État, territoriale, hospitalière, contractuels).
4. **Les dispositifs que vous mobilisez vraiment**, ceux que vous déconseillez, et pourquoi. Les cartes du financement les nomment tous, sans hiérarchie.
5. **Vos sources de confiance** : sites officiels, bases de formations, interlocuteurs. Les liens actuels sont tous officiels.
6. **Les moments que vous recommandez** pour une demande d'évolution, au-delà des quatre cartes (entretien de parcours professionnel, entretien annuel, poste ouvert, besoin nouveau).
7. **La confidentialité quand l'employeur finance le bilan**, et pour un agent de l'État (le document de synthèse y est communicable aux ressources humaines, sauf opposition expresse) : l'encadré dit « sans votre accord » ; faut-il une phrase pour la fonction publique ?
8. **Le programme et le site** : étendre la phrase « Un projet de création ajoute un module d'environ 2 h entre les séances 9 et 10. » aux trois modules (texte réglementaire, à votre demande seulement), puis le dire au site (`recap-site-parcours.md` : « seul le module création existe » n'est plus vrai).

## 8. La suite

1. Vous relisez les deux modules, Lysiane et vous : les PDF se génèrent avec `python Scripts/main_generate_module_reconversion.py` et `python Scripts/main_generate_module_evolution_interne.py`, et l'app les propose au catalogue.
2. Vos réponses à la section 7 et vos retouches s'appliquent dans les fichiers de `workbooks/`, dans cette PR ou la suivante.
3. Puis un essai de leur personnalisation avec la vraie clé, sur des profils types : deux appels par module, annoncés avant.
