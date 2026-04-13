import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SignalSender:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        requests.post(url, data={"chat_id": self.chat_id, "text": message})