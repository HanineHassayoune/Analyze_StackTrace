from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # charge les variables d'environnement depuis le fichier .env

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))# pour que le SDK de Google puisse communiquer avec l’API Gemini

model = genai.GenerativeModel("gemini-1.5-flash") # Initialisation de l'IA Gemini 1.5 Flash

app = FastAPI()

class LogInput(BaseModel):
    stack_trace: str

@app.post("/analyze")
async def analyze_log(log: LogInput):
    prompt = f"""
Tu es un assistant expert en analyse de logs.
Voici une stacktrace : {log.stack_trace}
Catégorise précisément cette erreur selon son type exact, sans te limiter à une liste prédéfinie.
Retourne uniquement la catégorie sous forme d'un texte court, par exemple 'Data Not Found Exception', 'Null Pointer Exception', 'Timeout Error', ou toute autre catégorie pertinente.
"""


    try:
        response = model.generate_content(prompt)
        category = response.text.strip()

        return {
            "category": category,
            "original": log.stack_trace
        }
    except Exception as e:
        return {"error": str(e)}
