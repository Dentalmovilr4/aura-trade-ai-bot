import streamlit as st
from src.data_loader import DataLoader
from src.indicators import calculate_ema, calculate_rsi

st.title("Aura Trade AI Bot")

loader = DataLoader()
data = loader.get_data()

data['ema'] = calculate_ema(data)
data['rsi'] = calculate_rsi(data)

st.line_chart(data[['close','ema']])
st.line_chart(data['rsi'])