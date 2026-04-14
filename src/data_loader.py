import requests
import pandas as pd
import time

class DataLoader:
    def __init__(self):
        self.base_url = "https://api.bybit.com"

    def get_data(self, symbol, interval="1"):
        url = f"{self.base_url}/v5/market/kline"

        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": interval,
            "limit": 200
        }

        try:
            res = requests.get(url, params=params, timeout=10).json()
            raw = res["result"]["list"]
            raw.reverse()

            df = pd.DataFrame(raw)

            df["close"] = df[4].astype(float)

            return df[["close"]]

        except Exception as e:
            print(f"⚠️ Error {symbol}: {e}")
            return pd.DataFrame()

    def get_multi_symbols(self):
        symbols = ["BTCUSDT", "BNBUSDT", "SOLUSDT"]

        data = {}

        for s in symbols:
            data[s] = self.get_data(s)
            time.sleep(0.2)

        return data