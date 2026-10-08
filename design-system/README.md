Marge de Manœuvre est un organisme de bilans de compétences, 100 % à distance. Sa DA s'appelle « Éditorial & Affirmé » : un magazine sûr de lui, sur un papier crème. De grands titres serrés à l'encre avec un mot en corail, des repères en police machine à écrire, des cartes pastel très arrondies. Et quelques traces faites main (un post-it scotché, une annotation manuscrite, une flèche dessinée) qui rappellent un vrai carnet de travail.

Quatre registres, chacun porté par une police :

| Registre | Ce qui le porte |
|---|---|
| Affirmé | `titre-section`, `titre-hero` (DM Sans très gras, resserré, ponctué), un mot en `brand-coral` ou `brand-blue` |
| Éditorial | fond `surface`, beaucoup d'air, un `sourcil` au-dessus de chaque titre |
| Précis | PT Mono (`sourcil`, `etiquette`, `numero`, `pastille`) pour tous les repères |
| Humain | Instrument Serif italique (`annotation`, `post-it`) |

## Contenu et ton

- **Vouvoiement.** Phrases courtes, affirmatives et concrètes. Les titres sont des affirmations ponctuées d'un point : « Prenez de la marge. », « Entre deux séances, le bilan continue. », « Sept carnets, sept livrables validés en séance. », « Le budget ne doit pas décider à votre place. », « Lire avant de décider. »
- **Le positionnement, c'est le passage à l'action réaliste** : un projet piloté, le marché du travail, l'IA, un salaire et un rythme de vie sécurisés. « Au-delà de la quête de sens : un projet de transition piloté jusqu'à l'action. »
- **Lexique** : action, décision, projet, livrable, marché, faisabilité, salaire, rythme de vie, arbitrage, « validé en séance ».
- **À bannir** : le registre du développement personnel (« quête de sens » comme promesse, « retrouver votre élan », « espace d'écoute bienveillant », « croyances limitantes », « syndrome de l'imposteur », ennéagramme).
- **Le métier** : dire « consultant en transformation », jamais « coach ». Pour l'accompagnant : « la personne qui vous accompagne » ou « votre référent·e ».
- **« Cabinet »** : jamais pour désigner Marge de Manœuvre.
- **« Binôme »** : seulement pour la conception de la méthode (« une méthode à quatre mains »), jamais d'une façon qui laisse croire à deux personnes en séance.
- **Jamais « présentiel »** : tout se fait à distance.
- **Aucune statistique sans source**, aucun partenariat ni témoignage inventé.
- **Typographie française** : guillemets « » avec espaces insécables, espace insécable avant : ; ! ? et entre un nombre et son unité (« 93 questions »), « œ ».
- **Libellés des boutons 3D** : en minuscules (« réserver un 1er échange gratuit »). Pas d'émoji.

## Couleur

- **Le fond** : `surface` (crème) par défaut, `surface-card` (blanc) pour les cartes et les pages, `surface-alt` (lin) pour une section sur deux et le pied de page. Un seul grand bloc `brand-blue` plein marque le moment de l'action, en texte blanc avec des disques `pastel-jasmine` et `brand-coral` coupés par les bords.
- **Le dosage** : environ 80 % de `surface`, `surface-card` et `ink`. Les pastels servent aux grands blocs. `brand-coral` et `brand-blue` sont des touches : un mot, un disque, une icône. Une couleur d'accent par titre, deux au plus.
- **Le texte** : sur tous les fonds clairs (`surface`, `surface-card`, `surface-alt`, les six `pastel-*`), seuls `ink`, `ink-muted`, `brand-blue` et `brand-coral-strong` sont autorisés.
- **Le corail** : `brand-coral` est un décor. En texte, il est réservé aux titres de 24 px et plus, sur `surface` ou `surface-card`. Partout ailleurs, le texte corail passe en `brand-coral-strong`.
- **Le texte blanc** : seulement sur `ink`, `brand-blue`, `brand-blue-hover` et `brand-coral-strong`. Jamais sur `brand-coral`.
- **Le rouge** : `brand-red` sert uniquement au bouton 3D, sur `surface` ou `surface-card`.
- **Les zones à remplir** ont une bordure `line-strong`, jamais `line`.
- **Les usages des pastels** : post-it en `pastel-jasmine` ou `pastel-almond` ; livrable en post-it `pastel-jasmine` ; carnets en `pastel-lilac` ; copilote IA en `pastel-mint` ; « case gagnante » d'un comparatif en `pastel-mint` ; sélection de texte en `pastel-jasmine`.
- **Les `values-*`** marquent les quatre catégories du Test des valeurs (points, traits, pastilles). Jamais en texte, seulement sur `surface` ou `surface-card`.

## Typographie

