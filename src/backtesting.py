class Backtester:
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self, data):
        balance = 1000
        position = None

        for i in range(len(data)):
            self.strategy.data = data.iloc[:i+1]
            signal = self.strategy.generate_signal()
            price = data.iloc[i]["close"]

            if signal == "BUY" and position is None:
                position = price
            elif signal == "SELL" and position:
                balance += price - position
                position = None

        return balance