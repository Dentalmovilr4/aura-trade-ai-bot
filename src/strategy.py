from indicators import calculate_ema, calculate_rsi

class Strategy:
    def __init__(self):
        self.model = None
        self.data = None

    def generate_signal(self):
        df = self.data.copy()

        df['ema50'] = calculate_ema(df, 50)
        df['ema200'] = calculate_ema(df, 200)
        df['rsi'] = calculate_rsi(df)

        df = df.dropna()

        if len(df) < 10:
            return "HOLD"

        row = df.iloc[-1]

        trend_up = row['ema50'] > row['ema200']
        trend_down = row['ema50'] < row['ema200']

        # 🔥 FILTRO INTELIGENTE
        if trend_up and row['rsi'] < 35:
            return "BUY"

        if trend_down and row['rsi'] > 65:
            return "SELL"

        # IA solo si hay indecisión
        if self.model:
            features = [row['close'], row['ema50'], row['rsi']]
            prediction = self.model.predict(features)
            return "BUY" if prediction == 1 else "SELL"

        return "HOLD"