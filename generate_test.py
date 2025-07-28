import requests
from PIL import Image
import io

# Clé API
headers = {
    "Authorization": "Bearer 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"
}

def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    # Vérifie que le retour est bien une image
    if response.status_code == 200 and response.headers['content-type'].startswith("image/"):
        image = Image.open(io.BytesIO(response.content))
        return image
    else:
        print(f"Erreur HTTP {response.status_code}")
        print("Contenu brut :", response.text if response.text else "[Données binaires non affichables]")
        return None

# Utilisation
image = generate_image("A beautiful sunset over mountains")
if image:
    image.save("output.png")
    print("✅ Image enregistrée sous output.png")
