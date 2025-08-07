import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyAXDI5jl1gaQ-WUUJF_ANiVqf_woof_38E")

genai.configure(api_key=GOOGLE_API_KEY)

MODEL_NAME = "gemini-2.5-flash"
