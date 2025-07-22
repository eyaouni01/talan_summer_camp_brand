# ============================================================================
# 📄 linkedin_auth.py
# ============================================================================
import os
import requests
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
from requests_oauthlib import OAuth2Session
import json
from datetime import datetime
import os
from dotenv import load_dotenv  # ⬅️ Ajoute ça
load_dotenv()  # ⬅️ Et ça


class LinkedInAuth:
    """
    Gestionnaire d'authentification LinkedIn OAuth2 pour publication réelle
    """
    
    def __init__(self):


        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8000/callback')
        print("🔍 ID:", self.client_id)
        print("🔍 SECRET:", self.client_secret)
        print("🔍 REDIRECT_URI:", self.redirect_uri)
        
        # URLs LinkedIn OAuth2
        self.authorization_url = 'https://www.linkedin.com/oauth/v2/authorization'
        self.token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        
        # Scopes nécessaires pour publier
        self.scopes = ['openid', 'profile', 'w_member_social', 'email']
    
    def get_authorization_url(self):
        """Génère l'URL d'autorisation LinkedIn"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes),
            'state': 'random_state_string'  # Pour la sécurité
        }
        
        auth_url = f"{self.authorization_url}?{urlencode(params)}"
        return auth_url
    
    def authenticate(self):
        """Lance le processus d'authentification LinkedIn"""
        try:
            print("🔐 Début de l'authentification LinkedIn...")
            print("📋 Étapes à suivre:")
            print("1. Une page web va s'ouvrir")
            print("2. Connectez-vous à LinkedIn")
            print("3. Autorisez l'application")
            print("4. Copiez l'URL de redirection complète")
            
            # Générer et ouvrir l'URL d'autorisation
            auth_url = self.get_authorization_url()
            print(f"\n🌐 URL d'autorisation: {auth_url}")
            
            # Ouvrir automatiquement dans le navigateur
            webbrowser.open(auth_url)
            
            # Demander à l'utilisateur de coller l'URL de retour
            print("\n📋 Après autorisation, vous serez redirigé vers une URL.")
            print("⚠️ La page peut afficher une erreur, c'est normal.")
            print("📋 Copiez l'URL complète de la barre d'adresse:")
            
            callback_url = input("\n🔗 Collez l'URL de callback ici: ").strip()
            
            # Extraire le code d'autorisation
            parsed_url = urlparse(callback_url)
            query_params = parse_qs(parsed_url.query)
            
            if 'code' not in query_params:
                print("❌ Code d'autorisation non trouvé dans l'URL")
                return None
            
            auth_code = query_params['code'][0]
            print(f"✅ Code d'autorisation récupéré: {auth_code[:10]}...")
            
            # Échanger le code contre un access token
            access_token = self.exchange_code_for_token(auth_code)
            
            if access_token:
                print("✅ Authentification réussie!")
                print(f"🔑 Access Token: {access_token[:20]}...")
                
                # Sauvegarder le token
                self.save_token(access_token)
                return access_token
            else:
                print("❌ Échec de l'obtention du token")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de l'authentification: {e}")
            return None
    
    def exchange_code_for_token(self, auth_code):
        """Échange le code d'autorisation contre un access token"""
        try:
            data = {
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(self.token_url, data=data, headers=headers)
            
            if response.status_code == 200:
                token_data = response.json()
                return token_data.get('access_token')
            else:
                print(f"❌ Erreur token exchange: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur lors de l'échange: {e}")
            return None
    
    def save_token(self, access_token):
        """Sauvegarde le token dans un fichier sécurisé"""
        try:
            token_data = {
                'access_token': access_token,
                'timestamp': str(datetime.now())
            }
            
            with open('.linkedin_token.json', 'w') as f:
                json.dump(token_data, f)
            
            print("💾 Token sauvegardé dans .linkedin_token.json")
            print("⚠️ Ajoutez ce token dans votre .env: LINKEDIN_ACCESS_TOKEN")
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde token: {e}")
    
    def load_saved_token(self):
        """Charge un token sauvegardé"""
        try:
            if os.path.exists('.linkedin_token.json'):
                with open('.linkedin_token.json', 'r') as f:
                    token_data = json.load(f)
                return token_data.get('access_token')
        except:
            pass
        return None