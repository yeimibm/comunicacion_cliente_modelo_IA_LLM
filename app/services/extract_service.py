import os
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from ..schemas.response import ExtractResponse


def extract_information(text: str, domain: str) -> ExtractResponse:
    """
    Servicio principal para extracción de información usando LLM.
    
    Flujo:
    1. Obtiene el prompt y parser de LangChain
    2. Inicializa el modelo ChatAnthropic con temperature=0
    3. Construye la cadena: prompt → modelo → parser
    4. Invoca el LLM con el texto y dominio proporcionados
    5. Retorna la respuesta validada con Pydantic
    
    Args:
        text: Texto a analizar
        domain: Dominio o contexto (ej: "universidad")
    
    Returns:
        ExtractResponse: Respuesta estructurada validada
    
    Raises:
        ValueError: Si ANTHROPIC_API_KEY no está configurada
    """
    
    # Verificar que la clave de API esté configurada
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("ANTHROPIC_API_KEY no está configurada en las variables de entorno")
    
    # Crear el parser de Pydantic
    parser = PydanticOutputParser(pydantic_object=ExtractResponse)
    format_instructions = parser.get_format_instructions()
    
    # Crear la plantilla del prompt
    prompt_template = ChatPromptTemplate.from_template(
        """Eres un experto en procesamiento de lenguaje natural y extracción de información.
        
Tu tarea es analizar el siguiente texto en el dominio de "{domain}" y extraer información estructurada.

TEXTO A ANALIZAR:
"{text}"

INSTRUCCIONES DETALLADAS:

1. RESUMEN: Genera un resumen conciso (máximo 60 palabras) que capture la esencia del texto.

2. ENTIDADES: Identifica y extrae todas las entidades presentes:
   - PERSON: Nombres de personas
   - ORG: Organizaciones, empresas, instituciones
   - DATE: Fechas específicas o períodos
   - LOCATION: Lugares geográficos
   - OTHER: Cualquier otra entidad relevante

3. ACCIONES: Lista las acciones, tareas o actividades explícitamente mencionadas o claramente implicadas.

4. CONFIANZA (0-1): Asigna un nivel de confianza basado en:
   - 0.9-1.0: Información muy clara, específica y completa
   - 0.7-0.89: Información clara pero con detalles menores que podrían mejorarse
   - 0.5-0.69: Información parcial o con cierta ambigüedad
   - 0.0-0.49: Información muy vaga o incompleta

5. ACLARACIONES NECESARIAS: Determina si necesita clarificación SOLO en estos casos:
   ✓ SI needs_clarification = true CUANDO:
     - Información crítica está completamente ausente (ej: fecha sin hour cuando es importante)
     - El propósito principal es completamente ambiguo
     - Datos esenciales para la acción están faltando
     - El contexto es confuso o contradictorio
   
   ✗ NO needs_clarification = false CUANDO:
     - El texto es claro y específico aunque tenga detalles menores
     - El propósito puede inferirse del contexto
     - La información es suficiente para actuar
     - Los detalles menores no afectan la comprensión

6. PREGUNTAS CLARIFICADORAS: Solo genera si needs_clarification = true
   - Máximo 3 preguntas específicas y útiles
   - Si needs_clarification = false, dejar como lista vacía []

REGLAS IMPORTANTES:
- NO inventes información que no esté en el texto
- Sé preciso y conservador en el análisis
- La presencia de todos los detalles hace que needs_clarification = false
- Si puedes realizar la acción con la información dada, no necesita clarificación

{format_instructions}

Responde SOLO en formato JSON válido según el esquema especificado, sin ningún texto adicional."""
    )
    
    # Inicializar el modelo LLM con temperature=0 para reducir alucinaciones
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0,
        max_tokens=1024
    )
    
    # Construir la cadena: prompt → LLM → parser
    chain = prompt_template | llm | parser
    
    # Invocar la cadena con los parámetros (incluir format_instructions)
    response = chain.invoke({
        "text": text,
        "domain": domain,
        "format_instructions": format_instructions
    })
    
    return response
