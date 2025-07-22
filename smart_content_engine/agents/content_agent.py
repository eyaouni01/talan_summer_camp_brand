# ============================================================================
# 📄 agents/content_agent.py
# ============================================================================
import asyncio
from core.content_generator import ContentGenerator
from typing import Dict, Optional

class ContentAgent:
    """
    Agent MCP pour la génération de contenu business
    """
    
    def __init__(self):
        self.content_generator = ContentGenerator()
    
    async def generate_business_content(self, preferences: Dict) -> Optional[str]:
        """
        Interface principale pour générer du contenu business
        
        Args:
            preferences: Préférences business utilisateur
            
        Returns:
            str: Contenu business généré
        """
        print("🤖 Agent Content Business: Démarrage de la génération...")
        
        # Génération contenu business
        content = await self.content_generator.generate_business_content(preferences)
        
        if content:
            print("✅ Agent Content Business: Contenu généré avec succès")
            return content
        else:
            print("❌ Agent Content Business: Échec de génération")
            return None
