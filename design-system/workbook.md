# Adapter au workbook

Propositions pour le générateur de carnets de bord. Elles ne viennent pas du site : elles appliquent ses règles au papier et au PDF, et restent à valider.

## Ce que sont les carnets

- **Sept carnets de bord**, du carnet 1 au carnet 7. Le carnet N prépare la séance N.
  - Carnet 1 · L'état des lieux (et les héritages)
  - Carnet 2 · Mon parcours
  - Carnet 3 · Mes fonctionnements propres
  - Carnet 4 · Mon rapport à l'argent
  - Carnet 5 · Valeurs et moteurs profonds
  - Carnet 6 · L'exploration
  - Carnet 7 · Confronter au terrain
- **Ensuite**, le carnet de route du temps 3, avec un module propre au projet : création ou reprise, reconversion, ou évolution interne.
- **Chaque carnet** contient un objectif, des exercices avec leur durée, et un livrable validé en séance avec la personne qui accompagne.
- **Ils se travaillent entre les séances.** Le composant PageCarnet montre comment le site présente un carnet.

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
- **Ouverture de carnet** :
  - `sourcil` « CARNET DE BORD · CARNET 4 » (« CARNET DE ROUTE » pour le carnet de route) ;
  - `numero` et sous-titre en `etiquette` ;
  - `titre-bloc`, puis l'objectif en `corps` ;
  - un encadré « EXERCICES & PROTOCOLES » en ListeEtoiles ;
  - trois lignes à icône : durée et découpage conseillé, cadre, mode d'emploi.
- **Page d'exercice** :
  - une `etiquette` « EXERCICE 2 · NOM · 20 MIN », puis la consigne en `corps` ;
  - des zones d'écriture sur `surface-card`, avec une bordure 1 px `line-strong` et un rayon `radius-bouton`, ou des lignes pointillées en `ink` à 25 % ;
  - les échelles et les jauges en pastilles `radius-full`.
- **Encadré** (conseil, rappel, exemple) : une CartePastel avec une Etiquette.
- **Exemple contrasté** : « En surface » sur `surface-card`, « Exploitable » sur une CartePastel, tirés d'un métier voisin.
- **Exercice à forte charge** : « AVANT DE COMMENCER » (avertissement et droit de laisser vierge), puis « POUR CLORE » (phrase d'ancrage).
- **Fin de carnet** : le PostIt « LIVRABLE » en `pastel-jasmine` et le Tampon « Validé en séance », avec la date et une case à cocher, puis trois zones courtes guidées.
- **Folio** en `sourcil`, par exemple « marge de manœuvre · carnet 4/7 · p. 12 » ou « marge de manœuvre · carnet de route · p. 4 ».

## Dosage

- Une seule touche faite main par page : un PostIt **ou** une Annotation.
- Un pastel dominant par carnet, pour s'y repérer d'un carnet à l'autre. Le texte posé dessus reste en `ink`. Il suit les temps du programme : `pastel-sky`, `pastel-lilac`, `pastel-mint`, `pastel-sky`, `pastel-lilac` pour les carnets 1 à 5, `pastel-almond` et `pastel-blush` pour les carnets 6 et 7, `pastel-jasmine` pour le carnet de route.
