# ============================================================================
# 📄 agents/posting_agent.py - AVEC SUPPORT IMAGES + FACEBOOK
# ============================================================================
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any
from core.linkedin_poster import LinkedInPoster
from core.facebook_poster import FacebookPoster

class PostingAgent:
    """
    Agent spécialisé dans la publication de contenu multi-plateforme
    Support des images générées automatiquement pour LinkedIn et Facebook
    """
    
    def __init__(self):
        self.linkedin_poster = LinkedInPoster()
        self.facebook_poster = None
    
    def set_facebook_token(self, access_token: str):
        """Configure le token Facebook"""
        self.facebook_poster = FacebookPoster(access_token)
    
    # ========== LINKEDIN (Code existant adapté) ==========
    
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
            
            # Publication avec ou sans image via votre LinkedInPoster existant
            result = self.linkedin_poster.post_content_with_image(
                content=content,
                access_token=linkedin_token,
                image_path=image_path
            )
            
            if result:
                # Enrichir le résultat avec les métadonnées
                result['platform'] = 'linkedin'
                result['preferences'] = preferences
                result['content_length'] = len(content)
                result['language'] = preferences.get('language', 'fr')
                result['business_sector'] = preferences.get('business_sector', 'unknown')
                result['has_image'] = image_path is not None and os.path.exists(image_path)
                
                # Sauvegarder le résultat
                self._save_publication_result(result, 'linkedin')
                
                return result
            else:
                print("❌ Échec de la publication LinkedIn")
                return None
                
        except Exception as e:
            print(f"❌ Erreur dans PostingAgent (LinkedIn): {e}")
            import traceback
            traceback.print_exc()
            return None
    
    # ========== FACEBOOK (Nouveau code) ==========
    
    async def post_to_facebook_real(self, content, preferences, image_path=None, **kwargs):
        try:
            with open('facebook_token.json', 'r', encoding='utf-8') as f:
                fb_token_data = json.load(f)

            pages = fb_token_data.get("pages", [])
            if not pages:
                print("❌ Aucune page Facebook trouvée.")
                return None

            # Choisir la première page automatiquement (ou selon préférences)
            page = pages[0]
            page_id = page['id']
            page_token = page['access_token']

            poster = FacebookPoster()
            result = poster.post_to_page(
                page_id=page_id,
                page_token=page_token,
                content=content,
                image_path=image_path
            )
            return result

        except Exception as e:
            print(f"❌ Erreur post_to_facebook_real: {e}")
            return None

    
    # ========== PUBLICATION MULTI-PLATEFORME ==========
    
    async def post_to_all_platforms(self, content: str, preferences: Dict, 
                                  image_path: str = None) -> Dict[str, Any]:
        """
        Publication sur toutes les plateformes configurées
        
        Args:
            content: Le contenu à publier
            preferences: Préférences avec tokens et configuration
            image_path: Chemin vers l'image (optionnel)
        
        Returns:
            Dictionnaire avec résultats pour chaque plateforme
        """
        results = {
            'linkedin': None,
            'facebook': None,
            'success_count': 0,
            'total_platforms': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # LinkedIn
        if preferences.get('linkedin') and preferences.get('linkedin_token'):
            results['total_platforms'] += 1
            print("\n📘 Publication LinkedIn...")
            linkedin_result = await self.post_to_linkedin_real(content, preferences, image_path)
            if linkedin_result:
                results['linkedin'] = linkedin_result
                results['success_count'] += 1
                print("✅ LinkedIn: Publié avec succès!")
                if linkedin_result.get('post_url'):
                    print(f"   🔗 {linkedin_result['post_url']}")
            else:
                print("❌ LinkedIn: Échec de publication")
        
        # Facebook
        if preferences.get('facebook') and self.facebook_poster:
            results['total_platforms'] += 1
            print("\n📘 Publication Facebook...")
            facebook_result = await self.post_to_facebook_real(content, preferences, image_path)
            if facebook_result:
                results['facebook'] = facebook_result
                results['success_count'] += 1
                print("✅ Facebook: Publié avec succès!")
                if facebook_result.get('post_url'):
                    print(f"   🔗 {facebook_result['post_url']}")
                if facebook_result.get('page_name'):
                    print(f"   📄 Page: {facebook_result['page_name']}")
            else:
                print("❌ Facebook: Échec de publication")
        
        # Sauvegarder les résultats combinés
        self._save_multi_platform_results(results, content, preferences, image_path)
        
        return results
    
    # ========== SIMULATION ET SAUVEGARDE ==========
    
    def simulate_posting(self, content: str, preferences: Dict, image_path: str = None) -> Dict:
        """
        Simulation de publication (mode test/dev) - Compatible multi-plateforme
        """
        print("🧪 Mode simulation - Publication fictive")
        
        platforms_enabled = []
        if preferences.get('linkedin'):
            platforms_enabled.append('linkedin')
        if preferences.get('facebook'):
            platforms_enabled.append('facebook')
        
        result = {
            "status": "simulated",
            "post_id": f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "post_url": "https://simulation.com/post",
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "preferences": preferences,
            "platforms": platforms_enabled,
            "has_image": image_path is not None and os.path.exists(image_path),
            "image_path": image_path if image_path else None,
            "content_length": len(content),
            "simulation": True
        }
        
        # Sauvegarder même les simulations
        self._save_publication_result(result, 'simulation')
        
        return result
    
    def _save_publication_result(self, result: Dict, platform: str):
        """
        Sauvegarde le résultat de publication avec métadonnées complètes
        """
        try:
            os.makedirs("data/posted_content", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/posted_content/{platform}_post_{timestamp}.json"
            
            # Ajouter des métadonnées de tracking
            result['tracking'] = {
                'publication_timestamp': datetime.now().isoformat(),
                'agent': 'PostingAgent',
                'version': '3.0_multi_platform',
                'platform': platform
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"📁 Résultat {platform} sauvegardé: {filename}")
            
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde résultat {platform}: {e}")
    
    def _save_multi_platform_results(self, results: Dict, content: str, preferences: Dict, image_path: str = None):
        """
        Sauvegarde les résultats de publication multi-plateforme
        """
        try:
            os.makedirs("data/posted_content", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/posted_content/multi_platform_post_{timestamp}.json"
            
            # Données complètes de la publication
            complete_data = {
                "timestamp": timestamp,
                "content": content,
                "image_path": image_path,
                "preferences": preferences,
                "results": results,
                "summary": {
                    "platforms_attempted": results['total_platforms'],
                    "platforms_successful": results['success_count'],
                    "success_rate": f"{(results['success_count']/results['total_platforms']*100):.1f}%" if results['total_platforms'] > 0 else "0%",
                    "has_image": image_path is not None and os.path.exists(image_path),
                    "content_length": len(content)
                },
                "tracking": {
                    "publication_timestamp": datetime.now().isoformat(),
                    "agent": 'PostingAgent',
                    "version": '3.0_multi_platform'
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(complete_data, f, ensure_ascii=False, indent=2)
            
            print(f"📁 Résultats multi-plateforme sauvegardés: {filename}")
            
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde multi-plateforme: {e}")
    
    def get_publication_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques des publications passées
        """
        try:
            stats = {
                'total_posts': 0,
                'linkedin_posts': 0,
                'facebook_posts': 0,
                'multi_platform_posts': 0,
                'posts_with_images': 0,
                'recent_posts': []
            }
            
            posts_dir = "data/posted_content"
            if not os.path.exists(posts_dir):
                return stats
            
            for filename in os.listdir(posts_dir):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(posts_dir, filename), 'r', encoding='utf-8') as f:
                            post_data = json.load(f)
                        
                        stats['total_posts'] += 1
                        
                        if 'linkedin' in filename:
                            stats['linkedin_posts'] += 1
                        elif 'facebook' in filename:
                            stats['facebook_posts'] += 1
                        elif 'multi_platform' in filename:
                            stats['multi_platform_posts'] += 1
                        
                        if post_data.get('has_image'):
                            stats['posts_with_images'] += 1
                        
                        # Garder les 5 posts les plus récents
                        if len(stats['recent_posts']) < 5:
                            stats['recent_posts'].append({
                                'filename': filename,
                                'timestamp': post_data.get('timestamp'),
                                'platform': post_data.get('platform', 'unknown'),
                                'has_image': post_data.get('has_image', False)
                            })
                    
                    except Exception as e:
                        continue
            
            return stats
            
        except Exception as e:
            print(f"⚠️ Erreur récupération stats: {e}")
            return {'error': str(e)}