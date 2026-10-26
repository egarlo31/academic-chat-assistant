import asyncio
from retriever import PostgresRetriever

async def simular_peticion_backend():
    print("Iniciando conexión con el Retriever de PostgreSQL...\n")
    motor = PostgresRetriever()
    
    consulta = "¿Cuáles son los tipos de datos básicos en C?"
    print(f"Pregunta simulada del alumno: '{consulta}'\n")
    
    # El ChatService ejecuta tu método asíncrono
    chunks = await motor.retrieve(consulta, limit=3)
    
    if not chunks:
        print("No se encontraron resultados (Lista vacía devuelta correctamente).")
        return
        
    print(f"Éxito: Se retornaron {len(chunks)} objetos validados por el contrato Pydantic.\n")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"--- Chunk {i} (Score: {chunk.score}) ---")
        print(f"ID Único: {chunk.chunk_id}")
        print(f"Fuente:   {chunk.title} | {chunk.source_url}")
        print(f"Texto:    {chunk.text[:150]}...\n")

if __name__ == "__main__":
    asyncio.run(simular_peticion_backend())