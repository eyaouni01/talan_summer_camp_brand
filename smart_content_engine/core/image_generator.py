# smart_content_engine/core/image_generator.py

import os
import requests
from PIL import Image
import io
import time

class ImageGenerator:
    def __init__(self, hf_token=None):
        """
        Initialise le générateur avec accès à l'API Hugging Face
        """
        self.api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        self.hf_token = hf_token or os.getenv("HF_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.hf_token}"
        }

        print("🎨 ImageGenerator Hugging Face initialisé")
        print("🔗 Modèle : black-forest-labs/FLUX.1-schnell")
    
    def generate_image(self, prompt: str, output_path: str = "generated_image.png", **kwargs):
        """
        Génère une image via l'API HF à partir d'un prompt

        Args:
            prompt (str): Prompt textuel
            output_path (str): Chemin de sauvegarde
        """
        print(f"📝 Prompt : {prompt[:100]}...")
        start_time = time.time()

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": prompt},
                timeout=60  # en secondes
            )

            if response.status_code == 200 and response.headers['content-type'].startswith("image/"):
                image = Image.open(io.BytesIO(response.content))
                os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
                image.save(output_path, quality=95, optimize=True)
                print(f"✅ Image enregistrée : {output_path} ({time.time() - start_time:.1f}s)")
                return output_path
            else:
                print(f"❌ Erreur HTTP {response.status_code}")
                print(f"📩 Contenu brut : {response.text[:200]}...")
                return None

        except Exception as e:
            print(f"❌ Exception lors de la génération : {e}")
            return None
    
    def generate_batch(self, prompts: list, output_dir: str = "generated_images", **kwargs):
        """
        Génère un batch d’images via l’API
        """
        os.makedirs(output_dir, exist_ok=True)
        results = []

        print(f"🎨 Génération de {len(prompts)} images en batch...")

        for i, prompt in enumerate(prompts):
            output_path = os.path.join(output_dir, f"image_{i+1:03d}.png")
            result = self.generate_image(prompt, output_path, **kwargs)
            results.append(result)

        return results
    
    def unload_model(self):
        """
        Méthode placeholder pour compatibilité (ne fait rien ici)
        """
        print("ℹ️ Aucun modèle local à décharger avec API Hugging Face")

# Test
def test_image_generation():
    """
    Teste l’intégration du modèle HF
    """
    generator = ImageGenerator()
    prompts = [
        "Professional businessman in modern office, corporate style",
        "Modern tech workspace, computers, blue lighting",
        "Financial analyst with charts and screens, corporate environment"
    ]

    for i, prompt in enumerate(prompts):
        output_path = f"test_output/hf_image_{i+1}.png"
        result = generator.generate_image(prompt, output_path)
        if result:
            print(f"✅ Généré : {result}")
        else:
            print(f"❌ Échec pour le prompt {i+1}")

if __name__ == "__main__":
    test_image_generation()
