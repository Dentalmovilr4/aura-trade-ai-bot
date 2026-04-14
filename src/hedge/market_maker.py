class MarketMaker:
    def run(self, price):
        buy_price = price * 0.999
        sell_price = price * 1.001

        print(f"MM BUY {buy_price}")
        print(f"MM SELL {sell_price}")