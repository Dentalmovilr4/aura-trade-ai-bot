import pandas as pd
import numpy as np

def calculate_ema(data, period=50):
    return data['close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_adx(df, period=14):
    df['high'] = df[2].astype(float)
    df['low'] = df[3].astype(float)

    plus_dm = df['high'].diff()
    minus_dm = df['low'].diff()

    plus_dm = np.where((plus_dm > minus_dm) & (plus_dm > 0), plus_dm, 0)
    minus_dm = np.where((minus_dm > plus_dm) & (minus_dm > 0), minus_dm, 0)

    tr1 = df['high'] - df['low']
    tr2 = abs(df['high'] - df['close'].shift())
    tr3 = abs(df['low'] - df['close'].shift())

    tr = np.maximum.reduce([tr1, tr2, tr3])
    atr = pd.Series(tr).rolling(period).mean()

    plus_di = 100 * (pd.Series(plus_dm).rolling(period).mean() / atr)
    minus_di = 100 * (pd.Series(minus_dm).rolling(period).mean() / atr)

    dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100
    adx = dx.rolling(period).mean()

    return adx