from app.llm.base import LLMProvider
from app.rag.retriever import PostgresRetriever # Ajusta esta ruta según dónde esté tu archivo

class ChatService:
    """Coordina el caso de uso de conversación académica inyectando contexto RAG."""
    
    def __init__(self, llm_provider: LLMProvider, retriever: PostgresRetriever = None) -> None:
        self._llm_provider = llm_provider
        # Instanciamos el retriever automáticamente si no se pasa uno
        self._retriever = retriever or PostgresRetriever()

    async def ask(self, message: str) -> str:
        """Responde una pregunta académica inyectando vectores."""
        
        # 1. Extraer los fragmentos asíncronamente
        chunks = await self._retriever.retrieve(query=message, limit=3)
        
        # 2. Ensamblar los fragmentos usando el atributo 'text' de tu RetrievedChunk
        contexto_formateado = "\n\n---\n\n".join([chunk.text for chunk in chunks])
        
        # 3. Construir el prompt estructurado
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres Academic Chat Assistant, un tutor educativo especializado en C/C++. "
                    "Responde a la duda del estudiante basándote ESTRICTAMENTE en el siguiente "
                    "contexto extraído de la documentación oficial. "
                    "Si la respuesta no se encuentra en este contexto, indícalo claramente "
                    "para no desinformar al alumno.\n\n"
                    f"CONTEXTO DOCUMENTAL:\n{contexto_formateado}"
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ]
        
        return await self._llm_provider.generate(messages)