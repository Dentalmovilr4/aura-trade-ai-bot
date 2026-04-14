import streamlit as st
import requests

st.title("💸 Aura Trade SaaS")

users = requests.get("http://localhost:5000/users").json()

st.write("### Usuarios conectados")
st.write(users)

st.write("### Añadir usuario")

name = st.text_input("Nombre")
key = st.text_input("API Key")
secret = st.text_input("API Secret")
balance = st.number_input("Balance")

if st.button("Agregar"):
    requests.post("http://localhost:5000/add_user", json={
        "name": name,
        "api_key": key,
        "api_secret": secret,
        "balance": balance
    })