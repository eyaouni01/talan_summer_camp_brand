# ============================================================================
# 📄 core/linkedin_token_manager.py - GESTION DES TOKENS AVEC REFRESH
# ============================================================================
import os
import json
import requests
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from urllib.parse import urlencode

class LinkedInTokenManager:
    """
    Gestionnaire de tokens LinkedIn avec refresh automatique
    """
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str = "http://localhost:8000/callback"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_file = "data/linkedin_tokens.json"
        self.base_url = "https://www.linkedin.com/oauth/v2"
        
        # Créer le dossier si nécessaire
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
    
    def get_authorization_url(self, scopes: list = None) -> str:
        """
        Génère l'URL d'autorisation LinkedIn
        """
        if scopes is None:
            scopes = [
                'r_liteprofile',      # Profil de base
                'r_emailaddress',     # Email
                'w_member_social',    # Publication
                'w_organization_social'  # Publication organisation (si nécessaire)
            ]
        
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(scopes),
            'state': f"linkedin_auth_{int(time.time())}"  # Protection CSRF
        }
        
        auth_url = f"{self.base_url}/authorization?{urlencode(params)}"
        
        print("🔐 === AUTORISATION LINKEDIN ===")
        print(f"📋 Scopes demandés: {', '.join(scopes)}")
        print(f"🔗 URL d'autorisation:")
        print(f"{auth_url}")
        print("\n📝 Instructions:")
        print("1. Ouvrez cette URL dans votre navigateur")
        print("2. Connectez-vous à LinkedIn et autorisez l'application")
        print("3. Copiez le code d'autorisation depuis l'URL de retour")
        print("4. Utilisez exchange_code_for_tokens(code) avec ce code")
        
        return auth_url
    
    def exchange_code_for_tokens(self, authorization_code: str) -> Optional[Dict]:
        """
        Échange le code d'autorisation contre des tokens
        """
        try:
            print("🔄 Échange du code d'autorisation...")
            
            data = {
                'grant_type': 'authorization_code',
                'code': authorization_code,
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(
                f"{self.base_url}/accessToken",
                headers=headers,
                data=data,
                timeout=30
            )
            
            print(f"🔍 Status: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                
                # Calculer l'expiration
                expires_in = token_data.get('expires_in', 5184000)  # ~60 jours par défaut
                expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                # Enrichir les données
                enriched_data = {
                    'access_token': token_data['access_token'],
                    'refresh_token': token_data.get('refresh_token'),  # Peut être None
                    'expires_in': expires_in,
                    'expires_at': expires_at.isoformat(),
                    'token_type': token_data.get('token_type', 'Bearer'),
                    'scope': token_data.get('scope', ''),
                    'created_at': datetime.now().isoformat(),
                    'last_refresh': datetime.now().isoformat()
                }
                
                # Sauvegarder
                self.save_tokens(enriched_data)
                
                print("✅ Tokens obtenus et sauvegardés!")
                print(f"🕒 Expire le: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"🔄 Refresh token: {'Oui' if enriched_data['refresh_token'] else 'Non'}")
                
                return enriched_data
            else:
                print(f"❌ Erreur échange: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur échange code: {e}")
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Dict]:
        """
        Rafraîchit le token d'accès
        """
        try:
            print("🔄 Rafraîchissement du token...")
            
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(
                f"{self.base_url}/accessToken",
                headers=headers,
                data=data,
                timeout=30
            )
            
            print(f"🔍 Refresh status: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                
                # Calculer nouvelle expiration
                expires_in = token_data.get('expires_in', 5184000)
                expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                # Conserver les anciennes données et mettre à jour
                old_data = self.load_tokens() or {}
                
                refreshed_data = {
                    **old_data,  # Conserver les anciennes données
                    'access_token': token_data['access_token'],
                    'refresh_token': token_data.get('refresh_token', old_data.get('refresh_token')),
                    'expires_in': expires_in,
                    'expires_at': expires_at.isoformat(),
                    'last_refresh': datetime.now().isoformat()
                }
                
                self.save_tokens(refreshed_data)
                
                print("✅ Token rafraîchi!")
                print(f"🕒 Nouvelle expiration: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
                
                return refreshed_data
            else:
                print(f"❌ Erreur refresh: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur refresh token: {e}")
            return None
    
    def get_valid_token(self) -> Optional[str]:
        """
        Retourne un token valide, le rafraîchit si nécessaire
        """
        try:
            tokens = self.load_tokens()
            
            if not tokens:
                print("❌ Aucun token sauvegardé")
                print("💡 Utilisez get_authorization_url() pour obtenir un nouveau token")
                return None
            
            # Vérifier expiration
            expires_at = datetime.fromisoformat(tokens['expires_at'])
            now = datetime.now()
            
            # Marge de sécurité de 5 minutes
            if expires_at <= now + timedelta(minutes=5):
                print("⚠️ Token expiré ou expire bientôt")
                
                # Tenter le refresh si disponible
                refresh_token = tokens.get('refresh_token')
                if refresh_token:
                    print("🔄 Tentative de rafraîchissement...")
                    refreshed = self.refresh_access_token(refresh_token)
                    if refreshed:
                        return refreshed['access_token']
                    else:
                        print("❌ Échec du rafraîchissement")
                else:
                    print("❌ Pas de refresh token disponible")
                
                print("💡 Nouvelle autorisation nécessaire:")
                print("   1. Utilisez get_authorization_url()")
                print("   2. Puis exchange_code_for_tokens(code)")
                return None
            else:
                remaining = expires_at - now
                print(f"✅ Token valide (expire dans {remaining})")
                return tokens['access_token']
                
        except Exception as e:
            print(f"❌ Erreur validation token: {e}")
            return None
    
    def save_tokens(self, token_data: Dict):
        """
        Sauvegarde les tokens
        """
        try:
            with open(self.token_file, 'w', encoding='utf-8') as f:
                json.dump(token_data, f, ensure_ascii=False, indent=2)
            print(f"💾 Tokens sauvegardés: {self.token_file}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde tokens: {e}")
    
    def load_tokens(self) -> Optional[Dict]:
        """
        Charge les tokens sauvegardés
        """
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"❌ Erreur chargement tokens: {e}")
            return None
    
    def get_token_status(self) -> Dict:
        """
        Retourne le statut des tokens
        """
        tokens = self.load_tokens()
        
        if not tokens:
            return {
                "status": "no_token",
                "message": "Aucun token sauvegardé",
                "action_needed": "Nouvelle autorisation requise"
            }
        
        try:
            expires_at = datetime.fromisoformat(tokens['expires_at'])
            now = datetime.now()
            remaining = expires_at - now
            
            if remaining.total_seconds() <= 0:
                return {
                    "status": "expired",
                    "message": f"Token expiré depuis {abs(remaining)}",
                    "action_needed": "Rafraîchissement ou nouvelle autorisation",
                    "has_refresh": bool(tokens.get('refresh_token'))
                }
            elif remaining.total_seconds() <= 300:  # 5 minutes
                return {
                    "status": "expiring_soon",
                    "message": f"Token expire dans {remaining}",
                    "action_needed": "Rafraîchissement recommandé",
                    "has_refresh": bool(tokens.get('refresh_token'))
                }
            else:
                return {
                    "status": "valid",
                    "message": f"Token valide (expire dans {remaining})",
                    "action_needed": "Aucune",
                    "expires_at": expires_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erreur lecture token: {e}",
                "action_needed": "Vérifier le fichier de tokens"
            }
    
    def revoke_token(self, access_token: str = None) -> bool:
        """
        Révoque le token (optionnel)
        """
        try:
            if not access_token:
                tokens = self.load_tokens()
                if tokens:
                    access_token = tokens['access_token']
                else:
                    print("❌ Aucun token à révoquer")
                    return False
            
            # LinkedIn n'a pas d'endpoint de révocation standard
            # On supprime juste le fichier local
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
                print("✅ Tokens locaux supprimés")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur révocation: {e}")
            return False

# ============================================================================
# 📄 EXEMPLE D'UTILISATION
# ============================================================================

def exemple_utilisation():
    """
    Exemple d'utilisation du gestionnaire de tokens
    """
    # Configuration (à adapter)
    CLIENT_ID = "votre_client_id"
    CLIENT_SECRET = "votre_client_secret"
    
    # Initialiser le gestionnaire
    token_manager = LinkedInTokenManager(CLIENT_ID, CLIENT_SECRET)
    
    # Vérifier le statut
    status = token_manager.get_token_status()
    print(f"📊 Statut: {status}")
    
    # Si besoin d'autorisation
    if status['status'] in ['no_token', 'expired']:
        if status.get('has_refresh'):
            # Tenter refresh
            tokens = token_manager.load_tokens()
            refreshed = token_manager.refresh_access_token(tokens['refresh_token'])
            if not refreshed:
                # Nouvelle autorisation nécessaire
                auth_url = token_manager.get_authorization_url()
                print(f"Ouvrir: {auth_url}")
        else:
            # Nouvelle autorisation
            auth_url = token_manager.get_authorization_url()
            print(f"Ouvrir: {auth_url}")
    
    # Utiliser le token
    valid_token = token_manager.get_valid_token()
    if valid_token:
        print(f"✅ Token prêt à utiliser: {valid_token[:20]}...")
        # Utiliser avec LinkedInPublisher
    else:
        print("❌ Impossible d'obtenir un token valide")

if __name__ == "__main__":
    exemple_utilisation()