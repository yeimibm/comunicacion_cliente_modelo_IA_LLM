# Text Information Extraction API

API de microservicio en Python para extracción de información estructurada de textos usando LLMs (Large Language Models) con FastAPI, LangChain y Anthropic Claude.

## 🎯 Descripción del Proyecto

Esta API recibe un texto y dominio específico, utiliza un modelo de IA (OpenAI) para analizar el contenido y devuelve información estructurada en formato JSON validado, incluyendo:

- **Resumen**: Síntesis del contenido (máximo 60 palabras)
- **Entidades**: Personas, organizaciones, fechas, ubicaciones extraídas
- **Acciones**: Tareas o actividades mencionadas
- **Confianza**: Nivel de certeza en la extracción (0-1)
- **Aclaraciones**: Preguntas si el texto es ambiguo




## 📐 Arquitectura del Sistema

```mermaid
graph TD
    A[Cliente HTTP] -->|POST /extract| B[FastAPI Router]
    B -->|Valida con Pydantic| C[ExtractRequest]
    C -->|Llama| D[Extract Service]
    D -->|Construye| E[ChatPromptTemplate]
    D -->|Inicializa| F[ChatOpenAI<br/>temperature=0]
    E -->|Crea cadena| G[Prompt | LLM | Parser]
    F -->|Procesa| G
    G -->|Valida JSON| H[PydanticOutputParser]
    H -->|Retorna| I[ExtractResponse]
    I -->|JSON validado| A
```



