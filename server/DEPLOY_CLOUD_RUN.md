# Guide de Déploiement : Cloud Run & Lancement Local

Ce guide vous explique comment lancer l'interface web en local et comment la déployer sur **Google Cloud Run** pour que vos collègues puissent l'utiliser depuis n'importe où.

---

## 1. Lancement en Local (Pour tester immédiatement)

Depuis la racine du projet, lancez simplement :

```powershell
python -m uvicorn server.app:app --port 8080 --reload
```

Ouvrez ensuite votre navigateur sur :
👉 **`http://localhost:8080`**

### Fonctionnalités disponibles sur l'interface :
1. **Bouton "Charger un exemple"** : Remplit instantanément les notes avec un cas concret (Julien, Chapitre 4).
2. **"1. Analyser & Structurer"** : Appelle Gemini Flash pour découper les notes en 7 ou 8 pages calibrées. Vous pouvez retoucher le titre d'une page directement sur l'écran si nécessaire.
3. **"Télécharger le Livret PDF"** : Compile et télécharge le livret PDF immédiatement en haute définition (AcroForm interactif, vectoriel, charte MDM).
4. **"🚀 Génération directe 1-Click"** : Prend les notes et télécharge le livret en un seul clic sans étape intermédiaire.

---

## 2. Déploiement sur Google Cloud Run (Clé en main)

Google Cloud Run permet d'héberger ce service gratuitement (dans le quota Free Tier mensuel de 2 millions de requêtes).

### Prérequis :
* Le SDK Google Cloud installé (`gcloud`).
* Un projet GCP actif avec facturation activée.

### Commande de déploiement en 1 ligne :

```bash
gcloud run deploy mdm-workbook-generator \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY="VOTRE_CLE_API_GEMINI" \
  --memory 1Gi \
  --cpu 1
```

### Ce que fait cette commande automatiquement :
1. Envoie le code vers Google Cloud Build.
2. Construit l'image Docker à partir de notre `Dockerfile` optimisé.
3. Déploie le conteneur sur Cloud Run dans la région Europe (Belgique).
4. Vous fournit instantanément une **URL HTTPS sécurisée** du type :  
   `https://mdm-workbook-generator-xxxx-ew.a.run.app`

---

## 3. Sécuriser l'accès pour vos collègues (Options)

Si vous ne souhaitez pas que l'outil soit ouvert au grand public (`--no-allow-unauthenticated`) :

* **Option A (Google IAP / Comptes Google)** : Identity-Aware Proxy sur Cloud Run restreint l'accès aux membres autorisés (@margedemanoeuvre.fr).
* **Option B (Protection simple)** : Mot de passe d'équipe partagé au niveau de l'interface web.

---

## 4. Mettre à jour l'application après une modification sur GitHub

### Méthode 1 : Mise à jour manuelle rapide (2 commandes dans Cloud Shell)

Dès que vous avez poussé (`git push`) du nouveau code sur GitHub :

1. Ouvrez votre Cloud Shell et tapez :
   ```bash
   cd ~/workbook-mdm
   git pull
   ```
2. Relancez le déploiement (Cloud Run conserve automatiquement toutes les configurations et variables d'environnement existantes) :
   ```bash
   gcloud run deploy mdm-workbook-generator --source . --region europe-west1
   ```
   *En 1 à 2 minutes, la nouvelle version est en ligne sans coupure de service !*

---

### Méthode 2 : Déploiement automatique continu (CI/CD GitHub)

Si vous voulez que **chaque `git push` déclenche le redéploiement automatiquement** sans ouvrir Cloud Shell :

1. Rendez-vous sur la console Cloud Run :  
   👉 **[console.cloud.google.com/run?project=mdm-workbooks-2026](https://console.cloud.google.com/run?project=mdm-workbooks-2026)**
2. Cliquez sur votre service `mdm-workbook-generator`.
3. En haut, cliquez sur **"Configurer la livraison continue"** (Set up Continuous Deployment).
4. Connectez votre compte GitHub et sélectionnez votre dépôt `Nick18201/workbook-mdm`.
5. Sélectionnez la branche `main` et le type de compilation **Dockerfile**.
6. Cliquez sur Enregistrer. Désormais, chaque push déploie automatiquement la nouvelle version.

