import time
from data_loader import DataLoader
from trainer import Trainer
from strategy import Strategy
from risk_management import RiskManager
from signal_sender import SignalSender
from database import Database
from backtesting import Backtester

loader = DataLoader()
trainer = Trainer()
strategy = Strategy()
risk = RiskManager()
sender = SignalSender()
db = Database()

print("📡 Cargando datos...")
data = loader.get_data(limit=500)

print("🧠 Entrenando modelo...")
try:
    model = trainer.train(data)
    strategy.model = model
except Exception as e:
    print(f"⚠️ Error entrenando modelo: {e}")
    exit()

print("📊 Backtesting...")
bt = Backtester(strategy)
results = bt.run(data)

print("💰 Balance:", results["balance"])
print("📊 Trades:", results["trades"])
print("🎯 Winrate:", results["winrate"], "%")

print("🚀 Bot en ejecución...")

while True:
    data = loader.get_data(limit=500)
    strategy.data = data

    signal = strategy.generate_signal()

    if risk.validate(signal) and signal != "HOLD":
        msg = f"🚨 {signal}"
        print(msg)
        sender.send(msg)
        db.insert(signal)

    time.sleep(60)