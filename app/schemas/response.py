from pydantic import BaseModel, Field
from typing import List, Literal


class Entity(BaseModel):
    """
    Representa una entidad encontrada en el texto.
    
    Attributes:
        name: Nombre o valor de la entidad
        type: Tipo de entidad (PERSON, ORG, DATE, LOCATION, OTHER)
    """
    name: str
    type: Literal["PERSON", "ORG", "DATE", "LOCATION", "OTHER"]


class ExtractResponse(BaseModel):
    """
    Esquema de respuesta con información estructurada extraída del texto.
    
    Attributes:
        summary: Resumen del contenido (máximo 500 caracteres)
        entities: Lista de entidades encontradas
        actions: Lista de acciones o tareas mencionadas
        confidence: Nivel de confianza en la extracción (0-1)
        needs_clarification: Indica si el texto necesita aclaraciones
        clarifying_questions: Preguntas para aclarar información faltante
    """
    summary: str = Field(..., max_length=500)
    entities: List[Entity]
    actions: List[str]
    confidence: float = Field(..., ge=0, le=1)
    needs_clarification: bool
    clarifying_questions: List[str]
