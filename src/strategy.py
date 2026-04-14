from indicators import calculate_ema, calculate_rsi

class Strategy:
    def __init__(self):
        self.data_1m = None
        self.data_5m = None
        self.model = None

    def analyze(self, df):
        df['ema50'] = calculate_ema(df, 50)
        df['ema200'] = calculate_ema(df, 200)
        df['rsi'] = calculate_rsi(df)

        df = df.dropna()
        if len(df) < 50:
            return None
if df is None or df.empty or 'close' not in df.columns:
    return None

        return df.iloc[-1]

    def generate_signal(self):
        row_1m = self.analyze(self.data_1m)
        row_5m = self.analyze(self.data_5m)

        if row_1m is None or row_5m is None:
            return "HOLD"

        trend_up = row_1m['ema50'] > row_1m['ema200'] and row_5m['ema50'] > row_5m['ema200']
        trend_down = row_1m['ema50'] < row_1m['ema200'] and row_5m['ema50'] < row_5m['ema200']

        if self.model:
            features = [
                row_1m['close'],
                row_1m['ema50'],
                row_1m['ema200'],
                row_1m['rsi']
            ]
            ai_decision = self.model.predict(features)
        else:
            ai_decision = None

        if trend_up and row_1m['rsi'] < 40:
            if ai_decision == 1:
                return "BUY"

        if trend_down and row_1m['rsi'] > 60:
            if ai_decision == 0:
                return "SELL"

        return "HOLD"