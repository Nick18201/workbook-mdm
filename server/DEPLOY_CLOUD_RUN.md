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

* **Option A (Google IAP / Comptes Google)** : Activez Identity-Aware Proxy sur Cloud Run pour autoriser uniquement les adresses email de votre organisation / domaine.
* **Option B (Protection simple)** : Ajouter un mot de passe d'équipe partagé au niveau de l'interface web.
