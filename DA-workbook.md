# Direction artistique « Éditorial & Affirmé » : Marge de Manœuvre

Fiche de transmission pour la refonte du générateur de workbooks (les carnets de bord des bénéficiaires).
Elle est tirée du code du site (`tailwind.config.mjs`, `global.css`, composants) au 2026-10-07.

**Comment lire cette fiche**
- Sections 1 à 7 : la DA telle qu'elle est en ligne. Les valeurs sont exactes, à reprendre telles quelles.
- Section 8 : des propositions pour adapter la DA au workbook. Ce ne sont pas des règles du site : elles sont à faire valider.
- Section 9 : ce qu'il ne faut pas faire. Section 10 : les tokens à copier.
- Version détaillée, avec un aperçu par composant : le dossier `design-system/` (copie du design system publié sur claude.ai). Commencer par son `README.md`, puis `tokens.json` et `components/<Composant>/README.md`.

---

## 1. Contexte

- **Marge de Manœuvre** est un organisme de bilans de compétences, **100 % à distance**. La méthode a été conçue par une psychologue du travail et un consultant en transformation. Chaque bénéficiaire est accompagné par une seule personne.
- **Positionnement** : le passage à l'action réaliste (un projet piloté, le marché du travail, l'IA, un salaire et un rythme de vie sécurisés). Il rompt avec les bilans « quête de sens » et le développement personnel.
- **Les workbooks** sont les « carnets de bord », travaillés entre les séances :
  - un tronc commun de 7 carnets (chapitres 0 à 6) : Le Prélude, L'État des lieux, Mon parcours, Mes fonctionnements propres, Mon rapport à l'argent, Valeurs & moteurs profonds, Phase d'exploration ;
  - puis un carnet de route propre au projet : reconversion, création ou reprise, ou évolution interne.
  - Chaque carnet contient un objectif, 4 exercices ou protocoles et **un livrable validé en séance**.
- **Public** : des adultes en transition professionnelle, souvent fatigués ou inquiets. La priorité va à la lisibilité et au calme, sans tomber dans le mièvre.

## 2. L'esprit

> Un magazine éditorial sûr de lui, sur un papier crème. De grands titres serrés en noir avec un mot en corail, des repères en police machine à écrire, des cartes pastel très arrondies. Et quelques traces faites main (un post-it scotché, une annotation manuscrite, une flèche dessinée) qui rappellent un vrai carnet de travail.

Quatre registres, chacun porté par une police :

| Registre | Ce qui le porte |
|---|---|
| **Affirmé** | Titres DM Sans très gras, resserrés et ponctués. Un mot d'accent en corail ou en bleu. |
| **Éditorial** | Fond crème, beaucoup d'air, hiérarchie nette, un sourcil au-dessus de chaque titre. |
| **Précis, presque clinique** | PT Mono pour tous les repères : numéros, étiquettes, durées, compteurs. |
| **Humain** | Instrument Serif italique pour les post-it et les annotations manuscrites. |

**Géométrie** : des disques, des pilules et des arrondis. Le dynamisme vient d'une légère rotation ou d'une légère courbe. Jamais de formes organiques (gouttes, blobs).

## 3. Couleurs

### Neutres
| Token | Hex | Rôle |
|---|---|---|
| `surface` | `#FAF8F5` | Crème : fond par défaut des pages |
| `surface-card` | `#FFFFFF` | Blanc : cartes, pages intérieures, calques |
| `surface-alt` | `#F1EBE6` | Lin : sections alternées, pied de page |
| `ink` | `#111111` | Encre : texte principal, traits dessinés |
| `ink-muted` | `#4A4844` | Texte secondaire, sourcils |
| `line` | `#E5E5EE` | Filets, bordures de carte |
| `line-strong` | `#8A8680` | Bordure de champ ou de zone à remplir (contraste 3:1) |

