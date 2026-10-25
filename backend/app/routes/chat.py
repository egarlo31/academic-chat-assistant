import logging
from fastapi import APIRouter, HTTPException, Request, status

from app.application.chat_service import ChatService
from app.llm.exceptions import LLMProviderError, LLMRateLimitError, LLMTimeoutError
from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    # Obtenemos el servicio
    service: ChatService = request.app.state.chat_service
    
    try:
        answer = await service.ask(payload.message)
        return ChatResponse(answer=answer)
        
    except LLMRateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="El asistente está ocupado. Intenta de nuevo más tarde."
        ) from exc
    except LLMTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="El modelo tardó demasiado en responder."
        ) from exc
    except LLMProviderError as exc:
        logger.warning("Falló la generación mediante el proveedor LLM.")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No fue posible obtener una respuesta del asistente."
        ) from exc