# Conception du Workbook "Mon Livre de Transition" (MDM)

Ce document définit la structure, le contenu et la logique de génération du Workbook.
Chaque "Chapitre" est un fichier PDF généré automatiquement après que le bénéficiaire a rempli ses exercices en ligne.

## 📚 Structure Globale

Le Workbook final sera l'assemblage de ces composants :

1.  **Couverture Personnalisée** (Nom, Date de début, "Manifeste")
2.  **Introduction & Cadrage** (Le pacte d'engagement)
3.  **Chapitres Thématiques** (1 par étape clé, pas forcément 1 par séance)
4.  **Annexes & Boîte à Outils** (Fiches pratiques)

---

## 🧩 Détail des Chapitres

### 0. Le Prélude (Onboarding)
*   **Moment d'envoi** : Après signature du contrat.
*   **Contenu** :
    *   Mot de bienvenue.
    *   Rappel des objectifs (co-confruits lors du RDV découverte).
    *   Le "Cadre de Travail" (Engagement, Confidentialité, Logistique).
    *   **Action** : "Mon Intention" (Le bénéficiaire signe symboliquement son engagement).

### 1. Chapitre : L'État des Lieux (S1 - S2)
*   **Thème** : "D'où je pars".
*   **Inputs (Formulaires)** :
    *   Jeu des émotions (État d'esprit actuel).
    *   L'Objectif Boussole (Définition initiale).
    *   Le "Sac à dos" (Ce qui pèse, ce qui aide).
*   **Rendu Visuel** :
    *   Une page "Météo Intérieure".
    *   Un encart "Ma Boussole" mis en valeur graphiquement.

### 2. Chapitre : Mes Racines (S2 - S3)
*   **Thème** : "D'où je viens".
*   **Inputs** :
    *   La Ligne de Vie (Faits marquants, réussites, échecs).
    *   L'Héritage (Phrases marquantes des parents sur le travail).
    *   Figures d'inspiration (Qui j'admire et pourquoi).
*   **Rendu Visuel** :
    *   **Frise Chronologique** horizontale.
    *   Arbre ou schéma pour l'héritage familial.

### 3. Chapitre : Mon Identité (S3 - S4)
*   **Thème** : "Qui je suis".
*   **Inputs** :
    *   Synthèse MBTI (Les 4 lettres + description).
    *   Les résultats du 360° (Les mots des proches).
    *   Mes Moteurs (Top 3 des motivations intrinsèques).
*   **Rendu Visuel** :
    *   Nuage de mots (Wordcloud) généré à partir du 360°.
    *   Cartes "Talents" illustrées.

### 4. Chapitre : Ma Relation à l'Argent (S4 - S5)
*   **Thème** : "Mes Ressources".
*   **Inputs** :
    *   Archétype Financier (Le profil dominant).
    *   La Lettre à l'Argent (Texte intégral).
*   **Rendu Visuel** :
    *   Mise en page type "Manuscrit" pour la lettre.
    *   Fiche "Mon Archétype" avec ses forces et ses défis.

### 5. Chapitre : Mes Valeurs (S4 - S5)
*   **Thème** : "Mes Moteurs Profonds".
*   **Inputs (Formulaires)** :
    *   Expériences d'alignement et de désalignement.
    *   Choix difficiles et hiérarchisation des valeurs.
    *   Traduction en conditions de travail et tensions de valeurs.
*   **Rendu Visuel** :
    *   Liste hiérarchisée des valeurs.
    *   Cartes des "3 valeurs non négociables".
    *   Tableau des conditions de travail et tensions.

### 6. Chapitre : Phase d'exploration (S5)
*   **Thème** : "Mes Pistes Métiers & Cartographie".
*   **Inputs** :
    *   Cartographie personnelle (MBTI, Ce que j'aime, Envies).
    *   Le retour des proches (Secteurs/métiers, avis, vécu).
    *   10 fiches métiers (5 "no limit", 5 "réalistes").
*   **Rendu Visuel** :
    *   Cartographie sous forme de cartes (MBTI, Activités, Envies).
    *   Blocs retours de l'entourage.
    *   Fiches métiers structurées.

### 7. Chapitre : Le Champ des Possibles (S5 - S6)
*   **Thème** : "Où je vais".
*   **Inputs (Formulaires)** :
    *   Les pistes explorées (Plan A, Plan B).
    *   Retour des Enquêtes Métier (Ce que j'ai appris).
    *   Matrice de Faisabilité (Feu rouge/orange/vert).
*   **Rendu Visuel** :
    *   Tableau comparatif des pistes.
    *   Checklist de faisabilité.

### 8. Chapitre : La Feuille de Route (S7)
*   **Thème** : "Comment j'y vais".
*   **Inputs** :
    *   Le Plan d'Action (Les grandes étapes à 6 mois).
    *   Le "Pas de côté" (Ce que je ne ferai plus).
*   **Rendu Visuel** :
    *   Calendrier / Roadmap visuelle.
    *   Engagement final (Signature).

---

## 🎨 Identité Visuelle (Idées)

*   **Format** : A4 vertical (facile à imprimer) ou A4 Paysage (plus "présentation"). -> *Recommandation : A4 Paysage pour les timelines et tableaux.*
*   **Style** :
    *   Minimaliste & Élégant.
    *   Utilisation d'icônes fines (Line art).
    *   Couleurs douces (Pastels ou Terre) pour favoriser l'introspection.
*   **Typographie** :
    *   Titres : Serif (ex: Playfair Display) pour le côté "Livre/Récit".
    *   Corps : Sans-Serif (ex: Inter ou Lato) pour la lisibilité.

## 🛠️ Stack Technique Proposée

1.  **Collecte** : **Tally.so** (Gratuit, illimité, très beau design, pas de branding agressif).
2.  **Base de Données** : **Airtable** ou **Google Sheets** (Pour stocker les réponses et les traiter).
3.  **Génération PDF** :
    *   Option A (Robuste) : **Documer** ou **PDFMonkey** (Templates HTML/CSS).
    *   Option B (Simple) : **Google Docs + Variables** (Via Make).
4.  **Envoi** : **Gmail** (Via Make).
