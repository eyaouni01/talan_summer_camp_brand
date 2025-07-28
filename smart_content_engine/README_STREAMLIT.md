# 🚀 Smart Content Engine - Interface Streamlit

## 📋 Description

Interface graphique moderne pour la création de contenu LinkedIn business avec des étapes guidées et des effets visuels.

## ✨ Fonctionnalités

### 🎯 Interface par étapes

- **Étape 1**: Configuration business (entreprise, secteur, audience)
- **Étape 2**: Préférences de contenu (langue, type, objectif)
- **Étape 3**: Génération de contenu avec IA
- **Étape 4**: Review automatique du contenu
- **Étape 5**: Génération d'image avec Stable Diffusion
- **Étape 6**: Preview LinkedIn avant publication
- **Étape 7**: Publication sur LinkedIn

### 🎨 Effets visuels

- ✅ Indicateurs de progression pour chaque étape
- 🔄 Boutons de régénération pour le contenu et les images
- 📱 Preview réaliste du post LinkedIn
- 🎯 Interface moderne et intuitive

### 🔄 Fonctionnalités de régénération

- Régénération du contenu si insatisfait
- Régénération de l'image si insatisfait
- Retour en arrière entre les étapes
- Sauvegarde automatique des données

## 🚀 Installation et lancement

### Méthode 1: Script automatique (Recommandé)

```bash
cd smart_content_engine
python run_streamlit.py
```

### Méthode 2: Lancement manuel

```bash
cd smart_content_engine
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## ⚙️ Configuration

### 1. Fichier .env

Créez un fichier `.env` dans le dossier `smart_content_engine` :

```env
# Configuration des API
GOOGLE_API_KEY=your_google_api_key_here
LINKEDIN_ACCESS_TOKEN=your_linkedin_token_here

# Configuration LinkedIn (optionnel)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
```

### 2. Obtenir les clés API

#### Google API Key (pour Gemini)

1. Allez sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Créez un nouveau projet
3. Générez une clé API
4. Ajoutez-la dans votre fichier `.env`

#### LinkedIn Access Token

1. Utilisez l'interface Streamlit pour configurer LinkedIn
2. Ou suivez la documentation LinkedIn API

## 📱 Utilisation

### 1. Configuration Business

- Renseignez les informations de votre entreprise
- Sélectionnez votre secteur d'activité
- Définissez votre audience cible
- Choisissez la taille de votre entreprise

### 2. Préférences de Contenu

- Sélectionnez la langue (FR/EN)
- Choisissez le type de contenu
- Ajoutez un sujet spécifique (optionnel)
- Définissez l'objectif du post

### 3. Génération et Review

- L'IA génère automatiquement le contenu
- Le contenu est reviewé pour qualité et pertinence
- Possibilité de régénérer si insatisfait

### 4. Génération d'Image

- L'IA génère un prompt d'image basé sur le contenu
- Stable Diffusion crée une image personnalisée
- Possibilité de régénérer l'image

### 5. Preview et Publication

- Aperçu réaliste du post LinkedIn
- Validation finale avant publication
- Publication directe sur LinkedIn

## 🎨 Personnalisation

### CSS personnalisé

L'interface utilise du CSS personnalisé pour :

- Indicateurs de progression
- Preview LinkedIn réaliste
- Boutons de régénération stylisés
- Effets visuels modernes

### Thèmes

L'interface s'adapte automatiquement au thème de votre navigateur (clair/sombre).

## 🔧 Dépannage

### Problèmes courants

#### 1. Erreur de dépendances

```bash
pip install -r requirements.txt
```

#### 2. Erreur de clé API

- Vérifiez votre fichier `.env`
- Assurez-vous que les clés API sont valides

#### 3. Erreur de génération d'image

- Vérifiez l'espace disque disponible
- Assurez-vous que Stable Diffusion est configuré

#### 4. Erreur de publication LinkedIn

- Vérifiez votre token LinkedIn
- Assurez-vous que les permissions sont correctes

### Logs

Les logs sont affichés directement dans l'interface Streamlit pour faciliter le débogage.

## 📊 Fonctionnalités avancées

### Sauvegarde automatique

- Les données sont sauvegardées à chaque étape
- Possibilité de reprendre une session interrompue

### Export de données

- Contenu généré sauvegardé localement
- Images générées dans le dossier `assets/`

### Intégration complète

- Utilise tous les agents existants
- Compatible avec l'architecture actuelle
- Pas de modification du code existant

## 🎯 Avantages de l'interface Streamlit

1. **Interface intuitive** : Pas besoin de connaissances techniques
2. **Étapes guidées** : Processus clair et structuré
3. **Feedback visuel** : Progression et statuts en temps réel
4. **Régénération facile** : Boutons pour régénérer contenu et images
5. **Preview réaliste** : Aperçu exact du post LinkedIn
6. **Responsive** : Fonctionne sur tous les appareils

## 🔮 Évolutions futures

- [ ] Support multi-langues pour l'interface
- [ ] Templates de posts prédéfinis
- [ ] Historique des posts créés
- [ ] Analytics de performance
- [ ] Intégration avec d'autres réseaux sociaux

---

**Développé avec ❤️ pour simplifier la création de contenu LinkedIn business**
