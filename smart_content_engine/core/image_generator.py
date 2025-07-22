# smart_content_engine/core/image_generator.py
import os
from diffusers import StableDiffusionPipeline
import torch

class ImageGenerator:
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
        self.pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    def generate_image(self, prompt: str, output_path: str = "generated_image.png"):
        image = self.pipe(prompt).images[0]
        # Crée le dossier de sortie s'il n'existe pas
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Sauvegarde de l’image
        image.save(output_path)
        
