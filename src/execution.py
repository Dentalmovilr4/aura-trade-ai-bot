from exchange import Exchange

class Executor:
    def __init__(self):
        self.exchange = Exchange()

    def execute(self, signal):
        if signal == "BUY":
            print("🟢 Ejecutando BUY en Bybit")
            self.exchange.market_buy()

        elif signal == "SELL":
            print("🔴 Ejecutando SELL en Bybit")
            self.exchange.market_sell()