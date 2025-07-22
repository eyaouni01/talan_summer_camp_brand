# ============================================================================
# 📄 agents/posting_agent.py
# ============================================================================
from core.linkedin_poster import LinkedInPoster
from typing import Dict, Optional

class PostingAgent:
    """
    Agent MCP pour la publication LinkedIn RÉELLE
    """
    
    def __init__(self):
        self.linkedin_poster = LinkedInPoster()
    
    async def post_to_linkedin_real(self, content: str, preferences: Dict) -> Optional[Dict]:
        """
        Interface principale pour publier RÉELLEMENT sur LinkedIn
        
        Args:
            content: Contenu à publier
            preferences: Préférences contenant le token LinkedIn
            
        Returns:
            dict: Résultat de la publication ou None
        """
        print("🤖 Agent Posting: Démarrage de la publication RÉELLE...")
        
        access_token = preferences.get('linkedin_token')
        
        if not access_token:
            print("❌ Token LinkedIn manquant - Impossible de publier")
            return None
        
        result =  self.linkedin_poster.post_content_real(content, access_token)
        
        if result:
            print("✅ Agent Posting: Publication LinkedIn réussie!")
            return result
        else:
            print("❌ Agent Posting: Échec de publication LinkedIn")
            return None