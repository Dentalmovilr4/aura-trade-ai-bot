from indicators import calculate_ema, calculate_rsi, calculate_adx

class Strategy:
    def __init__(self):
        self.data = {}

    def analyze(self, df):
        if df is None or df.empty:
            return None

        df['ema50'] = calculate_ema(df, 50)
        df['ema200'] = calculate_ema(df, 200)
        df['rsi'] = calculate_rsi(df)
        df['adx'] = calculate_adx(df)

        df = df.dropna()

        if len(df) < 50:
            return None

        return df.iloc[-1]

    def generate_signal(self, symbol):
        df = self.data.get(symbol)
        row = self.analyze(df)

        if row is None:
            return "HOLD"

        # 🔥 SOLO OPERAR SI HAY TENDENCIA FUERTE
        if row['adx'] < 20:
            return "HOLD"

        trend_up = row['ema50'] > row['ema200']
        trend_down = row['ema50'] < row['ema200']

        if trend_up and row['rsi'] < 45:
            return "BUY"

        if trend_down and row['rsi'] > 55:
            return "SELL"

        return "HOLD"