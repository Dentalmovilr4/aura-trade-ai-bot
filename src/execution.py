from exchange import Exchange
from risk_management import RiskManager

class Executor:
    def __init__(self):
        self.exchange = Exchange()
        self.risk = RiskManager()

    def execute(self, signal, price):
        qty = self.risk.calculate_position_size(price)

        if signal == "BUY":
            print(f"🟢 BUY {qty}")
            self.exchange.place_order("Buy", qty, price)

        elif signal == "SELL":
            print(f"🔴 SELL {qty}")
            self.exchange.place_order("Sell", qty, price)