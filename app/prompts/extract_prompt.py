from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from ..schemas.response import ExtractResponse


def get_extract_prompt():
    """
    Construye la plantilla de prompt para extracción de información.
    
    Retorna:
        tuple: (ChatPromptTemplate, PydanticOutputParser)
    """
    
    # Parser que valida la salida según el esquema ExtractResponse
    parser = PydanticOutputParser(pydantic_object=ExtractResponse)
    
    # Obtener las instrucciones de formato del parser
    format_instructions = parser.get_format_instructions()
    
    # Crear la plantilla del prompt
    prompt_template = ChatPromptTemplate.from_template(
        """Eres un experto en procesamiento de lenguaje natural y extracción de información.
        
Tu tarea es analizar el siguiente texto en el dominio de "{domain}" y extraer información estructurada.

TEXTO A ANALIZAR:
"{text}"

INSTRUCCIONES:
1. Genera un resumen conciso del texto (máximo 60 palabras).
2. Identifica todas las entidades (personas, organizaciones, fechas, ubicaciones).
3. Extrae acciones o tareas mencionadas.
4. Asigna un nivel de confianza (0-1) basado en la claridad del texto.
5. Si el texto carece de información importante:
   - Establece needs_clarification = true
   - Genera al menos 2 preguntas clarificadoras
6. Si el texto es claro:
   - Establece needs_clarification = false
   - Deja clarifying_questions vacío

IMPORTANTE:
- NO inventes información que no esté en el texto.
- Sé conservador con el nivel de confianza.
- Las preguntas clarificadoras deben ser específicas y útiles.

{format_instructions}

Responde en formato JSON válido según el esquema especificado."""
    )
    
    return prompt_template, parser
