# Feuille de route : restructuration des carnets

Ce document prépare le chantier qui suit l'unification. Il a été écrit le 8 octobre 2026 pour être repris dans une nouvelle conversation. Il complète la carte du parcours (`carte-parcours-unifie.md`), qui reste la référence pour le contenu de chaque carnet. Sa section 9, « À prendre », est remplacée par les décisions ci-dessous.

## 1. Où on en est

| Étape | État |
|---|---|
| Audit, carte du parcours, récapitulatif pour le site | Fusionnés (PR #48 et #49) |
| Programme du bilan : séances 5 / 3 / 2, test des fonctionnements cognitifs, plus de Hexa3D | PR #50, à fusionner |
| Unification : une seule source, `workbooks/*.json`, un seul moteur, MBTI retiré des carnets | PR #51, à fusionner |
| Site (`marge-de-manoeuvre`) | À faire par l'agent du site, avec `recap-site-parcours.md`, en même temps que le programme |

**Avant de commencer : fusionner les PR #50 et #51**, puis partir d'une branche à jour de `main`. Ne pas empiler les branches.

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

## 3. Les PR, dans l'ordre

Une PR par ligne, fusionnée par Nicolas avant de passer à la suivante.

| PR | Contenu | Points d'attention |
|---|---|---|
| **R0 · Socle** | Le gabarit commun et le système de nommage (détails en section 4). La carte : section 9 mise à jour. | Touche tous les documents. Comparer avant et après chaque document, et ne garder que les changements voulus. |
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
- **Les données qui circulent.** Les écrire une seule fois et les reporter avec leur origine (carte, section 7).
- **Durée.** Viser la durée cible, la mettre dans le sourcil des exercices et mettre à jour le budget (carte, section 6).
- **Vérifier le rendu de chaque page.**

## 4. Le socle (R0) en détail

**Nommage**
- `DocumentBuilder` accepte les carnets 1 à 7 (folio « carnet N/7 ») et le carnet de route (folio « carnet de route »). L'ouverture affiche « Carnet de bord · carnet N » au lieu de « chapitre N ».
- `PDFStyle.CARNET_PASTELS` est réattribué pour 1 à 7 et pour le carnet de route. **Montrer 3 ou 4 palettes côte à côte avant de trancher** : c'est la règle pour les choix de teintes.
- Les scripts `main_generate_carnet_N.py`, le catalogue de l'app, la CI et les tests suivent.

**Gabarit commun** (carte, section 4 ; synthèse, lot 2)
- **Le bloc « protocole »**, en trois temps. Avant l'exercice : « Si cet exercice vous semble trop lourd seul, laissez-le vierge, nous l'aborderons ensemble. » Après l'exercice : un champ d'ancrage court, « Aujourd'hui, avec le recul, je sais que… ».
- **La durée dans le sourcil** (« Exercice 2 · 15-20 min »). La page d'ouverture donne le total et le découpage conseillé, avec une ligne de cadre (qui lit, droit de passer une question).
- **L'exemple contrasté**, avec un rendu commun « En surface / Exploitable ».
- **La météo et le récapitulatif** dans le gabarit de chaque carnet.
- **La fin de carnet en trois zones guidées**, avec le fil des pistes à partir du carnet 2. Elle remplace la grande zone « notes ».
- **Accessibilité** : la langue `fr` dans le catalogue du PDF.
- Chaque nouveau bloc suit la liste « Adding a new page template or atomic block » de `CLAUDE.md` : `spec.py`, `compiler.py`, aperçu dans l'app, test, planche de démonstration. Il s'ajoute aussi à `REFERENCE_BLOCKS_RULES` s'il ne doit pas être créé par Gemini.

**Format** (carte, section 10)
- **La marque « fixe / adaptable »** sur chaque bloc. Une seule règle de lecture pour la personnalisation : Gemini ne touche que l'adaptable.
- **Des identifiants stables pour les données** (par exemple `c4.seuils`). Un renvoi devient alors « Reportez vos seuils · carnet 4, p. 12 » au moment de la génération, sans numéro de page écrit à la main.
- Ces deux points peuvent former une PR à part (R0 bis) si le socle devient trop gros.

## 5. Comment travailler

- **Le contenu** est dans `workbooks/<id>.json`, au format de `Scripts/workbook_generator/spec.py` (la docstring de `BlockSpec` donne la forme de chaque bloc). On prend exemple sur les carnets existants.
- **Générer** un document : `python Scripts/main_generate_<id>.py --output <fichier>.pdf`, depuis la racine du dépôt.
- **Voir les pages** : les rendre en PNG avec pymupdf (`page.get_pixmap(dpi=60).save(...)`) dans `previews/` (ignoré par git), et les relire une à une.
- **Comparer** avant et après (pour le socle) : générer les PDF de `main` dans un dossier temporaire, puis comparer page par page l'image (`pixmap.samples`), le texte (`get_text`) et les champs (`widgets()`).
- **Tester** : `python -m pytest tests`. `tests/test_workbooks.py` vérifie :
  - que chaque fichier est au catalogue ;
  - qu'aucun `field_id` n'est en double ;
  - que les fichiers ne gardent que ce qu'ils définissent : pas de `null`, pas de valeur par défaut recopiée.
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
- **Les 51 champs trop bas** pour l'écriture à la main : les agrandir au fil des PR de carnet.
- **Les exemples du livret** décrivent peut-être une personne réelle. Ils disparaissent avec le carnet de route (R8), mais si c'est le cas, l'historique git les garde.
- **La personnalisation partie par partie** du livret business plan, dans l'app (R10).

## 8. Pour reprendre dans une nouvelle conversation

Message à coller :

> Reprends la restructuration des carnets. Lis d'abord `audit-carnets-2026-10/feuille-de-route-restructuration.md`, puis la carte `audit-carnets-2026-10/carte-parcours-unifie.md`. Vérifie que les PR #50 et #51 sont fusionnées, puis lance la PR R0 (le socle) depuis `main`. Commence par me montrer les palettes de pastels candidates pour les carnets 1 à 7 et le carnet de route.
