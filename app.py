import streamlit as st

from coordination.coordinator import DemoCoordinator
from demo.catalog import CATALOG


st.set_page_config(page_title="OutfitGen Demo", page_icon="👗", layout="wide")


def _catboost_demo(result):
    """Build an educational CatBoost view without loading a private model."""
    analysis = result.get("analysis", {})
    category = analysis.get("category") or "sin categoría"
    category_confidence = 0.96 if analysis.get("category") else 0.18
    gender = "unisex"
    gender_confidence = 0.84 if analysis.get("category") else 0.51
    return {
        "category": category,
        "category_confidence": category_confidence,
        "gender": gender,
        "gender_confidence": gender_confidence,
        "features": {
            "categoría detectada": category_confidence,
            "color detectado": 0.78 if analysis.get("color") else 0.24,
            "longitud de consulta": 0.62,
            "señales visuales": 0.00,
        },
    }


def _show_explanation_tabs(result):
    tab_catboost, tab_agents, tab_embeddings, tab_architecture, tab_about = st.tabs(
        ["🧠 CatBoost", "🤖 Agentes", "🎯 Embeddings", "🧩 Arquitectura", "ℹ️ Acerca de"]
    )

    with tab_catboost:
        st.subheader("Clasificación de atributos")
        st.caption("Vista educativa. El modelo CatBoost real no está incluido en este repositorio público.")
        prediction = _catboost_demo(result)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Categoría", prediction["category"].title(), f"{prediction['category_confidence']:.0%}")
            st.metric("Género estimado", prediction["gender"].title(), f"{prediction['gender_confidence']:.0%}")
        with col2:
            st.write("**Señales de entrada ilustrativas**")
            st.bar_chart(prediction["features"], horizontal=True)
        st.info("En la versión completa, CatBoost clasifica atributos a partir de características de productos y modelos entrenados. Aquí se muestra el lugar que ocupa dentro del flujo.")

    with tab_agents:
        st.subheader("Agentes que intervienen")
        agents = [
            ("1", "Analizador de consulta", "Detecta categoría y color en el texto."),
            ("2", "Refinador de consulta", "Indica qué dato falta para continuar."),
            ("3", "Clasificador CatBoost", "En producción clasifica atributos del producto."),
            ("4", "Buscador de embeddings", "En producción recupera elementos semánticamente similares."),
            ("5", "Presentador de resultados", "Ordena y comunica las recomendaciones."),
        ]
        for number, name, description in agents:
            st.markdown(f"**{number}. {name}**  ")
            st.caption(description)
        st.success("En esta demo están activos el analizador, el refinador y el filtro sobre el catálogo sintético.")

    with tab_embeddings:
        st.subheader("Búsqueda semántica")
        st.caption("La búsqueda vectorial real requiere un modelo de embeddings y una base pgvector.")
        st.write("La versión completa representa consultas y productos como vectores para encontrar coincidencias de significado, no solo coincidencias exactas de palabras.")
        st.code("consulta -> embedding -> similitud -> ranking de productos", language="text")
        st.dataframe(
            [
                {"etapa": "Entrada", "ejemplo": result.get("user_input", "camisa azul")},
                {"etapa": "Modo público", "valor": "Filtro sintético por categoría/color"},
                {"etapa": "Modo completo", "valor": "API de embeddings + pgvector"},
            ],
            hide_index=True,
            use_container_width=True,
        )

    with tab_architecture:
        st.subheader("Flujo de la aplicación")
        st.code(
            "Consulta del usuario\n"
            "      ↓\n"
            "Analizador de consulta\n"
            "      ↓\n"
            "Refinador\n"
            "      ↓\n"
            "CatBoost + embeddings (opcionales en demo)\n"
            "      ↓\n"
            "Recomendaciones",
            language="text",
        )
        st.write("La demo conserva el recorrido conceptual del sistema original, pero reemplaza infraestructura privada por componentes locales y reproducibles.")

    with tab_about:
        st.subheader("OutfitGen")
        st.write("Demostración académica de una arquitectura multiagente aplicada a recomendaciones de moda.")
        st.markdown(
            "- **Demo pública:** funciona sin credenciales, base de datos ni APIs.\n"
            "- **Versión completa:** incorpora LLM, CatBoost, embeddings y PostgreSQL/pgvector.\n"
            "- **Datos:** el catálogo de esta versión es completamente sintético."
        )

st.title("OutfitGen · Demo pública")
st.caption("Sistema multiagente de recomendación de moda, ejecutable sin servicios externos")

with st.sidebar:
    st.header("Consulta")
    st.write("Prueba el flujo con el catálogo sintético incluido.")
    query = st.text_input("¿Qué estás buscando?", placeholder="Busco una camisa azul")
    st.divider()
    st.caption("Modo actual")
    st.success("Demo local")
    st.caption("CatBoost, embeddings y APIs reales se documentan como integraciones opcionales.")

result = DemoCoordinator(CATALOG).process_query(query) if query else {
    "user_input": "",
    "analysis": {},
    "refinement": {"needs_clarification": False},
    "response": "Escribe una consulta para comenzar.",
    "products": [],
}

st.info(result["response"])
if result["products"]:
    st.subheader("Recomendaciones")
    st.dataframe(result["products"], hide_index=True, use_container_width=True)

_show_explanation_tabs(result)