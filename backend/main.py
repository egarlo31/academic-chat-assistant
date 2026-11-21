from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from app.application.chat_service import ChatService
from app.llm.exceptions import LLMConfigurationError
from app.llm.providers.groq import GroqProvider
from app.rag.retriever import PostgresRetriever
from app.routes.chat import router as chat_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    provider = None
    retriever = None
    
    try:
        provider = GroqProvider()
        retriever = PostgresRetriever()
        app.state.chat_service = ChatService(provider, retriever)
        logger.info("ChatService, GroqProvider y PostgresRetriever inicializados correctamente.")
        yield
    except LLMConfigurationError as e:
        logger.critical(f"Error fatal de configuración: {e}")
        raise RuntimeError("No se puede iniciar el servidor sin configuración válida.") from e
    finally:
        # Cerrar cliente de Groq
        if provider is not None:
            try:
                await provider.close()
                logger.info("Cliente de Groq cerrado.")
            except Exception:
                logger.exception("Error al cerrar el cliente de Groq.")
                
        # Cerrar conexiones de PostgreSQL
        if retriever is not None:
            try:
                await retriever.close()
                logger.info("Conexiones del retriever PostgreSQL cerradas.")
            except Exception:
                logger.exception("Error al cerrar el retriever PostgreSQL.")

app = FastAPI(
    title="Academic Chat Assistant",
    lifespan=lifespan
)

app.include_router(chat_router)

@app.get("/health")
async def health():
    return {"status": "ok"}