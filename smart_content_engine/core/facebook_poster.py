# ============================================================================
# 📄 core/facebook_poster.py - Compatible avec votre structure core/
# ============================================================================
import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any

class FacebookPoster:
    """
    Module de publication sur Facebook Pages - Version compatible avec structure core/
    Similaire à LinkedInPoster pour maintenir la cohérence
    """
    
    def __init__(self, access_token: str = None):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def get_pages(self) -> list:
        """Récupère la liste des pages gérées par l'utilisateur"""
        if not self.access_token:
            return []
        
        url = f"{self.base_url}/me/accounts"
        params = {
            'access_token': self.access_token,
            'fields': 'id,name,access_token,category,fan_count'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            print(f"❌ Erreur récupération pages: {e}")
            return []
    
    def post_content_with_image(self, content: str, page_id: str, page_token: str, image_path: str = None) -> Optional[Dict[str, Any]]:
        """
        Publie du contenu avec image optionnelle - Interface similaire à LinkedInPoster
        
        Args:
            content: Texte du post
            page_id: ID de la page Facebook
            page_token: Token d'accès de la page
            image_path: Chemin vers l'image (optionnel)
        
        Returns:
            Dictionnaire avec le résultat de la publication
        """
        if image_path and os.path.exists(image_path):
            return self._post_with_image(page_id, page_token, content, image_path)
        else:
            return self._post_text_only(page_id, page_token, content)
    
    def _post_with_image(self, page_id: str, page_token: str, message: str, image_path: str) -> Optional[Dict[str, Any]]:
        """Publie un post avec image sur une page"""
        url = f"{self.base_url}/{page_id}/photos"
        
        try:
            with open(image_path, 'rb') as image_file:
                files = {'source': image_file}
                data = {
                    'access_token': page_token,
                    'message': message,
                    'published': 'true'
                }
                
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                
                result = response.json()
                post_id = result.get('post_id') or result.get('id')
                
                return {
                    'success': True,
                    'post_id': post_id,
                    'post_url': f"https://www.facebook.com/{post_id.replace('_', '/posts/')}",
                    'type': 'photo',
                    'has_image': True,
                    'image_path': image_path,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Erreur publication avec image: {e}")
            print("🔄 Tentative de publication en texte seul...")
            return self._post_text_only(page_id, page_token, message)
    
    def _post_text_only(self, page_id: str, page_token: str, message: str) -> Optional[Dict[str, Any]]:
        """Publie un post texte seul sur une page"""
        url = f"{self.base_url}/{page_id}/feed"
        
        data = {
            'access_token': page_token,
            'message': message
        }
        
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id')
            
            return {
                'success': True,
                'post_id': post_id,
                'post_url': f"https://www.facebook.com/{post_id.replace('_', '/posts/')}",
                'type': 'text',
                'has_image': False,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Erreur publication texte: {e}")
            return None
    
    def post_to_page(self, page_id: str, page_token: str, content: str, image_path: str = None) -> Optional[Dict[str, Any]]:
        """
        Interface publique pour publier sur une page Facebook
        Méthode principale similaire à votre LinkedInPoster
        """
        print(f"📤 Publication sur la page Facebook {page_id}...")
        
        try:
            result = self.post_content_with_image(content, page_id, page_token, image_path)
            
            if result and result.get('success'):
                print(f"✅ Publication Facebook réussie!")
                if result.get('post_url'):
                    print(f"🔗 URL: {result['post_url']}")
                return result
            else:
                print("❌ Échec de la publication Facebook")
                return None
                
        except Exception as e:
            print(f"❌ Erreur dans post_to_page: {e}")
            return None
    
    def get_page_insights(self, page_id: str, page_token: str) -> Dict[str, Any]:
        """Récupère les insights d'une page (statistiques)"""
        url = f"{self.base_url}/{page_id}/insights"
        params = {
            'access_token': page_token,
            'metric': 'page_fans,page_impressions,page_engaged_users',
            'period': 'day'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erreur récupération insights: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """Test la connexion et la validité du token"""
        if not self.access_token:
            return False
        
        url = f"{self.base_url}/me"
        params = {'access_token': self.access_token}
        
        try:
            response = requests.get(url, params=params)
            return response.status_code == 200
        except:
            return False
    
    def get_user_info(self) -> Dict[str, Any]:
        """Récupère les informations de l'utilisateur connecté"""
        if not self.access_token:
            return {}
        
        url = f"{self.base_url}/me"
        params = {
            'access_token': self.access_token,
            'fields': 'id,name,email'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erreur récupération info utilisateur: {e}")
            return {}