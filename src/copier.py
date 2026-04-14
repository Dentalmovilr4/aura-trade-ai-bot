from exchange import Exchange
from users import UserManager

class Copier:
    def __init__(self):
        self.users = UserManager()

    def copy_trade(self, signal, price):
        users = self.users.get_users()

        for user in users:
            _, name, key, secret, balance = user

            ex = Exchange(key, secret)

            qty = round((balance * 0.01) / price, 6)

            print(f"👤 {name} ejecutando {signal}")

            if signal == "BUY":
                ex.place_order("Buy", qty, price)

            elif signal == "SELL":
                ex.place_order("Sell", qty, price)