import streamlit as st

from coordination.coordinator import DemoCoordinator
from demo.catalog import CATALOG


st.set_page_config(page_title="OutfitGen Demo", page_icon="👗", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --outfit-primary: #1E88E5;
        --outfit-secondary: #3B82F6;
        --outfit-accent: #1E3A8A;
        --outfit-muted: #64748B;
    }

    .stApp {
        background: #FFFFFF;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3 {
        color: var(--outfit-accent);
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid #E2E8F0;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        padding-bottom: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background: #F0F2F6;
        border: 2px solid transparent;
        border-radius: 8px;
        color: #262730;
        font-size: 15px;
        font-weight: 600;
        padding: 0 18px;
        white-space: nowrap;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: #E0E4E8;
        border-color: var(--outfit-primary);
    }

    .stTabs [aria-selected="true"] {
        background: var(--outfit-primary) !important;
        border-color: var(--outfit-primary) !important;
        box-shadow: 0 2px 8px rgba(30, 136, 229, 0.3);
        color: white !important;
    }

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #CBD5E1;
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: var(--outfit-primary);
        color: var(--outfit-primary);
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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
    tab_catboost, tab_agents, tab_embeddings, tab_reports, tab_config, tab_architecture, tab_about = st.tabs(
        [
            "🧠 CatBoost",
            "🤖 Agentes",
            "🎯 Embeddings",
            "📊 Reportes",
            "⚙️ Configuración LLM",
            "🧩 Arquitectura",
            "ℹ️ Acerca de",
        ]
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

    with tab_reports:
        st.subheader("Reportes de la demo")
        st.caption("Métricas ilustrativas del catálogo sintético, no datos de usuarios ni producción.")
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Productos disponibles", len(CATALOG))
        metric_col2.metric("Categorías", len({product["category"] for product in CATALOG}))
        metric_col3.metric("Consultas externas", "0")
        st.write("**Distribución del catálogo")
        category_counts = {}
        for product in CATALOG:
            category_counts[product["category"]] = category_counts.get(product["category"], 0) + 1
        st.bar_chart(category_counts, horizontal=True)
        st.info("La versión completa puede alimentar esta sección con métricas persistidas en PostgreSQL.")

    with tab_config:
        st.subheader("Configuración de agentes LLM")
        st.caption("Plantillas de referencia. La demo no llama a un LLM ni guarda cambios.")
        prompts = {
            "AnalizadorConsulta": "Extrae categoría, color y ocasión de la consulta del usuario.",
            "EspecialistaOutfits": "Propón una combinación coherente con las prendas recuperadas.",
            "PresentadorResultados": "Explica las recomendaciones de forma clara y breve.",
        }
        selected_agent = st.selectbox("Agente", list(prompts))
        st.text_area("Prompt de ejemplo", value=prompts[selected_agent], height=120, disabled=True)
        st.checkbox("Activo en modo completo", value=True, disabled=True)
        st.warning("Las claves, temperaturas y prompts productivos se configuran fuera de este repositorio.")

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

def _reference_banner(message="Vista de referencia · no funcional en este demo"):
    st.warning(f"⚠️ {message}")


def _render_sidebar(result=None, page="Chat"):
    with st.sidebar:
        st.markdown("<div class='sidebar-brand'>OutfitGen</div>", unsafe_allow_html=True)
        st.markdown("### ¡Hola, Demo!")
        st.divider()
        navigation = [
            "Chat",
            "Reportes",
            "Perfil",
            "Configuración LLM",
            "Arquitectura",
            "Acerca de",
            "Login (referencia)",
            "Registro (referencia)",
        ]
        selected = st.radio("Navegación", navigation, index=navigation.index(page), key="main_navigation")

        if selected == "Chat":
            st.divider()
            search_mode = st.selectbox(
                "🔍 Modo de Búsqueda",
                ["Automático", "Texto", "Imagen", "Híbrido"],
                help="Control visual heredado del proyecto madre; la demo ejecuta búsquedas de texto sintéticas.",
            )
            st.session_state["search_mode"] = search_mode

            with st.expander("⚙️ Configuración", expanded=False):
                st.checkbox("🧠 LLM Activado", value=True, disabled=True)
                st.checkbox("Usar LLM para describir imagen", value=True, disabled=True)
                st.caption("No se realizan llamadas al LLM en esta versión.")
                st.button("🗑️ Limpiar Historial", disabled=True, use_container_width=True)

            with st.expander("🎯 Análisis ML - CatBoost", expanded=False):
                if result and result.get("analysis", {}).get("category"):
                    prediction = _catboost_demo(result)
                    st.markdown(f"**📦 Categoría:** {prediction['category'].title()}")
                    st.progress(prediction["category_confidence"])
                    st.caption(f"Confianza: {prediction['category_confidence']:.1%}")
                    st.markdown(f"**👤 Género:** {prediction['gender'].title()}")
                    st.progress(prediction["gender_confidence"])
                else:
                    st.info("Haz una consulta para ver las predicciones ML")
                    st.caption("📦 Categoría · 👤 Género · 🎯 Confianza")

            with st.expander("🔄 Ciclo de Vida - Agentes", expanded=False):
                st.markdown("**Procesamiento de la última consulta**")
                for step in ["🧠 Analizador de consulta", "🔧 Refinador", "🤖 Clasificador CatBoost", "🔍 Buscador de embeddings", "📋 Presentador"]:
                    st.write(step)
                st.caption("Los agentes marcados como integración no se ejecutan en el demo.")

            with st.expander("🎯 Colores de Similitud", expanded=False):
                st.write("🟢 Excelente (>80%)")
                st.write("🟡 Buena (>60%)")
                st.write("🔴 Regular (<60%)")

        st.divider()
        st.caption("Modo actual")
        st.success("Demo local")
        st.caption("Sin base de datos, modelos privados ni APIs externas.")
        if selected != page:
            st.query_params["page"] = selected.lower().replace(" ", "-")
            st.rerun()
    return selected


def _render_product_grid(products):
    if not products:
        return
    st.markdown("### Resultados de búsqueda")
    columns = st.columns(min(5, len(products)))
    for column, product in zip(columns, products):
        with column:
            st.markdown(
                f"<div class='product-card'><h4>{product['name']}</h4>"
                f"<div class='product-placeholder'>{product['category'].title()}</div>"
                f"<p><b>📝 Texto:</b> 86% 🟢<br><b>🖼️ Imagen:</b> 72% 🟡</p></div>",
                unsafe_allow_html=True,
            )
            with st.expander("📝 Ver detalles"):
                st.write(f"**Categoría:** {product['category'].title()}")
                st.write(f"**Color:** {product['color'].title()}")
                st.write(f"**Ocasión:** {product['occasion'].title()}")


def _render_chat():
    st.title("OutfitGen")
    st.caption("Chat de recomendaciones · vista pública basada en el frontend del proyecto madre")
    st.caption("Escribí una consulta o adjuntá una imagen para explorar la interfaz multimodal.")
    prompt = st.chat_input(
        "Describí la prenda que buscás o adjuntá una imagen...",
        accept_file="multiple",
        file_type=["jpg", "jpeg", "png", "webp"],
    )
    if prompt:
        query = prompt.text if hasattr(prompt, "text") else (prompt if isinstance(prompt, str) else "")
        if getattr(prompt, "files", []):
            st.info("La carga de imágenes está representada visualmente; el análisis de imagen no forma parte de este demo.")
    else:
        query = st.session_state.get("chat_query", "")
    st.session_state["chat_query"] = query
    result = DemoCoordinator(CATALOG).process_query(query) if query else {
        "user_input": "", "analysis": {}, "refinement": {"needs_clarification": False},
        "response": "Escribe una consulta para comenzar.", "products": [],
    }
    st.info(result["response"])
    _render_product_grid(result["products"])
    with st.expander("Flujo de agentes", expanded=False):
        st.write("1. Analizador de consulta → 2. Refinador → 3. Filtro de recomendaciones")
    _show_explanation_tabs(result)
    return result


def _render_reports():
    st.title("Reportes de Consultas")
    _reference_banner("Los datos de usuarios, consultas y costos no se incluyen en este demo")
    st.markdown("### Indicadores Clave de Performance")
    cols = st.columns(4)
    for col, label, value in zip(cols, ["Total Mensajes", "Conversaciones", "Usuarios Activos", "Tiempo Respuesta"], ["1,284", "346", "72", "0.84s"]):
        col.metric(label, value)
    st.markdown("### Análisis y Tendencias")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Actividad por Día")
        st.line_chart({"Consultas": [12, 18, 16, 27, 24, 31, 29]})
    with right:
        st.markdown("#### Distribución de Búsquedas")
        st.bar_chart({"Texto": 62, "Imagen": 18, "Híbrida": 20})
    st.markdown("### Costos y Uso de LLM")
    cost_left, cost_right = st.columns(2)
    cost_left.metric("Costo estimado", "No disponible")
    cost_right.metric("Tokens procesados", "No disponible")
    st.caption("Esta composición replica los paneles del proyecto madre con valores ilustrativos.")


def _render_profile():
    st.title("Mi Perfil")
    _reference_banner()
    left, right = st.columns([1, 2])
    with left:
        st.markdown("<div class='avatar-placeholder'>D</div>", unsafe_allow_html=True)
        st.caption("Foto de perfil")
    with right:
        form_left, form_mid, form_right = st.columns(3)
        with form_left:
            st.text_input("Nombre", value="Demo", disabled=True)
            st.text_input("Apellido", value="Usuario", disabled=True)
            st.text_input("Usuario", value="demo_usuario", disabled=True)
        with form_mid:
            st.text_input("Nueva contraseña", type="password", disabled=True)
            st.text_input("Confirmar", type="password", disabled=True)
        with form_right:
            st.file_uploader("Cambiar foto", disabled=True)
            st.button("Guardar", disabled=True, use_container_width=True)


def _render_llm_config():
    st.title("Configuración de Agentes LLM")
    _reference_banner("Los prompts y la temperatura se gestionan en la base de datos de la versión completa")
    tab_prompts, tab_temperature = st.tabs(["📝 Prompts de Agentes", "🌡️ Temperatura LLM"])
    with tab_prompts:
        agents = {"Coordinador": "Orquesta el flujo multiagente.", "AnalizadorConsulta": "Extrae señales de la consulta.", "PresentadorResultados": "Comunica las recomendaciones."}
        selected = st.selectbox("Agente", list(agents))
        st.text_area("Contenido del Prompt", value=agents[selected], height=180, disabled=True)
        st.checkbox("Activo", value=True, disabled=True)
        st.button("Editar", disabled=True)
    with tab_temperature:
        st.slider("Temperatura", 0.0, 1.0, 0.2, disabled=True)
        st.caption("No se guardan cambios en el demo público.")


def _render_architecture():
    st.title("Arquitectura del Sistema")
    _reference_banner("El diagrama es una representación pública; los servicios privados no están conectados")
    tab_diagram, tab_docs = st.tabs(["Diagrama", "Documentación"])
    with tab_diagram:
        st.markdown("### Flujo multiagente")
        st.code("Entrada texto / imagen\n        ↓\nCoordinador inteligente\n  ↙    ↓    ↘\nAnalizador  CatBoost  Embeddings\n        ↓\nPresentador de resultados", language="text")
    with tab_docs:
        st.markdown("La versión completa integra Azure OpenAI, PostgreSQL/pgvector, CatBoost y OpenFashionCLIP. Esta edición conserva la arquitectura conceptual sin incluir infraestructura ni datos privados.")


def _render_about():
    st.title("Acerca de StyleDesigner")
    st.markdown("### Sistema Multi-Agente de Recomendación de Moda")
    st.write("Versión pública demostrativa del proyecto académico UTEC · Grupo 12")
    st.markdown("**Características representadas:** búsqueda por texto e imagen, clasificación CatBoost, similitud semántica, prompts de agentes y navegación Streamlit.")
    st.markdown("**Agentes del sistema:** Coordinador, Analizador de Consulta, Especialista en Outfits, Clasificador CatBoost, Refinador, Buscador de Embeddings, Presentador y Analizador de Imágenes.")
    _reference_banner("Las integraciones reales y los datos de producción no forman parte de este demo")


def _render_auth_reference(register=False):
    st.title("Registrarme" if register else "Iniciar sesión")
    _reference_banner("Pantalla visual de referencia · no funcional en este demo")
    left, right = st.columns([1.3, 1])
    with left:
        st.markdown("<div class='brand-placeholder'>OutfitGen</div>", unsafe_allow_html=True)
        st.caption("UTEC · Grupo 12")
    with right:
        st.markdown(f"### {'Crear cuenta' if register else 'Iniciar sesión'}")
        if register:
            st.text_input("Nombre", disabled=True)
            st.text_input("Apellido", disabled=True)
        st.text_input("Usuario", disabled=True)
        st.text_input("Contraseña", type="password", disabled=True)
        st.button("Crear cuenta" if register else "Iniciar sesión", disabled=True, use_container_width=True)
        st.button("Volver", disabled=True, use_container_width=True)


st.markdown("<style>.sidebar-brand{background:#1E88E5;border-radius:8px;color:white;font-size:25px;font-weight:700;padding:12px;text-align:center;margin-bottom:16px}.product-card{border:1px solid #e0e0e0;border-radius:12px;padding:1rem;min-height:250px;box-shadow:0 2px 4px rgba(0,0,0,.05);background:white}.product-card h4{text-align:center;min-height:42px}.product-placeholder{height:120px;background:#E3F2FD;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#1E88E5;font-weight:700;margin-bottom:12px}.avatar-placeholder{width:120px;height:120px;border-radius:50%;background:#f0f2f6;border:3px solid #e0e0e0;display:flex;align-items:center;justify-content:center;font-size:42px;color:#1E88E5;margin:20px auto}.brand-placeholder{height:220px;display:flex;align-items:center;justify-content:center;background:#E3F2FD;border-radius:20px;color:#1E88E5;font-size:42px;font-weight:700;margin-top:60px}</style>", unsafe_allow_html=True)

page = st.query_params.get("page", "chat").replace("-", " ").title()
page_aliases = {"Login (Referencia)": "Login (referencia)", "Registro (Referencia)": "Registro (referencia)", "Configuración Llm": "Configuración LLM"}
page = page_aliases.get(page, page)
result_for_sidebar = st.session_state.get("last_demo_result")
selected_page = _render_sidebar(result_for_sidebar, page if page in ["Chat", "Reportes", "Perfil", "Configuración LLM", "Arquitectura", "Acerca de", "Login (referencia)", "Registro (referencia)"] else "Chat")

if selected_page == "Chat":
    result_for_sidebar = _render_chat()
    st.session_state["last_demo_result"] = result_for_sidebar
elif selected_page == "Reportes":
    _render_reports()
elif selected_page == "Perfil":
    _render_profile()
elif selected_page == "Configuración LLM":
    _render_llm_config()
elif selected_page == "Arquitectura":
    _render_architecture()
elif selected_page == "Acerca de":
    _render_about()
elif selected_page == "Login (referencia)":
    _render_auth_reference()
else:
    _render_auth_reference(register=True)