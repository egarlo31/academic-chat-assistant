import asyncio
import logging
import random
from typing import Any

from groq import (
    AsyncGroq,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    RateLimitError,
)

from app.config.settings import (
    GROQ_MAX_RETRIES,
    GROQ_MODEL,
    GROQ_TIMEOUT_SECONDS,
    get_groq_api_key,
)
from app.llm.base import LLMProvider
from app.llm.exceptions import (
    LLMConfigurationError,
    LLMProviderError,
    LLMRateLimitError,
    LLMTimeoutError,
)

logger = logging.getLogger(__name__)

class GroqProvider(LLMProvider):
    def __init__(self):
        try:
            api_key = get_groq_api_key()
        except ValueError as e:
            raise LLMConfigurationError(str(e))
            
        # max_retries=0 porque nosotros manejamos los reintentos abajo
        self.client = AsyncGroq(
            api_key=api_key, 
            timeout=GROQ_TIMEOUT_SECONDS, 
            max_retries=0
        )
        self.model = GROQ_MODEL

    async def generate(
        self,
        messages: list[dict[str, Any]],
        *,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:
        last_exception = None

        for attempt in range(GROQ_MAX_RETRIES + 1):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_completion_tokens=max_tokens,
                )
                return response.choices[0].message.content

            except RateLimitError as e:
                last_exception = e
                if attempt == GROQ_MAX_RETRIES:
                    raise LLMRateLimitError("Límite de uso de Groq excedido.") from e
                wait = (2 ** attempt) + random.uniform(0, 0.5)
                logger.warning(f"Rate limit (429). Reintentando en {wait:.2f}s...")
                await asyncio.sleep(wait)

            except APITimeoutError as e:
                last_exception = e
                if attempt == GROQ_MAX_RETRIES:
                    raise LLMTimeoutError("Tiempo de espera agotado al conectar con Groq.") from e
                wait = (2 ** attempt) + random.uniform(0, 0.5)
                logger.warning(f"Timeout. Reintentando en {wait:.2f}s...")
                await asyncio.sleep(wait)

            except APIStatusError as e:
                # 401, 403, 404 no se reintentan porque no se arreglan solos
                if e.status_code in [401, 403, 404]:
                    logger.error(f"Error de cliente Groq: {e.status_code}")
                    raise LLMProviderError(f"Error de configuración con Groq: {e.status_code}") from e
                
                last_exception = e
                if attempt == GROQ_MAX_RETRIES:
                    raise LLMProviderError(f"Fallo de Groq después de varios intentos: {e.status_code}") from e
                wait = (2 ** attempt) + random.uniform(0, 0.5)
                await asyncio.sleep(wait)

            except Exception as e:
                logger.exception("Error inesperado en GroqProvider")
                raise LLMProviderError("Error interno al comunicarse con Groq.") from e

        raise LLMProviderError(f"Fallo después de {GROQ_MAX_RETRIES} intentos: {last_exception}")

    async def close(self):
        await self.client.close()