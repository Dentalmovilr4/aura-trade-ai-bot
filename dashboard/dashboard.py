import streamlit as st
import sys
import os

# 🔥 Agregar src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from database import Database

db = Database()

st.title("📊 Aura Trade AI Bot")

trades = db.get_all()

st.write("### Historial de Trades")
st.write(trades)

st.write(f"Total trades: {len(trades)}")