from indicators import calculate_ema, calculate_rsi
from ai_model import AIModel

class Trainer:
    def __init__(self):
        self.model = AIModel()

    def prepare_data(self, df):
        df['ema'] = calculate_ema(df)
        df['rsi'] = calculate_rsi(df)
        df = df.dropna()

        X = df[['close','ema','rsi']]
        y = (df['close'].shift(-1) > df['close']).astype(int)

        return X[:-1], y[:-1]

    def train(self, df):
        X, y = self.prepare_data(df)
        self.model.train(X, y)
        self.model.save()
        return self.model