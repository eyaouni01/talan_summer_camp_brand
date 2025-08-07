#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'images via l'API Hugging Face
Version corrigée avec gestion d'erreurs améliorée
"""

import os
import requests
from PIL import Image
import io
import time

class ImageGenerator:
    def __init__(self, hf_token=None):
        """
        Initialise le générateur avec accès à l'API Hugging Face
        
        Args:
            hf_token (str): Token Hugging Face (optionnel, utilise la variable d'env si None)
        """
        # Token par défaut ou depuis l'environnement
        self.hf_token = hf_token or "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"
        
        # Configuration API
        self.api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        self.headers = {
            "Authorization": f"Bearer {self.hf_token}"
        }
        
        print("🎨 ImageGenerator Hugging Face initialisé")
        print(f"🔗 Modèle : black-forest-labs/FLUX.1-schnell")
        print(f"🔑 Token configuré : {'Oui' if self.hf_token else 'Non'}")
    
    def generate_image(self, prompt: str, output_path: str = "generated_image.png", **kwargs):
        """
        Génère une image via l'API HF à partir d'un prompt
        
        Args:
            prompt (str): Prompt textuel pour la génération
            output_path (str): Chemin de sauvegarde de l'image
            **kwargs: Arguments supplémentaires (compatibilité)
            
        Returns:
            str|None: Chemin de l'image générée ou None en cas d'erreur
        """
        print(f"📝 Génération pour : {prompt[:100]}...")
        start_time = time.time()
        
        try:
            # Préparation du dossier de sortie
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Paramètres de la requête
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": kwargs.get("num_inference_steps", 4),  # FLUX.1-schnell optimisé pour 4 steps
                    "guidance_scale": kwargs.get("guidance_scale", 0.0),  # FLUX.1-schnell fonctionne mieux avec guidance_scale=0
                    "width": kwargs.get("width", 1024),
                    "height": kwargs.get("height", 1024)
                }
            }
            
            # Tentative de génération avec retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"🔄 Tentative {attempt + 1}/{max_retries}...")
                    
                    response = requests.post(
                        self.api_url,
                        headers=self.headers,
                        json=payload,
                        timeout=60
                    )
                    
                    # Vérification du statut de réponse
                    if response.status_code == 200:
                        # Vérifier que c'est bien une image
                        if response.headers.get('content-type', '').startswith('image/'):
                            # Traitement de l'image
                            image = Image.open(io.BytesIO(response.content))
                            
                            # Conversion en RGB si nécessaire (pour PNG)
                            if image.mode in ('RGBA', 'LA', 'P'):
                                background = Image.new('RGB', image.size, (255, 255, 255))
                                if image.mode == 'P':
                                    image = image.convert('RGBA')
                                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                                image = background
                            
                            # Sauvegarde avec optimisation
                            image.save(output_path, format='PNG', quality=95, optimize=True)
                            
                            generation_time = time.time() - start_time
                            print(f"✅ Image générée : {output_path} ({generation_time:.1f}s)")
                            print(f"📏 Dimensions : {image.size}")
                            
                            return output_path
                        
                        else:
                            # Réponse texte (probablement erreur)
                            error_text = response.text
                            print(f"❌ Erreur API : {error_text}")
                            
                            # Si le modèle est en cours de chargement, attendre
                            if "loading" in error_text.lower() or "warming up" in error_text.lower():
                                wait_time = 20 * (attempt + 1)
                                print(f"⏳ Modèle en chargement, attente {wait_time}s...")
                                time.sleep(wait_time)
                                continue
                    
                    elif response.status_code == 503:
                        # Service indisponible, retry avec attente
                        wait_time = 10 * (attempt + 1)
                        print(f"⏳ Service indisponible, retry dans {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    
                    else:
                        print(f"❌ Erreur HTTP {response.status_code}: {response.text}")
                        if attempt < max_retries - 1:
                            time.sleep(5)
                            continue
                        break
                
                except requests.exceptions.Timeout:
                    print(f"⏰ Timeout sur tentative {attempt + 1}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
                
                except Exception as e:
                    print(f"❌ Erreur requête tentative {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
                    break
            
            print("❌ Échec de génération après tous les retries")
            return None
            
        except Exception as e:
            print(f"❌ Erreur générale génération image: {e}")
            return None
    
    def generate_batch(self, prompts: list, output_dir: str = "generated_images", **kwargs):
        """
        Génère un batch d'images via l'API
        
        Args:
            prompts (list): Liste des prompts
            output_dir (str): Dossier de sortie
            **kwargs: Arguments supplémentaires
            
        Returns:
            list: Liste des chemins des images générées
        """
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        print(f"🎨 Génération de {len(prompts)} images en batch...")
        
        for i, prompt in enumerate(prompts):
            print(f"\n📝 Image {i+1}/{len(prompts)}")
            
            output_path = os.path.join(output_dir, f"image_{i+1:03d}.png")
            result = self.generate_image(prompt, output_path, **kwargs)
            results.append(result)
            
            # Pause entre les générations pour éviter le rate limiting
            if i < len(prompts) - 1:
                print("⏳ Pause 3s entre générations...")
                time.sleep(3)
        
        successful = [r for r in results if r is not None]
        print(f"\n📊 Batch terminé: {len(successful)}/{len(prompts)} images générées")
        
        return results
    
    def unload_model(self):
        """
        Méthode placeholder pour compatibilité (ne fait rien avec l'API)
        """
        print("ℹ️ Aucun modèle local à décharger avec l'API Hugging Face")
    
    def test_connection(self):
        """
        Teste la connexion à l'API Hugging Face
        
        Returns:
            bool: True si la connexion fonctionne
        """
        print("🔍 Test de connexion à l'API...")
        
        try:
            # Test avec un prompt simple
            test_prompt = "simple test image, white background"
            test_path = "test_connection.png"
            
            result = self.generate_image(test_prompt, test_path)
            
            if result and os.path.exists(test_path):
                # Nettoyer le fichier de test
                try:
                    os.remove(test_path)
                except:
                    pass
                
                print("✅ Connexion API fonctionnelle")
                return True
            else:
                print("❌ Échec du test de connexion")
                return False
                
        except Exception as e:
            print(f"❌ Erreur test connexion: {e}")
            return False
    
    def get_model_info(self):
        """
        Récupère les informations sur le modèle utilisé
        
        Returns:
            dict: Informations sur le modèle
        """
        return {
            "model_name": "black-forest-labs/FLUX.1-schnell",
            "api_url": self.api_url,
            "type": "diffusion_model",
            "provider": "Hugging Face",
            "optimal_steps": 4,
            "recommended_guidance": 0.0,
            "max_resolution": "1024x1024",
            "supported_formats": ["PNG", "JPEG"]
        }

# Fonctions utilitaires pour la génération d'images
def create_professional_prompt(role: str, style: str = "corporate") -> str:
    """
    Crée un prompt professionnel optimisé pour un rôle donné
    
    Args:
        role (str): Le rôle professionnel
        style (str): Le style souhaité
        
    Returns:
        str: Prompt optimisé
    """
    base_styles = {
        "corporate": "clean corporate office, professional lighting, modern design",
        "tech": "modern tech workspace, multiple monitors, coding environment",
        "creative": "creative studio, inspiring workspace, artistic tools",
        "minimal": "minimalist workspace, clean lines, simple design"
    }
    
    style_desc = base_styles.get(style, base_styles["corporate"])
    
    prompt = f"Professional {role} workspace, {style_desc}, high quality, 4K resolution, professional photography"
    
    return prompt

def test_image_generation():
    """
    Teste l'intégration du modèle HF avec différents scénarios
    """
    print("🧪 === TEST GÉNÉRATION D'IMAGES ===")
    
    generator = ImageGenerator()
    
    # Test de connexion
    if not generator.test_connection():
        print("❌ Impossible de continuer les tests")
        return
    
    # Tests avec différents prompts
    test_cases = [
        {
            "name": "Data Scientist",
            "prompt": create_professional_prompt("Data Scientist", "tech"),
            "output": "test_output/data_scientist.png"
        },
        {
            "name": "Product Manager", 
            "prompt": create_professional_prompt("Product Manager", "corporate"),
            "output": "test_output/product_manager.png"
        },
        {
            "name": "Designer",
            "prompt": create_professional_prompt("UX Designer", "creative"),
            "output": "test_output/designer.png"
        }
    ]
    
    os.makedirs("test_output", exist_ok=True)
    
    successful_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}/{len(test_cases)}: {test_case['name']}")
        
        result = generator.generate_image(
            test_case["prompt"], 
            test_case["output"]
        )
        
        if result and os.path.exists(result):
            successful_tests += 1
            print(f"✅ Test réussi: {result}")
        else:
            print(f"❌ Test échoué pour {test_case['name']}")
    
    print(f"\n📊 Résultat des tests: {successful_tests}/{len(test_cases)} réussis")
    
    # Affichage des informations du modèle
    model_info = generator.get_model_info()
    print(f"\n📋 Modèle utilisé: {model_info['model_name']}")
    print(f"🔧 Steps optimaux: {model_info['optimal_steps']}")
    print(f"📏 Résolution max: {model_info['max_resolution']}")

if __name__ == "__main__":
    test_image_generation()