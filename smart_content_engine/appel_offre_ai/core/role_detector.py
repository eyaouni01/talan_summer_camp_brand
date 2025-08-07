#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Détecteur de rôles basé sur l'IA pour analyser les besoins d'un projet
"""

import os
import sys
from pathlib import Path

# Configuration pour Google Generative AI
try:
    import google.generativeai as genai
    from config import MODEL_NAME, GOOGLE_API_KEY
    
    # Configuration de l'API
    genai.configure(api_key=GOOGLE_API_KEY)
    GEMINI_AVAILABLE = True
    
except ImportError:
    print("⚠️ Google Generative AI non disponible")
    GEMINI_AVAILABLE = False
except Exception as e:
    print(f"⚠️ Erreur configuration Gemini: {e}")
    GEMINI_AVAILABLE = False

def load_prompt(path="prompts/generate_roles_prompt.txt"):
    """
    Charge le template de prompt depuis un fichier
    
    Args:
        path (str): Chemin vers le fichier de prompt
        
    Returns:
        str: Template de prompt ou prompt par défaut
    """
    try:
        # Essayer le chemin relatif depuis le dossier courant
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        
        # Essayer depuis le dossier parent
        parent_path = os.path.join("..", path)
        if os.path.exists(parent_path):
            with open(parent_path, "r", encoding="utf-8") as f:
                return f.read()
        
        # Créer le prompt par défaut si le fichier n'existe pas
        print(f"⚠️ Fichier prompt non trouvé: {path}")
        return create_default_prompt()
        
    except Exception as e:
        print(f"❌ Erreur lecture prompt: {e}")
        return create_default_prompt()

def create_default_prompt():
    """
    Crée un prompt par défaut pour la détection de rôles
    
    Returns:
        str: Prompt par défaut
    """
    return """
Analysez cette description de projet et identifiez les rôles/compétences nécessaires pour le mener à bien.

PROJET À ANALYSER:
{{DESCRIPTION}}

Fournissez une analyse détaillée incluant:

1. RÔLES TECHNIQUES NÉCESSAIRES:
   - Développeurs (précisez les technologies)
   - Data Scientists / Analystes
   - DevOps / Infrastructure
   - Architectes techniques
   - Autres spécialistes techniques

2. RÔLES MÉTIER/GESTION:
   - Product Manager
   - Project Manager
   - Business Analyst
   - UX/UI Designer
   - Autres rôles métier

3. COMPÉTENCES TRANSVERSALES:
   - Technologies spécifiques requises
   - Soft skills importantes
   - Certifications ou expériences préférées

4. PRIORITÉS DE RECRUTEMENT:
   - Rôles critiques à recruter en premier
   - Rôles qui peuvent être recrutés plus tard
   - Possibilités de polyvalence

Pour chaque rôle, indiquez:
- Les responsabilités principales
- Les compétences techniques requises
- Le niveau d'expérience souhaité
- L'urgence de recrutement (Critique/Important/Souhaitable)

Soyez spécifique et pratique dans vos recommandations.
"""

def detect_roles(description: str) -> str:
    """
    Détecte les rôles nécessaires pour un projet via IA
    
    Args:
        description (str): Description du projet
        
    Returns:
        str: Analyse des rôles nécessaires
    """
    print("🤖 Analyse des rôles nécessaires...")
    
    try:
        if GEMINI_AVAILABLE:
            return detect_roles_gemini(description)
        else:
            return detect_roles_fallback(description)
            
    except Exception as e:
        print(f"❌ Erreur détection rôles: {e}")
        return detect_roles_fallback(description)

def detect_roles_gemini(description: str) -> str:
    """
    Détection via Google Gemini
    
    Args:
        description (str): Description du projet
        
    Returns:
        str: Analyse des rôles
    """
    try:
        # Charger et préparer le prompt
        prompt_template = load_prompt()
        prompt = prompt_template.replace("{{DESCRIPTION}}", description)
        
        # Initialiser le modèle
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Configuration de génération
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        print("🔄 Génération via Gemini...")
        
        # Générer la réponse
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        if response and response.text:
            print("✅ Analyse générée avec succès")
            return response.text.strip()
        else:
            print("⚠️ Réponse vide de Gemini")
            return detect_roles_fallback(description)
            
    except Exception as e:
        print(f"❌ Erreur Gemini: {e}")
        return detect_roles_fallback(description)

def detect_roles_fallback(description: str) -> str:
    """
    Analyse de fallback basée sur des mots-clés
    
    Args:
        description (str): Description du projet
        
    Returns:
        str: Analyse basique des rôles
    """
    print("🔄 Analyse par mots-clés (fallback)...")
    
    # Analyse par mots-clés
    desc_lower = description.lower()
    
    # Détection des technologies/domaines
    tech_keywords = {
        "web": ["web", "site", "application web", "frontend", "backend"],
        "mobile": ["mobile", "app", "android", "ios", "react native"],
        "data": ["data", "données", "analyse", "machine learning", "ia", "ai", "analytics"],
        "cloud": ["cloud", "aws", "azure", "gcp", "infrastructure", "devops"],
        "design": ["design", "ux", "ui", "interface", "expérience utilisateur"],
        "ecommerce": ["e-commerce", "vente", "boutique", "commande", "paiement"],
        "fintech": ["finance", "fintech", "banque", "paiement", "transaction"],
        "saas": ["saas", "software as a service", "plateforme", "abonnement"]
    }
    
    detected_domains = []
    for domain, keywords in tech_keywords.items():
        if any(keyword in desc_lower for keyword in keywords):
            detected_domains.append(domain)
    
    # Génération de l'analyse basée sur les domaines détectés
    analysis = f"""
