import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Charger les variables d'environnement
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def clean_prompt_tokens(prompt):
    """Nettoie les prompts pour supprimer toute référence aux personnes ou éléments interdits."""
    forbidden = ['person', 'people', 'man', 'woman', 'face', 'hands', 'character', 'silhouette', 'portrait']
    for word in forbidden:
        prompt = re.sub(rf'\b{word}\b', '', prompt, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', prompt).strip()

def generate_image_prompt(reviewed_content: str,preferences=None) -> str:
    print("📥 Reviewed content:", reviewed_content)
    model = genai.GenerativeModel("gemini-2.5-flash")

    instruction = f"""
You are a prompt compressor. Based on the following text, generate a **very short and explicit visual image prompt** (max 15 words), in English, suitable for a professional LinkedIn image.

RULES:
- Be direct, no storytelling, no adjectives, no colors.
- NO people or references to humans or body parts.
- Just describe the core visual concept to illustrate.
- Avoid style, focus on WHAT to show.

EXAMPLES:
- "Comparison between MCP and A2A"
- "Job offer for data analyst"
- "Timeline of product development"
- "LinkedIn dashboard with engagement KPIs"

TEXT:
{reviewed_content[:300]}...
"""

    try:
        response = model.generate_content(instruction)
        prompt = clean_prompt_tokens(response.text.strip())
        words = prompt.split()
        if len(words) > 15:
            prompt = ' '.join(words[:15])

        print(f"✅ Short visual prompt: {prompt}")
        return prompt

    except Exception as e:
        print(f"⚠️ Prompt generation failed: {e}")
        return "Business chart or concept diagram for LinkedIn post"
