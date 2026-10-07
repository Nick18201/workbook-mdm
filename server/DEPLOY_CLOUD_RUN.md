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
2. **"1. Analyser & Structurer"** : Appelle Gemini Flash pour découper les notes en 7 ou 8 pages calibrées. Vous pouvez retoucher le titre d'une page directement sur l'écran si nécessaire. Sans `GEMINI_API_KEY` (variable d'environnement ou fichier `.env`), un livret générique de secours est produit et un bandeau orange le signale.
3. **"Télécharger le Livret PDF"** : Compile et télécharge le livret PDF immédiatement en haute définition (AcroForm interactif, vectoriel, charte MDM).
4. **"🚀 Génération directe 1-Click"** : Prend les notes et télécharge le livret en un seul clic sans étape intermédiaire.

---

## 2. Déploiement sur Google Cloud Run (Clé en main)

Google Cloud Run permet d'héberger ce service gratuitement (dans le quota Free Tier mensuel de 2 millions de requêtes).

### Prérequis :
* Le SDK Google Cloud installé (`gcloud`).
* Un projet GCP actif avec facturation activée.

### Commande de premier déploiement :

```bash
gcloud run deploy mdm-workbook-generator \
  --source . \
  --region europe-west1 \
  --no-allow-unauthenticated \
  --iap \
  --set-env-vars GEMINI_API_KEY="VOTRE_CLE_API_GEMINI" \
  --memory 512Mi \
  --cpu 1
```

> ⚠️ **Ne jamais ajouter `--allow-unauthenticated`** : ce flag donne le rôle d'invocation à `allUsers`, ce qui rend l'adresse `*.run.app` publique et contourne l'IAP. L'application n'a aucune authentification propre : toute la protection vient de l'IAP (section 3).

Variable d'environnement facultative : `GEMINI_MODELS` (liste séparée par des virgules) pour changer les modèles Gemini essayés dans l'ordre, sans modifier le code.

### Ce que fait cette commande automatiquement :
1. Envoie le code vers Google Cloud Build.
2. Construit l'image Docker à partir de notre `Dockerfile` optimisé.
3. Déploie le conteneur sur Cloud Run dans la région Europe (Belgique), avec l'IAP activé.
4. Vous fournit une **URL HTTPS** du type :  
   `https://mdm-workbook-generator-xxxx-ew.a.run.app`

---

## 3. Contrôle d'accès (IAP)

Le service est protégé par **Identity-Aware Proxy activé directement sur Cloud Run** : toute requête, API comprise, passe par une connexion Google, et seuls les comptes **@margedemanoeuvre.fr** sont autorisés.

Configuration attendue :
* L'invocation Cloud Run (`roles/run.invoker`) n'est accordée qu'à l'agent de service IAP (`service-<NUMÉRO_PROJET>@gcp-sa-iap.iam.gserviceaccount.com`), jamais à `allUsers` ni `allAuthenticatedUsers`.
* L'accès IAP (`roles/iap.httpsResourceAccessor`) est accordé à `domain:margedemanoeuvre.fr`.

Pour l'accorder au domaine (à faire une fois) :

```bash
gcloud iap web add-iam-policy-binding --resource-type=cloud-run --service=mdm-workbook-generator --region=europe-west1 --member=domain:margedemanoeuvre.fr --role=roles/iap.httpsResourceAccessor
```

Pour vérifier (aucune ligne ne doit contenir `allUsers` ni `allAuthenticatedUsers`) :

```bash
gcloud run services get-iam-policy mdm-workbook-generator --region europe-west1
```

```bash
gcloud iap web get-iam-policy --resource-type=cloud-run --service=mdm-workbook-generator --region=europe-west1
```

Test rapide : ouvrir `https://<url>/api/templates` dans une fenêtre de navigation privée doit afficher l'écran de connexion Google, et non du JSON.

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

