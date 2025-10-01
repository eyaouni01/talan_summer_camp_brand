# ============================================================================
# 📄 core/content_generator.py
# ============================================================================
import os
import json
import google.generativeai as genai
from datetime import datetime
from typing import Dict, Optional

class ContentGenerator:
    """
    Générateur de contenu business intelligent utilisant Gemini Flash
    """
    
    def __init__(self):
        # Configuration de Gemini Flash
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY manquant dans .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    async def generate_business_content(self, preferences: Dict) -> Optional[str]:
        """
        Génère du contenu business optimisé
        
        Args:
            preferences: Dict contenant les préférences business
            
        Returns:
            str: Contenu généré ou None en cas d'erreur
        """
        try:
            print("🤖 Génération en cours avec Gemini Flash...")
            
            # Création du prompt business
            prompt = self._create_business_prompt(preferences)
            
            # Génération avec Gemini Flash
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # Sauvegarde du contenu généré
                await self._save_generated_content(response.text, preferences)
                print("✅ Contenu généré avec succès!")
                return response.text
            else:
                print("❌ Pas de contenu généré par Gemini")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return None
    
    def _create_business_prompt(self, preferences: Dict) -> str:
        """Crée un prompt business optimisé pour Gemini Flash"""
        language = preferences.get('language', 'fr')
        content_type = preferences.get('content_type', 'thought_leadership')
        topic = preferences.get('topic', '')
        cta_type = preferences.get('cta_type', 'engagement')
        business_sector = preferences.get('business_sector', 'technology')
        company_name = preferences.get('company_name', 'Notre entreprise')
        target_audience = preferences.get('target_audience', 'professionals')
        company_size = preferences.get('company_size', 'medium')
        
        lang_text = "français" if language == 'fr' else "English"
        
        # Adaptation du ton selon la taille d'entreprise
        if language == 'fr':
            tones = {
                "freelance": "Personnel et authentique",
                "startup": "Dynamique et innovant",
                "sme": "Professionnel et accessible", 
                "medium": "Expert et crédible",
                "enterprise": "Autoritaire et institutionnel"
            }
        else:
            tones = {
                "freelance": "Personal and authentic",
                "startup": "Dynamic and innovative",
                "sme": "Professional and accessible",
                "medium": "Expert and credible", 
                "enterprise": "Authoritative and institutional"
            }
        
        voice_tone = tones.get(company_size, tones["medium"])
        
        if language == 'fr':
            prompt = f"""
Tu es un expert en content marketing B2B et LinkedIn pour les entreprises.

MISSION: Créer un post LinkedIn business professionnel en {lang_text}.

CONTEXTE BUSINESS:
- Entreprise: {company_name}
- Secteur: {business_sector}
- Audience: {target_audience}
- Type de contenu: {content_type}
- Sujet spécifique: {topic if topic else 'Sujet libre dans le secteur'}
- Objectif CTA: {cta_type}
- Taille entreprise: {company_size}
- Ton: {voice_tone}

EXIGENCES STRICTES:
✅ Longueur: 1000-1500 caractères maximum
✅ Ton: {voice_tone}
✅ Structure: Hook + Développement + Insights + CTA
✅ Emojis: 4-6 emojis pertinents et professionnels
✅ Hashtags: 3-5 hashtags sectoriels pertinents
✅ Crédibilité: Basé sur des insights réels du secteur
✅ Valeur ajoutée: Information utile pour l'audience

STYLE BUSINESS:
- Parler en tant qu'expert du secteur
- Partager des insights concrets et actionnables
- Utiliser des données/statistiques si pertinent
- Créer de l'engagement authentique
- Éviter le jargon excessif
- Favoriser la discussion professionnelle

CTA selon l'objectif {cta_type}:
- engagement: "Qu'en pensez-vous? Partagez votre expérience en commentaire."
- traffic: "Lien vers notre analyse complète en commentaire."
- lead_gen: "DM pour échanger sur votre situation."
- networking: "Mentionnez quelqu'un qui devrait voir ça."
- education: Question ouverte pour susciter réflexion

GÉNÈRE LE POST BUSINESS:
"""
        
        else:  # English
            prompt = f"""
You are a B2B content marketing and LinkedIn expert for businesses.

MISSION: Create a professional business LinkedIn post in {lang_text}.

BUSINESS CONTEXT:
- Company: {company_name}
- Industry: {business_sector}
- Audience: {target_audience}
- Content type: {content_type}
- Specific topic: {topic if topic else 'Free topic within the industry'}
- CTA objective: {cta_type}
- Company size: {company_size}
- Tone: {voice_tone}

STRICT REQUIREMENTS:
✅ Length: 1000-1500 characters maximum
✅ Tone: {voice_tone}
✅ Structure: Hook + Development + Insights + CTA
✅ Emojis: 4-6 relevant and professional emojis
✅ Hashtags: 3-5 relevant industry hashtags
✅ Credibility: Based on real industry insights
✅ Value: Useful information for the audience

BUSINESS STYLE:
- Speak as an industry expert
- Share concrete and actionable insights
- Use data/statistics when relevant
- Create authentic engagement
- Avoid excessive jargon
- Foster professional discussion

CTA according to {cta_type} objective:
- engagement: "What do you think? Share your experience in the comments."
- traffic: "Link to our complete analysis in comments."
- lead_gen: "DM to discuss your situation."
- networking: "Tag someone who should see this."
- education: Open question to spark reflection

GENERATE THE BUSINESS POST:
"""
        
        return prompt
    
    async def _save_generated_content(self, content: str, preferences: Dict):
        """Sauvegarde le contenu généré"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/generated_content/business_content_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "content": content,
            "preferences": preferences,
            "status": "generated",
            "type": "business"
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)