import time
import os

from data_loader import DataLoader
from strategy import Strategy
from risk_management import RiskManager
from signal_sender import SignalSender
from database import Database
from execution import Executor

from ai.dataset import DatasetBuilder
from ai.model_lstm import LSTMModel


# ========================
# CONFIG
# ========================
MODEL_PATH = "models/lstm_model.h5"
RETRAIN_INTERVAL = 100  # ciclos para reentrenar IA

# ========================
# INIT
# ========================
loader = DataLoader()
strategy = Strategy()
risk = RiskManager()
sender = SignalSender()
db = Database()
executor = Executor()

cycle_count = 0


# ========================
# ENTRENAR / CARGAR MODELO
# ========================
def load_or_train_model():
    model = LSTMModel()

    if os.path.exists(MODEL_PATH):
        print("📦 Cargando modelo existente...")
        model.load(MODEL_PATH)
        return model

    print("🧠 Entrenando modelo por primera vez...")

    data_1m, _ = loader.get_multi_timeframe()

    dataset = DatasetBuilder()
    X, y = dataset.build(data_1m)

    if len(X) == 0:
        raise ValueError("❌ No hay datos suficientes para entrenar IA")

    model.train(X, y)
    model.save(MODEL_PATH)

    print("✅ Modelo entrenado y guardado")

    return model


# ========================
# REENTRENAMIENTO
# ========================
def retrain_model():
    print("🔄 Reentrenando IA...")

    data_1m, _ = loader.get_multi_timeframe()

    dataset = DatasetBuilder()
    X, y = dataset.build(data_1m)

    if len(X) == 0:
        print("⚠️ No hay datos para reentrenar")
        return None

    model = LSTMModel()
    model.train(X, y)
    model.save(MODEL_PATH)

    print("✅ IA actualizada")

    return model


# ========================
# CARGAR MODELO
# ========================
strategy.model = load_or_train_model()


# ========================
# LOOP PRINCIPAL
# ========================
print("🚀 Bot en vivo...")

while True:
    try:
        data_1m, data_5m = loader.get_multi_timeframe()

        if data_1m is None or data_5m is None or len(data_1m) == 0:
            print("⚠️ Datos inválidos")
            time.sleep(60)
            continue

        strategy.data_1m = data_1m
        strategy.data_5m = data_5m

        price = data_1m.iloc[-1]["close"]

        signal = strategy.generate_signal()

        if signal != "HOLD" and risk.validate(signal):
            msg = f"🚨 {signal} @ {price}"
            print(msg)

            # guardar + enviar
            sender.send(msg)
            db.insert(signal)

            # ejecución real con precio
            executor.execute(signal, price)

        else:
            print(f"⏸️ HOLD @ {price}")

        # 🔁 REENTRENAMIENTO AUTOMÁTICO
        cycle_count += 1
        if cycle_count >= RETRAIN_INTERVAL:
            new_model = retrain_model()
            if new_model:
                strategy.model = new_model
            cycle_count = 0

    except Exception as e:
        print(f"❌ Error en ejecución: {e}")

    time.sleep(60)