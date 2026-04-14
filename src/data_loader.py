import requests
import pandas as pd

class DataLoader:
    def __init__(self):
        self.base_url = "https://api.bybit.com"

    def get_data(self, symbol="BTCUSDT", interval="1", limit=500):
        """
        interval:
        1   = 1 minuto
        5   = 5 minutos
        15  = 15 minutos
        60  = 1 hora
        """

        url = f"{self.base_url}/v5/market/kline"

        params = {
            "category": "linear",   # USDT perpetual
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "result" not in data or "list" not in data["result"]:
            raise ValueError(f"❌ Error obteniendo datos Bybit: {data}")

        raw = data["result"]["list"]

        # Bybit devuelve en orden inverso (más reciente primero)
        raw.reverse()

        df = pd.DataFrame(raw, columns=[
            "time", "open", "high", "low", "close", "volume", "turnover"
        ])

        df["close"] = df["close"].astype(float)

        return df[["close"]]

    def get_multi_timeframe(self):
        data_1m = self.get_data(interval="1")
        data_5m = self.get_data(interval="5")
        return data_1m, data_5m