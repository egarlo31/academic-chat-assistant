import uuid
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from sqlalchemy.ext.asyncio import create_async_engine

class RetrievedChunk(BaseModel):
    chunk_id: str
    text: str
    score: float
    title: str
    source_url: str
    metadata: dict

class DocumentRetriever(ABC):
    @abstractmethod
    async def retrieve(self, query: str, limit: int = 3) -> List[RetrievedChunk]:
        pass

class PostgresRetriever(DocumentRetriever):
    def __init__(self, 
                 connection_string: str = "postgresql+psycopg_async://postgres:admin@localhost:5432/rag_db", 
                 collection_name: str = "tutor_c"):
        
        # Modelo local gratuito inyectado (asegúrate de que la URL sea correcta para tu WSL)
        self.embedder = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://127.0.0.1:11434" 
        )
        
        self.async_engine = create_async_engine(connection_string)
        
        self.vector_store = PGVector(
            embeddings=self.embedder,
            collection_name=collection_name,
            connection=self.async_engine,
            use_jsonb=True
        )

    async def retrieve(self, query: str, limit: int = 3) -> List[RetrievedChunk]:
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
            print(f"Error en la recuperación desde PostgreSQL: {e}")
            return []