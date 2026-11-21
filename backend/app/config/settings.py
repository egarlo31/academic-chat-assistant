import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import URL



# CARGA DE ENTORNO

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)



# UTILIDADES DE VALIDACIÓN

def get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()

    if not value:
        raise ValueError(
            f"Falta configurar {name} en el archivo .env"
        )

    return value


def get_int_env(name: str, default: str) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError as exc:
        raise RuntimeError(
            f"{name} debe ser un número entero."
        ) from exc


def get_float_env(name: str, default: str) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError as exc:
        raise RuntimeError(
            f"{name} debe ser un número."
        ) from exc



# GROQ

def get_groq_api_key() -> str:
    return get_required_env("GROQ_API_KEY")


GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
).strip()

GROQ_TIMEOUT_SECONDS = get_float_env(
    "GROQ_TIMEOUT_SECONDS",
    "30",
)

GROQ_MAX_RETRIES = get_int_env(
    "GROQ_MAX_RETRIES",
    "3",
)

if not GROQ_MODEL:
    raise RuntimeError("GROQ_MODEL no puede estar vacío.")

if GROQ_TIMEOUT_SECONDS <= 0:
    raise RuntimeError(
        "GROQ_TIMEOUT_SECONDS debe ser mayor que cero."
    )

if GROQ_MAX_RETRIES < 0:
    raise RuntimeError(
        "GROQ_MAX_RETRIES no puede ser negativo."
    )



# POSTGRESQL

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost",
).strip()

POSTGRES_PORT = get_int_env(
    "POSTGRES_PORT",
    "5432",
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "rag_db",
).strip()

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "postgres",
).strip()


def build_db_url(driver: str) -> str:
    """
    Construye una URL de PostgreSQL utilizando las variables de entorno.

    La contraseña se valida únicamente cuando se solicita construir la URL.
    """

    password = get_required_env("POSTGRES_PASSWORD")

    if not POSTGRES_HOST:
        raise ValueError("POSTGRES_HOST no puede estar vacío.")

    if not POSTGRES_DB:
        raise ValueError("POSTGRES_DB no puede estar vacío.")

    if not POSTGRES_USER:
        raise ValueError("POSTGRES_USER no puede estar vacío.")

    if not 1 <= POSTGRES_PORT <= 65535:
        raise ValueError(
            "POSTGRES_PORT debe estar entre 1 y 65535."
        )

    url = URL.create(
        drivername=driver,
        username=POSTGRES_USER,
        password=password,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
    )

    return url.render_as_string(hide_password=False)


def get_database_url_sync() -> str:
    return build_db_url("postgresql+psycopg")


def get_database_url_async() -> str:
    return build_db_url("postgresql+psycopg_async")



# RAG / PGVECTOR

PG_VECTOR_COLLECTION = os.getenv(
    "PG_VECTOR_COLLECTION",
    "tutor_c",
).strip()

RAG_TOP_K = get_int_env(
    "RAG_TOP_K",
    "3",
)

if not PG_VECTOR_COLLECTION:
    raise RuntimeError(
        "PG_VECTOR_COLLECTION no puede estar vacío."
    )

if RAG_TOP_K <= 0:
    raise RuntimeError(
        "RAG_TOP_K debe ser mayor que cero."
    )



# OLLAMA

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://127.0.0.1:11434",
).strip()

OLLAMA_EMBEDDING_MODEL = os.getenv(
    "OLLAMA_EMBEDDING_MODEL",
    "nomic-embed-text",
).strip()

if not OLLAMA_BASE_URL:
    raise RuntimeError(
        "OLLAMA_BASE_URL no puede estar vacío."
    )

if not OLLAMA_EMBEDDING_MODEL:
    raise RuntimeError(
        "OLLAMA_EMBEDDING_MODEL no puede estar vacío."
    )
