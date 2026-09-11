# UTEC-G12-OutfitGen-public

Versión pública y mínima del proyecto académico OutfitGen. Esta edición muestra la idea central de una arquitectura multiagente para recomendaciones de moda sin depender de credenciales, bases de datos, modelos propietarios ni servicios externos.

## Ejecutar la demo

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

La demo usa un catálogo ficticio incluido en `demo/catalog.py`. No contiene productos, usuarios, imágenes ni datos extraídos del sistema original. No realiza llamadas a APIs externas y no necesita claves para ejecutarse.

## Arquitectura

- `agents/analizador_consulta.py`: extrae categoría y color mediante reglas simples.
- `agents/refinador_consulta.py`: detecta información faltante.
- `coordination/coordinator.py`: coordina el flujo.
- `demo/catalog.py`: datos sintéticos para ejecutar la demo localmente.
- `integrations/README.md`: contrato y configuración esperada para servicios externos opcionales.
- `app.py`: interfaz Streamlit.

La versión completa del proyecto utiliza Azure OpenAI, PostgreSQL/pgvector, un servicio de embeddings y modelos de clasificación. Esas integraciones no se incluyen aquí: deben configurarse fuera de este repositorio y nunca deben añadirse claves reales a un commit. Esta separación es intencional para que el repositorio sea seguro, pequeño y reproducible.

## Demo frente a versión completa

| Modo | Servicios externos | Datos | Uso |
| --- | --- | --- | --- |
| Demo pública | Ninguno | Catálogo sintético | Ejecutar y revisar el flujo multiagente |
| Integración completa | APIs y base de datos configuradas por el usuario | Datos propios | Desarrollo o despliegue privado |

La demo representa el flujo de análisis, refinamiento y filtrado. No debe interpretarse como una copia autónoma de la infraestructura de producción.

## Tests

```powershell
pytest
```

## Alcance y licencia

Este repositorio es una demostración académica. Revisa y añade una licencia antes de redistribuirlo formalmente.