### Marque
| Token | Hex | Rôle |
|---|---|---|
| `brand-coral` | `#FF3B3B` | Corail vif : **décor** (disques, point final). En texte, seulement à 24 px ou plus, et seulement sur crème ou blanc. |
| `brand-coral-strong` | `#C22626` | Corail foncé : **tout texte corail** en petit, étiquettes, tampons, puces. C'est aussi le fond qui porte du texte blanc. |
| `brand-blue` | `#251FD3` | Bleu, second accent : un mot de titre, les icônes, les gros numéros, le grand bloc d'action (texte blanc dessus). |
| `brand-blue-hover` | `#1C18A8` | Bleu au survol |
| `brand-red` | `#E40B1A` | Rouge vif : libellé des boutons 3D, et seulement sur crème ou blanc |

### Pastels (fonds de carte, post-it, formes de fond)
| Token | Hex |
|---|---|
| `pastel-almond` (amande) | `#FFDDCB` |
| `pastel-jasmine` (jasmin) | `#FFEA8C` |
| `pastel-lilac` (lilas) | `#E7E0FF` |
| `pastel-sky` (ciel) | `#DDEAF9` |
| `pastel-mint` (menthe) | `#D7F2E3` |
| `pastel-blush` (rose poudré) | `#FFE2D9` |

### Règles de contraste (WCAG, vérifiées par des tests sur le site)
- **Couleurs de texte autorisées sur tous les fonds clairs** (crème, blanc, lin, les 6 pastels) : `ink`, `ink-muted`, `brand-blue`, `brand-coral-strong`. `ink` et `ink-muted` passent même le niveau AAA (7:1).
- **Texte blanc** : seulement sur `ink`, `brand-blue`, `brand-blue-hover` et `brand-coral-strong`. Jamais sur le corail vif (3,5:1).
- **Corail vif** : jamais en petit texte. Sur le lin et les pastels, le texte corail passe en `brand-coral-strong`.
- **Zones à remplir** : bordure `line-strong`, jamais `line`, trop pâle.

### Dosage et usages observés
- Environ 80 % de crème, de blanc et d'encre. Les pastels servent aux grands blocs. Le corail et le bleu sont des touches : un mot, un disque, une icône.
- Une couleur d'accent par titre, deux au plus.
- Le jasmin sert aussi de couleur de sélection de texte.

| Élément | Pastel utilisé sur le site |
|---|---|
| Post-it | jasmin ou amande |
| Livrable | post-it jasmin |
| Carnets | lilas |
| Ressources | jasmin |
| Copilote IA | menthe |
| Téléphone | ciel |
| « Case gagnante » d'un comparatif | menthe |

### Palette du Test des valeurs (seulement si un carnet affiche les valeurs de Schwartz)
| Catégorie | Marque | Fond associé |
|---|---|---|
| Ouverture au changement | ocre `#C07A00` | jasmin |
| Affirmation de soi | `#C22626` | rose poudré |
| Conservation | bleu `#2F35DB` | ciel |
| Dépassement de soi | sarcelle `#0E8C7A` | menthe |

Les couleurs de marque servent aux points, traits et pastilles, **jamais au texte**. Elles ne se posent que sur crème ou blanc : l'ocre tombe sous 3:1 sur le lin et sur les pastels. Sur un fond pastel, le texte reste à l'encre.

## 4. Typographie

Les quatre familles sont sur Google Fonts.

| Rôle | Police | Graisses | Usage |
|---|---|---|---|
| Titres | **DM Sans** | 700 (titres courants), 800 (grands titres) ; italique 400 pour la 2e partie d'un titre | Titres h1 à h6, titres de carte, accroches |
| Corps | **Manrope** | 400 ; 600 pour le gras dans le texte ; 800 pour le logotype | Paragraphes, consignes, descriptions |
| Repères | **PT Mono** | **400 uniquement** | Sourcils, étiquettes, numéros, durées, compteurs, métadonnées : en MAJUSCULES, interlettrage large |
| Annotations | **Instrument Serif** | **400 italique uniquement** | Post-it, annotations manuscrites, citations |

