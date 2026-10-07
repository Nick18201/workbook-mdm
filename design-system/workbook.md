# Adapter au workbook

Propositions pour le générateur de carnets de bord. Elles ne viennent pas du site : elles appliquent ses règles au papier et au PDF, et restent à valider.

## Ce que sont les carnets

- **Le tronc commun** : 7 carnets, chapitres 0 à 6.
  - Le Prélude
  - L'État des lieux
  - Mon parcours
  - Mes fonctionnements propres (MBTI®)
  - Mon rapport à l'argent
  - Valeurs & moteurs profonds
  - Phase d'exploration
- **Ensuite**, un carnet de route propre au projet : reconversion, création ou reprise, ou évolution interne.
- **Chaque carnet** contient un objectif, 4 exercices ou protocoles, et un livrable validé en séance avec la personne qui accompagne.
- **Ils se travaillent entre les séances.** Le composant PageCarnet montre comment le site présente un chapitre.

## Impression

- **Tailles** :
  - `corps` : 10 à 11 pt, interligne d'environ 1,5 ;
  - titres (`titre-section`) : 28 à 40 pt ;
  - `sourcil` : 8 à 9 pt ;
  - `annotation` : 12 pt au moins.
- **Couleurs** : les tokens sont des couleurs d'écran (RVB). `brand-blue` et `brand-coral` sont très saturés et risquent de ternir en CMJN : faire un test d'impression avant de valider.
- **Noir et blanc** : les bénéficiaires impriment parfois en noir et blanc. La hiérarchie ne tient jamais à la seule couleur : `sourcil`, `numero` et filets doivent rester lisibles en gris.

## Gabarits

- **Couverture** :
  - fond `surface` et logotype ;
  - le `numero` du carnet en `brand-blue` ;
  - le titre en `titre-section` avec un mot en `brand-coral` (« Mon rapport *à l'argent.* ») ;
  - un disque pastel coupé par le bord ;
  - un post-it qui porte la promesse du carnet.
- **Ouverture de chapitre** :
  - `sourcil` « CARNET DE BORD · CHAPITRE 4 » ;
  - `numero` et sous-titre en `etiquette` ;
  - `titre-bloc`, puis l'objectif en `corps` ;
  - un encadré « EXERCICES & PROTOCOLES » en ListeEtoiles.
- **Page d'exercice** :
  - une `etiquette` « EXERCICE 2 · 20 MIN », puis la consigne en `corps` ;
  - des zones d'écriture sur `surface-card`, avec une bordure 1 px `line-strong` et un rayon `radius-bouton`, ou des lignes pointillées en `ink` à 25 % ;
  - les échelles et les jauges en pastilles `radius-full`.
- **Encadré** (conseil, rappel, exemple) : une CartePastel avec une Etiquette.
- **Fin de carnet** : le PostIt « LIVRABLE » en `pastel-jasmine` et le Tampon « Validé en séance », avec la date et une case à cocher.
- **Folio** en `sourcil`, par exemple « marge de manœuvre · carnet 4/7 · p. 12 ».

## Dosage

- Une seule touche faite main par page : un PostIt **ou** une Annotation.
- Un pastel dominant par carnet, pour s'y repérer d'un carnet à l'autre. Le texte posé dessus reste en `ink`.
