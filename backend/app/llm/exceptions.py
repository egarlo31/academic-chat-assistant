class LLMError(Exception):
    """Error base del subsistema de modelos de lenguaje."""


class LLMConfigurationError(LLMError):
    """La configuración del proveedor es incorrecta."""


class LLMRateLimitError(LLMError):
    """El proveedor rechazó la solicitud por límite de uso."""


class LLMTimeoutError(LLMError):
    """La solicitud excedió el tiempo de espera."""


class LLMProviderError(LLMError):
    """El proveedor no pudo completar la solicitud."""