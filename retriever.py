import uuid
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from sqlalchemy.ext.asyncio import create_async_engine

# 1. Contrato de datos exigido por el ChatService
class RetrievedChunk(BaseModel):
    chunk_id: str
    text: str
    score: float
    title: str
    source_url: str
    metadata: dict

# 2. Interfaz abstracta base
class DocumentRetriever(ABC):
    @abstractmethod
    async def retrieve(self, query: str, limit: int = 3) -> List[RetrievedChunk]:
        pass

# 3. Implementación asíncrona con PostgreSQL
class PostgresRetriever(DocumentRetriever):
    def __init__(self, 
                 # Añadimos _async al dialecto de conexión
                 connection_string: str = "postgresql+psycopg_async://postgres:admin@localhost:5432/rag_db", 
                 collection_name: str = "tutor_c"):
        
        self.embedder = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://172.21.192.1:11434"
        )
        
        # Instanciamos el motor asíncrono explícitamente para evitar el error de LangChain
        self.async_engine = create_async_engine(connection_string)
        
        self.vector_store = PGVector(
            embeddings=self.embedder,
            collection_name=collection_name,
            connection=self.async_engine,
            use_jsonb=True
        )

    async def retrieve(self, query: str, limit: int = 3) -> List[RetrievedChunk]:
        try:
            # Búsqueda asíncrona nativa
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

if __name__ == "__main__":
    import asyncio
    
    async def probar_retriever():
        retriever = PostgresRetriever()
        resultados = await retriever.retrieve("¿Cómo usar punteros en C++?", limit=3)
        print(f"Se encontraron {len(resultados)} fragmentos.")
        for item in resultados:
            print(f"ID: {item.chunk_id} | Score: {item.score} | Título: {item.title}")
            
    asyncio.run(probar_retriever())