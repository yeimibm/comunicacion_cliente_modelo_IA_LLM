from fastapi import FastAPI

from dotenv import load_dotenv
from .api.routes import router

# Cargar variables de entorno desde .env
load_dotenv()

# Crear aplicación FastAPI
app = FastAPI(
    title="Text Information Extraction API",
    description="API para extracción de información estructurada usando LLMs",
    version="1.0.0"
)



# Registrar el router con los endpoints
app.include_router(router)


@app.get("/")
def root():
    """Endpoint raíz que devuelve información de la API."""
    return {
        "name": "Text Information Extraction API",
        "version": "1.0.0",
        "description": "API para extracción de información estructurada de textos usando LLMs",
        "endpoints": {
            "extract": "POST /extract - Extrae información estructurada de un texto"
        }
    }


@app.get("/health")
def health_check():
    """Endpoint para verificar que la API está activa."""
    return {
        "status": "healthy",
        "service": "text-extraction-api"
    }
