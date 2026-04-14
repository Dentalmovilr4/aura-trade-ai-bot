import streamlit as st
import requests

st.set_page_config(page_title="Aura Admin", layout="wide")
st.title("🏢 Panel de Control - Aura Trade AI")

try:
    users = requests.get("http://localhost:5000/users").json()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes Totales", len(users))
    col2.metric("Ingresos (MRR)", f"${len(users) * 29}")
    col3.metric("Estado del Bot", "🟢 Activo")

    st.write("### Base de Datos de Clientes")
    st.dataframe(users, use_container_width=True)

except Exception as e:
    st.error(f"No se pudo conectar con la API. ¿Está app.py corriendo? Error: {e}")
