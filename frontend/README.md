# Academic Chat Assistant — Frontend

Interfaz web en React y Vite para el asistente académico especializado en lenguaje C.

## Requisitos

- Node.js 18 o superior
- npm
- Backend disponible en `http://localhost:8000`

## Instalación

Desde la raíz del proyecto:

```sh
cd frontend
npm install
```

## Desarrollo local

Con el backend activo en el puerto `8000`, ejecuta:

```sh
npm run dev
```

Abre `http://localhost:5173/`. Vite redirige `/api` y `/health` al backend automáticamente.

## Configuración opcional

Puedes copiar `.env.example` si necesitas apuntar el frontend a una API distinta:

```dotenv
VITE_API_BASE_URL=http://localhost:8000
```

Si se deja vacío, se usa el proxy local definido en `vite.config.js`.

## Compilación

Para generar una compilación de producción:

```sh
npm run build
```

Los archivos finales se crean en `dist/`, una carpeta ignorada por Git.

## Características

- Conversación enfocada en lenguaje C
- Renderizado de encabezados, listas, código inline y bloques de código
- Tablas de Markdown con desplazamiento horizontal
- Indicador de carga y manejo de errores
- Persistencia local del historial
- Copiado de respuestas al portapapeles
