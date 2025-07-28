import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, request
import threading
import webbrowser

load_dotenv()

class FacebookAuth:
    """
    Authentification Facebook avec récupération automatique du code via Flask.
    """
    def __init__(self):
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        self.redirect_uri = os.getenv('FACEBOOK_REDIRECT_URI', 'http://localhost:8000/callback')
        self.token_file = 'facebook_token.json'

    def get_auth_url(self):
        permissions = [
            'pages_manage_posts',
            'pages_read_engagement',
            'pages_show_list'
        ]
        base_url = "https://www.facebook.com/v18.0/dialog/oauth"
        params = {
            'client_id': self.app_id,
            'redirect_uri': self.redirect_uri,
            'scope': ','.join(permissions),
            'response_type': 'code',
            'state': 'facebook_auth'
        }
        return f"{base_url}?" + "&".join([f"{k}={v}" for k, v in params.items()])

    def exchange_code_for_token(self, code):
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'redirect_uri': self.redirect_uri,
            'code': code
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            token_data = response.json()

            if 'access_token' in token_data:
                user_info = self.get_user_info(token_data['access_token'])
                pages = self.get_user_pages(token_data['access_token'])

                self.save_token({
                    'access_token': token_data['access_token'],
                    'user_info': user_info,
                    'pages': pages,
                    'expires_at': datetime.now() + timedelta(seconds=token_data.get('expires_in', 3600)),
                    'created_at': datetime.now().isoformat()
                })
                return token_data['access_token']
            else:
                print(f"❌ Erreur token: {token_data}")
                return None

        except requests.RequestException as e:
            print(f"❌ Erreur réseau: {e}")
            return None

    def authenticate(self):
        """Lance le processus automatisé avec mini serveur Flask"""
        if not self.app_id or not self.app_secret:
            print("❌ FACEBOOK_APP_ID ou APP_SECRET manquants.")
            return None

        saved = self.load_saved_token()
        if saved:
            return saved['access_token']

        code_container = {}

        # Démarrage de Flask dans un thread
        app = Flask(__name__)

        @app.route("/callback")
        def callback():
            code = request.args.get("code")
            if code:
                code_container["code"] = code
                return "<h3>✅ Code reçu ! Vous pouvez retourner dans votre terminal.</h3>"
            return "<h3>❌ Code manquant</h3>"

        def run_flask():
            app.run(port=8000)

        thread = threading.Thread(target=run_flask)
        thread.daemon = True
        thread.start()

        # Ouvrir le navigateur
        auth_url = self.get_auth_url()
        print(f"🌐 Navigateur lancé vers: {auth_url}")
        webbrowser.open(auth_url)

        print("⏳ En attente de l'autorisation (max 120 secondes)...")

        # Attente active du code
        import time
        for _ in range(120):
            if "code" in code_container:
                break
            time.sleep(1)

        if "code" in code_container:
            return self.exchange_code_for_token(code_container["code"])
        else:
            print("❌ Délai dépassé sans réception du code.")
            return None

    def get_user_info(self, access_token):
        url = f"https://graph.facebook.com/v18.0/me"
        params = {'access_token': access_token, 'fields': 'id,name,email'}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def get_user_pages(self, access_token):
        url = f"https://graph.facebook.com/v18.0/me/accounts"
        params = {'access_token': access_token, 'fields': 'id,name,access_token,category'}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except:
            return []

    def save_token(self, token_data):
        try:
            if 'expires_at' in token_data and hasattr(token_data['expires_at'], 'isoformat'):
                token_data['expires_at'] = token_data['expires_at'].isoformat()
            with open(self.token_file, 'w', encoding='utf-8') as f:
                json.dump(token_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Token Facebook sauvegardé dans {self.token_file}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde token: {e}")

    def load_saved_token(self):
        if not os.path.exists(self.token_file):
            return None
        try:
            with open(self.token_file, 'r', encoding='utf-8') as f:
                token_data = json.load(f)
            if 'expires_at' in token_data:
                expires_at = datetime.fromisoformat(token_data['expires_at'])
                if datetime.now() >= expires_at:
                    print("⚠️ Token expiré")
                    return None
            return token_data
        except:
            return None
