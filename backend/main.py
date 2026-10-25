from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.llm.providers.groq import GroqProvider  
from app.llm.exceptions import LLMConfigurationError

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al arrancar FastAPI, inicializamos el cliente de Groq
    try:
        app.state.llm_provider = GroqProvider()
        print("GroqProvider inicializado correctamente.")
    except LLMConfigurationError as e:
        print(f"ADVERTENCIA: {e}")
        # Opcionalmente podrías lanzar el error aquí para detener el servidor
    
    yield
    
    # Al apagar FastAPI, cerramos la conexión
    if hasattr(app.state, "llm_provider"):
        await app.state.llm_provider.close()

app = FastAPI(
    title="Academic Chat Assistant",
    lifespan=lifespan
)

app.include_router(chat_router)

@app.get("/health")
async def health():
    return {"status": "ok"}