**Règles**
- **Jamais de gras sur PT Mono ni sur Instrument Serif** : ces polices n'existent qu'en 400, et le faux gras bave. Pour hiérarchiser des repères, on joue sur les majuscules, l'interlettrage et la couleur.
- Instrument Serif : toujours en italique, et un cran plus grand que le texte voisin (16 px minimum).
- Titres : interlettrage négatif (−0,03 em ; −0,05 em pour les très grands titres), interlignage de 0,95 à 1,1, lignes équilibrées (`text-wrap: balance`).
- Corps : interlignage 1,65. Jamais moins de 14 px pour un texte de lecture.
- Échelle (px) : 12 · 14 · 16 · 18 · 20 · 24 · 30 · 36 · 48 · 60 · 72 · 96. Pas de taille arbitraire.

**Motifs de titres**
1. **Phrase à l'encre, fin en corail, avec un point final.** « Prenez de la ***marge.*** » (« marge. » en corail). « Entre deux séances, ***le bilan continue.*** » Les titres sont des affirmations ponctuées.
2. **Titre de carte en deux temps** : une 1re ligne DM Sans 700 à l'encre, puis une 2e ligne en *DM Sans italique 400, en bleu*. Exemple : « Moteurs profonds et réalité économique / *pour valider chaque décision* ».
3. **Deux accents au plus** : « Une décision éclairée (bleu) et un plan d'action concret (corail). »

**Sourcil (eyebrow)** : PT Mono 12 px, majuscules, interlettrage 0,2 em, `ink-muted`. Il se place au-dessus de chaque titre de section (« NOTRE APPROCHE », « ENTRE LES SÉANCES »).

**Étiquette** : PT Mono 12 px, majuscules, interlettrage 0,14 em, dans une pilule à rayon plein (marges intérieures 6 × 12 px). Sur une carte pastel, elle a un fond blanc à 70 % et un texte bleu ou encre. Exemple : « UNE MÉTHODE À QUATRE MAINS ».

## 5. Éléments signature

1. **Carte pastel** : un aplat pastel, rayon 32 px (40 px pour les grandes cartes), sans bordure ni ombre, marges intérieures de 24 à 40 px. Dedans : une étiquette, un titre, un texte, et éventuellement une liste à icônes séparée par des filets `ink` à 10 %.
2. **Carte blanche** : fond blanc, bordure 1 px `line`, rayon de 32 à 40 px. Elle peut porter l'ombre « bento » : `0 20px 40px -10px rgba(0,0,0,.08), 0 8px 16px -4px rgba(0,0,0,.04)`.
3. **Post-it** :
   - fond jasmin ou amande, rayon 2 px, rotation entre −3° et +2° ;
   - ombre `0 10px 25px -4px rgba(0,0,0,.14), 0 4px 8px -2px rgba(0,0,0,.06)` et un filet haut de 1 px `line` à 60 % ;
   - un **ruban washi** : 48 à 56 × 16 px, blanc à 60 %, bordure pointillée blanche à 40 %, rotation de ±1 à 2°, centré, qui dépasse de 10 px en haut ;
   - un texte en Instrument Serif italique, de 18 à 24 px, à l'encre : une phrase courte qui reformule (« Du bilan à l'action. », « De la réflexion à une décision concrète. »).
4. **Annotation manuscrite avec flèche dessinée** :
   - le texte : Instrument Serif italique, de 18 à 30 px, à l'encre, rotation de −2° à −3°, environ 15 à 19 rem de large au plus ;
   - la flèche : un trait à l'encre de 1,75 px, extrémités et jointures rondes, sans remplissage. Une courbe de Bézier, puis une pointe ouverte en chevron :
   ```svg
   <svg viewBox="0 0 90 50" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
     <path d="M4 44 C 24 40, 52 30, 80 12" /><path d="M70 8 L81 11 L76 21" />
   </svg>
   ```
