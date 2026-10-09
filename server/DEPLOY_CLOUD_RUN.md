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
1. **Bouton "Charger un exemple"** : Remplit instantanément les notes avec un cas concret (Julien, carnet 5).
2. **"1. Analyser & Structurer"** : Appelle Gemini Flash pour découper les notes en 7 ou 8 pages calibrées. Vous pouvez retoucher le titre d'une page directement sur l'écran si nécessaire. Sans `GEMINI_API_KEY` (variable d'environnement ou fichier `.env`), un livret générique de secours est produit et un bandeau orange le signale.
3. **"Télécharger le Livret PDF"** : Compile et télécharge le livret PDF immédiatement en haute définition (AcroForm interactif, vectoriel, charte MDM).
4. **"🚀 Génération directe 1-Click"** : Prend les notes et télécharge le livret en un seul clic sans étape intermédiaire.

---

## 2. Déploiement sur Google Cloud Run (Clé en main)

Google Cloud Run permet d'héberger ce service gratuitement (dans le quota Free Tier mensuel de 2 millions de requêtes).

### Prérequis :
* Le SDK Google Cloud installé (`gcloud`).
* Un projet GCP actif avec facturation activée.

### Clé Gemini dans Secret Manager (à faire une fois)

La clé n'est jamais écrite dans la configuration Cloud Run : elle est rangée dans le secret `gemini-api-key`, et Cloud Run l'injecte au démarrage dans la variable d'environnement `GEMINI_API_KEY` que lit l'application. Ne jamais la passer avec `--set-env-vars` : elle serait lisible en clair par tout compte qui peut consulter le service, et recopiée dans chaque révision.

1. Créer la clé dans Google AI Studio (https://aistudio.google.com/api-keys, **Create API key**). Les nouvelles clés sont limitées à l'API Gemini par défaut.
2. Activer Secret Manager :
   ```bash
   gcloud services enable secretmanager.googleapis.com
   ```
3. Créer le secret dans la console (**Sécurité → Secret Manager → Créer un secret**), nom `gemini-api-key`, en collant la clé comme valeur, sans espace ni retour à la ligne final.
4. Autoriser le compte d'exécution du service (par défaut le compte Compute) à lire ce secret, et uniquement celui-là :
   ```bash
   gcloud secrets add-iam-policy-binding gemini-api-key --member=serviceAccount:<NUMÉRO_PROJET>-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor
   ```

### Commande de premier déploiement :

```bash
gcloud run deploy mdm-workbook-generator \
  --source . \
  --region europe-west1 \
  --no-allow-unauthenticated \
  --iap \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest \
  --memory 512Mi \
  --cpu 1
```

Pour vérifier qu'aucune clé n'est en clair, la variable doit apparaître comme une référence au secret (`secretKeyRef`), sans `value` :

```bash
gcloud run services describe mdm-workbook-generator --region europe-west1 --format="value(spec.template.spec.containers[0].env)"
```

### Changer de clé (rotation)

1. Créer une nouvelle clé dans AI Studio, sans supprimer l'ancienne.
2. Dans la console Secret Manager, ouvrir `gemini-api-key` et **Ajouter une version** avec la nouvelle clé.
3. Créer une nouvelle révision pour que les instances relisent le secret (il est lu au démarrage) :
   ```bash
   gcloud run services update mdm-workbook-generator --region europe-west1 --update-secrets GEMINI_API_KEY=gemini-api-key:latest
   ```
4. Lancer une analyse dans l'interface : pas de bandeau orange = la nouvelle clé fonctionne.
5. Supprimer l'ancienne clé dans AI Studio, puis désactiver l'ancienne version du secret.

> ⚠️ **Ne jamais ajouter `--allow-unauthenticated`** : ce flag donne le rôle d'invocation à `allUsers`, ce qui rend l'adresse `*.run.app` publique et contourne l'IAP. L'application n'a aucune authentification propre : toute la protection vient de l'IAP (section 3).

Variables d'environnement facultatives, modifiables sans toucher au code :
- `GEMINI_MODELS` : modèle Gemini utilisé (`gemini-3.8-flash` par défaut). Une liste séparée par des virgules fait essayer les modèles dans l'ordre.
- `GEMINI_TIMEOUT_S` : délai maximal d'un appel Gemini, en secondes (240 par défaut, sous les 300 s après lesquelles Cloud Run coupe la requête ; une analyse prend environ 30 s, le module création personnalisé environ 110 s). Au-delà, l'application passe au modèle de secours heuristique et l'interface affiche le bandeau orange.

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
2. Relancez le déploiement (Cloud Run conserve automatiquement toutes les configurations, variables d'environnement et références au secret existantes ; inutile de repasser la clé) :
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

