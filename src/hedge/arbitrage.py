class Arbitrage:
    def check(self, price_a, price_b):
        if abs(price_a - price_b) > 10:
            print("💰 Oportunidad arbitraje")