import requests
import pandas as pd
import time


class DataLoader:
    def __init__(self):
        self.base_url = "https://api.bybit.com"

    def safe_request(self, url, params):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"⚠️ HTTP {response.status_code}")
                return None

            data = response.json()

            if "result" not in data:
                print("⚠️ Respuesta inválida")
                return None

            return data

        except Exception as e:
            print(f"⚠️ Error request: {e}")
            return None

    def get_data(self, symbol="BTCUSDT", interval="1", limit=200):
        url = f"{self.base_url}/v5/market/kline"

        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        res = self.safe_request(url, params)

        if res is None:
            return pd.DataFrame()

        raw = res["result"].get("list", [])

        if not raw:
            return pd.DataFrame()

        raw.reverse()

        df = pd.DataFrame(raw)

        # 🔥 FORZAR columna close correctamente
        try:
            df["close"] = df[4].astype(float)
        except Exception:
            print("❌ Error creando columna close")
            return pd.DataFrame()

        return df[["close"]]

    def get_multi_timeframe(self):
        data_1m = self.get_data(interval="1")
        data_5m = self.get_data(interval="5")

        return data_1m, data_5m