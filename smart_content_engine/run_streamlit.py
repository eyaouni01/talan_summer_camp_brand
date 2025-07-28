#!/usr/bin/env python3
# ============================================================================
# 📄 run_streamlit.py - Script de lancement pour l'application Streamlit
# ============================================================================
import subprocess
import sys
import os

def main():
    """Lance l'application Streamlit"""
    print("🚀 Lancement de Smart Content Engine - Interface Streamlit")
    print("=" * 60)
    
    # Vérifier que Streamlit est installé
    try:
        import streamlit
        print("✅ Streamlit est installé")
    except ImportError:
        print("❌ Streamlit n'est pas installé")
        print("📦 Installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installé avec succès")
    
    # Vérifier les dépendances
    required_packages = [
        "PIL", "google.generativeai", "requests", "python-dotenv", 
        "pyyaml", "requests-oauthlib", "schedule", "beautifulsoup4", "aiofiles"
    ]
    
    print("\n🔍 Vérification des dépendances...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} manquant")
            print(f"📦 Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # Vérifier le fichier .env
    if not os.path.exists(".env"):
        print("\n⚠️ Fichier .env non trouvé")
        print("📝 Création d'un template .env...")
        with open(".env", "w") as f:
            f.write("""# Configuration des API
GOOGLE_API_KEY=your_google_api_key_here
LINKEDIN_ACCESS_TOKEN=your_linkedin_token_here

# Configuration LinkedIn (optionnel)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
""")
        print("✅ Template .env créé")
        print("⚠️ N'oubliez pas de configurer vos clés API dans le fichier .env")
    
    print("\n🌐 Lancement de l'application...")
    print("📱 L'interface sera disponible dans votre navigateur")
    print("🔗 URL: http://localhost:8501")
    print("\n" + "=" * 60)
    
    # Lancer Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application fermée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

if __name__ == "__main__":
    main() 