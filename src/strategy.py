from indicators import calculate_ema, calculate_rsi
import numpy as np

class Strategy:
    def __init__(self):
        self.data = {}
        self.model = None

    def analyze(self, df):
        if df is None or df.empty or 'close' not in df.columns:
            return None

        df['ema50'] = calculate_ema(df, 50)
        df['ema200'] = calculate_ema(df, 200)
        df['rsi'] = calculate_rsi(df)

        # 🔥 VOLATILIDAD
        df['returns'] = df['close'].pct_change()
        df['volatility'] = df['returns'].rolling(20).std()

        df = df.dropna()

        if len(df) < 50:
            return None

        return df.iloc[-1]

    def generate_signal(self, symbol):
        df = self.data.get(symbol)

        row = self.analyze(df)

        if row is None:
            return "HOLD"

        # 🔥 FILTRO DE MERCADO LATERAL
        if row['volatility'] < 0.001:
            return "HOLD"

        trend_up = row['ema50'] > row['ema200']
        trend_down = row['ema50'] < row['ema200']

        if trend_up and row['rsi'] < 40:
            return "BUY"

        if trend_down and row['rsi'] > 60:
            return "SELL"

        return "HOLD"