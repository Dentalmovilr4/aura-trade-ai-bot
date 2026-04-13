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
data = loader.get_data()

print("🧠 Entrenando modelo...")
model = trainer.train(data)
strategy.model = model

print("📊 Backtesting...")
bt = Backtester(strategy)
result = bt.run(data)
print(f"💰 Resultado: {result}")

print("🚀 Iniciando bot...")

while True:
    data = loader.get_data()
    strategy.data = data

    signal = strategy.generate_signal()

    if risk.validate(signal):
        msg = f"🚨 Señal: {signal}"
        print(msg)
        sender.send(msg)
        db.insert(signal)

    time.sleep(60)