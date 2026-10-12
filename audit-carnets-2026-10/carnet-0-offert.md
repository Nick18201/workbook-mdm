# Le carnet 0, offert avant le bilan

Version du 12 octobre 2026. Le carnet 0 est offert en échange d'une adresse e-mail. Il applique la règle du parcours, « le carnet N prépare la séance N » : **le carnet 0 prépare le premier échange**, gratuit, de 30 min. Il est utile même à qui ne réserve pas. Qui réserve arrive avec sa question.

Il ne fait pas partie du bilan : ni des 14 h, ni des 10 à 20 h d'écriture, ni de la suite des sept carnets. La décision du 8 octobre (« plus de carnet 0 » dans le parcours) tient : le carnet 1 ne change pas.

## 1. Ce qu'il contient

`workbooks/carnet-0.json`, 11 pages, 30 min, teinte jasmin (choisie le 12 octobre face au ciel et au lin, sur planche comparée) : la porte d'entrée et la sortie, le carnet de route, partagent leur teinte.

| Page | Contenu | Durée |
|---|---|---|
| Couverture | « Mesurer votre *marge.* », le 0 géant, la rangée des sept carnets vides, « Avant le carnet 1 », « Offert · 30 minutes » | |
| Ouverture | Ce qu'il prépare, la question qu'il aide à poser, la liste des exercices. Le cadre : les réponses restent dans le fichier, une question peut se passer | |
| Avant de commencer | Météo du jour, puis le mode d'emploi du PDF | 2 min |
| Exercice 1 · Ce qui vous fait bouger | Le déclic, depuis quand, ce que je veux que ça change. Exemple : muséographe | 5 min |
| Exercice 2 · Votre semaine, côté énergie | Trois moments qui donnent de l'énergie, trois qui en coûtent, puis « Donc, ma prochaine façon de travailler devra… ». Exemple : scénographe | 8 min |
| Exercice 3 · Votre marge de manœuvre | Six leviers notés de 1 à 5 (temps, réserve, énergie, savoir-faire, réseau, liberté), le plus solide et celui à renforcer. Exemple : botaniste | 8 min |
| Exercice 4 · Les chemins possibles | Ajuster son poste, évoluer dans l'entreprise, changer de métier, créer, ne pas savoir encore : les trois modules du carnet de route, sans le dire. Puis ce qu'il faudrait savoir pour avancer | 3 min |
| Livrable | « Votre question de départ » : la question à poser au premier échange, ce qui étonne en relisant. Ni tampon « Validé en séance », ni date de séance | 2 min |
| À lire · Le bilan, en une page | Dix séances, le suivi, les carnets, la frise des trois temps, la synthèse qui n'appartient qu'à la personne, le CPF ; trois liens : réserver l'échange, le test des valeurs, le simulateur CPF | 2 min |
| Dos | « Pour aller plus loin : un premier échange de 30 minutes, gratuit. » | |

Il suit le gabarit commun et passe le contrôle de conformité sans remarque. Aucun chiffre sans source, aucune donnée déclarée (rien n'est reporté dans le carnet 1 : la personne n'a pas forcément rempli le carnet 0).

## 2. Ce que le moteur sait du carnet 0

`PDFStyle.CARNET_OFFERED = 0` :
- folio « carnet 0 », sourcil d'ouverture « Avant le bilan · carnet 0 », rangée de la couverture « Avant le carnet 1 » ;
- l'ouverture dit « Vos réponses restent dans ce fichier, sur votre ordinateur » et « gardez-le ouvert pendant le premier échange », au lieu de « renvoyez-le complété avant la séance » ; la durée ne parle pas d'entretiens ni de recherches ;
- la page livrable n'a ni tampon ni case « Livrable validé en séance », et ses zones sont « Avant le premier échange » ;
- l'app le propose dans « Adapter un carnet » (niveau moyen, comme les carnets 1, 3 et 5) : une variante par public, un métier ou un thème, se fait en un appel.

## 3. Le lot du site (dépôt `marge-de-manoeuvre`)

À confier à l'agent du site :
1. **Une page et un formulaire** : l'adresse e-mail, le même consentement que le test des valeurs (`submitQuiz` : refus des conseils et des offres, case facultative décochée, art. L.34-5 du CPCE), le pot de miel et la limite de débit.
2. **Le mail** : le lien du PDF. Le PDF est statique, dans `public/documents/` ; son lien n'est donné que dans le mail. L'adresse e-mail est le prix de la découverte, pas un verrou.
3. **Le PDF** : `python Scripts/main_generate_carnet_0.py --output <fichier>`. Le script ne le recopie pas dans le site, contrairement au programme : le nom et l'emplacement se décident au lot du site.
4. **La mesure** : le lien de réservation du PDF porte `?source=carnet-0` (`https://margedemanoeuvre.fr/contact/?source=carnet-0`). Le formulaire de contact peut le lire pour compter les échanges réservés depuis le carnet.
5. **Les renvois** : le mail du test des valeurs propose le carnet 0 ; le carnet 0 propose déjà le test des valeurs et le simulateur CPF.

## 4. Ce qui reste à trancher

- **Envoyer le carnet avant le premier échange.** L'échange serait plus riche, mais le cabinet recevrait des réponses personnelles. Proposé : non, « gardez-le ouvert pendant l'échange » (c'est ce que dit le carnet).
- **Une suite de mails** sur dix jours (le lien, une lecture de la grille des leviers, l'invitation au premier échange) : à décider au lot du site, avec le consentement déjà recueilli.
- **Le récapitulatif du site** (`recap-site-parcours.md`) dit « plus de carnet 0 » : c'est vrai du parcours. Le site doit présenter le carnet 0 comme offert, avant le bilan, et non comme le premier des carnets.
