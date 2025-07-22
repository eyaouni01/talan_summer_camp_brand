# ============================================================================
# 📄 core/content_reviewer.py
# ============================================================================
import os
import json
import google.generativeai as genai
from datetime import datetime
from typing import Dict, Optional

class ContentReviewer:
    """
    Reviewer intelligent de contenu business utilisant Gemini Flash
    """
    
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY manquant dans .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def review_business_content(self, content: str, preferences: Dict) -> Optional[str]:
        """
        Review et améliore le contenu business généré
        
        Args:
            content: Contenu à reviewer
            preferences: Préférences business
            
        Returns:
            str: Contenu business reviewé et optimisé
        """
        try:
            print("🔍 Début de la review du contenu business...")
            
            # Création du prompt de review business
            review_prompt = self._create_business_review_prompt(content, preferences)
            
            # Review avec Gemini Flash
            response = self.model.generate_content(review_prompt)
            
            if response and response.text:
                # Sauvegarde du contenu reviewé
                await self._save_reviewed_content(response.text, preferences)
                print("✅ Review business terminée avec succès")
                return response.text
            else:
                print("⚠️ Problème lors de la review, retour du contenu original")
                return content
                
        except Exception as e:
            print(f"❌ Erreur lors de la review business: {e}")
            return content
    
    def _create_business_review_prompt(self, content: str, preferences: Dict) -> str:
        """Crée un prompt de review spécialisé business"""
        language = preferences.get('language', 'fr')
        content_type = preferences.get('content_type', 'thought_leadership')
        business_sector = preferences.get('business_sector', 'technology')
        cta_type = preferences.get('cta_type', 'engagement')
        
        lang_text = "français" if language == 'fr' else "English"
        
        if language == 'fr':
            prompt = f"""
Tu es un expert en optimisation de contenu LinkedIn B2B et marketing business.

MISSION: Review et optimise ce post LinkedIn business selon les meilleures pratiques.

CONTENU À REVIEWER:
```
{content}
```

CONTEXTE BUSINESS:
- Secteur: {business_sector}
- Type: {content_type}
- Langue: {lang_text}
- Objectif CTA: {cta_type}

CRITÈRES DE REVIEW BUSINESS:

✅ STRUCTURE & LONGUEUR:
- Longueur optimale: 1000-1500 caractères
- Hook accrocheur dans les 2 premières lignes
- Structure claire: Hook + Développement + Insights + CTA
- Paragraphes courts (2-3 lignes max)

✅ CONTENU BUSINESS:
- Crédibilité professionnelle
- Valeur ajoutée concrète pour l'audience
- Insights actionnables
- Langage accessible mais expert
- Éviter le jargon excessif

✅ OPTIMISATION LINKEDIN:
- Emojis pertinents (4-6 maximum)
- Hashtags sectoriels (3-5 maximum)
- CTA adapté à l'objectif {cta_type}
- Format scannable sur mobile
- Engagement naturel encouragé

✅ QUALITÉ LINGUISTIQUE:
- Orthographe et grammaire parfaites
- Syntaxe fluide et professionnelle
- Ton cohérent avec le secteur {business_sector}

OPTIMISATIONS SPÉCIFIQUES:
- Renforce la crédibilité business
- Améliore l'engagement potentiel
- Optimise pour les algorithmes LinkedIn
- Assure la cohérence avec les standards du secteur

INSTRUCTIONS:
- Garde l'essence du message original
- Optimise sans changer le style fondamental
- Assure la conformité aux standards LinkedIn business
- Retourne UNIQUEMENT le contenu final optimisé

CONTENU BUSINESS OPTIMISÉ:
"""
        
        else:  # English
            prompt = f"""
You are an expert in LinkedIn B2B content optimization and business marketing.

MISSION: Review and optimize this business LinkedIn post according to best practices.

CONTENT TO REVIEW:
```
{content}
```

BUSINESS CONTEXT:
- Industry: {business_sector}
- Type: {content_type}
- Language: {lang_text}
- CTA objective: {cta_type}

BUSINESS REVIEW CRITERIA:

✅ STRUCTURE & LENGTH:
- Optimal length: 1000-1500 characters
- Catchy hook in first 2 lines
- Clear structure: Hook + Development + Insights + CTA
- Short paragraphs (2-3 lines max)

✅ BUSINESS CONTENT:
- Professional credibility
- Concrete value for audience
- Actionable insights
- Accessible yet expert language
- Avoid excessive jargon

✅ LINKEDIN OPTIMIZATION:
- Relevant emojis (4-6 maximum)
- Industry hashtags (3-5 maximum)
- CTA adapted to {cta_type} objective
- Mobile-scannable format
- Natural engagement encouraged

✅ LANGUAGE QUALITY:
- Perfect spelling and grammar
- Fluent and professional syntax
- Tone consistent with {business_sector} industry

SPECIFIC OPTIMIZATIONS:
- Strengthen business credibility
- Improve engagement potential
- Optimize for LinkedIn algorithms
- Ensure consistency with industry standards

INSTRUCTIONS:
- Keep the essence of the original message
- Optimize without changing fundamental style
- Ensure compliance with LinkedIn business standards
- Return ONLY the final optimized content

OPTIMIZED BUSINESS CONTENT:
"""
        
        return prompt
    
    async def _save_reviewed_content(self, content: str, preferences: Dict):
        """Sauvegarde le contenu business reviewé"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/reviewed_content/business_reviewed_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "content": content,
            "preferences": preferences,
            "status": "reviewed",
            "type": "business"
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)