🎯 ANALYSE DU PROJET
Description: {description[:200]}{'...' if len(description) > 200 else ''}

🔍 DOMAINES DÉTECTÉS: {', '.join(detected_domains) if detected_domains else 'Généraliste'}

📋 RÔLES RECOMMANDÉS:

🔧 RÔLES TECHNIQUES CRITIQUES:
"""
    
    # Recommandations basées sur les domaines
    if "web" in detected_domains:
        analysis += """
• Développeur Full-Stack (React/Vue.js + Python/Node.js)
  - Développement frontend et backend
  - Intégration API et bases de données
  - Urgence: CRITIQUE

• Développeur Frontend (React/Vue.js)
  - Interface utilisateur responsive
  - Expérience utilisateur optimisée
  - Urgence: IMPORTANT
"""
    
    if "mobile" in detected_domains:
        analysis += """
• Développeur Mobile (React Native/Flutter)
  - Applications iOS et Android
  - Intégration services natifs
  - Urgence: IMPORTANT
"""
    
    if "data" in detected_domains:
        analysis += """
• Data Scientist / Analyst
  - Analyse de données et ML
  - Python, SQL, frameworks ML
  - Urgence: CRITIQUE

• Data Engineer
  - Pipeline de données
  - ETL et infrastructure data
  - Urgence: IMPORTANT
"""
    
    if "cloud" in detected_domains or "devops" in desc_lower:
        analysis += """
• DevOps Engineer
  - Infrastructure cloud (AWS/Azure/GCP)
  - CI/CD et automatisation
  - Urgence: IMPORTANT
"""
    
    # Rôles métier universels
    analysis += """

👥 RÔLES MÉTIER ESSENTIELS:

• Product Manager
  - Vision produit et roadmap
  - Coordination des équipes
  - Urgence: CRITIQUE

• UX/UI Designer
  - Design d'interface et expérience
  - Prototypage et tests utilisateurs
  - Urgence: IMPORTANT

• Project Manager / Scrum Master
  - Gestion de projet agile
  - Coordination et planning
  - Urgence: SOUHAITABLE

🎯 COMPÉTENCES TRANSVERSALES RECHERCHÉES:
• Expérience en méthodologies agiles
• Esprit d'équipe et communication
• Capacité d'adaptation et d'innovation
• Orientation résultats

📈 PLAN DE RECRUTEMENT SUGGÉRÉ:
1. PHASE 1 (Critique): Product Manager, Développeur principal
2. PHASE 2 (Important): Designer, Développeur complémentaire
3. PHASE 3 (Souhaitable): DevOps, Rôles spécialisés
"""
    
    return analysis

def create_prompt_file():
    """
    Crée le fichier de prompt par défaut s'il n'existe pas
    """
    prompt_dir = "prompts"
    prompt_file = os.path.join(prompt_dir, "generate_roles_prompt.txt")
    
    if not os.path.exists(prompt_file):
        os.makedirs(prompt_dir, exist_ok=True)
        
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(create_default_prompt())
        
        print(f"📁 Fichier prompt créé: {prompt_file}")

def test_role_detection():
    """
    Teste la détection de rôles avec différents exemples
    """
    print("🧪 === TEST DÉTECTION DE RÔLES ===")
    
    test_projects = [
        {
            "name": "E-commerce avec IA",
            "description": "Développement d'une plateforme e-commerce avec système de recommandation par intelligence artificielle, interface mobile et web, paiements sécurisés et analytics avancés."
        },
        {
            "name": "App Fintech Mobile",
            "description": "Application mobile de gestion financière personnelle avec budgeting automatique, investissements, et tableau de bord en temps réel."
        },
        {
            "name": "Plateforme SaaS B2B",
            "description": "Plateforme SaaS pour la gestion de projets d'équipes distribuées avec collaboration en temps réel, intégrations multiples et dashboard analytique."
        }
    ]
    
    for i, project in enumerate(test_projects, 1):
        print(f"\n📝 Test {i}/{len(test_projects)}: {project['name']}")
        print(f"📋 Description: {project['description']}")
        
        try:
            roles = detect_roles(project['description'])
            print(f"✅ Analyse générée ({len(roles)} caractères)")
            print(f"📊 Aperçu: {roles[:200]}...")
            
        except Exception as e:
            print(f"❌ Erreur pour {project['name']}: {e}")
    
    print("\n🏁 Tests terminés")

# Initialisation
def initialize_role_detector():
    """
    Initialise le détecteur de rôles
    """
    print("🔧 Initialisation du détecteur de rôles...")
    
    # Créer le fichier de prompt si nécessaire
    create_prompt_file()
    
    # Vérifier la configuration
    if GEMINI_AVAILABLE:
        print("✅ Google Gemini configuré")
    else:
        print("⚠️ Mode fallback (analyse par mots-clés)")
    
    print("✔️ Détecteur de rôles prêt")

if __name__ == "__main__":
    initialize_role_detector()
    test_role_detection()