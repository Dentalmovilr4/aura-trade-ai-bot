from exchange import Exchange
from risk_management import RiskManager

class Executor:
    def __init__(self):
        self.exchange = Exchange()
        self.risk = RiskManager()
        self.positions = {}

    def execute(self, symbol, signal, price):
        qty = self.risk.calculate_position_size(price)

        # ENTRADA
        if signal == "BUY" and symbol not in self.positions:
            print(f"🟢 BUY {symbol} {qty}")

            self.exchange.place_order("Buy", qty, price)

            self.positions[symbol] = {
                "entry": price,
                "qty": qty,
                "side": "LONG",
                "trail": price * 0.995
            }

        # TRAILING STOP
        if symbol in self.positions:
            pos = self.positions[symbol]

            # subir trailing si el precio sube
            if price > pos["entry"]:
                pos["trail"] = max(pos["trail"], price * 0.995)

            # salir si toca trailing
            if price <= pos["trail"]:
                print(f"🔴 TRAILING STOP {symbol}")

                self.exchange.place_order("Sell", pos["qty"], price)
                del self.positions[symbol]

        # SELL directo
        if signal == "SELL" and symbol not in self.positions:
            print(f"🔴 SELL {symbol} {qty}")
            self.exchange.place_order("Sell", qty, price)