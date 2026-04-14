import requests
import time
import hmac
import hashlib
import os

class Exchange:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key or os.getenv("MASTER_API_KEY")
        self.api_secret = api_secret or os.getenv("MASTER_API_SECRET")
        self.base_url = "https://api.bybit.com"
        self.symbol = "BTCUSDT"

    def _sign(self, payload):
        return hmac.new(
            self.api_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

    def place_order(self, side, qty, price):
        ts = str(int(time.time() * 1000))

        body = {
            "category": "linear",
            "symbol": self.symbol,
            "side": side,
            "orderType": "Market",
            "qty": str(qty)
        }

        body_str = str(body).replace("'", '"')
        payload = ts + self.api_key + "5000" + body_str
        sign = self._sign(payload)

        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": sign,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": ts,
            "X-BAPI-RECV-WINDOW": "5000",
            "Content-Type": "application/json"
        }

        res = requests.post(f"{self.base_url}/v5/order/create", headers=headers, data=body_str)

        print(res.json())