import os
from dotenv import load_dotenv
import google.generativeai as genai

# Charger les variables d'environnement
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_image_prompt(reviewed_text: str) -> str:
    """
    Génère un prompt visuel à partir d’un contenu validé, inspiré pour une image de style LinkedIn.
    Le prompt est formaté pour être compatible avec Stable Diffusion (max 77 tokens, neutre et corporate).
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    instruction = (
        "Tu es un expert en création d'images professionnelles adaptées à LinkedIn. "
        "Transforme le texte ci-dessous en un prompt court, clair et visuellement inspirant. "
        "Objectif : créer une image de type corporate, moderne, sobre, crédible, sans éléments artistiques flous. "
        "Décris les visuels clés : ambiance, couleurs dominantes, objets, posture, arrière-plan, style graphique. "
        "Fais en sorte que le style de l’image soit adapté à un post LinkedIn (contexte business, innovation, tech ou communication). "
        "N’utilise pas de balises, ni d’instructions techniques. Pas plus de 77 tokens."
    )

    prompt = f"{instruction}\n\nTexte à transformer : {reviewed_text}"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[ERREUR] Impossible de générer le prompt : {e}"
