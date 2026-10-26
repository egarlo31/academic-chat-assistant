import uuid
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

# Configuración de conexión al contenedor Docker
connection_string = "postgresql+psycopg://postgres:admin@localhost:5432/rag_db"
collection_name = "tutor_c"

print("1. Descargando documentación...")
url = "https://www.gnu.org/software/gnu-c-manual/gnu-c-manual.html"
loader = WebBaseLoader(url)
documentos = loader.load()

print("2. Aplicando chunking seguro para sintaxis C...")
# Mantenemos el particionador especializado en C++ para evitar cortar funciones
particionador = RecursiveCharacterTextSplitter.from_language(
    language=Language.CPP, 
    chunk_size=1000, 
    chunk_overlap=100
)
chunks = particionador.split_documents(documentos)

print("3. Inyectando metadatos estructurados...")
# El modelo Pydantic del equipo requiere estas llaves exactas
for doc in chunks:
    doc.metadata["chunk_id"] = str(uuid.uuid4())
    doc.metadata["title"] = "Manual de Referencia GNU C" 
    doc.metadata["source"] = url
    # LangChain por defecto guarda info extra como 'language', la dejamos intacta.

print(f"4. Vectorizando y guardando {len(chunks)} fragmentos en pgvector...")
embedder = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://172.21.192.1:11434"
)

# Reemplazo directo de Chroma.from_documents por PGVector.from_documents
db = PGVector.from_documents(
    embedding=embedder,
    documents=chunks,
    collection_name=collection_name,
    connection=connection_string,
    use_jsonb=True
)

print("✅ Ingesta completada con éxito en PostgreSQL.")