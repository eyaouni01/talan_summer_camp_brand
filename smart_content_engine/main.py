# ============================================================================
# 📄 main.py
# ============================================================================
import os
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv

# Import des agents
from agents.content_agent import ContentAgent
from agents.reviewer_agent import ReviewerAgent
from agents.posting_agent import PostingAgent
from agents.trend_agent import TrendAgent

# Import des modules core
from core.content_generator import ContentGenerator
from linkedin_auth import LinkedInAuth

# Chargement des variables d'environnement
load_dotenv()

class SmartContentEngine:
    """
    Moteur principal de génération et publication de contenu business
    """
    
    def __init__(self):
        self.linkedin_auth = LinkedInAuth()
        
        # Agents MCP
        self.content_agent = ContentAgent()
        self.reviewer_agent = ReviewerAgent()
        self.posting_agent = PostingAgent()
        self.trend_agent = TrendAgent()
        
        # Création des dossiers nécessaires
        self._create_directories()
    
    def _create_directories(self):
        """Créer les dossiers nécessaires s'ils n'existent pas"""
        directories = [
            "data/trends",
            "data/generated_content", 
            "data/reviewed_content",
            "data/posted_content"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    async def get_business_info(self):
        """Collecte les informations business de l'utilisateur"""
        print("🏢 Configuration de votre business")
        print("=" * 40)
        
        # Nom de l'entreprise
        company_name = input("📛 Nom de votre entreprise: ").strip()
        while not company_name:
            company_name = input("❌ Nom requis. Nom de votre entreprise: ").strip()
        
        # Secteur d'activité
        print(f"\n🏭 Secteur d'activité:")
        sectors = {
            "1": "technology",
            "2": "marketing", 
            "3": "finance",
            "4": "consulting",
            "5": "healthcare",
            "6": "education",
            "7": "retail",
            "8": "manufacturing",
            "9": "real_estate",
            "10": "autre"
        }
        
        for key, value in sectors.items():
            print(f"{key}. {value.title()}")
        
        while True:
            sector_choice = input("\nChoisissez votre secteur (1-10): ").strip()
            if sector_choice in sectors:
                break
            print("❌ Choix invalide. Choisissez un nombre entre 1 et 10.")
        
        business_sector = sectors[sector_choice]
        if business_sector == "autre":
            business_sector = input("📝 Précisez votre secteur: ").strip()
        
        # Audience cible
        print(f"\n🎯 Votre audience cible:")
        audiences = {
            "1": "professionals",
            "2": "entrepreneurs", 
            "3": "executives",
            "4": "managers",
            "5": "consultants",
            "6": "freelancers"
        }
        
        for key, value in audiences.items():
            print(f"{key}. {value.title()}")
        
        while True:
            audience_choice = input("\nChoisissez votre audience (1-6): ").strip()
            if audience_choice in audiences:
                break
            print("❌ Choix invalide.")
        
        target_audience = audiences[audience_choice]
        
        # Taille de l'entreprise
        print(f"\n👥 Taille de votre entreprise:")
        print("1. Freelance/Solo")
        print("2. Startup (2-10 employés)")
        print("3. PME (11-50 employés)")
        print("4. Moyenne entreprise (51-250)")
        print("5. Grande entreprise (250+)")
        
        while True:
            size_choice = input("\nChoisissez la taille (1-5): ").strip()
            if size_choice in ["1", "2", "3", "4", "5"]:
                break
            print("❌ Choix invalide.")
        
        company_sizes = {
            "1": "freelance",
            "2": "startup", 
            "3": "sme",
            "4": "medium",
            "5": "enterprise"
        }
        company_size = company_sizes[size_choice]
        
        return {
            "company_name": company_name,
            "business_sector": business_sector,
            "target_audience": target_audience,
            "company_size": company_size
        }
    
    async def get_content_preferences(self):
        """Collecte les préférences de contenu"""
        print("\n📝 Préférences de contenu")
        print("=" * 30)
        
        # Langue
        print("🌐 Langue du contenu:")
        print("1. Français")
        print("2. English")
        
        while True:
            lang_choice = input("\nChoisissez la langue (1 ou 2): ").strip()
            if lang_choice in ["1", "2"]:
                break
            print("❌ Veuillez choisir 1 ou 2")
        
        language = "fr" if lang_choice == "1" else "en"
        
        # Type de contenu business
        print(f"\n📈 Type de contenu:")
        content_types = {
            "1": "thought_leadership",
            "2": "company_update",
            "3": "industry_insight",
            "4": "product_showcase",
            "5": "team_culture",
            "6": "educational"
        }
        
        descriptions = {
            "thought_leadership": "Leadership/Expertise",
            "company_update": "Actualités entreprise",
            "industry_insight": "Insights secteur",
            "product_showcase": "Produit/Service",
            "team_culture": "Équipe/Culture",
            "educational": "Éducatif/Conseils"
        }
        
        for key, value in content_types.items():
            desc = descriptions.get(value, value.title())
            print(f"{key}. {desc}")
        
        while True:
            content_choice = input("\nChoisissez le type (1-6): ").strip()
            if content_choice in content_types:
                break
            print("❌ Choix invalide.")
        
        content_type = content_types[content_choice]
        
        # Sujet spécifique
        topic = input(f"\n💡 Sujet spécifique (optionnel): ").strip()
        
        # Call-to-action
        print(f"\n🎯 Objectif du post:")
        print("1. Engagement (likes, commentaires)")
        print("2. Trafic vers site web")
        print("3. Génération de leads")
        print("4. Networking professionnel")
        print("5. Éducation/Sensibilisation")
        
        while True:
            cta_choice = input("\nChoisissez l'objectif (1-5): ").strip()
            if cta_choice in ["1", "2", "3", "4", "5"]:
                break
            print("❌ Choix invalide.")
        
        cta_types = {
            "1": "engagement",
            "2": "traffic",
            "3": "lead_gen",
            "4": "networking",
            "5": "education"
        }
        
        cta_type = cta_types[cta_choice]
        
        return {
            "language": language,
            "content_type": content_type,
            "topic": topic if topic else None,
            "cta_type": cta_type
        }
    
    async def setup_linkedin_auth(self):
        """Configure l'authentification LinkedIn si nécessaire"""
        access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        
        if not access_token:
            print("🔐 Configuration LinkedIn requise...")
            
            # Vérifier si un token est déjà sauvegardé
            saved_token = self.linkedin_auth.load_saved_token()
            if saved_token:
                print("✅ Token LinkedIn trouvé dans la sauvegarde")
                return saved_token
            
            # Demander authentification
            setup = input("📋 Voulez-vous configurer LinkedIn maintenant? (o/n): ").strip().lower()
            
            if setup in ['o', 'oui', 'y', 'yes']:
                token = self.linkedin_auth.authenticate()
                if token:
                    print("✅ LinkedIn configuré avec succès!")
                    return token
                else:
                    print("❌ Configuration LinkedIn échouée")
                    return None
            else:
                print("⚠️ Mode simulation activé (pas de publication réelle)")
                return None
        else:
            print("✅ Token LinkedIn trouvé dans .env")
            return access_token
    
    async def run_pipeline(self):
        """Exécute le pipeline complet de génération de contenu business"""
        print("🚀 Smart Content Engine - Business Edition")
        print("=" * 50)
        
        try:
            # Étape 0: Configuration LinkedIn
            linkedin_token = await self.setup_linkedin_auth()
            
            # Étape 1: Informations business
            business_info = await self.get_business_info()
            
            # Étape 2: Préférences contenu
            content_preferences = await self.get_content_preferences()
            
            # Fusion des configurations
            preferences = {**business_info, **content_preferences}
            preferences['linkedin_token'] = linkedin_token
            
            print(f"\n📊 CONFIGURATION:")
            print(f"🏢 {preferences['company_name']} ({preferences['company_size']})")
            print(f"🏭 {preferences['business_sector']}")
            print(f"🎯 {preferences['target_audience']}")
            print(f"📝 {preferences['content_type']} ({preferences['language']})")
            
            # Étape 3: Génération du contenu business
            print(f"\n📝 Génération du contenu business...")
            content = await self.content_agent.generate_business_content(preferences)
            
            if not content:
                print("❌ Échec de la génération de contenu")
                return
            
            print(f"✅ Contenu généré avec succès!")
            
            # Étape 4: Review du contenu
            print(f"\n🔍 Review du contenu business...")
            reviewed_content = await self.reviewer_agent.review_business_content(content, preferences)
            
            if not reviewed_content:
                print("❌ Échec de la review du contenu")
                return
                
            print(f"✅ Contenu reviewé avec succès!")
            
            # Affichage du contenu final
            print(f"\n📋 CONTENU BUSINESS FINAL:")
            print("=" * 50)
            print(reviewed_content)
            print("=" * 50)
            
            # Étape 5: Publication réelle sur LinkedIn
            if linkedin_token:
                publish = input(f"\n📤 Publier sur LinkedIn maintenant? (o/n): ").strip().lower()
                
                if publish in ['o', 'oui', 'y', 'yes']:
                    print("📤 Publication en cours sur LinkedIn...")
                    result =  await self.posting_agent.post_to_linkedin_real(reviewed_content, preferences)
                    if result:
                        print("✅ Contenu publié sur LinkedIn avec succès!")
                        print(f"🔗 URL du post: {result.get('post_url', 'Non disponible')}")
                    else:
                        print("❌ Échec de la publication sur LinkedIn")
                else:
                    print("📁 Contenu sauvegardé localement")
            else:
                print("⚠️ Publication ignorée (pas de token LinkedIn)")
                
        except Exception as e:
            print(f"❌ Erreur dans le pipeline: {e}")
            import traceback
            traceback.print_exc()

# Point d'entrée principal
async def main():
    """Fonction principale"""
    engine = SmartContentEngine()
    await engine.run_pipeline()

if __name__ == "__main__":
    asyncio.run(main())
