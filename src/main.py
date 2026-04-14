import time

from data_loader import DataLoader
from strategy import Strategy
from risk_management import RiskManager
from execution import Executor

loader = DataLoader()
strategy = Strategy()
risk = RiskManager()
executor = Executor()

print("🚀 Multi Bot en vivo...")

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

                executor.execute(symbol, signal, price)

            else:
                print(f"⏸️ {symbol} HOLD")

    except Exception as e:
        print(f"❌ Error: {e}")

    time.sleep(60)