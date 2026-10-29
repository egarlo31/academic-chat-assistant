from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """Contrato común para proveedores de modelos de lenguaje."""

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, Any]],
        *,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:
        """Genera una respuesta y devuelve únicamente el texto."""
        raise NotImplementedError