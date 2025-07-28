# 🚀 Guide de démarrage rapide - Smart Content Engine

## ⚡ Lancement en 3 étapes

### 1. Installation des dépendances

```bash
cd smart_content_engine
pip install -r requirements.txt
```

### 2. Configuration des API

Créez un fichier `.env` dans le dossier `smart_content_engine` :

```env
# Configuration des API
GOOGLE_API_KEY=your_google_api_key_here
LINKEDIN_ACCESS_TOKEN=your_linkedin_token_here

# Configuration LinkedIn (optionnel)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
```

### 3. Lancement de l'application

#### Option A: Script automatique

```bash
python run_streamlit.py
```

#### Option B: Lancement direct

```bash
streamlit run streamlit_app.py
```

#### Option C: Script Windows (mode clair)

Double-cliquez sur `launch.bat`

## 🌐 Accès à l'interface

L'application sera disponible à l'adresse : **http://localhost:8501**

**Note :** L'interface est configurée en mode clair par défaut pour une meilleure lisibilité.

## 📋 Utilisation

### Étape 1: Configuration Business

- Renseignez les informations de votre entreprise
- Sélectionnez votre secteur d'activité
- Définissez votre audience cible

### Étape 2: Préférences de Contenu

- Choisissez la langue (FR/EN)
- Sélectionnez le type de contenu
- Ajoutez un sujet spécifique (optionnel)

### Étape 3: Génération

- L'IA génère automatiquement le contenu
- Possibilité de régénérer si insatisfait

### Étape 4: Review

- Le contenu est reviewé pour qualité
- Possibilité de régénérer

### Étape 5: Image

- Génération d'image avec Stable Diffusion
- Possibilité de régénérer l'image

### Étape 6: Preview

- Aperçu réaliste du post LinkedIn
- Validation finale

### Étape 7: Publication

- Publication directe sur LinkedIn
- Ou sauvegarde pour publication manuelle

## 🎨 Interface en mode clair

L'interface est optimisée pour le mode clair avec :

- ✅ Fond blanc pour une meilleure lisibilité
- 🎯 Couleurs LinkedIn (bleu #0077b5)
- 📱 Design moderne et professionnel
- 🔄 Transitions fluides
- 💡 Ombres subtiles pour la profondeur

## 🔧 Dépannage

### Erreur de dépendances

```bash
pip install --upgrade -r requirements.txt
```

### Erreur de port

L'application utilise le port 8501. Si occupé, modifiez dans `streamlit_app.py` :

```python
st.set_page_config(..., port=8502)
```

### Erreur de clé API

- Vérifiez votre fichier `.env`
- Assurez-vous que les clés sont valides

### Forcer le mode clair

Si l'interface apparaît en mode sombre :

1. Utilisez le script `launch.bat`
2. Ou ajoutez `--theme.base light` à la commande streamlit

## 📱 Fonctionnalités

- ✅ Interface par étapes avec progression visuelle
- 🔄 Régénération de contenu et d'images
- 📱 Preview réaliste LinkedIn
- 🎨 Interface moderne en mode clair
- 💾 Sauvegarde automatique des données
- 🌟 Design professionnel optimisé

## 🆘 Support

En cas de problème :

1. Vérifiez les logs dans la console
2. Assurez-vous que toutes les dépendances sont installées
3. Vérifiez la configuration des API
4. Redémarrez l'application si nécessaire

---

**Prêt à créer du contenu LinkedIn professionnel en mode clair ! 🚀**
