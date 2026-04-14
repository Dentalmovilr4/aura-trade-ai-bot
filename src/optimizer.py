import random

class Optimizer:
    def __init__(self):
        self.best_params = {
            "rsi_buy": 45,
            "rsi_sell": 55
        }

    def tune(self):
        self.best_params["rsi_buy"] = random.randint(30, 50)
        self.best_params["rsi_sell"] = random.randint(50, 70)

        print("⚙️ Nuevos parámetros:", self.best_params)

        return self.best_params