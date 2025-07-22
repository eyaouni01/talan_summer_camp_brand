# ============================================================================
# 📄 core/linkedin_poster.py - AVEC SUPPORT OPENID USERINFO
# ============================================================================
import os
import json
import requests
import base64
from datetime import datetime
from typing import Optional, Dict

class LinkedInPoster:
    """
    Gestionnaire de publication LinkedIn avec extraction ID du token
    Support des nouveaux scopes OpenID Connect
    """
    
    def __init__(self):
        self.base_url = "https://api.linkedin.com/v2"
    
    def extract_user_id_from_token(self, access_token: str) -> Optional[str]:
        """
        Extrait l'ID utilisateur depuis le token JWT LinkedIn
        """
        try:
            # LinkedIn utilise parfois des tokens JWT
            # Essayons de décoder la partie payload
            if '.' in access_token:
                parts = access_token.split('.')
                if len(parts) >= 2:
                    # Décoder le payload (partie 2 du JWT)
                    payload = parts[1]
                    # Ajouter padding si nécessaire
                    missing_padding = len(payload) % 4
                    if missing_padding:
                        payload += '=' * (4 - missing_padding)
                    
                    try:
                        decoded = base64.urlsafe_b64decode(payload)
                        token_data = json.loads(decoded)
                        
                        # Chercher l'ID dans différents champs
                        user_id = token_data.get('sub') or token_data.get('user_id') or token_data.get('id')
                        if user_id:
                            print(f"✅ ID extrait du token: {user_id}")
                            return str(user_id)
                    except Exception as decode_error:
                        print(f"⚠️ Erreur décodage JWT: {decode_error}")
            
            print("⚠️ Impossible d'extraire l'ID du token")
            return None
            
        except Exception as e:
            print(f"❌ Erreur extraction ID: {e}")
            return None
    
    def get_user_id_alternative(self, access_token: str) -> Optional[str]:
        """
        Méthode alternative pour récupérer l'ID utilisateur avec nouveaux scopes
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # PRIORITÉ 1: Essayer userinfo (OpenID Connect) - NOUVEAU SCOPE
            try:
                print("🔍 Test userinfo (OpenID Connect)...")
                response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
                print(f"🔍 Status userinfo: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"🔍 Userinfo data: {data}")
                    
                    # OpenID Connect utilise 'sub' pour l'ID utilisateur
                    user_id = data.get('sub')
                    if user_id:
                        print(f"✅ ID trouvé via userinfo: {user_id}")
                        return str(user_id)
                else:
                    print(f"⚠️ Userinfo failed: {response.text}")
            except Exception as e:
                print(f"⚠️ Erreur userinfo: {e}")
            
            # PRIORITÉ 2: Essayer avec profile scope (nouveau format)
            try:
                print("🔍 Test avec profile scope...")
                response = requests.get(f"{self.base_url}/people/~:(id,localizedFirstName)", headers=headers)
                print(f"🔍 Status profile: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"🔍 Profile data: {data}")
                    
                    user_id = data.get('id')
                    name = data.get('localizedFirstName', 'Utilisateur')
                    if user_id:
                        print(f"✅ ID trouvé via profile: {user_id} ({name})")
                        return str(user_id)
                else:
                    print(f"⚠️ Profile failed: {response.text}")
            except Exception as e:
                print(f"⚠️ Erreur profile: {e}")
            
            # PRIORITÉ 3: Essayer avec endpoint me
            try:
                print("🔍 Test endpoint /me...")
                response = requests.get(f"{self.base_url}/me", headers=headers)
                print(f"🔍 Status /me: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"🔍 Me data: {data}")
                    
                    user_id = data.get('id') or data.get('sub')
                    if user_id:
                        print(f"✅ ID trouvé via /me: {user_id}")
                        return str(user_id)
                else:
                    print(f"⚠️ Me endpoint failed: {response.text}")
            except Exception as e:
                print(f"⚠️ Erreur /me: {e}")
            
            # PRIORITÉ 4: Essayer les anciens endpoints
            print("🔍 Test anciens endpoints...")
            endpoints = [
                f"{self.base_url}/people/~:(id)",
                f"{self.base_url}/people/~"
            ]
            
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, headers=headers)
                    print(f"🔍 Test {endpoint}: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        user_id = data.get('id') or data.get('sub')
                        if user_id:
                            print(f"✅ ID trouvé via {endpoint}: {user_id}")
                            return str(user_id)
                    else:
                        print(f"⚠️ {endpoint} failed: {response.text}")
                except Exception as e:
                    print(f"⚠️ Erreur {endpoint}: {e}")
                    continue
            
            print("❌ Aucune méthode n'a fonctionné pour récupérer l'ID")
            return None
            
        except Exception as e:
            print(f"❌ Erreur récupération alternative: {e}")
            return None
    
    def post_content_real(self, content: str, access_token: str) -> Optional[Dict]:
        """
        Publication LinkedIn avec récupération ID intelligente
        """
        try:
            print("🔍 Recherche de l'ID utilisateur...")
            print(f"🔍 Token (20 premiers chars): {access_token[:20]}...")
            
            # Méthode 1: Extraction depuis le token
            user_id = self.extract_user_id_from_token(access_token)
            
            # Méthode 2: Si échec, tentative via API
            if not user_id:
                user_id = self.get_user_id_alternative(access_token)
            
            # Méthode 3: Si toujours échec, essayer avec un ID factice mais valide
            if not user_id:
                print("⚠️ Utilisation d'une méthode de contournement...")
                return self._try_workaround_method(content, access_token)
            
            # Tentative de publication avec l'ID trouvé
            return self._publish_with_id(content, access_token, user_id)
            
        except Exception as e:
            print(f"❌ Erreur globale: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _publish_with_id(self, content: str, access_token: str, user_id: str) -> Optional[Dict]:
        """
        Publication avec ID utilisateur spécifique
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'LinkedIn-Version': '202308'
            }
            
            # Essayer format member
            post_data = {
                "author": f"urn:li:member:{user_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            print(f"📤 Publication avec urn:li:member:{user_id}")
            print(f"📤 Contenu (100 premiers chars): {content[:100]}...")
            
            response = requests.post(f"{self.base_url}/ugcPosts", headers=headers, json=post_data)
            
            print(f"🔍 Status: {response.status_code}")
            print(f"🔍 Response: {response.text}")
            
            if response.status_code in [200, 201]:
                print("🎉 Publication réussie!")
                return self._create_success_result(content, response.json())
            
            # Si member échoue, essayer person
            print(f"🔄 Tentative avec urn:li:person:{user_id}")
            post_data["author"] = f"urn:li:person:{user_id}"
            
            response = requests.post(f"{self.base_url}/ugcPosts", headers=headers, json=post_data)
            
            print(f"🔍 Status person: {response.status_code}")
            print(f"🔍 Response person: {response.text}")
            
            if response.status_code in [200, 201]:
                print("🎉 Publication réussie avec format person!")
                return self._create_success_result(content, response.json())
            
            print(f"❌ Échec avec ID {user_id}")
            return None
            
        except Exception as e:
            print(f"❌ Erreur publication avec ID: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _try_workaround_method(self, content: str, access_token: str) -> Optional[Dict]:
        """
        Méthode de contournement sans ID utilisateur
        """
        try:
            print("🔧 Tentative méthode de contournement...")
            
            # Créer un pseudo-post pour sauvegarder le contenu
            result = {
                "status": "content_saved",
                "timestamp": datetime.now().isoformat(),
                "content": content,
                "method": "workaround_save",
                "note": "Contenu sauvegardé - Publication manuelle recommandée"
            }
            
            self._save_posted_content(result)
            
            print("📁 Contenu sauvegardé pour publication manuelle")
            print("💡 Copiez-collez le contenu sur LinkedIn manuellement")
            print("🔗 https://www.linkedin.com/feed/")
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur contournement: {e}")
            return None
    
    def _create_success_result(self, content: str, api_response: dict) -> Dict:
        """
        Crée un résultat de succès
        """
        post_id = api_response.get('id', '')
        
        return {
            "status": "success",
            "post_id": post_id,
            "post_url": f"https://www.linkedin.com/feed/update/{post_id}" if post_id else "URL non disponible",
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "api_response": api_response
        }
    
    def _save_posted_content(self, result: Dict):
        """Sauvegarde le résultat"""
        try:
            os.makedirs("data/posted_content", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/posted_content/post_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"📁 Sauvegardé: {filename}")
            
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde: {e}")
    
    def test_token_permissions(self, access_token: str):
        """
        Teste les permissions du token pour diagnostic
        """
        print("🧪 Test des permissions du token...")
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Test userinfo
        try:
            response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
            print(f"🧪 userinfo: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"🧪 userinfo error: {e}")
        
        # Test people
        try:
            response = requests.get(f"{self.base_url}/people/~", headers=headers)
            print(f"🧪 people: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"🧪 people error: {e}")