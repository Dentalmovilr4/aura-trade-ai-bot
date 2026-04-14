import os
from dotenv import load_dotenv

load_dotenv()

class RiskManager:
    def __init__(self):
        self.risk_percent = float(os.getenv("RISK_PERCENT", 0.01))
        self.balance = float(os.getenv("ACCOUNT_BALANCE", 1000))

    def calculate_position_size(self, price):
        risk_amount = self.balance * self.risk_percent
        qty = risk_amount / price
        return round(qty, 6)

    def validate(self, signal):
        return signal in ["BUY", "SELL"]