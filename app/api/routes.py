from fastapi import APIRouter
from ..schemas.request import ExtractRequest
from ..schemas.response import ExtractResponse
from ..services.extract_service import extract_information


router = APIRouter()


@router.post("/extract", response_model=ExtractResponse)
def extract(data: ExtractRequest) -> ExtractResponse:
    """
    Endpoint para extracción de información estructurada del texto.
    
    Este endpoint recibe texto y un dominio, lo procesa con LLM,
    y devuelve información estructurada en formato JSON validado.
    
    Args:
        data: ExtractRequest con "text" y "domain"
    
    Returns:
        ExtractResponse: Información estructurada extraída
    
    Ejemplo:
        POST /extract
        {
            "text": "La universidad tendrá una reunión el 10 de abril",
            "domain": "universidad"
        }
    """
    
    result = extract_information(
        text=data.text,
        domain=data.domain
    )
    
    return result
