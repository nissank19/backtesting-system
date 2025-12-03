class Backtester:
    def runback(self, df, initial=1000):
        self.cash = initial
        self.shares = 0
        self.value = []

        position = 0

        for _, row in df.iterrows():
            price = row["adj_close"]
            signal = row["signal"]

            if position == 0 and signal == 1:
                qty = self.cash / price
                self.shares = qty
                self.cash = 0
                position = 1

            elif position == 1 and signal == -1:
                self.cash = self.shares * price
                self.shares = 0
                position = 0

            v = self.cash + self.shares * price
            self.value.append(v)
