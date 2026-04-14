class Backtester:
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self, data):
        balance = 1000
        position = None
        entry_price = 0

        trades = 0
        wins = 0

        for i in range(len(data)):
            self.strategy.data = data.iloc[:i+1]
            signal = self.strategy.generate_signal()

            price = data.iloc[i]["close"]

            # ENTRADA
            if signal == "BUY" and position is None:
                position = "LONG"
                entry_price = price
                trades += 1

            # SALIDA
            elif signal == "SELL" and position == "LONG":
                profit = price - entry_price
                balance += profit

                if profit > 0:
                    wins += 1

                position = None

        winrate = (wins / trades * 100) if trades > 0 else 0

        return {
            "balance": balance,
            "trades": trades,
            "winrate": winrate
        }