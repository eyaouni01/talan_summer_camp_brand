#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application principale pour la génération et publication d'offres d'emploi LinkedIn
"""

import os
import sys
from pathlib import Path

# Ajout du chemin parent pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from core.offer_creator import OfferCreator
from core.linkedin_publisher import LinkedInPublisher
from core.role_detector import detect_roles
import json
from datetime import datetime

class JobOfferApp:
    def __init__(self):
        """Initialise l'application"""
        self.offer_creator = OfferCreator()
        self.linkedin_publisher = LinkedInPublisher()
        
        # Configuration
        self.output_dir = "generated_offers"
        self.config_file = "config/linkedin_config.json"
        
        # Créer les dossiers nécessaires
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs("config", exist_ok=True)
        os.makedirs("data/posted_content", exist_ok=True)
        
        print("🚀 Application JobOffer initialisée")
    
    def load_linkedin_token(self):
        """Charge le token LinkedIn depuis la config"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('access_token')
            else:
                print("⚠️ Fichier de configuration LinkedIn non trouvé")
                return self.create_config_file()
        except Exception as e:
            print(f"❌ Erreur lecture config: {e}")
            return None
    
    def create_config_file(self):
        """Crée un fichier de configuration pour LinkedIn"""
        print("\n📝 Configuration LinkedIn requise")
        print("Pour obtenir un token d'accès LinkedIn :")
        print("1. Allez sur https://developer.linkedin.com/")
        print("2. Créez une application")
        print("3. Obtenez votre access_token avec les scopes : w_member_social, r_liteprofile")
        
        token = input("\n🔑 Entrez votre LinkedIn access_token : ").strip()
        
        if token:
            config = {
                "access_token": token,
                "created_at": datetime.now().isoformat(),
                "scopes": ["w_member_social", "r_liteprofile"]
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuration sauvegardée dans {self.config_file}")
            return token
        
        return None
    
    def analyze_project_and_get_roles(self):
        """Analyse le projet et détecte les rôles nécessaires"""
        print("\n" + "="*60)
        print("🔍 ANALYSE DU PROJET ET DÉTECTION DES RÔLES")
        print("="*60)
        
        print("\nDécrivez votre projet en détail :")
        print("(Technologies, objectifs, contraintes, équipe actuelle, etc.)")
        
        project_description = input("\n📝 Description du projet : ").strip()
        
        if not project_description:
            print("❌ Description vide, utilisation d'un exemple")
            project_description = "Développement d'une plateforme e-commerce avec IA pour la recommandation personnalisée"
        
        print(f"\n🤖 Analyse en cours de : {project_description[:100]}...")
        
        try:
            # Détection des rôles via IA
            detected_roles = detect_roles(project_description)
            print(f"\n✅ Rôles détectés :\n{detected_roles}")
            
            return project_description, detected_roles
            
        except Exception as e:
            print(f"❌ Erreur détection des rôles : {e}")
            print("📋 Utilisation de rôles par défaut")
            
            default_roles = """
