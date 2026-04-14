from indicators import calculate_ema, calculate_rsi
from ai_model import AIModel

class Trainer:
    def __init__(self):
        self.model = AIModel()

    def prepare_data(self, df):
        df['ema50'] = calculate_ema(df, 50)
        df['rsi'] = calculate_rsi(df)

        df = df.dropna()

        if df.empty:
            return [], []

        X = df[['close','ema50','rsi']]
        y = (df['close'].shift(-1) > df['close']).astype(int)

        X = X[:-1]
        y = y[:-1]

        return X, y

    def train(self, df):
        X, y = self.prepare_data(df)

        if len(X) == 0:
            raise ValueError("No hay datos suficientes")

        self.model.train(X, y)
        self.model.save()

        return self.model