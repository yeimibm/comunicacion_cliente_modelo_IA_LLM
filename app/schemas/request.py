from pydantic import BaseModel


class ExtractRequest(BaseModel):
    """
    Esquema de validación para la solicitud de extracción de información.
    
    Attributes:
        text: Texto a analizar
        domain: Dominio o contexto del texto (ej: "universidad", "empresa", etc.)
    """
    text: str
    domain: str
