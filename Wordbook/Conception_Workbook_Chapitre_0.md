# Workbook - Chapitre 0 : Le Prélude 🕯️
*Ce document sert de spécification pour le contenu textuel, le formulaire de collecte et le rendu PDF.*

---

## 1. Concept & Objectif
*   **Moment** : Envoyé immédiatement après la signature du contrat et le paiement.
*   **Objectif** : Accueillir, rassurer, engager solennellement ("Onboarding rituel").
*   **Ton** : Chaleureux, solennel, professionnel, encourageant.

## 2. Structure du PDF (Rendu Final)

### Page 1 : La Couverture
*   **Visuel** : Fond épuré, typographie élégante.
*   **Textes** :
    *   Titre : "MON LIVRE DE TRANSITION"
    *   Sous-titre : "Bilan de Compétences & Alignement Professionnel"
    *   Variable : `[Prénom] [Nom]`
    *   Variable : `[Date de Démarrage]`

### Page 2 : Bienvenue (Édito)
*   **Titre** : "Bienvenue [Prénom],"
*   **Corps** :
    > "Si vous lisez ceci, c’est que vous avez choisi de vous mettre en mouvement. Bravo.
    > Ce livre n'est pas un simple rapport. C'est le réceptacle de votre histoire, de vos découvertes et de vos ambitions.
    > Il va s'écrire page après page, au rythme de notre travail.
    > Aujourd'hui, nous posons la première pierre."

### Page 3 : Le Cadre de Confiance (Le Pacte)
*   **Concept** : Une version "noble" des règles du jeu.
*   **Les 3 Piliers** :
    1.  **Confidentialité** : "Tout ce qui se dit ici, reste ici."
    2.  **Authenticité** : "Pas de masque. C'est votre vérité qui compte."
    3.  **Action** : "La clarté vient du mouvement, pas seulement de la pensée."

### Page 4 : Mon Intention (Formulaire à Remplir)
*   **Titre** : "Mon Engagement Envers Moi-même"
*   **Champs Interactifs** :
    *   "Moi, `[Champ Texte : Prénom]`..."
    *   "...décide aujourd'hui d'investir `[Champ Texte : Heures]` heures par semaine pour mon avenir."
    *   "Mon objectif principal est de : `[Champ Texte Multi-lignes : Objectif]`."
    *   "Pour réussir, je m'autorise à : `[Champ Texte Multi-lignes : Autorisation]`."
*   **Validation** : Case à cocher "Je m'engage solennellement".
*   **Signature** : Champ libre pour la date et le lieu.

---

## 3. Données à Collecter (Champs PDF)

Ce document est un **PDF Interactif** envoyé au bénéficiaire.

**Zone 1 : Identité**
*   Champ : `nom_complet`

**Zone 2 : La Boussole**
*   Champ : `objectif_3_mois` (Question : "Quelle serait votre situation idéale à la fin de ce bilan ?")

**Zone 3 : Le Pacte**
*   Champ : `engagement_hebdo` (Nombre d'heures)
*   Champ : `permission_personnelle` (Quelle autorisation vous donnez-vous ?)

---

## 4. Instructions Techniques (Automation Google Workspace)

1.  **Envoi** : Le bénéficiaire reçoit le `Workbook_Chap0_Interactive.pdf` par email.
2.  **Remplissage** : Le bénéficiaire remplit le PDF sur son poste.
3.  **Retour** :
    *   Option A : Upload via Google Form.
    *   Option B : Envoi à `intersession@margedemanoeuvre...`.
4.  **Traitement (Google Workspace)** :
    *   Trigger : Réception du fichier (Drive ou Gmail).
    *   App Script : Extraction des données du formulaire PDF (parsing des champs).
    *   Stockage : Mise à jour de la fiche bénéficiaire (Sheet/Doc).
