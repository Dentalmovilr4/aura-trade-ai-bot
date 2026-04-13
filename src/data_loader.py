import requests
import pandas as pd

class DataLoader:
    def get_data(self, symbol="BTCUSDT", interval="1m", limit=100):
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        data = requests.get(url, params=params).json()

        df = pd.DataFrame(data, columns=[
            "time","open","high","low","close","volume",
            "ct","qav","trades","tb","tq","ignore"
        ])

        df["close"] = df["close"].astype(float)
        return df[["close"]]