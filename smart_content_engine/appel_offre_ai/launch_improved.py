#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement pour l'interface Streamlit améliorée
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Lance l'application Streamlit améliorée"""
    print("🚀 Lancement de l'interface Job Offer améliorée")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    current_dir = Path(__file__).parent
    os.chdir(current_dir)
    
    print(f"📁 Répertoire : {os.getcwd()}")
    
    # Vérifications préalables
    print("\n🔍 Vérifications...")
    
    # Vérifier Streamlit
    try:
        import streamlit
        print("✅ Streamlit installé")
    except ImportError:
        print("❌ Streamlit non installé")
        print("💡 Installez avec : pip install streamlit")
        return
    
    # Vérifier le fichier principal
    if not os.path.exists("job_offer_streamlit.py"):
        print("❌ Fichier job_offer_streamlit.py non trouvé")
        return
    print("✅ Fichier principal trouvé")
    
    # Vérifier les modules requis
    required_modules = [
        "core/role_detector.py",
        "core/offer_creator.py",
        "core/linkedin_publisher.py"
    ]
    
    missing_modules = []
    for module in required_modules:
        if not os.path.exists(module):
            missing_modules.append(module)
    
    if missing_modules:
        print(f"⚠️ Modules manquants : {missing_modules}")
        print("💡 Vérifiez la structure du projet")
    else:
        print("✅ Tous les modules requis sont présents")
    
    # Configuration pour le mode light
    env_vars = {
        "STREAMLIT_SERVER_HEADLESS": "false",  # Garder l'interface visible
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
        "STREAMLIT_SERVER_ENABLE_CORS": "false",
        "STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION": "false",
        "STREAMLIT_SERVER_ENABLE_STATIC_SERVING": "true",
        "STREAMLIT_SERVER_MAX_UPLOAD_SIZE": "200",
        "STREAMLIT_SERVER_FILE_WATCHER_TYPE": "none"
    }
    
    # Mettre à jour l'environnement
    os.environ.update(env_vars)
    
    print("\n🎨 Interface améliorée activée")
    print("💡 Nouvelles fonctionnalités :")
    print("   - Affichage structuré des profils détectés")
    print("   - Interface interactive pour la sélection")
    print("   - Statistiques et métriques visuelles")
    print("   - Design moderne et responsive")
    
    # Lancer l'application
    print("\n🌐 Lancement de l'application...")
    print("💡 URL : http://localhost:8501")
    print("💡 Ctrl+C pour arrêter")
    print("\n" + "="*60)
    
    try:
        subprocess.run([
            "streamlit", "run", "job_offer_streamlit.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "false",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
            "--server.enableStaticServing", "true",
            "--server.maxUploadSize", "200",
            "--server.fileWatcherType", "none",
            "--browser.gatherUsageStats", "false",
            "--logger.level", "info"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        print("💡 Vérifiez que Streamlit est bien installé")

if __name__ == "__main__":
    main() 