class RiskManager:
    def __init__(self):
        self.max_trades = 5
        self.current_trades = 0

    def validate(self, signal):
        if signal in ["BUY", "SELL"] and self.current_trades < self.max_trades:
            self.current_trades += 1
            return True
        return False