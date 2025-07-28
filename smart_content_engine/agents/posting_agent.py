# ============================================================================
# 📄 agents/posting_agent.py - AVEC SUPPORT IMAGES
# ============================================================================
import os
import json
from datetime import datetime
from typing import Optional, Dict
from core.linkedin_poster import LinkedInPoster

class PostingAgent:
    """
    Agent spécialisé dans la publication de contenu sur LinkedIn
    Support des images générées automatiquement
    """
    
    def __init__(self):
        self.linkedin_poster = LinkedInPoster()
    
    async def post_to_linkedin_real(self, content: str, preferences: Dict, image_path: str = None) -> Optional[Dict]:
        """
        Publication réelle sur LinkedIn avec support d'images
        
        Args:
            content: Le contenu textuel à publier
            preferences: Dictionnaire contenant les préférences et le token LinkedIn
            image_path: Chemin vers l'image à publier (optionnel)
        
        Returns:
            Dictionnaire avec le résultat de la publication
        """
        try:
            linkedin_token = preferences.get('linkedin_token')
            
            if not linkedin_token:
                print("❌ Token LinkedIn manquant")
                return None
            
            print("📤 Publication LinkedIn en cours...")
            if image_path and os.path.exists(image_path):
                print(f"🖼️ Avec image: {image_path}")
            else:
                print("📝 Contenu texte uniquement")
            
            # Publication avec ou sans image
            result = self.linkedin_poster.post_content_with_image(
                content=content,
                access_token=linkedin_token,
                image_path=image_path
            )
            
            if result:
                # Enrichir le résultat avec les métadonnées
                result['preferences'] = preferences
                result['content_length'] = len(content)
                result['language'] = preferences.get('language', 'fr')
                result['business_sector'] = preferences.get('business_sector', 'unknown')
                
                # Sauvegarder le résultat
                self._save_publication_result(result)
                
                return result
            else:
                print("❌ Échec de la publication")
                return None
                
        except Exception as e:
            print(f"❌ Erreur dans PostingAgent: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _save_publication_result(self, result: Dict):
        """
        Sauvegarde le résultat de publication avec métadonnées complètes
        """
        try:
            os.makedirs("data/posted_content", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/posted_content/linkedin_post_{timestamp}.json"
            
            # Ajouter des métadonnées de tracking
            result['tracking'] = {
                'publication_timestamp': datetime.now().isoformat(),
                'agent': 'PostingAgent',
                'version': '2.0_with_images'
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"📁 Résultat sauvegardé: {filename}")
            
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde résultat: {e}")
    
    def simulate_posting(self, content: str, preferences: Dict, image_path: str = None) -> Dict:
        """
        Simulation de publication (mode test/dev)
        """
        print("🧪 Mode simulation - Publication fictive")
        
        result = {
            "status": "simulated",
            "post_id": f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "post_url": "https://linkedin.com/feed/simulation",
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "preferences": preferences,
            "has_image": image_path is not None and os.path.exists(image_path),
            "image_path": image_path if image_path else None,
            "content_length": len(content),
            "simulation": True
        }
        
        # Sauvegarder même les simulations
        self._save_publication_result(result)
        
        return result