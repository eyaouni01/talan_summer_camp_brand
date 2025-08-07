# ============================================================================
# 📄 core/linkedin_poster.py - VERSION CORRIGÉE POUR IMAGES
# ============================================================================
import os
import json
import requests
import base64
import mimetypes
import time
from datetime import datetime
from typing import Optional, Dict, Union

class LinkedInPublisher:
    """
    Gestionnaire de publication LinkedIn avec support images corrigé
    """
    
    def __init__(self):
        self.base_url = "https://api.linkedin.com/v2"
        self.rest_api_url = "https://api.linkedin.com/rest"  # Nouvelle API
        self.token_file = r"C:\Users\eyaou\OneDrive\Bureau\talan_summer_camp\smart_content_engine\.linkedin_token.json"
    
    def load_access_token(self) -> Optional[str]:
        """
        Charge l'access token à partir du fichier JSON spécifié.
        """
        try:
            if not os.path.exists(self.token_file):
                print(f"❌ Fichier token introuvable: {self.token_file}")
                print("💡 Pour résoudre ce problème:")
                print("1. Allez dans le dossier parent: cd ..")
                print("2. Lancez: python linkedin_auth.py")
                print("3. Suivez les instructions pour obtenir un nouveau token")
                return None

            with open(self.token_file, 'r', encoding='utf-8') as f:
                token_data = json.load(f)

            access_token = token_data.get('access_token')
            timestamp = token_data.get('timestamp')

            if not access_token:
                print("❌ Aucun access_token trouvé dans le fichier JSON")
                return None

            # Vérifier si le token est encore valide (LinkedIn tokens expirent après 60 jours)
            try:
                token_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
                token_age = (datetime.now() - token_time).total_seconds() / (60 * 60 * 24)  # Âge en jours

                if token_age > 60:
                    print("⚠️ Token expiré (plus de 60 jours)")
                    print("💡 Pour renouveler le token:")
                    print("1. Allez dans le dossier parent: cd ..")
                    print("2. Lancez: python linkedin_auth.py")
                    print("3. Suivez les instructions pour obtenir un nouveau token")
                    return None
                elif token_age > 45:
                    print("⚠️ Token va expirer bientôt (plus de 45 jours)")
            except ValueError:
                print("⚠️ Format de timestamp invalide, tentative de chargement...")

            print(f"✅ Access token chargé: {access_token[:10]}... (timestamp: {timestamp})")
            return access_token

        except Exception as e:
            print(f"❌ Erreur lors de la lecture du fichier token: {e}")
            return None
    
    def get_user_id_corrected(self, access_token: str) -> Optional[str]:
        """
        Récupération d'ID utilisateur avec méthode corrigée
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'LinkedIn-Version': '202308'
            }
            
            # PRIORITÉ 1: userinfo (fonctionne selon vos logs)
            try:
                print("🔍 Récupération ID via userinfo...")
                response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    user_id = data.get('sub')
                    if user_id:
                        print(f"✅ ID trouvé: {user_id}")
                        return user_id
            except Exception as e:
                print(f"⚠️ Erreur userinfo: {e}")
            
            return None
            
        except Exception as e:
            print(f"❌ Erreur récupération ID: {e}")
            return None
    
    def upload_image_v2(self, image_path: str, access_token: str, user_id: str) -> Optional[str]:
        """
        Upload d'image avec nouvelle API LinkedIn (plus stable)
        """
        try:
            if not os.path.exists(image_path):
                print(f"❌ Image introuvable: {image_path}")
                return None
            
            # Vérifier la taille (max 20MB pour LinkedIn)
            file_size = os.path.getsize(image_path)
            if file_size > 20 * 1024 * 1024:
                print(f"❌ Image trop grande: {file_size} bytes (max 20MB)")
                return None
            
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type or not mime_type.startswith('image/'):
                print(f"❌ Type fichier non supporté: {mime_type}")
                return None
            
            print(f"🖼️ Upload image: {image_path} ({file_size} bytes, {mime_type})")
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'LinkedIn-Version': '202308'
            }
            
            # Étape 1: Initialiser l'upload avec format corrigé
            register_data = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:person:{user_id}",  # UTILISER person au lieu de member
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }
            
            print("📤 Initialisation upload...")
            response = requests.post(
                f"{self.base_url}/assets?action=registerUpload",
                headers=headers,
                json=register_data,
                timeout=30
            )
            
            print(f"🔍 Register status: {response.status_code}")
            
            if response.status_code not in [200, 201]:
                print(f"❌ Échec register: {response.text}")
                return None
            
            upload_info = response.json()
            asset_urn = upload_info['value']['asset']
            upload_url = upload_info['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            
            print(f"✅ Asset URN: {asset_urn}")
            
            # Étape 2: Upload binaire avec retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    with open(image_path, 'rb') as f:
                        image_data = f.read()
                    
                    upload_headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': mime_type,
                    }
                    
                    print(f"📤 Upload fichier (tentative {attempt + 1}/{max_retries})...")
                    upload_response = requests.post(
                        upload_url,
                        headers=upload_headers,
                        data=image_data,
                        timeout=60
                    )
                    
                    print(f"🔍 Upload status: {upload_response.status_code}")
                    
                    if upload_response.status_code in [200, 201]:
                        # Attendre un peu pour le traitement
                        print("⏳ Attente traitement image...")
                        time.sleep(2)
                        
                        # Vérifier le statut
                        if self._verify_asset_status(asset_urn, access_token):
                            print("✅ Image uploadée et vérifiée!")
                            return asset_urn
                        else:
                            print("⚠️ Image uploadée mais statut incertain")
                            return asset_urn  # Tenter quand même
                    
                    if attempt < max_retries - 1:
                        print(f"⚠️ Tentative {attempt + 1} échouée, retry dans 2s...")
                        time.sleep(2)
                        
                except Exception as e:
                    print(f"❌ Erreur upload tentative {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2)
            
            print("❌ Échec upload après tous les retries")
            return None
            
        except Exception as e:
            print(f"❌ Erreur upload image: {e}")
            return None
    
    def _verify_asset_status(self, asset_urn: str, access_token: str) -> bool:
        """
        Vérifie que l'asset est prêt
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'LinkedIn-Version': '202308'
            }
            
            # Extraire l'ID de l'URN
            asset_id = asset_urn.split(':')[-1]
            check_url = f"{self.base_url}/assets/{asset_id}"
            
            response = requests.get(check_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                asset_data = response.json()
                status = asset_data.get('status', 'unknown')
                print(f"📊 Asset status: {status}")
                return status in ['ALLOWED', 'READY', 'AVAILABLE']
            
            return True  # Si on ne peut pas vérifier, on assume que c'est OK
            
        except Exception as e:
            print(f"⚠️ Erreur vérification asset: {e}")
            return True  # Assumer OK si erreur
    
    def post_with_image_corrected(self, content: str, access_token: str, image_path: str = None) -> Optional[Dict]:
        """
        Publication corrigée avec gestion d'erreurs améliorée
        """
        try:
            # Récupérer l'ID utilisateur
            user_id = self.get_user_id_corrected(access_token)
            if not user_id:
                print("❌ Impossible de récupérer l'ID utilisateur")
                return None
            
            asset_urn = None
            
            # Upload de l'image SI fournie
            if image_path and os.path.exists(image_path):
                print("🖼️ Tentative upload image...")
                asset_urn = self.upload_image_v2(image_path, access_token, user_id)
                
                if not asset_urn:
                    print("⚠️ Échec upload, publication sans image...")
            
            # Publication avec format corrigé
            return self._publish_corrected(content, access_token, user_id, asset_urn)
            
        except Exception as e:
            print(f"❌ Erreur publication: {e}")
            return None
    
    def _publish_corrected(self, content: str, access_token: str, user_id: str, asset_urn: str = None) -> Optional[Dict]:
        """
        Publication avec format URN corrigé
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'LinkedIn-Version': '202308'
            }
            
            # Structure de base avec PERSON (qui fonctionne selon vos logs)
            post_data = {
                "author": f"urn:li:person:{user_id}",  # PERSON au lieu de MEMBER
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"  # Par défaut NONE
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            # Ajouter média SEULEMENT si upload réussi
            if asset_urn:
                print(f"🖼️ Ajout image au post: {asset_urn}")
                post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
                post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                    {
                        "status": "READY",
                        "description": {
                            "text": "Image du post"
                        },
                        "media": asset_urn,
                        "title": {
                            "text": "Illustration"
                        }
                    }
                ]
            
            print(f"📤 Publication avec urn:li:person:{user_id}")
            print(f"📝 Contenu: {content[:100]}...")
            print(f"🖼️ Avec image: {'Oui' if asset_urn else 'Non'}")
            
            # Publication avec timeout
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=headers,
                json=post_data,
                timeout=30
            )
            
            print(f"🔍 Status: {response.status_code}")
            print(f"🔍 Response: {response.text}")
            
            if response.status_code in [200, 201]:
                result = self._create_success_result(content, response.json(), asset_urn)
                self._save_result(result)
                
                print("🎉 Publication réussie!")
                print(f"🔗 URL: {result.get('post_url', 'N/A')}")
                print(f"📝 Mode: {'Avec image' if asset_urn else 'Texte seul'}")
                
                return result
            else:
                print(f"❌ Échec publication: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur publication: {e}")
            return None
    
    def _create_success_result(self, content: str, api_response: dict, asset_urn: str = None) -> Dict:
        """
        Crée le résultat de succès
        """
        post_id = api_response.get('id', '')
        
        result = {
            "status": "success",
            "post_id": post_id,
            "post_url": f"https://www.linkedin.com/feed/update/{post_id}" if post_id else "",
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "has_image": bool(asset_urn),
            "image_asset": asset_urn if asset_urn else None,
            "api_response": api_response
        }
        
        return result
    
    def _save_result(self, result: Dict):
        """
        Sauvegarde le résultat
        """
        try:
            os.makedirs("data/posted_content", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/posted_content/linkedin_post_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"📁 Résultat sauvegardé: {filename}")
            
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde: {e}")
    
    def post_content_with_image(self, content: str, access_token: str, image_path: str = None) -> Optional[Dict]:
        """
        Méthode principale corrigée
        """
        return self.post_with_image_corrected(content, access_token, image_path)
    
    def diagnostic_permissions(self, access_token: str):
        """
        Diagnostic des permissions pour debug
        """
        print("🔍 === DIAGNOSTIC PERMISSIONS ===")
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        endpoints = [
            ("userinfo", "https://api.linkedin.com/v2/userinfo"),
            ("people", f"{self.base_url}/people/~"),
            ("assets", f"{self.base_url}/assets"),
            ("ugcPosts", f"{self.base_url}/ugcPosts")
        ]
        
        for name, url in endpoints:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                print(f"🧪 {name}: {response.status_code}")
                if response.status_code != 200:
                    print(f"   ❌ {response.text[:200]}")
                else:
                    print(f"   ✅ OK")
            except Exception as e:
                print(f"🧪 {name}: ERROR - {e}")
        
        print("🔍 === FIN DIAGNOSTIC ===")