5. **Gros numéro de chapitre** : PT Mono de 60 à 72 px, en bleu, interligne 1. À côté, un sous-titre en PT Mono 12 px, majuscules, `ink-muted`. Le titre du chapitre vient dessous, en DM Sans 800.
6. **Puce étoile à 4 branches** : 14 px, en `brand-coral-strong`, pour les listes d'exercices :
   ```svg
   <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0 C 8.6 5.2, 10.8 7.4, 16 8 C 10.8 8.6, 8.6 10.8, 8 16 C 7.4 10.8, 5.2 8.6, 0 8 C 5.2 7.4, 7.4 5.2, 8 0 Z"/></svg>
   ```
7. **Tampon « Validé en séance »** : bordure 2 px `brand-coral-strong`, rayon 8 px, PT Mono 12 px en majuscules avec un interlettrage large, texte `brand-coral-strong`, une icône de coche, rotation de −4°. Sur le site, il est posé sur le post-it jasmin « LIVRABLE ».
8. **Pastilles d'icône** : un disque de 48 à 56 px, blanc à 70 % sur une carte pastel, ou pastel sur la crème et le lin. L'icône fait de 24 à 30 px, en bleu ou à l'encre. Les icônes viennent de **Material Symbols, style Outlined** (menu-book, auto-awesome, fact-check, route, shield, query-stats, forum, check, lock…).
9. **Formes de fond** :
   - de grands disques pastel pleins (jasmin, ciel, amande ou lilas, à 70–90 %), coupés par le bord de la page, souvent dans le coin haut droit ;
   - une pilule épaisse légèrement courbée en S (bleu ciel) ;
   - un petit disque corail plein (56 à 64 px), comme une ponctuation qui chevauche le bord d'une photo.

   Ces formes restent toujours derrière le contenu, sont courtes et ne gênent jamais la lecture.
10. **Le point corail** : la signature se termine par un disque corail d'environ 0,17 em. Il répond au « marge. » corail du titre d'accueil.
11. **Frise** :
   - un trait pointillé de 2 px, à l'encre à 25 % ;
   - un point plein à l'encre de 12 px au départ, un triangle plein à l'arrivée ;
   - les étapes sont des pastilles d'icône posées sur le trait, entourées d'un anneau de 6 px de la couleur du fond.
   - Libellés des extrémités en PT Mono majuscules (« APRÈS LA SÉANCE » → « AVANT LA SUIVANTE »).
