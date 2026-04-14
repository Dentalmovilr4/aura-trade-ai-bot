import requests
import pandas as pd
import time

class DataLoader:
    def __init__(self):
        self.base_url = "https://api.bybit.com"

    def get_historical_data(self, symbol="BTCUSDT", interval="1", total=5000):
        url = f"{self.base_url}/v5/market/kline"
        all_data = []
        cursor = None

        while len(all_data) < total:
            params = {
                "category": "linear",
                "symbol": symbol,
                "interval": interval,
                "limit": 200,
            }

            if cursor:
                params["cursor"] = cursor

            res = requests.get(url, params=params).json()

            data = res["result"]["list"]
            cursor = res["result"].get("nextPageCursor")

            all_data.extend(data)

            if not cursor:
                break

            time.sleep(0.2)

        all_data.reverse()

        df = pd.DataFrame(all_data, columns=[
            "time","open","high","low","close","volume","turnover"
        ])

        df["close"] = df["close"].astype(float)

        return df[["close"]]

    def get_multi_timeframe(self):
        data_1m = self.get_historical_data(interval="1", total=1000)
        data_5m = self.get_historical_data(interval="5", total=1000)
        return data_1m, data_5m