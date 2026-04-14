import time
import hmac
import hashlib
import requests
import os
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

class Exchange:
    def __init__(self):
        self.api_key = os.getenv("BYBIT_API_KEY")
        self.api_secret = os.getenv("BYBIT_API_SECRET")
        self.base_url = os.getenv("BYBIT_BASE_URL", "https://api.bybit.com")
        self.symbol = os.getenv("SYMBOL", "BTCUSDT")
        self.qty = float(os.getenv("ORDER_QTY", "0.001"))

    def _timestamp(self):
        return str(int(time.time() * 1000))

    def _sign(self, payload: str) -> str:
        return hmac.new(
            self.api_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _headers(self, signature, timestamp):
        return {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": "5000",
            "Content-Type": "application/json"
        }

    def _post(self, endpoint, body: dict):
        url = f"{self.base_url}{endpoint}"
        timestamp = self._timestamp()

        body_str = str(body).replace("'", '"')  # JSON string simple
        payload = timestamp + self.api_key + "5000" + body_str
        signature = self._sign(payload)

        headers = self._headers(signature, timestamp)

        res = requests.post(url, headers=headers, data=body_str)
        data = res.json()

        if data.get("retCode") != 0:
            print("❌ Error Bybit:", data)
        else:
            print("✅ Orden enviada:", data["result"])

        return data

    def market_buy(self):
        body = {
            "category": "linear",
            "symbol": self.symbol,
            "side": "Buy",
            "orderType": "Market",
            "qty": str(self.qty),
            "timeInForce": "IOC"
        }
        return self._post("/v5/order/create", body)

    def market_sell(self):
        body = {
            "category": "linear",
            "symbol": self.symbol,
            "side": "Sell",
            "orderType": "Market",
            "qty": str(self.qty),
            "timeInForce": "IOC"
        }
        return self._post("/v5/order/create", body)