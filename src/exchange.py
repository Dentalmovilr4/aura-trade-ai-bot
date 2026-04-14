import ccxt
import os
from dotenv import load_dotenv

load_dotenv()

class Exchange:
    def __init__(self):
        self.exchange = ccxt.binance({
            "apiKey": os.getenv("API_KEY"),
            "secret": os.getenv("API_SECRET"),
            "enableRateLimit": True
        })

    def market_buy(self, symbol="BTC/USDT", amount=0.001):
        try:
            order = self.exchange.create_market_buy_order(symbol, amount)
            print("🟢 BUY ejecutado:", order)
        except Exception as e:
            print("❌ Error BUY:", e)

    def market_sell(self, symbol="BTC/USDT", amount=0.001):
        try:
            order = self.exchange.create_market_sell_order(symbol, amount)
            print("🔴 SELL ejecutado:", order)
        except Exception as e:
            print("❌ Error SELL:", e)