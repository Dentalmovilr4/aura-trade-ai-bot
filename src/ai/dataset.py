import pandas as pd
from indicators import calculate_ema, calculate_rsi

class DatasetBuilder:
    def build(self, df):
        df['ema50'] = calculate_ema(df, 50)
        df['ema200'] = calculate_ema(df, 200)
        df['rsi'] = calculate_rsi(df)

        df = df.dropna()

        X = df[['close','ema50','ema200','rsi']].values
        y = (df['close'].shift(-1) > df['close']).astype(int).values

        return X[:-1], y[:-1]