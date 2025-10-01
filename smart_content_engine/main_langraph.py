# ============================================================================
# 📄 main.py - Version adaptée pour orchestration LangGraph
# ============================================================================
import os
import asyncio
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import des agents
from agents.content_agent import ContentAgent
from agents.reviewer_agent import ReviewerAgent
from agents.posting_agent import PostingAgent
from agents.trend_agent import TrendAgent

# Import des modules core
from core.content_generator import ContentGenerator
from linkedin_auth import LinkedInAuth
from facebook_auth import FacebookAuth

from agents.agent_image_prompt import generate_image_prompt
from core.image_generator import ImageGenerator

# Import du scheduler
from scheduler import ContentScheduler

# Chargement des variables d'environnement
load_dotenv()

class SmartContentEngine:
    """
    Moteur principal de génération et publication de contenu business
    Support LinkedIn, Facebook et publication programmée
    Orchestration avec LangGraph
    """
    
    def __init__(self, preferences=None):
        """
        Initialisation avec préférences optionnelles (pour LangGraph)
        
        Args:
            preferences (dict): Préférences business depuis LangGraph state
        """
        self.preferences = preferences  # Ajout pour LangGraph
        
        self.linkedin_auth = LinkedInAuth()
        self.facebook_auth = FacebookAuth()
        
        # Agents MCP
        self.content_agent = ContentAgent()
        self.reviewer_agent = ReviewerAgent()
        self.posting_agent = PostingAgent()
        self.trend_agent = TrendAgent()
        
        # Scheduler pour publication programmée
        self.scheduler = ContentScheduler()
        
        # Création des dossiers nécessaires
        self._create_directories()
    
    def _create_directories(self):
        """Créer les dossiers nécessaires s'ils n'existent pas"""
        directories = [
            "data/trends",
            "data/generated_content", 
            "data/reviewed_content",
            "data/posted_content",
            "data/scheduled_posts",
            "assets"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    async def get_business_info(self) -> dict:
        """
        Récupère les infos business - soit depuis LangGraph state, soit depuis user input
        """
        if self.preferences and all(k in self.preferences for k in ["company_name", "business_sector", "target_audience", "company_size"]):
            # Mode orchestration LangGraph
            print("📊 Utilisation des informations business depuis LangGraph state")
            return {
                "company_name": self.preferences.get("company_name"),
                "business_sector": self.preferences.get("business_sector"),
                "target_audience": self.preferences.get("target_audience"),
                "company_size": self.preferences.get("company_size")
            }
        else:
            # Mode standalone - collecte interactive
            return await self._collect_business_info_interactive()
    
    async def _collect_business_info_interactive(self):
        """Collecte interactive des informations business (code original)"""
        print("🏢 Configuration de votre business")
        print("=" * 40)
        
        # Nom de l'entreprise
        company_name = input("📛 Nom de votre entreprise: ").strip()
        while not company_name:
            company_name = input("❌ Nom requis. Nom de votre entreprise: ").strip()
        
        # Secteur d'activité
        print(f"\n🏭 Secteur d'activité:")
        sectors = {
            "1": "technology", "2": "marketing", "3": "finance", "4": "consulting",
            "5": "healthcare", "6": "education", "7": "retail", "8": "manufacturing",
            "9": "real_estate", "10": "autre"
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
            "1": "professionals", "2": "entrepreneurs", "3": "executives",
            "4": "managers", "5": "consultants", "6": "freelancers",
            "7": "customers", "8": "community"
        }
        
        for key, value in audiences.items():
            print(f"{key}. {value.title()}")
        
        while True:
            audience_choice = input("\nChoisissez votre audience (1-8): ").strip()
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
            "1": "freelance", "2": "startup", "3": "sme", "4": "medium", "5": "enterprise"
        }
        company_size = company_sizes[size_choice]
        
        return {
            "company_name": company_name,
            "business_sector": business_sector,
            "target_audience": target_audience,
            "company_size": company_size
        }

    async def get_publication_mode(self):
        """Choix entre publication immédiate ou programmée"""
        print("\n📅 Mode de publication")
        print("=" * 30)
        print("1. Publication immédiate")
        print("2. Publication programmée")
        
        while True:
            choice = input("\nChoisissez le mode (1 ou 2): ").strip()
            if choice in ["1", "2"]:
                break
            print("❌ Veuillez choisir 1 ou 2")
        
        return "immediate" if choice == "1" else "scheduled"
    
    async def get_schedule_datetime(self):
        """Collecte la date/heure de publication programmée"""
        print("\n⏰ Programmation de la publication")
        print("=" * 35)
        print("1. Dans 1 heure")
        print("2. Dans 2 heures")
        print("3. Dans 6 heures")
        print("4. Demain à 9h00")
        print("5. Demain à 14h00")
        print("6. Date/heure personnalisée")
        
        while True:
            choice = input("\nChoisissez l'option (1-6): ").strip()
            
            if choice == "1":
                return datetime.now() + timedelta(hours=1)
            elif choice == "2":
                return datetime.now() + timedelta(hours=2)
            elif choice == "3":
                return datetime.now() + timedelta(hours=6)
            elif choice == "4":
                tomorrow = datetime.now() + timedelta(days=1)
                return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            elif choice == "5":
                tomorrow = datetime.now() + timedelta(days=1)
                return tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
            elif choice == "6":
                try:
                    date_str = input("📅 Date (DD/MM/YYYY): ").strip()
                    time_str = input("🕐 Heure (HH:MM): ").strip()
                    
                    day, month, year = map(int, date_str.split('/'))
                    hour, minute = map(int, time_str.split(':'))
                    
                    schedule_time = datetime(year, month, day, hour, minute)
                    
                    if schedule_time <= datetime.now():
                        print("❌ La date doit être dans le futur")
                        continue
                    
                    return schedule_time
                except ValueError:
                    print("❌ Format invalide. Utilisez DD/MM/YYYY et HH:MM")
                    continue
            else:
                print("❌ Choix invalide")
    
    async def get_platform_choice(self):
        """Permet de choisir la plateforme de publication"""
        print("🌐 Choix de la plateforme de publication")
        print("=" * 40)
        print("1. LinkedIn seulement")
        print("2. Facebook seulement") 
        print("3. LinkedIn + Facebook (publication croisée)")
        
        while True:
            choice = input("\nChoisissez votre plateforme (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                break
            print("❌ Choix invalide. Choisissez 1, 2 ou 3.")
        
        return {
            "1": {"linkedin": True, "facebook": False},
            "2": {"linkedin": False, "facebook": True},
            "3": {"linkedin": True, "facebook": True}
        }[choice]
    
    async def get_content_preferences(self, platforms):
        """Collecte les préférences de contenu selon les plateformes choisies"""
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
        
        # Type de contenu business adapté aux plateformes
        print(f"\n📈 Type de contenu:")
        if platforms["facebook"]:
            content_types = {
                "1": "thought_leadership", "2": "company_update", "3": "industry_insight",
                "4": "product_showcase", "5": "team_culture", "6": "educational",
                "7": "promotional", "8": "community_event"
            }
        else:
            content_types = {
                "1": "thought_leadership", "2": "company_update", "3": "industry_insight",
                "4": "product_showcase", "5": "team_culture", "6": "educational"
            }
        
        descriptions = {
            "thought_leadership": "Leadership/Expertise", "company_update": "Actualités entreprise",
            "industry_insight": "Insights secteur", "product_showcase": "Produit/Service",
            "team_culture": "Équipe/Culture", "educational": "Éducatif/Conseils",
            "promotional": "Promotionnel/Marketing", "community_event": "Événement communauté"
        }
        
        for key, value in content_types.items():
            desc = descriptions.get(value, value.title())
            print(f"{key}. {desc}")
        
        max_choice = len(content_types)
        while True:
            content_choice = input(f"\nChoisissez le type (1-{max_choice}): ").strip()
            if content_choice in content_types:
                break
            print("❌ Choix invalide.")
        
        content_type = content_types[content_choice]
        
        # Sujet spécifique
        topic = input(f"\n💡 Sujet spécifique (optionnel): ").strip()
        
        # Call-to-action
        print(f"\n🎯 Objectif du post:")
        cta_options = ["1. Engagement", "2. Trafic vers site web", "3. Génération de leads",
                      "4. Networking professionnel", "5. Éducation/Sensibilisation"]
        if platforms["facebook"]:
            cta_options.extend(["6. Ventes/Conversion", "7. Notoriété de marque"])
        
        for option in cta_options:
            print(option)
        
        max_cta = 7 if platforms["facebook"] else 5
        while True:
            cta_choice = input(f"\nChoisissez l'objectif (1-{max_cta}): ").strip()
            if cta_choice in [str(i) for i in range(1, max_cta + 1)]:
                break
            print("❌ Choix invalide.")
        
        cta_types = {
            "1": "engagement", "2": "traffic", "3": "lead_gen", "4": "networking",
            "5": "education", "6": "sales", "7": "brand_awareness"
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
            saved_token = self.linkedin_auth.load_saved_token()
            if saved_token:
                print("✅ Token LinkedIn trouvé dans la sauvegarde")
                return saved_token
            
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
                print("⚠️ Mode simulation LinkedIn activé")
                return None
        else:
            print("✅ Token LinkedIn trouvé dans .env")
            return access_token
    
    async def setup_facebook_auth(self):
        """Configure l'authentification Facebook si nécessaire"""
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        
        if not access_token:
            print("🔐 Configuration Facebook requise...")
            saved_token = self.facebook_auth.load_saved_token()
            if saved_token:
                print("✅ Token Facebook trouvé dans la sauvegarde")
                return saved_token
            
            setup = input("📋 Voulez-vous configurer Facebook maintenant? (o/n): ").strip().lower()
            if setup in ['o', 'oui', 'y', 'yes']:
                token = self.facebook_auth.authenticate()
                if token:
                    print("✅ Facebook configuré avec succès!")
                    return token
                else:
                    print("❌ Configuration Facebook échouée")
                    return None
            else:
                print("⚠️ Mode simulation Facebook activé")
                return None
        else:
            print("✅ Token Facebook trouvé dans .env")
            return access_token
    
    # ... [Le reste des méthodes restent identiques]
    
    async def run_pipeline(self):
        """Exécute le pipeline complet avec orchestration LangGraph"""
        print("🚀 Smart Content Engine - LangGraph Orchestration")
        print("=" * 70)
        
        try:
            # Mode détection
            if self.preferences:
                print("🔗 Mode orchestration LangGraph détecté")
            else:
                print("🎛️ Mode standalone détecté")
            
            # Étape 0: Mode de publication
            publication_mode = await self.get_publication_mode()
            
            # Étape 1: Choix des plateformes
            platforms = await self.get_platform_choice()
            
            # Configuration authentification
            linkedin_token = None
            facebook_token = None
            
            if platforms["linkedin"]:
                linkedin_token = await self.setup_linkedin_auth()
            
            if platforms["facebook"]:
                facebook_token = await self.setup_facebook_auth()
            
            # Étape 2: Informations business (orchestrées ou interactives)
            business_info = await self.get_business_info()
            
            # Étape 3: Préférences contenu (toujours interactives)
            content_preferences = await self.get_content_preferences(platforms)
            
            # Fusion des configurations
            preferences = {**business_info, **content_preferences}
            preferences['linkedin_token'] = linkedin_token
            preferences['facebook_token'] = facebook_token
            preferences['platforms'] = platforms
            
            print(f"\n📊 CONFIGURATION:")
            print(f"🏢 {preferences['company_name']} ({preferences['company_size']})")
            print(f"🏭 {preferences['business_sector']}")
            print(f"🎯 {preferences['target_audience']}")
            print(f"📝 {preferences['content_type']} ({preferences['language']})")
            
            selected_platforms = []
            if platforms["linkedin"]: selected_platforms.append("LinkedIn")
            if platforms["facebook"]: selected_platforms.append("Facebook")
            print(f"🌐 Plateformes: {' + '.join(selected_platforms)}")
            print(f"📅 Mode: {'Publication immédiate' if publication_mode == 'immediate' else 'Publication programmée'}")
            
            # Suite du pipeline (génération, review, image, publication)
            # [Le reste du code reste identique...]
            
            # Génération du contenu
            print(f"\n📝 Génération du contenu business...")
            
            if platforms["facebook"] and not platforms["linkedin"]:
                preferences['platform_style'] = 'facebook'
                preferences['content_style'] = 'conversational'
            elif platforms["linkedin"] and platforms["facebook"]:
                preferences['platform_style'] = 'hybrid'
                preferences['content_style'] = 'professional_friendly'
            else:
                preferences['platform_style'] = 'linkedin'
                preferences['content_style'] = 'professional'
            
            content = await self.content_agent.generate_business_content(preferences)
            
            if not content:
                print("❌ Échec de la génération de contenu")
                return
            
            print(f"✅ Contenu généré avec succès!")
            
            # Review du contenu
            print(f"\n🔍 Review du contenu business...")
            reviewed_content = await self.reviewer_agent.review_business_content(content, preferences)
            
            if not reviewed_content:
                print("❌ Échec de la review du contenu")
                return
            
            print(f"✅ Contenu reviewé avec succès!")
            
            # Génération du prompt d'image
            print("🧠 Génération du prompt d'image depuis le contenu validé...")
            prompt_image = generate_image_prompt(reviewed_content, preferences)
            print(f"📌 Prompt généré : {prompt_image}")
            
            # Générer l'image
            print("\n🎨 Génération de l'image...")
            image_generator = ImageGenerator()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"assets/generated_image_{timestamp}.png"
            
            image_generator.generate_image(prompt_image, output_path=image_path, num_inference_steps=20, width=512, height=512)
            
            print(f"✅ Image enregistrée dans {image_path}")
            
            if os.path.exists(image_path):
                print(f"🖼️ Image générée: {image_path}")
            else:
                print(f"⚠️ Attention: Image non trouvée à {image_path}")
                image_path = None
            
            # Affichage du contenu final
            print(f"\n📋 CONTENU BUSINESS FINAL:")
            print("=" * 50)
            print(reviewed_content)
            print("=" * 50)
            
            # Publication selon le mode choisi
            if publication_mode == "immediate":
                await self._handle_immediate_publication(reviewed_content, image_path, preferences, platforms, linkedin_token, facebook_token)
            else:
                await self._handle_scheduled_publication(reviewed_content, image_path, preferences, platforms)
                
        except Exception as e:
            print(f"❌ Erreur dans le pipeline: {e}")
            import traceback
            traceback.print_exc()

# Fonction d'interface pour LangGraph
async def run_content_engine_with_state(state: dict) -> dict:
    """
    Interface pour LangGraph - fonction d'orchestration
    
    Args:
        state: Dict contenant les informations business depuis LangGraph
    
    Returns:
        dict: Résultats de l'exécution
    """
    try:
        # Extraction des préférences business depuis le state
        business_preferences = {
            "company_name": state.get("company_name"),
            "business_sector": state.get("business_sector"),
            "target_audience": state.get("target_audience"),
            "company_size": state.get("company_size")
        }
        
        # Création de l'engine avec les préférences
        engine = SmartContentEngine(preferences=business_preferences)
        
        # Exécution du pipeline
        await engine.run_pipeline()
        
        return {
            "status": "success",
            "message": "Pipeline content engine exécuté avec succès"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erreur dans l'exécution: {str(e)}"
        }

# Point d'entrée principal (mode standalone)
async def main():
    """Fonction principale - mode standalone"""
    engine = SmartContentEngine()
    await engine.run_pipeline()

if __name__ == "__main__":
    asyncio.run(main())