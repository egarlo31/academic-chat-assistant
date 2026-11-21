from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("1. Descargando página de GNU C...")
url = "https://www.gnu.org/software/gnu-c-manual/gnu-c-manual.html"
loader = WebBaseLoader(url)
documentos = loader.load()

print(f"Texto extraído: {len(documentos[0].page_content)} caracteres en total.")

print("\n2. Aplicando Chunking...")
# Cortamos en fragmentos de 1000 caracteres, con 100 de solapamiento
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(documentos)

print(f"Se generaron {len(chunks)} fragmentos.")
print("\n--- PREVISIÓN DEL PRIMER FRAGMENTO ---")
print(chunks[0].page_content)