#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Créateur d'offres d'emploi avec génération d'images et textes optimisés
"""

import os
import json
from datetime import datetime
from core.image_generator import ImageGenerator

class OfferCreator:
    def __init__(self):
        """Initialise le créateur d'offres"""
        self.image_generator = ImageGenerator()
        print("📝 OfferCreator initialisé")
    
    def create_offer(self, role: str, project_description: str, output_dir="generated_offers"):
        """
        Crée une offre de recrutement complète avec image et texte optimisé
        
        Args:
            role (str): Le rôle à recruter
            project_description (str): Description du projet
            output_dir (str): Dossier de sortie
            
        Returns:
            dict: Informations de l'offre créée
        """
        print(f"🎯 Création d'offre pour : {role}")
        
        try:
            # Génération du texte LinkedIn optimisé
            linkedin_text = self._generate_linkedin_text(role, project_description)
            
            # Génération du prompt image professionnel
            image_prompt = self._generate_image_prompt(role)
            
            # Préparation des chemins de sortie
            os.makedirs(output_dir, exist_ok=True)
            safe_filename = self._sanitize_filename(role)
            image_path = os.path.join(output_dir, f"{safe_filename}.png")
            
            # Génération de l'image
            print(f"🖼️ Génération de l'image pour {role}...")
            generated_image = self.image_generator.generate_image(image_prompt, image_path)
            
            if not generated_image or not os.path.exists(image_path):
                print(f"⚠️ Erreur génération image pour {role}")
                image_path = None
            
            # Création de l'objet offre
            offer = {
                "role": role,
                "text": linkedin_text,
                "image": image_path,
                "project_description": project_description,
                "created_at": datetime.now().isoformat(),
                "image_prompt": image_prompt
            }
            
            # Sauvegarde des métadonnées
            self._save_offer_metadata(offer, output_dir, safe_filename)
            
            print(f"✅ Offre créée pour {role}")
            return offer
            
        except Exception as e:
            print(f"❌ Erreur création offre pour {role}: {e}")
            return None
    
    def _generate_linkedin_text(self, role: str, project_description: str) -> str:
        """
        Génère un texte LinkedIn optimisé pour l'engagement
        
        Args:
            role (str): Le rôle à recruter
            project_description (str): Description du projet
            
        Returns:
            str: Texte LinkedIn formaté
        """
        # Templates de textes selon le rôle
        role_templates = {
            "data scientist": {
                "emoji": "📊",
                "skills": "Machine Learning, Python, SQL, Data Visualization",
                "challenge": "transformer les données en insights stratégiques"
            },
            "développeur": {
                "emoji": "💻",
                "skills": "développement logiciel, architecture, résolution de problèmes",
                "challenge": "créer des solutions techniques innovantes"
            },
            "product manager": {
                "emoji": "🚀",
                "skills": "gestion de produit, analyse stratégique, leadership",
                "challenge": "piloter la vision produit de demain"
            },
            "devops": {
                "emoji": "⚙️",
                "skills": "infrastructure, CI/CD, automatisation, cloud",
                "challenge": "optimiser nos processus de déploiement"
            },
            "designer": {
                "emoji": "🎨",
                "skills": "UX/UI, design thinking, prototypage",
                "challenge": "créer des expériences utilisateur exceptionnelles"
            }
        }
        
        # Détecter le template approprié basé sur le rôle
        template_key = None
        role_lower = role.lower()
        
        for key in role_templates.keys():
            if key in role_lower:
                template_key = key
                break
        
        # Template par défaut si aucun match
        if not template_key:
            template_info = {
                "emoji": "🎯",
                "skills": "expertise technique, innovation, collaboration",
                "challenge": "relever les défis de notre projet ambitieux"
            }
        else:
            template_info = role_templates[template_key]
        
        # Construction du texte LinkedIn
        linkedin_text = f"""🚀 NOUS RECRUTONS ! {template_info['emoji']}

📢 Offre d'emploi : {role}

🎯 LE DÉFI
{project_description[:200]}{'...' if len(project_description) > 200 else ''}

✨ PROFIL RECHERCHÉ
• Passionné(e) par {template_info['skills']}
• Prêt(e) à {template_info['challenge']}
• Esprit d'équipe et goût de l'innovation

🌟 POURQUOI NOUS REJOINDRE ?
• Projet innovant à fort impact
• Équipe dynamique et bienveillante  
• Opportunités d'évolution
• Technologies de pointe

📍 Poste à pourvoir immédiatement !

#Recrutement #{role.replace(' ', '')} #Innovation #TechJobs #Opportunité

👉 Intéressé(e) ? Contactez-nous en commentaire ou MP !"""

        return linkedin_text
    
    def _generate_image_prompt(self, role: str) -> str:
        """
        Génère un prompt optimisé pour l'image selon le rôle
        
        Args:
            role (str): Le rôle à recruter
            
        Returns:
            str: Prompt pour la génération d'image
        """
        # Prompts spécialisés par rôle
        role_prompts = {
            "data scientist": "Modern data analyst workspace, multiple monitors displaying graphs and charts, Python code on screen, clean office environment, professional lighting, blue and white color scheme",
            
            "développeur": "Software developer workspace, coding environment with multiple screens, modern keyboard and mouse, clean desk setup, programming languages visible, tech atmosphere, blue lighting",
            
            "product manager": "Modern business meeting room, strategic planning boards, laptop with project management tools, professional corporate environment, team collaboration space, clean design",
            
            "devops": "DevOps engineer workspace, server monitoring dashboards, cloud infrastructure diagrams, terminal windows, modern tech office, network cables, professional setup",
            
            "designer": "Creative designer workspace, large monitor with design software, color palettes, sketches, modern desk setup, artistic tools, creative environment, clean and inspirational",
            
            "marketing": "Digital marketing workspace, analytics dashboards, social media management tools, creative materials, modern office setup, collaborative environment",
            
            "sales": "Professional sales environment, CRM software on screen, business charts, meeting room setup, corporate atmosphere, success metrics displayed"
        }
        
        # Trouver le prompt approprié
        role_lower = role.lower()
        prompt = None
        
        for key, value in role_prompts.items():
            if key in role_lower:
                prompt = value
                break
        
        # Prompt générique si aucun match
        if not prompt:
            prompt = f"Professional {role} workspace, modern office environment, corporate style, clean desk setup, technology tools, blue and white color scheme, inspirational atmosphere"
        
        # Ajout de qualificatifs pour améliorer la qualité
        enhanced_prompt = f"{prompt}, high quality, professional photography, 4K resolution, corporate branding, modern aesthetic"
        
        return enhanced_prompt
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Nettoie un nom de fichier pour éviter les caractères problématiques
        
        Args:
            filename (str): Nom de fichier à nettoyer
            
        Returns:
            str: Nom de fichier nettoyé
        """
        # Remplacer les caractères spéciaux et espaces
        safe_name = filename.lower()
        safe_name = safe_name.replace(' ', '_')
        safe_name = safe_name.replace('/', '_')
        safe_name = safe_name.replace('\\', '_')
        safe_name = safe_name.replace(':', '_')
        safe_name = safe_name.replace('*', '_')
        safe_name = safe_name.replace('?', '_')
        safe_name = safe_name.replace('"', '_')
        safe_name = safe_name.replace('<', '_')
        safe_name = safe_name.replace('>', '_')
        safe_name = safe_name.replace('|', '_')
        
        # Limiter la longueur
        if len(safe_name) > 50:
            safe_name = safe_name[:50]
        
        return safe_name
    
    def _save_offer_metadata(self, offer: dict, output_dir: str, filename: str):
        """
        Sauvegarde les métadonnées de l'offre
        
        Args:
            offer (dict): Données de l'offre
            output_dir (str): Dossier de sortie
            filename (str): Nom de fichier
        """
        try:
            metadata_path = os.path.join(output_dir, f"{filename}_metadata.json")
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(offer, f, ensure_ascii=False, indent=2)
            
            print(f"📁 Métadonnées sauvegardées : {metadata_path}")
            
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde métadonnées: {e}")
    
    def create_batch_offers(self, roles_and_descriptions: list, output_dir="generated_offers"):
        """
        Crée plusieurs offres en batch
        
        Args:
            roles_and_descriptions (list): Liste de tuples (role, description)
            output_dir (str): Dossier de sortie
            
        Returns:
            list: Liste des offres créées
        """
        print(f"🔄 Création de {len(roles_and_descriptions)} offres en batch...")
        
        offers = []
        
        for i, (role, description) in enumerate(roles_and_descriptions, 1):
            print(f"\n📝 Traitement {i}/{len(roles_and_descriptions)}: {role}")
            
            offer = self.create_offer(role, description, output_dir)
            if offer:
                offers.append(offer)
        
        print(f"\n✅ Batch terminé : {len(offers)}/{len(roles_and_descriptions)} offres créées")
        return offers
    
    def get_generated_offers(self, output_dir="generated_offers"):
        """
        Récupère toutes les offres générées dans un dossier
        
        Args:
            output_dir (str): Dossier à scanner
            
        Returns:
            list: Liste des offres trouvées
        """
        if not os.path.exists(output_dir):
            return []
        
        offers = []
        
        for filename in os.listdir(output_dir):
            if filename.endswith('_metadata.json'):
                try:
                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        offer = json.load(f)
                        offers.append(offer)
                except Exception as e:
                    print(f"⚠️ Erreur lecture {filename}: {e}")
        
        return offers

# Test de la classe
def test_offer_creator():
    """Teste le créateur d'offres"""
    creator = OfferCreator()
    
    test_roles = [
        ("Data Scientist", "Développement d'une plateforme d'analyse prédictive pour l'e-commerce"),
        ("Développeur Full-Stack", "Création d'une application web moderne avec React et Python"),
        ("Product Manager", "Lancement d'un nouveau produit SaaS dans le domaine de la fintech")
    ]
    
    offers = creator.create_batch_offers(test_roles, "test_offers")
    
    print(f"\n📊 Test terminé : {len(offers)} offres créées")
    for offer in offers:
        print(f"  ✅ {offer['role']} - Image: {'OK' if offer['image'] else 'KO'}")

if __name__ == "__main__":
    test_offer_creator()