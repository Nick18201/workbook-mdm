# Direction Artistique (DA) - Workbook "Marge de Manœuvre"

Ce document sert de référence absolue pour le design des supports PDF, en respectant strictement la règle du "Zéro Noir".

## 1. Philosophie Visuelle : "Bullet Journal Professionnel"
L'esthétique globale est un hybride entre un carnet de développement personnel (Bullet Journal) et un livret de formation moderne.
*   **Ambiance** : Intime, bienveillante, créative mais structurée.
*   **Texture** : Le document doit donner une impression tactile de papier grâce à la trame de fond.
*   **Lumière** : L'ensemble est lumineux, fuyant les contrastes agressifs du noir pur au profit de teintes profondes et chaudes.

## 2. Palette Chromatique (Gamme "Zéro Noir")
Toutes les couleurs sombres sont des déclinaisons de bleu profond ou de gris coloré. **Interdiction d'utiliser le noir pur (#000000).**

| Rôle | Nom | Hex | Usage |
| :--- | :--- | :--- | :--- |
| **Fond Dominant** | **Nude / Blush** | `#FFF0E6` | Arrière-plan de toutes les pages de contenu et couverture. |
| **Couleur Principale** | **Indigo Électrique** | `#2F2EFA` | Titres principaux (H1), pages intercalaires (fonds pleins), feuilles graphiques, grille (transparence). |
| **Texte (Faux Noir)** | **Gunmetal** | `#2F2EFA` | Corps de texte, paragraphes, lignes fines de tableaux. (Aligné sur l'Indigo dans l'implémentation actuelle) |
| **Accent Vif** | **Rouge Vif** | `#FF4D4D` | Puces, sous-titres H2, formes géométriques d'ancrage. |
| **Lumière** | **Jaune Soleil** | `#FFEB3B` | Touches de lumière très ponctuelles. |
| **Neutre** | **Blanc Pur** | `#FFFFFF` | Textes sur fond bleu, cercles de respiration sur fond nude. |

## 3. Typographie
*   **Titres (Headings)** :
    *   *Police* : **Montserrat** (Black, Bold ou ExtraBold). Alternative : League Spartan.
    *   *Usage* : Grands titres (INTRODUCTION, FAIRE LE POINT).
    *   *Style* : Majuscules, Géométrique, Solide.
*   **Corps de texte (Body)** :
    *   *Police* : **Lato** (Regular et Italic). Alternative : Nunito Sans.
    *   *Usage* : Paragraphes de lecture.
    *   *Style* : Humaniste, aéré, lisible.
*   **Accents / Déco** :
    *   *Police* : **Amatic SC** ou **Caveat**.
    *   *Usage* : Citations, Logos, "Le mot d'accueil".
    *   *Style* : Manuscrit, humain.

## 4. Univers Graphique
*   **La Trame de Fond (Dot Grid)** :
    *   Indigo (`#2F2EFA`) à **20-30%** d'opacité (Plus visible).
*   **Formes Organiques (Feuilles)** :
    *   Flat design, sans contours.
    *   Compositions florales (Branches courbes).
*   **Card UI (Nouveau)** :
    *   Le contenu texte (Body) ne flotte plus sur le fond.
    *   Il est contenu dans une **Carte Blanche** aux coins arrondis, centrée sur la page.
    *   Ombre portée légère pour détacher la carte du fond Nude.

## 5. Structure des Pages Types
*   **Page de Couverture** : Fond Nude + Dot Grid. Cercle blanc, Feuilles, Carré rouge.
*   **Page Sommaire / "Au Programme"** : **Fond Indigo Plein (#2F2EFA)**. Texte Blanc. Puces vectorielles.
*   **Pages de Contenu (Mot d'accueil, etc.)** : Fond Nude + Dot Grid + **Carte Blanche** centrale contenant le texte.
