import asyncio
import sys
from pathlib import Path

# Permite importar 'app' desde la carpeta backend/
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.llm.providers.groq import GroqProvider
from app.llm.exceptions import LLMError

async def main():
    print("Probando conexión con Groq...")
    try:
        provider = GroqProvider()
        answer = await provider.generate(
            [{"role": "user", "content": "Responde exactamente: Conexión exitosa."}]
        )
        print("\nRespuesta recibida:")
        print(answer)
        await provider.close()
    except LLMError as e:
        print(f"\nError de configuración o conexión: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(main())