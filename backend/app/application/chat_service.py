from app.llm.base import LLMProvider

class ChatService:
    """Coordina el caso de uso de conversación académica."""
    
    def __init__(self, llm_provider: LLMProvider) -> None:
        self._llm_provider = llm_provider

    async def ask(self, message: str) -> str:
        """Responde una pregunta académica."""
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres Academic Chat Assistant, un tutor educativo "
                    "especializado en programación en C. "
                    "Explica con claridad y utiliza ejemplos detallados "
                    "cuando sean útiles."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ]
        return await self._llm_provider.generate(messages)