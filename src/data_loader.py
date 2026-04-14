import requests
import pandas as pd
import time


class DataLoader:
    def __init__(self):
        self.base_url = "https://api.bybit.com"

    def safe_request(self, url, params, retries=3):
        for i in range(retries):
            try:
                response = requests.get(url, params=params, timeout=10)

                if response.status_code != 200:
                    print(f"⚠️ HTTP Error {response.status_code}")
                    time.sleep(1)
                    continue

                try:
                    return response.json()
                except Exception:
                    print("⚠️ Error decodificando JSON")
                    time.sleep(1)
                    continue

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Request error: {e}")
                time.sleep(1)

        return None

    def get_historical_data(self, symbol="BTCUSDT", interval="1", total=500):
        url = f"{self.base_url}/v5/market/kline"
        all_data = []

        while len(all_data) < total:
            params = {
                "category": "linear",
                "symbol": symbol,
                "interval": interval,
                "limit": 200
            }

            res = self.safe_request(url, params)

            if res is None:
                print("❌ No se pudo obtener datos")
                break

            if "result" not in res or "list" not in res["result"]:
                print(f"❌ Respuesta inválida: {res}")
                break

            data = res["result"]["list"]

            if not data:
                break

            all_data.extend(data)

            time.sleep(0.2)  # evita rate limit

            if len(data) < 200:
                break

        if not all_data:
            return pd.DataFrame()

        all_data.reverse()

        df = pd.DataFrame(all_data, columns=[
            "time","open","high","low","close","volume","turnover"
        ])

        df["close"] = df["close"].astype(float)

        return df[["close"]]

    def get_multi_timeframe(self):
        data_1m = self.get_historical_data(interval="1", total=500)
        data_5m = self.get_historical_data(interval="5", total=500)

        return data_1m, data_5m