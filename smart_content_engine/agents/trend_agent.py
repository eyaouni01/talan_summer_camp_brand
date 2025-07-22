# ============================================================================
# 📄 agents/trend_agent.py
# ============================================================================
from core.trend_collector import TrendCollector
from typing import Dict, Optional, List

class TrendAgent:
    """
    Agent MCP pour la collecte de trends
    """
    
    def __init__(self):
        self.trend_collector = TrendCollector()
    
    async def collect_trends(self, business_sector: str, language: str = "fr") -> Optional[List[Dict]]:
        """
        Interface principale pour collecter les trends
        
        Args:
            business_sector: Secteur d'activité
            language: Langue pour les trends
            
        Returns:
            List[Dict]: Liste des trends collectées
        """
        print("🤖 Agent Trends: Démarrage de la collecte...")
        
        trends = await self.trend_collector.collect_sector_trends(business_sector, language)
        
        if trends:
            print(f"✅ Agent Trends: {len(trends)} trends collectées")
            return trends
        else:
            print("❌ Agent Trends: Aucune trend collectée")
            return None