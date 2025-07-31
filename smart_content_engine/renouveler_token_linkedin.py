#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour renouveler le token LinkedIn
"""

import os
import sys
from pathlib import Path

# Ajouter le chemin pour les imports
sys.path.append(str(Path(__file__).parent))

from linkedin_auth import LinkedInAuth

def main():
    print("🔄 Renouvellement du token LinkedIn")
    print("=" * 40)
    
    try:
        # Initialiser l'authentification LinkedIn
        auth = LinkedInAuth()
        
        print("📋 Étapes à suivre:")
        print("1. Une page web va s'ouvrir")
        print("2. Connectez-vous à LinkedIn")
        print("3. Autorisez l'application")
        print("4. Copiez l'URL de redirection complète")
        
        # Lancer l'authentification
        token = auth.authenticate()
        
        if token:
            print("\n✅ Token LinkedIn renouvelé avec succès!")
            print(f"🔑 Nouveau token: {token[:20]}...")
            print("💾 Token sauvegardé dans .linkedin_token.json")
            print("\n🎉 Vous pouvez maintenant relancer votre application!")
        else:
            print("\n❌ Échec du renouvellement du token")
            print("💡 Vérifiez vos credentials LinkedIn et réessayez")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("💡 Assurez-vous que vos variables d'environnement sont configurées:")
        print("   - LINKEDIN_CLIENT_ID")
        print("   - LINKEDIN_CLIENT_SECRET")
        print("   - LINKEDIN_REDIRECT_URI")

if __name__ == "__main__":
    main() 