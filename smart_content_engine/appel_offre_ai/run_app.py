#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple pour lancer l'application Streamlit des offres d'emploi
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Lance l'application Streamlit"""
    print("🚀 Lancement de l'application Job Offer Streamlit")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    current_dir = Path(__file__).parent
    os.chdir(current_dir)
    
    print(f"📁 Répertoire : {os.getcwd()}")
    
    # Vérifier les dépendances
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
    
    # Lancer l'application
    print("\n🌐 Lancement de l'application...")
    print("💡 URL : http://localhost:8501")
    print("💡 Ctrl+C pour arrêter")
    print("\n" + "="*50)
    
    try:
        subprocess.run([
            "streamlit", "run", "job_offer_streamlit.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main() 