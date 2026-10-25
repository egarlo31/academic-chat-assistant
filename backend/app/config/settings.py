import os
from pathlib import Path
from dotenv import load_dotenv

# Carga el .env desde la carpeta backend
BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")

def get_groq_api_key() -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("Falta GROQ_API_KEY en el archivo .env")
    return api_key

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
GROQ_TIMEOUT_SECONDS = float(os.getenv("GROQ_TIMEOUT_SECONDS", "30"))
GROQ_MAX_RETRIES = int(os.getenv("GROQ_MAX_RETRIES", "3"))