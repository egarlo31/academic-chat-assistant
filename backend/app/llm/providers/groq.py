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
            
        self.client = AsyncGroq(
            api_key=api_key, 
            timeout=GROQ_TIMEOUT_SECONDS, 
            max_retries=0                       #  Reintentos
        )
        self.model = GROQ_MODEL
        self.max_retries = GROQ_MAX_RETRIES

    async def _backoff(self, attempt: int):
        wait = (2 ** attempt) + random.uniform(0, 0.5)
        await asyncio.sleep(wait)

    async def generate(
        self,
        messages: list[dict[str, Any]],
        *,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:
        
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_completion_tokens=max_tokens,
                )
                
                # Validación de respuesta
                if not response.choices:
                    raise LLMProviderError("El proveedor devolvió una respuesta sin opciones.")
                
                content = response.choices[0].message.content
                if not isinstance(content, str) or not content.strip():
                    raise LLMProviderError("El proveedor no devolvió texto válido.")
                
                return content.strip()

            except RateLimitError as exc:
                if attempt >= self.max_retries:
                    raise LLMRateLimitError("Límite de uso de Groq excedido.") from exc
                logger.warning("Rate limit (429). Reintentando...")
                await self._backoff(attempt)

            except APITimeoutError as exc:
                if attempt >= self.max_retries:
                    raise LLMTimeoutError("Tiempo de espera agotado.") from exc
                logger.warning("Timeout. Reintentando...")
                await self._backoff(attempt)
                
            except APIConnectionError as exc:
                if attempt >= self.max_retries:
                    raise LLMProviderError("Fallo de conexión de red.") from exc
                logger.warning("Error de red. Reintentando...")
                await self._backoff(attempt)

            except APIStatusError as exc:
                # Errores 5xx son del servidor (reintentar). 
                # 4xx son errores del cliente (NO reintentar).
                if exc.status_code in [500, 502, 503, 504]:
                    if attempt >= self.max_retries:
                        raise LLMProviderError(f"Fallo en servidores de Groq: {exc.status_code}") from exc
                    logger.warning(f"Error 5xx ({exc.status_code}). Reintentando...")
                    await self._backoff(attempt)
                else:
                    # 400, 401, 403, 404, 422 no se arreglan solos.
                    logger.error(f"Error de cliente Groq: {exc.status_code}")
                    raise LLMProviderError(f"Error de configuración o petición: {exc.status_code}") from exc

            except LLMProviderError:
                # Errores de validación propios, no reintentar.
                raise
            except Exception as exc:
                logger.exception("Error inesperado en GroqProvider")
                raise LLMProviderError("Error interno al comunicarse con Groq.") from exc

    async def close(self):
        await self.client.close()