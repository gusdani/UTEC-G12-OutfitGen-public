import streamlit as st

from coordination.coordinator import DemoCoordinator
from demo.catalog import CATALOG


st.set_page_config(page_title="OutfitGen Demo", page_icon="👗", layout="centered")

st.title("OutfitGen")
st.caption("Demo pública de un sistema de recomendación multiagente")
st.write("Escribe una consulta como `camisa azul` o `vestido rojo`.")

query = st.text_input("Consulta de moda", placeholder="Busco una camisa azul")

if query:
    result = DemoCoordinator(CATALOG).process_query(query)
    st.info(result["response"])
    if result["products"]:
        st.dataframe(result["products"], hide_index=True, use_container_width=True)

with st.expander("Flujo de agentes"):
    st.write("1. Analizador de consulta")
    st.write("2. Refinador de consulta")
    st.write("3. Filtro de recomendaciones sobre catálogo ficticio")