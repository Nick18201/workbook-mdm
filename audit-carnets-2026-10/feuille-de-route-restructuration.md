# Feuille de route : restructuration des carnets

Ce document prépare le chantier qui suit l'unification. Il a été écrit le 8 octobre 2026 pour être repris dans une nouvelle conversation. Il complète la carte du parcours (`carte-parcours-unifie.md`), qui reste la référence pour le contenu de chaque carnet. Sa section 9, « À prendre », est remplacée par les décisions ci-dessous.

## 1. Où on en est

| Étape | État |
|---|---|
| Audit, carte du parcours, récapitulatif pour le site | Fusionnés (PR #48 et #49) |
| Programme du bilan : séances 5 / 3 / 2, test des fonctionnements cognitifs, plus de Hexa3D | Fusionné (PR #50) |
| Unification : une seule source, `workbooks/*.json`, un seul moteur, MBTI retiré des carnets | Fusionné (PR #51) |
| R0 · Socle : nommage, palette, gabarit commun, langue du PDF | Fusionné (PR #52) |
| R0 bis · Format : fixe / adaptable, identifiants de données, reports | Fusionné (PR #53) |
| R1 · Carnet 1 · L'état des lieux (`carnet-1.json`) | PR en cours |
| Site (`marge-de-manoeuvre`) | À faire par l'agent du site, avec `recap-site-parcours.md`, en même temps que le programme |

**Avant chaque PR : vérifier que la précédente est fusionnée**, puis partir d'une branche à jour de `main`. Ne pas empiler les branches.

## 2. Les décisions

**Prises le 8 octobre 2026 (rappel de la carte)**
- Plus de carnet 0. Le carnet N prépare la séance N : carnets 1 à 7, puis le carnet de route au temps 3.
- Séances réparties en 5 / 3 / 2. L'option « Initiation à l'IA » ouvre la séance 6.
- Le « test des fonctionnements cognitifs », conçu et éprouvé par Lysiane Brand, remplace le MBTI partout. Seule exception : la certification MBTI® de Lysiane, dans sa présentation. Hexa3D est abandonné.
- Pas de date de bascule : le nouveau parcours vaut pour les futurs bénéficiaires.
- La charge émotionnelle suit la ligne de James Pennebaker : des questions franches, avec le protocole en trois temps (avertissement, optionnalité stricte, phrase d'ancrage).

**Prises le 8 octobre 2026, suite**
1. **Le business plan existe en deux formats.**
   - Le **module création** du carnet de route, environ 12 pages (S9 → S10). Gemini le personnalise en une fois.
   - Le **livret complet**, un outil autonome pour l'accompagnement à la création après le bilan. L'app le personnalise partie par partie si besoin, car 36 pages d'un coup sont trop pour le modèle.
2. **Les quatre retraits sont validés.**
   - La vision à 360° (elle double les domaines de vie).
   - Quatre des huit questions de « Faire le point ».
   - L'arbre de vie devient facultatif.
   - Trois fiches métiers complètes au lieu de dix : les sept autres deviennent facultatives.
3. **Les modules reconversion et évolution interne viennent plus tard.** Leur chantier est décrit dans `chantier-modules-s9.md`. D'ici là, le carnet de route prévoit leur place, et la séance 9 traite le sujet à l'oral.
4. **« Carnet N » partout, identifiants compris.** « Carnet 1 » à « Carnet 7 » et « Carnet de route » s'affichent dans les PDF, l'app et le site. Les fichiers deviennent `carnet-1.json` … `carnet-7.json`, `carnet-de-route.json` et `business-plan.json` (plus `module-creation.json`). Le mot « chapitre » disparaît.
5. **Les cinq pièces de l'app reviennent, aux places prévues par la carte.**
   - Les trois règles, dans le cadre du carnet 1.
   - Les quatre zones, au carnet 2.
   - « Ce que je me dis → ce que montrent les faits », au carnet 4.
   - La grille d'entretien et le message d'approche, au carnet 7.
   - L'arbitrage A/B, les feuilles de route à 30, 60 et 90 jours et les garde-fous, au carnet de route.

   Leur texte d'origine se retrouve dans l'historique git : `git show 1696357:server/predefined_workbooks.py`.
6. **Découpage : un socle commun, puis une PR par carnet**, dans l'ordre du parcours.

**Prises pendant R0 (8 octobre 2026)**
7. **La palette suit les temps du programme** (choisie parmi quatre palettes comparées côte à côte, toutes pastels de la DA) :
   - temps 1, teintes froides : carnet 1 ciel, carnet 2 lilas, carnet 3 menthe, carnet 4 ciel, carnet 5 lilas ;
   - temps 2, teintes chaudes : carnet 6 amande, carnet 7 rose poudré ;
   - temps 3 : le carnet de route en jasmin.
   Écartées : le cycle des pastels sans logique, et les huit teintes distinctes, qui demandaient trois pastels nouveaux (pistache, pivoine, lagon) hors de la DA.

**Prises pendant R1 (8 octobre 2026)**
8. **La page « Avant de commencer » porte la météo**, dans chaque carnet. Au carnet 1, elle porte aussi l'engagement ; à partir du carnet 2, le récapitulatif guidé. Elle n'est pas numérotée : les exercices numérotés sont ceux qu'on écrit (cinq au carnet 1).
9. **Le carnet 1 s'ouvre par une page « Bienvenue »** : les trois temps du bilan sur une frise (carnets 1 à 5, 6 et 7, carnet de route) et le lien vers l'espace Notion. Puis le cadre de travail.
10. **Les huit domaines de vie**, notation de référence du parcours, reprise au carnet de route : travail, carrière · argent, finances · santé, énergie · famille · amis, vie sociale · temps pour soi, loisirs · lieu de vie, environnement · utilité, engagements. Bornes « Pas du tout satisfaisant » et « Pleinement satisfaisant ». Le carnet 4 reprend la note « Argent, finances ».
11. **Les anciens carnets restent dans l'app jusqu'à R11**, avec « (ancien parcours) » dans leur titre quand un nouveau carnet les remplace (`chap0` et `chap1` depuis R1).

## 3. Les PR, dans l'ordre

Une PR par ligne, fusionnée par Nicolas avant de passer à la suivante.

| PR | Contenu | Points d'attention |
|---|---|---|
| **R0 · Socle** | Le gabarit commun et le système de nommage (détails en section 4). La carte : section 9 mise à jour. | Touche tous les documents. Comparer avant et après chaque document, et ne garder que les changements voulus. |
| **R0 bis · Format** | La marque « fixe / adaptable » et les identifiants de données, avec le bloc de report (« Reportez vos seuils · carnet 4, p. 12 ») et la règle de personnalisation qui en découle dans l'app. | Séparée de R0 pour garder le socle lisible. À fusionner avant R2, le premier carnet qui reporte des données. |
| **R1 · Carnet 1** | État des lieux et héritages, à partir du carnet 0 et du carnet 1 actuels et de l'app (carte, section 5). | Le cadre de travail est fixe et jamais personnalisé. Une alternative pour une famille absente ou douloureuse. |
| **R2 · Carnet 2** | Parcours : objectif boussole, expériences et travail réel, travail empêché, quatre zones, fil rouge, ligne de vie, arbre de vie facultatif, interview. | Il absorbe le travail réel du livret. Cible : 2 h 45. |
| **R3 · Carnet 3** | Fonctionnements : l'encadré « À savoir sur le test », les 17 mises en situation réécrites, la page « ce que j'en retiens ». | Aucune mention du MBTI. Q16 est réécrite du point de vue des proches. |
| **R4 · Carnet 4** | Argent : la seule saisie du profil validé, la carte des 4 seuils, « ce que je me dis → les faits ». | La question sur le couple est posée au passé. Aucun chiffre personnel en exemple. |
| **R5 · Carnet 5** | Valeurs : la liste corrigée, la grille anti-compromis (seul endroit des 3 valeurs), l'entourage et la demande aux proches. | Les réponses des proches arrivent avant la séance 6. |
| **R6 · Carnet 6** | Exploration : la cartographie en reports, le retour des proches, les ressources, 10 pistes. | Les seuils restent dans une zone « à garder pour vous ». |
| **R7 · Carnet 7** | Confronter, en deux parties : les 3 fiches à critères, la préparation des enquêtes, salaires et débouchés, puis les comptes rendus, le terrain et la matrice. | Des liens officiels, pas de chiffres écrits dans le carnet. |
| **R8 · Carnet de route** | Deux parties. D'abord : profil en reports, compétences prouvées, deux récits. Ensuite : pistes A et B, feuilles de route à 30, 60 et 90 jours, premières actions, garde-fous et alliés, chemin parcouru, préparation du suivi, place du module de projet. | Remplace le livret. Ses 28 exemples (un seul profil, peut-être une personne réelle) disparaissent au profit d'exemples contrastés tirés de métiers différents. |
| **R9 · Module création** | Le business plan court, environ 12 pages : fondations, problème, offre, prix, point mort, test, synthèse. Il reprend les seuils, la grille anti-compromis et l'entretien prospects de l'app. | Il est personnalisable en une fois. |
| **R10 · Livret business plan** | Le livret complet autonome, avec les refontes de l'audit (rapport `08-business_plan.md`), et la personnalisation partie par partie dans l'app. | Informations réglementaires renvoyées vers les sources officielles. |
| **R11 · Nettoyage** | Supprimer `chap0` à `chap6.json` et `livret.json`, mettre à jour le catalogue de l'app, la CI et `test_cli_documents.py`. Vérifier la cohérence avec le programme et le récapitulatif du site. | Tant que R11 n'est pas fusionnée, les anciens carnets restent disponibles à côté des nouveaux. |
| Plus tard | Modules reconversion et évolution interne | Voir `chantier-modules-s9.md`. |

Pour chaque PR de carnet :
- **Contenu.** Suivre le tableau de la carte (section 5) et les recommandations du rapport du carnet (`rapports/`).
- **Charge émotionnelle.** Poser le protocole sur chaque exercice à forte charge.
- **Les données qui circulent.** Les écrire une seule fois (`data_id`) et les reporter avec un bloc `report` (carte, section 7, pour les identifiants). Les tests vérifient qu'un report vise une donnée déclarée.
- **Fixe ou adaptable.** Marquer `"fixed": true` ce que la personnalisation ne doit pas toucher (carte, section 8) : le cadre et les héritages (carnet 1), les questions du test (carnet 3), la liste de valeurs (carnet 5), les critères des fiches, la définition des seuils.
- **Durée.** Viser la durée cible, la mettre dans le sourcil des exercices et mettre à jour le budget (carte, section 6).
- **Vérifier le rendu de chaque page.**
- **Relire l'audit** (`synthese.html` et le rapport du carnet) une fois le carnet construit, recommandation par recommandation, et itérer.

## 4. Le socle (R0) en détail

**Nommage**
- `DocumentBuilder` accepte les carnets 1 à 7 (folio « carnet N/7 ») et le carnet de route (folio « carnet de route »). L'ouverture affiche « Carnet de bord · carnet N » au lieu de « chapitre N ».
- `PDFStyle.CARNET_PASTELS` est réattribué pour 1 à 7 et pour le carnet de route. **Fait** : palette « par temps » (section 2, point 7).
- Les scripts `main_generate_carnet_N.py`, le catalogue de l'app, la CI et les tests suivent.

**Gabarit commun** (carte, section 4 ; synthèse, lot 2)
- **Le bloc « protocole »**, en trois temps. Avant l'exercice : un avertissement, puis « Si cet exercice vous semble trop lourd à faire hors séance, laissez-le vierge : nous l'aborderons ensemble. » (« trop lourd seul » s'accordait avec la personne). Après l'exercice : un champ d'ancrage court, « Aujourd'hui, avec le recul, je sais que… ».
- **La durée dans le sourcil** (« Exercice 2 · 15-20 min »). La page d'ouverture donne le total et le découpage conseillé, avec une ligne de cadre (qui lit, droit de passer une question).
- **L'exemple contrasté**, avec un rendu commun « En surface / Exploitable ».
- **La météo et le récapitulatif** dans le gabarit de chaque carnet.
- **La fin de carnet en trois zones guidées**, avec le fil des pistes à partir du carnet 2. Elle remplace la grande zone « notes ».
- **Accessibilité** : la langue `fr` dans le catalogue du PDF.
- Chaque nouveau bloc suit la liste « Adding a new page template or atomic block » de `CLAUDE.md` : `spec.py`, `compiler.py`, aperçu dans l'app, test, planche de démonstration. Il s'ajoute aussi à `REFERENCE_BLOCKS_RULES` s'il ne doit pas être créé par Gemini.

**Format** (carte, section 10) : fait dans R0 bis
- **La marque « fixe / adaptable »** sur chaque bloc. Une seule règle de lecture pour la personnalisation : ce qui porte `"fixed": true` (une page entière ou un bloc) ne change pas, le reste est adaptable. Le protocole, l'ancrage, la météo et les reports sont toujours fixes. L'app ne se contente pas de le demander à Gemini : elle rétablit ce qui est fixe après chaque personnalisation (`keep_fixed`). La retouche d'un livret (« itérer ») suit la consigne du consultant, qui peut demander de modifier une page fixe.
- **Des identifiants stables pour les données** (par exemple `c4.seuils`), posés par `data_id` sur la page ou le bloc qui écrit la donnée. Le bloc `report` la reporte : « Vos quatre seuils · carnet 4 · p. 12 », la page étant lue dans le carnet 4 de `workbooks/` au moment de la génération. Sans fichier pour ce carnet, la ligne affiche « carnet 4 ». Les identifiants à utiliser sont dans la carte, section 7.

## 5. Comment travailler

- **Le contenu** est dans `workbooks/<id>.json`, au format de `Scripts/workbook_generator/spec.py` (la docstring de `BlockSpec` donne la forme de chaque bloc). On prend exemple sur les carnets existants.
- **Générer** un document : `python Scripts/main_generate_<id>.py --output <fichier>.pdf`, depuis la racine du dépôt.
- **Voir les pages** : les rendre en PNG avec pymupdf (`page.get_pixmap(dpi=60).save(...)`) dans `previews/` (ignoré par git), et les relire une à une.
- **Comparer** avant et après (pour le socle) : générer les PDF de `main` dans un dossier temporaire, puis comparer page par page l'image (`pixmap.samples`), le texte (`get_text`) et les champs (`widgets()`).
- **Tester** : `python -m pytest tests`. `tests/test_workbooks.py` vérifie :
  - que chaque fichier est au catalogue ;
  - qu'aucun `field_id` n'est en double ;
  - que les fichiers ne gardent que ce qu'ils définissent : pas de `null`, pas de valeur par défaut recopiée.
- **Les conventions posées par le carnet 1** (`workbooks/carnet-1.json`), à suivre dans les suivants :
  - en tête du fichier, `"carnet": N` (pastel, folio et sourcils viennent de là), sans `folio` ni `pastel` ;
  - les identifiants de champs commencent par `cN_` (`c1_objectif`), ceux de la météo par `cN_meteo` et ceux du livrable par `cN_livrable` ;
  - l'ouverture liste chaque élément avec sa durée (« Exercice 3 · Votre objectif, première version · 10 min »), donne `duration` et `split` ; la somme fait la cible de la carte ;
  - chaque page d'exercice a pour sourcil « Exercice N · nom court · durée », une page par partie quand l'exercice en a deux, et s'ouvre par une phrase qui dit à quoi il sert ;
  - un seul exemple contrasté par exercice, d'un métier au nom épicène et différent à chaque fois (juriste, cariste, commis de cuisine, comptable, ébéniste au carnet 1) ; un exemple de plus peut aller dans le champ `example` d'une question ;
  - le protocole ouvre la première page d'un exercice lourd, l'ancrage ferme la dernière ;
  - `fixed: true` sur la page entière quand tout y est fixe, sur le bloc sinon ; un paragraphe qui renvoie à un autre carnet (« vous la préciserez au carnet 2 ») est fixe, comme le dos ;
  - deux lignes manuscrites pour une réponse en phrase (case de 1,6 cm au moins), une ligne pour un mot (0,8 cm) ; `tests/test_workbooks.py` le vérifie pour chaque carnet, avec une info-bulle sur chaque champ ;
  - une page ne déborde jamais sur une page « (suite) » : passer des cases en grille de deux colonnes, raccourcir un libellé ou un exemple, plutôt que de descendre sous ces hauteurs.
- **Tester l'app en local** : `python -m uvicorn server.app:app --port 8080`. Sans clé Gemini, l'app fonctionne en mode de secours. Avec la vraie clé, tester la personnalisation des carnets 6, 7, du carnet de route et du module création, ceux qui s'y prêtent le plus (carte, section 8).

## 6. Les règles à garder en tête

- **Le ton (DA, section 7).**
  - Vouvoiement, phrases courtes et affirmatives, titres ponctués en casse de phrase.
  - Jamais « coach » : on dit « consultant en transformation » ou « la personne qui vous accompagne ».
  - Pas de registre de développement personnel, jamais « présentiel », aucun chiffre sans source.
- **Pas de formule genrée.** « Ce qui m'étonne », et non « Ce qui m'a surpris ».
- **Les exemples viennent d'un métier voisin**, jamais du métier de la personne, et d'un métier différent à chaque fois.
- **Ne sont jamais personnalisés** : le cadre, le protocole, les textes réglementaires et les renvois entre carnets.
- **Le programme est un texte réglementaire** : on le modifie seulement sur demande. Si un carnet change ce que le programme promet (séances, livrables, durées), le signaler à Nicolas et prévenir pour le site.

## 7. Ce qui reste ouvert

- **La politique des champs** : police fixe avec défilement, ou police automatique. À trancher après un test de saisie dans de vrais lecteurs PDF (Acrobat, Aperçu, navigateur).
- **Les 51 champs trop bas** pour l'écriture à la main : les agrandir au fil des PR de carnet. Depuis R1, un test le vérifie pour chaque nouveau carnet (1,6 cm pour une phrase, 0,8 cm pour un mot), et la case « Ce chiffre s'explique surtout par… » de la météo passe de 1,2 à 1,6 cm.
- **Les exemples du livret** décrivent peut-être une personne réelle. Ils disparaissent avec le carnet de route (R8), mais si c'est le cas, l'historique git les garde.
- **La personnalisation partie par partie** du livret business plan, dans l'app (R10).

## 8. Pour reprendre dans une nouvelle conversation

Message à coller, une fois la PR R1 (carnet 1, #54) fusionnée :

```text
Reprends la restructuration des carnets avec la PR R2 : le carnet 2, « Mon parcours ».

1. Prérequis
- Vérifie que la PR Nick18201/workbook-mdm#54 (R1, carnet 1) est fusionnée dans main.
- Crée ensuite une branche depuis main à jour. N'empile pas les branches.

2. À lire, dans cet ordre
- audit-carnets-2026-10/feuille-de-route-restructuration.md, sections 2 à 7. La section 5 donne les conventions posées par le carnet 1.
- audit-carnets-2026-10/carte-parcours-unifie.md :
  - section 4 (gabarit commun) ;
  - section 5, carnet 2 ;
  - sections 6 (budget), 7 (identifiants c2.*) et 8 (fixe ou adaptable : carnet 2 = pertinence moyenne).
- audit-carnets-2026-10/rapports/02-chap2.md en entier, et rapports/07-livret.md, thème 2 (le travail réel, que le carnet 2 absorbe).
- La synthèse audit-carnets-2026-10/synthese.html, sections 02 (constats transversaux) et 06 (conditions de remplissage).
- workbooks/carnet-1.json, le modèle à suivre, et workbooks/chap2.json, le contenu actuel.
- Les quatre zones de l'app : git show 1696357:server/predefined_workbooks.py, fonction _build_chap3_spec.

3. Ce qu'il faut construire
workbooks/carnet-2.json, cible 2 h 45 d'écriture.
- Une page « Avant de commencer » : la météo (c2.meteo) et le récapitulatif guidé de la séance 1. Ce récapitulatif utilise des blocs report vers c1.objectif et c1.autorisation pour préciser l'objectif boussole (c2.boussole).
- Les exercices de la carte :
  - « À lire : comprendre ses racines », allégé à trois notions, avec protocole, sans « névrose de classe » ;
  - les expériences et le travail réel, une fiche par expérience, quatre au choix ;
  - le travail empêché, avec protocole et un seul terme ;
  - les quatre zones ;
  - le fil rouge en une phrase, les trois verbes d'action, et pour chaque moteur « je le veux / on l'attend de moi » ;
  - la ligne de vie, avec protocole sur les vallées ;
  - les compétences de vie, avec une ligne « épreuves » facultative ;
  - l'arbre de vie, facultatif ;
  - l'interview, facultative et hors temps d'écriture, en proposant de choisir parmi les modèles du carnet 1 (report de c1.modeles).
- Une fin de carnet avec le fil des pistes (pistes: true) et c2.livrable.
- Les autres data_id de la carte, section 7.
- Les marques fixed de la section 8 : le protocole, les questions franches, et les renvois entre carnets.

4. Les règles à tenir
- Le ton de la DA : vouvoiement, jamais « coach », pas de registre de développement personnel, aucun chiffre sans source.
- Aucune formule genrée : ni participe ni adjectif accordé dans les amorces en « je ».
- Un exemple contrasté par exercice, d'un métier au nom épicène, différent de ceux du carnet 1 (juriste, cariste, commis de cuisine, comptable, ébéniste).
- Le protocole ouvre la première page d'un exercice lourd, l'ancrage ferme la dernière.
- Les tailles de case : 1,6 cm au moins pour une phrase, 0,8 cm pour un mot. tests/test_workbooks.py le vérifie.
- Aucune page « (suite) ». S'il manque de la place : une grille de deux colonnes, un libellé ou un exemple plus court.
- Attention : la ligne de vie et l'arbre de vie remplissent le reste de leur page.

5. Méthode
a. Commence par me montrer le plan du carnet 2, page par page, avec les durées et leur total, et les choix à trancher en fin de message. Attends ma réponse avant d'écrire le JSON.
b. Écris le JSON. Ajoute Scripts/main_generate_carnet_2.py, la ligne de tests/test_cli_documents.py, et l'entrée carnet-2 du catalogue (server/predefined_workbooks.py), avec « (ancien parcours) » sur chap2.
c. Rends chaque page en PNG dans previews/ avec pymupdf et relis-les une à une.
d. Lance python -m pytest tests, puis génère tous les Scripts/main_generate_*.py.
e. Relis la synthèse et les rapports 02 et 07, recommandation par recommandation. Itère, puis dis-moi ce qui est traité et ce qui est écarté, avec la raison.
f. Mets à jour la feuille de route :
   - section 1 (état des PR) ;
   - section 2 (décisions prises pendant R2) ;
   - section 5 (nouvelles conventions, s'il y en a) ;
   - section 8 (le prompt de reprise pour R3, rédigé sur ce modèle).
   Mets aussi à jour la carte, section 6 (budget du carnet 2).
g. Commite sur la branche. J'ouvrirai la PR avec le bouton.

6. Environnement (Windows, dans un worktree)
- Le Python du venv est ../../../.venv/Scripts/python.exe.
- Pour importer le moteur hors des scripts : PYTHONPATH="Scripts;." (point-virgule sous Windows) et PYTHONIOENCODING=utf-8.
```
