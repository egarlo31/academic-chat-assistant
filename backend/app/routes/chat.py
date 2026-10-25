import logging
from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.llm.base import LLMProvider
from app.llm.exceptions import LLMProviderError, LLMRateLimitError, LLMTimeoutError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    provider: LLMProvider = request.app.state.llm_provider
    
    messages = [
        {
            "role": "system",
            "content": "Eres Academic Chat Assistant, un tutor educativo especializado en C. Explica con claridad."
        },
        {"role": "user", "content": payload.message}
    ]

    try:
        answer = await provider.generate(messages)
        return ChatResponse(answer=answer)
        
    except LLMRateLimitError:
        raise HTTPException(status_code=429, detail="El asistente está ocupado. Intenta de nuevo en unos segundos.")
    except LLMTimeoutError:
        raise HTTPException(status_code=504, detail="El modelo tardó demasiado en responder.")
    except LLMProviderError as e:
        logger.error(f"Error del proveedor LLM: {e}")
        raise HTTPException(status_code=502, detail="Error de comunicación con el modelo de IA.")