Rôles recommandés pour ce projet :
1. Data Scientist - Analyse et modélisation des données
2. Développeur Full-Stack - Développement de la plateforme
3. DevOps Engineer - Infrastructure et déploiement
4. Product Manager - Gestion de produit et stratégie
"""
            return project_description, default_roles
    
    def select_roles_to_recruit(self, detected_roles):
        """Permet à l'utilisateur de sélectionner les rôles à recruter"""
        print("\n" + "="*60)
        print("👥 SÉLECTION DES RÔLES À RECRUTER")
        print("="*60)
        
        print(f"Rôles détectés :\n{detected_roles}")
        
        print("\n📋 Entrez les rôles que vous souhaitez recruter (un par ligne)")
        print("💡 Exemple : Data Scientist, Développeur Python, etc.")
        print("⏹️  Tapez 'fin' pour terminer la saisie")
        
        selected_roles = []
        
        while True:
            role = input(f"\n🎯 Rôle {len(selected_roles) + 1} : ").strip()
            
            if role.lower() in ['fin', 'stop', 'done', '']:
                break
            
            selected_roles.append(role)
            print(f"✅ Ajouté : {role}")
        
        if not selected_roles:
            print("⚠️ Aucun rôle sélectionné, utilisation d'exemples")
            selected_roles = ["Data Scientist", "Développeur Full-Stack", "Product Manager"]
        
        print(f"\n📊 {len(selected_roles)} rôle(s) sélectionné(s) :")
        for i, role in enumerate(selected_roles, 1):
            print(f"   {i}. {role}")
        
        return selected_roles
    
    def generate_offers(self, project_description, selected_roles):
        """Génère les offres d'emploi avec images"""
        print("\n" + "="*60)
        print("🎨 GÉNÉRATION DES OFFRES D'EMPLOI")
        print("="*60)
        
        generated_offers = []
        
        for i, role in enumerate(selected_roles, 1):
            print(f"\n🔄 Génération {i}/{len(selected_roles)} : {role}")
            
            try:
                offer = self.offer_creator.create_offer(role, project_description, self.output_dir)
                
                if offer and os.path.exists(offer.get('image', '')):
                    generated_offers.append(offer)
                    print(f"✅ Offre générée pour {role}")
                    print(f"   📝 Texte : {offer['text'][:100]}...")
                    print(f"   🖼️  Image : {offer['image']}")
                else:
                    print(f"❌ Erreur génération pour {role}")
                    
            except Exception as e:
                print(f"❌ Erreur pour {role}: {e}")
        
        print(f"\n📊 Résultat : {len(generated_offers)}/{len(selected_roles)} offres générées")
        return generated_offers
    
    def publish_offers(self, offers):
        """Publie les offres sur LinkedIn"""
        if not offers:
            print("❌ Aucune offre à publier")
            return
        
        print("\n" + "="*60)
        print("📤 PUBLICATION SUR LINKEDIN")
        print("="*60)
        
        # Charger le token LinkedIn
        access_token = self.load_linkedin_token()
        if not access_token:
            print("❌ Token LinkedIn requis pour la publication")
            return
        
        # Diagnostic des permissions
        print("\n🔍 Vérification des permissions LinkedIn...")
        self.linkedin_publisher.diagnostic_permissions(access_token)
        
        # Publication des offres
        published_count = 0
        
        for i, offer in enumerate(offers, 1):
            print(f"\n📤 Publication {i}/{len(offers)} : {offer['role']}")
            
            try:
                result = self.linkedin_publisher.post_content_with_image(
                    content=offer['text'],
                    access_token=access_token,
                    image_path=offer['image']
                )
                
                if result and result.get('status') == 'success':
                    published_count += 1
                    print(f"✅ Publication réussie pour {offer['role']}")
                    print(f"🔗 URL : {result.get('post_url', 'N/A')}")
                else:
                    print(f"❌ Échec publication pour {offer['role']}")
                    
                # Pause entre publications
                if i < len(offers):
                    print("⏳ Pause de 30 secondes entre publications...")
                    import time
                    time.sleep(30)
                    
            except Exception as e:
                print(f"❌ Erreur publication {offer['role']}: {e}")
        
        print(f"\n📊 Résultat final : {published_count}/{len(offers)} offres publiées")
    
    def run(self):
        """Lance l'application complète"""
        print("🚀 GÉNÉRATEUR D'OFFRES D'EMPLOI LINKEDIN")
        print("="*60)
        
        try:
            # 1. Analyser le projet et détecter les rôles
            project_description, detected_roles = self.analyze_project_and_get_roles()
            
            # 2. Sélectionner les rôles à recruter
            selected_roles = self.select_roles_to_recruit(detected_roles)
            
            # 3. Générer les offres avec images
            offers = self.generate_offers(project_description, selected_roles)
            
            # 4. Publier sur LinkedIn
            if offers:
                publish = input("\n📤 Publier sur LinkedIn ? (o/n) : ").strip().lower()
                if publish in ['o', 'oui', 'y', 'yes']:
                    self.publish_offers(offers)
                else:
                    print("📁 Offres générées mais non publiées")
                    print(f"📂 Dossier : {os.path.abspath(self.output_dir)}")
            
            print("\n🎉 Application terminée avec succès !")
            
        except KeyboardInterrupt:
            print("\n⚠️ Application interrompue par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur générale : {e}")

def main():
    """Point d'entrée principal"""
    app = JobOfferApp()
    app.run()

if __name__ == "__main__":
    main()