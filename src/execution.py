from exchange import Exchange

class Executor:
    def __init__(self):
        self.exchange = Exchange()

    def execute(self, signal):
        if signal == "BUY":
            self.exchange.market_buy()
        elif signal == "SELL":
            self.exchange.market_sell()