import os
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

# Configuración
CONNECTION_STRING = "postgresql+psycopg://postgres:admin@localhost:5432/rag_db"
COLLECTION_NAME = "tutor_c"
DATA_DIR = "./data"

print("1. Escaneando y cargando documentos locales desde ./data ...")

# Cargar todos los PDFs de la carpeta
pdf_loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
pdf_docs = pdf_loader.load()

# Cargar todos los HTMLs de la carpeta
html_loader = DirectoryLoader(DATA_DIR, glob="**/*.html", loader_cls=BSHTMLLoader)
html_docs = html_loader.load()

documentos = pdf_docs + html_docs
print(f"Total de documentos procesados: {len(documentos)}")

print("2. Aplicando chunking semántico...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documentos)
print(f"Total de fragmentos generados: {len(chunks)}")

print("3. Conectando a Ollama y PostgreSQL...")
embedder = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://127.0.0.1:11434"
)

print("4. Vectorizando y guardando en pgvector (esto puede tomar varios minutos)...")
db = PGVector.from_documents(
    documents=chunks,
    embedding=embedder,
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
    use_jsonb=True
)

print("✅ Ingesta masiva completada con éxito.")