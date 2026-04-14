import time
import hmac
import hashlib
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Exchange:
    def __init__(self):
        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")
        self.base_url = os.getenv("BYBIT_BASE_URL")
        self.symbol = os.getenv("SYMBOL")

        self.tp = float(os.getenv("TAKE_PROFIT", 0.005))
        self.sl = float(os.getenv("STOP_LOSS", 0.003))

    def _timestamp(self):
        return str(int(time.time() * 1000))

    def _sign(self, payload):
        return hmac.new(
            self.api_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

    def _headers(self, sign, ts):
        return {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": sign,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": ts,
            "X-BAPI-RECV-WINDOW": "5000",
            "Content-Type": "application/json"
        }

    def place_order(self, side, qty, price):
        url = f"{self.base_url}/v5/order/create"
        ts = self._timestamp()

        if side == "Buy":
            tp_price = price * (1 + self.tp)
            sl_price = price * (1 - self.sl)
        else:
            tp_price = price * (1 - self.tp)
            sl_price = price * (1 + self.sl)

        body = {
            "category": "linear",
            "symbol": self.symbol,
            "side": side,
            "orderType": "Market",
            "qty": str(qty),
            "takeProfit": str(round(tp_price, 2)),
            "stopLoss": str(round(sl_price, 2)),
            "timeInForce": "IOC"
        }

        body_str = str(body).replace("'", '"')
        payload = ts + self.api_key + "5000" + body_str
        sign = self._sign(payload)

        headers = self._headers(sign, ts)

        res = requests.post(url, headers=headers, data=body_str)
        print(res.json())