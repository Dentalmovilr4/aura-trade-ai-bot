import time
from data_loader import DataLoader
from strategy import Strategy
from risk_management import RiskManager
from signal_sender import SignalSender
from database import Database
from execution import Executor
from ai.dataset import DatasetBuilder
from ai.model_lstm import LSTMModel

loader = DataLoader()
strategy = Strategy()
risk = RiskManager()
sender = SignalSender()
db = Database()
executor = Executor()

print("📡 Cargando datos...")
data_1m, data_5m = loader.get_multi_timeframe()

# 🧠 ENTRENAMIENTO IA
print("🧠 Entrenando IA Deep Learning...")
dataset = DatasetBuilder()
X, y = dataset.build(data_1m)

model = LSTMModel()
model.train(X, y)
model.save()

strategy.model = model

print("🚀 Bot en vivo...")

while True:
    data_1m, data_5m = loader.get_multi_timeframe()

    strategy.data_1m = data_1m
    strategy.data_5m = data_5m

    signal = strategy.generate_signal()

    if risk.validate(signal) and signal != "HOLD":
        msg = f"🚨 {signal}"
        print(msg)

        sender.send(msg)
        db.insert(signal)
        executor.execute(signal)

    time.sleep(60)