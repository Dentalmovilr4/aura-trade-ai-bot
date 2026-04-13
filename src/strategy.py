from indicators import calculate_ema, calculate_rsi

class Strategy:
    def __init__(self):
        self.model = None
        self.data = None

    def generate_signal(self):
        self.data['ema'] = calculate_ema(self.data)
        self.data['rsi'] = calculate_rsi(self.data)

        row = self.data.iloc[-1]
        features = [row['close'], row['ema'], row['rsi']]

        if row['rsi'] < 30:
            return "BUY"
        elif row['rsi'] > 70:
            return "SELL"

        prediction = self.model.predict(features)
        return "BUY" if prediction == 1 else "SELL"