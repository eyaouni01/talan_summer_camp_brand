# ============================================================================
# 📄 agents/reviewer_agent.py
# ============================================================================
from core.content_reviewer import ContentReviewer
from typing import Dict, Optional

class ReviewerAgent:
    """
    Agent MCP pour la review de contenu business
    """
    
    def __init__(self):
        self.content_reviewer = ContentReviewer()
    
    async def review_business_content(self, content: str, preferences: Dict) -> Optional[str]:
        """
        Interface principale pour reviewer le contenu business
        """
        print("🤖 Agent Reviewer Business: Démarrage de la review...")
        
        reviewed_content = await self.content_reviewer.review_business_content(content, preferences)
        
        if reviewed_content:
            print("✅ Agent Reviewer Business: Review terminée avec succès")
            return reviewed_content
        else:
            print("❌ Agent Reviewer Business: Problème lors de la review")
            return content