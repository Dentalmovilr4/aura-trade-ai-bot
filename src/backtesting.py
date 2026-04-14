class Backtester:
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self, data_1m, data_5m):
        balance = 1000
        position = None
        entry = 0

        trades = 0
        wins = 0

        for i in range(200, len(data_1m)):
            self.strategy.data_1m = data_1m.iloc[:i]
            self.strategy.data_5m = data_5m.iloc[:i]

            signal = self.strategy.generate_signal()
            price = data_1m.iloc[i]["close"]

            # ENTRADA
            if signal == "BUY" and position is None:
                position = "LONG"
                entry = price
                trades += 1

            # TP / SL
            if position == "LONG":
                profit = price - entry

                if profit > 5:  # take profit
                    balance += profit
                    wins += 1
                    position = None

                elif profit < -3:  # stop loss
                    balance += profit
                    position = None

        winrate = (wins / trades * 100) if trades else 0

        return {
            "balance": balance,
            "trades": trades,
            "winrate": winrate
        }