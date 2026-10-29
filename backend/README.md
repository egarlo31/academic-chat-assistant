## Configuración del Backend y API de Groq

1. Crea un entorno virtual: `python -m venv venv`
2. Actívalo: `.\venv\Scripts\Activate.ps1` (Windows)
3. Instala dependencias: `pip install -r backend/requirements.txt`
4. Copia `backend/.env.example` a `backend/.env` y coloca tu propia `GROQ_API_KEY`.
5. Prueba la conexión: `python backend/scripts/test_connection.py`
6. Levanta el servidor: `cd backend` y luego `uvicorn main:app --reload`