12. **Diagramme de Venn** : des cercles translucides corail à 20 %, jasmin à 70 % et bleu à 15 %. L'intersection est en bleu plein, avec un libellé blanc.
13. **Flèche signature** (dans les boutons et les liens d'action) :
   ```svg
   <svg viewBox="0 0 20 14"><path d="M19.046 6.7487L12.3238 0.0791016V4.89712H0.371094V8.6068H12.3238V13.4183L19.046 6.7487Z" fill="currentColor"/></svg>
   ```
14. **Bouton 3D double calque** (sur écran uniquement) :
   - un calque blanc décalé de +3/+3 px et un contour de 1 px rouge décalé de −3/−3 px ;
   - un libellé en DM Sans 900, minuscules, rouge, avec la flèche signature ; il existe une variante bleue ;
   - au survol, les calques s'écartent à 6 px ;
   - en option, une pastille PT Mono à cheval sur le contour (« 30 MIN »).
15. **Photos** :
   - **à fond perdu**, collées aux bords de la carte ; ou bien isolées, avec un rayon de 24 à 32 px et l'ombre bento ;
   - jamais de cadre en retrait ni de vide décoratif au-dessus d'une image ;
   - lumière naturelle, vraies personnes, travail à distance.
16. **Logotype** :
   - « marge / de manœuvre » sur deux lignes, en Manrope 800, minuscules, interlettrage très serré (−0,05 em), interligne 0,85 ;
   - souligné d'un trait épais à l'encre (environ 96 × 4 px) ;
   - en très grand, sur une seule ligne, il se termine par le point corail.

## 6. Mise en page

- **Fonds alternés** : crème, puis lin, puis crème. Un seul grand bloc bleu plein (texte blanc, disques jasmin et corail coupés par les bords) marque le moment de l'action.
- Beaucoup d'air, mais **pas de vide décoratif**. Les grilles sont en deux colonnes (texte d'un côté, visuel de l'autre), avec environ 32 px entre les blocs.
- **En-tête de section** : le sourcil et le grand titre à gauche, un post-it ou une annotation à droite, alignés en bas.
- **Rayons** : 32 à 40 px pour les cartes, 24 px pour les pages intérieures, 2 px pour les post-it, 8 px pour les tampons, 12 à 16 px pour les boutons. Rayon plein pour les pilules et les disques.
- **Animations** (sur écran) : courtes, environ 0,2 s. Elles respectent `prefers-reduced-motion`.

## 7. Ton et vocabulaire

- **Vouvoiement.** Phrases courtes, affirmatives et concrètes. Les titres sont ponctués.
- **Lexique** : action, décision, projet, livrable, marché, faisabilité, salaire, rythme de vie, arbitrage, « validé en séance ».
- **À éviter** : le registre du développement personnel (« quête de sens », « retrouver votre élan », « espace d'écoute bienveillant », « croyances limitantes », « syndrome de l'imposteur », l'ennéagramme).
- **Le métier** : dire « consultant en transformation », **jamais « coach »**. Pour parler de l'accompagnant : « la personne qui vous accompagne » ou « votre référent·e ».
- **« Cabinet »** : jamais pour désigner Marge de Manœuvre.
- **« Binôme »** : seulement pour parler de la conception de la méthode. Jamais d'une façon qui laisse croire que deux personnes sont présentes en séance.
- **Jamais « présentiel »** : tout se fait à distance.
- **Aucune statistique sans source.**
- **Typographie française** :
  - guillemets « » avec des espaces insécables ;
  - une espace insécable avant : ; ! ? ;
  - une espace insécable entre un nombre et son unité (« 8 domaines », « 93 questions ») ;
  - « œ » ;
  - Le test du bilan est le « test des fonctionnements cognitifs » : jamais « MBTI » (marque sous licence) ni type en quatre lettres.

## 8. Adapter la DA au workbook (propositions à valider)

**Impression**
- Corps en Manrope, 10 à 11 pt, interligne d'environ 1,5. Titres en DM Sans 800, de 28 à 40 pt. Sourcils en PT Mono, 8 à 9 pt, majuscules, interlettrage 0,2 em. Annotations en Instrument Serif italique, 12 pt au moins.
- Les hex sont des couleurs d'écran (RVB). Le bleu `#251FD3` et le corail `#FF3B3B` sont très saturés : ils risquent de ternir en impression CMJN. Faites un test d'impression avant de valider.
- Les bénéficiaires impriment parfois en noir et blanc. La hiérarchie ne doit donc **jamais tenir à la seule couleur** : les sourcils, les numéros et les filets doivent rester lisibles en gris.

**Gabarits suggérés**
- **Couverture** :
  - fond crème et logotype ;
  - le gros numéro du carnet en PT Mono bleu, puis le titre en DM Sans 800 avec un mot d'accent (« Mon rapport ***à l'argent.*** ») ;
  - un disque pastel coupé par le bord, et un post-it qui porte la promesse du carnet.
  - Illustration retenue le 2026-10-07 : la table de travail vue du dessus (`assets/illustrations/couverture.svg`), faite des formes de la DA (disques, pilules, traits à l'encre arrondis, étoiles). Le disque pastel prend la couleur du carnet, et le post-it de la promesse est collé sur les carnets fermés.
  - Ne pas reprendre l'illustration de l'ancien livret (voir section 9).
- **Ouverture de chapitre** :
  - un sourcil « CARNET DE BORD · CHAPITRE 3 », puis le gros numéro et le sous-titre en PT Mono ;
  - le titre, puis l'objectif en Manrope ;
  - un encadré « EXERCICES & PROTOCOLES » avec les puces étoile.
- **Page d'exercice** :
  - une étiquette PT Mono (« EXERCICE 2 · 20 MIN »), puis la consigne ;
  - des zones d'écriture sur fond blanc, avec une bordure `line-strong` de 1 px et un rayon de 16 px, ou des lignes pointillées à l'encre à 25 % ;
  - les échelles et les jauges sous forme de pastilles.
- **Encadré** (conseil, rappel, exemple) : une carte pastel avec une étiquette.
- **Fin de carnet** : le post-it jasmin « LIVRABLE » et le tampon « Validé en séance », avec la date et une case à cocher.
- **Folio** : en PT Mono, en bas de page, par exemple « marge de manœuvre · carnet 3/7 · p. 12 ».

**Dosage**
- Une seule touche « faite main » par page : un post-it **ou** une annotation.
- Un pastel dominant par carnet, pour s'y retrouver d'un carnet à l'autre. Le texte posé dessus reste toujours à l'encre.

## 9. À ne pas faire

- Reprendre l'ancienne DA :
  - la palette « Kraft & Ink » ;
  - les polices Newsreader et Plus Jakarta Sans ;
  - **les illustrations végétales à plat**, comme sur la couverture actuelle du livret d'accompagnement (photo d'un livret corail et bleu avec une plante). Cette direction a été abandonnée.
- Utiliser des couleurs hors palette (par exemple les palettes par défaut d'un framework) ou du texte en gris clair.
- Mettre en gras du PT Mono ou de l'Instrument Serif, ou utiliser Instrument Serif en romain (droit).
- Poser du corail vif en petit texte ou sur un pastel. Poser du texte blanc sur du corail vif. Écrire en ocre.
- Dessiner des formes organiques (gouttes, blobs), ou un décor qui passe sous le texte.
- Inventer des chiffres, des témoignages ou des partenariats.

## 10. Tokens à copier

```css
/* Polices : Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400..900;1,9..40,400&family=Manrope:wght@400..800&family=PT+Mono&family=Instrument+Serif:ital@1&display=swap');

:root {
  /* Neutres */
  --color-surface: #FAF8F5;       /* crème : fond de page */
  --color-surface-card: #FFFFFF;  /* blanc : cartes */
  --color-surface-alt: #F1EBE6;   /* lin : fonds alternés */
  --color-ink: #111111;
  --color-ink-muted: #4A4844;
  --color-line: #E5E5EE;
  --color-line-strong: #8A8680;   /* bordures de champs */

  /* Marque */
  --color-coral: #FF3B3B;         /* décor ; texte >= 24px sur crème/blanc */
  --color-coral-strong: #C22626;  /* tout texte corail */
  --color-blue: #251FD3;
  --color-blue-hover: #1C18A8;
  --color-red: #E40B1A;           /* libellé des boutons 3D */

  /* Pastels */
  --color-almond: #FFDDCB;
  --color-jasmine: #FFEA8C;
  --color-lilac: #E7E0FF;
  --color-sky: #DDEAF9;
  --color-mint: #D7F2E3;
  --color-blush: #FFE2D9;

  /* Typographie */
  --font-heading: 'DM Sans', sans-serif;               /* 700 / 800, italique 400 */
  --font-body: 'Manrope', sans-serif;                  /* 400 / 600 / 800 */
  --font-label: 'PT Mono', monospace;                  /* 400 seulement, MAJUSCULES */
  --font-serif: 'Instrument Serif', Georgia, serif;    /* italique 400 seulement */
  --tracking-display: -0.03em;
  --leading-tight: 1.1;
  --leading-relaxed: 1.65;

  /* Formes */
  --radius-card: 2rem;       /* 32px ; 2.5rem pour les grandes cartes */
  --radius-page: 1.5rem;     /* 24px */
  --radius-postit: 2px;
  --radius-stamp: 0.5rem;
  --shadow-bento: 0 20px 40px -10px rgba(0,0,0,.08), 0 8px 16px -4px rgba(0,0,0,.04);
  --shadow-postit: 0 10px 25px -4px rgba(0,0,0,.14), 0 4px 8px -2px rgba(0,0,0,.06);
}
```