- **Titres** en DM Sans : `titre-hero`, `titre-section`, `titre-carte`, `titre-bloc`, `titre-element`. Interlettrage négatif, interlignage serré, `text-wrap: balance`.
  - **Trois motifs** :
    1. Une phrase en `ink` qui finit en `brand-coral` (« Prenez de la *marge.* »).
    2. Un titre de carte en deux temps, avec la suite en `titre-carte-suite` (italique 400, `brand-blue`).
    3. Deux accents au plus, un bleu et un corail (« *Une décision éclairée* et un *plan d'action concret.* »).
- **Texte** en Manrope : `corps` (16 px) et `corps-petit` (14 px), interlignage 1,65. Le gras dans le texte est en 600, couleur `ink`. Le `chapeau` est en `ink-muted`. Jamais moins de 14 px pour un texte de lecture.
- **Repères** en PT Mono, 400 uniquement : `sourcil` (12 px, 0,2 em, `ink-muted`), `etiquette` (12 px, 0,14 em), `numero`, `pastille`. Toujours en majuscules. **Jamais de gras** : la hiérarchie passe par l'interlettrage et la couleur.
- **Annotations** en Instrument Serif, italique 400 uniquement : `annotation`, `post-it`. Jamais en romain, jamais en gras, 16 px au moins.
- **Logotype** : `logotype`, en Manrope 800, en minuscules, sur deux lignes, souligné d'un trait `ink` épais. Il n'existe pas de fichier logo : il se compose en texte (voir le composant Logotype).

## Espacement et mise en page

- Les espacements suivent l'échelle `space-*`. Comptez `space-8` entre deux blocs d'une section, `space-8` à `space-10` à l'intérieur d'une carte, `space-12` de gouttière dès la tablette et `space-24` en haut et en bas d'une section.
- **Pas de vide décoratif.** Les sections s'enchaînent dans un flux fluide (`space-16` de part et d'autre d'un fond lin).
- **En-tête de section** : le `sourcil` puis le titre à gauche ; un post-it ou une annotation à droite, aligné en bas.
- **Grilles** en deux colonnes, texte et visuel. Le texte ne dépasse pas `largeur-texte` ; le contenu ne dépasse pas `largeur-max`.

## Formes, bordures, ombres

- **Géométrie arrondie** : disques, pilules et grands rayons. Le dynamisme vient d'une légère rotation (`rotation-*`, jamais plus de 4°) ou d'une légère courbe. Jamais de forme organique (goutte, blob).
- **Rayons** : `radius-carte` ou `radius-carte-lg` pour les cartes, `radius-page` pour les pages et les photos, `radius-postit` pour le post-it, `radius-tampon` pour le tampon, `radius-full` pour les pilules et les disques.
- **Les cartes pastel n'ont ni bordure ni ombre.** La carte blanche a une bordure de 1 px `line`, et parfois l'ombre `shadow-bento`. Le post-it porte `shadow-postit`, et son ruban `shadow-washi`.
- **Formes de fond** :
  - de grands disques pastel pleins, coupés par le bord de la page (souvent le coin haut droit) ;
  - une pilule `pastel-sky` épaisse et légèrement courbée en S ;
  - un petit disque `brand-coral` qui chevauche le bord d'une photo.

  Ces formes restent toujours derrière le contenu, sont courtes et ne gênent jamais la lecture.
- **Traits dessinés** : `trait-fleche` en `ink`, extrémités et jointures rondes, sans remplissage. Une courbe, puis une pointe ouverte en chevron.

## Images

- **Photos à fond perdu**, collées aux bords de leur carte. Ou bien isolées, avec `radius-page` à `radius-carte` et `shadow-bento`.
- **Jamais** de cadre en retrait ni de vide décoratif au-dessus d'une image.
- Vraies personnes, lumière naturelle, travail à distance.
- **Direction abandonnée** : les illustrations à plat de l'ancienne DA (plantes, aplats bleu et corail). Ne pas les reproduire.

## Iconographie

- **Material Symbols, style Outlined** (Google Fonts), dans une pastille ronde (`radius-full`, 48 à 56 px) : blanc à 70 % sur une carte pastel, ou un pastel sur `surface` et `surface-alt`.
- Icône en `brand-blue` ou `ink`, de 24 à 30 px.
- Exemples tirés du site : menu_book, auto_awesome, fact_check, route, shield, query_stats, forum, check, verified_user, lock.
- **Puces de liste d'exercices** : une étoile à 4 branches en `brand-coral-strong` (voir ListeEtoiles).
- **Flèche d'action** : la flèche pleine du bouton 3D (voir LienFleche).
- Pas d'émoji.

## États et mouvement

- **Focus clavier** : `focus-ring`, visible au clavier seulement (focus-visible). Sur un fond bleu, l'anneau est blanc ; sur un bouton 3D, c'est un contour `brand-red` de 2 px décalé de 4 px.
- **Survol** :
  - les calques du bouton 3D s'écartent de 3 à 6 px ;
  - la flèche avance de 4 à 7 px ;
  - le bouton rond grossit à 105 % et tourne de -5°.
- **Durées** : environ 0,2 s. Tout mouvement s'arrête avec `prefers-reduced-motion`.
- **Inactif** : opacité 40 %, curseur interdit.
