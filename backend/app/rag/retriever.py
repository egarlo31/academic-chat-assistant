import uuid
import logging
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from sqlalchemy.ext.asyncio import create_async_engine

from app.config.settings import (
    PG_VECTOR_COLLECTION, 
    get_database_url_async,
    OLLAMA_BASE_URL,
    OLLAMA_EMBEDDING_MODEL,
    RAG_TOP_K
)

logger = logging.getLogger(__name__)

class RetrievedChunk(BaseModel):
    chunk_id: str
    text: str
    score: float
    title: str
    source_url: str
    metadata: dict

class DocumentRetriever(ABC):
    @abstractmethod
    async def retrieve(self, query: str, limit: int = RAG_TOP_K) -> List[RetrievedChunk]:
        pass

class PostgresRetriever(DocumentRetriever):
    def __init__(self, connection_string: str | None = None, collection_name: str = PG_VECTOR_COLLECTION):
        if connection_string is None:
            connection_string = get_database_url_async()
            
        self.embedder = OllamaEmbeddings(
            model=OLLAMA_EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        
        self.async_engine = create_async_engine(connection_string)
        
        self.vector_store = PGVector(
            embeddings=self.embedder,
            collection_name=collection_name,
            connection=self.async_engine,
            use_jsonb=True
        )
        logger.info("PostgresRetriever inicializado correctamente.")

    async def close(self) -> None:
        """Cierra el pool de conexiones de la base de datos."""
        await self.async_engine.dispose()

    async def retrieve(self, query: str, limit: int = RAG_TOP_K) -> List[RetrievedChunk]:
        try:
            resultados = await self.vector_store.asimilarity_search_with_score(query, k=limit)
            
            chunks_recuperados = []
            for doc, distancia in resultados:
                score_similitud = 1.0 - distancia
                chunk = RetrievedChunk(
                    chunk_id=doc.metadata.get("chunk_id", str(uuid.uuid4())),
                    text=doc.page_content,
                    score=round(score_similitud, 4),
                    title=doc.metadata.get("title", "Documentación C"),
                    source_url=doc.metadata.get("source", "https://gcc.gnu.org/"),
                    metadata=doc.metadata
                )
                chunks_recuperados.append(chunk)
                
            chunks_recuperados.sort(key=lambda x: x.score, reverse=True)
            return chunks_recuperados
            
        except Exception as e:
            logger.error(f"Error en la recuperación desde PostgreSQL: {e}")
            return []