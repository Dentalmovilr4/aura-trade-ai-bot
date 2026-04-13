class RiskManager:
    def validate(self, signal):
        return signal in ["BUY", "SELL"]