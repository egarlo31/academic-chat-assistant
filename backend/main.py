from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from app.application.chat_service import ChatService
from app.llm.exceptions import LLMConfigurationError
from app.llm.providers.groq import GroqProvider
from app.routes.chat import router as chat_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    provider = None
    try:
        provider = GroqProvider()
        app.state.chat_service = ChatService(provider)
        logger.info("ChatService y GroqProvider inicializados correctamente.")
        yield
    except LLMConfigurationError as e:
        logger.critical(f"Error fatal de configuración: {e}")
        # Detiene el servidor si no hay API Key
        raise RuntimeError("No se puede iniciar el servidor sin configuración válida.") from e
    finally:
        if provider is not None:
            await provider.close()
            logger.info("Cliente de Groq cerrado.")

app = FastAPI(
    title="Academic Chat Assistant",
    lifespan=lifespan
)

app.include_router(chat_router)

@app.get("/health")
async def health():
    return {"status": "ok"}