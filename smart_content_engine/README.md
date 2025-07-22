# 🚀 Smart Content Engine - Business Edition

Moteur intelligent de génération et publication de contenu LinkedIn B2B avec posting **RÉEL** via l'API LinkedIn officielle.

## 🎯 Fonctionnalités Principales

### ✅ Génération de Contenu Business
- **Configuration dynamique** : Questionnaire intelligent pour adapter le contenu
- **Multi-secteurs** : Technology, Marketing, Finance, Consulting, Healthcare, etc.
- **Multi-langues** : Français et Anglais avec adaptation culturelle
- **Types de contenu** : Thought Leadership, Company Updates, Industry Insights, etc.
- **Personnalisation** : Adaptation selon la taille d'entreprise et l'audience

### ✅ Publication LinkedIn Réelle
- **API LinkedIn officielle** : Publication directe sur votre profil
- **Authentification OAuth2** : Processus sécurisé et guidé
- **Sauvegarde automatique** : Historique de toutes les publications
- **Mode simulation** : Test sans publication réelle

### ✅ Intelligence Artificielle
- **Gemini Flash** : Génération de contenu gratuite et performante
- **Review automatique** : Optimisation par IA experte business
- **Templates sectoriels** : Structures adaptées par industrie
- **CTA optimisés** : Calls-to-action selon l'objectif business

## 🛠️ Installation Rapide

### 1. Prérequis
```bash
Python 3.8+
pip install -r requirements.txt
```

### 2. Configuration API

#### Google Gemini (OBLIGATOIRE - GRATUIT)
1. Aller sur https://aistudio.google.com/
2. Créer compte → Générer API key
3. Ajouter dans `.env`: `GOOGLE_API_KEY=votre_cle`

#### LinkedIn API (OPTIONNEL)
1. Créer app sur https://developer.linkedin.com/
2. Configurer OAuth2 avec redirect: `http://localhost:8000/callback`
3. Ajouter Client ID et Secret dans `.env`


### 3. Structure des Fichiers
```
smart_content_engine/
├── 📄 main.py                    # Point d'entrée principal
├── 📄 linkedin_auth.py           # Authentification LinkedIn
├── 📄 requirements.txt           # Dépendances Python
├── 📄 .env                       # Configuration API
├── 📁 agents/                    # Agents MCP
│   ├── content_agent.py          # Génération contenu
│   ├── reviewer_agent.py         # Review et optimisation
│   ├── posting_agent.py          # Publication LinkedIn
│   └── trend_agent.py            # Collecte trends (futur)
├── 📁 core/                      # Moteurs principaux
│   ├── content_generator.py      # IA génération
│   ├── content_reviewer.py       # IA review
│   ├── linkedin_poster.py        # API LinkedIn
│   └── trend_collector.py        # Collecteur trends
├── 📁 templates/                 # Templates business
│   ├── business_templates_fr.json
│   └── business_templates_en.json
├── 📁 config/                    # Configuration
│   ├── apis.yaml
│   └── prompts.yaml
└── 📁 data/                      # Données générées
    ├── generated_content/
    ├── reviewed_content/
    └── posted_content/
```

## 🚀 Utilisation

### Lancement
```bash
python main.py
```

### Workflow Automatisé
1. **Configuration Business** 
   - Nom entreprise, secteur, taille, audience
2. **Préférences Contenu**
   - Type, langue, sujet, objectif CTA
3. **Génération IA**
   - Contenu personnalisé avec Gemini Flash
4. **Review Automatique**
   - Optimisation par IA experte business
5. **Publication LinkedIn**
   - Option publication réelle ou simulation

## 📊 Types de Contenu Supportés

### 🎯 Thought Leadership
- Partage d'expertise sectorielle
- Insights basés sur l'expérience
- Analyses de tendances
- Conseils stratégiques

### 📢 Company Updates
- Annonces produits/services
- Milestones entreprise
- Actualités corporate
- Recrutement

### 📈 Industry Insights
- Analyses de marché
- Prédictions sectorielles
- Benchmarks industrie
- Signaux faibles

### 🏢 Team & Culture
- Présentation équipe
- Valeurs d'entreprise
- Success stories
- Philosophie business

### 📚 Educational
- Guides pratiques
- Tips & astuces
- Tutoriels
- Décryptages

## 🎨 Adaptation Intelligente

### Selon la Taille d'Entreprise
- **Freelance** : Ton personnel et authentique
- **Startup** : Dynamique et innovant
- **PME** : Professionnel et accessible
- **Grande entreprise** : Autoritaire et institutionnel

### Selon l'Objectif CTA
- **Engagement** : Questions pour discussion
- **Traffic** : Redirection vers contenus
- **Lead Gen** : Invitation au contact
- **Networking** : Expansion du réseau

### Selon la Langue
- **Français** : Adaptation culturelle française
- **English** : Ton international business

## 📈 Performance & Métriques

### Vitesse de Génération
- **Contenu** : 5-10 secondes
- **Review** : 3-5 secondes  
- **Publication** : 2-3 secondes
- **Total** : ~15 secondes de bout en bout

### Qualité Assurée
- Templates testés par secteur
- Review par IA experte LinkedIn
- Optimisation algorithmique
- Format mobile-first

### Coûts
- **Gemini Flash** : Gratuit (1M tokens/jour)
- **LinkedIn API** : Gratuit (100 posts/jour)
- **Total** : 100% gratuit pour usage standard

## 🔐 Sécurité & Données

### Authentification
- OAuth2 LinkedIn standard
- Tokens stockés localement
- Pas de données sur serveurs externes

### Sauvegarde
- Historique complet des publications
- Timestamps et métadonnées
- Format JSON facilement exploitable

### Conformité
- Respect des limites API LinkedIn
- Guidelines LinkedIn Business
- RGPD compliance

## 🚨 Guide de Démarrage Rapide

### Étape 1 : Installation (2 minutes)
```bash
git clone [repository]
cd smart_content_engine
pip install -r requirements.txt
```

### Étape 2 : Configuration Gemini (2 minutes)
1. https://aistudio.google.com/ → Créer API key
2. `.env` → `GOOGLE_API_KEY=votre_cle`

### Étape 3 : Test Immédiat (1 minute)
```bash
python main.py
```

### Étape 4 : LinkedIn (optionnel - 15 minutes)
1. https://developer.linkedin.com/ → Créer app
2. Configurer OAuth2
3. Ajouter credentials dans `.env`

## 🆘 Support & Dépannage

### Erreurs Communes
- **"GOOGLE_API_KEY manquant"** → Vérifier `.env`
- **"LinkedIn auth failed"** → Vérifier OAuth2 config
- **"No content generated"** → Vérifier connexion internet

### Logs & Debug
- Tous les fichiers générés dans `data/`
- Messages d'erreur détaillés
- Historique des publications

### Performance
- Requêtes Gemini limitées à 15/minute
- Publications LinkedIn limitées à 100/jour
- Sauvegarde automatique de tous les contenus

---
