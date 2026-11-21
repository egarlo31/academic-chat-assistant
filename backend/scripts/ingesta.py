import logging
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

from app.config.settings import (
    get_database_url_sync,
    PG_VECTOR_COLLECTION,
    OLLAMA_BASE_URL,
    OLLAMA_EMBEDDING_MODEL
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# CONFIGURACIÓN

CONNECTION_STRING = get_database_url_sync()
COLLECTION_NAME = PG_VECTOR_COLLECTION

# Ruta absoluta a la carpeta data en la raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

logger.info(f"1. Escaneando y cargando documentos locales desde {DATA_DIR} ...")

# Cargar todos los PDFs de la carpeta
pdf_loader = DirectoryLoader(str(DATA_DIR), glob="**/*.pdf", loader_cls=PyPDFLoader)
pdf_docs = pdf_loader.load()

# Cargar todos los HTMLs de la carpeta
html_loader = DirectoryLoader(str(DATA_DIR), glob="**/*.html", loader_cls=BSHTMLLoader)
html_docs = html_loader.load()

documentos = pdf_docs + html_docs
logger.info(f"Total de documentos procesados: {len(documentos)}")

logger.info("2. Aplicando chunking semántico...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documentos)
logger.info(f"Total de fragmentos generados: {len(chunks)}")

logger.info("3. Conectando a Ollama y PostgreSQL...")
embedder = OllamaEmbeddings(
    model=OLLAMA_EMBEDDING_MODEL,
    base_url=OLLAMA_BASE_URL
)

logger.info("4. Vectorizando y guardando en pgvector (esto puede tomar varios minutos)...")
db = PGVector.from_documents(
    documents=chunks,
    embedding=embedder,
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
    use_jsonb=True
)

logger.info("Ingesta masiva completada con éxito.")