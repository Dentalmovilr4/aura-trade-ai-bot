from strategy import Strategy
from copier import Copier

class Engine:
    def __init__(self):
        self.strategy = Strategy()
        self.copier = Copier()

    def run(self, data):
        self.strategy.data = data

        for symbol, df in data.items():
            if df.empty:
                continue

            price = df.iloc[-1]["close"]
            signal = self.strategy.generate_signal(symbol)

            if signal != "HOLD":
                print(f"🚨 {symbol} {signal}")
                self.copier.copy_trade(signal, price)