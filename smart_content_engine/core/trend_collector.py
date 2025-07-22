
# ============================================================================
# 📄 core/trend_collector.py
# ============================================================================
import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

class TrendCollector:
    """
    Collecteur de trends multi-sources pour le contenu business
    """
    
    def __init__(self):
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        
    async def collect_sector_trends(self, business_sector: str, language: str = "fr") -> Optional[List[Dict]]:
        """
        Collecte les trends d'un secteur spécifique
        
        Args:
            business_sector: Secteur d'activité
            language: Langue pour les trends
            
        Returns:
            List[Dict]: Liste des trends collectées
        """
        try:
            print(f"🔍 Collecte des trends pour le secteur: {business_sector}")
            
            trends = []
            
            # Collecte depuis Google Trends (simulé)
            google_trends = await self._collect_google_trends(business_sector, language)
            if google_trends:
                trends.extend(google_trends)
            
            # Collecte depuis les actualités
            news_trends = await self._collect_news_trends(business_sector, language)
            if news_trends:
                trends.extend(news_trends)
            
            # Sauvegarde des trends
            if trends:
                await self._save_trends(trends, business_sector)
                print(f"✅ {len(trends)} trends collectées pour {business_sector}")
                return trends
            else:
                print("⚠️ Aucune trend collectée")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de la collecte de trends: {e}")
            return None
    
    async def _collect_google_trends(self, sector: str, language: str) -> List[Dict]:
        """Collecte trends depuis Google Trends (version simulée)"""
        # Simulation de trends par secteur
        trends_data = {
            "technology": [
                {"keyword": "intelligence artificielle", "interest": 95, "growth": "+25%"},
                {"keyword": "cybersécurité", "interest": 88, "growth": "+15%"},
                {"keyword": "cloud computing", "interest": 82, "growth": "+18%"},
                {"keyword": "blockchain", "interest": 75, "growth": "+12%"},
                {"keyword": "IoT", "interest": 70, "growth": "+20%"}
            ],
            "marketing": [
                {"keyword": "marketing automation", "interest": 90, "growth": "+30%"},
                {"keyword": "content marketing", "interest": 85, "growth": "+22%"},
                {"keyword": "influencer marketing", "interest": 80, "growth": "+35%"},
                {"keyword": "SEO", "interest": 95, "growth": "+10%"},
                {"keyword": "social media", "interest": 88, "growth": "+15%"}
            ],
            "finance": [
                {"keyword": "fintech", "interest": 92, "growth": "+28%"},
                {"keyword": "cryptocurrency", "interest": 85, "growth": "+40%"},
                {"keyword": "robo-advisors", "interest": 70, "growth": "+25%"},
                {"keyword": "digital banking", "interest": 78, "growth": "+20%"},
                {"keyword": "ESG investing", "interest": 75, "growth": "+45%"}
            ]
        }
        
        sector_trends = trends_data.get(sector, [])
        
        return [
            {
                "source": "google_trends",
                "keyword": trend["keyword"],
                "interest_score": trend["interest"],
                "growth": trend["growth"],
                "language": language,
                "timestamp": datetime.now().isoformat()
            }
            for trend in sector_trends[:3]  # Top 3 trends
        ]
    
    async def _collect_news_trends(self, sector: str, language: str) -> List[Dict]:
        """Collecte trends depuis les actualités"""
        # Simulation de news trends
        news_data = {
            "technology": [
                {"title": "L'IA générative transforme les entreprises", "relevance": 95},
                {"title": "Cybersécurité: nouvelles menaces en 2024", "relevance": 88},
                {"title": "Le cloud hybride en pleine expansion", "relevance": 82}
            ],
            "marketing": [
                {"title": "Marketing automation: ROI en hausse", "relevance": 90},
                {"title": "TikTok Business prend de l'ampleur", "relevance": 85},
                {"title": "Cookies tiers: la fin d'une époque", "relevance": 80}
            ],
            "finance": [
                {"title": "FinTech: levées de fonds record", "relevance": 92},
                {"title": "Banques numériques vs traditionnelles", "relevance": 85},
                {"title": "Réglementation crypto renforcée", "relevance": 78}
            ]
        }
        
        sector_news = news_data.get(sector, [])
        
        return [
            {
                "source": "news",
                "title": news["title"],
                "relevance_score": news["relevance"],
                "language": language,
                "timestamp": datetime.now().isoformat()
            }
            for news in sector_news[:2]  # Top 2 news
        ]
    
    async def _save_trends(self, trends: List[Dict], sector: str):
        """Sauvegarde les trends collectées"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/trends/trends_{sector}_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "sector": sector,
            "trends_count": len(trends),
            "trends": trends
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)