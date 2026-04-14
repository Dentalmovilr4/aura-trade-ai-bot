import time

from data_loader import DataLoader
from strategy import Strategy
from risk_management import RiskManager
from execution import Executor
from database import Database
from optimizer import Optimizer

loader = DataLoader()
strategy = Strategy()
risk = RiskManager()
executor = Executor()
db = Database()
optimizer = Optimizer()

print("🚀 Bot PRO en vivo...")

cycle = 0

while True:
    try:
        market_data = loader.get_multi_symbols()
        strategy.data = market_data

        for symbol, df in market_data.items():

            if df is None or df.empty:
                continue

            price = df.iloc[-1]["close"]
            signal = strategy.generate_signal(symbol)

            if signal != "HOLD" and risk.validate(signal):
                print(f"🚨 {symbol} {signal} @ {price}")

                db.insert(symbol, signal, price)
                executor.execute(symbol, signal, price)

        cycle += 1

        # 🔥 AUTO TUNING CADA 50 CICLOS
        if cycle >= 50:
            optimizer.tune()
            cycle = 0

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(60)