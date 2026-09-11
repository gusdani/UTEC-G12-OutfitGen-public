# Integraciones externas opcionales

La demo pública no necesita esta carpeta para ejecutarse y no realiza llamadas de red.

La versión completa puede añadir adaptadores privados para:

- Azure OpenAI o un proveedor LLM compatible.
- PostgreSQL con pgvector.
- Un servicio de embeddings de texto e imagen.
- Modelos de clasificación descargados desde un almacenamiento autorizado.

Los adaptadores deben leer su configuración desde variables de entorno o un gestor de secretos. No guardes claves, contraseñas, endpoints internos ni datos de producción en este repositorio.

## Configuración sugerida

Usa `.env.example` como referencia local y define los valores reales únicamente en el entorno donde se ejecute la integración. La demo seguirá funcionando aunque ninguna de estas variables exista.
