import pandas as pd

def calculate_ema(data, period=50):
    return data['close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))